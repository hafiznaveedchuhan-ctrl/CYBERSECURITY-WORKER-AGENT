# Feature Specification: AI-SOC SecOps Agents Platform

**Feature Branch**: `1-ai-soc-platform`
**Created**: 2026-01-04
**Status**: Draft
**Input**: Production-grade AI-SOC system with Docusaurus textbook, RAG chatbot, MCP tools, and domain sub-agents

---

## Executive Summary

Build a production-grade full-stack AI-SOC (Security Operations Center) platform that:
1. Publishes an AI-native textbook site for "AI-SOC / SecOps Agents" using Docusaurus
2. Embeds a stylish RAG chatbot widget inside the book UI with agent name badges
3. Uses domain sub-agents (AI employees) for specialized security tasks
4. Provides reusable MCP tools for security operations
5. Deploys on Kubernetes with enterprise-grade observability and security

---

## User Scenarios & Testing

### User Story 1 - SOC Analyst Alert Triage (Priority: P1)

A SOC L1 analyst receives a security alert and needs immediate context, severity assessment, and recommended next steps without manually searching through logs and documentation.

**Why this priority**: Core value proposition - reducing alert fatigue and mean-time-to-triage (MTTT) is the primary goal of the AI-SOC system.

**Independent Test**: Can be tested by pasting an alert into the chat widget and verifying the agent returns severity, rationale, and actionable next steps within 30 seconds.

**Acceptance Scenarios**:

1. **Given** a logged-in SOC analyst on the textbook page, **When** they paste a phishing alert into the chat widget, **Then** TRIAGE-AGENT responds with severity level (Critical/High/Medium/Low), clear rationale citing relevant textbook sections, and 3-5 specific next steps.

2. **Given** a security alert with IP indicators, **When** the analyst requests enrichment, **Then** ENRICHMENT-AGENT provides IP reputation, GeoIP context, and historical activity summary with risk score.

3. **Given** an ambiguous alert, **When** the analyst asks clarifying questions, **Then** the system asks targeted questions to gather more context before providing assessment.

---

### User Story 2 - Incident Report Generation (Priority: P1)

After investigating an incident, the analyst needs to generate a professional incident report with timeline, findings, impact, remediation, and prevention recommendations.

**Why this priority**: Reduces documentation burden and ensures consistent, high-quality reports across the team.

**Independent Test**: Can be tested by requesting a report for a case and verifying the output contains all required sections with accurate information.

**Acceptance Scenarios**:

1. **Given** a case with notes and evidence, **When** the analyst requests "generate incident report", **Then** REPORT-WRITER-AGENT produces a structured report with executive summary, timeline, technical findings, business impact, remediation steps, and prevention recommendations.

2. **Given** a generated report, **When** the analyst reviews it, **Then** all facts are grounded in case data and textbook citations are included for methodology references.

---

### User Story 3 - Interactive Textbook Learning (Priority: P2)

Students and analysts learning SOC operations can highlight text in the textbook and ask the AI to explain concepts in more detail.

**Why this priority**: Enables self-paced learning and reduces training time for new SOC team members.

**Independent Test**: Can be tested by highlighting text on any textbook page and asking "explain this" - the response should prioritize the selected text.

**Acceptance Scenarios**:

1. **Given** a user reading Module 1 Chapter 3 (SIEM fundamentals), **When** they highlight "correlation rules" and click "Ask AI", **Then** the chatbot explains correlation rules with examples from the textbook, prioritizing the selected text context.

2. **Given** a user asking a question without selected text, **When** they type "What is an IOC?", **Then** the system retrieves relevant textbook sections and provides a grounded answer with citations.

---

### User Story 4 - Human-Approved Response Actions (Priority: P2)

For disruptive actions (disable user, isolate host, block IOC), the system must request and wait for human approval before execution.

**Why this priority**: Critical for safety - AI agents must not autonomously execute high-impact actions.

**Independent Test**: Can be tested by triggering a "disable user" recommendation and verifying the approval UI appears and blocks execution until approved.

**Acceptance Scenarios**:

1. **Given** INCIDENT-COMMANDER recommends "disable compromised user account", **When** the recommendation is generated, **Then** an approval request appears in the UI with action details, risk assessment, and Approve/Reject buttons.

