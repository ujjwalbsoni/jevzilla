"""
Cybersecurity — Third-party vendor risk assessment.

Scenario: A security team reviews a vendor's questionnaire responses. JEV flags whether gaps are acceptable, routes the decision, and scores overall vendor security risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python vendor_risk_assessment.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'vendor': 'Cloud storage vendor for internal documents', 'questionnaire_notes': 'Vendor has no documented incident response plan, encrypts data at rest but not explicitly in transit, and could not confirm data residency location.'}

QUESTIONS = {
    "unacceptable_gaps": {
        "type": "noul",
        "instructions": 'Do these gaps represent risk significant enough to be unacceptable without remediation?',
        "criteria": {"true": 'Missing incident response plan combined with unclear encryption-in-transit and residency are material gaps.', "false": 'Gaps are minor and within acceptable risk tolerance.'},
    },
    "decision_route": {
        "type": "choice",
        "instructions": 'What should the security team recommend?',
        "criteria": {'approve_vendor': 'Gaps are minor; approve as-is.', 'approve_with_remediation_plan': 'Require the vendor to address gaps before or shortly after onboarding.', 'reject_vendor': 'Gaps are significant enough to recommend against this vendor.'},
    },
    "vendor_risk": {
        "type": "score",
        "instructions": "What is this vendor's overall security risk rating?",
        "criteria": ['Low', 'Moderate', 'High', 'Unacceptable'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Cybersecurity — Third-party vendor risk assessment", 'Vendor security questionnaire review', res.answers)
