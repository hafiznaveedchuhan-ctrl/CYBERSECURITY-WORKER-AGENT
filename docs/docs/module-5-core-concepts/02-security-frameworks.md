---
id: 02-security-frameworks
title: Chapter 2 - Security Frameworks & Standards
sidebar_position: 2
---

# Security Frameworks & Standards

Security frameworks provide structured approaches to managing cybersecurity risk. Understanding these frameworks is essential for SOC operations and compliance.

## NIST Cybersecurity Framework (CSF)

The NIST CSF is widely adopted across industries and provides a flexible approach to managing cybersecurity risk.

### Core Functions

| Function | Purpose | Key Activities |
|----------|---------|----------------|
| **Identify** | Understand your environment | Asset inventory, risk assessment, vulnerability management |
| **Protect** | Implement safeguards | Access control, training, data security, encryption |
| **Detect** | Identify security events | Monitoring, anomaly detection, logging, threat intelligence |
| **Respond** | Take action on incidents | IR planning, communications, containment, eradication |
| **Recover** | Restore capabilities | Recovery planning, improvements, lessons learned |

### Implementation Tiers

1. **Partial (Tier 1)**: Ad-hoc, reactive
   - Limited awareness of security risks
   - Processes not documented
   - No formal incident response

2. **Risk-Informed (Tier 2)**: Approved but not organization-wide
   - Risk management practices in place
   - Policies approved but inconsistent
   - Incident response procedures exist

3. **Repeatable (Tier 3)**: Formal policies, regularly updated
   - Formal risk management
   - Policies applied consistently
   - Regular reviews and updates

4. **Adaptive (Tier 4)**: Continuous improvement based on lessons
   - Advanced threat intelligence
   - Continuous monitoring and optimization
   - Automated processes and intelligence

### SOC Alignment

```
SOC Function          NIST CSF Alignment
─────────────────────────────────────────
Alert Detection       Detect function
Triage & Analysis    Detect function
Threat Hunting       Detect function
Incident Response    Respond function
Security Monitoring  Detect function
```

## MITRE ATT&CK Framework

A knowledge base of adversary tactics and techniques based on real-world observations.

### Key Components

- **Tactics**: The adversary's high-level objectives (14 total)
- **Techniques**: How objectives are achieved (150+ techniques)
- **Procedures**: Specific implementations used by threat actors
- **Mitigations**: Defensive measures and controls
- **Detections**: Methods to identify technique usage

### SOC Applications

| Use Case | ATT&CK Application | Benefit |
|----------|------------------|---------|
| **Detection Engineering** | Map rules to techniques | Understand coverage |
| **Threat Hunting** | Prioritize based on coverage gaps | Find missing detections |
| **Incident Analysis** | Classify observed behaviors | Standardize reporting |
| **Red Team Planning** | Simulate realistic adversary TTPs | Test defenses |
| **Security Gap Analysis** | Identify missing controls | Prioritize investments |
| **Training** | Teach analysts about adversary patterns | Build expertise |

### Coverage Analysis

Track which techniques you can detect and respond to:

```
Techniques Covered:     92 of 150 (61%)
Techniques With Rules:  45 of 150 (30%)
Techniques Huntable:    25 of 150 (17%)
Blind Spots:           58 of 150 (39%)

Action: Develop detections for high-risk blind spots
```

## CIS Controls

The Center for Internet Security (CIS) Controls are prioritized security actions based on real-world attack patterns.

### Implementation Groups

**IG1 (Essential)**: Basic cyber hygiene - All organizations

- Inventory of hardware/software assets
- Secure configuration
- Continuous vulnerability management
- Access control
- Email and browser protections
- Malware defenses

**IG2 (Foundational)**: Medium-sized organizations

- All IG1 controls plus:
- Data protection
- Audit logging
- Security awareness training
- Application security

**IG3 (Organizational)**: Large enterprises

- All IG1 and IG2 controls plus:
- Penetration testing and simulations
- Advanced incident response
- Network segmentation
- Advanced threat detection

### Mapping to SOC Activities

| CIS Control | SOC Activity |
|-------------|--------------|
| Control 6: Protect User Accounts | Enforce MFA, manage credentials |
| Control 8: Malware Defenses | Monitor and block malware |
| Control 13: Network Monitoring | SIEM and logging |
| Control 17: Incident Response | Incident management process |
| Control 18: Application Security | Code review and testing |

## ISO 27001

International standard for Information Security Management Systems (ISMS).

### Key Domains (14 Total)

1. Information Security Policies
2. Organization of Information Security
3. Human Resource Security
4. Asset Management
5. Access Control
6. Cryptography
7. Physical Security
8. Operations Security
9. Communications Security
10. System Acquisition and Development
11. Supplier Relationships
12. Incident Management
13. Business Continuity
14. Compliance

### Certification Process

1. **Gap Analysis**: Identify current state vs ISO 27001
2. **Risk Assessment**: Understand threats and vulnerabilities
3. **Policy Development**: Create security policies
4. **Implementation**: Deploy controls
5. **Internal Audit**: Test effectiveness
6. **External Audit**: Independent verification
7. **Certification**: Achieve ISO 27001 certification
8. **Ongoing Maintenance**: Regular reviews and updates

