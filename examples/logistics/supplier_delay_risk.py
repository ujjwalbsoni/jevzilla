"""
Logistics / Supply Chain — Supplier delay risk review.

Scenario: A supplier's shipment status is behind schedule. JEV flags whether it threatens production, routes escalation, and scores overall supplier reliability risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python supplier_delay_risk.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'supplier': 'Tier 1 electronics component supplier', 'notes': "Shipment is now 9 days late against a promised date, with the supplier citing a 'temporary capacity issue' and no firm new ship date provided."}

QUESTIONS = {
    "threatens_production": {
        "type": "noul",
        "instructions": 'Does this delay put downstream production at risk given typical safety-stock buffers?',
        "criteria": {"true": 'A 9-day delay with no firm new date is a recognized threat to production continuity.', "false": 'Delay is within buffer stock and does not threaten production.'},
    },
    "escalation_route": {
        "type": "choice",
        "instructions": 'How should this be escalated?',
        "criteria": {'monitor_no_action': 'Within buffer; monitor only.', 'procurement_escalation_call': 'Needs a direct escalation call with the supplier.', 'activate_backup_supplier': 'Risk is high enough to activate a backup source now.'},
    },
    "reliability_risk": {
        "type": "score",
        "instructions": "How should this supplier's reliability risk be rated going forward?",
        "criteria": ['Low', 'Moderate', 'High', 'Consider replacing'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Logistics / Supply Chain — Supplier delay risk review", 'Supplier shipment 9 days late', res.answers)
