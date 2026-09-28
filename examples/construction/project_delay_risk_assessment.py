"""Construction: Project Delay Risk Assessment

Gate: Is project at risk of significant delay?
Route: Which mitigation strategy? (Monitor, Accelerate, Rescope)
Priority: What's the delay impact?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "project_name": "Downtown Office Complex",
    "timeline_status": "2 weeks behind schedule",
    "current_phase": "Foundation work (40% complete)",
    "weather_forecast": "Heavy rain expected next week",
    "material_supply": "Steel delivery delayed by 1 week",
    "crew_availability": "2 crew members out sick, replacements sourced",
    "budget_impact": "Current delay cost ~$50K per day",
}

QUESTIONS = {
    "at_risk": noul("Is project at significant delay risk?"),
    "mitigation": choice("Recommended strategy?", {
        "monitor": "Monitor closely, adjust as needed",
        "accelerate": "Accelerate non-critical path",
        "rescope": "Rescope deliverables",
    }),
    "impact": score("Potential delay impact?", ["Minimal", "Moderate", "Significant", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
