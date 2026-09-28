"""
Hospitality / Travel — Online review response priority.

Scenario: A public review of a property is posted. JEV flags whether it needs a rapid public response, routes it, and scores reputational impact.

Run:
    set OPENROUTER_API_KEY=your-key
    python review_response_priority.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'review': "1-star review states: 'Found a cockroach in the bathroom. Staff seemed unsurprised, like this happens often. Would never stay here again and warn others.'", 'platform': 'Major review site, property has 1,200+ reviews'}

QUESTIONS = {
    "needs_rapid_response": {
        "type": "noul",
        "instructions": 'Does this review describe an issue serious enough (pest, safety/hygiene) to need a prompt public response?',
        "criteria": {"true": 'A specific pest complaint with an implication of a recurring problem is a high-impact hygiene concern.', "false": 'Review describes a general or minor dissatisfaction.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'How should this be routed?',
        "criteria": {'standard_response_queue': 'General feedback; standard response timeline.', 'gm_priority_response': 'Hygiene complaint warrants a prompt, personal GM response.', 'operations_investigation_required': 'Implication of a recurring pest issue warrants an operational investigation, not just a reply.'},
    },
    "reputational_impact": {
        "type": "score",
        "instructions": 'How much reputational impact could this review have if unaddressed?',
        "criteria": ['Low', 'Moderate', 'High', 'Severe'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Hospitality / Travel — Online review response priority", '1-star public review', res.answers)
