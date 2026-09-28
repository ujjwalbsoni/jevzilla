"""Sports & Fitness: Training Injury Assessment & Clearance

Gate: Is injury serious enough to halt training?
Route: Which clearance? (Full activity, Modified activity, Rest period, Medical referral)
Priority: What's the injury severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "member": "Regular gym-goer, 3x/week routine",
    "injury": "Minor knee discomfort after running",
    "duration": "Mild swelling, localized pain",
    "onset": "Started during cardio workout yesterday",
    "rest_tried": "Elevated, ice applied, feels better today",
    "medical_history": "No prior knee issues",
    "desire": "Wants to continue light training",
}

QUESTIONS = {
    "halt_training": noul("Should training be halted?"),
    "clearance": choice("Clearance level?", {
        "full": "Full activity cleared",
        "modified": "Modified activity only",
        "rest": "Rest period required",
        "referral": "Medical referral required",
    }),
    "severity": score("Injury severity?", ["Very minor", "Minor", "Moderate", "Serious"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
