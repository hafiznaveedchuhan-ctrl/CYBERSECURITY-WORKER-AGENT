# Tasks: AI-SOC SecOps Agents Platform

**Input**: Design documents from `/specs/1-ai-soc-platform/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Branch**: `1-ai-soc-platform`
**Generated**: 2026-01-04

**Tests**: Not explicitly requested - test tasks omitted. Add TDD tasks if needed.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US7)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, repository structure, and development environment

- [ ] T001 Create root project structure per plan.md layout (frontend/, backend/, docs/, mcp/, deploy/, scripts/)
- [ ] T002 [P] Initialize frontend Next.js 14 project with TypeScript in frontend/
- [ ] T003 [P] Initialize backend Python project with Poetry in backend/pyproject.toml
- [ ] T004 [P] Initialize docs Docusaurus 3.x project in docs/
- [ ] T005 [P] Initialize MCP server Python project with Poetry in mcp/pyproject.toml
- [ ] T006 [P] Create .env.example with all required environment variables
- [ ] T007 [P] Configure ESLint, Prettier for frontend in frontend/.eslintrc.js
- [ ] T008 [P] Configure ruff, mypy for Python projects in backend/pyproject.toml and mcp/pyproject.toml
- [ ] T009 [P] Create GitHub Actions CI workflow in .github/workflows/ci.yaml
- [ ] T010 [P] Create docker-compose.yaml for local development with all services
- [ ] T011 Create Dockerfiles for all services (frontend, docs, chatbot-api, rag-service, ingestion-service, mcp-server)

**Checkpoint**: Project structure ready, all projects initialized with dependencies

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database & Models (Shared)

- [ ] T012 Configure Alembic for async migrations in backend/alembic/
- [ ] T013 Create SQLAlchemy async engine and session factory in backend/libs/db/session.py
- [ ] T014 [P] Create User SQLAlchemy model in backend/libs/db/models.py
- [ ] T015 [P] Create Session SQLAlchemy model in backend/libs/db/models.py
- [ ] T016 [P] Create ChatMessage SQLAlchemy model in backend/libs/db/models.py
- [ ] T017 [P] Create AuditLog SQLAlchemy model in backend/libs/db/models.py
- [ ] T018 [P] Create ApprovalRequest SQLAlchemy model in backend/libs/db/models.py
- [ ] T019 [P] Create AgentRun SQLAlchemy model in backend/libs/db/models.py
- [ ] T020 Create initial Alembic migration with all tables in backend/alembic/versions/001_initial_schema.py

### Pydantic Schemas (Shared)

- [ ] T021 [P] Create User Pydantic schemas in backend/libs/schemas/user.py
- [ ] T022 [P] Create Session Pydantic schemas in backend/libs/schemas/session.py
- [ ] T023 [P] Create ChatMessage Pydantic schemas in backend/libs/schemas/chat.py
- [ ] T024 [P] Create AuditLog Pydantic schemas in backend/libs/schemas/audit.py
- [ ] T025 [P] Create ApprovalRequest Pydantic schemas in backend/libs/schemas/approval.py
- [ ] T026 [P] Create AgentRun Pydantic schemas in backend/libs/schemas/agent_run.py

### Auth Infrastructure (Shared)

- [ ] T027 Implement JWT token generation and validation in backend/libs/auth/jwt.py
- [ ] T028 Implement password hashing with bcrypt in backend/libs/auth/password.py
- [ ] T029 Create auth dependency injection in backend/services/chatbot_api/deps.py

### FastAPI Setup (Shared)

- [ ] T030 Create FastAPI app with lifespan in backend/services/chatbot_api/main.py
- [ ] T031 [P] Create config with Pydantic Settings in backend/services/chatbot_api/config.py
- [ ] T032 [P] Implement request_id and trace_id middleware in backend/services/chatbot_api/middleware.py
- [ ] T033 [P] Create health check router in backend/services/chatbot_api/routers/health.py
- [ ] T034 Implement rate limiting middleware in backend/services/chatbot_api/middleware.py

### Qdrant Setup (Shared)

- [ ] T035 Create Qdrant client wrapper in backend/libs/qdrant_client/client.py
- [ ] T036 Create textbook_chunks collection initialization in backend/libs/qdrant_client/collections.py

### MCP Server Foundation

- [ ] T037 Create FastMCP app in mcp/server/main.py
- [ ] T038 [P] Create audit middleware for tool logging in mcp/server/middleware/audit.py
- [ ] T039 [P] Create auth middleware for agent tokens in mcp/server/middleware/auth.py
- [ ] T040 Create tool schemas base in mcp/server/schemas/tool_schemas.py

### Frontend Foundation

- [ ] T041 Install TailwindCSS, shadcn/ui in frontend/
- [ ] T042 [P] Create API client with fetch wrapper in frontend/src/lib/api.ts
- [ ] T043 [P] Create auth context provider in frontend/src/lib/auth.ts
- [ ] T044 [P] Create Navbar component in frontend/src/components/Navbar.tsx
- [ ] T045 [P] Create Footer component in frontend/src/components/Footer.tsx

### Docusaurus Foundation

- [ ] T046 Configure Docusaurus with custom theme in docs/docusaurus.config.ts
- [ ] T047 Create sidebar configuration in docs/sidebars.ts
- [ ] T048 Create placeholder module structure in docs/docs/module-1-soc-foundations/

**Checkpoint**: Foundation ready - all services can start, database tables exist, auth works. User story implementation can now begin in parallel.

---

## Phase 3: User Story 5 - Authentication & Session (Priority: P2 - Prerequisite for all)

**Goal**: Users can sign up, log in, and maintain persistent sessions across visits

**Independent Test**: Sign up → logout → login → verify chat history is accessible

**Note**: Although P2 priority, this story MUST be implemented first as it's a prerequisite for all other stories

### Implementation for User Story 5

- [ ] T049 [US5] Implement signup endpoint in backend/services/chatbot_api/routers/auth.py (POST /auth/signup)
- [ ] T050 [US5] Implement login endpoint in backend/services/chatbot_api/routers/auth.py (POST /auth/login)
- [ ] T051 [US5] Implement logout endpoint in backend/services/chatbot_api/routers/auth.py (POST /auth/logout)
- [ ] T052 [US5] Implement token refresh endpoint in backend/services/chatbot_api/routers/auth.py (POST /auth/refresh)
- [ ] T053 [US5] Implement get current user endpoint in backend/services/chatbot_api/routers/auth.py (GET /auth/me)
- [ ] T054 [US5] Implement session list endpoint in backend/services/chatbot_api/routers/auth.py (GET /auth/sessions)
- [ ] T055 [US5] Implement session revocation endpoint in backend/services/chatbot_api/routers/auth.py (DELETE /auth/sessions/{id})
- [ ] T056 [P] [US5] Create AuthForm component in frontend/src/components/AuthForm.tsx
- [ ] T057 [P] [US5] Create login page in frontend/src/app/login/page.tsx
- [ ] T058 [P] [US5] Create signup page in frontend/src/app/signup/page.tsx
- [ ] T059 [US5] Add session validation middleware to protected routes in backend/services/chatbot_api/deps.py
- [ ] T060 [US5] Implement account lockout after failed attempts in backend/services/chatbot_api/routers/auth.py

**Checkpoint**: Users can create accounts, login, maintain sessions. All subsequent stories can now authenticate users.

---

## Phase 4: User Story 3 - Interactive Textbook Learning (Priority: P2)

**Goal**: Students can highlight text and ask AI for explanations with RAG context

**Independent Test**: Highlight text on textbook page → click "Ask AI" → response prioritizes selected text with citations

### RAG Service

- [ ] T061 [US3] Create RAG service FastAPI app in backend/services/rag_service/main.py
- [ ] T062 [US3] Implement OpenAI embeddings wrapper in backend/services/rag_service/embeddings.py
- [ ] T063 [US3] Implement context-aware retriever with page filtering in backend/services/rag_service/retriever.py
- [ ] T064 [US3] Create retrieve endpoint (POST /retrieve) in backend/services/rag_service/main.py
- [ ] T065 [US3] Create RAG service Dockerfile in backend/services/rag_service/Dockerfile

### Ingestion Service

- [ ] T066 [P] [US3] Create ingestion service FastAPI app in backend/services/ingestion_service/main.py
- [ ] T067 [P] [US3] Implement markdown chunker in backend/services/ingestion_service/chunker.py
- [ ] T068 [P] [US3] Implement Qdrant indexer in backend/services/ingestion_service/indexer.py
- [ ] T069 [US3] Create textbook ingest endpoint (POST /ingest/textbook) in backend/services/ingestion_service/main.py
- [ ] T070 [US3] Create ingest job status endpoint (GET /ingest/jobs/{id}) in backend/services/ingestion_service/main.py
- [ ] T071 [US3] Create ingestion service Dockerfile in backend/services/ingestion_service/Dockerfile

### Textbook Content

- [ ] T072 [P] [US3] Create Module 1 placeholder content in docs/docs/module-1-soc-foundations/
- [ ] T073 [P] [US3] Create Module 2 placeholder content in docs/docs/module-2-agentic-ai/
- [ ] T074 [P] [US3] Create Module 3 placeholder content in docs/docs/module-3-ai-soc-workflows/
- [ ] T075 [P] [US3] Create Module 4 placeholder content in docs/docs/module-4-ai-security/

### Chat Widget - Text Selection

- [ ] T076 [US3] Create ChatWidget container component in frontend/src/components/ChatWidget/ChatWidget.tsx
- [ ] T077 [P] [US3] Create MessageBubble component in frontend/src/components/ChatWidget/MessageBubble.tsx
- [ ] T078 [P] [US3] Create AgentBadge component in frontend/src/components/ChatWidget/AgentBadge.tsx
- [ ] T079 [P] [US3] Create CitationsPanel component in frontend/src/components/ChatWidget/CitationsPanel.tsx
- [ ] T080 [US3] Implement text selection detection in Docusaurus theme in docs/src/theme/Root.js
- [ ] T081 [US3] Implement chat widget embedding in Docusaurus in docs/src/theme/Root.js

### Chat Backend - Basic Messages

- [ ] T082 [US3] Implement send message endpoint (POST /chat/messages) in backend/services/chatbot_api/routers/chat.py
- [ ] T083 [US3] Implement chat history endpoint (GET /chat/history) in backend/services/chatbot_api/routers/chat.py
- [ ] T084 [US3] Implement clear history endpoint (POST /chat/history/clear) in backend/services/chatbot_api/routers/chat.py

**Checkpoint**: Textbook is browsable, text can be selected, basic chat with RAG retrieval works. Citations are displayed.

---

## Phase 5: User Story 1 - SOC Analyst Alert Triage (Priority: P1) - MVP

**Goal**: SOC analyst can paste alert, receive severity assessment with rationale and next steps in <30 seconds

**Independent Test**: Paste phishing alert → TRIAGE-AGENT responds with severity, rationale citing textbook, 3-5 next steps

### Supervisor Agent

- [ ] T085 [US1] Create base agent class with tool calling in backend/services/chatbot_api/agents/base.py
- [ ] T086 [US1] Implement SUPERVISOR agent with intent routing in backend/services/chatbot_api/agents/supervisor.py
- [ ] T087 [US1] Create tool allowlist registry in backend/services/chatbot_api/policies/tool_allowlist.py

### TRIAGE Agent

- [ ] T088 [US1] Implement TRIAGE-AGENT with severity classification in backend/services/chatbot_api/agents/triage_agent.py
- [ ] T089 [US1] Create triage prompt templates with few-shot examples in backend/services/chatbot_api/agents/prompts/triage.py

### ENRICHMENT Agent

- [ ] T090 [P] [US1] Implement ENRICHMENT-AGENT for IOC enrichment in backend/services/chatbot_api/agents/enrichment_agent.py
- [ ] T091 [P] [US1] Create enrichment prompt templates in backend/services/chatbot_api/agents/prompts/enrichment.py

### MCP Tools - Evidence & Logs

- [ ] T092 [P] [US1] Implement log_search tool in mcp/server/tools/evidence_logs.py
- [ ] T093 [P] [US1] Implement event_timeline tool in mcp/server/tools/evidence_logs.py
- [ ] T094 [P] [US1] Implement normalize_iocs tool in mcp/server/tools/evidence_logs.py
- [ ] T095 [P] [US1] Implement parse_raw_log tool in mcp/server/tools/evidence_logs.py

### MCP Tools - Threat Intel

- [ ] T096 [P] [US1] Implement ioc_reputation tool in mcp/server/tools/threat_intel.py
- [ ] T097 [P] [US1] Implement enrichment_geoip tool in mcp/server/tools/threat_intel.py

### MCP Tools - RAG

- [ ] T098 [US1] Implement rag_retrieve tool in mcp/server/tools/rag_knowledge.py

### Agent Run Tracking

- [ ] T099 [US1] Implement agent run logging in backend/services/chatbot_api/agents/base.py
- [ ] T100 [US1] Add token counting and budget enforcement in backend/services/chatbot_api/agents/base.py

### Chat Integration

- [ ] T101 [US1] Integrate SUPERVISOR with chat endpoint in backend/services/chatbot_api/routers/chat.py
- [ ] T102 [US1] Add agent name to response for badge display in backend/services/chatbot_api/routers/chat.py
- [ ] T103 [US1] Implement streaming response endpoint (POST /chat/messages/stream) in backend/services/chatbot_api/routers/chat.py

**Checkpoint**: Core MVP complete. Alert triage works with severity, rationale, next steps, and citations. Agent badges display.

---

## Phase 6: User Story 2 - Incident Report Generation (Priority: P1)

**Goal**: Analyst can request incident report and receive structured report with all sections in <60 seconds

**Independent Test**: Request "generate incident report" for case → REPORT-WRITER produces executive summary, timeline, findings, impact, remediation, prevention

### REPORT-WRITER Agent

- [ ] T104 [US2] Implement REPORT-WRITER-AGENT in backend/services/chatbot_api/agents/report_writer_agent.py
- [ ] T105 [US2] Create report prompt templates with section structure in backend/services/chatbot_api/agents/prompts/report.py

### MCP Tools - Case Management

- [ ] T106 [P] [US2] Implement create_case tool in mcp/server/tools/case_management.py
- [ ] T107 [P] [US2] Implement add_case_note tool in mcp/server/tools/case_management.py
- [ ] T108 [US2] Implement generate_incident_report tool in mcp/server/tools/case_management.py

### Report Generation

- [ ] T109 [US2] Connect REPORT-WRITER to case data in backend/services/chatbot_api/agents/report_writer_agent.py
- [ ] T110 [US2] Add report formatting with markdown in backend/services/chatbot_api/agents/report_writer_agent.py
- [ ] T111 [US2] Add textbook citation grounding to reports in backend/services/chatbot_api/agents/report_writer_agent.py

**Checkpoint**: Incident reports can be generated with all required sections, citations, and proper formatting.

---

## Phase 7: User Story 4 - Human-Approved Response Actions (Priority: P2)

**Goal**: Disruptive actions require human approval before execution with full audit trail

**Independent Test**: Trigger "disable user" → approval dialog appears → approve → action logged and confirmed

### INCIDENT-COMMANDER Agent

- [ ] T112 [US4] Implement INCIDENT-COMMANDER-AGENT in backend/services/chatbot_api/agents/incident_commander_agent.py
- [ ] T113 [US4] Create incident commander prompts in backend/services/chatbot_api/agents/prompts/incident_commander.py

### Approval Gate Infrastructure

- [ ] T114 [US4] Implement approval gate policy in backend/services/chatbot_api/policies/approval_gate.py
- [ ] T115 [US4] Create approval request service in backend/services/chatbot_api/services/approval_service.py
- [ ] T116 [US4] Implement approval expiration scheduler in backend/services/chatbot_api/services/approval_scheduler.py

### Approval API Endpoints

- [ ] T117 [US4] Implement list approvals endpoint (GET /approvals) in backend/services/chatbot_api/routers/approvals.py
- [ ] T118 [US4] Implement get approval endpoint (GET /approvals/{id}) in backend/services/chatbot_api/routers/approvals.py
- [ ] T119 [US4] Implement approve action endpoint (POST /approvals/{id}/approve) in backend/services/chatbot_api/routers/approvals.py
- [ ] T120 [US4] Implement reject action endpoint (POST /approvals/{id}/reject) in backend/services/chatbot_api/routers/approvals.py

### MCP Tools - Safe Actions

- [ ] T121 [P] [US4] Implement request_action tool in mcp/server/tools/safe_actions.py
- [ ] T122 [P] [US4] Implement approve_action tool (internal) in mcp/server/tools/safe_actions.py

### Approval UI

- [ ] T123 [US4] Create ApprovalDialog component in frontend/src/components/ChatWidget/ApprovalDialog.tsx
- [ ] T124 [US4] Integrate approval display into chat flow in frontend/src/components/ChatWidget/ChatWidget.tsx
- [ ] T125 [US4] Create dashboard page with pending approvals in frontend/src/app/dashboard/page.tsx

### Audit Trail

- [ ] T126 [US4] Ensure all approval actions logged in backend/services/chatbot_api/services/approval_service.py
- [ ] T127 [US4] Add resolver tracking to approval workflow in backend/services/chatbot_api/services/approval_service.py

**Checkpoint**: Disruptive actions require approval, UI displays requests, approvals/rejections are logged.

---

## Phase 8: User Story 6 - MITRE ATT&CK Mapping (Priority: P3)

**Goal**: Analyst can request MITRE mapping for alert text and receive relevant technique IDs with explanations

**Independent Test**: Provide lateral movement description → THREATINTEL-AGENT returns T1021 with explanation

### THREATINTEL Agent

- [ ] T128 [US6] Implement THREATINTEL-AGENT in backend/services/chatbot_api/agents/threatintel_agent.py
- [ ] T129 [US6] Create threatintel prompts with MITRE context in backend/services/chatbot_api/agents/prompts/threatintel.py

### MCP Tools - MITRE Mapper

- [ ] T130 [US6] Implement mitre_mapper tool in mcp/server/tools/threat_intel.py
- [ ] T131 [US6] Create MITRE ATT&CK technique database/lookup in mcp/server/tools/threat_intel.py

### Integration

- [ ] T132 [US6] Add MITRE mapping to THREATINTEL routing in backend/services/chatbot_api/agents/supervisor.py
- [ ] T133 [US6] Add MITRE technique display formatting in frontend/src/components/ChatWidget/MessageBubble.tsx

**Checkpoint**: MITRE ATT&CK mapping works, technique IDs returned with explanations.

---

## Phase 9: User Story 7 - Detection Rule Suggestions (Priority: P3)

**Goal**: Analyst can request detection rules for attack patterns with tuning recommendations

**Independent Test**: Describe attack pattern → DETECTION-ENGINEER returns rule template with tuning advice

### DETECTION-ENGINEER Agent

- [ ] T134 [US7] Implement DETECTION-ENGINEER-AGENT in backend/services/chatbot_api/agents/detection_engineer_agent.py
- [ ] T135 [US7] Create detection engineering prompts in backend/services/chatbot_api/agents/prompts/detection.py
- [ ] T136 [US7] Add detection rule templates (Sigma, YARA, Splunk) in backend/services/chatbot_api/agents/templates/

### Integration

- [ ] T137 [US7] Add detection engineering to supervisor routing in backend/services/chatbot_api/agents/supervisor.py
- [ ] T138 [US7] Add code block formatting for rules in frontend/src/components/ChatWidget/MessageBubble.tsx

**Checkpoint**: Detection rule suggestions work with templates and tuning recommendations.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Observability, deployment, security hardening, and final integration

### Observability

- [ ] T139 [P] Configure Prometheus metrics in backend/services/chatbot_api/metrics.py
- [ ] T140 [P] Configure Jaeger tracing in backend/services/chatbot_api/tracing.py
- [ ] T141 [P] Create Grafana dashboards in deploy/observability/grafana/
- [ ] T142 [P] Create Prometheus alert rules in deploy/observability/prometheus/

### Deployment

- [ ] T143 [P] Create umbrella Helm chart in deploy/helm/ai-soc-platform/Chart.yaml
- [ ] T144 [P] Create frontend Helm chart in deploy/helm/frontend/
- [ ] T145 [P] Create docs Helm chart in deploy/helm/docs/
- [ ] T146 [P] Create chatbot-api Helm chart in deploy/helm/chatbot-api/
- [ ] T147 [P] Create rag-service Helm chart in deploy/helm/rag-service/
- [ ] T148 [P] Create ingestion-service Helm chart in deploy/helm/ingestion-service/
- [ ] T149 [P] Create mcp-server Helm chart in deploy/helm/mcp-server/
- [ ] T150 Configure Dapr components in deploy/dapr/components/
- [ ] T151 Create values-local.yaml for Minikube in deploy/helm/ai-soc-platform/
- [ ] T152 Create values-prod.yaml for GKE in deploy/helm/ai-soc-platform/

### Kubernetes Security

- [ ] T153 [P] Create RBAC manifests in deploy/k8s/rbac/
- [ ] T154 [P] Create NetworkPolicy manifests in deploy/k8s/network-policies/
- [ ] T155 [P] Create PodSecurityPolicy manifests in deploy/k8s/pod-security/

### CI/CD

- [ ] T156 [P] Create CD staging workflow in .github/workflows/cd-staging.yaml
- [ ] T157 [P] Create CD production workflow in .github/workflows/cd-production.yaml
- [ ] T158 Add image scanning to CI in .github/workflows/ci.yaml
- [ ] T159 Add SBOM generation to CI in .github/workflows/ci.yaml

### Scripts

- [ ] T160 [P] Create local-dev.sh script in scripts/
- [ ] T161 [P] Create deploy-minikube.sh script in scripts/
- [ ] T162 [P] Create deploy-gke.sh script in scripts/
- [ ] T163 [P] Create run-tests.sh script in scripts/

### RAG Evaluation

- [ ] T164 Create RAG evaluation suite in backend/scripts/run_rag_eval.py
- [ ] T165 Create evaluation dataset in backend/evaluation/textbook_eval.json
- [ ] T166 Implement rag_eval_run MCP tool in mcp/server/tools/rag_knowledge.py

### Edge Cases & Error Handling

- [ ] T167 Implement Qdrant unavailable graceful degradation in backend/services/rag_service/retriever.py
- [ ] T168 Implement OpenAI rate limit backoff in backend/services/chatbot_api/agents/base.py
- [ ] T169 Implement chat history pagination in backend/services/chatbot_api/routers/chat.py
- [ ] T170 Implement MCP tool failure handling with user notification in backend/services/chatbot_api/agents/base.py

### Landing Page

- [ ] T171 [P] Create Hero component in frontend/src/components/Hero.tsx
- [ ] T172 [P] Create landing page in frontend/src/app/page.tsx

### Documentation

- [ ] T173 Update README.md with project overview
- [ ] T174 Verify quickstart.md against actual implementation

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ─────► Phase 2 (Foundational) ─────► Phase 3 (US5: Auth)
                                                            │
                                                            ▼
                                                     Phase 4 (US3: Textbook)
                                                            │
                                                            ▼
                                                     Phase 5 (US1: Triage) ──► MVP!
                                                            │
                                    ┌───────────────────────┼───────────────────────┐
                                    ▼                       ▼                       ▼
                             Phase 6 (US2)           Phase 7 (US4)           Phase 8 (US6)
                             Report Gen              Approvals               MITRE Map
                                    │                       │                       │
                                    └───────────────────────┼───────────────────────┘
                                                            │
                                                            ▼
                                                     Phase 9 (US7: Detection)
                                                            │
                                                            ▼
                                                     Phase 10 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|---------------------|
| US5 (Auth) | Foundational only | - |
| US3 (Textbook) | US5 | - |
| US1 (Triage) | US3, US5 | - |
| US2 (Reports) | US1 | US4, US6 |
| US4 (Approvals) | US1 | US2, US6 |
| US6 (MITRE) | US1 | US2, US4 |
| US7 (Detection) | US1 | - |

### Within Each Phase

- Models before services
- Services before endpoints
- Core implementation before integration
- Backend before frontend (for same feature)

---

## Parallel Opportunities

### Phase 2 Parallel Groups

```bash
# Group 1: Database Models (all independent)
T014, T015, T016, T017, T018, T019

