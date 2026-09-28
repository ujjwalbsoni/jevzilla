"""
Legal — Litigation hold trigger review.

Scenario: A business team reports a customer complaint that mentions legal action. JEV flags whether a litigation hold should be triggered, routes notification, and scores urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python litigation_hold_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'complaint_note': "Customer's email states: 'If this isn't resolved I'll be speaking to my attorney about your handling of my data.' No formal legal notice received yet."}

QUESTIONS = {
    "trigger_hold": {
        "type": "noul",
        "instructions": 'Does this complaint create a reasonable anticipation of litigation that should trigger a litigation hold on related records?',
        "criteria": {"true": 'An explicit mention of consulting an attorney about a specific dispute is a recognized hold trigger.', "false": 'Complaint is a general grievance without a credible litigation signal.'},
    },
    "notify": {
        "type": "choice",
        "instructions": 'Who needs to be notified first?',
        "criteria": {'customer_support_lead': 'Low signal; handle as standard escalation.', 'legal_department': 'Credible signal; legal should assess a hold.', 'legal_and_it_records': 'Hold should likely be issued; IT needs to preserve records now.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently does this need to be acted on?',
        "criteria": ['Low', 'This week', 'Today', 'Immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Legal — Litigation hold trigger review", 'Customer complaint mentioning potential legal action', res.answers)
