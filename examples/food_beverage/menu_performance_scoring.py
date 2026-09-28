"""Food & Beverage: Menu Item Performance Scoring & Recommendations

Gate: Should menu item be retained or modified?
Route: Which action? (Keep, Modify recipe, Reprice, Remove)
Priority: What's the performance level?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "item": "Signature burger",
    "popularity": "Ordered 15% of all meals (top 5)",
    "profit_margin": "28% margin (healthy)",
    "food_cost": "$5.50, selling $18",
    "waste_rate": "3% (low)",
    "customer_feedback": "4.2/5 stars, 80 reviews, consistent praise",
    "labor_time": "8 minutes average (efficient)",
    "supply_reliability": "Consistent supply chain",
}

QUESTIONS = {
    "retain": noul("Should menu item be retained?"),
    "action": choice("Recommended action?", {
        "keep": "Keep as-is, maintain menu position",
        "modify": "Modify recipe or presentation",
        "reprice": "Adjust pricing",
        "remove": "Remove from menu",
    }),
    "performance": score("Performance level?", ["Below average", "Average", "Good", "Excellent"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
