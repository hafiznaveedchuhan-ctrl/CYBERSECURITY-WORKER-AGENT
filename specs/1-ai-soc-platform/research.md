# Research: AI-SOC SecOps Agents Platform

**Branch**: `1-ai-soc-platform` | **Date**: 2026-01-04 | **Phase**: 0
**Input**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

---

## Purpose

Document technology decisions, best practices research, and implementation patterns for the AI-SOC platform before starting Phase 1 design work.

---

## Technology Stack Research

### 1. Frontend Framework: Next.js 14 + App Router

**Decision**: Use Next.js 14 with App Router for the frontend application.

**Research Findings**:
- **App Router** provides React Server Components, reducing client-side JavaScript bundle
- **Route Handlers** simplify API proxying without separate BFF layer
- **Built-in Image Optimization** reduces bandwidth for documentation assets
- **Streaming SSR** enables progressive rendering for chat widget

**Best Practices**:
- Use `"use client"` directive only for interactive components (ChatWidget, AuthForm)
- Implement route groups for (auth), (dashboard), (docs) layout separation
- Use React Query for server state management with optimistic updates
- Implement proper error boundaries per route segment

**References**:
- [Next.js App Router Docs](https://nextjs.org/docs/app)
- [React Server Components RFC](https://github.com/reactjs/rfcs/pull/188)

---

### 2. Documentation Framework: Docusaurus 3.x

**Decision**: Use Docusaurus 3.x with custom theme for textbook content.

**Research Findings**:
- **MDX 2.0 Support** enables React components embedded in markdown
- **Versioning** built-in for textbook revision management
- **Search Integration** via Algolia DocSearch or local search plugin
- **i18n Ready** for future multi-language support

**Best Practices**:
- Use sidebar auto-generation from folder structure
- Implement custom `AskAI` component for text selection context
- Add front matter for chapter metadata (difficulty, prerequisites, estimated time)
- Enable reading time plugin for study planning

**Chat Widget Integration Pattern**:
```jsx
// src/theme/Root.js - Global chat widget wrapper
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatWidget
        onTextSelect={(text, page) => setContext({text, page})}
      />
    </>
  );
}
```

**References**:
- [Docusaurus Documentation](https://docusaurus.io/docs)
- [MDX Components Guide](https://docusaurus.io/docs/markdown-features/react)

---

### 3. Backend Framework: FastAPI

**Decision**: Use FastAPI for all Python backend services.

**Research Findings**:
- **Async Native** with ASGI support (uvicorn/hypercorn)
- **Pydantic v2** for data validation with improved performance
- **OpenAPI Auto-Generation** for API documentation and client codegen
- **Dependency Injection** for clean auth, db session management

**Best Practices**:
- Use `lifespan` context manager for startup/shutdown
- Implement proper request_id middleware for tracing
- Use `BackgroundTasks` for non-blocking audit logging
- Structure with routers per domain (auth, chat, admin)

**Service Structure Pattern**:
```
services/chatbot_api/
├── main.py           # FastAPI app, lifespan, middleware
├── config.py         # Pydantic Settings
├── deps.py           # Dependency injection
├── routers/
│   ├── auth.py       # /auth endpoints
│   ├── chat.py       # /chat endpoints
│   └── health.py     # /health, /ready
├── agents/           # LangChain agent implementations
├── policies/         # Tool allowlists, approval gates
└── schemas/          # Pydantic request/response models
```

**References**:
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic V2 Migration](https://docs.pydantic.dev/latest/migration/)

---

### 4. AI/ML Stack: OpenAI SDK + LangChain

**Decision**: Use OpenAI SDK with LangChain for agent orchestration.

**Research Findings**:
- **OpenAI Agents SDK** (Beta) provides native tool calling with structured outputs
- **LangChain Expression Language (LCEL)** for composable agent chains
- **LangSmith** for tracing and evaluation (optional)
- **Token Counting** via tiktoken for budget enforcement

**Agent Architecture Pattern**:
```python
# Supervisor Agent Pattern
class SupervisorAgent:
    """Routes to specialized sub-agents based on intent"""

    def __init__(self):
        self.agents = {
            "triage": TriageAgent(),
            "enrichment": EnrichmentAgent(),
            "threatintel": ThreatIntelAgent(),
            "detection": DetectionEngineerAgent(),
            "incident": IncidentCommanderAgent(),
            "report": ReportWriterAgent(),
        }
        self.tool_registry = MCPToolRegistry()

    async def route(self, message: str, context: ChatContext) -> AgentResponse:
        intent = await self.classify_intent(message)
        agent = self.agents[intent.agent_name]

        # Apply tool allowlist for selected agent
        allowed_tools = self.tool_registry.get_allowlist(intent.agent_name)

        return await agent.execute(
            message=message,
            context=context,
            tools=allowed_tools
        )
```

**Tool Allow-List Implementation**:
```python
AGENT_TOOL_ALLOWLISTS = {
    "triage": ["log_search", "rag_retrieve", "mitre_mapper"],
    "enrichment": ["ioc_reputation", "enrichment_geoip", "event_timeline"],
    "threatintel": ["ioc_reputation", "mitre_mapper", "rag_retrieve"],
    "detection": ["log_search", "rag_retrieve", "parse_raw_log"],
    "incident": ["create_case", "add_case_note", "request_action"],  # request_action requires approval
    "report": ["rag_retrieve", "generate_incident_report"],
}

DISRUPTIVE_TOOLS = ["disable_user", "isolate_host", "block_ioc"]
```

**References**:
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [LangChain Agent Concepts](https://python.langchain.com/docs/modules/agents/)

---

### 5. Vector Database: Qdrant

**Decision**: Use Qdrant for vector similarity search on textbook content.

**Research Findings**:
- **Filtering Support** enables metadata-based result refinement
- **Payload Storage** co-locates metadata with vectors
- **Batch Operations** for efficient bulk ingestion
- **Snapshot/Backup** for disaster recovery

**Collection Schema**:
```python
TEXTBOOK_COLLECTION = {
    "name": "textbook_chunks",
    "vectors_config": {
        "size": 1536,  # text-embedding-3-small
        "distance": "Cosine"
    },
    "payload_schema": {
        "source_page": "keyword",      # e.g., "/module-1/chapter-3"
        "module": "keyword",           # e.g., "module-1-soc-foundations"
        "chapter": "keyword",          # e.g., "siem-fundamentals"
        "chunk_index": "integer",      # position within page
        "content": "text",             # raw text for display
        "metadata": "json"             # title, difficulty, etc.
    }
}
```

**Retrieval Pattern**:
```python
async def retrieve_context(query: str, filter_page: str = None) -> List[Chunk]:
    query_vector = await embed(query)

    filter_condition = None
    if filter_page:
        filter_condition = models.Filter(
            must=[models.FieldCondition(
                key="source_page",
                match=models.MatchValue(value=filter_page)
            )]
        )

    results = client.search(
        collection_name="textbook_chunks",
        query_vector=query_vector,
        query_filter=filter_condition,
        limit=5,
        with_payload=True
    )
    return [Chunk.from_qdrant(r) for r in results]
```

**References**:
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Python Client](https://github.com/qdrant/qdrant-client)

---

### 6. Relational Database: Neon Postgres

**Decision**: Use Neon Postgres for transactional data.

**Research Findings**:
- **Serverless Architecture** with automatic scaling to zero
- **Connection Pooling** via built-in proxy (pgbouncer-compatible)
- **Branching** for development/testing environments
- **Point-in-Time Recovery** for disaster recovery

**Connection Pattern**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")  # neon connection string

engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

**Migration Strategy**:
- Use Alembic with async support
- Version control all migrations
- Test rollback procedures in CI

**References**:
- [Neon Documentation](https://neon.tech/docs)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

---

### 7. MCP Server: FastMCP

**Decision**: Use FastMCP for Model Context Protocol server implementation.

**Research Findings**:
- **Schema-First** development with JSON Schema validation
- **Middleware Support** for logging, auth, rate limiting
- **Async Native** compatible with FastAPI ecosystem

**Tool Registration Pattern**:
```python
from fastmcp import FastMCP, Tool

mcp = FastMCP("ai-soc-tools")

@mcp.tool()
async def log_search(
    query: str,
    time_range: str = "24h",
    source: str = None
) -> dict:
    """Search security logs for matching events.

    Args:
        query: Search query (Lucene syntax)
        time_range: Time range (1h, 24h, 7d)
        source: Optional log source filter

    Returns:
        Matching log entries with metadata
    """
    # Implementation with audit logging
    audit_log.record(
        tool="log_search",
        inputs={"query": query, "time_range": time_range},
        user=get_current_user()
    )
    return await log_backend.search(query, time_range, source)
```

**Audit Middleware**:
```python
@mcp.middleware
async def audit_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)

    await AuditLog.create(
        user_id=request.user_id,
        tool_name=request.tool_name,
        inputs=request.inputs,
        outputs=response.outputs,
        latency_ms=(time.time() - start) * 1000,
        status="success" if not response.error else "error"
    )

    return response
```

**References**:
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

---

### 8. Container Orchestration: Kubernetes + Dapr

**Decision**: Use Kubernetes with Dapr sidecars for service mesh.

**Research Findings**:
- **Dapr Service Invocation** provides automatic mTLS, retries, load balancing
- **Dapr State Store** abstracts cache/session storage
- **Dapr Pub/Sub** for async event processing
- **Dapr Secrets** for centralized secret management

**Dapr Components**:
```yaml
# components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
    - name: redisHost
      value: "redis:6379"

---
# components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      secretKeyRef:
        name: neon-credentials
        key: connection-string
```

**Service Invocation Pattern**:
```python
from dapr.clients import DaprClient

async def call_rag_service(query: str, context: dict):
    async with DaprClient() as client:
        response = await client.invoke_method(
            app_id="rag-service",
            method_name="retrieve",
            data=json.dumps({"query": query, "context": context}),
            content_type="application/json"
        )
        return json.loads(response.data)
```

**References**:
- [Dapr Documentation](https://docs.dapr.io/)
- [Dapr Python SDK](https://github.com/dapr/python-sdk)

---

### 9. Observability Stack

**Decision**: Prometheus + Grafana + Jaeger for observability.

**Research Findings**:
- **Prometheus** for metrics collection with PromQL queries
- **Grafana** for dashboards and alerting
- **Jaeger** for distributed tracing
- **OpenTelemetry** for instrumentation standard

**Key Metrics**:
```python
from prometheus_client import Counter, Histogram, Gauge

# Agent metrics
AGENT_REQUESTS = Counter(
    "agent_requests_total",
    "Total agent requests",
    ["agent_name", "status"]
)

AGENT_LATENCY = Histogram(
    "agent_latency_seconds",
    "Agent response latency",
    ["agent_name"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

# Tool metrics
TOOL_CALLS = Counter(
    "tool_calls_total",
    "Total MCP tool calls",
    ["tool_name", "agent_name", "status"]
)

# RAG metrics
RAG_RETRIEVAL_LATENCY = Histogram(
    "rag_retrieval_latency_seconds",
    "RAG retrieval latency",
    buckets=[0.05, 0.1, 0.25, 0.5, 1.0]
)

RAG_RELEVANCE_SCORE = Histogram(
    "rag_relevance_score",
    "RAG result relevance scores",
    buckets=[0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
)
```

**SLO Alerts**:
```yaml
# SLO: 99.5% success rate
- alert: AgentErrorRateHigh
  expr: |
    sum(rate(agent_requests_total{status="error"}[5m]))
    / sum(rate(agent_requests_total[5m])) > 0.005
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: Agent error rate exceeds 0.5%

# SLO: p95 latency < 2s
- alert: AgentLatencyHigh
  expr: histogram_quantile(0.95, rate(agent_latency_seconds_bucket[5m])) > 2
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: Agent p95 latency exceeds 2 seconds
```

**References**:
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)

---

### 10. CI/CD Pipeline: GitHub Actions

**Decision**: Use GitHub Actions for CI/CD with security scanning.

**Research Findings**:
- **Reusable Workflows** for consistent patterns across services
- **OIDC Authentication** for secure GCP access without long-lived tokens
- **Matrix Builds** for parallel testing across Python versions
- **Artifact Attestation** for supply chain security

**Pipeline Stages**:
```yaml
# .github/workflows/ci.yaml
name: CI Pipeline

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run ruff
        run: ruff check .
      - name: Run mypy
        run: mypy .

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'
      - name: Run Snyk
        uses: snyk/actions/python@master

  build:
    needs: [lint, test, security-scan]
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: docker compose build
      - name: Scan images
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'ai-soc-chatbot-api:latest'
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
```

**References**:
- [GitHub Actions Security](https://docs.github.com/en/actions/security-guides)
- [Container Security Scanning](https://aquasecurity.github.io/trivy/)

---

## RAG Evaluation Strategy

**Decision**: Custom evaluation suite with automated metrics.

**Metrics**:
1. **Retrieval Precision@K**: % of top-K results that are relevant
2. **Retrieval Recall**: % of relevant documents retrieved
3. **Answer Groundedness**: % of response grounded in retrieved context
4. **Citation Accuracy**: % of citations pointing to correct source

**Evaluation Dataset Structure**:
```json
{
  "queries": [
    {
      "id": "eval-001",
      "query": "What is a SIEM system?",
      "expected_chunks": ["module-1/chapter-2#siem-definition"],
      "expected_answer_contains": ["Security Information", "Event Management", "correlation"],
      "category": "definition"
    }
  ]
}
```

**Evaluation Script**:
```python
async def evaluate_rag_pipeline(eval_dataset: str):
    results = []
    for query in load_dataset(eval_dataset):
        retrieved = await rag_service.retrieve(query.query)
        response = await agent.generate(query.query, retrieved)

        results.append({
            "query_id": query.id,
            "precision_at_5": calculate_precision(retrieved[:5], query.expected_chunks),
            "recall": calculate_recall(retrieved, query.expected_chunks),
            "groundedness": calculate_groundedness(response, retrieved),
            "citation_accuracy": calculate_citation_accuracy(response.citations, retrieved)
        })

    return aggregate_metrics(results)
```

---

## Human-in-the-Loop Workflow

**Decision**: Approval gates for disruptive actions with timeout.

**Workflow**:
```
1. Agent suggests disruptive action
2. System creates ApprovalRequest in DB
3. UI displays approval dialog to authorized users
4. User approves/rejects with optional reason
5. System executes action (if approved) and logs result
6. Request expires after 24 hours if not acted upon
```

**ApprovalRequest States**:
```
PENDING ──► APPROVED ──► EXECUTED
    │           │
    └──► REJECTED
    │
    └──► EXPIRED (after 24h)
```

**UI Component**:
```tsx
function ApprovalDialog({ request }: { request: ApprovalRequest }) {
  return (
    <Dialog open={request.status === 'pending'}>
      <DialogHeader>
        <Badge variant="warning">Approval Required</Badge>
        <h3>{request.action_type}</h3>
      </DialogHeader>
      <DialogContent>
        <p>Agent: {request.agent_name}</p>
        <p>Action: {request.action_type}</p>
        <p>Target: {JSON.stringify(request.params)}</p>
        <p>Risk: {request.risk_assessment}</p>
      </DialogContent>
      <DialogFooter>
        <Button variant="destructive" onClick={() => reject(request.id)}>
          Reject
        </Button>
        <Button variant="default" onClick={() => approve(request.id)}>
          Approve
        </Button>
      </DialogFooter>
    </Dialog>
  );
}
```

---

## Next Steps

1. **Phase 1**: Create `data-model.md` with complete database schemas
2. **Phase 1**: Create API contracts in `contracts/` directory
3. **Phase 1**: Create `quickstart.md` for local development
4. **Phase 2**: Generate implementation tasks via `/sp.tasks`

---

## Research Approval

- [ ] Technical Lead review
- [ ] Security review for disruptive action workflow
- [ ] DevOps review for deployment strategy
