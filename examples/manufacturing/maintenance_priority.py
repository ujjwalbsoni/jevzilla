"""
Manufacturing — Maintenance request prioritization.

Scenario: A work order is submitted for equipment showing early signs of failure. JEV flags whether it's production-blocking, routes it to the right maintenance team, and scores scheduling priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python maintenance_priority.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'equipment': 'CNC Mill #7', 'request': 'Operator reports unusual vibration and a burning smell during the last 2 cycles. Machine is currently the only one running this part number this week.'}

QUESTIONS = {
    "production_blocking": {
        "type": "noul",
        "instructions": 'If this equipment fails completely, would it stop production of a part with no immediate backup capacity?',
        "criteria": {"true": 'This is the sole machine currently running this part number.', "false": 'Other equipment or capacity can cover this part if it fails.'},
    },
    "team_route": {
        "type": "choice",
        "instructions": 'Which maintenance team should take this work order?',
        "criteria": {'electrical_maintenance': 'Symptoms suggest an electrical/motor issue (burning smell).', 'mechanical_maintenance': 'Symptoms suggest a mechanical/bearing issue (vibration).', 'engineering_investigation': 'Symptoms are ambiguous and need root-cause diagnosis first.'},
    },
    "priority": {
        "type": "score",
        "instructions": "How should this work order be prioritized in today's schedule?",
        "criteria": ['Next available slot', 'Today', 'Immediate - pull equipment', 'Emergency shutdown'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Manufacturing — Maintenance request prioritization", 'Work order for CNC Mill #7', res.answers)
