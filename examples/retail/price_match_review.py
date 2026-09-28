"""
Retail / E-commerce — Price match request review.

Scenario: A customer requests a price match after purchase. JEV flags whether it meets policy, routes approval, and scores customer value for follow-up.

Run:
    set OPENROUTER_API_KEY=your-key
    python price_match_review.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'request': 'Customer purchased a TV for $899 three days ago; found the same model for $749 at a competitor today, and requests a price match.', 'policy_note': 'Standard price-match policy covers requests within 14 days for identical in-stock items from listed approved competitors.'}

QUESTIONS = {
    "meets_policy": {
        "type": "noul",
        "instructions": 'Does this request fall within the stated price-match policy terms?',
        "criteria": {"true": 'Within the 14-day window for an identical item is consistent with standard policy.', "false": 'Request falls outside stated policy terms.'},
    },
    "approval_route": {
        "type": "choice",
        "instructions": 'How should this request be handled?',
        "criteria": {'auto_approve_refund_difference': 'Meets policy; process automatically.', 'agent_verification_needed': 'Needs an agent to verify the competitor price and item match.', 'manager_exception_review': 'Falls outside policy but may warrant a goodwill exception.'},
    },
    "customer_value": {
        "type": "score",
        "instructions": 'How should this customer be prioritized for retention follow-up?',
        "criteria": ['Standard', 'Valued repeat customer', 'High lifetime value', 'At-risk of churn'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Retail / E-commerce — Price match request review", 'Price match request, $150 difference', res.answers)
