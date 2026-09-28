"""
Manufacturing — Plant safety incident triage.

Scenario: A near-miss or minor incident is logged by a floor supervisor. JEV flags whether OSHA-style recordability applies, routes investigation ownership, and scores incident severity.

Run:
    set OPENROUTER_API_KEY=your-key
    python safety_incident_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'location': 'Line 2, Packaging area', 'report': "Operator's sleeve caught on a conveyor guard that was left open after maintenance. No injury; operator freed themselves and reported immediately."}

QUESTIONS = {
    "recordable_risk": {
        "type": "noul",
        "instructions": 'Does this incident describe conditions that plausibly meet recordable-incident criteria (even though no injury occurred this time)?',
        "criteria": {"true": 'Involves an unguarded moving machine part with direct operator contact.', "false": 'Describes a lower-risk condition with no direct hazard contact.'},
    },
    "investigation_owner": {
        "type": "choice",
        "instructions": 'Who should lead the investigation?',
        "criteria": {'shift_supervisor': 'Minor, can be handled and closed at shift level.', 'ehs_team': 'Guard/interlock failure; needs formal EHS investigation.', 'engineering_review': 'May indicate a design or maintenance-procedure flaw.'},
    },
    "severity": {
        "type": "score",
        "instructions": 'How severe is this near-miss for the incident log?',
        "criteria": ['Minor', 'Moderate', 'Serious potential', 'Critical potential'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Manufacturing — Plant safety incident triage", 'Near-miss report, Line 2 Packaging', res.answers)
