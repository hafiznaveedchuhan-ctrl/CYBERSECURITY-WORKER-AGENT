"""Threat intelligence MCP tools."""

import hashlib
import ipaddress
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class IOCReputationInput(BaseModel):
    """Input for IOC reputation lookup."""
    ioc: str = Field(..., description="IOC to check (IP, domain, hash)")
    ioc_type: str = Field(..., description="Type of IOC (ip, domain, md5, sha256)")


class GeoIPInput(BaseModel):
    """Input for GeoIP enrichment."""
    ip_address: str = Field(..., description="IP address to look up")


class MITREMapperInput(BaseModel):
    """Input for MITRE ATT&CK mapping."""
    description: str = Field(..., description="Attack or technique description")
    include_subtechniques: bool = Field(default=True)


class ThreatActorInput(BaseModel):
    """Input for threat actor lookup."""
    query: str = Field(..., description="Threat actor name, alias, or related IOC")


async def ioc_reputation(input: IOCReputationInput) -> dict:
    """
    Check reputation of an IOC against threat intelligence sources.

    Returns reputation score and associated threat data.
    """
    ioc = input.ioc
    ioc_type = input.ioc_type

    # Simulated reputation data (replace with actual TI integration)
    # In production, integrate with VirusTotal, OTX, MISP, etc.

    # Generate deterministic score based on IOC hash
    score_hash = int(hashlib.md5(ioc.encode()).hexdigest()[:8], 16)
    reputation_score = (score_hash % 100)

    is_malicious = reputation_score > 70
    is_suspicious = reputation_score > 40 and not is_malicious

    result = {
        "ioc": ioc,
        "ioc_type": ioc_type,
        "reputation_score": reputation_score,
        "verdict": "malicious" if is_malicious else ("suspicious" if is_suspicious else "clean"),
        "confidence": "high" if reputation_score > 80 or reputation_score < 20 else "medium",
        "sources_checked": ["virustotal", "otx", "misp", "abuse_ch"],
        "first_seen": "2024-01-15T10:30:00Z" if is_malicious else None,
        "last_seen": datetime.utcnow().isoformat() if is_malicious else None,
        "tags": [],
        "associated_malware": [],
        "associated_campaigns": [],
    }

    if is_malicious:
        result["tags"] = ["malware", "c2", "apt"]
        result["associated_malware"] = ["Emotet", "Cobalt Strike"]
        result["associated_campaigns"] = ["APT29 Campaign 2024"]
    elif is_suspicious:
        result["tags"] = ["suspicious", "newly_registered"]

    return result


async def enrichment_geoip(input: GeoIPInput) -> dict:
    """
    Enrich IP address with geolocation data.

    Returns country, ASN, and hosting information.
    """
    ip = input.ip_address

    # Validate IP
    try:
        ip_obj = ipaddress.ip_address(ip)
        is_private = ip_obj.is_private
        is_reserved = ip_obj.is_reserved
    except ValueError:
        return {"error": "Invalid IP address", "ip": ip}

    if is_private:
        return {
            "ip": ip,
            "is_private": True,
            "note": "Private IP address - no geolocation available",
        }

    # Simulated GeoIP data (replace with MaxMind or similar)
    # Generate deterministic location based on IP hash
    ip_hash = int(hashlib.md5(ip.encode()).hexdigest()[:8], 16)

    countries = ["US", "RU", "CN", "DE", "NL", "GB", "FR", "KR", "JP", "BR"]
    cities = {
        "US": ["New York", "Los Angeles", "Chicago"],
        "RU": ["Moscow", "Saint Petersburg"],
        "CN": ["Beijing", "Shanghai", "Shenzhen"],
        "DE": ["Berlin", "Frankfurt", "Munich"],
        "NL": ["Amsterdam", "Rotterdam"],
        "GB": ["London", "Manchester"],
        "FR": ["Paris", "Lyon"],
        "KR": ["Seoul", "Busan"],
        "JP": ["Tokyo", "Osaka"],
        "BR": ["Sao Paulo", "Rio de Janeiro"],
    }

    country = countries[ip_hash % len(countries)]
    city_list = cities[country]
    city = city_list[ip_hash % len(city_list)]

    hosting_providers = [
        "Amazon AWS", "Microsoft Azure", "Google Cloud",
        "DigitalOcean", "OVH", "Hetzner", "Linode"
    ]

    return {
        "ip": ip,
        "is_private": False,
        "country": country,
        "country_name": {
            "US": "United States", "RU": "Russia", "CN": "China",
            "DE": "Germany", "NL": "Netherlands", "GB": "United Kingdom",
            "FR": "France", "KR": "South Korea", "JP": "Japan", "BR": "Brazil"
        }[country],
        "city": city,
        "latitude": 40.7128 + (ip_hash % 100) / 10,
        "longitude": -74.0060 + (ip_hash % 100) / 10,
        "asn": f"AS{10000 + (ip_hash % 50000)}",
        "asn_org": hosting_providers[ip_hash % len(hosting_providers)],
        "is_hosting": ip_hash % 3 == 0,
        "is_vpn": ip_hash % 7 == 0,
        "is_tor": ip_hash % 20 == 0,
        "is_proxy": ip_hash % 10 == 0,
    }


