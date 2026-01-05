"""Evidence and logs MCP tools."""

import re
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field


class LogSearchInput(BaseModel):
    """Input for log search tool."""
    query: str = Field(..., description="Search query for logs")
    time_range: str = Field(default="1h", description="Time range (1h, 24h, 7d, 30d)")
    source: str = Field(default="all", description="Log source (firewall, edr, siem, all)")
    limit: int = Field(default=100, ge=1, le=1000)


class LogSearchResult(BaseModel):
    """A single log entry."""
    timestamp: str
    source: str
    message: str
    severity: str
    metadata: dict


class EventTimelineInput(BaseModel):
    """Input for event timeline tool."""
    entity: str = Field(..., description="Entity to build timeline for (IP, user, host)")
    entity_type: str = Field(..., description="Type of entity (ip, user, host)")
    time_range: str = Field(default="24h")


class TimelineEvent(BaseModel):
    """A timeline event."""
    timestamp: str
    event_type: str
    description: str
    source: str
    severity: str


class NormalizeIOCsInput(BaseModel):
    """Input for IOC normalization."""
    raw_text: str = Field(..., description="Raw text containing IOCs")


class ParseRawLogInput(BaseModel):
    """Input for raw log parsing."""
    raw_log: str = Field(..., description="Raw log entry to parse")
    log_format: Optional[str] = Field(default=None, description="Expected format (cef, syslog, json)")


async def log_search(input: LogSearchInput) -> dict:
    """
    Search logs for specific patterns or queries.

    This tool searches across log sources for matching entries.
    """
    # Parse time range
    time_map = {
        "1h": timedelta(hours=1),
        "24h": timedelta(hours=24),
        "7d": timedelta(days=7),
        "30d": timedelta(days=30),
    }
    delta = time_map.get(input.time_range, timedelta(hours=1))
    start_time = datetime.utcnow() - delta

    # Simulated log search (replace with actual SIEM integration)
    sample_logs = [
        LogSearchResult(
            timestamp=datetime.utcnow().isoformat(),
            source="firewall",
            message=f"Connection from {input.query} to internal network",
            severity="medium",
            metadata={"src_ip": input.query, "dst_port": 443}
        ),
        LogSearchResult(
            timestamp=(datetime.utcnow() - timedelta(minutes=5)).isoformat(),
            source="edr",
            message=f"Process execution related to {input.query}",
            severity="high",
            metadata={"process": "powershell.exe", "user": "SYSTEM"}
        ),
    ]

    return {
        "query": input.query,
        "time_range": input.time_range,
        "source": input.source,
        "results": [log.model_dump() for log in sample_logs],
        "total_count": len(sample_logs),
    }


async def event_timeline(input: EventTimelineInput) -> dict:
    """
    Build a timeline of events for an entity.

    Creates a chronological view of all activities related to the entity.
    """
    # Simulated timeline (replace with actual data source)
    events = [
        TimelineEvent(
            timestamp=(datetime.utcnow() - timedelta(hours=2)).isoformat(),
            event_type="login",
            description=f"Successful login for {input.entity}",
            source="auth_logs",
            severity="info"
        ),
        TimelineEvent(
            timestamp=(datetime.utcnow() - timedelta(hours=1, minutes=30)).isoformat(),
            event_type="network",
            description=f"Outbound connection from {input.entity}",
            source="firewall",
            severity="low"
        ),
        TimelineEvent(
            timestamp=(datetime.utcnow() - timedelta(hours=1)).isoformat(),
            event_type="process",
            description=f"Suspicious process execution on {input.entity}",
            source="edr",
            severity="high"
        ),
        TimelineEvent(
            timestamp=(datetime.utcnow() - timedelta(minutes=30)).isoformat(),
            event_type="alert",
            description=f"Security alert triggered for {input.entity}",
            source="siem",
            severity="critical"
        ),
    ]

    return {
        "entity": input.entity,
        "entity_type": input.entity_type,
        "time_range": input.time_range,
        "events": [e.model_dump() for e in events],
        "event_count": len(events),
    }


