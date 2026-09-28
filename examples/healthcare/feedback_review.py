"""
Healthcare Ops — Patient feedback review.

Scenario: A post-visit survey comment comes in. JEV flags whether it needs a service-recovery follow-up, routes it to the right team, and scores severity for the quality dashboard.

Run:
    set OPENROUTER_API_KEY=your-key
    python feedback_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'survey_comment': 'Waited over an hour past my appointment time with no update from staff. The doctor himself was great once I was seen.', 'visit_type': 'Primary care, routine'}

QUESTIONS = {
    "needs_followup": {
        "type": "noul",
        "instructions": 'Does this comment describe a service issue significant enough to warrant a direct follow-up with the patient?',
        "criteria": {"true": 'Describes a specific, notable service failure (extended unexplained wait).', "false": 'Comment is general or does not indicate a specific service failure.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Which team should this feedback be routed to?',
        "criteria": {'front_office_operations': 'Issue is about wait time/communication, not clinical care.', 'clinical_quality_team': 'Issue involves clinical care quality.', 'no_action_positive_feedback': 'Feedback is primarily positive.'},
    },
    "severity": {
        "type": "score",
        "instructions": "How should this be scored for the clinic's quality dashboard?",
        "criteria": ['Positive', 'Minor concern', 'Moderate concern', 'Service recovery needed'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Healthcare Ops — Patient feedback review", 'Post-visit survey comment', res.answers)
