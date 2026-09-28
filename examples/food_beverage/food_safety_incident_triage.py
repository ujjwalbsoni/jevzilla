"""Food & Beverage: Food Safety Incident Triage

Gate: Is this a reportable food safety incident?
Route: Which response level? (Internal investigation, Health dept notification, Recall)
Priority: What's the public health risk?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "incident": "Customer reports possible foodborne illness",
    "customer_symptoms": "Nausea, mild GI distress, symptoms started 6 hours post-meal",
    "date_consumed": "Yesterday evening",
    "items_ordered": "Chicken sandwich, salad, iced tea",
    "other_cases": "No similar complaints from that time period",
    "food_storage": "Checked, all items held at correct temperature",
    "employee_health": "All kitchen staff healthy, no absences",
}

QUESTIONS = {
    "reportable": noul("Is this reportable food safety incident?"),
    "response": choice("Response level?", {
        "internal": "Internal investigation",
        "health_dept": "Notify health department",
        "recall": "Initiate product recall",
    }),
    "risk": score("Public health risk?", ["Low", "Moderate", "High", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
