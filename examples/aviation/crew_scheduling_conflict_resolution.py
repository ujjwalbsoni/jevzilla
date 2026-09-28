"""Aviation: Crew Scheduling Conflict Resolution

Gate: Can conflict be resolved within regulations?
Route: Which resolution strategy? (Reassign, Overtime, Delay, Cancel)
Priority: What's the conflict complexity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "conflict": "Captain scheduled for 2 flights exceeds duty limit",
    "root_cause": "Earlier flight delayed 90 minutes due to weather",
    "first_flight": "Completed safely, crew duty 9 hours so far",
    "second_flight": "Scheduled 6-hour international route",
    "regulation": "FAA duty limit 10 hours (12 with allowances)",
    "available_crew": "One captain on reserve, 45 min away",
    "passenger_count": "145 passengers already boarded",
}

QUESTIONS = {
    "can_resolve": noul("Can conflict be resolved within regulations?"),
    "strategy": choice("Resolution strategy?", {
        "reassign": "Reassign captain to reserve crew",
        "overtime": "Operate within duty limits (regulatory allowance)",
        "delay": "Delay flight 45 minutes for crew relief",
        "cancel": "Cancel flight",
    }),
    "complexity": score("Conflict complexity?", ["Simple", "Moderate", "Complex", "Very complex"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
