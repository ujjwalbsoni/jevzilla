"""
Media / Entertainment — Ad placement brand safety review.

Scenario: An ad is about to be placed alongside a piece of content. JEV flags whether the content is brand-safe, routes the placement decision, and scores risk for the advertiser relationship.

Run:
    set OPENROUTER_API_KEY=your-key
    python brand_safety_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'content': "News-adjacent video discussing a developing violent crime story, ad slot is for a children's toy brand.", 'context': 'Content itself is factual reporting, not graphic, but topic is sensitive.'}

QUESTIONS = {
    "brand_mismatch_risk": {
        "type": "noul",
        "instructions": "Does this content topic present a mismatch risk for this specific advertiser's brand (sensitive topic + children's brand)?",
        "criteria": {"true": "Sensitive crime-related content next to a children's brand is a recognized brand-safety mismatch, regardless of factual tone.", "false": 'Content topic is a reasonable match for this advertiser.'},
    },
    "placement_route": {
        "type": "choice",
        "instructions": 'How should this placement be handled?',
        "criteria": {'proceed_with_placement': 'No mismatch; proceed as planned.', 'reroute_to_different_ad_slot': 'Reroute this advertiser to different, better-matched content.', 'flag_for_advertiser_approval': 'Mismatch is borderline enough to require advertiser sign-off before placing.'},
    },
    "advertiser_risk": {
        "type": "score",
        "instructions": 'How much risk does this placement pose to the advertiser relationship?',
        "criteria": ['Low', 'Moderate', 'High', 'Severe - likely complaint'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Media / Entertainment — Ad placement brand safety review", 'Ad placement review: news content + toy brand', res.answers)
