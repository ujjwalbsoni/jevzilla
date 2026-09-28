"""Pharmaceutical: Clinical Trial Participant Eligibility Screening

Gate: Does patient meet trial inclusion criteria?
Route: Which track? (Eligible, Conditional, Ineligible)
Priority: How critical are the exclusion factors?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "trial": "Phase 3 Hypertension Study",
    "patient_age": 58,
    "diagnosis": "Mild hypertension, controlled with medication",
    "comorbidities": "Hypothyroidism (stable), no diabetes",
    "current_medications": "Lisinopril 10mg daily",
    "lab_results": "Kidney function normal, liver function normal",
    "recent_hospitalization": "None in past 12 months",
    "prior_participation": "Participated in 1 trial 3 years ago",
}

QUESTIONS = {
    "eligible": noul("Does patient meet inclusion criteria?"),
    "track": choice("Eligibility track?", {
        "eligible": "Eligible for enrollment",
        "conditional": "Eligible with conditions (monitoring required)",
        "ineligible": "Does not meet criteria",
    }),
    "criticality": score("Exclusion factor criticality?", ["None", "Minor", "Moderate", "Major"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
