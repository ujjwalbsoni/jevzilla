"""
Retail / E-commerce — Product review moderation.

Scenario: A submitted product review is queued for moderation. JEV flags policy violations, routes the moderation action, and scores review authenticity risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python review_moderation.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'product': 'Wireless earbuds', 'review_text': 'These are amazing!!! Best earbuds ever, use code SAVE20 at [competitor site] for a better deal on the same product from the real manufacturer!'}

QUESTIONS = {
    "policy_violation": {
        "type": "noul",
        "instructions": 'Does this review violate typical marketplace content policy (e.g. promotional links, competitor redirection)?',
        "criteria": {"true": 'Contains a promotional code and a redirect to a competitor site.', "false": 'Review is a normal product opinion with no policy issues.'},
    },
    "moderation_action": {
        "type": "choice",
        "instructions": 'What moderation action should be taken?',
        "criteria": {'publish_as_is': 'No violation; publish normally.', 'edit_or_reject': 'Remove promotional content or reject the review.', 'flag_account_for_review': 'Pattern suggests this account may be posting spam reviews regularly.'},
    },
    "authenticity_risk": {
        "type": "score",
        "instructions": 'How likely is this review to be inauthentic (incentivized or bot-generated)?',
        "criteria": ['Low', 'Moderate', 'High', 'Very high'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Retail / E-commerce — Product review moderation", 'Product review submission', res.answers)
