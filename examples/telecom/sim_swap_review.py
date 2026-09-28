"""
Telecom — SIM swap fraud review.

Scenario: A SIM swap request comes in. JEV flags fraud risk, routes verification requirements, and scores account risk given the sensitivity of SIM swap fraud.

Run:
    set OPENROUTER_API_KEY=your-key
    python sim_swap_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'request': 'SIM swap requested online for a number that was also used to reset a linked email password 2 hours earlier.', 'account_note': 'Account has had no SIM swap requests in its 6-year history.'}

QUESTIONS = {
    "high_fraud_risk": {
        "type": "noul",
        "instructions": 'Does this request show a pattern commonly associated with SIM swap fraud (used for account takeover)?',
        "criteria": {"true": 'A SIM swap request shortly after a linked email password reset is a well-known account-takeover pattern.', "false": 'Request does not show a notable fraud pattern.'},
    },
    "verification_route": {
        "type": "choice",
        "instructions": 'What verification should be required?',
        "criteria": {'standard_verification': 'No flags; standard identity verification.', 'enhanced_verification_required': 'Pattern warrants enhanced verification (e.g. video ID, callback to a known number).', 'block_and_manual_review': 'Pattern is strong enough to block automatically and require manual fraud team review.'},
    },
    "account_risk": {
        "type": "score",
        "instructions": 'How should this account be rated for risk given the SIM swap sensitivity?',
        "criteria": ['Low', 'Moderate', 'High', 'Critical - likely takeover attempt'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Telecom — SIM swap fraud review", 'SIM swap request review', res.answers)
