# JEV Examples — 100 working scenarios across 20 sectors

Each script is a real, runnable business decision built on [JEVzilla](../README.md)
and JEV's `noul` / `choice` / `score` question types. Every scenario follows the
same three-question shape: a **gate** (should this be flagged/escalated?), a
**route** (which team/track owns it?), and a **priority/severity score**.

| Sector | Folder | Scripts |
|---|---|---|
| HR | `hr/` | resume_screening, interview_feedback_review, grievance_triage, performance_calibration, offer_risk_review |
| Manufacturing | `manufacturing/` | defect_triage, supplier_audit, safety_incident_triage, maintenance_priority, change_request_review |
| Finance | `finance/` | invoice_review, expense_audit, budget_variance_review, credit_application_review, anomaly_flag |
| Healthcare Ops | `healthcare/` | intake_triage, preauth_review, no_show_risk, billing_dispute_triage, feedback_review |
| Legal | `legal/` | contract_clause_review, nda_review, compliance_gap_review, litigation_hold_triage, trademark_dispute_triage |
| Sales | `sales/` | lead_qualification, deal_risk_review, churn_risk_review, proposal_review, discount_approval_review |
| IT / DevOps | `it_devops/` | incident_severity, change_risk_review, code_review_risk, access_request_review, vendor_security_review |
| Insurance | `insurance/` | claims_triage, renewal_risk_review, underwriting_review, subrogation_review, complaint_triage |
| Retail / E-commerce | `retail/` | return_fraud_review, review_moderation, reorder_priority, complaint_routing, price_match_review |
| Logistics / Supply Chain | `logistics/` | shipment_exception, supplier_delay_risk, customs_review, carrier_performance, warehouse_incident |
| Real Estate | `real_estate/` | tenant_screening, maintenance_triage, lease_renewal_risk, inspection_review, offer_review |
| Education | `education/` | submission_review, admission_review, financial_aid_review, integrity_flag_review, course_feedback_review |
| Cybersecurity | `cybersecurity/` | phishing_triage, vulnerability_review, access_anomaly, incident_response_triage, vendor_risk_assessment |
| Marketing | `marketing/` | content_review, influencer_review, ad_copy_compliance, survey_sentiment, brand_mention_triage |
| Customer Support | `customer_support/` | ticket_triage, refund_review, churn_flag, escalation_review, csat_followup |
| Banking | `banking/` | loan_application_review, fraud_transaction_flag, account_opening_review, dispute_review, aml_alert_review |
| Telecom | `telecom/` | outage_triage, sim_swap_review, churn_risk_review, billing_dispute_review, upgrade_eligibility |
| Energy / Utilities | `energy/` | outage_report_triage, meter_anomaly_review, safety_incident_review, assistance_review, maintenance_priority |
| Hospitality / Travel | `hospitality/` | guest_complaint_triage, booking_fraud_review, overbooking_review, travel_refund_review, review_response_priority |
| Media / Entertainment | `media/` | content_moderation, copyright_claim_review, brand_safety_review, comment_moderation, licensing_request_review |

**100 scripts total** — 5 per sector, 20 sectors.

## Run any of them

```bash
pip install -e ..                       # installs jevzilla, if you haven't already
set OPENROUTER_API_KEY=your-key         # Windows (cmd)
cd hr
python resume_screening.py
```

Every script uses `JEVzilla(backend="openrouter")` and reads `OPENROUTER_API_KEY`
from the environment — no keys are hardcoded anywhere. Swap the `STATE` and
`QUESTIONS` dict at the top of any script for your own scenario and it works
the same way.

## Why the same three-question shape everywhere

- **`noul`** — a yes/no gate ("does this need escalation?").
- **`choice`** — routes to one of several named categories ("which team owns this?").
- **`score`** — an ordered severity/priority scale for reporting or sorting.

Real operational decisions are almost always a **gate + a route + a
priority**. Once you see the pattern in one sector, every other sector's
script reads the same way — that consistency is the point.

## ⚠️ Before you share or run these on real data

- These are **demo scenarios** with invented data — swap in your own for a real workflow.
- **Healthcare**, **Insurance**, **Banking**, and **Legal** examples are
  administrative/ops triage aids, not clinical, coverage, credit, or legal
  decisions. Sending real regulated data (PHI, financial account data, etc.)
  to a third-party API needs your organization's compliance sign-off first.
- Rotate/regenerate any API key before it appears in a screenshot, notebook,
  or public repo.