async def mitre_mapper(input: MITREMapperInput) -> dict:
    """
    Map attack description to MITRE ATT&CK techniques.

    Returns matching techniques with descriptions.
    """
    description = input.description.lower()

    # MITRE ATT&CK technique database (subset)
    techniques = [
        {
            "id": "T1059.001",
            "name": "PowerShell",
            "tactic": "Execution",
            "keywords": ["powershell", "ps1", "invoke-expression", "iex", "-enc"],
            "description": "Adversaries may abuse PowerShell commands and scripts for execution.",
        },
        {
            "id": "T1021.001",
            "name": "Remote Desktop Protocol",
            "tactic": "Lateral Movement",
            "keywords": ["rdp", "remote desktop", "3389", "mstsc"],
            "description": "Adversaries may use RDP to laterally move within a network.",
        },
        {
            "id": "T1021.002",
            "name": "SMB/Windows Admin Shares",
            "tactic": "Lateral Movement",
            "keywords": ["smb", "admin share", "c$", "admin$", "445"],
            "description": "Adversaries may use SMB to laterally move within a network.",
        },
        {
            "id": "T1078",
            "name": "Valid Accounts",
            "tactic": "Defense Evasion, Persistence, Privilege Escalation, Initial Access",
            "keywords": ["valid account", "credential", "stolen credential", "compromised account"],
            "description": "Adversaries may use valid accounts to maintain access.",
        },
        {
            "id": "T1566.001",
            "name": "Spearphishing Attachment",
            "tactic": "Initial Access",
            "keywords": ["phishing", "spearphishing", "attachment", "malicious document"],
            "description": "Adversaries may send spearphishing emails with malicious attachments.",
        },
        {
            "id": "T1486",
            "name": "Data Encrypted for Impact",
            "tactic": "Impact",
            "keywords": ["ransomware", "encrypt", "ransom", "locked files"],
            "description": "Adversaries may encrypt data to impact availability.",
        },
        {
            "id": "T1082",
            "name": "System Information Discovery",
            "tactic": "Discovery",
            "keywords": ["systeminfo", "hostname", "os version", "system discovery"],
            "description": "Adversaries may gather system information.",
        },
        {
            "id": "T1055",
            "name": "Process Injection",
            "tactic": "Defense Evasion, Privilege Escalation",
            "keywords": ["process injection", "dll injection", "hollowing", "inject"],
            "description": "Adversaries may inject code into processes.",
        },
        {
            "id": "T1003",
            "name": "OS Credential Dumping",
            "tactic": "Credential Access",
            "keywords": ["credential dump", "mimikatz", "lsass", "sam database", "ntds"],
            "description": "Adversaries may dump credentials from the OS.",
        },
        {
            "id": "T1105",
            "name": "Ingress Tool Transfer",
            "tactic": "Command and Control",
            "keywords": ["download", "transfer", "wget", "curl", "certutil"],
            "description": "Adversaries may transfer tools to the victim environment.",
        },
    ]

    # Find matching techniques
    matches = []
    for tech in techniques:
        score = 0
        matched_keywords = []

        for keyword in tech["keywords"]:
            if keyword in description:
                score += 1
                matched_keywords.append(keyword)

        if score > 0:
            matches.append({
                "technique_id": tech["id"],
                "technique_name": tech["name"],
                "tactic": tech["tactic"],
                "description": tech["description"],
                "confidence": "high" if score >= 2 else "medium",
                "matched_keywords": matched_keywords,
                "score": score,
            })

    # Sort by score
    matches.sort(key=lambda x: x["score"], reverse=True)

    return {
        "query": input.description,
        "techniques": matches[:5],  # Top 5 matches
        "total_matches": len(matches),
        "mitre_version": "14.1",
    }


