---
id: ir-process
title: Incident Response Process
sidebar_label: IR Process
---

# Incident Response Process

Incident Response (IR) is a structured approach to handling security incidents. Following a consistent process ensures effective response and thorough documentation.

## IR Frameworks

### NIST SP 800-61
The National Institute of Standards and Technology framework consists of four phases:

1. **Preparation**
2. **Detection & Analysis**
3. **Containment, Eradication & Recovery**
4. **Post-Incident Activity**

### SANS 6-Step Process
1. Preparation
2. Identification
3. Containment
4. Eradication
5. Recovery
6. Lessons Learned

## Phase 1: Preparation

Preparation is the foundation of effective incident response.

### Key Preparation Activities

**People**
- Define IR team roles and responsibilities
- Establish escalation paths
- Conduct regular training and tabletop exercises
- Maintain contact lists (internal and external)

**Process**
- Develop and maintain IR playbooks
- Define incident classification criteria
- Establish communication templates
- Create evidence handling procedures

**Technology**
- Deploy and configure security tools
- Ensure logging is comprehensive
- Prepare forensic workstations
- Maintain jump bags with essential tools

### IR Team Structure

| Role | Responsibility |
|------|----------------|
| Incident Commander | Overall coordination and decision-making |
| Lead Investigator | Technical analysis and investigation |
| Communications Lead | Internal and external communications |
| Scribe | Documentation and timeline maintenance |
| Subject Matter Experts | Domain-specific technical assistance |

## Phase 2: Detection & Analysis

The goal is to quickly and accurately identify security incidents.

### Detection Sources

- SIEM alerts
- EDR detections
- User reports
- Threat intelligence
- External notifications
- Vulnerability scans

### Initial Triage

```
┌─────────────────────────────────────────┐
│              Alert Received              │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│         Is it a true positive?          │
└────────────────────┬────────────────────┘
          ┌─────────┴─────────┐
          ▼                   ▼
┌─────────────────┐   ┌─────────────────┐
│   False Pos.    │   │   True Pos.     │
│   Document &    │   │   Escalate &    │
│   Close         │   │   Investigate   │
└─────────────────┘   └─────────────────┘
```

### Incident Classification

| Severity | Criteria | Response Time |
|----------|----------|---------------|
| Critical | Business-critical systems, data exfiltration | Immediate |
| High | Significant impact, active compromise | < 1 hour |
| Medium | Limited impact, contained threat | < 4 hours |
| Low | Minimal impact, policy violation | < 24 hours |

### Key Analysis Questions

1. **What** happened?
2. **When** did it start?
3. **How** did it occur (attack vector)?
4. **Who** is affected?
5. **What** is the current scope?
6. **What** is the potential impact?

## Phase 3: Containment

The goal is to limit damage and prevent further spread.

### Short-Term Containment
Immediate actions to stop the bleeding:
- Isolate affected systems from network
- Block malicious IPs/domains
- Disable compromised accounts
- Preserve evidence before changes

### Long-Term Containment
Sustainable measures while investigating:
- Implement additional monitoring
- Apply temporary security controls
- Set up clean systems for affected users
- Maintain business operations

### Containment Decision Matrix

| Scenario | Recommended Action |
|----------|-------------------|
| Active ransomware | Immediate network isolation |
| Compromised user account | Disable account, reset credentials |
| C2 communication detected | Block domains/IPs at firewall |
| Malware on single endpoint | Isolate endpoint, begin forensics |
| Data exfiltration in progress | Block egress, preserve evidence |

:::warning
Always consider evidence preservation before containment actions. Document the current state before making changes.
:::

## Phase 4: Eradication

Remove the threat from the environment completely.

### Eradication Steps

1. **Identify root cause**: How did the attacker get in?
2. **Remove malware**: Clean or reimage affected systems
3. **Close vulnerabilities**: Patch exploited flaws
4. **Reset credentials**: Change all potentially compromised passwords
5. **Review for persistence**: Check for backdoors and persistence mechanisms

### Persistence Mechanisms to Check

- Scheduled tasks
- Registry run keys
- Services
- WMI subscriptions
- Startup folders
- Cron jobs
- SSH authorized_keys
- Web shells

## Phase 5: Recovery

Restore systems to normal operation safely.

### Recovery Steps

1. **Validate clean systems**: Verify eradication was successful
2. **Restore from backup**: Use known-good backups if needed
3. **Gradual reconnection**: Bring systems online incrementally
4. **Enhanced monitoring**: Watch for signs of re-compromise
5. **Validate business functions**: Confirm systems work correctly

### Recovery Checklist

- [ ] All malware removed
- [ ] Vulnerabilities patched
- [ ] Credentials reset
- [ ] Systems restored/rebuilt
- [ ] Data restored from backup
- [ ] Enhanced monitoring in place
- [ ] Business functions tested
- [ ] Stakeholders notified

## Phase 6: Lessons Learned

Improve future response through post-incident review.

### Post-Incident Meeting

Conduct within 1-2 weeks of incident closure:

**Agenda**
1. Incident timeline review
2. What went well
3. What could be improved
4. Action items for improvement
5. Documentation updates needed

### Key Metrics to Track

- Time to detect (TTD)
- Time to contain (TTC)
- Time to resolve (TTR)
- Number of systems affected
- Data impacted
- Business impact (downtime, cost)

### Improvement Actions

| Finding | Action | Owner | Due Date |
|---------|--------|-------|----------|
| Slow detection | Improve alerting | SOC | 30 days |
| Missing logs | Expand logging | IT | 60 days |
| Unclear process | Update playbook | IR Lead | 14 days |

## Documentation

Thorough documentation is essential throughout the process.

### Required Documentation

1. **Incident Timeline**: Chronological record of events
2. **Evidence Log**: Chain of custody for all evidence
3. **Actions Taken**: All containment and remediation steps
4. **Communications**: All stakeholder communications
5. **Final Report**: Executive summary and technical details

### Incident Report Template

```markdown
# Incident Report: [Incident ID]

## Executive Summary
Brief overview for leadership

## Incident Details
- Detection Date/Time:
- Incident Type:
- Severity:
- Status:

## Timeline
Chronological events

## Technical Analysis
Detailed technical findings

## Impact Assessment
Business and data impact

## Response Actions
Steps taken to contain and remediate

## Root Cause
How the incident occurred

## Recommendations
Preventive measures

## Appendices
Supporting evidence and data
```

:::tip Best Practice
Start documentation immediately when an incident is detected. Memory fades quickly, and accurate timelines are critical for legal proceedings and lessons learned.
:::
