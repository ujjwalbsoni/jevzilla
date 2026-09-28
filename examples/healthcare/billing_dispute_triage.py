"""
Healthcare Ops — Medical billing dispute triage.

Scenario: A patient disputes a charge on their statement. JEV flags whether it looks like a billing error, routes it to the right team, and scores resolution urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python billing_dispute_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'dispute': "Patient states they were charged for an office visit and a separate 'consultation' fee on the same day for what they describe as a single 15-minute appointment.", 'account_note': 'No prior disputes on this account.'}

QUESTIONS = {
    "likely_billing_error": {
        "type": "noul",
        "instructions": 'Does this dispute describe a pattern consistent with a common billing error (e.g. duplicate or miscoded charges for one visit)?',
        "criteria": {"true": 'Two charges for what appears to be a single encounter is a recognized coding-error pattern.', "false": 'Dispute does not clearly indicate an error pattern.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Which team should handle this dispute?',
        "criteria": {'billing_coding_review': 'Likely coding/duplicate charge error.', 'patient_financial_services': 'Needs direct patient communication and account adjustment.', 'compliance_review': 'Pattern suggests a broader coding practice to review.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently should this dispute be resolved?',
        "criteria": ['Low', 'Normal', 'High - going to collections soon', 'Urgent - already in collections'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Healthcare Ops — Medical billing dispute triage", 'Billing dispute, single-visit double charge', res.answers)
