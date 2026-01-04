# Data Model: AI-SOC SecOps Agents Platform

**Branch**: `1-ai-soc-platform` | **Date**: 2026-01-04 | **Phase**: 1
**Input**: [plan.md](./plan.md) | [research.md](./research.md)

---

## Overview

This document defines the database schemas for both relational (Neon Postgres) and vector (Qdrant) storage systems.

---

## Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│    User     │────<│   Session   │────<│  ChatMessage    │
└─────────────┘     └─────────────┘     └─────────────────┘
      │                                          │
      │                                          │
      ▼                                          ▼
┌─────────────────┐                    ┌─────────────────┐
│   AuditLog      │                    │   AgentRun      │
└─────────────────┘                    └─────────────────┘
      │
      │
      ▼
┌─────────────────┐
│ ApprovalRequest │
└─────────────────┘

┌─────────────────┐
│ TextbookChunk   │  (Qdrant - Vector DB)
└─────────────────┘
```

---

## Neon Postgres Schemas

### 1. Users Table

Stores authenticated user accounts.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'analyst',
    display_name VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT true,
    email_verified BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMPTZ,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMPTZ,

    CONSTRAINT valid_role CHECK (role IN ('admin', 'senior_analyst', 'analyst', 'viewer'))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;

COMMENT ON TABLE users IS 'User accounts for authentication and authorization';
COMMENT ON COLUMN users.role IS 'User role: admin, senior_analyst, analyst, viewer';
COMMENT ON COLUMN users.locked_until IS 'Account locked until this time after failed login attempts';
```

**Pydantic Model**:
```python
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    SENIOR_ANALYST = "senior_analyst"
    ANALYST = "analyst"
    VIEWER = "viewer"

class User(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    display_name: str | None
    is_active: bool
    email_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None

    class Config:
        from_attributes = True
```

---

### 2. Sessions Table

Manages user authentication sessions.

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    user_agent TEXT,
    ip_address INET,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    last_activity_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT session_not_expired CHECK (expires_at > created_at)
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON sessions(token_hash);
CREATE INDEX idx_sessions_expires ON sessions(expires_at) WHERE revoked_at IS NULL;

COMMENT ON TABLE sessions IS 'Active user sessions with JWT token tracking';
COMMENT ON COLUMN sessions.token_hash IS 'SHA256 hash of JWT token for revocation lookup';
```

**Pydantic Model**:
```python
class Session(BaseModel):
    id: UUID
    user_id: UUID
    user_agent: str | None
    ip_address: str | None
    created_at: datetime
    expires_at: datetime
    revoked_at: datetime | None
    last_activity_at: datetime

    @property
    def is_valid(self) -> bool:
        return (
            self.revoked_at is None and
            self.expires_at > datetime.utcnow()
        )

    class Config:
        from_attributes = True
```

---

### 3. ChatMessages Table

Stores conversation history with agent context.

```sql
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    agent_name VARCHAR(50),
    citations JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    tokens_used INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT valid_role CHECK (role IN ('user', 'assistant', 'system')),
    CONSTRAINT valid_agent CHECK (
        role != 'assistant' OR agent_name IS NOT NULL
    )
);

CREATE INDEX idx_chat_messages_session ON chat_messages(session_id, created_at);
CREATE INDEX idx_chat_messages_agent ON chat_messages(agent_name) WHERE agent_name IS NOT NULL;
CREATE INDEX idx_chat_messages_created ON chat_messages(created_at);

COMMENT ON TABLE chat_messages IS 'Chat conversation history with agent attribution';
COMMENT ON COLUMN chat_messages.citations IS 'Array of source citations [{page, chunk_id, relevance}]';
COMMENT ON COLUMN chat_messages.agent_name IS 'Name of responding agent (SUPERVISOR, TRIAGE, etc.)';
```

**Pydantic Model**:
```python
class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Citation(BaseModel):
    page: str
    chunk_id: str
    relevance: float
    snippet: str | None = None

class ChatMessage(BaseModel):
    id: UUID
    session_id: UUID
    role: MessageRole
    content: str
    agent_name: str | None
    citations: list[Citation]
    metadata: dict
    tokens_used: int | None
    created_at: datetime

    class Config:
        from_attributes = True
