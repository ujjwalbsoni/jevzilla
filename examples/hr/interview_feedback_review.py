"""
HR — Interview feedback consolidation.

Scenario: An interview panel submits written feedback on a candidate. JEV flags conflicting signals, routes the hiring decision, and scores overall panel confidence.

Run:
    set OPENROUTER_API_KEY=your-key
    python interview_feedback_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'candidate': 'Priya Nair, Staff Engineer candidate', 'feedback': 'Panel of 4: two strong yes on system design, one no citing weak communication, one neutral citing limited leadership examples.'}

QUESTIONS = {
    "conflicting_signals": {
        "type": "noul",
        "instructions": 'Do the panel members show materially conflicting assessments of this candidate?',
        "criteria": {"true": 'Feedback ranges from strong yes to no on core competencies.', "false": 'Feedback is broadly consistent across panelists.'},
    },
    "next_step": {
        "type": "choice",
        "instructions": 'What should the hiring team do next?',
        "criteria": {'extend_offer': 'Consensus is positive; proceed to offer.', 'additional_interview': 'Signals conflict enough to warrant one more focused round.', 'reject': 'Consensus is negative.'},
    },
    "panel_confidence": {
        "type": "score",
        "instructions": 'How confident is the panel overall in this candidate?',
        "criteria": ['Low', 'Mixed', 'Solid', 'Unanimous'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("HR — Interview feedback consolidation", 'Panel feedback for Priya Nair', res.answers)
