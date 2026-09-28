"""
Marketing — Influencer partnership review.

Scenario: A proposed influencer partnership is reviewed before signing. JEV flags brand-safety risk, routes approval, and scores partnership value.

Run:
    set OPENROUTER_API_KEY=your-key
    python influencer_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'influencer': 'Lifestyle influencer, 340K followers', 'notes': 'Strong engagement rate and audience overlap with target demographic, but recent posts show unrelated controversial political commentary that generated significant public backlash 2 weeks ago.'}

QUESTIONS = {
    "brand_safety_risk": {
        "type": "noul",
        "instructions": "Does this influencer's recent activity present a brand-safety risk for partnership?",
        "criteria": {"true": 'Recent public backlash over controversial commentary is a recognized brand-safety flag.', "false": 'No notable brand-safety concerns in recent activity.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'How should this partnership be handled?',
        "criteria": {'approve_standard_terms': 'No concerns; proceed as planned.', 'proceed_with_monitoring_clause': 'Proceed but add a brand-safety/morals clause and monitor closely.', 'decline_partnership': 'Recent controversy is significant enough to decline.'},
    },
    "partnership_value": {
        "type": "score",
        "instructions": "How valuable would this partnership be if the risk weren't a factor?",
        "criteria": ['Low', 'Moderate', 'High', 'Exceptional fit'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Marketing — Influencer partnership review", 'Influencer partnership proposal review', res.answers)
