"""
Finance — Expense report audit flag.

Scenario: An automated expense system flags a submitted report for review. JEV decides whether it needs manager escalation, routes the audit type, and scores policy-violation risk.

Run:
    set OPENROUTER_API_KEY=your-key
    python expense_audit.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _display import print_verdict
from jevzilla import JEVzilla

STATE = {'employee': 'Regional Sales Manager', 'report_summary': "Client dinner expense of $840 for a party of 3, submitted with no itemized receipt, filed 47 days after the policy's 30-day submission window."}

QUESTIONS = {
    "needs_escalation": {
        "type": "noul",
        "instructions": 'Does this expense report show a pattern requiring manager-level review rather than routine AP processing?',
        "criteria": {"true": 'Missing itemized receipt plus a policy-window violation together warrant escalation.', "false": 'Minor, explainable discrepancy that routine processing can handle.'},
    },
    "audit_type": {
        "type": "choice",
        "instructions": 'What kind of review does this expense need?',
        "criteria": {'routine_ap_processing': 'Minor and explainable; process as normal.', 'manager_approval_required': "Needs the employee's manager to approve before reimbursement.", 'expense_policy_audit': "Pattern suggests a broader review of this employee's recent expenses."},
    },
    "violation_risk": {
        "type": "score",
        "instructions": 'How much policy-violation risk does this expense carry?',
        "criteria": ['Low', 'Moderate', 'High', 'Likely violation'],
    },
}

if __name__ == "__main__":
    jev = JEVzilla(backend="openrouter")
    res = jev.evaluate({"state": STATE, "questions": QUESTIONS})
    print_verdict("Finance — Expense report audit flag", 'Expense report: client dinner $840', res.answers)
