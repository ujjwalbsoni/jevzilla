"""Pharmaceutical: Research Proposal Prioritization & Funding

Gate: Should this proposal receive funding?
Route: Which tier? (Tier 1 priority, Tier 2 conditional, Tier 3 waitlist)
Priority: What's the research impact score?
"""

from jevzilla import JEVzilla, noul, choice, score

STATE = {
    "proposal": "Novel diabetic neuropathy treatment pathway",
    "pi_track_record": "Published 15 peer-reviewed papers, 2 successful grants",
    "research_merit": "Addresses unmet medical need, novel mechanism",
    "preliminary_data": "Strong in-vitro results, feasibility demonstrated",
    "team_composition": "Experienced team with complementary expertise",
    "budget": "$2.5M over 3 years",
    "budget_status": "Available funding: $5.5M",
    "timeline": "18-month initial phase",
}

QUESTIONS = {
    "fund": noul("Should proposal receive funding?"),
    "tier": choice("Funding tier?", {
        "tier1": "Tier 1 priority (immediate funding)",
        "tier2": "Tier 2 conditional (pending revisions)",
        "tier3": "Tier 3 waitlist (strong but lower priority)",
    }),
    "impact": score("Research impact?", ["Incremental", "Significant", "High impact", "Breakthrough potential"]),
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    response = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print(response.status_code, response.answers)
