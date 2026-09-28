"""Food & Beverage: Supplier Quality & Compliance Review

Gate: Should we continue ordering from this supplier?
Route: Which supplier status? (Approved, Probation, Discontinued)
Priority: What's the compliance risk?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "supplier": "Fresh Farms Produce Co",
    "product": "Organic vegetables, weekly delivery",
    "quality_record": "98% on-spec, 2% minor cosmetic issues",
    "timeliness": "On-time 92%, one late delivery (weather)",
    "certifications": "USDA Organic verified, food safety certified",
    "recent_recall": "None involving their products",
    "price": "Premium tier, but quality matches",
    "references": "5+ restaurants use, positive feedback",
}

QUESTIONS = {
    "continue": noul("Should we continue with this supplier?"),
    "status": choice("Supplier status?", {
        "approved": "Approved, continue current contract",
        "probation": "Probation status, 90-day review",
        "discontinued": "Discontinue relationship",
    }),
    "compliance": score("Compliance risk?", ["Low", "Acceptable", "Concern", "High risk"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
