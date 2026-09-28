"""
IT/DevOps — Pull request risk flag.

Scenario: A PR touching a critical service is opened. JEV flags whether it needs extra review, routes reviewer assignment, and scores deployment risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python code_review_risk.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'pr_summary': 'PR modifies the authentication token validation logic in the shared auth library used by 12 downstream services. Test coverage on the changed lines is under 40%.', 'author': 'Mid-level engineer, first PR to this repo'}

QUESTIONS = {
    "needs_extra_review": {
        "type": "noul",
        "instructions": "Does this PR's scope and test coverage indicate it needs more than a single standard reviewer?",
        "criteria": {"true": 'Shared-library auth changes with low test coverage and an author new to the repo are recognized risk factors.', "false": 'Change is low-scope with adequate test coverage.'},
    },
    "reviewer_assignment": {
        "type": "choice",
        "instructions": 'Who should review this PR?',
        "criteria": {'standard_peer_review': 'Low risk; normal peer review process.', 'senior_engineer_plus_security': 'Auth-related change; needs a senior engineer and security review.', 'architecture_review_required': 'Shared-library blast radius is large enough to need an architecture review.'},
    },
    "deployment_risk": {
        "type": "score",
        "instructions": 'How risky would deploying this change be to production?',
        "criteria": ['Low', 'Moderate', 'High', 'Do not deploy without more tests'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("IT/DevOps — Pull request risk flag", 'PR: auth library token validation change', res.answers)
