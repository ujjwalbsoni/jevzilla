"""
Retail / E-commerce — Customer complaint routing.

Scenario: A customer service message comes in through chat. JEV flags severity, routes it to the right team, and scores priority for the support queue.

Run:
    set OPENROUTER_API_KEY=your-key
    python complaint_routing.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'message': "I ordered a birthday gift for my daughter's party tomorrow and tracking shows it's still sitting at the origin facility, 3 days after it was supposed to ship."}

QUESTIONS = {
    "time_critical": {
        "type": "noul",
        "instructions": 'Does this message describe a time-critical situation tied to a specific upcoming event?',
        "criteria": {"true": 'Explicitly references a deadline (party tomorrow) tied to the order.', "false": 'No specific time-critical deadline is mentioned.'},
    },
    "route_to": {
        "type": "choice",
        "instructions": 'Which team should handle this?',
        "criteria": {'standard_support_queue': 'Normal shipping delay inquiry.', 'expedited_shipping_team': 'Time-critical; needs expedite or replacement options explored.', 'escalation_to_supervisor': 'May need a supervisor to authorize compensation or rush shipping.'},
    },
    "priority": {
        "type": "score",
        "instructions": 'How should this be prioritized in the support queue?',
        "criteria": ['Low', 'Normal', 'High', 'Immediate'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Retail / E-commerce — Customer complaint routing", 'Customer chat message', res.answers)
