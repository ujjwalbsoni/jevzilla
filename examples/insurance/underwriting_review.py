"""
Insurance — New business underwriting risk review.

Scenario: A new policy application comes in for underwriting. JEV flags red flags, routes it to the right underwriting tier, and scores initial risk for pricing.

Run:
    set OPENROUTER_API_KEY=your-key
    python underwriting_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'applicant': 'New commercial auto policy, 8-vehicle delivery fleet', 'application_notes': 'Two drivers on the fleet roster have DUI convictions within the last 3 years. Fleet has had 3 at-fault accidents in the past 24 months.'}

QUESTIONS = {
    "underwriting_flag": {
        "type": "noul",
        "instructions": 'Does this application show risk indicators that should be flagged before standard pricing is applied?',
        "criteria": {"true": 'Recent DUI convictions combined with multiple at-fault accidents are recognized high-risk indicators.', "false": 'Application shows no unusual risk indicators.'},
    },
    "underwriting_tier": {
        "type": "choice",
        "instructions": 'Which underwriting tier should this application go to?',
        "criteria": {'standard_tier_pricing': 'No unusual risk factors.', 'senior_underwriter_review': 'Risk factors present; needs experienced review.', 'decline_or_high_risk_pool': 'Risk factors may require decline or a high-risk pricing pool.'},
    },
    "initial_risk": {
        "type": "score",
        "instructions": 'What is the initial risk rating for pricing purposes?',
        "criteria": ['Standard', 'Elevated', 'High', 'Substandard'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Insurance — New business underwriting risk review", 'New commercial auto application, 8-vehicle fleet', res.answers)
