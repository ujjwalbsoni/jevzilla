"""
Customer Support — Support escalation review.

Scenario: A customer requests to speak with a manager after a support interaction. JEV flags whether escalation is warranted, routes it, and scores the interaction's reputational risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python escalation_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'request': 'Customer states this is their third contact about the same billing issue in 2 weeks, and threatens to post about it on social media if not resolved today.', 'prior_notes': "Previous two tickets show the issue was marked 'resolved' but the customer says the charge is still wrong."}

QUESTIONS = {
    "warranted_escalation": {
        "type": "noul",
        "instructions": 'Does this situation show a pattern (repeated unresolved contact, explicit reputational threat) that warrants manager escalation?',
        "criteria": {"true": 'Multiple unresolved contacts on the same issue plus a stated public threat are recognized escalation triggers.', "false": 'Situation does not show a clear escalation pattern.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'How should this be routed?',
        "criteria": {'standard_agent_resolution': 'Can likely still be resolved by a skilled agent.', 'manager_escalation': 'Pattern warrants manager involvement now.', 'social_media_risk_team': 'Explicit public threat warrants looping in the social/PR risk process.'},
    },
    "reputational_risk": {
        "type": "score",
        "instructions": 'How much reputational risk does this interaction carry if unresolved today?',
        "criteria": ['Low', 'Moderate', 'High', 'Urgent - public risk'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Customer Support — Support escalation review", 'Escalation request: repeated billing issue', res.answers)
