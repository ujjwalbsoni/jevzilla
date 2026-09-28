"""Transportation: Warranty Claim Review & Approval

Gate: Should this warranty claim be approved?
Route: Which claim tier? (Standard approval, Manager review, Dispute)
Priority: What's the claim validity score?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "claim_id": "WC-2024-08765",
    "vehicle": "2023 Toyota Highlander, 22,000 miles",
    "warranty_status": "In-warranty, 3/36 remaining",
    "issue": "Transmission slipping intermittently",
    "service_history": "Regular maintenance at authorized dealer",
    "damage_cause": "Manufacturing defect (suspected), no accident history",
    "repair_cost": "$3,200",
    "dealer_assessment": "Confirmed transmission fault, parts replaced",
}

QUESTIONS = {
    "approve": noul("Should warranty claim be approved?"),
    "tier": choice("Claim tier?", {
        "standard": "Standard approval",
        "manager": "Manager review required",
        "dispute": "Claim dispute - investigate further",
    }),
    "validity": score("Claim validity?", ["Weak", "Moderate", "Strong", "Definite"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
