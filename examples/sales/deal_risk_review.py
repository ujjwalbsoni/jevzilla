"""
Sales — Open deal risk review.

Scenario: A sales rep's CRM notes are reviewed mid-quarter. JEV flags whether a deal is at risk of slipping, routes it for manager attention, and scores deal health.

Run:
    set OPENROUTER_API_KEY=your-key
    python deal_risk_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'deal': 'Acme Corp, $85,000 ARR, forecast to close this month', 'notes': 'Champion contact went quiet for 2 weeks after being positive. No response to last 3 follow-ups. Economic buyer has not yet been looped in.'}

QUESTIONS = {
    "at_risk_of_slip": {
        "type": "noul",
        "instructions": 'Does this deal show signals consistent with slipping out of the forecast this period?',
        "criteria": {"true": 'Champion silence plus no economic buyer engagement are recognized slip indicators.', "false": 'Deal shows normal progression signals.'},
    },
    "manager_action": {
        "type": "choice",
        "instructions": 'What should the sales manager do with this deal?',
        "criteria": {'leave_with_rep': 'Signals are mild; rep can continue working it.', 'manager_joins_call': 'Needs manager involvement to re-engage or reach the economic buyer.', 'pull_from_forecast': "Signals suggest this should be pulled from this period's forecast."},
    },
    "deal_health": {
        "type": "score",
        "instructions": 'How healthy is this deal right now?',
        "criteria": ['Healthy', 'Slowing', 'At risk', 'Likely to slip'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Sales — Open deal risk review", 'Acme Corp deal, forecast to close this month', res.answers)
