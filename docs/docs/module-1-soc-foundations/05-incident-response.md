---
sidebar_position: 5
---

# Incident Response Basics

This section covers the fundamentals of incident response, including frameworks, processes, and best practices for handling security incidents.

## What is Incident Response?

**Incident Response (IR)** is the systematic approach to handling security incidents, including preparation, detection, containment, eradication, recovery, and lessons learned.

## Incident Response Frameworks

### NIST SP 800-61

The NIST Computer Security Incident Handling Guide defines four phases:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌────────────┐  ┌─────────────────┐  ┌──────────────────────┐ │
│  │Preparation │─►│Detection &      │─►│Containment,          │ │
│  │            │  │Analysis         │  │Eradication & Recovery│ │
│  └────────────┘  └─────────────────┘  └──────────────────────┘ │
│        ▲                                          │            │
│        │         ┌───────────────────┐            │            │
│        └─────────│Post-Incident      │◄───────────┘            │
│                  │Activity           │                         │
│                  └───────────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### SANS Incident Response Process

SANS defines six phases:

1. **Preparation**
2. **Identification**
3. **Containment**
4. **Eradication**
5. **Recovery**
6. **Lessons Learned**

## Phase 1: Preparation

Preparation is the foundation of effective incident response.

### Key Preparation Activities

**Documentation:**
- Incident response plan
- Communication templates
- Escalation procedures
- Contact lists

**Tools and Access:**
```markdown
## IR Toolkit Checklist

### Analysis Tools
- [ ] Forensic workstation
- [ ] Memory analysis tools (Volatility)
- [ ] Network analysis (Wireshark)
- [ ] Log analysis platform

### Access
- [ ] Admin credentials (secured)
- [ ] Network diagrams
- [ ] Asset inventory
- [ ] Backup access

### Communication
- [ ] War room (physical/virtual)
- [ ] Out-of-band communication
- [ ] Legal/PR contacts
```

**Training:**
- Tabletop exercises
- Red team engagements
- Playbook drills
- New hire onboarding

## Phase 2: Detection & Analysis

### Detection Sources

| Source | Examples |
|--------|----------|
| Automated | SIEM alerts, EDR detections, IDS/IPS |
| External | Threat intel feeds, vendor notifications |
| Internal | User reports, help desk tickets |
| Third-party | Law enforcement, security researchers |

### Initial Analysis

When an incident is detected:

1. **Validate the alert**
   - Is this a true positive?
   - What is the scope?

2. **Gather initial evidence**
   - System logs
   - Network traffic
   - User activity

3. **Determine severity**
   - Use your severity matrix
   - Consider business impact

### Severity Classification

| Level | Description | Example |
|-------|-------------|---------|
| SEV-1 | Critical business impact | Ransomware, active breach |
| SEV-2 | Significant impact | Confirmed malware, data exposure |
| SEV-3 | Limited impact | Contained incident, no data loss |
| SEV-4 | Minimal impact | Policy violation, false alarm |

## Phase 3: Containment

Containment prevents the incident from spreading.

### Containment Strategies

**Short-term Containment:**
- Isolate affected systems
- Block malicious IPs/domains
- Disable compromised accounts
- Preserve evidence

**Long-term Containment:**
- Rebuild systems from clean images
- Apply security patches
- Implement additional monitoring
- Update detection rules

### Containment Decision Matrix

```
                    Evidence Need
                    Low         High
              ┌─────────────┬─────────────┐
    Spread    │ Immediate   │ Controlled  │
    Risk High │ Isolation   │ Isolation   │
              ├─────────────┼─────────────┤
    Spread    │ Monitor &   │ Full        │
    Risk Low  │ Contain     │ Forensics   │
              └─────────────┴─────────────┘
```

### Containment Actions

```markdown
## System Isolation Checklist

### Network Isolation
- [ ] Remove from network (physical/VLAN)
- [ ] Block at firewall
- [ ] Disable VPN access
- [ ] Update DNS blackhole

### Account Isolation
- [ ] Disable user account
- [ ] Reset credentials
- [ ] Revoke sessions
- [ ] Update MFA

### Evidence Preservation
- [ ] Memory dump captured
- [ ] Disk image created
- [ ] Logs preserved
- [ ] Chain of custody documented
```

## Phase 4: Eradication

Eradication removes the threat from the environment.

### Eradication Steps

1. **Identify all affected systems**
   - Use IOCs to scan environment
   - Check lateral movement

