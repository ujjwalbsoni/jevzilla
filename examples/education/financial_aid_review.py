"""
Education — Financial aid appeal review.

Scenario: A student submits a financial aid appeal after a change in circumstances. JEV flags whether documentation supports the appeal, routes it for review, and scores urgency given enrollment deadlines.

Run:
    set OPENROUTER_API_KEY=your-key
    python financial_aid_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'appeal': "Student requests an aid increase citing a parent's job loss 6 weeks ago.", 'documentation_note': 'Appeal includes a termination letter and one recent pay stub showing reduced household income, but no updated tax documentation yet.'}

QUESTIONS = {
    "documentation_sufficient": {
        "type": "noul",
        "instructions": 'Is the documentation provided sufficient to support processing this appeal now?',
        "criteria": {"true": 'A termination letter plus a pay stub are commonly accepted initial support.', "false": 'Documentation is incomplete for standard appeal processing.'},
    },
    "review_route": {
        "type": "choice",
        "instructions": 'How should this appeal be routed?',
        "criteria": {'process_with_current_docs': 'Sufficient to process; move forward.', 'request_additional_documentation': 'Needs updated tax or income documentation before processing.', 'escalate_to_aid_committee': 'Complex enough to need committee-level judgment.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgent is this given enrollment/payment deadlines?',
        "criteria": ['Low', 'This month', 'Before payment deadline', 'Immediate - deadline in days'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Education — Financial aid appeal review", 'Financial aid appeal, parent job loss', res.answers)
