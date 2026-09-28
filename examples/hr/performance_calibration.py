"""
HR — Performance review calibration flag.

Scenario: During calibration, a manager's written justification for a rating is reviewed against typical patterns. JEV flags rating-language mismatches, routes for recalibration, and scores review quality.

Run:
    set OPENROUTER_API_KEY=your-key
    python performance_calibration.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'employee_role': 'Mid-level Product Manager', 'rating': 'Exceeds Expectations', 'justification': "Delivered two features on time. Team said they were 'fine to work with.' No mention of impact, ownership, or growth beyond stated tasks."}

QUESTIONS = {
    "rating_mismatch": {
        "type": "noul",
        "instructions": "Does the written justification's language and evidence support the rating given (e.g. 'Exceeds Expectations' should show above-and-beyond impact)?",
        "criteria": {"true": 'Justification language is notably weaker or more neutral than the rating claimed.', "false": 'Justification evidence is consistent with the rating given.'},
    },
    "calibration_action": {
        "type": "choice",
        "instructions": 'What should the calibration committee do with this review?',
        "criteria": {'approve_as_written': 'Justification supports the rating; approve.', 'request_stronger_evidence': 'Ask the manager for more specific evidence before approving.', 'flag_for_recalibration': 'Rating and evidence are mismatched enough to revisit the rating itself.'},
    },
    "review_quality": {
        "type": "score",
        "instructions": 'How well-written and specific is this justification overall?',
        "criteria": ['Vague', 'Basic', 'Solid', 'Exemplary'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("HR — Performance review calibration flag", 'PM performance review, rating: Exceeds Expectations', res.answers)
