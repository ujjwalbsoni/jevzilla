"""
Manufacturing — Production change request review.

Scenario: Engineering submits a change request to modify a manufacturing process. JEV flags regulatory/customer notification needs, routes approval, and scores implementation risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python change_request_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'process': 'Injection molding cycle time, connector housing line', 'change_request': 'Reduce cycle time by 8% by lowering cooling stage duration. Initial trial runs show no visible defects on a 50-unit sample.'}

QUESTIONS = {
    "notification_required": {
        "type": "noul",
        "instructions": "Does this process change plausibly require customer or regulatory notification (e.g. affects a qualified/PPAP'd process)?",
        "criteria": {"true": 'Change affects cooling parameters on a process likely under customer part-approval controls.', "false": 'Change is internal-only with no customer-facing process impact.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'What approval path does this change need?',
        "criteria": {'engineering_signoff_only': 'Low-risk internal optimization.', 'quality_and_customer_signoff': 'Affects a qualified process; needs formal change control.', 'reject_pending_more_data': 'Sample size and validation are insufficient to approve yet.'},
    },
    "implementation_risk": {
        "type": "score",
        "instructions": 'How much risk does implementing this change carry?',
        "criteria": ['Low', 'Moderate', 'High', 'Requires full requalification'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Manufacturing — Production change request review", 'Change request: connector housing cycle time', res.answers)
