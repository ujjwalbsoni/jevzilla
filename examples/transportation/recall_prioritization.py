"""Transportation: Vehicle Recall Prioritization

Gate: Should this vehicle be recalled immediately?
Route: Which recall action? (Immediate service, Scheduled appointment, Monitor)
Priority: What's the safety risk?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "vehicle": "2023 sedan in customer fleet (5 units owned)",
    "recall_issue": "Potential airbag deployment defect",
    "risk_level": "Safety issue, injury potential",
    "vehicles_affected": "487,000 nationwide, 12 in owner's fleet",
    "current_status": "No reported incidents",
    "airbag_function": "Currently passing diagnostics",
    "replacement_part_availability": "Available immediately",
}

QUESTIONS = {
    "immediate_recall": noul("Should vehicle be recalled immediately?"),
    "action": choice("Recall action?", {
        "immediate": "Immediate service stop, recall now",
        "scheduled": "Schedule urgent appointment",
        "monitor": "Monitor and schedule within 30 days",
    }),
    "safety_risk": score("Safety risk level?", ["Low", "Moderate", "High", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
