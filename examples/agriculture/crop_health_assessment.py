"""Agriculture: Crop Health Assessment & Intervention Decision

Gate: Does crop need intervention?
Route: Which intervention type? (Fertilizer, Pesticide, Irrigation, Other)
Priority: What's the intervention urgency?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "crop": "Corn field, 200 acres",
    "growth_stage": "V6 (6 leaves visible)",
    "soil_condition": "Adequate moisture, slightly low nitrogen",
    "pest_pressure": "Low aphid presence, well within threshold",
    "disease_risk": "No visible disease symptoms",
    "weather": "Warm, adequate rainfall",
    "yield_projection": "On track for 160 bu/acre",
}

QUESTIONS = {
    "needs_intervention": noul("Does crop need intervention?"),
    "intervention_type": choice("Intervention type?", {
        "fertilizer": "Apply nitrogen fertilizer",
        "pesticide": "Apply preventive pesticide",
        "irrigation": "Increase irrigation",
        "monitor": "Continue monitoring",
    }),
    "urgency": score("Intervention urgency?", ["Monitor", "This week", "Next 3 days", "Immediate"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
