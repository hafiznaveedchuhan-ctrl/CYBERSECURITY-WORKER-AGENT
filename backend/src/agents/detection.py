"""Detection Engineer agent - Sigma/YARA rule creation."""

from typing import Optional

from src.agents.base import BaseAgent, AgentMessage, AgentResponse


class DetectionEngineerAgent(BaseAgent):
    """
    Detection Engineer agent for creating detection rules.

    Responsibilities:
    - Sigma rule creation and optimization
    - YARA rule development
    - Detection gap analysis
    - Rule testing and validation guidance
    """

    agent_type = "detection"
    description = "Detection engineering, Sigma/YARA rule creation"

    system_prompt = """You are the DETECTION ENGINEER agent for an AI-powered SOC.

Your expertise:
- Sigma rule creation and syntax
- YARA rule development
- Detection logic design
- Log source mapping
- False positive reduction
- Detection coverage analysis

When creating detection rules:
1. Understand the threat behavior to detect
2. Identify appropriate log sources
3. Design detection logic with precision
4. Consider false positive scenarios
5. Provide testing guidance

Sigma Rule Structure:
```yaml
title: Rule Title
id: UUID
status: experimental|test|stable
description: What this rule detects
author: Author Name
date: YYYY/MM/DD
references:
  - https://reference.url
logsource:
  product: windows|linux|etc
  service: service_name
  category: category_name
detection:
  selection:
    FieldName: Value
  condition: selection
falsepositives:
  - Known false positive scenarios
level: critical|high|medium|low|informational
tags:
  - attack.tXXXX
```

Always provide:
- Complete, valid rule syntax
- Explanation of detection logic
- Known false positive considerations
- Testing recommendations
- MITRE ATT&CK mapping"""

    async def process(
        self,
        message: str,
        context: Optional[str] = None,
        conversation_history: Optional[list[AgentMessage]] = None,
    ) -> AgentResponse:
        """Process detection engineering request."""
        messages = self._build_messages(message, context, conversation_history)

        response_content = await self._call_llm(messages, temperature=0.3)

        return AgentResponse(
            content=response_content,
            agent_type=self.agent_type,
            confidence=0.85,
            metadata={"specialty": "detection_engineering"},
        )
