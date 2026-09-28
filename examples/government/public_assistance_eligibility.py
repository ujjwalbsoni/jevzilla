"""Government: Public Assistance Eligibility Verification

Gate: Does applicant meet eligibility criteria?
Route: Which assistance track? (Approved, Conditional, Deny)
Priority: What's the application processing level?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "program": "Emergency rental assistance",
    "household_size": 3,
    "income": "$2,400/month (120% of poverty line)",
    "employment_status": "1 employed, 1 underemployed, spouse laid off 3 months ago",
    "housing_cost": "$1,200/month rent, 50% of income",
    "missed_payments": "2 months behind on rent",
    "documentation": "All required documents provided, verified",
    "prior_assistance": "No prior rental assistance in past 12 months",
}

QUESTIONS = {
    "eligible": noul("Does applicant meet eligibility criteria?"),
    "track": choice("Assistance track?", {
        "approved": "Approved for full assistance",
        "conditional": "Conditional approval pending verification",
        "deny": "Does not meet criteria",
    }),
    "level": score("Processing level?", ["Routine", "Standard review", "Senior review", "Director review"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
