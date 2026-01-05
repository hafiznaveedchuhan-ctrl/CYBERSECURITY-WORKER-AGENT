"""Enrichment agent - data enrichment and IOC analysis."""

from typing import Optional

from src.agents.base import BaseAgent, AgentMessage, AgentResponse


class EnrichmentAgent(BaseAgent):
    """
    Enrichment agent for data enrichment and context gathering.

    Responsibilities:
    - IOC (Indicator of Compromise) enrichment
    - IP/Domain/Hash reputation lookup
    - User and asset context gathering
    - Historical correlation
    """

    agent_type = "enrichment"
    description = "Data enrichment, IOC analysis, and context gathering"

    system_prompt = """You are the ENRICHMENT agent for an AI-powered SOC.

Your expertise:
- IOC (Indicator of Compromise) analysis
- IP address reputation and geolocation
- Domain and URL analysis
- File hash reputation
- User behavior context
- Asset and network context

When enriching data:
1. Identify the type of indicator (IP, domain, hash, email, etc.)
2. Describe what enrichment sources would be valuable
3. Explain what the enriched data means
4. Highlight any red flags or concerns

Enrichment sources to consider:
- VirusTotal for file/URL/domain reputation
- AbuseIPDB for IP reputation
- WHOIS for domain registration
- Passive DNS for domain history
- GeoIP for location context
- Internal asset management for asset context
- SIEM for historical activity

Always provide:
- Summary of enrichment findings
- Risk indicators identified
- Contextual relevance to the investigation
- Recommendations for further analysis"""

    async def process(
        self,
        message: str,
        context: Optional[str] = None,
        conversation_history: Optional[list[AgentMessage]] = None,
    ) -> AgentResponse:
        """Process enrichment request."""
        messages = self._build_messages(message, context, conversation_history)

        response_content = await self._call_llm(messages, temperature=0.3)

        return AgentResponse(
            content=response_content,
            agent_type=self.agent_type,
            confidence=0.85,
            metadata={"specialty": "data_enrichment"},
        )
