"""Domain Analysis Tool."""

import re
from datetime import datetime


async def analyze(domain: str) -> str:
    """Analyze a domain for threat intelligence."""
    # Clean and validate domain
    domain = domain.strip().lower()

    # Remove protocol if present
    if "://" in domain:
        domain = domain.split("://")[1]

    # Remove path if present
    domain = domain.split("/")[0]

    # Basic validation
    if not is_valid_domain(domain):
        return f"Error: Invalid domain format: {domain}"

    result_lines = [
        f"Domain Analysis Report",
        f"=" * 50,
        f"Domain: {domain}",
        f"Analysis Time: {datetime.now().isoformat()}",
        "",
        "Domain Information:",
        f"  - TLD: .{domain.split('.')[-1]}",
        f"  - Subdomain Count: {len(domain.split('.')) - 2 if len(domain.split('.')) > 2 else 0}",
        "",
        "WHOIS Information (requires API):",
        "  - Registrar: Unknown",
        "  - Creation Date: Unknown",
        "  - Expiration Date: Unknown",
        "  - Registrant: Unknown",
        "",
        "DNS Records (requires lookup):",
        "  - A Records: Unknown",
        "  - MX Records: Unknown",
        "  - NS Records: Unknown",
        "  - TXT Records: Unknown",
        "",
        "Threat Intelligence (requires API keys):",
        "  - VirusTotal: [Configure VIRUSTOTAL_API_KEY]",
        "  - URLhaus: [Configure URLHAUS_API_KEY]",
        "  - PhishTank: [Check manually]",
        "",
        "Security Indicators:",
        "  - SSL Certificate: Unknown",
        "  - Domain Age: Unknown",
        "  - Reputation Score: Unknown",
        "",
    ]

    # Check for suspicious patterns
    warnings = check_suspicious_patterns(domain)
    if warnings:
        result_lines.append("Warnings:")
        for warning in warnings:
            result_lines.append(f"  - {warning}")
        result_lines.append("")

    result_lines.extend([
        "Recommendations:",
        "  - Check domain in VirusTotal",
        "  - Review DNS history for changes",
        "  - Check SSL certificate validity",
        "",
        "Manual Lookup URLs:",
        f"  - VirusTotal: https://www.virustotal.com/gui/domain/{domain}",
        f"  - URLhaus: https://urlhaus.abuse.ch/browse.php?search={domain}",
        f"  - WHOIS: https://whois.domaintools.com/{domain}",
    ])

    return "\n".join(result_lines)


def is_valid_domain(domain: str) -> bool:
    """Validate domain format."""
    # Basic domain validation
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))


def check_suspicious_patterns(domain: str) -> list[str]:
    """Check for suspicious domain patterns."""
    warnings = []

    # Check for lookalike characters
    lookalikes = {
        '0': 'o', '1': 'l', '5': 's', 'vv': 'w',
        'rn': 'm', 'cl': 'd', 'nn': 'm',
    }

    domain_lower = domain.lower()

    # Check for known brand impersonation patterns
    brands = ['google', 'microsoft', 'apple', 'amazon', 'paypal', 'facebook', 'instagram']
    for brand in brands:
        if brand in domain_lower and not domain_lower.endswith(f'.{brand}.com'):
            warnings.append(f"Possible {brand} impersonation")

    # Check for excessive hyphens
    if domain.count('-') > 3:
        warnings.append("Excessive hyphens (common in phishing)")

    # Check for very long subdomains
    parts = domain.split('.')
    for part in parts[:-2]:  # Exclude TLD and main domain
        if len(part) > 30:
            warnings.append("Unusually long subdomain")
            break

    # Check for IP-like patterns
    if re.search(r'\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}', domain):
        warnings.append("Contains IP-like pattern")

    # Check for suspicious TLDs
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work']
    for tld in suspicious_tlds:
        if domain.endswith(tld):
            warnings.append(f"Uses potentially suspicious TLD ({tld})")
            break

    return warnings
