"""
Hospitality / Travel — Booking fraud risk review.

Scenario: A reservation is flagged by the booking system. JEV flags fraud risk, routes verification, and scores risk for the front desk.

Run:
    set OPENROUTER_API_KEY=your-key
    python booking_fraud_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'booking': "5-night luxury suite booking, paid with a card not matching the guest name on the reservation, booked same-day for tonight's check-in."}

QUESTIONS = {
    "high_fraud_risk": {
        "type": "noul",
        "instructions": 'Does this booking show indicators commonly associated with fraudulent reservations (stolen card use)?',
        "criteria": {"true": 'Same-day booking of a high-value stay with a mismatched cardholder name is a recognized fraud pattern.', "false": 'Booking details are consistent with normal guest behavior.'},
    },
    "verification_route": {
        "type": "choice",
        "instructions": 'What should happen at check-in?',
        "criteria": {'standard_checkin': 'No flags; standard check-in process.', 'id_and_card_verification': 'Requires ID verification and card-present confirmation at check-in.', 'hold_pending_payment_verification': 'Risk is high enough to hold the reservation pending payment verification.'},
    },
    "risk_level": {
        "type": "score",
        "instructions": 'What is the fraud risk level for this booking?',
        "criteria": ['Low', 'Moderate', 'High', 'Very high'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Hospitality / Travel — Booking fraud risk review", 'Flagged reservation, mismatched card', res.answers)
