"""
Real Estate — Purchase offer review.

Scenario: A listing agent reviews an incoming purchase offer. JEV flags whether it's a strong offer, routes the seller recommendation, and scores negotiation leverage.

Run:
    set OPENROUTER_API_KEY=your-key
    python offer_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'listing_price': '$485,000', 'offer': '$462,000 offer, financing contingent, with a 45-day close request and an inspection contingency, no escalation clause.'}

QUESTIONS = {
    "below_market_expectation": {
        "type": "noul",
        "instructions": 'Is this offer meaningfully below what the listing strategy targeted?',
        "criteria": {"true": '$23,000 (about 4.7%) below asking with a longer close and no escalation clause together indicate a soft offer.', "false": 'Offer is close to or at the target range.'},
    },
    "seller_recommendation": {
        "type": "choice",
        "instructions": 'What should the agent recommend to the seller?',
        "criteria": {'accept_as_is': 'Offer is strong enough to accept.', 'counter_offer': 'Counter on price and/or close timeline.', 'wait_for_other_offers': 'Market conditions suggest waiting could yield a stronger offer.'},
    },
    "negotiation_leverage": {
        "type": "score",
        "instructions": 'How much negotiation leverage does the seller have here?',
        "criteria": ['Low', 'Moderate', 'High', 'Strong - multiple offers likely'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Real Estate — Purchase offer review", 'Purchase offer on $485,000 listing', res.answers)
