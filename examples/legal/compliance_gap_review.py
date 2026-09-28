"""
Legal — Policy compliance gap review.

Scenario: An internal audit note flags a possible policy gap. JEV decides whether it needs legal review, routes ownership, and scores regulatory exposure.

Run:
    set OPENROUTER_API_KEY=your-key
    python compliance_gap_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'policy_area': 'Data retention', 'audit_note': 'Customer support logs containing personal data are being retained indefinitely with no automated deletion process, despite a stated 24-month retention policy.'}

QUESTIONS = {
    "needs_legal_review": {
        "type": "noul",
        "instructions": 'Does this gap between stated policy and actual practice create potential regulatory exposure?',
        "criteria": {"true": 'Indefinite retention against a stated 24-month policy is a recognized compliance gap pattern.', "false": 'Gap appears to be a minor documentation issue with limited exposure.'},
    },
    "owner": {
        "type": "choice",
        "instructions": 'Who should own closing this gap?',
        "criteria": {'it_process_fix': 'Primarily a technical/process fix (automate deletion).', 'legal_compliance_review': 'Needs legal to assess regulatory exposure first.', 'executive_disclosure_review': 'Exposure may be significant enough to need leadership and possible disclosure review.'},
    },
    "exposure": {
        "type": "score",
        "instructions": 'How much regulatory exposure does this gap represent?',
        "criteria": ['Low', 'Moderate', 'High', 'Reportable'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Legal — Policy compliance gap review", 'Audit finding: data retention gap', res.answers)
