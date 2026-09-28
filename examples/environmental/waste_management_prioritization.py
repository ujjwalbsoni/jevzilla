"""Environmental: Waste Management Prioritization

Gate: Should waste stream be rerouted?
Route: Which option? (Landfill, Recycle, Incinerate, Special disposal)
Priority: What's the waste disposal urgency?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "waste_type": "Electronic waste (e-waste)",
    "volume": "2,400 lbs accumulated",
    "composition": "Mix of computing equipment, monitors, cables",
    "hazardous_materials": "Lead in CRTs, minimal mercury",
    "current_storage": "Contained in dedicated warehouse, organized",
    "recycler_contact": "Certified e-waste recycler available",
    "landfill_cost": "$400 vs recycler cost $150",
}

QUESTIONS = {
    "reroute": noul("Should waste stream be rerouted?"),
    "option": choice("Disposal option?", {
        "landfill": "Landfill disposal",
        "recycle": "Certified recycler",
        "incinerate": "Incineration facility",
        "special": "Specialized hazmat disposal",
    }),
    "urgency": score("Disposal urgency?", ["Routine", "Scheduled", "Urgent", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
