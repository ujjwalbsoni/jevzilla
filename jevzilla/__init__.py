"""
JEVzilla - a tiny, fearless client for JEV.

You write payloads exactly like the JEV API docs (https://jevplayground.com/jev-api):

    {"state": "...", "questions": {"urgent": {"type": "noul", "instructions": "..."}}}

Question types follow the docs: noul (alias: boolean), choice, score.
Before sending, JEVzilla translates the payload to the wire format the
playground endpoint (/api/evaluate) expects:

    noul, no criteria   -> {"instructions", "type": "boolean"}
    noul, with criteria -> {"instructions", "type": "choice", "criteria": {"true": ..., "false": ...}}
    choice              -> {"instructions", "type": "choice", "criteria": {label: description}}
    score               -> {"instructions", "type": "score",  "criteria": [level, ...]}

    state (str / dict / list) -> always a string on the playground wire.

backend="typesafe" instead sends the docs format as-is to the official
endpoint (POST https://api.typesafe.ai/v1/systemone) with a Bearer API key.
"""
from __future__ import annotations

import copy
import json
import os
import random
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Sequence, Tuple

import requests

__all__ = [
    "JEVzilla", "JEVResponse", "JEVError", "JEVValidationError", "JEVHTTPError",
    "to_playground_payload", "to_typesafe_payload",
    "noul", "choice", "score", "Noul", "Choice", "Score",
]
__version__ = "0.3.0"

PLAYGROUND_URL = "https://jevplayground.com/api/evaluate"
TYPESAFE_URL = "https://api.typesafe.ai/v1/systemone"
OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"
_ORIGIN = "https://jevplayground.com"
_RETRY_STATUSES = {429, 502, 503, 504, 529}

# docs-style type names accepted on input -> canonical
_TYPE_ALIASES = {
    "noul": "noul", "boolean": "noul", "bool": "noul",
    "choice": "choice",
    "score": "score",
}


class JEVError(Exception):
    """Base error for JEVzilla."""


class JEVValidationError(JEVError, ValueError):
    """Payload could not be translated into a valid JEV request."""


class JEVHTTPError(JEVError):
    def __init__(self, status_code: int, body: str):
        super().__init__(f"JEV API returned HTTP {status_code}: {body[:300]}")
        self.status_code = status_code
        self.body = body


