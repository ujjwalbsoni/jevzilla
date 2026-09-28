"""
Cybersecurity — Security incident response triage.

Scenario: A potential security incident is reported by a system admin. JEV flags severity, routes response ownership, and scores containment urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python incident_response_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'report': 'Admin notices unexpected outbound network traffic from a database server to an unfamiliar external IP address, occurring nightly for the past 3 days at the same time.'}

QUESTIONS = {
    "likely_active_threat": {
        "type": "noul",
        "instructions": 'Does this pattern indicate a likely active security threat (e.g. data exfiltration) rather than benign activity?',
        "criteria": {"true": 'Regular, unexplained outbound traffic to an external IP from a database server is a recognized exfiltration pattern.', "false": 'Pattern is likely explainable by legitimate scheduled activity.'},
    },
    "response_owner": {
        "type": "choice",
        "instructions": 'Who should own the response?',
        "criteria": {'system_admin_investigation': 'Low confidence; admin can investigate first.', 'security_operations_team': 'Pattern warrants SOC investigation.', 'incident_commander_activation': 'Pattern is strong enough to activate formal incident response.'},
    },
    "containment_urgency": {
        "type": "score",
        "instructions": 'How urgently should this traffic be contained/blocked?',
        "criteria": ['Low', 'Investigate first', 'Contain today', 'Immediate - isolate now'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Cybersecurity — Security incident response triage", 'Reported anomaly: unusual outbound traffic from DB server', res.answers)
