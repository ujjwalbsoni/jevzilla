"""Government: Compliance Violation Triage & Enforcement

Gate: Is violation enforcement action warranted?
Route: Which enforcement track? (Warning, Citation, Investigation)
Priority: What's the violation severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "violation": "Improper hazardous waste disposal",
    "location": "Manufacturing facility in industrial zone",
    "discovery": "Reported by employee, documented by inspectors",
    "extent": "Isolated incident, remediation plan in progress",
    "company_record": "First violation, otherwise good compliance history",
    "prior_violations": "None in past 5 years",
    "public_harm": "No public exposure, contained to facility",
    "remediation": "75% complete, timeline accelerated",
}

QUESTIONS = {
    "enforce": noul("Is enforcement action warranted?"),
    "track": choice("Enforcement track?", {
        "warning": "Formal warning notice",
        "citation": "Issue citation with penalty",
        "investigate": "Full investigation and potential prosecution",
    }),
    "severity": score("Violation severity?", ["Minor", "Moderate", "Serious", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