2. **Remove malware/artifacts**
   - Clean or reimage systems
   - Remove persistence mechanisms
   - Delete malicious files

3. **Close attack vectors**
   - Patch vulnerabilities
   - Remove compromised credentials
   - Fix misconfigurations

### Root Cause Analysis

| Question | Purpose |
|----------|---------|
| How did the attacker get in? | Initial access vector |
| What vulnerabilities were exploited? | Technical weaknesses |
| How long were they present? | Dwell time |
| What data was accessed/exfiltrated? | Impact assessment |

## Phase 5: Recovery

Recovery restores normal operations securely.

### Recovery Steps

1. **Restore systems**
   - From clean backups
   - Verify integrity
   - Apply latest patches

2. **Validate security**
   - Penetration testing
   - Vulnerability scanning
   - Configuration review

3. **Monitor closely**
   - Enhanced logging
   - Increased alert sensitivity
   - Watch for re-infection

### Recovery Validation Checklist

```markdown
## Pre-Production Validation

### System Integrity
- [ ] OS verified clean
- [ ] Applications reinstalled
- [ ] Patches current
- [ ] Configurations hardened

### Security Verification
- [ ] AV/EDR active
- [ ] Logging enabled
- [ ] Access controls verified
- [ ] Network segmentation confirmed

### Monitoring
- [ ] Alerts configured
- [ ] IOCs integrated
- [ ] Baseline established
```

## Phase 6: Post-Incident Activity

Learning from incidents improves future response.

### Incident Report

```markdown
# Incident Report: [Incident ID]

## Executive Summary
Brief description of incident, impact, and resolution.

## Timeline
| Time | Event |
|------|-------|
| T+0 | Initial detection |
| T+15m | Containment initiated |
| ... | ... |

## Root Cause
Technical description of how the incident occurred.

## Impact
- Systems affected: X
- Data exposed: Y
- Downtime: Z hours

## Response Effectiveness
What worked well and what could improve.

## Recommendations
1. Immediate actions
2. Short-term improvements
3. Long-term investments

## Appendix
- IOCs
- Technical details
- Evidence chain
```

### Lessons Learned Meeting

Conduct within 2 weeks of incident closure:

**Agenda:**
1. Incident recap
2. Timeline review
3. What worked well
4. What could improve
5. Action items

## Incident Response Playbooks

### Playbook Structure

```yaml
name: Malware Incident Response
severity: High
classification: Malware

triggers:
  - EDR malware detection
  - AV signature match
  - User report

containment:
  immediate:
    - Isolate affected endpoint
    - Block C2 domains/IPs
  evidence:
    - Capture memory dump
    - Preserve disk image

eradication:
  - Remove malware artifacts
  - Reset compromised credentials
  - Patch vulnerabilities

recovery:
  - Reimage if necessary
  - Restore from backup
  - Verify clean state

communication:
  internal:
    - IT Leadership
    - Affected business unit
  external:
    - If data breach: Legal, PR
```

### Common Playbooks Needed

| Scenario | Priority |
|----------|----------|
| Ransomware | Critical |
| Business Email Compromise | Critical |
| Data Breach | Critical |
| Malware Infection | High |
| Insider Threat | High |
| DDoS Attack | High |
| Phishing | Medium |
| Account Compromise | Medium |

## Metrics and Improvement

### Key IR Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| MTTD | Time from incident start to detection | < 24 hours |
| MTTA | Time from detection to acknowledgment | < 15 minutes |
| MTTC | Time to contain the incident | < 4 hours |
| MTTR | Time to full recovery | < 72 hours |

### Continuous Improvement

- Regular playbook reviews
- Tabletop exercises quarterly
- Red team exercises annually
- Post-incident improvements tracked

## Summary

Effective incident response requires preparation, clear processes, and continuous improvement. Following a structured framework ensures consistent handling of security incidents while minimizing business impact.

## Review Questions

1. What are the six phases of the SANS IR process?
2. Why is evidence preservation important during containment?
3. What should be included in a post-incident report?
4. How do playbooks improve incident response?

## Module 1 Complete

Congratulations! You have completed Module 1: SOC Foundations. You now understand:
- SOC structure and organization
- Team roles and responsibilities
- Alert triage processes
- Key SOC tools and technologies
- Incident response fundamentals

Continue to [Module 2: Agentic AI](../module-2-agentic-ai/) to learn how AI agents can enhance security operations.
