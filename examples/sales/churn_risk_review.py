"""
Sales — Renewal churn risk review.

Scenario: A customer success manager logs notes ahead of a renewal. JEV flags churn risk, routes it to the right save-play, and scores urgency before the renewal date.

Run:
    set OPENROUTER_API_KEY=your-key
    python churn_risk_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'account': 'Northwind Retail, renewal in 45 days', 'notes': "Product usage dropped 40% over the last quarter. Main champion left the company last month. No response yet to the new admin contact's onboarding email."}

QUESTIONS = {
    "high_churn_risk": {
        "type": "noul",
        "instructions": 'Does this account show signals consistent with meaningful churn risk ahead of renewal?',
        "criteria": {"true": 'Usage decline plus loss of the champion are recognized churn indicators.', "false": 'Account shows stable or improving engagement.'},
    },
    "save_play": {
        "type": "choice",
        "instructions": 'Which save-play should CS run for this account?',
        "criteria": {'standard_checkin': 'Low risk; standard renewal check-in.', 'executive_business_review': 'Moderate risk; schedule a business review to re-establish value.', 'escalate_to_leadership': 'High risk; needs CS leadership and possibly sales involvement now.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently does this account need attention before renewal?',
        "criteria": ['Low', 'This month', 'This week', 'Immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Sales — Renewal churn risk review", 'Northwind Retail renewal, 45 days out', res.answers)
