"""Safe actions MCP tools with approval gates."""

from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class RequestActionInput(BaseModel):
    """Input for requesting a disruptive action."""
    action_type: str = Field(..., description="Type of action (disable_user, isolate_host, block_ip, kill_process)")
    target: str = Field(..., description="Target of the action (username, hostname, IP, process ID)")
    reason: str = Field(..., description="Justification for the action")
    case_id: Optional[str] = Field(default=None, description="Related case ID")


class ApproveActionInput(BaseModel):
    """Input for approving a pending action."""
    approval_id: str = Field(..., description="Approval request ID")
    approved: bool = Field(..., description="Whether to approve or reject")
    approver_notes: Optional[str] = Field(default=None, description="Notes from the approver")


class ExecuteActionInput(BaseModel):
    """Input for executing an approved action."""
    approval_id: str = Field(..., description="Approval request ID")


# Action risk levels
ACTION_RISK_LEVELS = {
    "disable_user": "high",
    "isolate_host": "critical",
    "block_ip": "medium",
    "kill_process": "high",
    "reset_password": "medium",
    "revoke_session": "low",
}

# In-memory approval storage
pending_approvals: dict[str, dict] = {}


async def request_action(input: RequestActionInput) -> dict:
    """
    Request approval for a disruptive action.

    Creates a pending approval that requires human review.
    """
    approval_id = f"APR-{str(uuid4())[:8].upper()}"
    risk_level = ACTION_RISK_LEVELS.get(input.action_type, "medium")

    approval = {
        "id": approval_id,
        "action_type": input.action_type,
        "target": input.target,
        "reason": input.reason,
        "case_id": input.case_id,
        "risk_level": risk_level,
        "status": "pending",
        "requested_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        "requested_by": "triage-agent",  # Would come from context
        "approved_by": None,
        "approver_notes": None,
        "executed": False,
    }

    pending_approvals[approval_id] = approval

    return {
        "success": True,
        "approval_id": approval_id,
        "status": "pending",
        "risk_level": risk_level,
        "message": f"Action requires approval. Approval ID: {approval_id}",
        "expires_at": approval["expires_at"],
    }


async def approve_action(input: ApproveActionInput) -> dict:
    """
    Approve or reject a pending action.

    Only authorized users can approve actions.
    """
    approval = pending_approvals.get(input.approval_id)
    if not approval:
        return {
            "success": False,
            "error": f"Approval request {input.approval_id} not found",
        }

    if approval["status"] != "pending":
        return {
            "success": False,
            "error": f"Approval request is already {approval['status']}",
        }

    # Check expiration
    expires_at = datetime.fromisoformat(approval["expires_at"])
    if datetime.utcnow() > expires_at:
        approval["status"] = "expired"
        return {
            "success": False,
            "error": "Approval request has expired",
        }

    # Update approval status
    approval["status"] = "approved" if input.approved else "rejected"
    approval["approved_by"] = "security-analyst"  # Would come from auth
    approval["approver_notes"] = input.approver_notes
    approval["resolved_at"] = datetime.utcnow().isoformat()

    return {
        "success": True,
        "approval_id": input.approval_id,
        "status": approval["status"],
        "action_type": approval["action_type"],
        "target": approval["target"],
        "message": f"Action {approval['status']}",
    }


async def execute_action(input: ExecuteActionInput) -> dict:
    """
    Execute an approved action.

    Only executes if the action has been approved.
    """
    approval = pending_approvals.get(input.approval_id)
    if not approval:
        return {
            "success": False,
            "error": f"Approval request {input.approval_id} not found",
        }

    if approval["status"] != "approved":
        return {
            "success": False,
            "error": f"Cannot execute - action status is {approval['status']}",
        }

    if approval["executed"]:
        return {
            "success": False,
            "error": "Action has already been executed",
        }

    # Simulate action execution
    action_results = {
        "disable_user": f"User {approval['target']} has been disabled",
        "isolate_host": f"Host {approval['target']} has been isolated from network",
        "block_ip": f"IP {approval['target']} has been blocked at firewall",
        "kill_process": f"Process {approval['target']} has been terminated",
        "reset_password": f"Password reset initiated for {approval['target']}",
        "revoke_session": f"All sessions revoked for {approval['target']}",
    }

    result_message = action_results.get(
        approval["action_type"],
        f"Action {approval['action_type']} executed on {approval['target']}"
    )

    approval["executed"] = True
    approval["executed_at"] = datetime.utcnow().isoformat()

    return {
        "success": True,
        "approval_id": input.approval_id,
        "action_type": approval["action_type"],
        "target": approval["target"],
        "result": result_message,
        "executed_at": approval["executed_at"],
    }


async def list_pending_approvals() -> dict:
    """
    List all pending approval requests.
    """
    pending = [
        {
            "id": a["id"],
            "action_type": a["action_type"],
            "target": a["target"],
            "reason": a["reason"],
            "risk_level": a["risk_level"],
            "requested_at": a["requested_at"],
            "expires_at": a["expires_at"],
        }
        for a in pending_approvals.values()
        if a["status"] == "pending"
    ]

    return {
        "pending_count": len(pending),
        "approvals": pending,
    }


# Tool registry
SAFE_ACTIONS_TOOLS = {
    "request_action": {
        "function": request_action,
        "schema": RequestActionInput,
        "description": "Request approval for a disruptive action",
    },
    "approve_action": {
        "function": approve_action,
        "schema": ApproveActionInput,
        "description": "Approve or reject a pending action",
    },
    "execute_action": {
        "function": execute_action,
        "schema": ExecuteActionInput,
        "description": "Execute an approved action",
    },
}
