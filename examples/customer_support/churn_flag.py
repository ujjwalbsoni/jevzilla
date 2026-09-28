"""
Customer Support — Support interaction churn flag.

Scenario: A support conversation transcript is reviewed after resolution. JEV flags churn risk signals, routes it for CS follow-up, and scores priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python churn_flag.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'transcript_summary': "Customer's issue was resolved, but during the conversation they mentioned 'we're already looking at switching providers next renewal' and expressed frustration about repeated similar issues this quarter."}

QUESTIONS = {
    "churn_signal_present": {
        "type": "noul",
        "instructions": "Does this transcript contain an explicit or strong churn signal that support alone typically can't resolve?",
        "criteria": {"true": 'An explicit mention of evaluating a switch at renewal is a direct churn signal.', "false": 'Transcript does not contain a notable churn signal.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Where should this be routed?',
        "criteria": {'no_action_resolved': 'Issue resolved with no churn signal; no further action.', 'customer_success_notification': "Churn signal should be flagged to the customer's CS owner.", 'leadership_save_play': 'Signal plus repeated-issue pattern may need a leadership-level save conversation.'},
    },
    "priority": {
        "type": "score",
        "instructions": 'How should this be prioritized for follow-up?',
        "criteria": ['Low', 'Normal', 'High', 'Immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Customer Support — Support interaction churn flag", 'Post-resolution transcript review', res.answers)
