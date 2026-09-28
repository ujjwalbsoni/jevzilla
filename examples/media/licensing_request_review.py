"""
Media / Entertainment — Content licensing request review.

Scenario: A third party requests to license a piece of content. JEV flags whether the request fits standard terms, routes approval, and scores deal value potential.

Run:
    set OPENROUTER_API_KEY=your-key
    python licensing_request_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'request': 'Educational platform requests to license a documentary clip library for use in online courses, non-exclusive, requesting a 5-year term and worldwide rights.', 'catalog_note': 'This content category typically licenses for 2-3 year terms with regional options.'}

QUESTIONS = {
    "outside_standard_terms": {
        "type": "noul",
        "instructions": 'Does this request fall outside standard licensing terms typically offered for this content category?',
        "criteria": {"true": 'A 5-year worldwide term exceeds the typical 2-3 year, regional-option standard.', "false": 'Request is within standard licensing terms.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'How should this request be handled?',
        "criteria": {'standard_licensing_approval': 'Within standard terms; approve through normal process.', 'negotiate_terms': 'Outside standard terms; needs negotiation on length/territory.', 'executive_deal_review': 'Scope is large enough to need executive-level deal review.'},
    },
    "deal_value": {
        "type": "score",
        "instructions": 'How much deal value potential does this licensing request represent?',
        "criteria": ['Low', 'Moderate', 'High', 'Strategic'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Media / Entertainment — Content licensing request review", 'Licensing request: documentary clip library', res.answers)
