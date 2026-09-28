"""Agriculture: Harvest Readiness Scoring

Gate: Is crop ready to harvest?
Route: Which harvest approach? (Full harvest, Partial, Wait)
Priority: What's the harvest urgency?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "crop": "Wheat field, 300 acres",
    "moisture": "14.2% (target 13-14%)",
    "kernel_hardness": "Hard, not denting easily",
    "maturity": "~95% of heads have turned color",
    "weather": "Sunny forecast next 5 days",
    "equipment_ready": "Combines serviced and ready",
    "storage": "Bin capacity available",
}

QUESTIONS = {
    "ready": noul("Is crop ready to harvest?"),
    "approach": choice("Harvest approach?", {
        "full": "Begin full harvest operations",
        "partial": "Start partial harvest, monitor rest",
        "wait": "Wait 3-5 more days for optimal maturity",
    }),
    "urgency": score("Harvest urgency?", ["Flexible", "Soon", "This week", "Immediate"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