2. **Given** an approval request, **When** a senior analyst clicks "Approve", **Then** the action is logged to audit trail and executed, with confirmation displayed.

3. **Given** an approval request, **When** a user clicks "Reject", **Then** the action is not executed and the rejection is logged with optional reason.

---

### User Story 5 - User Authentication and Session Management (Priority: P2)

Users must be able to sign up, log in, and maintain persistent chat sessions across visits.

**Why this priority**: Foundation for personalization, audit trails, and rate limiting.

**Independent Test**: Can be tested by signing up, logging out, logging back in, and verifying chat history is preserved.

**Acceptance Scenarios**:

1. **Given** a new user, **When** they complete signup with email and password, **Then** an account is created and they are automatically logged in.

2. **Given** a logged-in user with chat history, **When** they close and reopen the browser, **Then** their session persists and chat history is accessible.

3. **Given** invalid credentials, **When** a user attempts login, **Then** a clear error message is displayed without revealing whether email or password was incorrect.

---

### User Story 6 - MITRE ATT&CK Mapping (Priority: P3)

Analysts can request TTP (Tactics, Techniques, Procedures) mapping for alert data to understand attacker behavior.

**Why this priority**: Enhances investigation quality by connecting alerts to known attack patterns.

**Independent Test**: Can be tested by providing alert text and verifying MITRE technique IDs and descriptions are returned.

**Acceptance Scenarios**:

1. **Given** alert text describing lateral movement behavior, **When** the analyst asks "map this to MITRE", **Then** THREATINTEL-AGENT returns relevant MITRE ATT&CK techniques (e.g., T1021 - Remote Services) with explanations.

---

### User Story 7 - Detection Rule Suggestions (Priority: P3)

Based on observed attack patterns, analysts can request detection rule suggestions to improve monitoring.

**Why this priority**: Proactive improvement of detection capabilities reduces future incident impact.

**Independent Test**: Can be tested by describing an attack pattern and verifying a detection rule template is returned.

**Acceptance Scenarios**:

1. **Given** an investigated incident pattern, **When** the analyst asks "suggest detection rules", **Then** DETECTION-ENGINEER-AGENT provides rule templates with tuning recommendations and expected false positive rates.

---

### Edge Cases

- What happens when Qdrant is unavailable? System should gracefully degrade with message "Knowledge base temporarily unavailable - responses may be less comprehensive."
- What happens when OpenAI API rate limit is hit? Display friendly message and implement exponential backoff.
- What happens when a user highlights non-text elements (images)? Ignore the selection gracefully.
- What happens when chat history exceeds 100 messages? Implement pagination and summary of older messages.
- What happens when MCP tool call fails? Log error, notify user, and suggest retry or manual fallback.
- What happens when approval request times out? After 24 hours, expire the request and notify the requester.

---

## Requirements

### Functional Requirements

#### Authentication & Session

- **FR-001**: System MUST allow users to create accounts with email and password
- **FR-002**: System MUST validate email format and password strength (minimum 8 characters, 1 uppercase, 1 number)
- **FR-003**: System MUST maintain authenticated sessions using secure tokens
- **FR-004**: System MUST allow users to log out and invalidate their session
- **FR-005**: System MUST persist chat history per user session

#### Textbook & Documentation

- **FR-006**: System MUST serve textbook content via Docusaurus with clean navigation
- **FR-007**: System MUST support sidebar navigation, search, and next/previous chapter links
- **FR-008**: System MUST embed the chat widget on all documentation pages
- **FR-009**: System MUST detect user-selected text and pass it as context to the chatbot

#### Chat & AI Agents

- **FR-010**: System MUST route user messages through a SUPERVISOR agent
- **FR-011**: System MUST delegate specialized tasks to domain sub-agents (TRIAGE, ENRICHMENT, THREATINTEL, DETECTION-ENGINEER, INCIDENT-COMMANDER, REPORT-WRITER)
- **FR-012**: System MUST retrieve relevant textbook chunks via RAG before generating responses
- **FR-013**: System MUST include citations with source page references in responses
- **FR-014**: System MUST display agent name badges (e.g., "TRIAGE-AGENT") in the chat UI
- **FR-015**: System MUST implement confidence thresholds - low confidence responses must acknowledge uncertainty

#### MCP Tools

