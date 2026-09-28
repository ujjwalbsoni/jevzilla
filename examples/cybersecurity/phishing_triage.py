"""
Cybersecurity — Reported phishing email triage.

Scenario: An employee reports a suspicious email. JEV flags whether it's likely a genuine threat, routes the response, and scores urgency for the security team.

Run:
    set OPENROUTER_API_KEY=your-key
    python phishing_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'reported_email': "Email appears to be from IT support, asks the employee to 'verify their password' via a link to a domain that isn't the company's, with urgent language about account suspension."}

QUESTIONS = {
    "likely_phishing": {
        "type": "noul",
        "instructions": 'Does this email show classic phishing indicators (credential request, off-domain link, urgency language)?',
        "criteria": {"true": 'Combination of a credential request, mismatched domain, and urgency language is a textbook phishing pattern.', "false": 'Email does not show typical phishing indicators.'},
    },
    "response_route": {
        "type": "choice",
        "instructions": 'What should the security team do?',
        "criteria": {'log_and_close': 'Low confidence; log for awareness only.', 'block_and_scan_org_wide': 'Confirmed pattern; block the domain and scan for other recipients.', 'incident_response_activation': 'Should check for evidence of prior clicks before treating as contained.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently should this be handled?',
        "criteria": ['Low', 'Today', 'Immediate', 'Critical - possible active compromise'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Cybersecurity — Reported phishing email triage", 'Employee-reported suspicious email', res.answers)
