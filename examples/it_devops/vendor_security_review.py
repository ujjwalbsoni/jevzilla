"""
IT/DevOps — Third-party vendor security review.

Scenario: Procurement requests a new SaaS vendor be approved. JEV flags data-handling risk, routes the review depth, and scores overall vendor risk for the security team.

Run:
    set OPENROUTER_API_KEY=your-key
    python vendor_security_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'vendor': 'New analytics SaaS tool', 'request_notes': "Vendor will ingest customer PII (names, emails, purchase history) for analytics. Vendor's public security page shows SOC 2 Type I but not Type II, and no mention of data residency options."}

QUESTIONS = {
    "elevated_data_risk": {
        "type": "noul",
        "instructions": "Does this vendor's data handling and certification level indicate elevated risk given it will process customer PII?",
        "criteria": {"true": 'PII processing with only SOC 2 Type I (not Type II) and no residency options are recognized risk indicators.', "false": "Vendor's certifications and data handling are adequate for the data involved."},
    },
    "review_depth": {
        "type": "choice",
        "instructions": 'What level of security review does this vendor need?',
        "criteria": {'standard_vendor_checklist': 'Low-risk data; standard checklist suffices.', 'full_security_questionnaire': 'PII involved; needs a full security questionnaire and DPA review.', 'escalate_to_ciso': 'Certification gaps are significant enough for CISO-level review.'},
    },
    "vendor_risk": {
        "type": "score",
        "instructions": "What is this vendor's overall risk rating?",
        "criteria": ['Low', 'Moderate', 'High', 'Do not approve as-is'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("IT/DevOps — Third-party vendor security review", 'New vendor review: analytics SaaS tool', res.answers)
