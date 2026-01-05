"""Sigma Rule Generator Tool."""

from datetime import datetime
from uuid import uuid4


def generate(
    title: str,
    description: str,
    log_source: str = "windows",
    severity: str = "medium",
    mitre_techniques: list[str] = None,
) -> str:
    """Generate a Sigma detection rule."""
    rule_id = str(uuid4())
    date = datetime.now().strftime("%Y/%m/%d")

    # Map log source to Sigma logsource
    logsource_config = get_logsource_config(log_source)

    # Generate tags
    tags = []
    if mitre_techniques:
        for technique in mitre_techniques:
            # Format: attack.tXXXX or attack.tXXXX.XXX
            technique = technique.lower()
            if not technique.startswith("attack."):
                technique = f"attack.{technique}"
            tags.append(technique)

    tags_yaml = "\n".join(f"    - {tag}" for tag in tags) if tags else "    - attack.execution"

    # Generate placeholder detection logic based on log source
    detection_logic = get_detection_template(log_source)

    rule = f'''title: {title}
id: {rule_id}
status: experimental
description: |
    {description}
references:
    - https://attack.mitre.org/
author: AI SOC Platform
date: {date}
modified: {date}

logsource:
{logsource_config}

detection:
{detection_logic}

falsepositives:
    - Legitimate administrative activity
    - Update the filter section to reduce false positives

level: {severity}

tags:
{tags_yaml}
'''

    return f"Generated Sigma Rule:\n```yaml\n{rule}\n```\n\nNote: Update the detection logic with specific field values for your environment."


def get_logsource_config(log_source: str) -> str:
    """Get logsource configuration for Sigma rule."""
    configs = {
        "windows": '''    product: windows
    category: process_creation''',

        "linux": '''    product: linux
    category: process_creation''',

        "network": '''    category: firewall
    # Or use: category: proxy, category: dns''',

        "cloud": '''    product: aws
    service: cloudtrail
    # Or use: product: azure, product: gcp''',

        "web": '''    category: webserver
    # Or use: category: proxy''',
    }

    return configs.get(log_source, configs["windows"])


def get_detection_template(log_source: str) -> str:
    """Get detection logic template based on log source."""
    templates = {
        "windows": '''    selection:
        # Process creation fields
        Image|endswith:
            - '\\suspicious.exe'
            - '\\malware.exe'
        # Or use CommandLine, ParentImage, User, etc.
        # CommandLine|contains:
        #     - 'suspicious_command'
    filter:
        # Filter out known good activity
        Image|endswith: '\\legitimate.exe'
    condition: selection and not filter''',

        "linux": '''    selection:
        # Process execution
        Image|endswith:
            - '/suspicious'
        # CommandLine|contains:
        #     - 'malicious_command'
    condition: selection''',

        "network": '''    selection:
        # Network indicators
        dst_ip:
            - '10.0.0.1'  # Replace with actual IOCs
        dst_port:
            - 4444
            - 8080
    condition: selection''',

        "cloud": '''    selection:
        eventName:
            - 'ConsoleLogin'
            - 'CreateUser'
        # errorCode: 'AccessDenied'
    condition: selection''',

        "web": '''    selection:
        cs-uri-query|contains:
            - 'cmd='
            - 'exec='
            - '../'
    condition: selection''',
    }

    return templates.get(log_source, templates["windows"])
