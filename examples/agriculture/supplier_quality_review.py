"""Agriculture: Supplier Quality & Input Vetting

Gate: Should we source from this supplier?
Route: Which supplier tier? (Preferred, Acceptable, Needs review)
Priority: What's the quality/risk score?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "supplier": "Midwest Fertilizer Co",
    "product": "Urea 46% nitrogen",
    "quality_tests": "Recent batch tested 46.2% nitrogen (spec 46%)",
    "delivery_record": "On-time 95% of year, one late shipment",
    "price": "Competitive, $5 lower per ton than market",
    "certifications": "ISO certified, organic inputs available",
    "references": "3 local farms use, satisfaction high",
}

QUESTIONS = {
    "approve": noul("Should we source from this supplier?"),
    "tier": choice("Supplier tier?", {
        "preferred": "Preferred supplier",
        "acceptable": "Acceptable, conditional approval",
        "review": "Needs additional review",
    }),
    "quality_score": score("Quality/risk score?", ["Low risk", "Acceptable", "Caution", "High risk"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
