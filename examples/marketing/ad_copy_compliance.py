"""
Marketing — Regulated-industry ad copy compliance.

Scenario: Ad copy for a financial product is reviewed for compliance before publishing. JEV flags disclosure gaps, routes legal review, and scores compliance risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python ad_copy_compliance.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'product': 'Personal loan product', 'copy': "'Get approved in minutes with rates as low as 4.9%!' No APR range disclosure, no mention that the advertised rate requires excellent credit."}

QUESTIONS = {
    "disclosure_gap": {
        "type": "noul",
        "instructions": 'Does this copy omit disclosures typically required for financial product advertising (e.g. representative APR, qualifying conditions)?',
        "criteria": {"true": 'A headline rate with no APR range or qualifying-credit disclosure is a recognized compliance gap.', "false": 'Copy includes standard required disclosures.'},
    },
    "review_route": {
        "type": "choice",
        "instructions": 'What review does this need?',
        "criteria": {'marketing_team_edit': 'Minor; marketing can add standard disclosure language.', 'compliance_legal_review': 'Needs compliance/legal sign-off on required disclosures.', 'hold_pending_full_review': 'Gap is significant enough to hold the campaign pending full review.'},
    },
    "compliance_risk": {
        "type": "score",
        "instructions": 'How much regulatory compliance risk does this copy carry as written?',
        "criteria": ['Low', 'Moderate', 'High', 'Do not publish as-is'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Marketing — Regulated-industry ad copy compliance", 'Financial product ad copy review', res.answers)