async def threat_actor_lookup(input: ThreatActorInput) -> dict:
    """
    Look up threat actor information.

    Returns known aliases, TTPs, and associated campaigns.
    """
    query = input.query.lower()

    # Simulated threat actor database
    threat_actors = {
        "apt29": {
            "name": "APT29",
            "aliases": ["Cozy Bear", "The Dukes", "CozyDuke", "YTTRIUM"],
            "origin": "Russia",
            "targets": ["Government", "Think Tanks", "Healthcare"],
            "description": "Russian state-sponsored threat actor known for espionage operations.",
            "techniques": ["T1566.001", "T1059.001", "T1078", "T1021.002"],
            "malware": ["WellMess", "WellMail", "SUNBURST"],
            "active": True,
        },
        "apt28": {
            "name": "APT28",
            "aliases": ["Fancy Bear", "Sofacy", "Pawn Storm", "STRONTIUM"],
            "origin": "Russia",
            "targets": ["Government", "Military", "Media"],
            "description": "Russian military intelligence threat actor.",
            "techniques": ["T1566", "T1055", "T1003", "T1105"],
            "malware": ["X-Agent", "Sofacy", "Zebrocy"],
            "active": True,
        },
        "lazarus": {
            "name": "Lazarus Group",
            "aliases": ["Hidden Cobra", "Guardians of Peace", "ZINC"],
            "origin": "North Korea",
            "targets": ["Financial", "Cryptocurrency", "Defense"],
            "description": "North Korean state-sponsored threat actor focused on financial gain.",
            "techniques": ["T1566", "T1486", "T1059", "T1082"],
            "malware": ["HOPLIGHT", "ELECTRICFISH", "FastCash"],
            "active": True,
        },
    }

    # Search for matching actor
    for key, actor in threat_actors.items():
        if query in key or query in actor["name"].lower():
            return {"found": True, "actor": actor}
        for alias in actor["aliases"]:
            if query in alias.lower():
                return {"found": True, "actor": actor}

    return {
        "found": False,
        "query": input.query,
        "suggestion": "Try searching with known APT names or aliases",
    }


# Tool registry
THREAT_INTEL_TOOLS = {
    "ioc_reputation": {
        "function": ioc_reputation,
        "schema": IOCReputationInput,
        "description": "Check reputation of an IOC against threat intelligence sources",
    },
    "enrichment_geoip": {
        "function": enrichment_geoip,
        "schema": GeoIPInput,
        "description": "Enrich IP address with geolocation data",
    },
    "mitre_mapper": {
        "function": mitre_mapper,
        "schema": MITREMapperInput,
        "description": "Map attack description to MITRE ATT&CK techniques",
    },
    "threat_actor_lookup": {
        "function": threat_actor_lookup,
        "schema": ThreatActorInput,
        "description": "Look up threat actor information",
    },
}
