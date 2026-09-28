"""
Banking — Personal loan application review.

Scenario: A loan application is reviewed by an underwriting system before human review. JEV flags red flags, routes the review tier, and scores initial risk (triage aid, not a final credit decision).

Run:
    set OPENROUTER_API_KEY=your-key
    python loan_application_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'application': '$25,000 personal loan, 5-year term', 'notes': 'Debt-to-income ratio is 48% (guideline threshold is 40%), but applicant has 8 years of stable employment at the same employer and no delinquencies in the last 5 years.'}

QUESTIONS = {
    "underwriting_flag": {
        "type": "noul",
        "instructions": 'Does this application show a risk factor that should be flagged before standard processing? This is a triage aid, not a final credit decision.',
        "criteria": {"true": 'Debt-to-income ratio above the standard guideline threshold is a recognized flag, even with mitigating factors.', "false": 'Application shows no factors outside standard guidelines.'},
    },
    "review_tier": {
        "type": "choice",
        "instructions": 'Which review tier should this go to?',
        "criteria": {'standard_automated_approval': 'No flags; standard automated processing.', 'manual_underwriter_review': 'DTI flag needs a human underwriter to weigh mitigating factors.', 'decline_pending_more_info': 'Risk factors suggest declining or requesting more information first.'},
    },
    "initial_risk_signal": {
        "type": "score",
        "instructions": 'What is the initial risk signal for underwriting?',
        "criteria": ['Low', 'Moderate', 'Elevated', 'High'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Banking — Personal loan application review", 'Personal loan application review', res.answers)
