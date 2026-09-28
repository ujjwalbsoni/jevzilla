"""
Media / Entertainment — Copyright claim review.

Scenario: A rights holder files a copyright claim against uploaded content. JEV flags whether the claim looks valid, routes the review, and scores dispute risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python copyright_claim_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'claim': 'Rights holder claims ownership of background music in a 10-second clip within a 15-minute video, requesting the entire video be taken down rather than just muted.'}

QUESTIONS = {
    "disproportionate_request": {
        "type": "noul",
        "instructions": 'Does the requested remedy (full takedown) appear disproportionate to the claimed infringement (a short clip within a much longer video)?',
        "criteria": {"true": 'A full-video takedown request over a 10-second segment in a 15-minute video is a recognized disproportionate-claim pattern.', "false": 'Requested remedy appears proportionate to the claim.'},
    },
    "review_route": {
        "type": "choice",
        "instructions": 'How should this claim be processed?',
        "criteria": {'process_takedown_as_requested': 'Claim and remedy appear proportionate; process as requested.', 'offer_partial_remedy_first': 'Offer muting/editing the specific segment instead of a full takedown.', 'flag_for_manual_claims_review': 'Disproportionate request warrants manual review before action.'},
    },
    "dispute_risk": {
        "type": "score",
        "instructions": 'How likely is the uploader to dispute this claim?',
        "criteria": ['Low', 'Moderate', 'High', 'Very high'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Media / Entertainment — Copyright claim review", 'Copyright claim on 10-second clip', res.answers)
