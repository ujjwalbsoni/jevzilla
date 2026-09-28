"""Aviation: Pilot Incident Review & Certification

Gate: Does pilot need remedial training?
Route: Which action? (Clear, Training required, Suspension, Investigation)
Priority: What's the incident severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "incident": "Failed to follow ATC instruction on approach",
    "pilot": "Senior captain, 15,000 flight hours",
    "context": "High-traffic approach, multiple aircraft",
    "consequence": "Slight deviation, corrected immediately upon notice",
    "pilot_acknowledgment": "Pilot acknowledged error, apologized",
    "prior_record": "Clean 10-year record",
    "similar_incidents": "None recorded",
    "atp_status": "Active, current ratings",
}

QUESTIONS = {
    "remedial_training": noul("Does pilot need remedial training?"),
    "action": choice("Action required?", {
        "clear": "No action, clear incident",
        "training": "Remedial training recommended",
        "suspension": "Suspend pending investigation",
        "investigate": "Full investigation initiated",
    }),
    "severity": score("Incident severity?", ["Minor", "Moderate", "Serious", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
