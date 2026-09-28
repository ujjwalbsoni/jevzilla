"""
Telecom — Service upgrade eligibility review.

Scenario: A customer requests an early device/plan upgrade. JEV flags whether they're eligible, routes the decision, and scores retention value of granting an exception.

Run:
    set OPENROUTER_API_KEY=your-key
    python upgrade_eligibility.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'request': 'Customer wants to upgrade their device 4 months before standard eligibility (18 of 22 months into contract), citing a broken screen from an accident.'}

QUESTIONS = {
    "outside_standard_policy": {
        "type": "noul",
        "instructions": 'Is this request outside standard upgrade eligibility policy?',
        "criteria": {"true": '4 months early is outside typical standard eligibility windows.', "false": 'Request falls within standard eligibility.'},
    },
    "decision_route": {
        "type": "choice",
        "instructions": 'How should this request be handled?',
        "criteria": {'auto_approve': 'Within policy; approve automatically.', 'offer_paid_early_upgrade_option': 'Outside policy; offer a paid early-upgrade path instead of a free exception.', 'escalate_for_exception_review': 'Circumstances may warrant a goodwill exception review.'},
    },
    "retention_value": {
        "type": "score",
        "instructions": 'How valuable would granting flexibility here be for retention?',
        "criteria": ['Low', 'Moderate', 'High', 'High - at renewal decision point'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Telecom — Service upgrade eligibility review", 'Early upgrade request', res.answers)
