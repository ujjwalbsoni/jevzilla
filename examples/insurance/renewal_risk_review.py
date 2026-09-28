"""
Insurance — Policy renewal risk review.

Scenario: An underwriter reviews a policy coming up for renewal. JEV flags whether risk has changed materially, routes the renewal decision, and scores premium-adjustment need.

Run:
    set OPENROUTER_API_KEY=your-key
    python renewal_risk_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'policy_type': 'Commercial property', 'renewal_notes': 'Insured added a second warehouse location with flammable materials storage since last renewal, not yet reflected in the current policy schedule.'}

QUESTIONS = {
    "material_risk_change": {
        "type": "noul",
        "instructions": "Has the insured's risk profile changed materially since the last renewal in a way that isn't reflected in the current policy?",
        "criteria": {"true": 'An unlisted new location with flammable materials storage is a material, unreflected risk change.', "false": 'Risk profile is consistent with the current policy terms.'},
    },
    "renewal_route": {
        "type": "choice",
        "instructions": 'How should this renewal be handled?',
        "criteria": {'standard_renewal': 'No material change; renew as-is.', 'underwriter_reassessment': 'Needs updated risk assessment and possible re-rating before renewal.', 'decline_renewal_pending_inspection': 'Change is significant enough to require inspection before renewing.'},
    },
    "premium_adjustment": {
        "type": "score",
        "instructions": 'How much premium adjustment is likely needed given this change?',
        "criteria": ['None', 'Minor', 'Significant', 'Requires full re-underwriting'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Insurance — Policy renewal risk review", 'Commercial property renewal review', res.answers)
