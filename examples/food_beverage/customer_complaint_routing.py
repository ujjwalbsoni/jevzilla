"""Food & Beverage: Customer Complaint Routing & Resolution

Gate: Does complaint warrant formal investigation?
Route: Which resolution path? (Staff apologize, Refund, Comped meal, Investigation)
Priority: What's the complaint severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "complaint": "Food arrived cold, undercooked in center",
    "customer_type": "Loyal regular, 20+ visits this year",
    "prior_issues": "No prior complaints on record",
    "meal_cost": "$28",
    "handling": "Server apologized, offered replacement",
    "customer_response": "Declined replacement, asked for refund",
    "tone": "Polite but firm, considering leaving negative review",
}

QUESTIONS = {
    "formal_investigation": noul("Does complaint warrant formal investigation?"),
    "resolution": choice("Resolution path?", {
        "apologize": "Staff apology, goodwill gesture",
        "refund": "Full refund",
        "comped": "Comp meal credit",
        "investigate": "Full investigation + resolution",
    }),
    "severity": score("Complaint severity?", ["Minor", "Moderate", "Serious", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
