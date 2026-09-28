"""
Finance — Small business credit application review.

Scenario: A loan officer logs a business credit application. JEV flags red flags for underwriting, routes the review tier, and scores default risk for initial triage (not a final credit decision).

Run:
    set OPENROUTER_API_KEY=your-key
    python credit_application_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'business': '3-year-old regional catering company', 'application_notes': 'Requesting a $75,000 line of credit. Revenue has grown steadily but debt-to-income ratio is above typical approval thresholds, and two recent late payments appear on the trade credit report.'}

QUESTIONS = {
    "underwriting_flag": {
        "type": "noul",
        "instructions": 'Does this application show risk indicators that should be flagged for underwriter attention before standard processing? This is a triage aid, not a final credit decision.',
        "criteria": {"true": 'Elevated debt ratio combined with recent late payments are recognized underwriting flags.', "false": 'Application shows no notable risk indicators beyond standard review.'},
    },
    "review_tier": {
        "type": "choice",
        "instructions": 'Which underwriting tier should this application go to?',
        "criteria": {'standard_underwriting': 'No unusual risk factors; standard process.', 'senior_underwriter_review': 'Risk factors present; needs a more experienced reviewer.', 'decline_or_restructure': 'Risk factors suggest this application may need restructuring or decline.'},
    },
    "default_risk_signal": {
        "type": "score",
        "instructions": 'What is the initial default-risk signal for triage purposes?',
        "criteria": ['Low', 'Moderate', 'Elevated', 'High'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Finance — Small business credit application review", 'Credit application, $75,000 line of credit', res.answers)
