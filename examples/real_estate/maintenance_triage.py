"""
Real Estate — Maintenance request triage.

Scenario: A tenant submits a maintenance request. JEV flags whether it's urgent, routes it to the right vendor type, and scores response-time priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python maintenance_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'unit': 'Apartment 4B', 'request': 'Tenant reports water dripping from the ceiling in the kitchen, getting worse over the last hour, with a light fixture nearby.'}

QUESTIONS = {
    "urgent_safety_issue": {
        "type": "noul",
        "instructions": 'Does this request describe a condition with potential safety risk (e.g. water near electrical) requiring urgent response?',
        "criteria": {"true": 'Water dripping near a light fixture is a recognized safety hazard pattern.', "false": 'Request does not describe a safety-risk condition.'},
    },
    "vendor_route": {
        "type": "choice",
        "instructions": 'Which vendor type should be dispatched?',
        "criteria": {'routine_maintenance_ticket': 'Non-urgent; standard maintenance queue.', 'emergency_plumber': 'Active water leak needs an emergency plumber.', 'electrician_and_plumber_urgent': 'Water near electrical needs both trades dispatched urgently.'},
    },
    "response_priority": {
        "type": "score",
        "instructions": 'How should this be prioritized for response time?',
        "criteria": ['Standard - within a week', 'Priority - within 48 hours', 'Same day', 'Emergency - immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Real Estate — Maintenance request triage", 'Maintenance request, Unit 4B', res.answers)
