"""Pharmaceutical: Regulatory Compliance Gap Detection

Gate: Are there regulatory compliance gaps?
Route: Which remediation track? (Plan correction, Urgent review, Regulatory report)
Priority: What's the compliance risk?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "area": "Manufacturing facility, Building C",
    "audit_type": "Internal compliance audit",
    "findings": ["Environmental monitoring logs incomplete for 2 weeks", "One employee expired GMP certification"],
    "current_status": "Batch 847 currently in production",
    "other_audit_history": "No prior significant findings",
    "remediation_plan": "Drafted but not yet approved",
    "regulatory_due": "FDA inspection scheduled 60 days",
}

QUESTIONS = {
    "has_gaps": noul("Are there regulatory compliance gaps?"),
    "track": choice("Remediation track?", {
        "plan": "Plan and execute correction",
        "urgent": "Urgent review, halt production if needed",
        "report": "Report to regulatory authority",
    }),
    "risk": score("Compliance risk?", ["Low", "Moderate", "High", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
