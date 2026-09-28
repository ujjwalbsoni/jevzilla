"""
Sales — Sales proposal review before sending.

Scenario: A rep submits a custom proposal for manager review before sending to a prospect. JEV flags pricing or scope risk, routes approval, and scores deal-margin risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python proposal_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'prospect': 'Mid-market manufacturing company, 200 seats', 'proposal_notes': "Proposal includes a 35% discount off list price plus 2 custom integration hours not normally included in this tier, to match a competitor's offer."}

QUESTIONS = {
    "outside_standard_terms": {
        "type": "noul",
        "instructions": 'Does this proposal include terms (discount depth, custom scope) outside what a rep can typically approve without review?',
        "criteria": {"true": '35% discount plus added custom scope together exceed typical rep-level authority.', "false": 'Terms are within standard, pre-approved ranges.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": "Who needs to approve this proposal before it's sent?",
        "criteria": {'rep_can_send': 'Within standard terms; send as-is.', 'sales_manager_approval': 'Discount level needs manager sign-off.', 'finance_and_solutions_approval': 'Custom scope needs finance and solutions engineering sign-off.'},
    },
    "margin_risk": {
        "type": "score",
        "instructions": 'How much margin risk does this proposal carry?',
        "criteria": ['Low', 'Moderate', 'High', 'Below minimum margin'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Sales — Sales proposal review before sending", 'Proposal draft for 200-seat mid-market deal', res.answers)
