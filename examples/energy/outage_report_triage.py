"""
Energy / Utilities — Power outage report triage.

Scenario: Customer outage reports are reviewed by the operations center. JEV flags whether it indicates a wider grid issue, routes crew dispatch, and scores restoration priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python outage_report_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'reports': '9 customers in the same substation service area report power loss within a 10-minute window, no reported storm activity in the area.'}

QUESTIONS = {
    "grid_level_issue": {
        "type": "noul",
        "instructions": 'Does this pattern indicate a substation or grid-level issue rather than isolated individual outages?',
        "criteria": {"true": 'A tight cluster in one substation area with no weather event points to a grid-level cause.', "false": "Reports don't show a clear geographic or timing cluster."},
    },
    "dispatch_route": {
        "type": "choice",
        "instructions": 'How should crew dispatch be handled?',
        "criteria": {'standard_individual_dispatch': 'Isolated issue; dispatch to individual addresses.', 'substation_inspection_crew': 'Pattern warrants dispatching a crew to inspect the substation.', 'emergency_response_activation': 'If a critical facility (hospital, etc.) is in the affected area, escalate immediately.'},
    },
    "restoration_priority": {
        "type": "score",
        "instructions": 'How should this be prioritized for restoration?',
        "criteria": ['Low', 'Normal', 'High', 'Critical'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Energy / Utilities — Power outage report triage", 'Outage reports, single substation area', res.answers)
