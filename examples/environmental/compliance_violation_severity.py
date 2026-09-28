"""Environmental: Environmental Compliance Violation Severity Assessment

Gate: Is violation enforcement action required?
Route: Which enforcement tier? (Warning, Citation, Investigation, Prosecution)
Priority: What's the violation severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "violation": "Wastewater discharge exceeded permitted parameters",
    "facility": "Manufacturing plant, 20+ years operation",
    "discharge_rate": "15% over permitted limit",
    "duration": "Identified during routine monitoring, single day",
    "corrective_action": "Plant operator corrected issue immediately",
    "environmental_impact": "Contained to industrial discharge zone",
    "history": "First violation in facility's record",
}

QUESTIONS = {
    "enforce": noul("Is enforcement action required?"),
    "tier": choice("Enforcement tier?", {
        "warning": "Written warning notice",
        "citation": "Citation with penalty",
        "investigate": "Investigation",
        "prosecute": "Prosecute",
    }),
    "severity": score("Violation severity?", ["Minor", "Moderate", "Serious", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
