"""
Banking — AML alert triage.

Scenario: An anti-money-laundering monitoring system generates an alert. JEV flags whether it needs a SAR (suspicious activity report) review, routes it, and scores investigation priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python aml_alert_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'alert': 'Account received 6 deposits just under the $10,000 reporting threshold within a 2-week period, followed by a wire transfer of the combined funds to an overseas account.'}

QUESTIONS = {
    "warrants_sar_review": {
        "type": "noul",
        "instructions": 'Does this pattern match recognized structuring indicators that warrant formal SAR review consideration?',
        "criteria": {"true": 'Multiple deposits just under the reporting threshold followed by an overseas wire is a textbook structuring pattern.', "false": 'Pattern does not match recognized structuring indicators.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'How should this alert be routed?',
        "criteria": {'close_as_false_positive': 'Pattern does not match structuring indicators.', 'aml_analyst_investigation': 'Pattern warrants formal AML analyst investigation.', 'immediate_compliance_escalation': 'Pattern strength and overseas transfer warrant immediate compliance escalation.'},
    },
    "investigation_priority": {
        "type": "score",
        "instructions": 'How should this be prioritized for investigation?',
        "criteria": ['Low', 'Normal', 'High', 'Immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Banking — AML alert triage", 'AML alert: structuring pattern', res.answers)
