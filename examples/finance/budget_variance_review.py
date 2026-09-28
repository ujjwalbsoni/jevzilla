"""
Finance — Budget variance review.

Scenario: A department's monthly spend is compared to budget. JEV flags whether the variance needs explanation, routes it to the right reviewer, and scores forecast risk for the quarter.

Run:
    set OPENROUTER_API_KEY=your-key
    python budget_variance_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'department': 'Marketing', 'variance_note': 'Department spent 34% over budget this month, driven by an unplanned $60,000 event sponsorship approved outside the normal budget cycle.'}

QUESTIONS = {
    "needs_explanation": {
        "type": "noul",
        "instructions": 'Is this variance large and unusual enough to require a formal written explanation from the department head?',
        "criteria": {"true": 'A single unplanned expense drove a variance well outside normal range.', "false": 'Variance is within normal monthly fluctuation.'},
    },
    "reviewer": {
        "type": "choice",
        "instructions": 'Who should review this variance?',
        "criteria": {'fp&a_analyst': 'Routine variance within normal review process.', 'department_head_explanation': 'Needs the department head to justify the unplanned spend.', 'cfo_review': 'Variance is large enough to affect quarterly forecasting.'},
    },
    "forecast_risk": {
        "type": "score",
        "instructions": 'How much risk does this variance pose to the quarterly forecast?',
        "criteria": ['Low', 'Moderate', 'High', 'Requires forecast revision'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Finance — Budget variance review", 'Marketing dept. monthly variance: +34%', res.answers)
