"""
Legal — Trademark dispute triage.

Scenario: A cease-and-desist-style inquiry arrives about brand usage. JEV flags whether it looks credible, routes ownership, and scores business risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python trademark_dispute_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'inquiry': 'Third party claims our new product name infringes their registered trademark in the same product category, citing a 2019 registration and requesting we stop use within 14 days.'}

QUESTIONS = {
    "credible_claim": {
        "type": "noul",
        "instructions": 'Does this claim include specifics (registration date, matching category) consistent with a credible trademark claim rather than a vague threat?',
        "criteria": {"true": 'A specific registration date and matching product category are credibility indicators.', "false": 'Claim lacks specifics that would indicate a credible basis.'},
    },
    "owner": {
        "type": "choice",
        "instructions": 'Who should own the initial response?',
        "criteria": {'brand_marketing_review': 'Low credibility; marketing can assess informally first.', 'ip_counsel_review': 'Credible claim; needs IP counsel assessment.', 'outside_counsel_engagement': 'High-stakes product name; may need outside trademark counsel.'},
    },
    "business_risk": {
        "type": "score",
        "instructions": 'How much business risk does this dispute carry given the 14-day timeline?',
        "criteria": ['Low', 'Moderate', 'High', 'Urgent - rebrand may be needed'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Legal — Trademark dispute triage", 'Trademark inquiry re: new product name', res.answers)
