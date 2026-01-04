<!--
SYNC IMPACT REPORT
==================
Version Change: 0.0.0 → 1.0.0 (MAJOR - Initial constitution creation)

Modified Principles: N/A (Initial creation)

Added Sections:
- 10 Core Principles for AI-SOC development
- Security & Compliance Requirements
- Development Workflow
- Governance Rules

Removed Sections: N/A

Templates Requiring Updates:
- .specify/templates/plan-template.md: ✅ Compatible
- .specify/templates/spec-template.md: ✅ Compatible
- .specify/templates/tasks-template.md: ✅ Compatible

Follow-up TODOs: None
-->

# AI-SOC / SecOps Agents Constitution

> **One-line Goal**: AI is no longer limited to the computer screen - it now works as an agent inside SOC/SecOps to investigate, decide, and safely respond to security incidents.

## Core Principles

### I. Security-First Design (NON-NEGOTIABLE)

All agent actions MUST be safe by default. Security is not an afterthought but the foundation:

- **Guardrails**: Allow-list tool calls only; no arbitrary command execution
- **Approval Gates**: Disruptive actions (isolate host, disable user, block IOC) MUST require human approval
- **Audit Logging**: Every agent action, decision, and tool call MUST be logged to Neon Postgres
- **Least Privilege**: Agents operate with minimal required permissions; no privileged containers

**Rationale**: AI agents in SOC environments can cause significant damage if unconstrained. Defense-in-depth ensures no single failure leads to catastrophic outcomes.

### II. Grounded Responses (RAG Mandatory)

All AI responses MUST be grounded in verified sources:

- Answers MUST cite retrieved chunks from Qdrant vector store
- Responses MUST stay within textbook and playbook boundaries
- Hallucination control via confidence thresholds and refusal rules
- Selected-text priority: when user highlights text, agent explains that selection first

**Rationale**: In cybersecurity, inaccurate information can lead to missed threats or false positives. Grounding ensures reliability.

### III. Microservices Architecture (REQUIRED)

The system MUST be decomposed into independent, containerized services:

- **Book Site Service**: Docusaurus hosting textbook + embedded chatbot widget
- **Chatbot API Service**: FastAPI orchestrating agent responses via OpenAI SDK
- **Ingestion/Embedding Service**: Converts content to embeddings, stores in Qdrant
- **Identity/Session/Audit Service**: Auth, sessions, chat history in Neon Postgres
- **Observability Stack**: Centralized logs/metrics/traces with dashboards

**Rationale**: Microservices enable independent scaling, deployment, and failure isolation critical for production SOC systems.

### IV. Kubernetes-Native Deployment (REQUIRED)

All services MUST be deployable on Kubernetes:

- Docker images for every microservice
- Helm charts for packaging and deployment
- Minikube for local development and testing
- Dapr runtime for service invocation, pub/sub, secrets, resiliency
- GKE as primary cloud target

**Rationale**: Industry-standard container orchestration ensures portability, scalability, and operational maturity.

### V. Observability & SLO-Driven Operations (REQUIRED)

Production systems MUST have comprehensive observability:

- Logs, metrics, traces correlated by request/trace ID across all services
- Dashboards for latency, error rate, throughput, dependency health
- SLO-style alerting: error budget burn, high latency (p95), elevated 5xx, queue backlogs
- Centralized logging with structured JSON format

**Rationale**: SOC systems require real-time visibility into agent behavior and system health for incident response.

### VI. CI/CD Pipeline (REQUIRED)

Automated pipelines MUST gate all deployments:

- Pipeline stages: build → test → docker push → helm deploy
- Environment separation: dev/staging/prod (minimum dev + prod)
- Image scanning in CI; fail on critical vulnerabilities
- SBOM generation for every release
- Dependency vulnerability scanning with lockfiles

**Rationale**: Automated quality gates prevent security issues and ensure consistent deployments.

### VII. Test-First Development (NON-NEGOTIABLE)

TDD is mandatory for all agent logic and security-critical code:

- Tests written → Tests fail → Implementation → Tests pass → Refactor
- RAG evaluation suite with retrieval metrics (hit rate, recall)
- Grounded-answer checks ensuring citations match sources
- Integration tests for service contracts and inter-service communication

