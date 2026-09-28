"""Environmental: Green Certification Eligibility Assessment

Gate: Is facility eligible for green certification?
Route: Which tier? (Gold, Silver, Bronze, Ineligible)
Priority: What's the sustainability score?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "facility": "Commercial office building",
    "energy_efficiency": "HVAC optimized, 25% below baseline",
    "water_usage": "Recycled water, 30% reduction",
    "waste_diversion": "65% diverted from landfill",
    "renewable_energy": "Solar panels supply 20% of power",
    "transportation": "EV charging stations, transit incentives",
    "certifications": "ISO 14001 environmental management",
    "score": "78/100",
}

QUESTIONS = {
    "eligible": noul("Is facility eligible for certification?"),
    "tier": choice("Certification tier?", {
        "gold": "Gold certification (80+)",
        "silver": "Silver certification (70-79)",
        "bronze": "Bronze certification (60-69)",
        "ineligible": "Does not meet minimum",
    }),
    "sustainability": score("Sustainability score?", ["Below 60", "60-69", "70-79", "80+"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
