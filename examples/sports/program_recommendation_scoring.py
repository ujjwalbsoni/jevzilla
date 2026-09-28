"""Sports & Fitness: Program Recommendation Scoring

Gate: Should member participate in advanced program?
Route: Which program? (Beginner, Intermediate, Advanced, Specialized)
Priority: What's the member readiness score?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "member": "8-month member, consistent attendance",
    "current_level": "Intermediate fitness",
    "strength": "Good upper body, wants to improve flexibility",
    "injuries": "Minor lower back issue, previously resolved",
    "goals": "Functional fitness, injury prevention focus",
    "availability": "3x/week, prefers mornings",
    "motivation": "High, participates in group classes",
}

QUESTIONS = {
    "advanced_ready": noul("Is member ready for advanced program?"),
    "program": choice("Program recommendation?", {
        "beginner": "Beginner fundamentals",
        "intermediate": "Intermediate conditioning",
        "advanced": "Advanced training",
        "specialized": "Specialized (yoga, pilates, etc)",
    }),
    "readiness": score("Readiness score?", ["Not ready", "Emerging", "Ready", "Highly ready"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
