"""
Media / Entertainment — User-generated content moderation.

Scenario: A user-uploaded video is flagged by automated moderation. JEV flags whether it violates policy, routes the moderation action, and scores review urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python content_moderation.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'flag_reason': 'Automated system flagged audio matching a copyrighted song for the full duration of a 4-minute user video, with no transformative editing detected.'}

QUESTIONS = {
    "policy_violation": {
        "type": "noul",
        "instructions": 'Does this flag indicate a likely content policy violation (unauthorized use of full copyrighted audio)?',
        "criteria": {"true": 'A full-duration audio match with no transformative use is a clear copyright policy violation pattern.', "false": 'Use appears to be short, transformative, or otherwise likely fair use.'},
    },
    "moderation_action": {
        "type": "choice",
        "instructions": 'What action should be taken?',
        "criteria": {'no_action_likely_fair_use': 'Use appears transformative; no action.', 'mute_audio_or_takedown': 'Clear match; mute the audio track or take down per policy.', 'escalate_to_rights_holder_review': 'Ambiguous case; route to rights holder for a claim decision.'},
    },
    "review_urgency": {
        "type": "score",
        "instructions": 'How urgently should this be reviewed?',
        "criteria": ['Low', 'Normal', 'High', 'Immediate - high-view content'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Media / Entertainment — User-generated content moderation", 'Flagged user video, audio match', res.answers)
