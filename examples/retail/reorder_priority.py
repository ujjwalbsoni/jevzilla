"""
Retail / E-commerce — Inventory reorder priority.

Scenario: A SKU's stock level and sales velocity are reviewed. JEV flags whether it's at stockout risk, routes the reorder decision, and scores reorder urgency.

Run:
    set OPENROUTER_API_KEY=your-key
    python reorder_priority.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'sku': "Best-selling kids' rain boots, size 8", 'notes': '12 units left in stock. Selling 8-10 units per day this week due to seasonal demand. Supplier lead time is currently 18 days.'}

QUESTIONS = {
    "stockout_risk": {
        "type": "noul",
        "instructions": 'Given current stock and sales velocity, is this SKU at meaningful risk of stocking out before a standard reorder would arrive?',
        "criteria": {"true": 'At current velocity, stock will run out in roughly 1-2 days, far inside the 18-day lead time.', "false": 'Current stock comfortably covers demand through the reorder lead time.'},
    },
    "reorder_decision": {
        "type": "choice",
        "instructions": 'What reorder action should be taken?',
        "criteria": {'standard_reorder_cycle': 'No urgency; reorder on the normal schedule.', 'expedited_reorder': 'Should reorder now, possibly with expedited shipping.', 'escalate_to_category_manager': 'Demand spike may need a larger-than-normal reorder decision.'},
    },
    "urgency": {
        "type": "score",
        "instructions": 'How urgent is this reorder?',
        "criteria": ['Low', 'This week', 'Today', 'Immediate - stockout imminent'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Retail / E-commerce — Inventory reorder priority", "SKU inventory review: kids' rain boots size 8", res.answers)
