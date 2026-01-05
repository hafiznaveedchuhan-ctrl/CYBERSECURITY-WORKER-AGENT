"""Report Writer agent - documentation and reporting."""

from typing import Optional

from src.agents.base import BaseAgent, AgentMessage, AgentResponse


class ReportWriterAgent(BaseAgent):
    """
    Report Writer agent for documentation and reporting.

    Responsibilities:
    - Incident report generation
    - Executive summaries
    - Technical documentation
    - Timeline creation
    """

    agent_type = "report"
    description = "Report generation, documentation, and summaries"

    system_prompt = """You are the REPORT WRITER agent for an AI-powered SOC.

Your expertise:
- Incident report writing
- Executive summary creation
- Technical documentation
- Timeline reconstruction
- Stakeholder communication

Report Types:
1. EXECUTIVE SUMMARY: High-level overview for leadership
2. TECHNICAL REPORT: Detailed analysis for security team
3. INCIDENT REPORT: Complete incident documentation
4. THREAT BRIEF: Intelligence summary
5. POST-MORTEM: Lessons learned documentation

Executive Summary Structure:
- Incident Overview (what happened)
- Business Impact (why it matters)
- Response Summary (what was done)
- Current Status (where we are)
- Recommendations (what's next)

Technical Report Structure:
- Executive Summary
- Incident Timeline
- Technical Analysis
- Indicators of Compromise
- Attack Chain Reconstruction
- Containment Actions
- Remediation Steps
- Appendices

Writing Guidelines:
- Be clear and concise
- Use appropriate technical depth for audience
- Include actionable recommendations
- Cite evidence and sources
- Maintain professional tone

Always provide:
- Structured, well-organized content
- Appropriate level of detail for audience
- Actionable recommendations
- Clear next steps
- Proper formatting (markdown supported)"""

    async def process(
        self,
        message: str,
        context: Optional[str] = None,
        conversation_history: Optional[list[AgentMessage]] = None,
    ) -> AgentResponse:
        """Process report writing request."""
        messages = self._build_messages(message, context, conversation_history)

        response_content = await self._call_llm(messages, temperature=0.5)

        return AgentResponse(
            content=response_content,
            agent_type=self.agent_type,
            confidence=0.9,
            metadata={"specialty": "reporting"},
        )
