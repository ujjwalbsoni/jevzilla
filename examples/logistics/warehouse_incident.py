"""
Logistics / Supply Chain — Warehouse incident triage.

Scenario: A warehouse incident is logged by a shift lead. JEV flags whether it's safety-recordable, routes investigation, and scores severity for the ops dashboard.

Run:
    set OPENROUTER_API_KEY=your-key
    python warehouse_incident.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'location': 'Receiving dock, Warehouse 3', 'report': 'Forklift operator backed into a support rack, causing a partial rack collapse. No injuries. Approximately $8,000 in damaged inventory.'}

QUESTIONS = {
    "safety_recordable": {
        "type": "noul",
        "instructions": 'Does this incident describe conditions that typically require formal safety incident recording, even without injury?',
        "criteria": {"true": 'Equipment-caused structural damage from an operator error is a recognized recordable-pattern incident.', "false": 'Incident does not indicate a recordable safety condition.'},
    },
    "investigation_route": {
        "type": "choice",
        "instructions": 'Who should investigate this incident?',
        "criteria": {'shift_lead_close_out': 'Minor; shift lead can document and close.', 'safety_team_investigation': 'Needs a formal safety investigation given the structural damage.', 'operations_and_safety_joint_review': 'Damage and pattern warrant a joint ops/safety review of rack safety zones.'},
    },
    "severity": {
        "type": "score",
        "instructions": 'How severe is this incident for the ops dashboard?',
        "criteria": ['Minor', 'Moderate', 'Serious - property damage', 'Critical - injury potential'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Logistics / Supply Chain — Warehouse incident triage", 'Warehouse incident: rack collapse', res.answers)
