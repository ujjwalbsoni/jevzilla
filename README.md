# JEVzilla 🦖

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/pypi-jevzilla-brightgreen.svg)](https://pypi.org/project/jevzilla/)

A fearless, lightweight Python client for the JEV decision evaluation API with **100 production-ready business decision examples** across 20 sectors.

Write decision payloads exactly like the [official JEV API docs](https://jevplayground.com/jev-api), and JEVzilla handles the translation automatically. Perfect for operational decisions, compliance automation, and AI-driven business logic.

## ✨ What Makes JEVzilla Special

- **Production-Ready Examples**: 100 real-world business decision scripts, fully runnable
- **Multi-Sector Coverage**: HR, Finance, Healthcare, Legal, Banking, Insurance, Cybersecurity, Retail, Supply Chain, and 10+ more
- **Simple, Intuitive API**: Just `noul()` (yes/no), `choice()` (select one), and `score()` (prioritize)
- **Flexible Backends**: Playground, Official API, or OpenRouter
- **Zero Boilerplate**: Auto-translates payloads — no manual wire format needed
- **Battle-Tested**: Retry logic, exponential backoff, comprehensive error handling

## 🚀 Quick Start

### Installation

```bash
pip install jevzilla
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

## 🎯 Question Types

JEVzilla supports three core question types:

| Type | Purpose | Example |
|------|---------|---------|
| **noul** | Yes/no binary decision | `noul("Is this urgent?")` |
| **choice** | Select one from options | `choice("Route to:", {"sales": "Sales Team", "support": "Support"})` |
| **score** | Rank by priority/severity | `score("Severity?", ["Low", "Medium", "High"])` |

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

### Custom Backends

```python
# Official TypeSafe API (requires TYPESAFE_API_KEY env var)
jev = JEVzilla(backend="typesafe")

# OpenRouter API (requires OPENROUTER_API_KEY env var)
jev = JEVzilla(backend="openrouter")

# Custom URL or API key
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

## 📚 100 Real-World Examples

JEVzilla includes **100 production-ready business decision scripts** organized by sector:

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
| **Cybersecurity** | 5 | Access anomalies, Incident response, Phishing, Vendor risk, Vulnerability |
| **Sales** | 5+ | Lead qualification, Deal risk, Churn prediction, Proposals, Discounts |

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

## 🎓 Use Cases

- **Compliance & Automation**: Flag risky applications, contracts, or transactions
- **Operational Triage**: Route tickets, incidents, and requests to the right team
- **Risk Assessment**: Score vendors, customers, and transactions
- **Quality Control**: Review content, code, or documentation
- **Decision Support**: Augment human judgment with consistent AI reasoning

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