```

---

### 4. AuditLogs Table

Tracks all significant actions for compliance and security.

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    session_id UUID REFERENCES sessions(id) ON DELETE SET NULL,
    action_type VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    tool_name VARCHAR(100),
    inputs JSONB,
    outputs JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'success',
    error_message TEXT,
    ip_address INET,
    user_agent TEXT,
    request_id UUID,
    trace_id VARCHAR(64),
    latency_ms INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT valid_status CHECK (status IN ('success', 'error', 'pending'))
);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id, created_at);
CREATE INDEX idx_audit_logs_action ON audit_logs(action_type, created_at);
CREATE INDEX idx_audit_logs_tool ON audit_logs(tool_name) WHERE tool_name IS NOT NULL;
CREATE INDEX idx_audit_logs_request ON audit_logs(request_id) WHERE request_id IS NOT NULL;
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

-- Partition by month for performance
CREATE TABLE audit_logs_2026_01 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

COMMENT ON TABLE audit_logs IS 'Comprehensive audit trail for all system actions';
COMMENT ON COLUMN audit_logs.trace_id IS 'Distributed tracing ID for cross-service correlation';
```

**Pydantic Model**:
```python
class AuditStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"

class AuditLog(BaseModel):
    id: UUID
    user_id: UUID | None
    session_id: UUID | None
    action_type: str
    resource_type: str | None
    resource_id: str | None
    tool_name: str | None
    inputs: dict | None
    outputs: dict | None
    status: AuditStatus
    error_message: str | None
    ip_address: str | None
    request_id: UUID | None
    trace_id: str | None
    latency_ms: int | None
    created_at: datetime

    class Config:
        from_attributes = True
```

---

### 5. ApprovalRequests Table

Manages human-in-the-loop approval workflow.

```sql
CREATE TABLE approval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requester_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    agent_name VARCHAR(50) NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    params JSONB NOT NULL,
    risk_assessment VARCHAR(20) NOT NULL,
    reason TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    resolver_id UUID REFERENCES users(id) ON DELETE SET NULL,
    resolution_reason TEXT,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,

    CONSTRAINT valid_status CHECK (status IN ('pending', 'approved', 'rejected', 'expired', 'executed')),
    CONSTRAINT valid_risk CHECK (risk_assessment IN ('low', 'medium', 'high', 'critical')),
    CONSTRAINT resolver_required CHECK (
        status = 'pending' OR status = 'expired' OR resolver_id IS NOT NULL
    )
);

CREATE INDEX idx_approvals_requester ON approval_requests(requester_id);
CREATE INDEX idx_approvals_status ON approval_requests(status) WHERE status = 'pending';
CREATE INDEX idx_approvals_expires ON approval_requests(expires_at) WHERE status = 'pending';

COMMENT ON TABLE approval_requests IS 'Human approval workflow for disruptive actions';
COMMENT ON COLUMN approval_requests.action_type IS 'Action type: disable_user, isolate_host, block_ioc';
COMMENT ON COLUMN approval_requests.expires_at IS 'Request expires after 24 hours if not acted upon';
```

**Pydantic Model**:
```python
class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    EXECUTED = "executed"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ApprovalRequest(BaseModel):
    id: UUID
    requester_id: UUID
    agent_name: str
    action_type: str
    params: dict
    risk_assessment: RiskLevel
    reason: str | None
    status: ApprovalStatus
    resolver_id: UUID | None
    resolution_reason: str | None
    expires_at: datetime
    created_at: datetime
    resolved_at: datetime | None

    @property
    def is_pending(self) -> bool:
        return self.status == ApprovalStatus.PENDING

    @property
    def is_expired(self) -> bool:
        return (
            self.status == ApprovalStatus.PENDING and
            self.expires_at < datetime.utcnow()
        )

    class Config:
        from_attributes = True
```

---

### 6. AgentRuns Table

Tracks agent execution for observability and cost tracking.

