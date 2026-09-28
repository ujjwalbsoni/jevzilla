"""
Healthcare Ops — Appointment no-show risk flag.

Scenario: A scheduling system reviews a patient's appointment history and a reminder response. JEV flags no-show risk, routes an outreach action, and scores priority for the scheduler's callback list.

Run:
    set OPENROUTER_API_KEY=your-key
    python no_show_risk.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'appointment_type': 'Follow-up, non-urgent', 'history_note': 'Patient has missed 2 of the last 3 scheduled appointments and has not responded to the automated reminder text sent yesterday.'}

QUESTIONS = {
    "high_no_show_risk": {
        "type": "noul",
        "instructions": "Does this patient's pattern indicate meaningfully elevated risk of a no-show tomorrow?",
        "criteria": {"true": 'Recent missed-appointment pattern plus no reminder response are recognized no-show indicators.', "false": 'Pattern does not indicate elevated risk.'},
    },
    "outreach_action": {
        "type": "choice",
        "instructions": 'What outreach should the scheduling team take?',
        "criteria": {'no_action_needed': 'Low risk; proceed as normal.', 'phone_call_reminder': 'Elevated risk; a personal call may help.', 'overbook_slot': 'High risk; consider double-booking this slot.'},
    },
    "callback_priority": {
        "type": "score",
        "instructions": "How should this be prioritized on today's scheduler callback list?",
        "criteria": ['Low', 'Normal', 'High', 'Call now'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Healthcare Ops — Appointment no-show risk flag", 'Follow-up appointment, tomorrow 2pm', res.answers)
