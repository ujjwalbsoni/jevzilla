"""
Energy / Utilities — Customer energy assistance request review.

Scenario: A customer requests financial assistance to avoid disconnection. JEV flags whether they likely qualify for an assistance program, routes the case, and scores urgency before disconnection.

Run:
    set OPENROUTER_API_KEY=your-key
    python assistance_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'request': 'Customer is 45 days past due on their bill and states they lost their job last month. Disconnection notice is scheduled to take effect in 5 days.', 'account_note': "No prior late payments in the account's 4-year history."}

QUESTIONS = {
    "likely_qualifies": {
        "type": "noul",
        "instructions": "Does this customer's situation match common criteria for hardship assistance programs?",
        "criteria": {"true": 'Recent job loss with a clean prior payment history matches typical hardship-program criteria.', "false": 'Situation does not clearly match standard qualification criteria.'},
    },
    "case_route": {
        "type": "choice",
        "instructions": 'How should this case be routed?',
        "criteria": {'standard_payment_plan_offer': 'Offer a standard payment plan first.', 'assistance_program_referral': 'Refer to hardship assistance program given apparent eligibility.', 'escalate_disconnection_hold': 'Given the timeline, request a disconnection hold while assistance is processed.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgent is this given the disconnection timeline?',
        "criteria": ['Low', 'This week', 'Before disconnection date', 'Immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Energy / Utilities — Customer energy assistance request review", 'Assistance request ahead of disconnection', res.answers)
