"""Sports & Fitness: Gym Membership Eligibility & Approval

Gate: Should membership be approved?
Route: Which tier? (Standard, Discounted, Conditional, Declined)
Priority: What's the membership fit score?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "applicant_age": 45,
    "fitness_goal": "General wellness, strength training",
    "prior_experience": "Gym membership 5 years ago, 2-year gap",
    "health_status": "Good health, doctor clearance obtained",
    "availability": "Weekday mornings and weekend access",
    "budget": "Standard tier pricing acceptable",
    "motivation": "High, specific goals documented",
}

QUESTIONS = {
    "approve": noul("Should membership be approved?"),
    "tier": choice("Membership tier?", {
        "standard": "Standard membership",
        "discount": "Discounted rate (new member)",
        "conditional": "Conditional (introductory period)",
        "decline": "Decline membership",
    }),
    "fit_score": score("Membership fit score?", ["Low", "Moderate", "Good", "Excellent"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
