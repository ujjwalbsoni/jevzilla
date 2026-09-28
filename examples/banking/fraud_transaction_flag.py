"""
Banking — Transaction fraud flag review.

Scenario: A card transaction is flagged by the fraud detection system. JEV decides whether to hold the transaction, routes the review, and scores fraud confidence.

Run:
    set OPENROUTER_API_KEY=your-key
    python fraud_transaction_flag.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'transaction': '$1,850 electronics purchase', 'notes': "Card is normally used for groceries and gas in one metro area. This transaction occurred in a different country 6 hours after the card's last use domestically."}

QUESTIONS = {
    "likely_fraud": {
        "type": "noul",
        "instructions": 'Does this transaction pattern match common card-fraud indicators (unusual location, amount, and category shift)?',
        "criteria": {"true": 'A sudden cross-border, high-value, category-mismatched transaction is a well-established fraud pattern.', "false": "Transaction is consistent with the cardholder's normal spending pattern."},
    },
    "review_route": {
        "type": "choice",
        "instructions": 'What action should be taken?',
        "criteria": {'approve_transaction': 'Pattern looks normal; approve.', 'hold_and_verify_with_customer': 'Pattern warrants a hold and customer verification (text/call).', 'block_and_freeze_card': 'Pattern is strong enough to block the transaction and freeze the card pending contact.'},
    },
    "fraud_confidence": {
        "type": "score",
        "instructions": 'How confident is this fraud flag?',
        "criteria": ['Low', 'Moderate', 'High', 'Very high'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Banking — Transaction fraud flag review", 'Flagged transaction: $1,850, different country', res.answers)
