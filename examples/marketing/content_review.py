"""
Marketing — Campaign content compliance review.

Scenario: A draft ad is submitted for legal/brand review before launch. JEV flags whether it makes risky claims, routes the review, and scores launch risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python content_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'campaign': 'Weight-loss supplement ad', 'copy': "'Lose 15 pounds in 2 weeks, guaranteed, no diet or exercise needed!' with a before/after image and no visible disclaimer."}

QUESTIONS = {
    "risky_claims": {
        "type": "noul",
        "instructions": 'Does this copy make claims that are commonly considered unsubstantiated or regulatorily risky (e.g. FTC-style health/efficacy guarantees)?',
        "criteria": {"true": 'Specific, guaranteed health outcome claims with no disclaimer are a recognized regulatory risk pattern.', "false": 'Claims are general and do not indicate regulatory risk.'},
    },
    "review_route": {
        "type": "choice",
        "instructions": 'What review does this ad need before launch?',
        "criteria": {'standard_brand_review': 'No risky claims; standard review only.', 'legal_compliance_review': 'Claims need legal review and likely a required disclaimer.', 'reject_and_revise': 'Claims are risky enough that copy should be revised before any review.'},
    },
    "launch_risk": {
        "type": "score",
        "instructions": 'How much risk would launching this as-is carry?',
        "criteria": ['Low', 'Moderate', 'High', 'Regulatory action risk'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Marketing — Campaign content compliance review", 'Draft ad copy review', res.answers)
