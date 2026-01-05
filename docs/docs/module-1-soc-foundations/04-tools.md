---
sidebar_position: 4
---

# SOC Tools and Technologies

This section covers the essential tools and technologies used in modern Security Operations Centers.

## Core SOC Tools

### Security Information and Event Management (SIEM)

The SIEM is the central nervous system of the SOC, aggregating logs and generating alerts.

**Key Functions:**
- Log collection and normalization
- Correlation and alerting
- Dashboard and visualization
- Compliance reporting
- Threat detection

**Popular SIEM Solutions:**
| Tool | Type | Best For |
|------|------|----------|
| Splunk | Commercial | Large enterprises, complex analytics |
| Microsoft Sentinel | Cloud | Azure environments, O365 integration |
| Elastic Security | Open Source | Cost-effective, flexible deployments |
| IBM QRadar | Commercial | Regulated industries, compliance |
| LogRhythm | Commercial | Mid-size organizations |

**Key SIEM Queries:**

```sql
-- Splunk: Failed logins in last hour
index=security sourcetype=auth action=failure
| stats count by user, src_ip
| where count > 5

-- Elastic: Suspicious PowerShell
event.action:process_started AND
process.name:powershell.exe AND
process.command_line:*-enc*

-- Sentinel (KQL): Brute force detection
SecurityEvent
| where EventID == 4625
| summarize count() by TargetAccount, IpAddress
| where count_ > 10
```

### Endpoint Detection and Response (EDR)

EDR solutions provide visibility into endpoint activity and enable rapid response.

**Key Capabilities:**
- Real-time endpoint monitoring
- Behavioral analysis
- Threat hunting
- Remote containment
- Forensic data collection

**Popular EDR Solutions:**
- CrowdStrike Falcon
- Microsoft Defender for Endpoint
- Carbon Black
- SentinelOne
- Cortex XDR

**EDR Investigation Flow:**
```
Alert → Process Tree → Network Connections → File Activity → Response
```

### Security Orchestration, Automation, and Response (SOAR)

SOAR platforms automate repetitive tasks and coordinate incident response.

**Key Functions:**
- Playbook automation
- Case management
- Integration hub
- Metrics and reporting

**Popular SOAR Platforms:**
- Palo Alto XSOAR
- Splunk SOAR (Phantom)
- IBM Resilient
- ServiceNow Security Operations
- Swimlane

**Example Playbook:**

```yaml
name: Phishing Response
trigger: phishing_alert
steps:
  - extract_iocs:
      from: email
      types: [url, domain, hash]

  - enrich_iocs:
      services: [virustotal, urlscan]

  - if: ioc_malicious
    then:
      - block_sender
      - quarantine_email
      - search_other_recipients
      - create_incident

  - notify:
      channel: security-alerts
      severity: ${alert.severity}
```

### Threat Intelligence Platforms (TIP)

TIPs aggregate and operationalize threat intelligence.

**Key Functions:**
- IOC aggregation
- Intelligence enrichment
- STIX/TAXII support
- Integration with security tools

**Popular TIP Solutions:**
- MISP
- Anomali ThreatStream
- Recorded Future
- ThreatConnect

### Network Detection and Response (NDR)

NDR tools analyze network traffic for threats.

**Key Capabilities:**
- Traffic analysis
- Protocol decoding
- Anomaly detection
- Packet capture

**Popular NDR Solutions:**
- Darktrace
- Vectra AI
- ExtraHop
- Corelight

## Supporting Tools

### Vulnerability Management

| Tool | Type | Strengths |
|------|------|-----------|
| Tenable Nessus | Commercial | Comprehensive scanning |
| Qualys | Commercial | Cloud-based, scalable |
| Rapid7 InsightVM | Commercial | Risk-based prioritization |
| OpenVAS | Open Source | Free, community-supported |

### Forensic Tools

| Tool | Purpose |
|------|---------|
| Autopsy | Disk forensics |
| Volatility | Memory forensics |
| Wireshark | Network forensics |
| Velociraptor | Endpoint forensics |

### Threat Hunting Tools

| Tool | Purpose |
|------|---------|
| YARA | Pattern matching |
| Sigma | Generic detection rules |
| OSQuery | Endpoint querying |
| Jupyter | Analysis notebooks |

## Tool Integration Architecture

```
                              ┌─────────────┐
                              │   SOAR      │
                              │ (Orchestration)
                              └──────┬──────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
    ┌────▼────┐                ┌─────▼─────┐               ┌─────▼────┐
    │  SIEM   │◄──────────────►│    TIP    │◄─────────────►│   EDR    │
    │         │                │           │               │          │
    └────┬────┘                └───────────┘               └────┬─────┘
         │                                                      │
         └──────────────────┬───────────────────────────────────┘
                            │
                    ┌───────▼───────┐
                    │ Case Management│
                    │   & Ticketing  │
                    └───────────────┘
```

## Detection Rule Languages

### Sigma Rules

Sigma is a generic signature format for SIEM systems.

```yaml
title: Suspicious PowerShell Download Cradle
status: experimental
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        CommandLine|contains|all:
            - 'powershell'
            - 'IEX'
            - 'WebClient'
    condition: selection
level: high
tags:
    - attack.execution
    - attack.t1059.001
```

### YARA Rules

YARA is used for malware identification.

```yara
rule Suspicious_Executable
{
    meta:
        description = "Detects suspicious packed executable"
        author = "SOC Team"

    strings:
        $mz = "MZ"
        $packed = "UPX" wide
        $api1 = "VirtualAlloc"
        $api2 = "VirtualProtect"

    condition:
        $mz at 0 and $packed and all of ($api*)
}
```

### Snort/Suricata Rules

For network-based detection:

```
alert tcp any any -> any 443 (
    msg:"Potential C2 Communication";
    flow:established,to_server;
    content:"POST";
    http_method;
    content:"/beacon";
    http_uri;
    classtype:trojan-activity;
    sid:1000001;
    rev:1;
)
```

## API Integration

Modern SOC tools expose APIs for automation:

```python
# Example: VirusTotal IOC lookup
import requests

def check_hash(file_hash: str) -> dict:
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VT_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]
        return {
            "hash": file_hash,
            "malicious": stats["malicious"],
            "suspicious": stats["suspicious"],
            "harmless": stats["harmless"]
        }
    return None
```

## Tool Selection Criteria

When selecting SOC tools, consider:

1. **Integration Capability**
   - API availability
   - Native integrations
   - Standard formats (STIX, CEF, Syslog)

2. **Scalability**
   - Data volume handling
   - Endpoint count support
   - Cloud vs. on-premises

3. **Total Cost of Ownership**
   - Licensing model
   - Implementation costs
   - Training requirements

4. **Vendor Support**
   - Community size
   - Documentation quality
   - Update frequency

## Summary

A well-integrated toolset is essential for effective SOC operations. The key is selecting tools that work together seamlessly and automate routine tasks, allowing analysts to focus on high-value activities.

## Review Questions

1. What are the core functions of a SIEM?
2. How does EDR differ from traditional antivirus?
3. What role does SOAR play in the SOC?
4. Why is tool integration important?

## Next Steps

Continue to [Incident Response Basics](./05-incident-response.md) to learn the fundamentals of responding to security incidents.
