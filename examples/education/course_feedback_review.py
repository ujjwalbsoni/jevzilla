"""
Education — Course feedback review.

Scenario: End-of-term course feedback is reviewed by a department chair. JEV flags whether a comment needs follow-up, routes it, and scores severity for the department dashboard.

Run:
    set OPENROUTER_API_KEY=your-key
    python course_feedback_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'comment': 'The professor was often 20+ minutes late to class and cancelled 4 sessions in the last month without notice or makeup content.', 'course': 'Required core course, 80 students enrolled'}

QUESTIONS = {
    "needs_followup": {
        "type": "noul",
        "instructions": 'Does this comment describe a pattern serious enough to warrant chair follow-up with the instructor?',
        "criteria": {"true": 'Repeated lateness and unnotified cancellations in a required course is a recognized pattern needing follow-up.', "false": 'Comment describes a minor, one-off concern.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'How should this be routed?',
        "criteria": {'aggregate_with_other_feedback': 'Wait to see if this is an isolated comment.', 'chair_conversation_with_instructor': 'Pattern warrants a direct conversation with the instructor.', 'academic_affairs_review': 'Given the required-course impact on many students, may need higher-level review.'},
    },
    "severity": {
        "type": "score",
        "instructions": "How should this be rated for the department's feedback dashboard?",
        "criteria": ['Minor', 'Moderate', 'Serious', 'Urgent - student impact at scale'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Education — Course feedback review", 'Course feedback comment', res.answers)
