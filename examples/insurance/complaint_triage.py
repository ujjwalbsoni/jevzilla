"""
Insurance — Policyholder complaint triage.

Scenario: A policyholder complaint comes in through the call center. JEV flags whether it's a regulatory-complaint risk, routes it to the right team, and scores resolution urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python complaint_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'complaint': 'Policyholder states their claim was denied without a clear explanation and they intend to file a complaint with the state insurance commissioner if not resolved this week.'}

QUESTIONS = {
    "regulatory_risk": {
        "type": "noul",
        "instructions": 'Does this complaint indicate a credible risk of escalation to a state regulator?',
        "criteria": {"true": 'An explicit mention of filing with the insurance commissioner is a recognized regulatory-escalation signal.', "false": 'Complaint is a standard service issue without a regulatory escalation signal.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Which team should handle this complaint?',
        "criteria": {'standard_customer_service': 'Low risk; standard service resolution.', 'claims_review_team': 'Needs a documented claims review with clear denial explanation.', 'compliance_and_legal': 'Regulatory risk warrants compliance and legal involvement.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently does this need to be resolved?',
        "criteria": ['Low', 'This week', 'Before regulator deadline', 'Immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Insurance — Policyholder complaint triage", 'Policyholder complaint re: denied claim', res.answers)
