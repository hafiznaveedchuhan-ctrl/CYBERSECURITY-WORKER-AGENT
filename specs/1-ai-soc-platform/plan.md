# Implementation Plan: AI-SOC SecOps Agents Platform

**Branch**: `1-ai-soc-platform` | **Date**: 2026-01-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-ai-soc-platform/spec.md`

---

## Summary

Build a production-grade AI-SOC platform with:
- **Docusaurus textbook** site for SOC/SecOps learning content
- **Embedded RAG chatbot** with domain sub-agents (TRIAGE, ENRICHMENT, THREATINTEL, DETECTION-ENGINEER, INCIDENT-COMMANDER, REPORT-WRITER)
- **MCP Server** providing 15+ reusable security tools with allow-lists and audit logging
- **Human-in-the-loop** approval workflow for disruptive actions
- **Kubernetes-native deployment** using Docker, Helm, Dapr, and Minikube/GKE

---

## Technical Context

**Languages/Versions**:
- Frontend: TypeScript 5.x, React 18, Next.js 14
- Docs: TypeScript/JavaScript, Docusaurus 3.x
- Backend: Python 3.11+, FastAPI 0.100+
- MCP Server: Python 3.11+ (FastMCP)

**Primary Dependencies**:
- **Frontend**: Next.js 14, TailwindCSS, shadcn/ui, React Query
- **Docs**: Docusaurus 3.x, MDX
- **Backend**: FastAPI, OpenAI SDK, LangChain, Pydantic
- **MCP**: FastMCP, JSON Schema validation
- **Infra**: Docker, Helm 3, Dapr 1.12+, Kubernetes 1.28+

**Storage**:
- **Relational**: Neon Postgres (users, sessions, chat_messages, audit_logs, approvals, agent_runs)
- **Vector**: Qdrant (textbook_chunks, playbook_chunks)

**Testing**:
- Python: pytest, pytest-asyncio, pytest-cov
- TypeScript: Vitest, Playwright (E2E)
- RAG: Custom evaluation suite with retrieval metrics

**Target Platforms**:
- Local: Minikube with Dapr sidecars
- Production: GKE (Google Kubernetes Engine)
- Browser: Chrome, Firefox, Safari, Edge (latest 2 versions)

**Project Type**: Web application (frontend + backend + docs microservices)

**Performance Goals**:
- Alert triage response: < 30 seconds
- p95 latency: < 2 seconds
- Concurrent users: 100+
- Chat widget load: < 3 seconds

**Constraints**:
- Rate limiting: 60 requests/user/minute
- Token budget: Per-request and monthly caps
- Memory: Pod limits per service tier
- Uptime SLO: 99.5%

**Scale/Scope**:
- Initial users: 100 concurrent
- Textbook size: ~100 chapters, ~500 chunks
- Services: 7 microservices

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| I. Security-First Design | ✅ PASS | Tool allow-lists per agent (FR-018), approval gates for disruptive actions (FR-019), audit logging (FR-017), least privilege via RBAC (FR-030) |
| II. Grounded Responses | ✅ PASS | RAG retrieval required (FR-012), citations mandatory (FR-013), confidence thresholds (FR-015), selected-text priority (FR-009) |
| III. Microservices Architecture | ✅ PASS | 7 services defined: frontend, docs, chatbot-api, rag-service, ingestion-service, mcp-server, observability |
| IV. Kubernetes-Native | ✅ PASS | Docker images, Helm charts, Minikube local, Dapr sidecars, GKE production target |
| V. Observability & SLO | ✅ PASS | Structured logs (FR-031), metrics (FR-032), traces (FR-033), dashboards (FR-034), SLO alerts (FR-035) |
| VI. CI/CD Pipeline | ✅ PASS | GitHub Actions required, image scanning, SBOM generation, env separation |
| VII. Test-First Development | ✅ PASS | TDD workflow, RAG evaluation suite, integration tests for contracts |
| VIII. Human-in-the-Loop | ✅ PASS | Approval gates (FR-019), approval UI (FR-020), audit trail (FR-017) |
| IX. Cost & Rate Controls | ✅ PASS | Rate limiting (FR-026), token budgets, caching, K8s resource quotas |
| X. Supply-Chain Security | ✅ PASS | Image scanning in CI, SBOM generation, dependency lockfiles |

**Gate Status**: ✅ PASSED - All 10 principles satisfied

---

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-soc-platform/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── auth-api.yaml
│   ├── chat-api.yaml
│   ├── mcp-tools.yaml
│   └── ingestion-api.yaml
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx           # Landing page
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   └── dashboard/page.tsx
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Hero.tsx
│   │   ├── Footer.tsx
│   │   ├── AuthForm.tsx
│   │   ├── ChatWidget/
│   │   │   ├── ChatWidget.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── AgentBadge.tsx
│   │   │   ├── CitationsPanel.tsx
│   │   │   └── ApprovalDialog.tsx
│   │   └── ui/               # shadcn components
│   ├── lib/
│   │   ├── api.ts
│   │   └── auth.ts
│   └── styles/
├── public/
├── tests/
│   ├── e2e/
│   └── unit/
├── Dockerfile
└── package.json

docs/
├── docusaurus.config.ts
├── sidebars.ts
├── docs/
│   ├── module-1-soc-foundations/
│   ├── module-2-agentic-ai/
│   ├── module-3-ai-soc-workflows/
│   └── module-4-ai-security/
├── src/
│   └── theme/              # Custom theme overrides
├── static/
├── Dockerfile
└── package.json

backend/
├── services/
│   ├── chatbot_api/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   └── health.py
│   │   ├── agents/
│   │   │   ├── supervisor.py
│   │   │   ├── triage_agent.py
│   │   │   ├── enrichment_agent.py
│   │   │   ├── threatintel_agent.py
│   │   │   ├── detection_engineer_agent.py
│   │   │   ├── incident_commander_agent.py
│   │   │   └── report_writer_agent.py
│   │   ├── policies/
│   │   │   ├── tool_allowlist.py
│   │   │   └── approval_gate.py
│   │   └── Dockerfile
│   ├── rag_service/
│   │   ├── main.py
│   │   ├── retriever.py
│   │   ├── embeddings.py
│   │   └── Dockerfile
│   └── ingestion_service/
│       ├── main.py
│       ├── chunker.py
│       ├── indexer.py
│       └── Dockerfile
├── libs/
│   ├── db/
│   │   ├── models.py
│   │   └── session.py
│   ├── auth/
│   │   ├── jwt.py
│   │   └── password.py
│   ├── qdrant_client/
│   │   └── client.py
│   └── schemas/
│       ├── user.py
│       ├── chat.py
│       └── audit.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── pyproject.toml

mcp/
├── server/
│   ├── main.py
│   ├── tools/
│   │   ├── evidence_logs.py      # log_search, event_timeline, normalize_iocs, parse_raw_log
│   │   ├── threat_intel.py       # ioc_reputation, mitre_mapper, enrichment_geoip
│   │   ├── case_management.py    # create_case, add_case_note, generate_incident_report
│   │   ├── rag_knowledge.py      # rag_retrieve, rag_eval_run
│   │   └── safe_actions.py       # request_action, approve_action
│   ├── schemas/
│   │   └── tool_schemas.py
│   └── middleware/
│       ├── audit.py
│       └── auth.py
├── tests/
│   ├── test_tools.py
│   └── test_schemas.py
├── Dockerfile
└── pyproject.toml

deploy/
├── helm/
│   ├── ai-soc-platform/         # Umbrella chart
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   ├── frontend/
│   ├── docs/
│   ├── chatbot-api/
│   ├── rag-service/
│   ├── ingestion-service/
│   └── mcp-server/
├── dapr/
│   ├── components/
│   │   ├── pubsub.yaml
│   │   ├── statestore.yaml
│   │   └── secrets.yaml
│   └── config.yaml
├── k8s/
│   ├── rbac/
│   ├── network-policies/
│   └── pod-security/
└── observability/
    ├── prometheus/
    ├── grafana/
    └── jaeger/

scripts/
├── local-dev.sh
├── deploy-minikube.sh
├── deploy-gke.sh
└── run-tests.sh

.github/
└── workflows/
    ├── ci.yaml
    ├── cd-staging.yaml
    └── cd-production.yaml
```

