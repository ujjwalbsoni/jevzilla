"""
Energy / Utilities — Smart meter anomaly review.

Scenario: A smart meter reading shows an unusual pattern. JEV flags whether it indicates a safety issue vs. billing anomaly, routes the response, and scores urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python meter_anomaly_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'meter_data': "Residential meter shows usage spike to 8x normal average starting 3 days ago, with no change in the account's service address or plan."}

QUESTIONS = {
    "possible_safety_issue": {
        "type": "noul",
        "instructions": 'Could this usage spike pattern indicate a safety issue (e.g. electrical fault) rather than just a billing anomaly?',
        "criteria": {"true": 'A sudden, sustained 8x spike with no explained cause can indicate an electrical fault or hazard.', "false": 'Pattern looks more consistent with a billing/meter reading error.'},
    },
    "response_route": {
        "type": "choice",
        "instructions": 'How should this be handled?',
        "criteria": {'billing_investigation_only': 'Likely a meter or billing issue; investigate billing first.', 'field_technician_dispatch': 'Spike pattern warrants a field check for safety reasons.', 'urgent_safety_inspection': 'Magnitude and duration warrant urgent inspection given fire/safety risk.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently should this be addressed?',
        "criteria": ['Low', 'This week', 'Today', 'Immediate - safety risk'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Energy / Utilities — Smart meter anomaly review", 'Meter usage anomaly', res.answers)
