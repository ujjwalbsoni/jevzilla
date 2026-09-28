"""Transportation: Vehicle Maintenance Scheduling

Gate: Does vehicle need immediate maintenance?
Route: Which maintenance priority? (Routine, Urgent, Critical)
Priority: What's the maintenance criticality?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "vehicle": "Class 8 truck, VIN 1HZBB8KA5EF123456",
    "mileage": "487,320 miles",
    "service_interval": "Next service due at 500,000 miles",
    "current_issues": "Brake pad wear light on, steering slightly stiff",
    "last_inspection": "45 days ago, passed",
    "utilization": "High, 3,000 miles/week",
    "fleet_size": "50 vehicles, 3 in shop",
}

QUESTIONS = {
    "needs_maintenance": noul("Does vehicle need immediate maintenance?"),
    "priority": choice("Maintenance priority?", {
        "routine": "Schedule routine service",
        "urgent": "Schedule within 1 week",
        "critical": "Take out of service immediately",
    }),
    "criticality": score("Maintenance criticality?", ["Routine", "Important", "Urgent", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