```sql
CREATE TABLE agent_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE SET NULL,
    message_id UUID REFERENCES chat_messages(id) ON DELETE SET NULL,
    agent_name VARCHAR(50) NOT NULL,
    parent_run_id UUID REFERENCES agent_runs(id) ON DELETE SET NULL,
    input_text TEXT NOT NULL,
    output_text TEXT,
    tools_called JSONB DEFAULT '[]'::jsonb,
    model_name VARCHAR(50),
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    latency_ms INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'running',
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,

    CONSTRAINT valid_status CHECK (status IN ('running', 'completed', 'failed', 'cancelled')),
    CONSTRAINT tokens_sum CHECK (
        total_tokens IS NULL OR
        total_tokens = COALESCE(prompt_tokens, 0) + COALESCE(completion_tokens, 0)
    )
);

CREATE INDEX idx_agent_runs_session ON agent_runs(session_id, created_at);
CREATE INDEX idx_agent_runs_agent ON agent_runs(agent_name, created_at);
CREATE INDEX idx_agent_runs_parent ON agent_runs(parent_run_id) WHERE parent_run_id IS NOT NULL;
CREATE INDEX idx_agent_runs_status ON agent_runs(status) WHERE status = 'running';

COMMENT ON TABLE agent_runs IS 'Agent execution tracking for observability and cost analysis';
COMMENT ON COLUMN agent_runs.parent_run_id IS 'Links sub-agent runs to supervisor run';
COMMENT ON COLUMN agent_runs.tools_called IS 'Array of tool calls [{name, inputs, outputs, latency_ms}]';
```

**Pydantic Model**:
```python
class RunStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ToolCall(BaseModel):
    name: str
    inputs: dict
    outputs: dict | None
    latency_ms: int | None
    status: str

class AgentRun(BaseModel):
    id: UUID
    session_id: UUID | None
    message_id: UUID | None
    agent_name: str
    parent_run_id: UUID | None
    input_text: str
    output_text: str | None
    tools_called: list[ToolCall]
    model_name: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    latency_ms: int | None
    status: RunStatus
    error_message: str | None
    metadata: dict
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True
```

---

## Qdrant Vector Schemas

### 7. TextbookChunks Collection

Stores embedded textbook content for RAG retrieval.

**Collection Configuration**:
```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PayloadSchemaType,
    TextIndexParams, TokenizerType
)

TEXTBOOK_CHUNKS_CONFIG = {
    "collection_name": "textbook_chunks",
    "vectors_config": VectorParams(
        size=1536,  # text-embedding-3-small dimensions
        distance=Distance.COSINE
    ),
    "payload_schema": {
        "source_page": PayloadSchemaType.KEYWORD,
        "module": PayloadSchemaType.KEYWORD,
        "chapter": PayloadSchemaType.KEYWORD,
        "section": PayloadSchemaType.KEYWORD,
        "chunk_index": PayloadSchemaType.INTEGER,
        "content": PayloadSchemaType.TEXT,
        "title": PayloadSchemaType.TEXT,
        "difficulty": PayloadSchemaType.KEYWORD,
        "prerequisites": PayloadSchemaType.KEYWORD,  # array
        "word_count": PayloadSchemaType.INTEGER,
        "created_at": PayloadSchemaType.DATETIME,
        "updated_at": PayloadSchemaType.DATETIME,
    }
}

# Create text index for full-text search fallback
TEXT_INDEX_CONFIG = TextIndexParams(
    type="text",
    tokenizer=TokenizerType.WORD,
    min_token_len=2,
    max_token_len=20,
    lowercase=True
)
```

**Chunk Schema**:
```python
class TextbookChunk(BaseModel):
    """Represents a chunk of textbook content in Qdrant"""

    id: str  # Format: {module}-{chapter}-{section}-{chunk_index}
    vector: list[float]  # 1536 dimensions

    # Payload fields
    source_page: str      # e.g., "/module-1/chapter-3/siem-basics"
    module: str           # e.g., "module-1-soc-foundations"
    chapter: str          # e.g., "chapter-3-siem-fundamentals"
    section: str | None   # e.g., "correlation-rules"
    chunk_index: int      # Position within page (0-indexed)
    content: str          # Raw text content
    title: str            # Section/chunk title
    difficulty: str       # "beginner", "intermediate", "advanced"
    prerequisites: list[str]  # List of prerequisite chunks
    word_count: int
    created_at: datetime
    updated_at: datetime

    def to_qdrant_point(self):
        return {
            "id": self.id,
            "vector": self.vector,
            "payload": {
                "source_page": self.source_page,
                "module": self.module,
                "chapter": self.chapter,
                "section": self.section,
                "chunk_index": self.chunk_index,
                "content": self.content,
                "title": self.title,
                "difficulty": self.difficulty,
                "prerequisites": self.prerequisites,
                "word_count": self.word_count,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat(),
            }
        }
```

