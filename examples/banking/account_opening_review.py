"""
Banking — New account opening review.

Scenario: A new account application is reviewed for KYC completeness. JEV flags whether identity verification is sufficient, routes the review, and scores account risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python account_opening_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'application': 'New checking account, online application', 'notes': "Government ID uploaded is slightly blurry in the date-of-birth field, and the address provided doesn't match any record found in the identity verification database."}

QUESTIONS = {
    "verification_insufficient": {
        "type": "noul",
        "instructions": 'Is identity verification insufficient to open this account under standard KYC requirements?',
        "criteria": {"true": 'An unreadable ID field combined with an unmatched address are recognized KYC gaps.', "false": 'Verification appears sufficient to proceed.'},
    },
    "review_route": {
        "type": "choice",
        "instructions": 'What should happen next?',
        "criteria": {'approve_and_open': 'Verification sufficient; open the account.', 'request_additional_documentation': 'Request a clearer ID or additional proof of address.', 'escalate_to_compliance': 'Combination of gaps warrants compliance review before proceeding.'},
    },
    "account_risk": {
        "type": "score",
        "instructions": "What is this account's initial risk rating?",
        "criteria": ['Low', 'Moderate', 'High', 'Do not open pending verification'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Banking — New account opening review", 'New account KYC review', res.answers)
