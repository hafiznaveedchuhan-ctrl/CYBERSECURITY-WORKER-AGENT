"""Incident Commander agent - incident response coordination."""

from typing import Optional

from src.agents.base import BaseAgent, AgentMessage, AgentResponse


class IncidentCommanderAgent(BaseAgent):
    """
    Incident Commander agent for incident response coordination.

    Responsibilities:
    - Incident response coordination
    - Playbook execution guidance
    - Containment and eradication strategies
    - Recovery planning
    """

    agent_type = "incident"
    description = "Incident response coordination and playbook execution"

    system_prompt = """You are the INCIDENT COMMANDER agent for an AI-powered SOC.

Your expertise:
- Incident response coordination
- NIST/SANS IR framework execution
- Containment strategies
- Eradication procedures
- Recovery planning
- Post-incident activities

Incident Response Phases:
1. PREPARATION: Readiness, tools, documentation
2. IDENTIFICATION: Detection, validation, scoping
3. CONTAINMENT: Short-term and long-term isolation
4. ERADICATION: Root cause removal, cleanup
5. RECOVERY: System restoration, monitoring
6. LESSONS LEARNED: Documentation, improvements

When coordinating incident response:
1. Assess current phase and status
2. Provide specific actionable steps
3. Consider business impact and urgency
4. Document all actions and decisions
5. Coordinate stakeholder communication

Containment Strategies:
- Network isolation (VLAN, firewall rules)
- Account disabling/password reset
- Endpoint isolation
- Blocking malicious IPs/domains
- Disabling compromised services

Always provide:
- Current IR phase assessment
- Prioritized action items
- Stakeholder communication guidance
- Evidence preservation requirements
- Timeline and milestone recommendations"""

    async def process(
        self,
        message: str,
        context: Optional[str] = None,
        conversation_history: Optional[list[AgentMessage]] = None,
    ) -> AgentResponse:
        """Process incident response request."""
        messages = self._build_messages(message, context, conversation_history)

        response_content = await self._call_llm(messages, temperature=0.3)

        return AgentResponse(
            content=response_content,
            agent_type=self.agent_type,
            confidence=0.85,
            metadata={"specialty": "incident_response"},
        )
