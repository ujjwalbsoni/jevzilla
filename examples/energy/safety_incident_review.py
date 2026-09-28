"""
Energy / Utilities — Field safety incident review.

Scenario: A field crew reports a safety incident. JEV flags whether it's OSHA-recordable, routes investigation, and scores severity.

Run:
    set OPENROUTER_API_KEY=your-key
    python safety_incident_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'report': 'Line worker received a minor electrical shock while working on what was believed to be a de-energized line, later confirmed the line was still live due to a tagging error.'}

QUESTIONS = {
    "recordable_incident": {
        "type": "noul",
        "instructions": 'Does this incident meet criteria typically requiring formal safety recording?',
        "criteria": {"true": 'An electrical shock from a lockout/tagout failure is a recognized recordable-incident pattern.', "false": 'Incident does not meet recordable criteria.'},
    },
    "investigation_route": {
        "type": "choice",
        "instructions": 'Who should investigate this incident?',
        "criteria": {'crew_supervisor_close_out': 'Minor; supervisor documents and closes.', 'safety_department_investigation': 'Lockout/tagout failure needs a formal safety investigation.', 'regulatory_notification_review': 'Severity may require regulatory notification review.'},
    },
    "severity": {
        "type": "score",
        "instructions": 'How severe is this incident?',
        "criteria": ['Minor', 'Moderate', 'Serious', 'Critical - near-fatality potential'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Energy / Utilities — Field safety incident review", 'Field incident: electrical shock, tagging error', res.answers)
