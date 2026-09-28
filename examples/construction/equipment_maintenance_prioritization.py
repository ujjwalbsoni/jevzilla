"""Construction: Equipment Maintenance Prioritization

Gate: Does this equipment need immediate maintenance?
Route: Which maintenance type? (Preventive, Corrective, Emergency)
Priority: What's the maintenance urgency?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "equipment": "Concrete mixer (CAT brand, 2018 model)",
    "runtime_hours": "3,847 hours",
    "last_service": "1,200 hours ago",
    "current_issues": "Slight vibration, minor fluid leak detected",
    "maintenance_schedule": "Service due at 4,000 hours",
    "backup_available": "Yes, spare mixer on standby",
    "project_impact": "Loss would delay work 1-2 days",
}

QUESTIONS = {
    "needs_maintenance": noul("Does this need immediate maintenance?"),
    "maintenance_type": choice("Maintenance type?", {
        "preventive": "Preventive service",
        "corrective": "Corrective (address issues)",
        "emergency": "Emergency repair",
    }),
    "urgency": score("Maintenance urgency?", ["Routine", "Scheduled", "Urgent", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
