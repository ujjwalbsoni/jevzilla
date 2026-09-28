"""Aviation: Regulatory Compliance Check & Certification

Gate: Does airline meet regulatory requirements?
Route: Which compliance status? (Compliant, Conditional, Non-compliant)
Priority: What's the compliance risk?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "airline": "Regional carrier, 40-aircraft fleet",
    "audit_type": "FAA compliance audit",
    "findings": ["Maintenance records: 98% compliant", "Crew training: 1 pilot recertification delayed"],
    "critical_violations": 0,
    "audit_history": "Clean audit 2 years ago",
    "remediation_status": "Pilot recertification scheduled within 30 days",
    "safety_record": "No accidents in 5 years",
}

QUESTIONS = {
    "compliant": noul("Does airline meet regulatory requirements?"),
    "status": choice("Compliance status?", {
        "compliant": "Fully compliant",
        "conditional": "Conditional compliance pending resolution",
        "noncompliant": "Non-compliant, corrective action required",
    }),
    "risk": score("Compliance risk?", ["Low", "Acceptable", "Concern", "High risk"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
