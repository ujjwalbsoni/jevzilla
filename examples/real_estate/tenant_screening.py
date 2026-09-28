"""
Real Estate — Tenant application screening.

Scenario: A rental application is reviewed. JEV flags whether it meets standard criteria, routes the approval decision, and scores overall applicant risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python tenant_screening.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'applicant': 'Applicant for a $2,400/month unit', 'notes': 'Income is 2.8x rent (policy requires 3x). Credit score is 680. No eviction history. Employment verified, 2 years at current job.'}

QUESTIONS = {
    "meets_income_criteria": {
        "type": "noul",
        "instructions": 'Does this application meet the standard income-to-rent ratio criteria?',
        "criteria": {"true": 'Application falls slightly below the required 3x income-to-rent ratio.', "false": 'Application meets or exceeds the required ratio.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'How should this application be processed?',
        "criteria": {'standard_approval': 'Meets all criteria; approve.', 'approval_with_conditions': 'Slightly below criteria; consider a co-signer or higher deposit.', 'denial_pending_review': 'Below criteria enough to warrant a closer look before deciding.'},
    },
    "applicant_risk": {
        "type": "score",
        "instructions": "What is this applicant's overall risk rating?",
        "criteria": ['Low', 'Moderate', 'Elevated', 'High'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Real Estate — Tenant application screening", 'Rental application review', res.answers)
