"""Transportation: Fleet Fuel Efficiency Anomaly Flag

Gate: Does vehicle show abnormal fuel consumption?
Route: Which investigation track? (Driver coaching, Maintenance, Tracking)
Priority: What's the efficiency deviation?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "vehicle": "Box truck, 22 ft, 3 years old",
    "typical_mpg": "8.5 mpg (average)",
    "current_mpg": "6.2 mpg (last 1,000 miles)",
    "deviation": "27% worse than expected",
    "driver": "5 years experience, good record",
    "terrain": "Mostly highway routes, normal routes",
    "maintenance": "Oil change due 500 miles ago",
    "tire_condition": "2 tires at 50% tread, within spec",
}

QUESTIONS = {
    "is_anomaly": noul("Does vehicle show abnormal fuel consumption?"),
    "investigation": choice("Investigation track?", {
        "coaching": "Driver coaching and training",
        "maintenance": "Schedule maintenance inspection",
        "tracking": "Increase GPS tracking for patterns",
    }),
    "deviation": score("Efficiency deviation?", ["Minor (5%)", "Moderate (10%)", "Significant (20%)", "Critical (30%+)"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
