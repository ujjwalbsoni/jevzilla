"""Government: FOIA Request Priority Scoring

Gate: Does request warrant expedited processing?
Route: Which process track? (Standard, Expedited, Complex hold)
Priority: What's the processing burden?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "request_type": "Meeting minutes from environmental board",
    "scope": "Single meeting, ~50 pages estimated",
    "classification": "Unclassified, minimal redaction expected",
    "requestor_type": "Media outlet, public interest journalism",
    "deadline_claim": "No claimed urgency",
    "backlog": "Current processing time 30 days",
    "availability": "Documents already compiled, readily accessible",
}

QUESTIONS = {
    "expedited": noul("Does request warrant expedited processing?"),
    "track": choice("Process track?", {
        "standard": "Standard processing timeline",
        "expedited": "Expedited processing",
        "complex": "Complex - extended processing time",
    }),
    "burden": score("Processing burden?", ["Low", "Moderate", "High", "Substantial"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
