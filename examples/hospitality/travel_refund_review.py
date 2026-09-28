"""
Hospitality / Travel — Travel refund request review.

Scenario: A traveler requests a refund outside standard cancellation policy. JEV flags whether it's a reasonable exception, routes approval, and scores customer value.

Run:
    set OPENROUTER_API_KEY=your-key
    python travel_refund_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'request': "Customer requests a refund on a non-refundable flight booking, citing a medical emergency 2 days before departure, with a doctor's note attached."}

QUESTIONS = {
    "reasonable_exception": {
        "type": "noul",
        "instructions": 'Does this request show documentation and circumstances commonly treated as a reasonable exception to non-refundable policy?',
        "criteria": {"true": 'A documented medical emergency close to departure is a widely recognized exception case.', "false": 'Request lacks the documentation typically required for an exception.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'How should this request be handled?',
        "criteria": {'agent_can_approve': 'Documentation supports a standard compassionate exception; agent can approve.', 'request_additional_documentation': 'Needs clearer or additional documentation before approving.', 'deny_per_policy': 'Does not meet exception criteria; deny per policy.'},
    },
    "customer_value": {
        "type": "score",
        "instructions": 'How should this customer be weighed in the decision?',
        "criteria": ['Standard', 'Repeat customer', 'High value', 'Elite/loyalty status'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Hospitality / Travel — Travel refund request review", 'Refund request, non-refundable fare', res.answers)
