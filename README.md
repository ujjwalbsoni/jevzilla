# JEVzilla 🦖

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/pypi-jevzilla-brightgreen.svg)](https://pypi.org/project/jevzilla/)

A fearless, lightweight Python client for the JEV decision evaluation API with **150+ production-ready business decision examples** across 30 sectors.

Write decision payloads exactly like the [official JEV API docs](https://jevplayground.com/jev-api), and JEVzilla handles the translation automatically. Perfect for operational decisions, compliance automation, and AI-driven business logic.

## 🤔 What is JEV?

**JEV** is a **decision layer for software applications** — not a chatbot or text generator, but a system designed to make **structured, typed decisions** that your code can consume and act on.

Given a piece of context (called **state**), JEV answers **typed questions** and returns **structured answers with probability signals**. Your application then branches on these decisions to automate workflows, route requests, or flag for human review.

### Why JEV is Different

| Traditional LLM | JEV |
|---|---|
| Open-ended text responses | **Bounded, typed decisions** |
| Requires parsing output | **Structured JSON answers** |
| May hallucinate or ramble | **Focused yes/no, choice, or score** |
| Hard to integrate into workflows | **Built for programmatic consumption** |

**JEV is best for:**
- ✅ Operational triage & routing (which team owns this?)
- ✅ Risk/severity scoring (how critical is this?)
- ✅ Yes/no classification (should this be escalated?)
- ✅ Conditional business logic (decide what happens next)

**JEV is NOT for:**
- ❌ Open-ended explanations
- ❌ Creative content generation
- ❌ Long conversational responses
- → Use a generative LLM for those

## ✨ What Makes JEVzilla Special

- **Production-Ready Examples**: 150+ real-world business decision scripts, fully runnable
- **Multi-Sector Coverage**: 30 sectors including HR, Finance, Healthcare, Legal, Banking, Insurance, Cybersecurity, Retail, Supply Chain, Construction, Agriculture, Transportation, Food & Beverage, Pharmaceutical, Government, Aviation, Tourism, Environmental, Sports, and more
- **Simple, Intuitive API**: Just `noul()` (yes/no), `choice()` (select one), and `score()` (prioritize)
- **Flexible Backends**: Playground, Official API, or OpenRouter
- **Zero Boilerplate**: Auto-translates payloads — no manual wire format needed
- **Battle-Tested**: Retry logic, exponential backoff, comprehensive error handling

## 🚀 Quick Start

### Installation

```bash
pip install jevzilla
```

### Getting an API Key (Recommended)

For **production use**, get an API key from one of these services:

- **OpenRouter** (Recommended): https://openrouter.ai/keys
- **TypeSafe Official**: https://api.typesafe.ai
- Or use **Playground** endpoint for testing (no key needed)

Set your API key as an environment variable:
```bash
# OpenRouter
export OPENROUTER_API_KEY="your-key-here"

# TypeSafe
export TYPESAFE_API_KEY="your-key-here"

# On Windows PowerShell:
# $env:OPENROUTER_API_KEY = "your-key-here"
```

### Basic Usage

```python
from jevzilla import JEVzilla, noul, choice, score

# Initialize the client
jev = JEVzilla()

# Ask a decision
response = jev.evaluate({
    "state": "Customer charged twice, cannot access account.",
    "questions": {
        "refund_review": noul("Does this need refund review?"),
        "team": choice("Which team?", {
            "billing": "Payment issues",
            "technical": "Access problems"
        }),
        "urgency": score("How urgent?", ["Routine", "Time-sensitive", "Blocked"]),
    },
})

print(response.status_code, response.answers)
# Output: 200 {'refund_review': {...}, 'team': {...}, 'urgency': {...}}
```

### Using Different Backends

JEVzilla supports three backends. **For production, use OpenRouter or TypeSafe** for better reliability:

#### OpenRouter (Recommended for Production)

```bash
# 1. Get API key from https://openrouter.ai/keys
# 2. Set environment variable
export OPENROUTER_API_KEY="your-api-key-here"

# On Windows PowerShell:
# $env:OPENROUTER_API_KEY = "your-api-key-here"
```

```python
from jevzilla import JEVzilla, noul

# Automatically uses OPENROUTER_API_KEY environment variable
jev = JEVzilla(backend="openrouter")

response = jev.evaluate({
    "state": "Customer issue",
    "questions": {
        "urgent": noul("Is this urgent?"),
    },
})
```

#### TypeSafe API (Official)

```bash
# Get API key from https://api.typesafe.ai
export TYPESAFE_API_KEY="your-api-key-here"
```

```python
jev = JEVzilla(backend="typesafe")
```

#### Playground (Default, for Testing)

```python
# No API key needed — uses public endpoint
jev = JEVzilla()  # or backend="playground"
```

| Backend | Reliability | Speed | Cost | Best For |
|---------|-------------|-------|------|----------|
| **OpenRouter** | ⭐⭐⭐⭐⭐ | Fast | Paid | Production |
| **TypeSafe** | ⭐⭐⭐⭐⭐ | Fast | Paid | Production |
| **Playground** | ⭐⭐⭐ | Variable | Free | Testing/Development |

### Inspecting the Payload

```python
# See the exact payload that gets sent
jev = JEVzilla()
payload = jev.build({
    "state": "High CPU usage detected",
    "questions": {
        "urgent": noul("Is this critical?"),
    }
})
print(payload)
```

## 🎯 The Three Question Types

JEV supports three core question types for making decisions:

### **Noul** — Yes/No Judgment
A **focused, proposition-based question** that returns a probability between 0 and 1.

**When to use:** Single yes/no decisions, risk flags, human review gates
```python
noul("Does this request contain an urgent deadline?")
# Returns: {"noul": 0.87}  (87% confidence it's urgent)
```

**Real examples:**
- "Should this order be flagged for manual review?"
- "Does the customer have churn risk?"
- "Is this transaction fraudulent?"

---

### **Choice** — Classification & Routing
Select **one option from a predefined set** of categories, plus confidence scores.

**When to use:** Routing decisions, ticket classification, routing to teams
```python
choice("Which team should handle this?", {
    "billing": "Payments & billing issues",
    "technical": "Technical problems",
    "support": "General support requests"
})
# Returns: {"choice": "billing", "confidence": 0.92}
```

**Real examples:**
- "Route this ticket to: Sales, Support, or Technical?"
- "Classify this transaction: Normal, Suspicious, or Blocked?"
- "Which priority bucket: Low, Medium, High, or Critical?"

---

### **Score** — Severity, Priority, or Quality Ranking
Rank context on an **ordered scale** with confidence signals (e.g., Low → Medium → High → Critical).

**When to use:** Risk/severity scoring, priority ranking, quality assessment
```python
score("How urgent is this incident?", ["Routine", "Time-sensitive", "Blocked"])
# Returns: {"score": 2, "legend": ["Routine", "Time-sensitive", "Blocked"]}
```

**Real examples:**
- "Incident severity: Info, Warning, or Critical?"
- "Churn risk: Low, Medium, or High?"
- "Loan approval score: 1–5?"

---

### Summary Table

| Type | Question | Answer | Use Case |
|------|----------|--------|----------|
| **noul** | Yes/no proposition | 0.0–1.0 probability | Gate decisions, flags |
| **choice** | Pick one category | One option + confidence | Routing, classification |
| **score** | Rank on ordered scale | Position + probability | Risk/severity scoring |

## 🔧 Advanced Features

### Convenience Shortcuts

```python
# Single-question shortcuts
response = jev.ask_noul(
    state="Server down for 2 hours",
    instructions="Is this a P1 incident?",
)

response = jev.ask_choice(
    state="New customer inquiry",
    instructions="Which team should handle this?",
    criteria={"sales": "Enterprise Sales", "support": "Support"},
)

response = jev.ask_score(
    state="Database backup failed",
    instructions="How critical?",
    levels=["Informational", "Warning", "Critical"],
)
```

### Custom URL & Headers

```python
# Custom endpoint URL
jev = JEVzilla(backend="typesafe", url="https://custom.api.com/v1/evaluate")

# Pass extra headers
jev = JEVzilla(
    backend="openrouter",
    extra_headers={"X-Custom-Header": "value"}
)

# Explicitly pass API key (instead of env var)
jev = JEVzilla(backend="typesafe", api_key="your-api-key-here")
```

### Retry & Timeout Control

```python
jev = JEVzilla(
    timeout=45.0,           # Request timeout in seconds
    retries=4,              # Max retry attempts
    backoff=1.0,            # Initial backoff multiplier
    max_backoff=30.0,       # Maximum backoff cap
)
```

### Batch Processing

```python
# Process multiple decisions
decisions = [
    {"state": "...", "questions": {...}},
    {"state": "...", "questions": {...}},
]

for decision in decisions:
    response = jev.evaluate(decision)
    if response.ok:
        print(f"Answer: {response.answers}")
```

## 📚 150+ Real-World Examples Across 30 Sectors

JEVzilla includes **150+ production-ready business decision scripts** organized by sector:

### Original 20 Sectors (100 examples)

| Sector | Scripts | Use Cases |
|--------|---------|-----------|
| **HR** | 5 | Resume screening, Interview feedback, Grievance triage, Performance calibration, Offer risk |
| **Finance** | 5 | Invoice review, Expense audit, Budget variance, Credit applications, Anomaly detection |
| **Healthcare** | 5 | Patient intake, Pre-auth review, No-show risk, Billing disputes, Feedback analysis |
| **Legal** | 5 | Contract review, NDA analysis, Compliance gaps, Litigation holds, Trademark disputes |
| **Banking** | 5 | Loan applications, Fraud detection, Account opening, Disputes, AML alerts |
| **Insurance** | 5 | Claims triage, Renewal risk, Underwriting, Subrogation, Complaints |
| **IT/DevOps** | 5 | Incident severity, Change risk, Code review, Access requests, Vendor security |
| **Manufacturing** | 5 | Defect triage, Supplier audit, Safety incidents, Maintenance, Change requests |
| **Logistics** | 5 | Shipment exceptions, Supplier delays, Customs review, Carrier performance, Warehouse |
| **Retail** | 5 | Return fraud, Review moderation, Reorder priority, Complaint routing, Price matching |
| **Real Estate** | 5 | Tenant screening, Maintenance, Lease renewal, Inspections, Offers |
| **Education** | 5 | Submission review, Admissions, Financial aid, Integrity checks, Feedback |
| **Cybersecurity** | 5 | Phishing triage, Vulnerability review, Access anomalies, Incident response, Vendor risk |
| **Marketing** | 5 | Content review, Influencer vetting, Ad compliance, Survey sentiment, Brand mentions |
| **Customer Support** | 5 | Ticket triage, Refund decisions, Churn flags, Escalation, CSAT follow-up |
| **Energy/Utilities** | 5 | Outage triage, Meter anomalies, Safety incidents, Assistance review, Maintenance |
| **Hospitality** | 5 | Guest complaints, Booking fraud, Overbooking, Travel refunds, Review responses |
| **Media/Entertainment** | 5 | Content moderation, Copyright claims, Brand safety, Comments, Licensing |
| **Telecom** | 5 | Outage triage, SIM swap review, Churn risk, Billing disputes, Upgrade eligibility |
| **Sales** | 5 | Lead qualification, Deal risk, Churn prediction, Proposals, Discount approvals |

### NEW 10 Sectors (50 examples)

| Sector | Scripts | Use Cases |
|--------|---------|-----------|
| **Construction** | 5 | Site safety triage, Contractor vetting, Project delay risk, Equipment maintenance, Permit compliance |
| **Agriculture** | 5 | Crop health assessment, Equipment maintenance, Pest/disease triage, Supplier quality, Harvest readiness |
| **Transportation** | 5 | Vehicle maintenance scheduling, Accident damage assessment, Warranty claims, Fuel efficiency, Recall prioritization |
| **Food & Beverage** | 5 | Health inspection escalation, Food safety incidents, Supplier quality, Customer complaints, Menu performance |
| **Pharmaceutical** | 5 | Clinical trial eligibility, Adverse event severity, Drug compound quality, Regulatory compliance gaps, Research proposals |
| **Government** | 5 | Permit applications, Public assistance eligibility, Compliance violations, Budget allocation, FOIA requests |
| **Aviation** | 5 | Maintenance scheduling, Safety incidents, Pilot incidents, Regulatory compliance, Crew scheduling |
| **Tourism** | 5 | Booking fraud detection, Travel insurance claims, Destination safety, Customer complaints, Tour guide vetting |
| **Environmental** | 5 | Environmental incidents, Compliance violations, Carbon footprint, Waste management, Green certification |
| **Sports & Fitness** | 5 | Gym membership eligibility, Training injury assessment, Equipment maintenance, Member complaints, Program recommendations |

### Running Examples

```bash
# Install the package
pip install -e .

# Set your API key
export OPENROUTER_API_KEY=your-key-here

# Run any example
cd examples/hr
python resume_screening.py

# Or run from any sector
cd examples/banking
python fraud_transaction_flag.py
```

Every script follows the same **gate + route + priority** pattern:
- **Gate** (`noul`): Should this be escalated/flagged?
- **Route** (`choice`): Which team owns this?
- **Priority** (`score`): How urgent/severe?

This consistency makes it easy to adapt examples to your own workflows.

## 🔐 Security & Compliance

- **No hardcoded keys**: All API keys via environment variables
- **Regulated data guidance**: Examples for Healthcare, Banking, Legal include compliance notes
- **Safe by default**: Demos use invented data — swap in yours with compliance approval
- **Transparent**: Source available, audit-ready

## 📊 Error Handling

```python
from jevzilla import JEVError, JEVValidationError, JEVHTTPError

try:
    response = jev.evaluate({"state": "...", "questions": {...}})
except JEVValidationError as e:
    print(f"Invalid payload: {e}")
except JEVHTTPError as e:
    print(f"API error {e.status_code}: {e.body}")
except JEVError as e:
    print(f"Other error: {e}")
```

## 🛠️ API Reference

### `JEVzilla` Class

```python
jev = JEVzilla(
    backend: str = "playground",        # "playground", "typesafe", or "openrouter"
    api_key: Optional[str] = None,      # API key (or use env vars)
    model: str = "jev-latest",          # Model version
    url: Optional[str] = None,          # Custom endpoint URL
    timeout: float = 30.0,              # Request timeout (seconds)
    retries: int = 4,                   # Max retry attempts
    backoff: float = 1.0,               # Initial backoff multiplier
    max_backoff: float = 30.0,          # Maximum backoff (seconds)
    session: Optional[requests.Session] = None,  # Custom session
    extra_headers: Optional[Dict] = None,       # Extra HTTP headers
)
```

### Methods

| Method | Purpose |
|--------|---------|
| `evaluate(payload, raise_for_status=True)` | Send a decision request |
| `build(payload)` | Get the exact body without sending |
| `ask_noul(state, instructions, ...)` | Quick yes/no question |
| `ask_choice(state, instructions, criteria, ...)` | Quick choice question |
| `ask_score(state, instructions, levels, ...)` | Quick score question |

### Response Object

```python
response.ok                    # bool: status in 200-299
response.status_code           # int: HTTP status
response.text                  # str: raw response body
response.data                  # dict: parsed JSON response
response.answers               # dict or list: the answers
response.noul(key, threshold)  # Extract boolean answer (0-1 probability)
response.choice(key)           # Extract choice answer
response.score_label(key)      # Extract score label
```

## 📦 Dependencies

- **Python**: 3.8+
- **requests**: 2.28+

## 📄 License

MIT License — see LICENSE file for details.

## 👨‍💻 Author

**Ujjwalkumar Soni**

## 🤝 Contributing

Contributions welcome! Submit issues, feature requests, or pull requests on GitHub.

## 🎓 Use Cases & Patterns

### Gate + Route + Priority Pattern

Every JEVzilla example follows the same battle-tested pattern:

1. **Gate** (`noul`): **Should this be escalated/flagged?**
   - "Does this need manual review?"
   - "Is this a fraud risk?"

2. **Route** (`choice`): **Which team owns this?**
   - "Route to: Billing, Technical, or Support?"
   - "Assign to: Team A, Team B, or Team C?"

3. **Priority** (`score`): **How urgent/severe is it?**
   - "Severity: Low, Medium, High, or Critical?"
   - "Priority: Routine, Standard, or Urgent?"

This consistency makes decisions **predictable, auditable, and easy to act on**.

### Real-World Applications

- **Compliance & Automation**: Flag risky applications, contracts, or transactions
- **Operational Triage**: Route tickets, incidents, and requests to the right team
- **Risk Assessment**: Score vendors, customers, transactions for underwriting/approval
- **Quality Control**: Review content, code, or documentation
- **Decision Support**: Augment human judgment with structured, consistent reasoning
- **Fraud Detection**: Identify suspicious patterns and route for investigation
- **Customer Support**: Triage complaints, determine response level, route to specialists
- **HR & Recruiting**: Screen resumes, assess candidates, route for interviews
- **Incident Response**: Classify severity, route to on-call engineer, set SLA

## ⚠️ Important Notes

- These **examples use invented data** — adapt to your own workflows
- For regulated data (PHI, financial account info, legal docs), ensure **organizational compliance approval** before sending to third-party APIs
- Always **rotate API keys** before committing or sharing
- This library translates payloads but doesn't replace human oversight for critical decisions

## 🔗 Resources

- [JEV API Playground](https://jevplayground.com/jev-api)
- [TypeSafe Official API](https://api.typesafe.ai/)
- [OpenRouter API](https://openrouter.ai/api/alpha/decisions)

## 📞 Support

- Found a bug? Open an issue
- Have a question? Check the examples first
- Want to share a use case? We'd love to hear it!

---

**Star this repo if JEVzilla saves you time or helps you build smarter business decisions!** ⭐
