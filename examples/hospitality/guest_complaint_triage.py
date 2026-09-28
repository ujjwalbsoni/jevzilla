"""
Hospitality / Travel — Guest complaint triage.

Scenario: A hotel guest complaint comes in during their stay. JEV flags whether it needs immediate GM attention, routes the response, and scores service-recovery priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python guest_complaint_triage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'complaint': "Guest reports their room hasn't been cleaned in 2 days despite requesting housekeeping twice, and they're celebrating their anniversary during this stay."}

QUESTIONS = {
    "needs_gm_attention": {
        "type": "noul",
        "instructions": 'Does this complaint describe a service failure significant enough to need general manager attention rather than routine front-desk handling?',
        "criteria": {"true": 'A repeated, unresolved service failure during a special-occasion stay is a recognized escalation trigger.', "false": 'Complaint can be resolved through standard front-desk service recovery.'},
    },
    "response_route": {
        "type": "choice",
        "instructions": 'How should this be handled?',
        "criteria": {'front_desk_standard_recovery': 'Standard service recovery (apology, priority cleaning).', 'manager_personal_followup': "Warrants a manager's personal follow-up given the repeated failure.", 'gm_comp_and_upgrade_offer': 'Special occasion plus repeated failure warrants a GM-level gesture (comp/upgrade).'},
    },
    "priority": {
        "type": "score",
        "instructions": 'How should this be prioritized for resolution?',
        "criteria": ['Low', 'Normal', 'High', 'Immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Hospitality / Travel — Guest complaint triage", 'In-stay guest complaint', res.answers)
