"""Agriculture: Equipment Maintenance Prioritization

Gate: Does farm equipment need immediate maintenance?
Route: Which maintenance type? (Preventive, Repair, Emergency)
Priority: What's the maintenance urgency?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "equipment": "John Deere combine harvester",
    "operating_hours": "1,250 hours this season",
    "condition": "Engine knocking, reduced power output",
    "last_service": "60 days ago",
    "harvest_stage": "Mid-harvest, 60% complete",
    "weather_window": "3 days of good weather remaining",
    "backup_equipment": "No spare available",
}

QUESTIONS = {
    "needs_maintenance": noul("Does equipment need immediate maintenance?"),
    "maintenance_type": choice("Maintenance type?", {
        "preventive": "Scheduled preventive service",
        "repair": "Repair specific issue",
        "emergency": "Emergency repair",
    }),
    "urgency": score("Maintenance urgency?", ["After harvest", "This week", "Next 2 days", "Now"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
