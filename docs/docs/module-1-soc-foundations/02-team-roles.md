---
sidebar_position: 2
---

# SOC Team Roles

A well-functioning SOC requires a diverse team with complementary skills. This section covers the key roles and responsibilities within a modern Security Operations Center.

## Core SOC Roles

### SOC Manager

The SOC Manager oversees all SOC operations and is responsible for:

- **Strategic Planning**: Defining SOC goals and metrics
- **Team Management**: Hiring, training, and performance evaluation
- **Budget Management**: Allocating resources for tools and personnel
- **Stakeholder Communication**: Reporting to executive leadership
- **Process Improvement**: Continuously optimizing SOC workflows

**Required Skills:**
- Leadership and management experience
- Deep understanding of security operations
- Strong communication skills
- Business acumen

### Security Analyst (Tier 1)

The first line of defense in the SOC:

**Responsibilities:**
- Monitor security dashboards and SIEM alerts
- Perform initial alert triage and classification
- Document alert investigations
- Escalate suspicious activity to Tier 2
- Follow standard operating procedures (SOPs)

**Required Skills:**
- Basic understanding of networking and security
- Familiarity with SIEM tools
- Attention to detail
- Ability to work under pressure

### Incident Responder (Tier 2)

Handles escalated incidents requiring deeper investigation:

**Responsibilities:**
- Conduct detailed incident analysis
- Perform forensic investigation
- Coordinate containment and eradication
- Develop incident timelines
- Write incident reports

**Required Skills:**
- Advanced knowledge of attack techniques
- Forensic analysis capabilities
- Log analysis expertise
- Strong documentation skills

### Threat Hunter (Tier 3)

Proactively searches for hidden threats:

**Responsibilities:**
- Develop and test hunting hypotheses
- Analyze historical data for indicators
- Identify gaps in detection coverage
- Create new detection rules
- Research emerging threats

**Required Skills:**
- Deep understanding of adversary tactics (MITRE ATT&CK)
- Advanced analytics and scripting
- Creative problem-solving
- Research and analysis abilities

### Detection Engineer

Builds and maintains detection capabilities:

**Responsibilities:**
- Write and tune detection rules
- Develop SIEM correlation logic
- Create Sigma, YARA, and Snort rules
- Reduce false positives
- Validate detection coverage

**Required Skills:**
- Regular expression and query languages
- Understanding of log formats
- Knowledge of attack patterns
- Programming/scripting abilities

### Threat Intelligence Analyst

Provides context for security decisions:

**Responsibilities:**
- Collect and analyze threat intelligence
- Create threat profiles and reports
- Map threats to organizational risks
- Share intelligence with analysts
- Track threat actor campaigns

**Required Skills:**
- OSINT research capabilities
- Analytical thinking
- Report writing
- Understanding of threat landscapes

## Supporting Roles

### Security Architect

Designs security infrastructure:
- Security tool selection and integration
- Network security architecture
- Cloud security design

### Forensic Analyst

Conducts detailed forensic investigations:
- Disk and memory forensics
- Malware analysis
- Evidence preservation

### Automation Engineer

Builds SOC automation:
- SOAR playbook development
- API integrations
- Custom tool development

## Team Structure Example

```
                    ┌─────────────────┐
                    │   SOC Manager   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌─────▼─────┐        ┌────▼────┐
   │ Tier 1  │         │  Tier 2   │        │ Tier 3  │
   │ Analysts│         │ Responders│        │ Hunters │
   │ (4-6)   │         │   (2-3)   │        │  (1-2)  │
   └─────────┘         └───────────┘        └─────────┘
```

## Shift Coverage

24/7 SOCs typically use shift rotations:

| Shift | Hours | Coverage |
|-------|-------|----------|
| Day | 8 AM - 4 PM | Primary analysts |
| Swing | 4 PM - 12 AM | Secondary team |
| Night | 12 AM - 8 AM | Skeleton crew |

## Career Progression

Typical SOC career path:

1. **Entry Level**: Tier 1 Analyst (0-2 years)
2. **Intermediate**: Tier 2 Responder (2-4 years)
3. **Senior**: Tier 3 Hunter / Specialist (4-7 years)
4. **Leadership**: SOC Manager / Director (7+ years)

## Certifications

Valuable certifications for SOC professionals:

| Role | Recommended Certifications |
|------|---------------------------|
| Tier 1 | CompTIA Security+, CySA+ |
| Tier 2 | GCIH, ECIH, CEH |
| Tier 3 | GCIA, OSCP, GREM |
| Manager | CISM, CISSP |

## Summary

A successful SOC requires a well-rounded team with diverse skills. Understanding the different roles helps organizations build effective teams and provides clarity for career development in security operations.

## Review Questions

1. What distinguishes a Tier 2 analyst from a Tier 1 analyst?
2. What are the primary responsibilities of a Detection Engineer?
3. How does shift coverage typically work in a 24/7 SOC?
4. What career progression options exist within a SOC?

## Next Steps

Continue to [Alert Triage Process](./03-alert-triage.md) to learn how SOC analysts prioritize and investigate security alerts.
