"""Sports & Fitness: Equipment Maintenance Prioritization

Gate: Does equipment need immediate maintenance?
Route: Which action? (Preventive, Corrective, Replace, Out of service)
Priority: What's the maintenance urgency?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "equipment": "Commercial treadmill",
    "model": "Life Fitness 95T",
    "age": "4 years old, well-maintained",
    "issue": "Display intermittent, electrical connector loose",
    "usage": "Heavy use, 40+ members/day",
    "safety": "Still functional and safe to use",
    "backup": "One other treadmill available",
    "repair_cost": "$250 vs replacement $8,000",
}

QUESTIONS = {
    "needs_maintenance": noul("Does equipment need immediate maintenance?"),
    "action": choice("Action?", {
        "preventive": "Schedule preventive maintenance",
        "corrective": "Corrective repair",
        "replace": "Replace equipment",
        "outofservice": "Take out of service",
    }),
    "urgency": score("Maintenance urgency?", ["Routine", "Soon", "This week", "Immediate"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