# ------------------------------------------------- docs-style builders
def noul(instructions: str, criteria: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    q: Dict[str, Any] = {"type": "noul", "instructions": instructions}
    if criteria is not None:
        q["criteria"] = criteria
    return q


def choice(instructions: str, criteria: Dict[str, str]) -> Dict[str, Any]:
    return {"type": "choice", "instructions": instructions, "criteria": criteria}


def score(instructions: str, criteria: Sequence[str]) -> Dict[str, Any]:
    return {"type": "score", "instructions": instructions, "criteria": list(criteria)}


Noul, Choice, Score = noul, choice, score  # mirror the SDK's capitalized names


# ------------------------------------------------------ parsing (docs style)
def _parse_question(name: str, q: Any) -> Tuple[str, str, Any]:
    """Validate one docs-style question -> (canonical type, instructions, criteria)."""
    where = f"questions[{name!r}]"
    if not isinstance(q, dict):
        raise JEVValidationError(f"{where} must be an object")

    instructions = q.get("instructions")
    if not isinstance(instructions, str) or not instructions.strip():
        raise JEVValidationError(f"{where}.instructions must be a non-empty string")

    raw = q.get("type")
    qtype = _TYPE_ALIASES.get(str(raw).strip().lower()) if raw is not None else None
    if qtype is None:
        raise JEVValidationError(f"{where}.type must be one of noul | boolean | choice | score (got {raw!r})")

    criteria = q.get("criteria")

    if qtype == "noul":
        if criteria in (None, {}, []):
            return qtype, instructions, None
        if not isinstance(criteria, dict):
            raise JEVValidationError(f"{where}.criteria for 'noul' must be an object like {{'true': ..., 'false': ...}}")
        return qtype, instructions, {str(k): str(v) for k, v in criteria.items()}

    if qtype == "choice":
        if isinstance(criteria, dict) and criteria:
            return qtype, instructions, {str(k): str(v) for k, v in criteria.items()}
        if isinstance(criteria, (list, tuple)) and criteria:   # lenient: ["a","b"] -> {"a":"a","b":"b"}
            return qtype, instructions, {str(c): str(c) for c in criteria}
        raise JEVValidationError(f"{where}.criteria must be a non-empty object for 'choice'")

    # score
    if isinstance(criteria, (list, tuple)) and criteria:
        return qtype, instructions, [str(c) for c in criteria]
    raise JEVValidationError(f"{where}.criteria must be a non-empty list of levels for 'score'")


def _parse_payload(payload: Dict[str, Any]) -> Tuple[Any, Dict[str, Tuple[str, str, Any]]]:
    if not isinstance(payload, dict):
        raise JEVValidationError("payload must be a dict")
    state = payload.get("state")
    if state is None or (isinstance(state, str) and not state.strip()) or state in ({}, []):
        raise JEVValidationError("payload.state must be a non-empty string, object or array")
    if not isinstance(state, (str, dict, list)):
        raise JEVValidationError("payload.state must be a string, object or array")
    questions = payload.get("questions")
    if not isinstance(questions, dict) or not questions:
        raise JEVValidationError("payload.questions must be a non-empty dict")
    parsed = {str(n): _parse_question(str(n), copy.deepcopy(q)) for n, q in questions.items()}
    return state, parsed


# ------------------------------------------------------------- translators
def to_playground_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """docs-style payload -> the exact shape /api/evaluate expects."""
    state, parsed = _parse_payload(payload)
    if not isinstance(state, str):
        state = json.dumps(state, ensure_ascii=False, indent=2)

    questions: Dict[str, Any] = {}
    for name, (qtype, instructions, criteria) in parsed.items():
        if qtype == "noul":
            if criteria is None:
                questions[name] = {"instructions": instructions, "type": "boolean"}
            else:  # true/false criteria -> the "choice" shape from the working example
                questions[name] = {"instructions": instructions, "type": "choice", "criteria": criteria}
        else:  # choice / score pass through
            questions[name] = {"instructions": instructions, "type": qtype, "criteria": criteria}
    return {"state": state, "questions": questions}


def to_typesafe_payload(payload: Dict[str, Any], model: str = "jev-latest") -> Dict[str, Any]:
    """docs-style payload -> validated body for the official /v1/systemone endpoint."""
    state, parsed = _parse_payload(payload)
    questions: Dict[str, Any] = {}
    for name, (qtype, instructions, criteria) in parsed.items():
        q = {"type": qtype, "instructions": instructions}
        if criteria is not None:
            q["criteria"] = criteria
        questions[name] = q
    return {"model": model, "state": state, "questions": questions}


# ------------------------------------------------------------------ client
@dataclass
class JEVResponse:
    status_code: int
    text: str
    data: Any = None
    request: Dict[str, Any] = field(default_factory=dict)  # the body actually sent

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300

    @property
    def answers(self) -> Any:
        """`data["answers"]` when present (official shape), else the raw parsed body."""
        if isinstance(self.data, dict) and "answers" in self.data:
            return self.data["answers"]
        return self.data

    def __getitem__(self, key):
        return self.answers[key]

    # ---- convenience readers for the real answer shapes ----
    def noul(self, key: str, threshold: float = 0.5) -> bool:
        """True/False reading of a noul answer (backend returns a 0-1 probability)."""
        return self.answers[key]["noul"] >= threshold

    def choice(self, key: str) -> str:
        return self.answers[key]["choice"]

    def score_label(self, key: str) -> str:
        a = self.answers[key]
        return a["legend"][str(round(a["score"]))]


class JEVzilla:
    """
    >>> jev = JEVzilla()                          # playground endpoint
    >>> jev.evaluate({
    ...     "state": "The customer says their production service is down.",
    ...     "questions": {"urgent": {"type": "noul", "instructions": "Is this request urgent?"}},
    ... })

    >>> jev = JEVzilla(backend="typesafe")        # official API, reads TYPESAFE_API_KEY
    """

    def __init__(self, backend: str = "playground", api_key: Optional[str] = None,
                 model: str = "jev-latest", url: Optional[str] = None, timeout: float = 30.0,
                 retries: int = 4, backoff: float = 1.0, max_backoff: float = 30.0,
                 session: Optional[requests.Session] = None,
                 extra_headers: Optional[Dict[str, str]] = None):
        if backend not in ("playground", "typesafe", "openrouter"):
            raise ValueError("backend must be 'playground', 'typesafe' or 'openrouter'")
        self.backend, self.model, self.timeout = backend, model, timeout
        self.retries, self.backoff, self.max_backoff = max(0, retries), backoff, max_backoff
        self.session = session or requests.Session()
        if backend == "playground":
            self.url = url or PLAYGROUND_URL
            self.headers = {"Content-Type": "application/json", "Origin": _ORIGIN, "Referer": _ORIGIN + "/"}
        elif backend == "typesafe":
            key = api_key or os.environ.get("TYPESAFE_API_KEY")
            if not key:
                raise JEVError("backend='typesafe' needs api_key= or the TYPESAFE_API_KEY env var")
            self.url = url or TYPESAFE_URL
            self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
        else:  # openrouter
            key = api_key or os.environ.get("OPENROUTER_API_KEY")
            if not key:
                raise JEVError("backend='openrouter' needs api_key= or the OPENROUTER_API_KEY env var")
            self.url = url or OPENROUTER_URL
            self.model = model if model != "jev-latest" else "typesafe/jev-1.13"
            self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
        self.headers.update(extra_headers or {})

    def build(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """The exact body that would be sent, without sending it."""
        if self.backend == "playground":
            return to_playground_payload(payload)
        return to_typesafe_payload(payload, self.model)

    def _sleep_time(self, attempt: int, resp: Optional[requests.Response]) -> float:
        if resp is not None:
            ra = resp.headers.get("Retry-After")
            if ra and ra.replace(".", "", 1).isdigit():
                return min(float(ra), self.max_backoff)
        return min(self.backoff * (2 ** attempt), self.max_backoff) * random.uniform(0.75, 1.25)

    def evaluate(self, payload: Dict[str, Any], raise_for_status: bool = True) -> JEVResponse:
        """POST the translated payload. Retries transient failures (429/502/503/504/529,
        timeouts, connection errors) with exponential backoff; 4xx like 401/422 are not retried."""
        body = self.build(payload)
        r: Optional[requests.Response] = None
        for attempt in range(self.retries + 1):
            try:
                r = self.session.post(self.url, json=body, headers=self.headers, timeout=self.timeout)
            except (requests.ConnectionError, requests.Timeout):
                if attempt == self.retries:
                    raise
                time.sleep(self._sleep_time(attempt, None))
                continue
            if r.status_code in _RETRY_STATUSES and attempt < self.retries:
                time.sleep(self._sleep_time(attempt, r))
                continue
            break
        try:
            data = r.json()
        except ValueError:
            data = None
        res = JEVResponse(r.status_code, r.text, data, body)
        if raise_for_status and not res.ok:
            raise JEVHTTPError(r.status_code, r.text)
        return res

    # single-question shortcuts (answer key defaults to "decision")
    def ask_noul(self, state, instructions, criteria=None, key="decision", **kw) -> JEVResponse:
        return self.evaluate({"state": state, "questions": {key: noul(instructions, criteria)}}, **kw)

    def ask_choice(self, state, instructions, criteria, key="decision", **kw) -> JEVResponse:
        return self.evaluate({"state": state, "questions": {key: choice(instructions, criteria)}}, **kw)

    def ask_score(self, state, instructions, levels, key="decision", **kw) -> JEVResponse:
        return self.evaluate({"state": state, "questions": {key: score(instructions, levels)}}, **kw)
