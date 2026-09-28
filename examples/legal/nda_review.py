"""
Legal — NDA turnaround review.

Scenario: A counterparty sends a redlined mutual NDA. JEV flags whether the redlines are standard, routes the review track, and scores negotiation effort needed.

Run:
    set OPENROUTER_API_KEY=your-key
    python nda_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'document': 'Mutual NDA, counterparty redline', 'redline_summary': 'Counterparty extended the confidentiality term from 3 years to indefinite and removed the residuals clause entirely.'}

QUESTIONS = {
    "nonstandard_redline": {
        "type": "noul",
        "instructions": 'Are these redlines materially outside standard NDA terms our team typically accepts?',
        "criteria": {"true": 'Indefinite term plus removing residuals are both recognized non-standard asks.', "false": 'Redlines are within normally accepted ranges.'},
    },
    "review_track": {
        "type": "choice",
        "instructions": 'Which review track should this NDA go to?',
        "criteria": {'paralegal_standard_terms': 'Within standard playbook; can be turned around quickly.', 'attorney_negotiation': 'Outside playbook; needs attorney-led negotiation.', 'business_stakeholder_input': 'Needs business input on whether the deal justifies these terms.'},
    },
    "negotiation_effort": {
        "type": "score",
        "instructions": 'How much negotiation effort will this NDA likely require?',
        "criteria": ['Minimal', 'Some back-and-forth', 'Significant', 'May stall the deal'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Legal — NDA turnaround review", 'Mutual NDA redline review', res.answers)
