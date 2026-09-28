"""
Customer Support — Low CSAT follow-up priority.

Scenario: A support interaction receives a low satisfaction score with a comment. JEV flags whether it needs manager follow-up, routes it, and scores priority for review.

Run:
    set OPENROUTER_API_KEY=your-key
    python csat_followup.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'csat_score': '1 out of 5', 'comment': "Agent was polite but clearly didn't understand my technical issue and kept reading from a script. Had to explain the same thing 4 times."}

QUESTIONS = {
    "needs_manager_followup": {
        "type": "noul",
        "instructions": 'Does this comment describe a coaching-relevant issue (e.g. knowledge gap) rather than a one-off customer mood issue?',
        "criteria": {"true": 'A specific, repeated pattern (not understanding the issue, scripted responses) points to a coaching need.', "false": 'Comment reflects general dissatisfaction without a specific, actionable pattern.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'How should this be routed?',
        "criteria": {'log_for_trend_only': 'General dissatisfaction; log for trend tracking.', 'manager_coaching_review': 'Specific issue warrants a coaching conversation with the agent.', 'escalate_customer_for_resolution': 'Underlying technical issue may still be unresolved and needs follow-up.'},
    },
    "priority": {
        "type": "score",
        "instructions": 'How should this be prioritized for review?',
        "criteria": ['Low', 'Normal', 'High', 'Immediate - unresolved issue'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Customer Support — Low CSAT follow-up priority", 'Low CSAT survey response', res.answers)
