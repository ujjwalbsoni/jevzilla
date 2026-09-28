"""Aviation: Maintenance Schedule Optimization

Gate: Should this aircraft be scheduled for immediate maintenance?
Route: Which schedule? (Preventive, Corrective, Emergency pulldown)
Priority: What's the maintenance urgency?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "aircraft": "Boeing 737-800, registration N45821",
    "flight_hours": "18,450 hours",
    "cycles": "12,340 cycles",
    "last_c_check": "800 hours ago",
    "known_issues": ["Minor hydraulic leak (monitored)", "Door actuator stiffness"],
    "upcoming_check_due": "4C check due at 20,000 hours (1,550 hours remaining)",
    "schedule": "Heavy summer schedule, 8-10 flights daily",
    "technician_assessment": "Corrective maintenance for 2-3 items before next check",
}

QUESTIONS = {
    "immediate_maintenance": noul("Should aircraft be scheduled immediately?"),
    "schedule": choice("Maintenance schedule?", {
        "preventive": "Schedule preventive maintenance",
        "corrective": "Corrective maintenance after flights",
        "emergency": "Emergency pulldown from service",
    }),
    "urgency": score("Maintenance urgency?", ["Routine", "Scheduled", "Urgent", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