**Retrieval Examples**:
```python
# Basic semantic search
async def search_chunks(query: str, limit: int = 5) -> list[TextbookChunk]:
    query_vector = await embeddings.embed(query)
    results = client.search(
        collection_name="textbook_chunks",
        query_vector=query_vector,
        limit=limit,
        with_payload=True
    )
    return [TextbookChunk.from_qdrant(r) for r in results]

# Filtered search (specific module)
async def search_in_module(query: str, module: str) -> list[TextbookChunk]:
    query_vector = await embeddings.embed(query)
    results = client.search(
        collection_name="textbook_chunks",
        query_vector=query_vector,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="module",
                    match=models.MatchValue(value=module)
                )
            ]
        ),
        limit=5,
        with_payload=True
    )
    return [TextbookChunk.from_qdrant(r) for r in results]

# Context-aware search (prioritize current page)
async def search_with_context(
    query: str,
    current_page: str,
    selected_text: str | None = None
) -> list[TextbookChunk]:
    # If text is selected, boost its context
    search_query = f"{selected_text} {query}" if selected_text else query
    query_vector = await embeddings.embed(search_query)

    # First: search current page
    page_results = client.search(
        collection_name="textbook_chunks",
        query_vector=query_vector,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="source_page",
                    match=models.MatchValue(value=current_page)
                )
            ]
        ),
        limit=3,
        with_payload=True
    )

    # Second: search entire textbook
    global_results = client.search(
        collection_name="textbook_chunks",
        query_vector=query_vector,
        limit=5,
        with_payload=True
    )

    # Merge and deduplicate, prioritizing page results
    return merge_results(page_results, global_results)
```

---

## Database Migrations

### Alembic Configuration

```python
# alembic/env.py
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

async def run_migrations_online():
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url")
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

# alembic/versions/001_initial_schema.py
def upgrade():
    # Create all tables in order
    op.create_table("users", ...)
    op.create_table("sessions", ...)
    op.create_table("chat_messages", ...)
    op.create_table("audit_logs", ...)
    op.create_table("approval_requests", ...)
    op.create_table("agent_runs", ...)

def downgrade():
    # Drop in reverse order
    op.drop_table("agent_runs")
    op.drop_table("approval_requests")
    op.drop_table("audit_logs")
    op.drop_table("chat_messages")
    op.drop_table("sessions")
    op.drop_table("users")
```

---

## Data Retention Policy

| Table | Retention | Action |
|-------|-----------|--------|
| users | Indefinite | Manual deletion only |
| sessions | 30 days after expiry | Auto-purge |
| chat_messages | 90 days | Archive then delete |
| audit_logs | 1 year | Archive to cold storage |
| approval_requests | 1 year | Archive to cold storage |
| agent_runs | 90 days | Archive then delete |
| textbook_chunks | Indefinite | Versioned updates |

**Cleanup Job**:
```sql
-- Run daily via pg_cron or external scheduler
DELETE FROM sessions
WHERE expires_at < NOW() - INTERVAL '30 days';

DELETE FROM chat_messages
WHERE created_at < NOW() - INTERVAL '90 days';

-- Archive before delete
INSERT INTO audit_logs_archive
SELECT * FROM audit_logs
WHERE created_at < NOW() - INTERVAL '1 year';

DELETE FROM audit_logs
WHERE created_at < NOW() - INTERVAL '1 year';
```

---

## Indexes Summary

| Table | Index | Purpose |
|-------|-------|---------|
| users | email | Login lookup |
| users | role | RBAC filtering |
| sessions | user_id | User session list |
| sessions | token_hash | Token validation |
| chat_messages | session_id, created_at | Conversation history |
| audit_logs | user_id, created_at | User activity |
| audit_logs | action_type, created_at | Action analysis |
| audit_logs | request_id | Request tracing |
| approval_requests | status | Pending approvals |
| agent_runs | agent_name, created_at | Agent analytics |

---

## Next Steps

1. Create API contracts in `contracts/` directory
2. Create `quickstart.md` for local development
3. Generate implementation tasks via `/sp.tasks`
