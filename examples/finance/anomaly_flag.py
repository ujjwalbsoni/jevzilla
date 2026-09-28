"""
Finance — Financial report anomaly flag.

Scenario: A monthly close review flags an unusual account movement. JEV decides whether it needs controller investigation, routes it to the right team, and scores materiality.

Run:
    set OPENROUTER_API_KEY=your-key
    python anomaly_flag.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'account': 'Accrued liabilities - vendor rebates', 'note': 'Balance increased 5x month-over-month with no corresponding change in vendor contract terms or purchase volume on record.'}

QUESTIONS = {
    "needs_investigation": {
        "type": "noul",
        "instructions": 'Does this account movement look unusual enough to warrant controller-level investigation before close is finalized?',
        "criteria": {"true": 'A large balance swing with no corresponding business driver is a recognized red flag.', "false": 'Movement has a clear, documented business explanation.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Who should investigate this anomaly first?',
        "criteria": {'staff_accountant_reconciliation': 'Likely a reconciliation or entry error.', 'controller_review': 'Needs controller-level judgment on treatment.', 'internal_audit': 'Pattern is unusual enough to warrant an audit look.'},
    },
    "materiality": {
        "type": "score",
        "instructions": 'How material is this anomaly to the financial statements?',
        "criteria": ['Immaterial', 'Minor', 'Material - needs disclosure review', 'Significant - may restate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Finance — Financial report anomaly flag", 'Account anomaly: accrued vendor rebates', res.answers)
