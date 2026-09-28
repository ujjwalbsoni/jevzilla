"""
Marketing — Customer survey sentiment triage.

Scenario: An open-ended customer survey response is reviewed. JEV flags whether it needs a direct follow-up, routes it, and scores sentiment severity for the dashboard.

Run:
    set OPENROUTER_API_KEY=your-key
    python survey_sentiment.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'response': "I've been a customer for 5 years and the last two updates have made the app so much harder to use that I'm actively looking at your competitor now.", 'nps_score': '4 (out of 10)'}

QUESTIONS = {
    "needs_direct_followup": {
        "type": "noul",
        "instructions": 'Does this comment describe churn risk specific and severe enough to warrant a direct outreach rather than aggregate reporting only?',
        "criteria": {"true": 'A long-tenured customer explicitly citing competitor evaluation is a strong, actionable churn signal.', "false": 'Comment is general feedback without a specific churn signal.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'How should this response be routed?',
        "criteria": {'aggregate_reporting_only': 'General feedback; include in aggregate trends only.', 'customer_success_outreach': 'Specific enough to warrant a direct customer success follow-up.', 'product_team_escalation': 'Usability complaint pattern may need product team attention beyond this one customer.'},
    },
    "sentiment_severity": {
        "type": "score",
        "instructions": 'How severe is this response for the sentiment dashboard?',
        "criteria": ['Positive', 'Neutral', 'Negative', 'Severe - churn risk'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Marketing — Customer survey sentiment triage", 'Open-ended NPS survey comment', res.answers)
