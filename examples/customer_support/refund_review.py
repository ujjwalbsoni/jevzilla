"""
Customer Support — Refund request review.

Scenario: A customer requests a refund outside the standard policy window. JEV flags whether it's a reasonable exception, routes approval, and scores customer value for the decision.

Run:
    set OPENROUTER_API_KEY=your-key
    python refund_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'request': "Customer requests a full refund on a $340 annual subscription, 60 days after purchase (policy window is 30 days), citing that they forgot to cancel before auto-renewal and haven't used the product since."}

QUESTIONS = {
    "reasonable_exception": {
        "type": "noul",
        "instructions": 'Does this request show characteristics commonly treated as a reasonable exception (e.g. clear non-use, past auto-renewal confusion) rather than policy abuse?',
        "criteria": {"true": 'Auto-renewal confusion with documented non-use is a commonly accepted exception pattern.', "false": 'Request does not show characteristics of a reasonable exception.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'How should this request be handled?',
        "criteria": {'agent_can_approve': 'Common, low-risk exception; agent can approve directly.', 'manager_approval_needed': 'Outside policy enough to need manager sign-off.', 'deny_per_policy': 'Should be denied per standard policy with no exception.'},
    },
    "customer_value": {
        "type": "score",
        "instructions": 'How should this customer be weighed in the decision?',
        "criteria": ['Standard', 'Good history', 'High value', 'Long-tenured / high value'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Customer Support — Refund request review", 'Refund request, 30 days past policy window', res.answers)
