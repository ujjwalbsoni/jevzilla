"""Construction: Site Safety Incident Triage

Gate: Should this safety incident be escalated to HSE?
Route: Which team handles this? (On-site, HSE, External contractor)
Priority: What's the incident severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "incident": "Worker fell from 8ft scaffold, hit support beam, conscious but in pain",
    "injuries": "Possible rib fracture, laceration on shoulder",
    "response_time": "First aid applied within 2 minutes",
    "weather": "Clear conditions",
    "site_activity": "Active construction with 12 workers present",
}

QUESTIONS = {
    "escalate_hse": noul("Should this be escalated to HSE?"),
    "route": choice("Which team owns initial response?", {
        "onsite": "On-site medical team",
        "hse": "HSE department",
        "external": "External emergency services",
    }),
    "severity": score("Incident severity?", ["Minor", "Moderate", "Serious", "Critical"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
