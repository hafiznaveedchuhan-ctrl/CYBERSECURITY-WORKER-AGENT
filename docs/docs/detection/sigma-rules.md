---
id: sigma-rules
title: Sigma Rules
sidebar_label: Sigma Rules
---

# Sigma Detection Rules

Sigma is a generic and open signature format that allows you to describe log events in a straightforward manner. It enables sharing of detection rules across different SIEM platforms.

## What is Sigma?

Sigma is to log files what YARA is to files and Snort is to network traffic. It provides:

- **Vendor-agnostic** detection rules
- **Shareable** format across organizations
- **Convertible** to various SIEM query languages
- **Standardized** detection engineering

## Rule Structure

A Sigma rule consists of several key sections:

```yaml
title: Detect Suspicious PowerShell Execution
id: 12345678-1234-1234-1234-123456789012
status: experimental
description: Detects suspicious PowerShell command line patterns
references:
    - https://attack.mitre.org/techniques/T1059/001/
author: SOC Team
date: 2024/01/15
modified: 2024/01/20

logsource:
    category: process_creation
    product: windows

detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains|all:
            - '-enc'
            - '-nop'
    condition: selection

falsepositives:
    - Legitimate administrative scripts
    - Software deployment tools

level: high

tags:
    - attack.execution
    - attack.t1059.001
```

## Key Components

### Metadata Fields

| Field | Description | Required |
|-------|-------------|----------|
| `title` | Short description | Yes |
| `id` | Unique UUID | Recommended |
| `status` | experimental, test, stable | Yes |
| `description` | Detailed explanation | Yes |
| `author` | Rule creator | Recommended |
| `date` | Creation date | Recommended |
| `level` | Severity level | Yes |

### Log Source

Defines where to look for events:

```yaml
logsource:
    product: windows          # OS or application
    category: process_creation # Event category
    service: sysmon           # Specific log source
```

Common categories:
- `process_creation`
- `network_connection`
- `file_event`
- `registry_event`
- `dns_query`

### Detection Logic

The `detection` section contains the actual rule logic:

```yaml
detection:
    selection_process:
        Image|endswith: '\cmd.exe'
    selection_command:
        CommandLine|contains:
            - '/c'
            - '/k'
    filter:
        ParentImage|endswith: '\explorer.exe'
    condition: (selection_process and selection_command) and not filter
```

### Modifiers

Sigma supports various field modifiers:

| Modifier | Description | Example |
|----------|-------------|---------|
| `contains` | Substring match | `CommandLine\|contains: '-enc'` |
| `endswith` | Suffix match | `Image\|endswith: '\cmd.exe'` |
| `startswith` | Prefix match | `User\|startswith: 'ADMIN'` |
| `all` | All values must match | `\|contains\|all:` |
| `base64` | Base64 decoded match | `\|base64:` |
| `re` | Regular expression | `\|re: '^cmd.*'` |

### Condition Logic

Combine selections with boolean operators:

```yaml
condition: selection1 or selection2
condition: selection1 and selection2
condition: selection1 and not filter
condition: 1 of selection*
condition: all of selection*
```

## Example Rules

### Detect Mimikatz Execution

```yaml
title: Mimikatz Execution
id: a0a278fe-2c0e-4de2-ac3c-c68b08a9ba98
status: stable
description: Detects Mimikatz credential dumping tool
author: SOC Team
date: 2024/01/15

logsource:
    category: process_creation
    product: windows

detection:
    selection_image:
        Image|endswith:
            - '\mimikatz.exe'
            - '\mimi.exe'
    selection_command:
        CommandLine|contains:
            - 'sekurlsa::'
            - 'kerberos::'
            - 'crypto::'
            - 'lsadump::'
    condition: selection_image or selection_command

falsepositives:
    - Legitimate security testing

level: critical

tags:
    - attack.credential_access
    - attack.t1003
```

### Detect Suspicious Network Connections

```yaml
title: Suspicious Outbound Connection from Office Application
id: b3e7a9d1-5f2a-4c8e-9d6f-1a2b3c4d5e6f
status: experimental
description: Detects Office applications making suspicious network connections

logsource:
    category: network_connection
    product: windows

detection:
    selection:
        Image|endswith:
            - '\winword.exe'
            - '\excel.exe'
            - '\powerpnt.exe'
        Initiated: 'true'
    filter_microsoft:
        DestinationHostname|endswith:
            - '.microsoft.com'
            - '.office.com'
    condition: selection and not filter_microsoft

level: medium

tags:
    - attack.command_and_control
    - attack.t1071
```

## Converting Rules

Sigma rules can be converted to various SIEM formats using `sigma-cli`:

```bash
# Install sigma-cli
pip install sigma-cli

# Convert to Splunk
sigma convert -t splunk rule.yml

# Convert to Elastic
sigma convert -t elasticsearch rule.yml

# Convert to Microsoft Sentinel
sigma convert -t microsoft365defender rule.yml
```

## Best Practices

### Writing Effective Rules

1. **Be Specific**: Avoid overly broad rules that generate false positives
2. **Include Filters**: Add filters for known legitimate activity
3. **Test Thoroughly**: Validate against real data before deployment
4. **Document Well**: Include references and detailed descriptions
5. **Use ATT&CK Tags**: Map to MITRE ATT&CK techniques

### Maintaining Rules

1. Regular review and updates
2. Track false positive rates
3. Adjust severity based on environment
4. Version control your rule sets
5. Share with the community (SigmaHQ)

### Rule Quality Checklist

- [ ] Unique UUID assigned
- [ ] Clear, descriptive title
- [ ] Detailed description
- [ ] ATT&CK technique mapping
- [ ] False positives documented
- [ ] Appropriate severity level
- [ ] Tested in lab environment
- [ ] Validated in production

:::tip Pro Tip
Start with rules from the [SigmaHQ repository](https://github.com/SigmaHQ/sigma) and customize them for your environment. Don't reinvent the wheel!
:::

## Resources

- [SigmaHQ GitHub](https://github.com/SigmaHQ/sigma)
- [Sigma Specification](https://github.com/SigmaHQ/sigma-specification)
- [pySigma Documentation](https://sigmahq.io/docs/basics/pysigma/)
