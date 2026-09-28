"""
Media / Entertainment — User comment moderation review.

Scenario: A comment on published content is flagged by users. JEV flags whether it violates community guidelines, routes the moderation action, and scores severity.

Run:
    set OPENROUTER_API_KEY=your-key
    python comment_moderation.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'comment': "Comment directed at another user includes a specific threat of violence tied to the target's real name, which appears elsewhere in the thread.", 'context': 'Comment has 3 user reports.'}

QUESTIONS = {
    "guideline_violation": {
        "type": "noul",
        "instructions": 'Does this comment violate community guidelines around threats or targeted harassment?',
        "criteria": {"true": 'A specific, named threat of violence is a clear and serious guideline violation.', "false": 'Comment does not rise to the level of a specific threat.'},
    },
    "moderation_action": {
        "type": "choice",
        "instructions": 'What action should be taken?',
        "criteria": {'no_action_within_guidelines': 'Comment does not violate guidelines; leave as-is.', 'remove_comment_and_warn_user': 'Clear violation; remove the comment and warn the user.', 'remove_ban_and_escalate': 'Specific violent threat warrants removal, an account ban, and escalation for possible law enforcement referral.'},
    },
    "severity": {
        "type": "score",
        "instructions": 'How severe is this violation?',
        "criteria": ['Low', 'Moderate', 'High', 'Critical - credible threat'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Media / Entertainment — User comment moderation review", 'Flagged comment, user reports', res.answers)
