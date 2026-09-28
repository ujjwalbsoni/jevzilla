"""Environmental: Carbon Footprint Assessment & Reduction

Gate: Does facility exceed carbon target?
Route: Which reduction track? (Monitoring, Improvement plan, Offset, Penalty)
Priority: What's the emission level?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "facility": "Distribution center, 500,000 sq ft",
    "carbon_target": "500 tons CO2e per year",
    "actual_emissions": "520 tons CO2e (2024)",
    "target_compliance": "4% over target",
    "improvements": "LED lighting installed, fleet electrification 20% complete",
    "forecast_2025": "Projected 480 tons (under target)",
    "tracking": "Monthly monitoring in place",
}

QUESTIONS = {
    "exceeds_target": noul("Does facility exceed carbon target?"),
    "track": choice("Reduction track?", {
        "monitor": "Continue monitoring, no action",
        "improve": "Execute improvement plan",
        "offset": "Purchase carbon offsets",
        "penalty": "Subject to penalty",
    }),
    "emission_level": score("Emission level?", ["On target", "Slightly high", "Moderately high", "Significantly high"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
