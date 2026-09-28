"""
Education — Admission application review.

Scenario: An admissions officer reviews an application flagged by initial screening. JEV flags whether it needs committee review, routes the track, and scores overall applicant strength.

Run:
    set OPENROUTER_API_KEY=your-key
    python admission_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'program': 'Graduate program, competitive admit rate', 'notes': 'GPA is below the typical admitted range, but application includes 3 years of directly relevant work experience and 2 strong recommendation letters citing specific project impact.'}

QUESTIONS = {
    "needs_committee_review": {
        "type": "noul",
        "instructions": 'Does this application show a mismatch between quantitative metrics and qualitative strength that warrants committee discussion rather than automatic screening?',
        "criteria": {"true": 'Below-range GPA alongside strong, specific recommendations is a recognized case for holistic review.', "false": 'Application is consistent across metrics with no notable mismatch.'},
    },
    "review_track": {
        "type": "choice",
        "instructions": 'What review track should this application take?',
        "criteria": {'standard_screening_decision': 'Consistent profile; standard decision applies.', 'holistic_committee_review': 'Mismatch warrants full committee discussion.', 'request_additional_materials': 'Would benefit from an additional writing sample or interview.'},
    },
    "applicant_strength": {
        "type": "score",
        "instructions": "How would you rate this applicant's overall strength?",
        "criteria": ['Below typical range', 'Borderline', 'Strong', 'Highly competitive'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Education — Admission application review", 'Graduate application review', res.answers)
