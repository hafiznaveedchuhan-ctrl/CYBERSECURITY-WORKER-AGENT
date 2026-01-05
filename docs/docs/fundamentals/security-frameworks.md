---
id: security-frameworks
title: Security Frameworks
sidebar_label: Security Frameworks
---

# Security Frameworks

Security frameworks provide structured approaches to managing cybersecurity risk. Understanding these frameworks is essential for SOC operations and compliance.

## NIST Cybersecurity Framework (CSF)

The NIST CSF is widely adopted across industries and provides a flexible approach to managing cybersecurity risk.

### Core Functions

| Function | Purpose | Key Activities |
|----------|---------|----------------|
| **Identify** | Understand your environment | Asset inventory, risk assessment |
| **Protect** | Implement safeguards | Access control, training, data security |
| **Detect** | Identify security events | Monitoring, anomaly detection |
| **Respond** | Take action on incidents | IR planning, communications |
| **Recover** | Restore capabilities | Recovery planning, improvements |

### Implementation Tiers

1. **Partial**: Ad-hoc, reactive
2. **Risk-Informed**: Approved but not organization-wide
3. **Repeatable**: Formal policies, regularly updated
4. **Adaptive**: Continuous improvement based on lessons

## MITRE ATT&CK

A knowledge base of adversary tactics and techniques based on real-world observations.

### Key Components

- **Tactics**: The adversary's objectives
- **Techniques**: How objectives are achieved
- **Procedures**: Specific implementations
- **Mitigations**: Defensive measures
- **Detections**: How to identify techniques

### SOC Applications

```
Use Case                    | ATT&CK Application
---------------------------|----------------------------------
Detection Engineering      | Map rules to techniques
Threat Hunting            | Prioritize based on coverage gaps
Incident Analysis         | Classify observed behaviors
Red Team Planning         | Simulate realistic adversary TTPs
Security Gap Analysis     | Identify missing controls
```

## CIS Controls

The Center for Internet Security (CIS) Controls are prioritized security actions.

### Implementation Groups

**IG1 (Essential)**: Basic cyber hygiene
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
- Security awareness
- Application security

**IG3 (Organizational)**: Large enterprises
- All IG1 and IG2 controls plus:
- Penetration testing
- Incident response
- Network monitoring

## ISO 27001

International standard for Information Security Management Systems (ISMS).

### Key Domains

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

1. Gap analysis
2. Risk assessment
3. Policy development
4. Implementation
5. Internal audit
6. External audit
7. Certification
8. Ongoing maintenance

## SOC 2

Service Organization Control 2 - focused on service providers.

### Trust Services Criteria

| Criterion | Focus Area |
|-----------|------------|
| Security | Protection against unauthorized access |
| Availability | Systems available for operation |
| Processing Integrity | Accurate and timely processing |
| Confidentiality | Protection of confidential information |
| Privacy | Personal information protection |

### Type I vs Type II

- **Type I**: Point-in-time assessment
- **Type II**: Assessment over a period (usually 6-12 months)

## Framework Selection

Consider these factors when choosing frameworks:

### Industry Requirements
- **Healthcare**: HIPAA, HITRUST
- **Financial**: PCI-DSS, SOX
- **Government**: FedRAMP, FISMA
- **All Industries**: NIST CSF, ISO 27001

### Organization Size
- **Small**: CIS Controls IG1
- **Medium**: CIS Controls IG2, NIST CSF
- **Large**: Full NIST CSF, ISO 27001

### Compliance Requirements
Regulatory requirements often mandate specific frameworks or controls.

:::tip Best Practice
Don't try to implement multiple frameworks from scratch. Map your existing controls to chosen frameworks and identify gaps. Most frameworks have significant overlap.
:::

## Mapping Frameworks

| NIST CSF | CIS Control | ISO 27001 |
|----------|-------------|-----------|
| ID.AM | 1, 2 | A.8 |
| PR.AC | 4, 5, 6 | A.9 |
| PR.DS | 3, 13, 14 | A.10, A.13 |
| DE.CM | 6, 7, 8, 12 | A.12 |
| RS.RP | 17, 19 | A.16 |

## Continuous Improvement

Frameworks are not one-time implementations:

1. Regular assessments
2. Gap analysis updates
3. Control effectiveness testing
4. Metrics and reporting
5. Lessons learned integration
