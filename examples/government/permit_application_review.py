"""Government: Permit Application Review & Approval

Gate: Does application meet requirements?
Route: Which approval path? (Approved, Conditional, Requires resubmission)
Priority: What's the processing complexity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "permit_type": "Commercial development variance",
    "application_completeness": "All required documents submitted",
    "zoning_compliance": "Property currently zoned residential, variance needed",
    "environmental_review": "EA completed, no significant impacts",
    "community_feedback": "Mixed, 6 support, 4 opposed, no major concerns",
    "financial_impact": "Estimated tax revenue +$500K annually",
    "legal_review": "Legal compliant with zoning ordinances",
}

QUESTIONS = {
    "meets_requirements": noul("Does application meet requirements?"),
    "path": choice("Approval path?", {
        "approved": "Approved as submitted",
        "conditional": "Approved with conditions",
        "resubmit": "Requires resubmission",
    }),
    "complexity": score("Processing complexity?", ["Simple", "Moderate", "Complex", "Highly complex"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
