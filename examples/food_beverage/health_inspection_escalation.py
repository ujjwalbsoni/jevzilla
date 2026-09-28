"""Food & Beverage: Health Inspection Score Escalation

Gate: Does score require management escalation?
Route: Which response track? (Plan corrective action, Stop service, Retrain staff)
Priority: What's the violation severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "restaurant": "Downtown Cafe, 3rd inspection this year",
    "score": "82/100 (down from 95 last quarter)",
    "violations": ["Cold storage at 42F (should be 40F)", "Improper food handler certification"],
    "critical_violations": 0,
    "history": "Good record, rare violations",
    "corrective_actions_pending": "Temperature controls serviced 2 weeks ago",
    "staff_turnover": "Recent new kitchen staff",
}

QUESTIONS = {
    "escalate": noul("Does score require management escalation?"),
    "response": choice("Response track?", {
        "corrective": "Plan and execute corrective action",
        "stop": "Stop service until corrected",
        "retrain": "Mandatory staff retraining",
    }),
    "severity": score("Violation severity?", ["Minor", "Moderate", "Significant", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