**Structure Decision**: Web application with microservices architecture. Frontend (Next.js), Docs (Docusaurus), Backend services (FastAPI), and MCP server are separate deployable units with Helm charts. Dapr sidecars provide service mesh capabilities.

---

## Complexity Tracking

> No violations requiring justification. Architecture follows constitution principles with appropriate complexity for production SOC system.

---

## Architecture Decisions

### ADR-001: Agent Orchestration Pattern

**Decision**: Use SUPERVISOR agent pattern with specialized sub-agents
**Rationale**:
- Centralizes policy enforcement and tool allow-listing
- Enables clear separation of concerns per SOC role
- Facilitates future agent additions without core changes
**Alternatives Rejected**:
- Single monolithic agent: Harder to maintain, audit, and extend
- Peer-to-peer agents: Complex coordination, harder policy enforcement

### ADR-002: MCP Server as Tool Bus

**Decision**: Centralized MCP server exposing all tools via standardized interface
**Rationale**:
- Single point for audit logging
- Consistent schema validation
- Reusable across projects
- Clear allow-list enforcement
**Alternatives Rejected**:
- Direct tool calls from agents: No centralized audit, harder to secure
- Multiple tool servers: Operational complexity, inconsistent schemas

### ADR-003: Dapr for Service Communication

**Decision**: Use Dapr sidecars for service invocation, pub/sub, secrets
**Rationale**:
- Cloud-agnostic service mesh
- Built-in resiliency patterns (retries, circuit breakers)
- Simplified secrets management
- Consistent observability hooks
**Alternatives Rejected**:
- Direct HTTP calls: No built-in resiliency, harder secret management
- Istio: Higher complexity, steeper learning curve

### ADR-004: Neon Postgres + Qdrant

