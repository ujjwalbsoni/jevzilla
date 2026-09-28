"""
Healthcare Ops — Insurance pre-authorization request review.

Scenario: An admin staffer logs a pre-authorization request before submission to a payer. JEV flags missing documentation, routes it for completion, and scores approval likelihood risk (administrative aid only, not a clinical or coverage decision).

Run:
    set OPENROUTER_API_KEY=your-key
    python preauth_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'procedure': 'MRI, lumbar spine', 'notes': 'Request includes physician order but no documented conservative-treatment history (e.g. physical therapy), which most payers require for imaging pre-auth.'}

QUESTIONS = {
    "missing_documentation": {
        "type": "noul",
        "instructions": 'Is documentation commonly required for payer approval missing from this request? Administrative completeness check only.',
        "criteria": {"true": 'Conservative-treatment history is a standard payer requirement that appears absent here.', "false": 'Request appears to include the documentation payers typically require.'},
    },
    "next_step": {
        "type": "choice",
        "instructions": 'What should the front office do next with this request?',
        "criteria": {'submit_as_is': 'Documentation appears complete; submit.', 'request_additional_notes': 'Follow up with the clinician for missing documentation before submitting.', 'escalate_to_billing_specialist': "Complex case; needs a billing specialist's review."},
    },
    "approval_risk": {
        "type": "score",
        "instructions": 'What is the administrative risk that this request gets denied for documentation reasons?',
        "criteria": ['Low', 'Moderate', 'High', 'Very high'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Healthcare Ops — Insurance pre-authorization request review", 'Pre-auth request: lumbar MRI', res.answers)
