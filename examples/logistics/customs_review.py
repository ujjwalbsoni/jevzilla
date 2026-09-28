"""
Logistics / Supply Chain — Customs document review.

Scenario: A cross-border shipment's paperwork is reviewed before clearance. JEV flags missing documentation, routes it for correction, and scores clearance-delay risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python customs_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'shipment': 'Import shipment, industrial equipment', 'notes': "Commercial invoice value doesn't match the packing list quantities, and the HS code listed doesn't match the product description provided."}

QUESTIONS = {
    "documentation_error": {
        "type": "noul",
        "instructions": 'Does this paperwork contain discrepancies likely to trigger a customs hold?',
        "criteria": {"true": 'Mismatched invoice/packing list values and an inconsistent HS code are recognized customs red flags.', "false": 'Documentation appears consistent and complete.'},
    },
    "correction_route": {
        "type": "choice",
        "instructions": 'What should happen next?',
        "criteria": {'submit_as_is': 'No discrepancies; submit for clearance.', 'correct_before_submission': 'Correct the paperwork before submitting to avoid a hold.', 'customs_broker_consultation': 'Discrepancy is significant enough to consult the customs broker first.'},
    },
    "delay_risk": {
        "type": "score",
        "instructions": 'What is the risk of a customs clearance delay?',
        "criteria": ['Low', 'Moderate', 'High', 'Likely hold'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Logistics / Supply Chain — Customs document review", 'Customs paperwork review, industrial equipment import', res.answers)