# Group 2: Pydantic Schemas (all independent)
T021, T022, T023, T024, T025, T026

# Group 3: Frontend Foundation (all independent)
T042, T043, T044, T045
```

### Phase 5 Parallel Groups

```bash
# MCP Tools can be built in parallel:
T092, T093, T094, T095, T096, T097
```

### Phase 10 Parallel Groups

```bash
# Helm Charts (all independent)
T143, T144, T145, T146, T147, T148, T149

# K8s Security (all independent)
T153, T154, T155

# Scripts (all independent)
T160, T161, T162, T163
```

---

## Implementation Strategy

### MVP First (Phases 1-5 Only)

1. Complete Phase 1: Setup (~11 tasks)
2. Complete Phase 2: Foundational (~29 tasks)
3. Complete Phase 3: Auth US5 (~12 tasks)
4. Complete Phase 4: Textbook US3 (~24 tasks)
5. Complete Phase 5: Triage US1 (~19 tasks)
6. **STOP and VALIDATE**: Test MVP independently
7. Deploy/demo alert triage with RAG

**MVP Total**: ~95 tasks

### Incremental Delivery

After MVP:
- Add US2 (Reports): 8 tasks
- Add US4 (Approvals): 16 tasks
- Add US6 (MITRE): 6 tasks
- Add US7 (Detection): 5 tasks
- Complete Polish: 36 tasks

**Full Platform Total**: 174 tasks

### Suggested Sprint Plan

| Sprint | Focus | Tasks |
|--------|-------|-------|
| 1 | Setup + Foundation | T001-T048 |
| 2 | Auth + Textbook Base | T049-T084 |
| 3 | Triage MVP | T085-T103 |
| 4 | Reports + Approvals | T104-T127 |
| 5 | MITRE + Detection | T128-T138 |
| 6 | Polish + Deploy | T139-T174 |

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 174 |
| **Phase 1 (Setup)** | 11 |
| **Phase 2 (Foundational)** | 37 |
| **Phase 3 (US5: Auth)** | 12 |
| **Phase 4 (US3: Textbook)** | 24 |
| **Phase 5 (US1: Triage)** | 19 |
| **Phase 6 (US2: Reports)** | 8 |
| **Phase 7 (US4: Approvals)** | 16 |
| **Phase 8 (US6: MITRE)** | 6 |
| **Phase 9 (US7: Detection)** | 5 |
| **Phase 10 (Polish)** | 36 |
| **MVP Tasks (to US1)** | 95 |
| **Parallel Opportunities** | 67 tasks marked [P] |

---

## Notes

- [P] tasks = different files, no dependencies within same phase
- [USx] label maps task to specific user story for traceability
- Each phase checkpoint allows independent validation
- Commit after each task or logical group
- US5 (Auth) is P2 but implemented first as prerequisite
- MVP stops at Phase 5 (US1: Alert Triage)