- **FR-016**: System MUST expose MCP tools with strict JSON input/output schemas
- **FR-017**: System MUST log all tool calls to audit_logs table (caller, tool, inputs, outputs, timestamp)
- **FR-018**: System MUST enforce tool allow-lists per agent
- **FR-019**: System MUST require human approval for disruptive tools (disable_user, isolate_host, block_ioc)
- **FR-020**: System MUST provide approval UI with action details and Approve/Reject buttons

#### Data Persistence

- **FR-021**: System MUST store user accounts in Neon Postgres
- **FR-022**: System MUST store chat messages with session references
- **FR-023**: System MUST store approval requests and their status
- **FR-024**: System MUST store agent run logs for observability
- **FR-025**: System MUST index textbook chunks in Qdrant with embeddings

#### Security

- **FR-026**: System MUST implement rate limiting per user (configurable, default 60 requests/minute)
- **FR-027**: System MUST validate all tool inputs against schemas before execution
- **FR-028**: System MUST sanitize user inputs to prevent prompt injection
- **FR-029**: System MUST encrypt sensitive data at rest and in transit
- **FR-030**: System MUST implement RBAC for administrative functions

#### Observability

- **FR-031**: System MUST emit structured logs with request_id and trace_id
- **FR-032**: System MUST expose metrics (latency, error rate, throughput) per service
- **FR-033**: System MUST implement distributed tracing across microservices
- **FR-034**: System MUST provide dashboards for key metrics
- **FR-035**: System MUST alert on SLO violations (error rate > 1%, p95 latency > 2s)

---

### Key Entities

- **User**: Represents an authenticated user with email, hashed password, role, created_at, last_login
- **Session**: Represents an active user session with user_id, token, created_at, expires_at
- **ChatMessage**: Represents a message in conversation with session_id, role (user/assistant/system), content, agent_name, citations, timestamp
- **AuditLog**: Records all significant actions with user_id, action_type, tool_name, inputs, outputs, timestamp, status
- **ApprovalRequest**: Tracks pending approvals with request_id, action_type, params, requester_id, status (pending/approved/rejected/expired), created_at, resolved_at, resolver_id
- **AgentRun**: Tracks agent executions with run_id, agent_name, input, output, tools_called, tokens_used, latency_ms, timestamp
- **TextbookChunk**: Represents indexed content with chunk_id, source_page, content, embedding_vector, metadata

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can complete alert triage (paste alert → receive assessment) in under 30 seconds
- **SC-002**: System handles 100 concurrent users without degradation (p95 latency < 2 seconds)
- **SC-003**: RAG retrieval returns relevant results for 90% of queries (measured via evaluation suite)
- **SC-004**: 95% of responses include at least one textbook citation when answering book-related questions
- **SC-005**: Approval workflow completes (request → approval → execution) in under 5 clicks
- **SC-006**: New users can sign up and send first message in under 2 minutes
- **SC-007**: System maintains 99.5% uptime during business hours
- **SC-008**: Mean time to generate incident report is under 60 seconds
- **SC-009**: All disruptive actions are logged with 100% completeness in audit trail
- **SC-010**: Chat widget loads and is interactive within 3 seconds on documentation pages

---

## Assumptions

1. Users have modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
2. Users have stable internet connectivity
3. OpenAI API is available with sufficient quota
4. Neon Postgres and Qdrant services are provisioned and accessible
5. Textbook content is available in Markdown format for ingestion
6. Users are familiar with basic SOC terminology
7. English is the primary interface language
8. Standard OAuth2/session-based authentication is acceptable
9. Industry-standard data retention (90 days for logs, 1 year for audit trails) applies
10. GKE is the target production environment

---

## Dependencies

1. OpenAI API access with sufficient credits
2. Neon Postgres database instance
3. Qdrant vector database instance
4. GitHub repository with CI/CD capabilities
5. Docker Hub or container registry access
6. Kubernetes cluster (Minikube for local, GKE for production)
7. Domain name for production deployment (optional for MVP)

---

## Out of Scope

1. Mobile native applications (web responsive only)
2. Multi-language support (English only for MVP)
3. Custom LLM fine-tuning
4. Integration with external SIEM/SOAR platforms (future roadmap)
5. Real-time log ingestion from production environments
6. Two-factor authentication (future enhancement)
7. Team/organization management features
8. Billing/subscription management
