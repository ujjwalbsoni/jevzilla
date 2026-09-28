"""Aviation: Safety Incident Severity Assessment & Reporting

Gate: Is this a reportable safety incident?
Route: Which report level? (Internal, FAA, NTSB)
Priority: What's the incident severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "incident": "Cabin pressure warning light during cruise",
    "altitude": "35,000 feet",
    "response": "Pressurization system functioning normally, light appears sensor issue",
    "symptoms": "No cabin discomfort, pressurization holding steady",
    "descent": "Initiated gradual descent to 25,000 feet as precaution",
    "landing": "Completed safely, no emergency declared",
    "technical_cause": "Likely pressure sensor malfunction",
}

QUESTIONS = {
    "reportable": noul("Is this a reportable safety incident?"),
    "report_level": choice("Report level?", {
        "internal": "Internal incident report only",
        "faa": "Report to FAA",
        "ntsb": "Report to NTSB (major incident)",
    }),
    "severity": score("Incident severity?", ["Minor", "Moderate", "Serious", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
