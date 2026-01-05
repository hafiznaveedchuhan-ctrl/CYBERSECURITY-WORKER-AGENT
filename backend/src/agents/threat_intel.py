"""Threat Intelligence agent - threat actor and TTP analysis."""

from typing import Optional

from src.agents.base import BaseAgent, AgentMessage, AgentResponse


class ThreatIntelAgent(BaseAgent):
    """
    Threat Intelligence agent for threat actor and TTP analysis.

    Responsibilities:
    - Threat actor profiling
    - TTP (Tactics, Techniques, Procedures) mapping
    - Campaign analysis
    - Strategic threat assessment
    """

    agent_type = "threatintel"
    description = "Threat intelligence, TTPs, and threat actor analysis"

    system_prompt = """You are the THREAT INTELLIGENCE agent for an AI-powered SOC.

Your expertise:
- Threat actor profiling and attribution
- MITRE ATT&CK framework mapping
- Campaign and operation analysis
- Strategic and tactical threat assessment
- Indicator contextualization

When analyzing threats:
1. Map observed activity to MITRE ATT&CK techniques
2. Identify potential threat actor groups based on TTPs
3. Assess the strategic intent and capability
4. Provide actionable intelligence

MITRE ATT&CK Tactics:
- Reconnaissance, Resource Development
- Initial Access, Execution, Persistence
- Privilege Escalation, Defense Evasion
- Credential Access, Discovery
- Lateral Movement, Collection
- Command and Control, Exfiltration
- Impact

Always provide:
- ATT&CK technique mappings (TXXXx.xxx)
- Threat actor assessment (if applicable)
- Confidence level in attribution
- Recommended defensive measures
- Intelligence gaps and collection priorities"""

    async def process(
        self,
        message: str,
        context: Optional[str] = None,
        conversation_history: Optional[list[AgentMessage]] = None,
    ) -> AgentResponse:
        """Process threat intelligence request."""
        messages = self._build_messages(message, context, conversation_history)

        response_content = await self._call_llm(messages, temperature=0.4)

        return AgentResponse(
            content=response_content,
            agent_type=self.agent_type,
            confidence=0.8,
            metadata={"specialty": "threat_intelligence"},
        )
