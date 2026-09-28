"""
Logistics / Supply Chain — Shipment exception triage.

Scenario: A tracking exception fires for an in-transit shipment. JEV flags whether it's customer-impacting, routes it to the right team, and scores resolution urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python shipment_exception.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'shipment': 'LTL freight, retail customer, delivery due tomorrow', 'exception_note': 'Carrier scan shows the shipment was misrouted to the wrong regional hub, adding an estimated 2 days to transit.'}

QUESTIONS = {
    "customer_impacting": {
        "type": "noul",
        "instructions": 'Does this exception put the delivery commitment to the customer at risk?',
        "criteria": {"true": 'A 2-day delay against a delivery due tomorrow directly breaks the commitment.', "false": 'Delay does not affect the committed delivery date.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Which team should handle this exception?',
        "criteria": {'standard_tracking_update': 'No customer impact; just update tracking.', 'carrier_relations_team': 'Needs to work with the carrier on expediting or rerouting.', 'customer_notification_required': 'Customer needs proactive notification of the delay.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgently does this need to be addressed?',
        "criteria": ['Low', 'Today', 'Immediate', 'Critical - contractual penalty risk'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Logistics / Supply Chain — Shipment exception triage", 'Shipment exception: misrouted freight', res.answers)
