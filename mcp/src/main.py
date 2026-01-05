"""AI SOC MCP Server - Main Entry Point."""

import asyncio
import re
from datetime import datetime
from uuid import uuid4

from mcp.server import Server
from mcp.types import Tool, TextContent
import structlog

from src.tools import ip_analyzer, hash_analyzer, sigma_generator, domain_analyzer

logger = structlog.get_logger()

# Create MCP server
server = Server("ai-soc-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available security tools."""
    return [
        Tool(
            name="analyze_ip",
            description="Analyze an IP address for threat intelligence including reputation, geolocation, and abuse reports",
            inputSchema={
                "type": "object",
                "properties": {
                    "ip": {
                        "type": "string",
                        "description": "IP address to analyze (IPv4 or IPv6)",
                    }
                },
                "required": ["ip"],
            },
        ),
        Tool(
            name="analyze_hash",
            description="Analyze a file hash for malware indicators using multiple threat intel sources",
            inputSchema={
                "type": "object",
                "properties": {
                    "hash": {
                        "type": "string",
                        "description": "File hash (MD5, SHA1, or SHA256)",
                    },
                    "hash_type": {
                        "type": "string",
                        "enum": ["md5", "sha1", "sha256", "auto"],
                        "description": "Hash type (auto-detected if not specified)",
                        "default": "auto",
                    },
                },
                "required": ["hash"],
            },
        ),
        Tool(
            name="analyze_domain",
            description="Analyze a domain for reputation, WHOIS data, and threat intelligence",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Domain name to analyze",
                    }
                },
                "required": ["domain"],
            },
        ),
        Tool(
            name="generate_sigma_rule",
            description="Generate a Sigma detection rule based on threat description",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title for the detection rule",
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of what to detect",
                    },
                    "log_source": {
                        "type": "string",
                        "enum": ["windows", "linux", "network", "cloud", "web"],
                        "description": "Log source category",
                        "default": "windows",
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"],
                        "description": "Rule severity level",
                        "default": "medium",
                    },
                    "mitre_techniques": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "MITRE ATT&CK technique IDs (e.g., T1059.001)",
                    },
                },
                "required": ["title", "description"],
            },
        ),
        Tool(
            name="generate_yara_rule",
            description="Generate a YARA rule for file/malware detection",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Rule name (no spaces, use underscores)",
                    },
                    "description": {
                        "type": "string",
                        "description": "What the rule should detect",
                    },
                    "strings": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Strings or patterns to match",
                    },
                    "condition": {
                        "type": "string",
                        "description": "Match condition (e.g., 'any of them', 'all of them')",
                        "default": "any of them",
                    },
                },
                "required": ["name", "description"],
            },
        ),
        Tool(
            name="enrich_ioc",
            description="Enrich an Indicator of Compromise with context from multiple sources",
            inputSchema={
                "type": "object",
                "properties": {
                    "ioc": {
                        "type": "string",
                        "description": "The IOC value (IP, domain, hash, URL, email)",
                    },
                    "ioc_type": {
                        "type": "string",
                        "enum": ["ip", "domain", "hash", "url", "email", "auto"],
                        "description": "Type of IOC (auto-detected if not specified)",
                        "default": "auto",
                    },
                },
                "required": ["ioc"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a security tool."""
    request_id = str(uuid4())[:8]
    logger.info("Tool called", tool=name, request_id=request_id)

    try:
        if name == "analyze_ip":
            result = await ip_analyzer.analyze(arguments.get("ip", ""))

        elif name == "analyze_hash":
            result = await hash_analyzer.analyze(
                arguments.get("hash", ""),
                arguments.get("hash_type", "auto"),
            )

        elif name == "analyze_domain":
            result = await domain_analyzer.analyze(arguments.get("domain", ""))

        elif name == "generate_sigma_rule":
            result = sigma_generator.generate(
                title=arguments.get("title", ""),
                description=arguments.get("description", ""),
                log_source=arguments.get("log_source", "windows"),
                severity=arguments.get("severity", "medium"),
                mitre_techniques=arguments.get("mitre_techniques", []),
            )

        elif name == "generate_yara_rule":
            result = generate_yara_rule(
                name=arguments.get("name", ""),
                description=arguments.get("description", ""),
                strings=arguments.get("strings", []),
                condition=arguments.get("condition", "any of them"),
            )

        elif name == "enrich_ioc":
            result = await enrich_ioc(
                arguments.get("ioc", ""),
                arguments.get("ioc_type", "auto"),
            )

        else:
            result = f"Unknown tool: {name}"

        logger.info("Tool completed", tool=name, request_id=request_id)
        return [TextContent(type="text", text=result)]

    except Exception as e:
        logger.error("Tool failed", tool=name, error=str(e), request_id=request_id)
        return [TextContent(type="text", text=f"Error executing {name}: {str(e)}")]


def generate_yara_rule(
    name: str,
    description: str,
    strings: list[str],
    condition: str,
) -> str:
    """Generate a YARA rule."""
    rule_id = str(uuid4())[:8]

    # Generate string definitions
    string_defs = []
    for i, s in enumerate(strings):
        if s.startswith("/") and s.endswith("/"):
            # Regex pattern
            string_defs.append(f'        $s{i} = {s}')
        elif s.startswith("{") and s.endswith("}"):
            # Hex pattern
            string_defs.append(f'        $s{i} = {s}')
        else:
            # Plain string
            string_defs.append(f'        $s{i} = "{s}" nocase')

    strings_section = "\n".join(string_defs) if string_defs else '        $placeholder = "REPLACE_ME"'

    return f'''rule {name} {{
    meta:
        description = "{description}"
        author = "AI SOC Platform"
        date = "{datetime.now().strftime("%Y-%m-%d")}"
        id = "{rule_id}"

    strings:
{strings_section}

    condition:
        {condition}
}}'''


async def enrich_ioc(ioc: str, ioc_type: str) -> str:
    """Enrich an IOC with threat intelligence."""
    # Auto-detect IOC type if needed
    if ioc_type == "auto":
        ioc_type = detect_ioc_type(ioc)

    result_lines = [
        f"IOC Enrichment Report",
        f"=" * 50,
        f"IOC: {ioc}",
        f"Type: {ioc_type}",
        f"Timestamp: {datetime.now().isoformat()}",
        "",
    ]

    if ioc_type == "ip":
        result_lines.extend([
            "IP Analysis:",
            "  - Geolocation: [Requires API integration]",
            "  - ASN: [Requires API integration]",
            "  - Reputation: [Requires VirusTotal/AbuseIPDB]",
            "  - Historical Data: [Requires threat intel feed]",
        ])
    elif ioc_type == "domain":
        result_lines.extend([
            "Domain Analysis:",
            "  - Registration: [Requires WHOIS API]",
            "  - DNS Records: [Requires DNS lookup]",
            "  - Reputation: [Requires VirusTotal/URLhaus]",
            "  - SSL Certificate: [Requires certificate check]",
        ])
    elif ioc_type == "hash":
        result_lines.extend([
            "Hash Analysis:",
            "  - File Type: [Requires VirusTotal]",
            "  - AV Detections: [Requires VirusTotal]",
            "  - First Seen: [Requires threat intel]",
            "  - Related Samples: [Requires MalwareBazaar]",
        ])
    else:
        result_lines.append(f"  Analysis for {ioc_type} type not yet implemented")

    result_lines.extend([
        "",
        "Note: Full enrichment requires API key configuration.",
        "Configure VIRUSTOTAL_API_KEY, ABUSEIPDB_API_KEY in .env",
    ])

    return "\n".join(result_lines)


def detect_ioc_type(ioc: str) -> str:
    """Auto-detect the type of IOC."""
    # IP address patterns
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'

    if re.match(ipv4_pattern, ioc) or re.match(ipv6_pattern, ioc):
        return "ip"

    # Hash patterns
    if re.match(r'^[a-fA-F0-9]{32}$', ioc):
        return "hash"  # MD5
    if re.match(r'^[a-fA-F0-9]{40}$', ioc):
        return "hash"  # SHA1
    if re.match(r'^[a-fA-F0-9]{64}$', ioc):
        return "hash"  # SHA256

    # URL pattern
    if ioc.startswith(("http://", "https://", "ftp://")):
        return "url"

    # Email pattern
    if "@" in ioc and "." in ioc.split("@")[-1]:
        return "email"

    # Domain (default for non-matching patterns)
    if "." in ioc and not "/" in ioc:
        return "domain"

    return "unknown"


async def main() -> None:
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server

    logger.info("Starting AI SOC MCP Server")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
