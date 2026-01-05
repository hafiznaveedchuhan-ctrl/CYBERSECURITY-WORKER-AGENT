"""Triage agent - alert assessment and prioritization."""

from typing import Optional

from src.agents.base import BaseAgent, AgentMessage, AgentResponse


class TriageAgent(BaseAgent):
    """
    Triage agent for initial alert assessment.

    Responsibilities:
    - Assess alert severity (Critical, High, Medium, Low, Info)
    - Identify false positives
    - Recommend priority and escalation
    - Initial context gathering
    """

    agent_type = "triage"
    description = "Alert triage, severity assessment, and prioritization"

    system_prompt = """You are the TRIAGE agent for an AI-powered SOC.

Your expertise:
- Alert severity classification (Critical, High, Medium, Low, Informational)
- False positive identification
- Initial alert contextualization
- Escalation recommendations

When triaging alerts:
1. Assess the severity based on potential impact and confidence
2. Check for common false positive patterns
3. Identify what additional context is needed
4. Recommend appropriate response priority

Severity Guidelines:
- CRITICAL: Active compromise, data exfiltration, ransomware execution
- HIGH: Successful exploitation, lateral movement, privilege escalation
- MEDIUM: Suspicious activity, policy violation, potential reconnaissance
- LOW: Anomalous but likely benign, minor policy violations
- INFO: Normal activity flagged for awareness

Always provide:
- Severity assessment with reasoning
- Confidence level (High/Medium/Low)
- Recommended next steps
- What additional enrichment would help"""

    async def process(
        self,
        message: str,
        context: Optional[str] = None,
        conversation_history: Optional[list[AgentMessage]] = None,
    ) -> AgentResponse:
        """Process triage request."""
        messages = self._build_messages(message, context, conversation_history)

        response_content = await self._call_llm(messages, temperature=0.3)

        return AgentResponse(
            content=response_content,
            agent_type=self.agent_type,
            confidence=0.85,
            metadata={"specialty": "alert_triage"},
        )
