"""Pharmaceutical: Drug Compound Quality & Stability Review

Gate: Does compound meet quality specifications?
Route: Which action? (Release, Rework, Reject, Hold)
Priority: What's the deficiency severity?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "batch": "PHA-2024-0847, 500g of active compound",
    "purity": "99.1% (spec: 99.0-99.5%)",
    "water_content": "0.08% (spec: <0.1%)",
    "particle_size": "2.1 microns (spec: 1.0-5.0 microns)",
    "sterility_test": "Passed all pathogens",
    "stability_data": "Consistent degradation profile",
    "manufacturing_record": "All parameters within tolerance",
    "documentation": "Complete and verified",
}

QUESTIONS = {
    "meets_spec": noul("Does compound meet specifications?"),
    "action": choice("Quality action?", {
        "release": "Release batch for use",
        "rework": "Rework to improve quality",
        "reject": "Reject batch",
        "hold": "Hold pending additional testing",
    }),
    "deficiency": score("Deficiency severity?", ["None", "Minor", "Moderate", "Major"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
