"""Transportation: Accident Damage Assessment & Claims Routing

Gate: Is this a reportable accident?
Route: Which claims path? (Insurance claim, Internal, Police report)
Priority: What's the damage severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "incident": "Minor rear-end collision at red light",
    "vehicles_involved": "Company truck (2024 Ford F-150), sedan (2020 Honda Civic)",
    "injuries": "No injuries reported",
    "damage_company": "Rear bumper dent, minor paint damage (~$2,500 est)",
    "damage_other": "Front bumper moderate damage (~$8,000 est)",
    "driver_fault": "Other driver ran red light, clear liability",
    "police_called": "No, both drivers agreed to exchange info",
}

QUESTIONS = {
    "reportable": noul("Is this a reportable accident?"),
    "claims_path": choice("Claims routing?", {
        "insurance": "File insurance claim",
        "internal": "Handle internally with other driver",
        "police": "Require police report first",
    }),
    "severity": score("Damage severity?", ["Minor", "Moderate", "Significant", "Major"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
