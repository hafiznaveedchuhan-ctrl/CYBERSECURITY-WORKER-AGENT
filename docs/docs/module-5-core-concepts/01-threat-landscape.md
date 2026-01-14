---
id: 01-threat-landscape
title: Chapter 1 - Understanding the Threat Landscape
sidebar_position: 1
---

# Understanding the Threat Landscape

The cybersecurity threat landscape is constantly evolving. Understanding current threats, threat actors, and attack vectors is essential for effective security operations.

## Threat Actor Categories

### Nation-State Actors (APTs)
- **Motivation**: Espionage, sabotage, geopolitical advantage
- **Capabilities**: Well-funded, sophisticated techniques
- **Targets**: Government, defense, critical infrastructure
- **Examples**: APT28, APT29, Lazarus Group
- **Impact**: High - can cause critical national/organizational damage

### Cybercriminals
- **Motivation**: Financial gain
- **Capabilities**: Varying levels, often use commodity malware
- **Targets**: Any organization with valuable data or assets
- **Examples**: Ransomware gangs (REvil, LockBit, BlackCat)
- **Impact**: Medium to High - widespread and damaging

### Hacktivists
- **Motivation**: Political or social causes
- **Capabilities**: Variable, often DDoS and defacement
- **Targets**: Organizations opposing their cause
- **Examples**: Anonymous, various regional groups
- **Impact**: Medium - often disruptive but short-lived

### Insider Threats
- **Motivation**: Revenge, financial gain, ideology
- **Capabilities**: Legitimate access, knowledge of systems
- **Targets**: Own organization
- **Risk Factors**: Disgruntled employees, contractors
- **Impact**: High - trusted access, hard to detect

## Common Attack Vectors

### Phishing and Social Engineering
The most common initial access vector:

- **Spear Phishing**: Targeted emails to specific individuals
  - Research organization and personnel
  - Personalized content increases success rate
  - Often includes malicious attachments or links

- **Business Email Compromise (BEC)**: Impersonating executives
  - Requests for wire transfers or sensitive data
  - Can result in significant financial loss
  - Often bypasses technical controls

- **Vishing**: Voice-based social engineering
  - Phone calls impersonating trusted parties
  - Tricks victim into revealing credentials
  - Difficult to detect without awareness training

- **Smishing**: SMS-based phishing
  - Text messages with malicious links
  - Often targets mobile users
  - May impersonate banks or services

### Exploitation of Vulnerabilities
- **Zero-Day Exploits**: Unknown vulnerabilities
  - No patch available yet
  - Highly valuable to attackers
  - Difficult to defend against

- **N-Day Exploits**: Known but unpatched vulnerabilities
  - Patch is available but not applied
  - Common due to operational constraints
  - Easily preventable with proper patching

- **Supply Chain Attacks**: Compromising software vendors
  - Affects all downstream customers
  - Difficult to detect
  - High impact (e.g., SolarWinds, KASEYA)

- **Misconfigurations**: Cloud, network, application errors
  - S3 buckets set to public
  - Default credentials left unchanged
  - Excessive permissions granted

### Credential Attacks
- **Password Spraying**: Testing common passwords
  - Tries same password across many accounts
  - Often successful with common passwords
  - Harder to detect than brute force

- **Credential Stuffing**: Using leaked credentials
  - Applies credentials from previous breaches
  - Very high success rate
  - Easy to automate

- **Brute Force**: Systematic password guessing
  - Tries many password combinations
  - Slow but effective without proper controls
  - Rate limiting helps prevent

- **Pass-the-Hash**: Using stolen credential hashes
  - Windows NTLM vulnerability
  - Doesn't require knowing actual password
  - Can be used for lateral movement

## Modern Threat Trends

### Ransomware Evolution
1. **Double Extortion**: Encrypt + data theft
   - Steals data before encrypting
   - Threatens to publish data if not paid
   - Increases pressure on victims

2. **Triple Extortion**: Add DDoS or customer notification
   - Also attacks customers/partners
   - Notifies customers of breach
   - Multiple pressure points on victims

3. **Ransomware-as-a-Service (RaaS)**: Affiliate models
   - Professional operations
   - Revenue sharing with affiliates
   - Sophisticated infrastructure

4. **Big Game Hunting**: Targeting large enterprises
   - High-value targets
   - Patient, long-term reconnaissance
   - Significant ransom demands

