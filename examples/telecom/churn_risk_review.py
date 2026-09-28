"""
Telecom — Telecom customer churn risk review.

Scenario: A customer's account activity and support history are reviewed. JEV flags churn risk, routes a retention action, and scores customer value for the offer decision.

Run:
    set OPENROUTER_API_KEY=your-key
    python churn_risk_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'account': '5-year customer, family plan, 4 lines', 'notes': 'Called twice this month asking about early termination fees and competitor promotional offers. No billing issues on the account.'}

QUESTIONS = {
    "high_churn_risk": {
        "type": "noul",
        "instructions": 'Do these signals indicate meaningful churn risk?',
        "criteria": {"true": 'Repeated inquiries about termination fees and competitor offers are direct churn signals.', "false": 'Signals do not indicate elevated churn risk.'},
    },
    "retention_action": {
        "type": "choice",
        "instructions": 'What retention action should be taken?',
        "criteria": {'no_action_needed': 'Low risk; no action needed.', 'standard_retention_offer': 'Moderate risk; offer a standard retention discount.', 'premium_retention_offer_from_manager': 'High value, high risk; needs a manager-level retention offer.'},
    },
    "customer_value": {
        "type": "score",
        "instructions": 'How valuable is this customer for retention purposes?',
        "criteria": ['Standard', 'Good - multi-line', 'High - long tenure multi-line', 'Top tier'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Telecom — Telecom customer churn risk review", 'Customer account review, family plan', res.answers)
