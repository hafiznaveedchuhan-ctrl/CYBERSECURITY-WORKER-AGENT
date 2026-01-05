---
sidebar_position: 2
---

# Agent Architecture

This section covers the technical architecture of AI agents, including design patterns and implementation considerations.

## Core Architecture Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         AI AGENT                                │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   INPUT     │  │   BRAIN     │  │        OUTPUT           │ │
│  │  PROCESSOR  │─►│    (LLM)    │─►│      GENERATOR          │ │
│  └─────────────┘  └──────┬──────┘  └─────────────────────────┘ │
│                          │                                      │
│         ┌────────────────┼────────────────┐                    │
│         │                │                │                    │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐            │
│  │   MEMORY    │  │    TOOLS    │  │  POLICIES   │            │
│  │   SYSTEM    │  │   MANAGER   │  │   ENGINE    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## The Language Model Core

### Model Selection Criteria

| Factor | Consideration |
|--------|---------------|
| Capability | Reasoning, coding, domain knowledge |
| Latency | Response time requirements |
| Cost | Token pricing, volume discounts |
| Context | Maximum context window size |
| Safety | Built-in guardrails |

### Prompt Engineering for Agents

```markdown
## System Prompt Structure

### Role Definition
You are a security analyst agent specializing in alert triage.

### Capabilities
You can:
- Analyze security alerts
- Query threat intelligence
- Search logs and events
- Classify severity

### Constraints
You must:
- Never execute destructive actions
- Always cite your sources
- Escalate high-severity findings
- Log all tool usage

### Output Format
Respond with structured analysis including:
1. Classification (TP/FP)
2. Severity (Critical/High/Medium/Low)
3. Rationale
4. Recommended actions
```

## Memory Systems

### Short-term Memory

Current conversation context:

```python
class ConversationMemory:
    def __init__(self, max_messages: int = 20):
        self.messages: list[Message] = []
        self.max_messages = max_messages

    def add(self, message: Message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self) -> str:
        return "\n".join(m.content for m in self.messages)
```

### Long-term Memory

Persistent knowledge storage:

```python
class VectorMemory:
    def __init__(self, embedding_model, vector_store):
        self.embedder = embedding_model
        self.store = vector_store

    async def remember(self, content: str, metadata: dict):
        embedding = await self.embedder.embed(content)
        await self.store.upsert(embedding, content, metadata)

    async def recall(self, query: str, top_k: int = 5):
        query_embedding = await self.embedder.embed(query)
        return await self.store.search(query_embedding, top_k)
```

### Working Memory

Current task state:

```python
class WorkingMemory:
    def __init__(self):
        self.current_goal: str = ""
        self.plan: list[str] = []
        self.completed_steps: list[str] = []
        self.observations: list[str] = []
        self.artifacts: dict = {}
```

## Tool System

### Tool Definition

```python
from pydantic import BaseModel, Field

class ToolSchema(BaseModel):
    """Schema for tool parameters."""
    pass

class SearchLogsInput(ToolSchema):
    query: str = Field(..., description="Search query")
    time_range: str = Field("1h", description="Time range (1h, 24h, 7d)")
    source: str = Field("all", description="Log source filter")

class Tool:
    name: str
    description: str
    input_schema: type[ToolSchema]

    async def execute(self, input: ToolSchema) -> str:
        raise NotImplementedError
```

### Tool Execution Flow

```
User Request
     │
     ▼
┌─────────────────┐
│ LLM determines  │
│ tool to use     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate input  │
│ against schema  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Check policy    │
│ permissions     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute tool    │
│ with timeout    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Log execution   │
│ for audit       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Return result   │
│ to LLM          │
└─────────────────┘
```

## Policy Engine

### Policy Types

1. **Permission Policies**: What actions are allowed
2. **Rate Policies**: How often actions can be taken
3. **Approval Policies**: What requires human approval
4. **Audit Policies**: What must be logged

### Policy Implementation

