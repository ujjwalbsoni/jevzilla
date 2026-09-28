"""
Marketing — Social brand mention triage.

Scenario: A social listening tool flags a brand mention. JEV flags whether it's a PR risk, routes the response, and scores response urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python brand_mention_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'mention': "Verified account with 200K followers posts: 'Just found out [brand]'s 'recycled' packaging claim is being investigated by a consumer watchdog group. Anyone else seeing this?'", 'context': 'No official statement has been made by the company yet.'}

QUESTIONS = {
    "pr_risk": {
        "type": "noul",
        "instructions": "Does this mention carry meaningful PR risk given the account's reach and the nature of the claim?",
        "criteria": {"true": 'A large, verified account raising a substantiation question about a sustainability claim is a recognized PR risk pattern.', "false": 'Mention has low reach or does not raise a substantive concern.'},
    },
    "response_route": {
        "type": "choice",
        "instructions": 'How should this be handled?',
        "criteria": {'monitor_only': 'Low reach or low substance; monitor for now.', 'social_team_response': 'Warrants a prepared, careful public or direct response.', 'escalate_to_pr_and_legal': 'Investigation claim is serious enough to involve PR and legal before responding.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently should this be addressed?',
        "criteria": ['Low', 'Today', 'Immediate', 'Critical - trending risk'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Marketing — Social brand mention triage", 'Flagged social mention, verified account', res.answers)
