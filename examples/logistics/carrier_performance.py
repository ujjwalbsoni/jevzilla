"""
Logistics / Supply Chain — Carrier performance review.

Scenario: A carrier's monthly performance is reviewed against contract SLAs. JEV flags whether it's an SLA breach, routes the response, and scores overall carrier risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python carrier_performance.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'carrier': 'Regional trucking partner', 'performance_note': 'On-time delivery rate dropped to 78% this month against a contracted 95% SLA, with damage claims also up 3x month-over-month.'}

QUESTIONS = {
    "sla_breach": {
        "type": "noul",
        "instructions": 'Does this performance data represent a breach of the contracted SLA?',
        "criteria": {"true": '78% on-time against a 95% SLA is a clear breach.', "false": 'Performance is within or close to contracted SLA levels.'},
    },
    "response_route": {
        "type": "choice",
        "instructions": 'How should this be addressed with the carrier?',
        "criteria": {'routine_scorecard_note': 'Minor dip; note on the routine scorecard.', 'formal_sla_breach_notice': 'Breach warrants a formal notice and corrective action plan.', 'begin_alternate_carrier_sourcing': 'Performance and damage trend together warrant starting to source alternatives.'},
    },
    "carrier_risk": {
        "type": "score",
        "instructions": "What is this carrier's overall risk rating going forward?",
        "criteria": ['Low', 'Watch', 'High', 'At risk of contract termination'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Logistics / Supply Chain — Carrier performance review", 'Monthly carrier performance review', res.answers)