**Decision**: Split storage between relational (Neon) and vector (Qdrant)
**Rationale**:
- Neon: Serverless Postgres with connection pooling, ideal for transactional data
- Qdrant: Purpose-built for vector similarity search with filtering
- Clear data boundary: structured vs. semantic
**Alternatives Rejected**:
- Single Postgres with pgvector: Performance concerns at scale for vector search
- All in Qdrant: Poor fit for relational/transactional data

---

## Service Communication Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                               KUBERNETES CLUSTER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌───────────────┐               │
│  │   Frontend   │     │     Docs     │     │  Ingestion    │               │
│  │  (Next.js)   │     │ (Docusaurus) │     │   Service     │               │
│  │   + Dapr     │     │   + Dapr     │     │   + Dapr      │               │
│  └──────┬───────┘     └──────┬───────┘     └───────┬───────┘               │
│         │                    │                     │                        │
│         │                    │                     │                        │
│         ▼                    ▼                     ▼                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        DAPR SERVICE MESH                            │   │
│  │                   (Invocation, PubSub, Secrets)                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                    │                     │                        │
│         ▼                    ▼                     ▼                        │
│  ┌──────────────┐     ┌──────────────┐     ┌───────────────┐               │
│  │  Chatbot API │────▶│  RAG Service │     │  MCP Server   │               │
│  │  (FastAPI)   │     │  (FastAPI)   │     │  (FastMCP)    │               │
│  │   + Dapr     │     │   + Dapr     │     │   + Dapr      │               │
│  │              │     │              │     │               │               │
│  │ ┌──────────┐ │     └──────┬───────┘     │ ┌───────────┐ │               │
│  │ │SUPERVISOR│ │            │             │ │   TOOLS   │ │               │
│  │ │  AGENT   │ │────────────┼─────────────▶│ Evidence  │ │               │
│  │ └────┬─────┘ │            │             │ │ ThreatInt │ │               │
│  │      │       │            │             │ │   Case    │ │               │
│  │ ┌────┴─────┐ │            │             │ │   RAG     │ │               │
│  │ │SUB-AGENTS│ │            │             │ │SafeAction │ │               │
│  │ │ TRIAGE   │ │            │             │ └───────────┘ │               │
│  │ │ ENRICH   │ │            │             └───────┬───────┘               │
│  │ │ THREAT   │ │            │                     │                        │
│  │ │ DETECT   │ │            │                     │                        │
│  │ │ IR-LEAD  │ │            │                     │                        │
│  │ │ REPORT   │ │            ▼                     │                        │
│  │ └──────────┘ │     ┌──────────────┐             │                        │
│  └──────┬───────┘     │    Qdrant    │             │                        │
│         │             │ (Vector DB)  │◀────────────┘                        │
│         │             └──────────────┘                                      │
│         ▼                                                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         NEON POSTGRES                                │  │
│  │  users │ sessions │ chat_messages │ audit_logs │ approvals │ runs   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      OBSERVABILITY STACK                             │  │
│  │           Prometheus │ Grafana │ Jaeger │ Alertmanager               │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                          ┌──────────────────┐
                          │   OpenAI API     │
                          │   (External)     │
                          └──────────────────┘
```

---

## Security Architecture

### Authentication Flow

```
User ──► Frontend ──► Chatbot API ──► JWT Validation ──► Session Check ──► Authorized
                                           │
                                           ▼
                                    Neon Postgres
                                    (users, sessions)
```

### Tool Execution Flow (with Approval Gate)

```
Agent ──► MCP Tool Call ──► Allow-List Check ──► Schema Validation
                                    │
                                    ▼
                            Disruptive Action?
                                   / \
                                  /   \
                                YES    NO
                                 │      │
                                 ▼      ▼
                          Create     Execute
                          Approval   Immediately
                          Request        │
                             │           │
                             ▼           │
                          Human          │
                          Approval       │
                             │           │
                             ▼           │
                          Execute◄───────┘
                             │
                             ▼
                        Audit Log
                        (Neon Postgres)
```

---

## Deployment Strategy

### Local Development (Minikube)

```bash
# Start Minikube with Dapr
minikube start --memory=8192 --cpus=4
dapr init --kubernetes

# Deploy all services
helm install ai-soc ./deploy/helm/ai-soc-platform -f ./deploy/helm/values-local.yaml

# Port forward for local access
kubectl port-forward svc/frontend 3000:80
kubectl port-forward svc/docs 3001:80
```

### Production (GKE)

```bash
# CI/CD pipeline handles:
# 1. Build Docker images
# 2. Push to GCR
# 3. Image security scan
# 4. SBOM generation
# 5. Helm deploy to staging
# 6. Integration tests
# 7. Manual approval gate
# 8. Helm deploy to production
```

---

## Phase Outputs Reference

| Phase | Artifact | Description |
|-------|----------|-------------|
| 0 | research.md | Technology decisions and best practices |
| 1 | data-model.md | Database schemas and entity relationships |
| 1 | contracts/*.yaml | OpenAPI specs for all services |
| 1 | quickstart.md | Local development setup guide |
| 2 | tasks.md | Implementation tasks (/sp.tasks output) |
