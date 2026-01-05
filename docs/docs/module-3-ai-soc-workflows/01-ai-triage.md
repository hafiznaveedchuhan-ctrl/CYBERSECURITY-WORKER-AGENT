---
sidebar_position: 1
---

# AI-Assisted Alert Triage

This section covers how AI agents can enhance the alert triage process in a SOC.

## The Triage Challenge

SOC analysts face:
- **High Volume**: Thousands of alerts daily
- **Alert Fatigue**: Repetitive investigation tasks
- **Time Pressure**: Need fast, accurate decisions
- **Context Gaps**: Incomplete information

## AI Triage Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TRIAGE AGENT                             │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   CLASSIFY   │───►│   ENRICH     │───►│   ASSESS     │  │
│  │   Intent     │    │   Context    │    │   Severity   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
│  Tools:                                                     │
│  - IOC Reputation    - Log Search      - RAG Knowledge     │
│  - MITRE Mapping     - Asset Lookup    - Similar Cases     │
└─────────────────────────────────────────────────────────────┘
```

## Triage Workflow

### Step 1: Alert Intake

```python
class AlertIntake:
    async def process(self, raw_alert: dict) -> NormalizedAlert:
        # Normalize alert format
        alert = self.normalize(raw_alert)

        # Extract IOCs
        alert.iocs = self.extract_iocs(alert.description)

        # Add asset context
        alert.asset = await self.lookup_asset(alert.host)

        return alert
```

### Step 2: AI Classification

The agent analyzes the alert:

```
System: You are a security triage agent. Analyze the following alert.

Alert: Suspicious PowerShell execution detected
Host: WORKSTATION-42
User: john.doe
Command: powershell -enc BASE64STRING

Classification required:
1. Alert Type (malware, phishing, lateral movement, etc.)
2. True/False Positive likelihood
3. Initial severity assessment
4. Key investigation questions
```

### Step 3: Automated Enrichment

```python
class EnrichmentPipeline:
    async def enrich(self, alert: NormalizedAlert) -> EnrichedAlert:
        # Parallel enrichment
        results = await asyncio.gather(
            self.check_ioc_reputation(alert.iocs),
            self.search_related_logs(alert),
            self.get_user_context(alert.user),
            self.check_asset_criticality(alert.host),
            self.find_similar_alerts(alert),
        )

        return EnrichedAlert(
            alert=alert,
            reputation=results[0],
            related_logs=results[1],
            user_context=results[2],
            asset_info=results[3],
            similar_cases=results[4],
        )
```

### Step 4: Severity Scoring

AI calculates severity based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| IOC Reputation | 25% | Known malicious indicators |
| Asset Criticality | 20% | Importance of affected system |
| User Risk | 15% | User's role and history |
| Attack Stage | 20% | Position in kill chain |
| Historical Pattern | 10% | Similar past incidents |
| Environmental Context | 10% | Time, location, behavior |

### Step 5: Response Recommendation

Agent provides actionable next steps:

```markdown
## Triage Summary

**Classification**: True Positive - Potential Malware Execution
**Severity**: HIGH (Score: 8.2/10)

### Rationale
- PowerShell with encoded command matches known evasion technique
- User john.doe not expected to run PowerShell
- WORKSTATION-42 is a finance department machine

### Recommended Actions
1. [ ] Isolate WORKSTATION-42 from network
2. [ ] Capture memory dump for analysis
3. [ ] Check for lateral movement from this host
4. [ ] Interview user about activity
5. [ ] Escalate to Tier 2 for investigation

### Related Intelligence
- MITRE ATT&CK: T1059.001 (PowerShell)
- Similar alert last week (Case #1234) - confirmed malware
```

## Integration Points

### SIEM Integration

```python
class SIEMConnector:
    async def fetch_alerts(self, query: str) -> list[Alert]:
        """Fetch alerts from SIEM."""
        pass

    async def update_alert(self, alert_id: str, status: str, notes: str):
        """Update alert status in SIEM."""
        pass

    async def search_logs(self, query: str, time_range: str) -> list[LogEntry]:
        """Search correlated logs."""
        pass
```

### Ticketing Integration

```python
class TicketConnector:
    async def create_incident(self, alert: EnrichedAlert) -> str:
        """Create incident ticket from alert."""
        return ticket_id

    async def link_alerts(self, ticket_id: str, alert_ids: list[str]):
        """Link related alerts to incident."""
        pass
```

## Measuring Triage Quality

### Key Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Triage Accuracy | (TP + TN) / Total | > 95% |
| Auto-close Rate | FP auto-closed / Total FP | > 80% |
| Escalation Accuracy | Valid escalations / Total escalations | > 90% |
| Mean Triage Time | Avg time to classify | < 2 min |

### Feedback Loop

```python
class FeedbackCollector:
    async def record_outcome(self, alert_id: str, actual_outcome: str):
        """Record actual outcome for model improvement."""
        prediction = await self.get_prediction(alert_id)

        await self.store_feedback(
            alert_id=alert_id,
            predicted=prediction,
            actual=actual_outcome,
            correct=prediction == actual_outcome,
        )

    async def analyze_accuracy(self, time_range: str) -> AccuracyReport:
        """Analyze prediction accuracy over time."""
        pass
```

## Best Practices

1. **Start Simple**: Begin with high-confidence classifications
2. **Human Verification**: Review AI decisions initially
3. **Continuous Tuning**: Adjust based on feedback
4. **Transparency**: Explain AI reasoning
5. **Fallback Plans**: Handle AI unavailability

## Summary

AI-assisted triage significantly reduces analyst workload while improving consistency. The key is combining AI capabilities with human oversight and continuous improvement.
