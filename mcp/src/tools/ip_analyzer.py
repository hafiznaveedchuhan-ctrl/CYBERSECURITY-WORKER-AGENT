"""IP Address Analysis Tool."""

import re
from datetime import datetime


async def analyze(ip: str) -> str:
    """Analyze an IP address for threat intelligence."""
    # Validate IP format
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'

    if not (re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip)):
        return f"Error: Invalid IP address format: {ip}"

    # Check for private/reserved ranges
    is_private = is_private_ip(ip)

    result_lines = [
        f"IP Analysis Report",
        f"=" * 50,
        f"IP Address: {ip}",
        f"Analysis Time: {datetime.now().isoformat()}",
        "",
        "Basic Information:",
        f"  - IP Version: {'IPv6' if ':' in ip else 'IPv4'}",
        f"  - Private/Reserved: {'Yes' if is_private else 'No'}",
        "",
    ]

    if is_private:
        result_lines.extend([
            "Note: This is a private/reserved IP address.",
            "Private IPs are not routable on the public internet.",
            "",
        ])

    result_lines.extend([
        "Threat Intelligence (requires API keys):",
        "  - VirusTotal: [Configure VIRUSTOTAL_API_KEY]",
        "  - AbuseIPDB: [Configure ABUSEIPDB_API_KEY]",
        "  - Shodan: [Configure SHODAN_API_KEY]",
        "",
        "Geolocation (requires API):",
        "  - Country: Unknown",
        "  - City: Unknown",
        "  - ASN: Unknown",
        "  - Organization: Unknown",
        "",
        "Recommendations:",
    ])

    if is_private:
        result_lines.append("  - Internal IP - check internal network logs")
    else:
        result_lines.extend([
            "  - Check firewall logs for this IP",
            "  - Review any connections to/from this IP",
            "  - Consider blocking if malicious",
        ])

    return "\n".join(result_lines)


def is_private_ip(ip: str) -> bool:
    """Check if IP is in private/reserved range."""
    if ":" in ip:
        # IPv6 - simplified check
        return ip.lower().startswith(("fe80:", "fc", "fd", "::1"))

    # IPv4 private ranges
    parts = [int(p) for p in ip.split(".")]

    # 10.0.0.0/8
    if parts[0] == 10:
        return True
    # 172.16.0.0/12
    if parts[0] == 172 and 16 <= parts[1] <= 31:
        return True
    # 192.168.0.0/16
    if parts[0] == 192 and parts[1] == 168:
        return True
    # Loopback 127.0.0.0/8
    if parts[0] == 127:
        return True
    # Link-local 169.254.0.0/16
    if parts[0] == 169 and parts[1] == 254:
        return True

    return False
