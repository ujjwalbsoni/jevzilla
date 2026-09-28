"""
Insurance — Subrogation opportunity review.

Scenario: A closed claim is reviewed for potential subrogation. JEV flags whether recovery looks viable, routes it to the right team, and scores recovery-potential priority.

Run:
    set OPENROUTER_API_KEY=your-key
    python subrogation_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'claim_summary': 'Auto claim paid $22,000 for water damage caused by a burst pipe. Building maintenance records show the pipe had a documented, unaddressed leak reported by a tenant 3 weeks before the burst.'}

QUESTIONS = {
    "subrogation_viable": {
        "type": "noul",
        "instructions": "Does this claim show a viable subrogation opportunity against a third party (e.g. property management's failure to address a known issue)?",
        "criteria": {"true": 'A documented, unaddressed prior report of the issue supports a negligence-based recovery claim.', "false": 'No clear third-party liability is indicated.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Who should pursue this subrogation opportunity?',
        "criteria": {'no_action_low_recovery': 'Recovery potential is too low to pursue.', 'internal_subrogation_team': 'Standard recovery case for the internal team.', 'outside_subrogation_counsel': 'Recovery amount and liability complexity warrant outside counsel.'},
    },
    "recovery_priority": {
        "type": "score",
        "instructions": 'How should this be prioritized for pursuit?',
        "criteria": ['Low', 'Moderate', 'High', 'Pursue immediately'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Insurance — Subrogation opportunity review", 'Closed claim: water damage, $22,000 paid', res.answers)
