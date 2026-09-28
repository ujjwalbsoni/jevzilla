"""
IT/DevOps — Elevated access request review.

Scenario: An employee requests elevated system access. JEV flags whether it's a standard request, routes approval, and scores the access-risk level for security logging.

Run:
    set OPENROUTER_API_KEY=your-key
    python access_request_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'requestor': 'Marketing contractor, 3-month engagement', 'request': "Requesting production database read/write access to 'help debug a reporting issue,' where a read-only reporting replica already exists for this purpose."}

QUESTIONS = {
    "unusual_request": {
        "type": "noul",
        "instructions": "Is this request unusual given the requestor's role and the stated purpose (a read-only replica already serves this purpose)?",
        "criteria": {"true": 'A contractor requesting write access to production for a task a read-only replica already covers is a notable mismatch.', "false": "Request matches the requestor's role and stated need."},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'What approval path should this request take?',
        "criteria": {'auto_approve_standard': 'Matches standard role-based access; approve.', 'manager_and_security_review': 'Mismatch needs manager and security sign-off.', 'deny_offer_alternative': 'Should be denied and redirected to the read-only replica.'},
    },
    "access_risk": {
        "type": "score",
        "instructions": 'How should this be logged for security risk tracking?',
        "criteria": ['Low', 'Moderate', 'High', 'Critical - production write access'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("IT/DevOps — Elevated access request review", 'Access request: production DB read/write', res.answers)