### Cloud Threats
- Misconfigured storage buckets (S3, Blob Storage)
- Excessive permissions (over-privileged accounts)
- Compromised API keys and tokens
- Container vulnerabilities
- Serverless code vulnerabilities

### AI-Enabled Attacks
- Deepfake voice for vishing
- AI-generated phishing content
- Automated vulnerability discovery
- Evasion of ML-based defenses

## MITRE ATT&CK Framework

The ATT&CK framework organizes adversary behavior into tactics and techniques, making it essential for SOC operations.

### Tactics (The "Why") - 14 Categories

1. **Reconnaissance** - Gather information about target
2. **Resource Development** - Acquire resources for attack
3. **Initial Access** - Get into the network
4. **Execution** - Run malicious code
5. **Persistence** - Maintain access
6. **Privilege Escalation** - Gain higher privileges
7. **Defense Evasion** - Avoid detection
8. **Credential Access** - Steal credentials
9. **Discovery** - Learn about the environment
10. **Lateral Movement** - Move through the network
11. **Collection** - Gather data of interest
12. **Command and Control** - Communicate with malware
13. **Exfiltration** - Steal data
14. **Impact** - Damage or destroy

### Techniques (The "How")

Each tactic contains multiple techniques describing specific adversary behaviors.

#### Example: T1566 - Phishing

```
Tactic: Initial Access
Technique: T1566 - Phishing
├─ T1566.001 - Spear Phishing Attachment
├─ T1566.002 - Phishing: Link
├─ T1566.003 - Spear Phishing via Service
└─ T1566.004 - Spear Phishing Attachment (alternative)
```

### Using ATT&CK in SOC Operations

| Use Case | Application |
|----------|-------------|
| **Detection Engineering** | Map detection rules to techniques for coverage analysis |
| **Threat Hunting** | Search for specific techniques and tactics |
| **Incident Analysis** | Classify observed behaviors and attack chain |
| **Red Team Planning** | Simulate realistic adversary behavior |
| **Security Gap Analysis** | Identify missing controls and detections |
| **Training** | Teach analysts about adversary behavior |

## Threat Intelligence Sources

### Open Source Intelligence (OSINT)
- **MITRE ATT&CK** - Tactics and techniques database
- **AlienVault OTX** - Threat indicators and analysis
- **Abuse.ch** - Malware and C2 tracking
- **VirusTotal** - File and URL scanning
- **GitHub** - Code repositories with IOCs

### Commercial Feeds
- **Recorded Future** - Threat intelligence platform
- **Mandiant** - Threat intelligence reports
- **CrowdStrike** - Adversary intelligence
- **Microsoft Threat Intelligence** - Cloud and endpoint data

### Government Sources
- **CISA Alerts** - US cybersecurity alerts
- **FBI Flash Reports** - FBI threat bulletins
- **NSA Cybersecurity Advisories** - NSA guidance
- **NCSC (UK)** - British cybersecurity advice

## Staying Current

To maintain awareness of the evolving threat landscape:

1. **Subscribe to threat intelligence feeds**
   - CISA alerts and advisories
   - Vendor threat reports
   - Industry-specific feeds

2. **Follow security researchers on social media**
   - Twitter security community
   - LinkedIn security experts
   - Blogs and research papers

3. **Attend industry conferences**
   - Virtual or in-person events
   - Black Hat, DEFCON, RSA, etc.
   - Vendor summits and webinars

4. **Participate in information sharing**
   - ISACs (Information Sharing and Analysis Centers)
   - CSIRT communities
   - Threat intelligence sharing groups

5. **Conduct regular threat landscape reviews**
   - Quarterly threat assessments
   - Industry trend analysis
   - Emerging threat evaluation

:::tip Key Insight
Prioritize threats based on your organization's industry, geography, and technology stack. Not all threats are equally relevant to every organization.
:::

## Threat Prioritization Matrix

Evaluate threats based on:

| Factor | Assessment | Priority |
|--------|------------|----------|
| **Likelihood** | How likely is this threat? | Medium |
| **Impact** | What damage could it cause? | High |
| **Capability** | Do attackers have skills? | Yes |
| **Motivation** | Is there motivation to attack? | Financial gain |
| **Overall Risk** | Likelihood × Impact | HIGH |

**Action**: Focus detection and prevention efforts on high-risk threats.
