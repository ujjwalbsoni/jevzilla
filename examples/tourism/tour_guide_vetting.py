"""Tourism: Tour Guide Vetting & Certification

Gate: Should tour guide be approved?
Route: Which tier? (Approved, Probation, Training required, Rejected)
Priority: What's the quality assessment?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "candidate": "Experienced guide, 8 years in industry",
    "certifications": "Standard tour guide license, 2-year recertification pending",
    "background_check": "Clear, no issues",
    "guest_feedback": "4.6/5 stars from 120+ reviews",
    "language_proficiency": "Native + 2 other languages fluent",
    "safety_training": "Current CPR, first aid certified",
    "guide_specialty": "Historical sites, cultural tours",
}

QUESTIONS = {
    "approve": noul("Should tour guide be approved?"),
    "tier": choice("Approval tier?", {
        "approved": "Approved for full assignment",
        "probation": "Probation - supervised tours",
        "training": "Training required, then reassess",
        "reject": "Not approved",
    }),
    "quality": score("Quality assessment?", ["Acceptable", "Good", "Very good", "Excellent"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
