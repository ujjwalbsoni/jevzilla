"""Sports & Fitness: Member Complaint Routing & Resolution

Gate: Does complaint warrant formal escalation?
Route: Which resolution? (Apologize, Service credit, Refund, Investigation)
Priority: What's the complaint severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "complaint": "Facility cleanliness issues, equipment not wiped down",
    "member": "3-year member, high satisfaction historically",
    "prior_complaints": "None on file",
    "issue_timing": "Recent observation, multiple visits",
    "staff_response": "Acknowledged, cleaning schedule reviewed",
    "corrective_action": "Additional cleaning staff scheduled",
    "membership_cost": "$80/month",
}

QUESTIONS = {
    "escalate": noul("Does complaint warrant formal escalation?"),
    "resolution": choice("Resolution?", {
        "apologize": "Formal apology, thank for feedback",
        "credit": "Service credit (one free month)",
        "refund": "Refund of recent payments",
        "investigate": "Formal investigation",
    }),
    "severity": score("Complaint severity?", ["Minor", "Moderate", "Significant", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
