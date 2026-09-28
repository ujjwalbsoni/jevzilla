"""
Education — Exam proctoring anomaly review.

Scenario: An online exam's proctoring software flags unusual activity. JEV flags whether it warrants review, routes the next step, and scores confidence in the flag.

Run:
    set OPENROUTER_API_KEY=your-key
    python integrity_flag_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'exam': 'Timed online final exam', 'flag_note': "Student's gaze left the screen area 14 times during a 60-minute exam, each lasting 3-8 seconds, with no other unusual activity (no additional devices, no browser tab switches) detected."}

QUESTIONS = {
    "warrants_review": {
        "type": "noul",
        "instructions": 'Does this specific pattern (brief, repeated gaze-aways with no other flags) indicate likely academic dishonesty rather than normal test-taking behavior?',
        "criteria": {"true": 'This pattern alone is weaker evidence and commonly overlaps with normal behavior like thinking or note-checking.', "false": 'Pattern is isolated and not indicative of dishonesty.'},
    },
    "next_step": {
        "type": "choice",
        "instructions": 'What should happen next?',
        "criteria": {'no_action_normal_behavior': 'Pattern alone is not strong evidence; no action needed.', 'instructor_spot_check': 'Worth a quick instructor review of the recording.', 'formal_review_with_other_flags': 'Should only escalate formally if combined with stronger evidence.'},
    },
    "flag_confidence": {
        "type": "score",
        "instructions": 'How confident is this specific flag on its own?',
        "criteria": ['Low', 'Weak', 'Moderate', 'Strong'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Education — Exam proctoring anomaly review", 'Proctoring anomaly flag', res.answers)
