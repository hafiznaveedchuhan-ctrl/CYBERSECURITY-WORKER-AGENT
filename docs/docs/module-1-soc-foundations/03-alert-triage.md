---
sidebar_position: 3
---

# Alert Triage Process

Alert triage is one of the most critical functions in a SOC. This section covers how to efficiently classify, prioritize, and investigate security alerts.

## What is Alert Triage?

**Alert triage** is the process of reviewing, classifying, and prioritizing security alerts to determine which require immediate attention and which can be deferred or dismissed.

## The Triage Workflow

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│ Alert Fires │ -> │ Initial      │ -> │ Classify    │ -> │ Take Action  │
│             │    │ Review       │    │ & Prioritize│    │              │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
                          │                   │                   │
                          ▼                   ▼                   ▼
                   - Source check      - True/False       - Escalate
                   - Context gather    - Severity         - Close
                   - IOC extract       - Impact           - Investigate
```

## Step 1: Initial Review

When an alert fires, perform these initial checks:

### Alert Source Validation
- Is the alert source reliable?
- Is the detection rule known to produce false positives?
- When was the rule last updated?

### Context Gathering
```
□ What system triggered the alert?
□ Who is the affected user?
□ What time did it occur?
□ Is this part of a pattern?
□ Are related alerts present?
```

### IOC Extraction
Identify and extract indicators of compromise:
- IP addresses
- Domain names
- File hashes
- URLs
- Email addresses

## Step 2: Classification

### True Positive vs. False Positive

| Classification | Description | Action |
|---------------|-------------|--------|
| **True Positive** | Actual malicious activity | Investigate and respond |
| **False Positive** | Benign activity flagged incorrectly | Document and close |
| **True Negative** | Benign activity not flagged | Expected behavior |
| **False Negative** | Malicious activity not detected | Detection gap |

### Decision Framework

Ask these questions to classify:

1. **Is the activity expected?**
   - Authorized maintenance window?
   - Known business process?
   - Scheduled activity?

2. **Does the context support malicious intent?**
   - Unusual timing?
   - Abnormal volume?
   - Suspicious source?

3. **Are there corroborating indicators?**
   - Multiple related alerts?
   - Threat intelligence matches?
   - Anomalous behavior patterns?

## Step 3: Severity Assessment

### Severity Levels

| Level | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| **Critical** | Active breach, data exfiltration | Immediate | Ransomware, APT activity |
| **High** | Confirmed threat, potential impact | < 1 hour | Malware infection, account compromise |
| **Medium** | Suspicious activity requiring investigation | < 4 hours | Unusual login, policy violation |
| **Low** | Minor issue, informational | < 24 hours | Failed logins, scans |

### Severity Calculation Factors

1. **Asset Criticality**
   - Crown jewel systems = Higher severity
   - Test systems = Lower severity

2. **Data Sensitivity**
   - PII, financial data = Higher severity
   - Public information = Lower severity

3. **Attack Stage**
   - Active exploitation = Higher severity
   - Reconnaissance = Lower severity

4. **Scope**
   - Multiple systems = Higher severity
   - Single endpoint = Lower severity

## Step 4: Prioritization

### Priority Matrix

```
                    IMPACT
                Low    Medium    High
           ┌────────┬────────┬────────┐
      Low  │   P4   │   P3   │   P2   │
URGENCY    ├────────┼────────┼────────┤
    Medium │   P3   │   P2   │   P1   │
           ├────────┼────────┼────────┤
      High │   P2   │   P1   │   P1   │
           └────────┴────────┴────────┘
```

### Priority Actions

| Priority | Response | SLA |
|----------|----------|-----|
| P1 | Immediate response, all hands | < 15 min |
| P2 | Urgent investigation | < 1 hour |
| P3 | Standard investigation | < 4 hours |
| P4 | Scheduled review | < 24 hours |

## Step 5: Investigation

### Investigation Checklist

```markdown
## Alert Investigation

### Basic Information
- [ ] Alert ID: _______________
- [ ] Timestamp: _______________
- [ ] Source: _______________
- [ ] Affected Asset: _______________

### Context
- [ ] User account involved
- [ ] Process/application
- [ ] Network connections
- [ ] Related alerts (last 24h)

### Analysis
- [ ] IOC reputation checks
- [ ] Log correlation
- [ ] Baseline comparison
- [ ] Threat intel matching

### Findings
- [ ] Classification: TP / FP
- [ ] Severity: Critical / High / Medium / Low
- [ ] Recommended action: _______________
```

## Step 6: Action

### Possible Actions

1. **Close as False Positive**
   - Document the reason
   - Consider tuning the rule
   - Track false positive rates

2. **Escalate to Tier 2**
   - Provide investigation notes
   - Include relevant artifacts
   - Suggest next steps

3. **Initiate Response**
   - Follow incident response playbook
   - Contain the threat
   - Notify stakeholders

4. **Request More Information**
   - Contact asset owner
   - Gather additional logs
   - Check with other teams

## Triage Best Practices

### Time Management
- Spend maximum 10-15 minutes on initial triage
- Escalate early if unsure
- Don't go down rabbit holes

### Documentation
- Document every decision
- Use consistent terminology
- Include timestamps

### Correlation
- Always check for related alerts
- Look at historical patterns
- Consider kill chain position

### Tool Usage
- Use threat intelligence lookups
- Leverage SIEM correlation
- Automate repetitive checks

## Common Alert Types

| Alert Type | Common Causes | Investigation Focus |
|------------|---------------|---------------------|
| Malware Detection | Signature match, behavioral | File analysis, execution context |
| Brute Force | Multiple failed logins | Source IP, account targeting |
| Data Exfiltration | Large transfers, unusual destinations | Volume, destination, user |
| Lateral Movement | Internal scanning, credential use | Source system, credential validity |
| Phishing | Email indicators, user action | Email headers, URL analysis |

## AI-Assisted Triage

Modern SOCs use AI to enhance triage:

- **Auto-classification**: ML models classify alerts
- **Priority scoring**: Risk-based prioritization
- **Context enrichment**: Automatic IOC lookups
- **Playbook suggestion**: Recommended response actions

## Summary

Effective alert triage is essential for SOC efficiency. By following a structured process, analysts can quickly identify true threats and respond appropriately while minimizing time spent on false positives.

## Review Questions

1. What factors determine alert severity?
2. How do you differentiate between a true positive and false positive?
3. What is the maximum time recommended for initial triage?
4. How can AI assist in the triage process?

## Next Steps

Continue to [SOC Tools and Technologies](./04-tools.md) to learn about the key tools used in security operations.
