"""Case management MCP tools."""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class CreateCaseInput(BaseModel):
    """Input for creating a new case."""
    title: str = Field(..., description="Case title")
    description: str = Field(..., description="Case description")
    severity: str = Field(default="medium", description="Severity (critical, high, medium, low)")
    alert_ids: list[str] = Field(default=[], description="Related alert IDs")


class AddCaseNoteInput(BaseModel):
    """Input for adding a note to a case."""
    case_id: str = Field(..., description="Case ID")
    note: str = Field(..., description="Note content")
    note_type: str = Field(default="investigation", description="Note type (investigation, action, evidence)")


class GenerateReportInput(BaseModel):
    """Input for generating an incident report."""
    case_id: str = Field(..., description="Case ID to generate report for")
    include_timeline: bool = Field(default=True)
    include_iocs: bool = Field(default=True)
    include_recommendations: bool = Field(default=True)
    format: str = Field(default="markdown", description="Report format (markdown, html, pdf)")


class UpdateCaseStatusInput(BaseModel):
    """Input for updating case status."""
    case_id: str = Field(..., description="Case ID")
    status: str = Field(..., description="New status (open, investigating, contained, resolved, closed)")
    resolution: Optional[str] = Field(default=None, description="Resolution notes if closing")


# In-memory case storage (use database in production)
cases: dict[str, dict] = {}


async def create_case(input: CreateCaseInput) -> dict:
    """
    Create a new incident case.

    Returns the created case with assigned ID.
    """
    case_id = f"CASE-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid4())[:8].upper()}"

    case = {
        "id": case_id,
        "title": input.title,
        "description": input.description,
        "severity": input.severity,
        "status": "open",
        "alert_ids": input.alert_ids,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "assigned_to": None,
        "notes": [],
        "timeline": [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "event": "Case created",
                "actor": "system",
            }
        ],
        "iocs": [],
        "affected_assets": [],
    }

    cases[case_id] = case

    return {
        "success": True,
        "case": case,
        "message": f"Case {case_id} created successfully",
    }


async def add_case_note(input: AddCaseNoteInput) -> dict:
    """
    Add a note to an existing case.

    Notes are timestamped and categorized.
    """
    case = cases.get(input.case_id)
    if not case:
        return {"success": False, "error": f"Case {input.case_id} not found"}

    note = {
        "id": str(uuid4())[:8],
        "content": input.note,
        "type": input.note_type,
        "created_at": datetime.utcnow().isoformat(),
        "author": "analyst",  # Would be from auth context
    }

    case["notes"].append(note)
    case["updated_at"] = datetime.utcnow().isoformat()

    # Add to timeline
    case["timeline"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "event": f"Note added: {input.note_type}",
        "actor": "analyst",
    })

    return {
        "success": True,
        "note": note,
        "case_id": input.case_id,
    }


async def generate_incident_report(input: GenerateReportInput) -> dict:
    """
    Generate a comprehensive incident report.

    Compiles case data into a structured report format.
    """
    case = cases.get(input.case_id)
    if not case:
        return {"success": False, "error": f"Case {input.case_id} not found"}

    # Build report sections
    sections = []

    # Executive Summary
    sections.append({
        "title": "Executive Summary",
        "content": f"""
## Executive Summary

**Case ID:** {case['id']}
**Severity:** {case['severity'].upper()}
**Status:** {case['status'].upper()}
**Created:** {case['created_at']}

### Overview
{case['description']}

### Impact Assessment
- Affected Systems: {len(case.get('affected_assets', []))} identified
- Related Alerts: {len(case.get('alert_ids', []))}
- IOCs Identified: {len(case.get('iocs', []))}
""",
    })

    # Timeline
    if input.include_timeline and case.get("timeline"):
        timeline_md = "\n".join([
            f"- **{e['timestamp']}** - {e['event']} (by {e['actor']})"
            for e in case["timeline"]
        ])
        sections.append({
            "title": "Incident Timeline",
            "content": f"## Incident Timeline\n\n{timeline_md}",
        })

    # IOCs
    if input.include_iocs and case.get("iocs"):
        iocs_md = "\n".join([
            f"- `{ioc['value']}` ({ioc['type']}) - {ioc.get('description', 'No description')}"
            for ioc in case["iocs"]
        ])
        sections.append({
            "title": "Indicators of Compromise",
            "content": f"## Indicators of Compromise\n\n{iocs_md}",
        })
    elif input.include_iocs:
        sections.append({
            "title": "Indicators of Compromise",
            "content": "## Indicators of Compromise\n\nNo IOCs have been documented for this case.",
        })

    # Investigation Notes
    if case.get("notes"):
        notes_md = "\n\n".join([
            f"### {n['type'].title()} Note ({n['created_at']})\n{n['content']}"
            for n in case["notes"]
        ])
        sections.append({
            "title": "Investigation Notes",
            "content": f"## Investigation Notes\n\n{notes_md}",
        })

    # Recommendations
    if input.include_recommendations:
        sections.append({
            "title": "Recommendations",
            "content": """## Recommendations

### Immediate Actions
1. Ensure all affected systems are isolated or monitored
2. Reset credentials for any compromised accounts
3. Update detection rules based on identified IOCs

### Short-term Improvements
1. Review access controls for affected systems
2. Conduct user awareness training if phishing was involved
3. Patch any identified vulnerabilities

### Long-term Measures
1. Implement additional monitoring for similar attack patterns
2. Review and update incident response procedures
3. Consider additional security controls for high-value assets
""",
        })

    # Compile full report
    full_report = "\n\n---\n\n".join([s["content"] for s in sections])

    # Add header
    report_header = f"""# Incident Report: {case['title']}

**Report Generated:** {datetime.utcnow().isoformat()}
**Case Reference:** {case['id']}

---

"""

    full_report = report_header + full_report

    return {
        "success": True,
        "report": {
            "case_id": input.case_id,
            "format": input.format,
            "content": full_report,
            "sections": [s["title"] for s in sections],
            "generated_at": datetime.utcnow().isoformat(),
        },
    }


async def update_case_status(input: UpdateCaseStatusInput) -> dict:
    """
    Update the status of a case.

    Tracks status changes in the timeline.
    """
    case = cases.get(input.case_id)
    if not case:
        return {"success": False, "error": f"Case {input.case_id} not found"}

    old_status = case["status"]
    case["status"] = input.status
    case["updated_at"] = datetime.utcnow().isoformat()

    if input.resolution and input.status in ["resolved", "closed"]:
        case["resolution"] = input.resolution

    # Add to timeline
    event_msg = f"Status changed from {old_status} to {input.status}"
    if input.resolution:
        event_msg += f" - Resolution: {input.resolution}"

    case["timeline"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_msg,
        "actor": "analyst",
    })

    return {
        "success": True,
        "case_id": input.case_id,
        "old_status": old_status,
        "new_status": input.status,
    }


# Tool registry
CASE_MANAGEMENT_TOOLS = {
    "create_case": {
        "function": create_case,
        "schema": CreateCaseInput,
        "description": "Create a new incident case",
    },
    "add_case_note": {
        "function": add_case_note,
        "schema": AddCaseNoteInput,
        "description": "Add a note to an existing case",
    },
    "generate_incident_report": {
        "function": generate_incident_report,
        "schema": GenerateReportInput,
        "description": "Generate a comprehensive incident report",
    },
    "update_case_status": {
        "function": update_case_status,
        "schema": UpdateCaseStatusInput,
        "description": "Update the status of a case",
    },
}
