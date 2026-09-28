"""Tourism: Travel Insurance Claim Review & Approval

Gate: Should insurance claim be approved?
Route: Which tier? (Full approval, Partial, Investigate, Deny)
Priority: What's the claim validity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "claim": "Trip cancellation due to illness",
    "trip_cost": "$4,200",
    "policy": "Comprehensive coverage, pre-existing condition exclusion applies",
    "pre_condition": "Claimed migraine 2 months prior to trip",
    "medical_documentation": "Doctor's note states sudden acute migraine day before trip",
    "claim_timing": "Filed within 30 days",
    "policy_status": "Premium paid, active",
}

QUESTIONS = {
    "approve": noul("Should claim be approved?"),
    "tier": choice("Decision tier?", {
        "full": "Full approval",
        "partial": "Partial reimbursement",
        "investigate": "Investigate further",
        "deny": "Deny claim",
    }),
    "validity": score("Claim validity?", ["Weak", "Moderate", "Strong", "Definite"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