```python
class PolicyEngine:
    def __init__(self):
        self.rules: list[PolicyRule] = []

    def check(self, action: Action, context: Context) -> PolicyDecision:
        for rule in self.rules:
            decision = rule.evaluate(action, context)
            if decision.is_terminal:
                return decision
        return PolicyDecision.ALLOW

    def add_rule(self, rule: PolicyRule):
        self.rules.append(rule)

class ToolAllowlistRule(PolicyRule):
    def __init__(self, allowed_tools: set[str]):
        self.allowed = allowed_tools

    def evaluate(self, action: Action, context: Context) -> PolicyDecision:
        if action.tool_name not in self.allowed:
            return PolicyDecision.DENY
        return PolicyDecision.CONTINUE
```

## Agent Patterns

### ReAct Pattern

Reasoning and Acting in an interleaved manner:

```
Thought: I need to check if this IP is malicious
Action: lookup_ip_reputation(ip="192.168.1.100")
Observation: IP is associated with known C2 infrastructure
Thought: This is likely malicious, I should check for related activity
Action: search_logs(query="src_ip:192.168.1.100", time_range="24h")
Observation: Found 150 connections to internal hosts
Thought: This indicates lateral movement, severity is high
Final Answer: High severity - confirmed C2 communication with lateral movement
```

### Plan-and-Execute Pattern

First create a plan, then execute:

```python
class PlanAndExecuteAgent:
    async def run(self, goal: str):
        # Planning phase
        plan = await self.planner.create_plan(goal)

        # Execution phase
        for step in plan.steps:
            result = await self.executor.execute(step)
            if result.requires_replan:
                plan = await self.planner.replan(goal, result)
```

### Supervisor Pattern

Orchestrating multiple specialized agents:

```python
class SupervisorAgent:
    def __init__(self, agents: dict[str, Agent]):
        self.agents = agents

    async def run(self, task: str):
        # Determine which agent to use
        agent_name = await self.route(task)

        # Delegate to specialized agent
        agent = self.agents[agent_name]
        result = await agent.run(task)

        return result

    async def route(self, task: str) -> str:
        # LLM-based routing decision
        prompt = f"Which agent should handle: {task}"
        return await self.llm.complete(prompt)
```

## Error Handling

### Graceful Degradation

```python
class RobustAgent:
    async def execute_with_fallback(self, action: Action):
        try:
            return await self.execute(action)
        except ToolTimeout:
            return "Tool timed out, please try again"
        except ToolError as e:
            return f"Tool error: {e}. Continuing without this data."
        except RateLimitError:
            await asyncio.sleep(60)
            return await self.execute(action)
```

### Retry Logic

```python
async def retry_with_backoff(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0
):
    for attempt in range(max_retries):
        try:
            return await func()
        except RetryableError:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
    raise MaxRetriesExceeded()
```

## Observability

### Logging

```python
import structlog

logger = structlog.get_logger()

class ObservableAgent:
    async def run(self, task: str):
        run_id = uuid4()

        logger.info("agent_run_started", run_id=run_id, task=task)

        try:
            result = await self._run(task)
            logger.info("agent_run_completed", run_id=run_id)
            return result
        except Exception as e:
            logger.error("agent_run_failed", run_id=run_id, error=str(e))
            raise
```

### Metrics

Key metrics to track:

| Metric | Description |
|--------|-------------|
| `agent_runs_total` | Total agent executions |
| `agent_run_duration` | Time per execution |
| `tool_calls_total` | Tool usage count |
| `tool_errors_total` | Tool failure count |
| `tokens_used` | LLM token consumption |

## Summary

Agent architecture combines language models with tools, memory, and policies to create autonomous systems. Good architecture emphasizes safety, observability, and graceful error handling.

## Review Questions

1. What are the three types of memory in an agent system?
2. How does the policy engine control agent behavior?
3. What is the difference between ReAct and Plan-and-Execute patterns?
4. Why is observability important for agent systems?
