"""
Cybersecurity — User access anomaly review.

Scenario: A SIEM alert flags unusual account activity. JEV flags whether it looks like account compromise, routes investigation, and scores response urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python access_anomaly.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'alert': "User account logged in from two countries 4,000 miles apart within a 20-minute window ('impossible travel'), followed by an attempt to download the full customer contact export."}

QUESTIONS = {
    "likely_compromise": {
        "type": "noul",
        "instructions": 'Does this activity pattern indicate likely account compromise rather than normal user behavior?',
        "criteria": {"true": 'Impossible travel combined with a bulk data export attempt is a well-established compromise indicator pair.', "false": 'Activity is explainable by normal user behavior (e.g. VPN use).'},
    },
    "investigation_route": {
        "type": "choice",
        "instructions": 'What should happen next?',
        "criteria": {'monitor_only': 'Low confidence; monitor for now.', 'disable_account_and_investigate': 'Pattern is strong enough to disable the account pending investigation.', 'full_incident_response': 'Bulk export of customer data may already indicate a breach in progress.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently should this be handled?',
        "criteria": ['Low', 'Today', 'Immediate', 'Critical - active breach possible'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Cybersecurity — User access anomaly review", 'SIEM alert: impossible travel + bulk export attempt', res.answers)
