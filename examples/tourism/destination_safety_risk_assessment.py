"""Tourism: Destination Safety Risk Assessment

Gate: Is destination unsafe for travelers?
Route: Which guidance? (Green, Caution, Warning, Do not travel)
Priority: What's the risk level?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "destination": "Popular beach resort in Central America",
    "current_status": "Stable, tourist areas secure",
    "recent_incidents": "One petty theft incident in market area (low risk)",
    "health_concerns": "Standard precautions, dengue fever low current rate",
    "government_warnings": "None active",
    "infrastructure": "Good, reliable electricity and water",
    "local_advice": "Tourist police presence adequate",
}

QUESTIONS = {
    "unsafe": noul("Is destination unsafe?"),
    "guidance": choice("Travel guidance?", {
        "green": "Safe, normal travel advisories",
        "caution": "Exercise caution in certain areas",
        "warning": "Significant risk, limit travel",
        "donot": "Do not travel",
    }),
    "risk": score("Risk level?", ["Low", "Moderate", "High", "Severe"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
