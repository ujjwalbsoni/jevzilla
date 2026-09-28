"""
Manufacturing — Supplier quality audit finding.

Scenario: An auditor logs a finding from a supplier site visit. JEV flags whether it's a critical nonconformance, routes the corrective-action owner, and scores supplier risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python supplier_audit.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'supplier': 'Precision Metal Works Ltd.', 'finding': 'Calibration records for 3 of 12 sampled measurement devices were missing or expired by more than 60 days. No documented root-cause process for past deviations found.'}

QUESTIONS = {
    "critical_finding": {
        "type": "noul",
        "instructions": 'Is this a critical nonconformance requiring supplier requalification before further shipments are accepted?',
        "criteria": {"true": 'Missing calibration and no corrective-action process together indicate systemic quality control gaps.', "false": 'Isolated documentation gap that does not indicate systemic risk.'},
    },
    "corrective_owner": {
        "type": "choice",
        "instructions": 'Who should own driving the corrective action?',
        "criteria": {'supplier_quality_team': 'Standard supplier corrective-action process.', 'procurement_leadership': 'Risk to supply continuity; needs sourcing-level decision.', 'customer_notification_required': 'Downstream product quality may already be affected.'},
    },
    "supplier_risk": {
        "type": "score",
        "instructions": "What is this supplier's overall quality risk rating after this finding?",
        "criteria": ['Low', 'Watch', 'High', 'Suspend sourcing'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Manufacturing — Supplier quality audit finding", 'Audit finding at Precision Metal Works Ltd.', res.answers)
