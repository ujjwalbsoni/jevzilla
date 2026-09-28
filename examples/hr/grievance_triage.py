"""
HR — Employee grievance triage.

Scenario: An employee submits a workplace grievance through HR's intake form. JEV flags whether it needs immediate escalation, routes it to the right HR track, and scores case sensitivity.

Run:
    set OPENROUTER_API_KEY=your-key
    python grievance_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'submitted_by': 'Employee, anonymized', 'grievance': 'Employee reports being repeatedly excluded from team meetings after raising a scheduling conflict tied to a disability accommodation.'}

QUESTIONS = {
    "needs_escalation": {
        "type": "noul",
        "instructions": 'Does this grievance describe a potential legal or compliance risk (e.g. discrimination, retaliation) requiring immediate HR leadership involvement?',
        "criteria": {"true": 'Describes a protected-class or retaliation concern.', "false": 'Describes an interpersonal or process issue without a compliance flag.'},
    },
    "track": {
        "type": "choice",
        "instructions": 'Which HR track should own this grievance?',
        "criteria": {'employee_relations': 'Standard interpersonal or team conflict.', 'compliance_legal': 'Potential discrimination, harassment, or retaliation.', 'accommodations_team': 'Primarily a disability/accommodation process issue.'},
    },
    "sensitivity": {
        "type": "score",
        "instructions": 'How sensitive is this case for handling and documentation?',
        "criteria": ['Routine', 'Elevated', 'High', 'Legal hold'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("HR — Employee grievance triage", 'Grievance intake, anonymized', res.answers)
