"""
Hospitality / Travel — Overbooking resolution review.

Scenario: The property is overbooked for tonight. JEV flags which reservation type to prioritize walking, routes the resolution process, and scores guest-relations risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python overbooking_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'situation': 'Property is overbooked by 3 rooms tonight. Options among lower-priority bookings include a loyalty member on their 12th stay and a first-time guest booked through a third-party site.'}

QUESTIONS = {
    "loyalty_member_involved": {
        "type": "noul",
        "instructions": 'Does resolving this situation risk walking a high-value loyalty guest, which typically requires extra care?',
        "criteria": {"true": 'A loyalty member with 12 stays is a recognized high-value guest requiring careful handling if walked.', "false": 'No high-value loyalty guests are involved in the affected bookings.'},
    },
    "resolution_route": {
        "type": "choice",
        "instructions": 'How should this overbooking be resolved?',
        "criteria": {'standard_walk_policy': 'No high-value guests involved; apply standard walk policy.', 'protect_loyalty_member_walk_other': "Walk the non-loyalty guest first and protect the loyalty member's room.", 'manager_personal_outreach_required': 'Given the loyalty tenure, a manager should personally handle whichever guest is walked.'},
    },
    "relations_risk": {
        "type": "score",
        "instructions": 'How much guest-relations risk does this situation carry?',
        "criteria": ['Low', 'Moderate', 'High', 'Severe - risk to loyalty relationship'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Hospitality / Travel — Overbooking resolution review", 'Overbooking resolution, 3 rooms', res.answers)
