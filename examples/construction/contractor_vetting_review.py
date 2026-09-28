"""Construction: Contractor Vetting & Vendor Risk Assessment

Gate: Should this contractor be approved?
Route: Which approval level is needed? (Standard, Senior review, Legal review)
Priority: What's the overall risk score?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "company_name": "BuildRight Solutions LLC",
    "registration_status": "Active, 8 years in business",
    "insurance": "General liability $2M, workers comp valid",
    "safety_record": "One minor incident 3 years ago, remediated",
    "references": "3 positive refs from past 2 years",
    "financial_health": "Good credit score 720+",
    "regulatory_flags": "None",
}

QUESTIONS = {
    "approve": noul("Should this contractor be approved?"),
    "approval_route": choice("Approval level needed?", {
        "standard": "Standard approval (PM)",
        "senior": "Senior review (Manager)",
        "legal": "Legal review required",
    }),
    "risk_score": score("Overall vendor risk?", ["Low", "Medium", "High", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
