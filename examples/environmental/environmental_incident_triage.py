"""Environmental: Environmental Incident Triage & Response

Gate: Is this an environmental emergency?
Route: Which response? (Monitor, Contain, Remediate, Escalate)
Priority: What's the environmental impact?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "incident": "Small fuel spill detected at gas station",
    "volume": "Approximately 10 gallons",
    "location": "Concrete pad, contained to small area",
    "weather": "Dry conditions, no rain predicted",
    "water_proximity": "Storm drain 30 feet away, sealed",
    "action_taken": "Spill kit deployed, area marked",
    "response_time": "Emergency services arrived within 15 minutes",
}

QUESTIONS = {
    "emergency": noul("Is this environmental emergency?"),
    "response": choice("Response level?", {
        "monitor": "Monitor, routine cleanup",
        "contain": "Activate containment protocols",
        "remediate": "Immediate remediation required",
        "escalate": "Escalate to EPA",
    }),
    "impact": score("Environmental impact?", ["Minimal", "Minor", "Moderate", "Major"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
