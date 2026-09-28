"""Pharmaceutical: Adverse Event Severity Assessment

Gate: Is this adverse event serious?
Route: Which reporting path? (Monitor, Report, Halt study, Escalate)
Priority: What's the severity level?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "trial": "Phase 2 antiviral compound study",
    "event": "Elevated liver enzymes (ALT 2.5x ULN, AST 2.2x ULN)",
    "patient_status": "Asymptomatic, feeling well",
    "previous_labs": "Normal baseline 6 weeks ago",
    "other_medications": "None concurrent",
    "alcohol_consumption": "Social drinker",
    "resolved": "Checking follow-up labs today",
}

QUESTIONS = {
    "is_serious": noul("Is this adverse event serious?"),
    "reporting": choice("Reporting path?", {
        "monitor": "Monitor closely, routine follow-up",
        "report": "Report to IRB within 7 days",
        "halt": "Halt enrollment, safety review",
        "escalate": "Escalate to FDA immediately",
    }),
    "severity": score("Severity level?", ["Grade 1 (Mild)", "Grade 2 (Moderate)", "Grade 3 (Severe)", "Grade 4 (Life-threatening)"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
