"""
Education — Student submission integrity review.

Scenario: An instructor's plagiarism-detection tool flags a submission. JEV flags whether it warrants an academic integrity case, routes the next step, and scores confidence for the flag.

Run:
    set OPENROUTER_API_KEY=your-key
    python submission_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'assignment': 'Research essay, undergraduate course', 'flag_note': "Similarity tool shows 62% overlap with a single online source, concentrated in the essay's argument section, not just citations or common phrases."}

QUESTIONS = {
    "warrants_integrity_case": {
        "type": "noul",
        "instructions": 'Does this flag pattern indicate a likely integrity violation rather than a false positive?',
        "criteria": {"true": 'High overlap concentrated in original argument content (not citations) is a recognized violation pattern.', "false": 'Overlap pattern is consistent with proper citation or common phrasing.'},
    },
    "next_step": {
        "type": "choice",
        "instructions": 'What should the instructor do next?',
        "criteria": {'no_action_likely_false_positive': 'Pattern looks like a false positive; no action needed.', 'student_conversation_first': 'Discuss with the student before escalating formally.', 'formal_integrity_case': 'Pattern is strong enough to open a formal academic integrity case.'},
    },
    "flag_confidence": {
        "type": "score",
        "instructions": 'How confident is this flag?',
        "criteria": ['Low', 'Moderate', 'High', 'Very high'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Education — Student submission integrity review", 'Similarity flag on research essay', res.answers)
