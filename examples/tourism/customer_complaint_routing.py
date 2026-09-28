"""Tourism: Customer Complaint Routing & Resolution

Gate: Does complaint warrant refund?
Route: Which resolution? (Apologize, Discount, Partial refund, Full refund)
Priority: What's the complaint severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "complaint": "Hotel room not as advertised, dirty carpet, noise at night",
    "booking_cost": "$2,800 for 5-night stay",
    "actions_taken": "Moved guest to different room day 2",
    "guest_satisfaction": "Partially satisfied with room change",
    "guest_type": "First-time guest, positive history with brand",
    "prior_issues": "None reported",
    "impact": "Lost 1.5 nights of quality experience",
}

QUESTIONS = {
    "warrant_refund": noul("Does complaint warrant refund?"),
    "resolution": choice("Resolution option?", {
        "apologize": "Formal apology, goodwill gesture",
        "discount": "10-20% discount on future stay",
        "partial": "Partial refund (25-50%)",
        "full": "Full refund",
    }),
    "severity": score("Complaint severity?", ["Minor", "Moderate", "Significant", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
