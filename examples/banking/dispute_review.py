"""
Banking — Transaction dispute review.

Scenario: A customer disputes a charge. JEV flags whether it looks like a legitimate dispute or likely friendly fraud, routes the case, and scores resolution priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python dispute_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'dispute': 'Customer disputes a $95 charge from a merchant, stating they never made the purchase.', 'account_note': "This is the customer's 4th disputed charge in the last 6 months, all from different merchants, all for similar amounts."}

QUESTIONS = {
    "possible_friendly_fraud": {
        "type": "noul",
        "instructions": "Does this account's dispute pattern suggest possible friendly fraud (repeated disputes) rather than a first-time legitimate issue?",
        "criteria": {"true": 'Four disputes in 6 months across different merchants is a recognized friendly-fraud pattern.', "false": 'This appears to be an isolated, first-time dispute.'},
    },
    "case_route": {
        "type": "choice",
        "instructions": 'How should this case be handled?',
        "criteria": {'standard_dispute_process': 'First-time dispute; process normally.', 'enhanced_review_required': 'Pattern warrants enhanced review before crediting the account.', 'fraud_team_pattern_review': 'Repeated pattern warrants a broader fraud team review of the account.'},
    },
    "resolution_priority": {
        "type": "score",
        "instructions": 'How should this be prioritized for resolution?',
        "criteria": ['Low', 'Normal', 'High', 'Urgent - regulatory deadline approaching'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Banking — Transaction dispute review", 'Transaction dispute review', res.answers)
