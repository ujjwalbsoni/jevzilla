"""
HR — Offer negotiation risk review.

Scenario: A recruiter logs a candidate's counter-offer request before it goes to compensation. JEV flags whether it's outside policy, routes approval, and scores flight risk if declined.

Run:
    set OPENROUTER_API_KEY=your-key
    python offer_risk_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'role': 'Senior Data Scientist', 'band_max': '$168,000', 'candidate_ask': '$182,000 base plus a signing bonus, citing a competing offer with a stated deadline in 3 days.'}

QUESTIONS = {
    "outside_policy": {
        "type": "noul",
        "instructions": "Is the candidate's ask outside standard compensation band policy for this role?",
        "criteria": {"true": 'Requested base exceeds the band maximum.', "false": 'Requested compensation is within or near the standard band.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'Who needs to approve this counter-offer?',
        "criteria": {'recruiter_can_close': 'Within policy; recruiter can finalize.', 'hiring_manager_approval': 'Slightly above band; needs hiring manager sign-off.', 'comp_committee_exception': 'Meaningfully above band; needs a formal comp exception.'},
    },
    "flight_risk": {
        "type": "score",
        "instructions": 'If this request is declined or delayed, how likely is the candidate to walk away?',
        "criteria": ['Low', 'Moderate', 'High', 'Imminent'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("HR — Offer negotiation risk review", 'Candidate counter-offer for Senior Data Scientist', res.answers)
