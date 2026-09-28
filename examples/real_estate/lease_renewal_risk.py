"""
Real Estate — Lease renewal risk review.

Scenario: A property manager reviews a tenant's file ahead of lease renewal. JEV flags churn risk, routes the renewal approach, and scores tenant value.

Run:
    set OPENROUTER_API_KEY=your-key
    python lease_renewal_risk.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'tenant': '2-year tenant, on-time payment history', 'notes': "Tenant called twice this month asking about the neighborhood's other rental listings and whether the lease has an early-termination clause."}

QUESTIONS = {
    "likely_to_leave": {
        "type": "noul",
        "instructions": 'Do these signals suggest the tenant is likely considering not renewing?',
        "criteria": {"true": 'Asking about other listings and early termination are recognized moving-intent signals.', "false": 'Signals do not suggest an intent to leave.'},
    },
    "renewal_approach": {
        "type": "choice",
        "instructions": 'How should the renewal conversation be approached?',
        "criteria": {'standard_renewal_offer': 'Low risk; send the standard renewal offer.', 'proactive_retention_call': 'Signals warrant a proactive call to address concerns.', 'prepare_for_vacancy': 'Signals are strong enough to start preparing for a possible vacancy.'},
    },
    "tenant_value": {
        "type": "score",
        "instructions": 'How should this tenant be valued for retention effort?',
        "criteria": ['Standard', 'Good - reliable payer', 'High value - long tenure', 'Priority retain'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Real Estate — Lease renewal risk review", 'Lease renewal review, 2-year tenant', res.answers)
