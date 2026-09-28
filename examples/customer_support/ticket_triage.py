"""
Customer Support — Support ticket triage.

Scenario: A support ticket comes in through the help desk. JEV flags whether it's a service outage, routes it to the right team, and scores priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python ticket_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'ticket': 'Customer reports they cannot log into their account at all, getting a generic error, and says 3 coworkers at their company are reporting the same thing right now.'}

QUESTIONS = {
    "possible_outage": {
        "type": "noul",
        "instructions": 'Does this ticket describe a pattern consistent with a broader service issue rather than an isolated account problem?',
        "criteria": {"true": 'Multiple users at the same company hitting the same error simultaneously suggests a systemic issue.', "false": 'Pattern is consistent with an isolated, single-account issue.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Which team should this be routed to?',
        "criteria": {'standard_account_support': 'Isolated issue; standard support can handle it.', 'engineering_escalation': 'Pattern suggests a possible service-wide issue; escalate to engineering.', 'status_page_and_mass_notification': 'If confirmed as an outage, needs status page update and customer notification.'},
    },
    "priority": {
        "type": "score",
        "instructions": 'How should this ticket be prioritized?',
        "criteria": ['Low', 'Normal', 'High', 'Critical - possible outage'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Customer Support — Support ticket triage", 'Support ticket: login failure, multiple users', res.answers)
