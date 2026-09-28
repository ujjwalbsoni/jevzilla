"""
Real Estate — Property inspection finding review.

Scenario: A routine property inspection report is reviewed. JEV flags whether a finding needs immediate action, routes it to the right owner, and scores repair urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python inspection_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'property': 'Single-family rental, annual inspection', 'finding': 'Inspector notes visible mold growth around a bathroom window frame, likely from a longstanding unaddressed seal failure.'}

QUESTIONS = {
    "immediate_action_needed": {
        "type": "noul",
        "instructions": 'Does this finding describe a condition requiring action before the next scheduled inspection cycle?',
        "criteria": {"true": 'Visible mold growth is a recognized condition requiring prompt remediation.', "false": 'Finding is minor and can wait for routine scheduling.'},
    },
    "owner_route": {
        "type": "choice",
        "instructions": 'Who should own addressing this finding?',
        "criteria": {'routine_maintenance_schedule': 'Minor; add to the routine schedule.', 'remediation_contractor_dispatch': 'Needs a specialized remediation contractor dispatched soon.', 'property_owner_notification': 'Owner should be notified given potential liability and cost.'},
    },
    "repair_urgency": {
        "type": "score",
        "instructions": 'How urgent is this repair?',
        "criteria": ['Low', 'Within 30 days', 'Within a week', 'Immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Real Estate — Property inspection finding review", 'Annual inspection finding: bathroom mold', res.answers)