**Rationale**: Security systems require verified behavior; untested code is untrustworthy code.

### VIII. Human-in-the-Loop Operations (NON-NEGOTIABLE)

Humans MUST remain in control of critical decisions:

- Approval gates before disruptive actions execute
- Clear escalation paths for ambiguous situations
- Executive summaries for non-technical stakeholders
- Audit trail enabling post-incident review

**Rationale**: AI assists SOC analysts; it does not replace human judgment for high-impact decisions.

### IX. Cost & Rate Controls (REQUIRED)

Production systems MUST implement cost protection:

- Request rate limits per user/session
- Token budgets: per-request caps and monthly monitoring
- Caching for repeated retrieval results and safe responses
- Resource quotas in Kubernetes

**Rationale**: LLM APIs are expensive; uncontrolled usage leads to budget overruns and potential DoS.

### X. Supply-Chain Security (REQUIRED)

All dependencies and images MUST be secured:

- Image scanning in CI pipeline (fail on critical CVEs)
- SBOM generation for all releases
- Dependency lockfiles with vulnerability scanning
- Base image updates on security advisory schedule

**Rationale**: Supply-chain attacks are a growing threat vector; proactive scanning prevents compromise.

## Security & Compliance Requirements

### Kubernetes Security Hardening

- **RBAC**: Least-privilege roles and service accounts for all workloads
- **NetworkPolicies**: Restrict east-west traffic; explicit allow-lists only
- **Pod Security**: Baseline/restricted posture; no privileged containers
- **Secrets**: Encrypted at rest, rotated regularly, accessed via Dapr secrets API

### Data Protection

- **Neon Postgres**: Encrypted connections, row-level security where applicable
- **Qdrant**: Access controlled, embeddings isolated per tenant if multi-tenant
- **Audit Logs**: Immutable, retained per compliance requirements
- **PII Handling**: Minimize collection, mask in logs, encrypt at rest

### Agent Safety Controls

- **Tool Allow-List**: Only pre-approved tools callable by agents
- **Policy Engine**: Runtime policy checks before tool execution
- **Sandboxing**: Tools execute in isolated environments
- **Kill Switch**: Ability to immediately disable agent actions

## Development Workflow

### Feature Development Cycle

1. **Spec**: Write feature specification with acceptance criteria
2. **Plan**: Create implementation plan with architecture decisions
3. **Tasks**: Break down into testable task units
4. **Red**: Write failing tests first
5. **Green**: Implement until tests pass
6. **Refactor**: Clean up while maintaining green tests
7. **Review**: PR with constitution compliance check
8. **Deploy**: CI/CD pipeline to staging → production

### Code Quality Gates

- All PRs require passing tests and security scans
- Constitution compliance verified in review checklist
- Documentation updated with code changes
- ADRs created for significant architectural decisions

### Incident Response Integration

- Runbooks documented for common operational scenarios
- On-call procedures defined with escalation paths
- Post-incident reviews required for production issues
- Lessons learned fed back into agent training data

## Governance

### Constitution Authority

This constitution supersedes all other project practices and guidelines. When conflicts arise:

1. Constitution principles take precedence
2. Security requirements are non-negotiable
3. Deviations require documented ADR with justification

### Amendment Process

1. Propose change via PR to constitution file
2. Document rationale and impact assessment
3. Review by project maintainers
4. Update dependent templates if affected
5. Increment version per semantic versioning:
   - MAJOR: Principle removal or redefinition
   - MINOR: New principle or section added
   - PATCH: Clarifications and typo fixes

### Compliance Verification

- All PRs MUST include constitution compliance checklist
- Quarterly reviews of security controls
- Annual architecture review against principles
- Continuous monitoring of SLO compliance

### Runtime Guidance

For day-to-day development guidance, refer to:
- `CLAUDE.md` for agent-specific instructions
- `README.md` for project overview and setup
- `.specify/templates/` for spec/plan/task templates

**Version**: 1.0.0 | **Ratified**: 2026-01-04 | **Last Amended**: 2026-01-04