### SOC Responsibility

ISO 27001 requires:
- Incident management procedures (A.16.1)
- Incident response plan (A.16.1.5)
- Incident monitoring (A.16.1.2)
- Post-incident review (A.16.1.5)

## SOC 2

Service Organization Control 2 - focused on service providers managing customer data.

### Trust Services Criteria

| Criterion | Focus Area |
|-----------|------------|
| **Security** | Protection against unauthorized access |
| **Availability** | Systems available for operation |
| **Processing Integrity** | Accurate and timely processing |
| **Confidentiality** | Protection of confidential information |
| **Privacy** | Personal information protection |

### Type I vs Type II

- **Type I**: Point-in-time assessment (single moment)
- **Type II**: Assessment over a period (usually 6-12 months)

### Key Controls

- Access control and authentication
- Monitoring and alerting
- Incident response procedures
- Encryption for data protection
- Audit logging and retention
- Change management
- Network segmentation
- Disaster recovery and business continuity

## Framework Comparison

| Aspect | NIST CSF | ISO 27001 | CIS Controls | SOC 2 |
|--------|----------|-----------|--------------|-------|
| **Type** | Risk-based | Standard | Best practices | Service provider |
| **Scope** | Organization-wide | ISMS | Controls list | Service operations |
| **Tiers/Levels** | 4 tiers | 14 domains | 3 groups | 2 types |
| **Certification** | No formal cert | Yes (external audit) | No formal cert | Yes (Type II) |
| **Flexibility** | High | Structured | Prescriptive | Structured |

## Framework Selection

Consider these factors when choosing frameworks:

### Industry Requirements

- **Healthcare**: HIPAA, HITRUST
- **Financial**: PCI-DSS, SOX, GLBA
- **Government**: FedRAMP, FISMA
- **All Industries**: NIST CSF, ISO 27001

### Organization Size

- **Small (1-50 people)**: CIS Controls IG1
- **Medium (50-500 people)**: CIS Controls IG2, NIST CSF
- **Large (500+ people)**: Full NIST CSF, ISO 27001, SOC 2 Type II

### Compliance Requirements

Regulatory requirements often mandate specific frameworks:
- GDPR: ISO 27001 aligned
- PCI-DSS: SOC 2 Type II
- HIPAA: NIST CSF
- SOX: Internal controls framework

### Risk Profile

- **High Risk**: NIST CSF + ISO 27001
- **Medium Risk**: NIST CSF + CIS IG2
- **Low Risk**: CIS IG1

## Mapping Frameworks

Understanding how frameworks map to each other helps avoid duplication:

| NIST CSF | CIS Control | ISO 27001 |
|----------|-------------|-----------|
| ID.AM (Asset Management) | 1, 2 | A.8 |
| PR.AC (Access Control) | 4, 5, 6 | A.9 |
| PR.DS (Data Security) | 3, 13, 14 | A.10, A.13 |
| DE.CM (Detection/Monitoring) | 6, 7, 8, 12 | A.12 |
| RS.RP (Response Planning) | 17, 19 | A.16 |
| RC.RP (Recovery Planning) | 11 | A.17 |

## Continuous Improvement

Frameworks are not one-time implementations:

1. **Regular Assessments** (Quarterly)
   - Review current state
   - Identify gaps
   - Prioritize improvements

2. **Gap Analysis Updates** (Semi-Annual)
   - Compare against framework requirements
   - Track remediation progress
   - Adjust roadmap

3. **Control Effectiveness Testing** (Quarterly)
   - Verify controls work as intended
   - Test incident response procedures
   - Conduct security assessments

4. **Metrics and Reporting** (Monthly)
   - Track control metrics
   - Report to management
   - Identify trends

5. **Lessons Learned Integration** (Post-Incident)
   - Review all incidents
   - Update controls based on findings
   - Share knowledge across organization

## Implementation Roadmap

### Phase 1: Assessment (Months 1-2)
- Understand current state
- Identify gaps
- Prioritize controls

### Phase 2: Planning (Months 2-3)
- Develop policies and procedures
- Allocate resources
- Create implementation timeline

### Phase 3: Implementation (Months 3-12)
- Deploy controls
- Configure systems
- Train personnel

### Phase 4: Validation (Months 10-12)
- Audit controls
- Test procedures
- Verify effectiveness

### Phase 5: Continuous Improvement (Ongoing)
- Regular reviews
- Metric tracking
- Lessons learned

:::tip Key Principle
Don't try to implement multiple frameworks from scratch. Map your existing controls to chosen frameworks and identify gaps. Most frameworks have significant overlap - focus on closing the gaps efficiently.
:::

## Summary

Understanding security frameworks is essential for:

✅ Prioritizing security investments
✅ Meeting compliance requirements
✅ Building effective SOC processes
✅ Communicating with management
✅ Achieving industry certifications
✅ Continuously improving security

Choose frameworks that align with your industry, organization size, and risk profile. Use mapping to avoid duplication and focus resources on closing security gaps.
