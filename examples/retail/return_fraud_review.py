"""
Retail / E-commerce — Return fraud risk review.

Scenario: A high-value return request comes in. JEV flags fraud risk, routes it to the right review tier, and scores customer risk for the fraud team.

Run:
    set OPENROUTER_API_KEY=your-key
    python return_fraud_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'order': '$620 order, returned 2 days before the 30-day window closes', 'notes': "Customer's account has 6 returns in the last 4 months, all just before the return window deadline, all citing 'item not as described.'"}

QUESTIONS = {
    "fraud_risk_flag": {
        "type": "noul",
        "instructions": 'Does this return pattern show indicators commonly associated with return abuse or fraud?',
        "criteria": {"true": 'Repeated last-minute returns with the same generic reason is a recognized abuse pattern.', "false": 'Return pattern looks like normal, occasional customer behavior.'},
    },
    "review_tier": {
        "type": "choice",
        "instructions": 'How should this return be processed?',
        "criteria": {'auto_approve_standard': 'No unusual pattern; process automatically.', 'manual_review_required': 'Pattern warrants a human review before refund.', 'flag_account_for_fraud_team': 'Pattern is strong enough to flag the account for the fraud team.'},
    },
    "customer_risk": {
        "type": "score",
        "instructions": "What is this customer's overall return-risk rating?",
        "criteria": ['Low', 'Moderate', 'High', 'Suspicious - restrict account'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Retail / E-commerce — Return fraud risk review", 'Return request, $620 order', res.answers)