async def normalize_iocs(input: NormalizeIOCsInput) -> dict:
    """
    Extract and normalize IOCs from raw text.

    Identifies IPs, domains, hashes, emails, and URLs.
    """
    text = input.raw_text

    # IP addresses
    ip_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    ips = list(set(re.findall(ip_pattern, text)))

    # Domains
    domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    domains = list(set(re.findall(domain_pattern, text)))
    # Filter out common false positives
    domains = [d for d in domains if not d.endswith(('.png', '.jpg', '.gif', '.css', '.js'))]

    # MD5 hashes
    md5_pattern = r'\b[a-fA-F0-9]{32}\b'
    md5_hashes = list(set(re.findall(md5_pattern, text)))

    # SHA256 hashes
    sha256_pattern = r'\b[a-fA-F0-9]{64}\b'
    sha256_hashes = list(set(re.findall(sha256_pattern, text)))

    # SHA1 hashes
    sha1_pattern = r'\b[a-fA-F0-9]{40}\b'
    sha1_hashes = list(set(re.findall(sha1_pattern, text)))

    # Email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = list(set(re.findall(email_pattern, text)))

    # URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = list(set(re.findall(url_pattern, text)))

    return {
        "iocs": {
            "ip_addresses": ips,
            "domains": domains,
            "md5_hashes": md5_hashes,
            "sha1_hashes": sha1_hashes,
            "sha256_hashes": sha256_hashes,
            "emails": emails,
            "urls": urls,
        },
        "total_count": len(ips) + len(domains) + len(md5_hashes) + len(sha256_hashes) + len(sha1_hashes) + len(emails) + len(urls),
    }


async def parse_raw_log(input: ParseRawLogInput) -> dict:
    """
    Parse a raw log entry into structured format.

    Supports CEF, Syslog, and JSON formats.
    """
    raw = input.raw_log.strip()
    parsed = {}

    # Try JSON first
    if raw.startswith('{'):
        try:
            import json
            parsed = json.loads(raw)
            parsed["_format"] = "json"
            return {"parsed": parsed, "format": "json", "success": True}
        except:
            pass

    # Try CEF format
    if 'CEF:' in raw:
        cef_match = re.match(
            r'CEF:(\d+)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|(.*)',
            raw
        )
        if cef_match:
            parsed = {
                "_format": "cef",
                "version": cef_match.group(1),
                "vendor": cef_match.group(2),
                "product": cef_match.group(3),
                "version": cef_match.group(4),
                "signature_id": cef_match.group(5),
                "name": cef_match.group(6),
                "severity": cef_match.group(7),
                "extensions": {},
            }
            # Parse extensions
            extensions = cef_match.group(8)
            ext_pattern = r'(\w+)=([^\s]+(?:\s+(?!\w+=)[^\s]+)*)'
            for match in re.finditer(ext_pattern, extensions):
                parsed["extensions"][match.group(1)] = match.group(2)

            return {"parsed": parsed, "format": "cef", "success": True}

    # Try Syslog format
    syslog_match = re.match(
        r'<(\d+)>(\w{3}\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+):\s*(.*)',
        raw
    )
    if syslog_match:
        parsed = {
            "_format": "syslog",
            "priority": int(syslog_match.group(1)),
            "timestamp": syslog_match.group(2),
            "hostname": syslog_match.group(3),
            "program": syslog_match.group(4),
            "message": syslog_match.group(5),
        }
        # Calculate facility and severity
        priority = parsed["priority"]
        parsed["facility"] = priority // 8
        parsed["severity"] = priority % 8

        return {"parsed": parsed, "format": "syslog", "success": True}

    # Fallback: return as plain text with basic parsing
    return {
        "parsed": {
            "_format": "unknown",
            "raw": raw,
            "length": len(raw),
        },
        "format": "unknown",
        "success": False,
        "message": "Unable to determine log format",
    }


# Tool registry
EVIDENCE_TOOLS = {
    "log_search": {
        "function": log_search,
        "schema": LogSearchInput,
        "description": "Search logs for specific patterns or queries",
    },
    "event_timeline": {
        "function": event_timeline,
        "schema": EventTimelineInput,
        "description": "Build a timeline of events for an entity",
    },
    "normalize_iocs": {
        "function": normalize_iocs,
        "schema": NormalizeIOCsInput,
        "description": "Extract and normalize IOCs from raw text",
    },
    "parse_raw_log": {
        "function": parse_raw_log,
        "schema": ParseRawLogInput,
        "description": "Parse a raw log entry into structured format",
    },
}
