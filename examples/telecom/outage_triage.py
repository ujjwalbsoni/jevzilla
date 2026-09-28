"""
Telecom — Network outage report triage.

Scenario: Multiple customer reports come in about service issues in one area. JEV flags whether it looks like an outage, routes it to the right team, and scores response priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python outage_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'reports_summary': "14 customer complaints in the last 30 minutes, all from the same city zip code, all reporting 'no signal' or 'can't make calls.'"}

QUESTIONS = {
    "likely_outage": {
        "type": "noul",
        "instructions": 'Does this pattern indicate a likely network outage rather than isolated individual device issues?',
        "criteria": {"true": 'A geographic cluster of similar complaints in a short window is a recognized outage pattern.', "false": 'Reports do not show a clear geographic or timing cluster.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Which team should this be routed to?',
        "criteria": {'standard_device_troubleshooting': 'Isolated issue; standard troubleshooting.', 'network_operations_center': 'Pattern warrants NOC investigation of local infrastructure.', 'public_outage_notification': 'If confirmed, needs a public status update to reduce support volume.'},
    },
    "priority": {
        "type": "score",
        "instructions": 'How should this be prioritized?',
        "criteria": ['Low', 'Normal', 'High', 'Critical - active outage'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Telecom — Network outage report triage", 'Cluster of service complaints, single zip code', res.answers)
