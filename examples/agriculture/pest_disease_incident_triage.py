"""Agriculture: Pest/Disease Incident Triage

Gate: Is pest/disease outbreak a concern?
Route: Which intervention required? (Monitor, Treat, Escalate)
Priority: What's the infestation severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "crop": "Soybean, 150 acres",
    "detection": "Japanese beetles observed at field edge",
    "count": "15-20 beetles per plant in 5% of field",
    "damage": "Minor leaf damage, <1% defoliation",
    "history": "Same field had minor pressure 2 years ago",
    "weather": "Hot and dry, favorable for beetle breeding",
    "threshold": "Economic threshold is 30 beetles per plant",
}

QUESTIONS = {
    "is_concern": noul("Is this pest outbreak a concern?"),
    "intervention": choice("Intervention required?", {
        "monitor": "Monitor closely, scout daily",
        "treat": "Apply targeted treatment",
        "escalate": "Escalate to regional entomologist",
    }),
    "severity": score("Infestation severity?", ["Minimal", "Low", "Moderate", "High"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
