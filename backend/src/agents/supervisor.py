"""Supervisor agent - orchestrates sub-agents."""

from typing import Optional

import structlog

from src.agents.base import BaseAgent, AgentMessage, AgentResponse

logger = structlog.get_logger()


class SupervisorAgent(BaseAgent):
    """
    Supervisor agent that routes queries to appropriate sub-agents.

    Responsibilities:
    - Analyze user queries to determine intent
    - Route to appropriate domain expert sub-agent
    - Aggregate responses when multiple agents needed
    - Maintain conversation coherence
    """

    agent_type = "supervisor"
    description = "Orchestrates sub-agents and routes queries"

    system_prompt = """You are the Supervisor agent for an AI-powered Security Operations Center (SOC).

Your role is to:
1. Analyze incoming security-related queries
2. Determine which domain expert should handle the query
3. Coordinate multi-agent responses when needed
4. Ensure responses are accurate and helpful

Available domain experts:
- TRIAGE: Initial alert assessment, severity classification, false positive detection
- ENRICHMENT: Data enrichment, IOC lookup, context gathering
- THREATINTEL: Threat intelligence analysis, TTPs, threat actors
- DETECTION: Sigma/YARA rule creation, detection engineering
- INCIDENT: Incident response coordination, playbook execution
- REPORT: Report generation, executive summaries, documentation

When responding:
- Be concise and professional
- Cite sources from the SOC textbook when available
- Recommend appropriate next steps
- Indicate which sub-agent would be best for follow-up questions

If the query is general or educational, provide a direct response using the textbook context."""

    async def process(
        self,
        message: str,
        context: Optional[str] = None,
        conversation_history: Optional[list[AgentMessage]] = None,
    ) -> AgentResponse:
        """Process message and route to appropriate sub-agent if needed."""
        messages = self._build_messages(message, context, conversation_history)

        # Add routing instruction
        messages.append({
            "role": "system",
            "content": (
                "First, determine if this query should be routed to a specific sub-agent. "
                "If yes, indicate which one. If no, provide a direct response."
            ),
        })

        response_content = await self._call_llm(messages, temperature=0.5)

        # Analyze response for routing
        recommended_agent = self._detect_routing(response_content, message)

        return AgentResponse(
            content=response_content,
            agent_type=self.agent_type,
            confidence=0.9,
            metadata={
                "recommended_agent": recommended_agent,
                "routed": recommended_agent is not None,
            },
        )

    def _detect_routing(self, response: str, query: str) -> Optional[str]:
        """Detect if query should be routed to a sub-agent."""
        query_lower = query.lower()
        response_lower = response.lower()

        routing_keywords = {
            "triage": ["triage", "alert", "severity", "priority", "false positive"],
            "enrichment": ["enrich", "ioc", "indicator", "lookup", "context"],
            "threatintel": ["threat intel", "threat actor", "ttp", "campaign", "apt"],
            "detection": ["sigma", "yara", "detection rule", "detect"],
            "incident": ["incident", "response", "playbook", "contain", "eradicate"],
            "report": ["report", "summary", "document", "executive"],
        }

        for agent, keywords in routing_keywords.items():
            if any(kw in query_lower or kw in response_lower for kw in keywords):
                return agent

        return None
