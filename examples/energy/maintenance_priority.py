"""
Energy / Utilities — Grid maintenance priority review.

Scenario: An inspection report flags aging infrastructure. JEV flags whether it's a priority repair, routes scheduling, and scores failure risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python maintenance_priority.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'asset': 'Transformer, 35 years old, serving a residential feeder', 'inspection_note': 'Inspector notes visible oil leakage and thermal imaging showing higher-than-normal operating temperature, consistent with early-stage failure indicators.'}

QUESTIONS = {
    "priority_repair": {
        "type": "noul",
        "instructions": 'Do these findings indicate a priority repair need rather than routine maintenance scheduling?',
        "criteria": {"true": 'Oil leakage combined with elevated thermal readings are recognized early-failure indicators.', "false": 'Findings are within normal wear parameters for routine scheduling.'},
    },
    "scheduling_route": {
        "type": "choice",
        "instructions": 'How should this be scheduled?',
        "criteria": {'routine_maintenance_schedule': 'Within normal parameters; routine schedule.', 'priority_repair_scheduling': 'Findings warrant scheduling repair ahead of routine queue.', 'emergency_replacement': 'Failure risk is high enough to warrant emergency replacement planning.'},
    },
    "failure_risk": {
        "type": "score",
        "instructions": "What is the failure risk if this isn't addressed soon?",
        "criteria": ['Low', 'Moderate', 'High', 'Imminent failure risk'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Energy / Utilities — Grid maintenance priority review", 'Transformer inspection finding', res.answers)
