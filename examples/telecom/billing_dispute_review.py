"""
Telecom — Telecom billing dispute review.

Scenario: A customer disputes their monthly bill. JEV flags whether it's likely a billing error, routes it, and scores resolution urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python billing_dispute_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'dispute': "Customer's bill shows an international roaming charge of $340 for a trip they say they never took, and they've disputed the same type of charge once before 8 months ago (which was found to be an error)."}

QUESTIONS = {
    "likely_billing_error": {
        "type": "noul",
        "instructions": "Given this account's history, does this dispute likely represent another billing error rather than a legitimate charge?",
        "criteria": {"true": 'A prior confirmed error of the same type raises the likelihood this is a repeat system issue.', "false": 'No prior pattern suggests this needs standard verification first.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'How should this be routed?',
        "criteria": {'standard_dispute_review': 'Verify normally against usage records.', 'expedited_billing_investigation': 'Prior confirmed error of the same type warrants expedited investigation.', 'systemic_issue_escalation': 'A repeat error type may indicate a broader system issue worth escalating.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently should this be resolved?',
        "criteria": ['Low', 'Normal', 'High', 'Urgent - repeat error pattern'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Telecom — Telecom billing dispute review", 'Billing dispute: roaming charge', res.answers)
