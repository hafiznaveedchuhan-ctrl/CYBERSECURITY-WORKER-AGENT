"""File Hash Analysis Tool."""

import re
from datetime import datetime


async def analyze(file_hash: str, hash_type: str = "auto") -> str:
    """Analyze a file hash for malware indicators."""
    # Clean the hash
    file_hash = file_hash.strip().lower()

    # Detect hash type if auto
    if hash_type == "auto":
        hash_type = detect_hash_type(file_hash)

    if hash_type == "unknown":
        return f"Error: Invalid hash format: {file_hash}"

    result_lines = [
        f"Hash Analysis Report",
        f"=" * 50,
        f"Hash: {file_hash}",
        f"Type: {hash_type.upper()}",
        f"Analysis Time: {datetime.now().isoformat()}",
        "",
        "Hash Validation:",
        f"  - Format: Valid {hash_type.upper()}",
        f"  - Length: {len(file_hash)} characters",
        "",
        "Threat Intelligence (requires API keys):",
        "  - VirusTotal: [Configure VIRUSTOTAL_API_KEY]",
        "  - MalwareBazaar: [Configure MALWAREBAZAAR_API_KEY]",
        "  - Hybrid Analysis: [Configure HYBRID_ANALYSIS_API_KEY]",
        "",
        "Analysis Results:",
        "  - Detection Ratio: Unknown (API required)",
        "  - First Seen: Unknown",
        "  - Last Seen: Unknown",
        "  - File Type: Unknown",
        "  - File Size: Unknown",
        "",
    ]

    # Add hash-specific info
    if hash_type == "md5":
        result_lines.extend([
            "Note: MD5 hashes are prone to collisions.",
            "Consider using SHA256 for more reliable identification.",
            "",
        ])

    result_lines.extend([
        "Recommendations:",
        "  - Search hash in VirusTotal manually if API not configured",
        "  - Check organization's EDR for file presence",
        "  - If malicious, isolate affected systems",
        "",
        "Manual Lookup URLs:",
        f"  - VirusTotal: https://www.virustotal.com/gui/search/{file_hash}",
        f"  - MalwareBazaar: https://bazaar.abuse.ch/browse.php?search={hash_type}:{file_hash}",
    ])

    return "\n".join(result_lines)


def detect_hash_type(file_hash: str) -> str:
    """Detect the type of hash based on length and format."""
    file_hash = file_hash.strip().lower()

    # Check if valid hex
    if not re.match(r'^[a-f0-9]+$', file_hash):
        return "unknown"

    length = len(file_hash)

    if length == 32:
        return "md5"
    elif length == 40:
        return "sha1"
    elif length == 64:
        return "sha256"
    elif length == 128:
        return "sha512"
    else:
        return "unknown"
