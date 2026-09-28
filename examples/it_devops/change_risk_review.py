"""
IT/DevOps — Change request risk review.

Scenario: A proposed infrastructure change is submitted through the change management process. JEV flags rollback risk, routes approval, and scores change-window priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python change_risk_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'change': 'Database schema migration on the primary orders table during business hours, with a stated 4-hour maintenance window and no documented rollback script.'}

QUESTIONS = {
    "high_rollback_risk": {
        "type": "noul",
        "instructions": "Does this change carry meaningful rollback risk given what's described?",
        "criteria": {"true": 'A production schema migration during business hours with no documented rollback script is a recognized high-risk pattern.', "false": 'Change has a clear, tested rollback path.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'What approval path should this change take?',
        "criteria": {'standard_change_approval': 'Low risk; standard peer approval is sufficient.', 'change_advisory_board': 'Needs CAB review given the risk factors.', 'reject_request_rollback_plan': 'Should not proceed until a rollback plan is documented.'},
    },
    "window_priority": {
        "type": "score",
        "instructions": 'How should this be prioritized for scheduling a maintenance window?',
        "criteria": ['Low priority', 'Next standard window', 'Dedicated off-hours window', 'Emergency change process'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("IT/DevOps — Change request risk review", 'Change request: orders table schema migration', res.answers)
