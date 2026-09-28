"""Tourism: Booking Fraud Detection & Review

Gate: Should booking be flagged for review?
Route: Which action? (Approve, Conditional hold, Block)
Priority: What's the fraud risk?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "booking": "Hotel reservation, 5 rooms for conference",
    "total": "$8,500",
    "guest_profile": "Corporate account, 3-year history",
    "payment": "Credit card (verified business card)",
    "booking_pattern": "Consistent with prior conference bookings",
    "red_flags": "Large volume but typical for corporate",
    "lead_time": "6 weeks advance, normal",
    "cancellation_history": "Rarely cancels",
}

QUESTIONS = {
    "flag_review": noul("Should booking be flagged for review?"),
    "action": choice("Action?", {
        "approve": "Approve booking",
        "hold": "Conditional hold, call to verify",
        "block": "Block and investigate",
    }),
    "fraud_risk": score("Fraud risk?", ["Very low", "Low", "Moderate", "High"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
