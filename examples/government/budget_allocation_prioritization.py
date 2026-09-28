"""Government: Budget Allocation Prioritization

Gate: Should this project receive funding?
Route: Which funding tier? (Full, Partial, Waitlist)
Priority: What's the project score?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "project": "Water main replacement, Main Street",
    "cost": "$2.8M",
    "age": "Pipe installed 1952, 72 years old",
    "break_frequency": "3 breaks in past year",
    "community_impact": "High traffic area, water disruption affects 5,000 residents",
    "quality_of_life": "Frequent outages, water quality issues",
    "economic_benefit": "Estimated $500K annual savings from reduced breaks",
    "available_budget": "$8.5M (capital budget)",
}

QUESTIONS = {
    "fund": noul("Should project receive funding?"),
    "tier": choice("Funding tier?", {
        "full": "Full funding approved",
        "partial": "Partial funding, phase 1",
        "waitlist": "Waitlist for next budget cycle",
    }),
    "score": score("Project priority score?", ["Low", "Moderate", "High", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
