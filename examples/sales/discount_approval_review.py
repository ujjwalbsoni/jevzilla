"""
Sales — Discount request approval review.

Scenario: A rep requests an end-of-quarter discount exception. JEV flags whether it's within policy, routes approval, and scores deal urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python discount_approval_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'deal': '$40,000 ACV, currently at 15% discount, rep requesting 28%', 'rep_note': 'Prospect says budget was cut and they need to close by end of month or the project is dead for the fiscal year.'}

QUESTIONS = {
    "outside_policy": {
        "type": "noul",
        "instructions": 'Is this discount request outside standard end-of-quarter policy thresholds?',
        "criteria": {"true": 'A jump to 28% exceeds typical standard discount authority.', "false": 'Requested discount is within standard policy.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'Who should approve this discount?',
        "criteria": {'auto_approved': 'Within policy; system can approve automatically.', 'sales_director_approval': 'Above standard threshold; needs director sign-off.', 'vp_approval_required': 'Deep discount; needs VP-level approval.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How time-sensitive is this approval given the stated deadline?',
        "criteria": ['Low', 'This week', 'This month', 'Deal dies if delayed'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Sales — Discount request approval review", 'Discount exception request, 15% to 28%', res.answers)
