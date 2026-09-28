"""Construction: Permit Compliance Review

Gate: Does project meet all permit requirements?
Route: Which compliance track? (Approved, Conditional, Non-compliant)
Priority: What's the compliance risk?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "project": "Residential development, 50 units",
    "permits_obtained": ["Building permit", "Environmental", "Water/sewer connection"],
    "inspections_passed": ["Foundation", "Framing phase 1"],
    "pending_inspections": ["Electrical", "Plumbing", "Final"],
    "violations": "None recorded",
    "timeline_compliance": "On schedule for next inspection",
    "documentation": "All records filed with city",
}

QUESTIONS = {
    "compliant": noul("Does project meet all permit requirements?"),
    "compliance_track": choice("Compliance status?", {
        "approved": "Approved, proceed as planned",
        "conditional": "Conditional, minor adjustments needed",
        "noncompliant": "Non-compliant, halt work pending resolution",
    }),
    "risk": score("Compliance risk level?", ["Low", "Medium", "High", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
