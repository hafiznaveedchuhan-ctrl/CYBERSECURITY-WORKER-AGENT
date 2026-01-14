---
name: backend-services-architect
description: |
  Use when designing FastAPI CRUD operations with validation and error handling, architecting microservices with service boundaries and contracts, implementing event streaming with Kafka, configuring DAPR for distributed state and async messaging, deploying to Kubernetes with proper resources and health checks, creating parameterized Helm charts for multi-environment deployments, setting up local Minikube development environments, or ensuring production readiness with logging, tracing, metrics, and graceful shutdown. NOT when using non-FastAPI frameworks, non-Kubernetes platforms (e.g., serverless, Docker Swarm), or simple monolithic applications without microservices patterns.
---

# Backend Services Architect

You are an expert at designing and implementing production-grade backend systems. This skill provides structured guidance for building robust microservices, APIs, and distributed systems.

## Core Workflows

### 1. Designing FastAPI CRUD Operations

**When to use:** User needs a new REST API endpoint with proper validation, error handling, and status codes.

**Process:**
1. Define request/response models using Pydantic v2
2. Implement proper HTTP status codes (201 create, 204 no-content, 400 validation, 404 not-found, 409 conflict, 422 unprocessable)
3. Add input validation with detailed error messages
4. Implement pagination (limit/offset or cursor-based)
5. Add request logging with correlation IDs
6. Document with OpenAPI annotations

**Key constraints:**
- Always use Pydantic v2 for validation
- Never accept unvalidated input at API boundaries
- Implement idempotency keys for critical operations (POST /payments, POST /orders)
- Use dependency injection for database connections
- Include proper error responses with error codes

**Status code reference:**
- 200: Success with response body
- 201: Created (POST/PUT)
- 204: No content (DELETE)
- 400: Bad request (client error)
- 404: Not found
- 409: Conflict (duplicate, constraint violation)
- 422: Unprocessable entity (validation failure)
- 500: Server error

### 2. Architecting Microservices

**When to use:** Designing service boundaries, defining inter-service communication, or planning service-to-service contracts.

**Key decisions:**
- **Service boundaries**: Split by business capability (User Service, Order Service, Payment Service)
- **Synchronous vs Asynchronous**: Use DAPR service invocation for immediate responses; use Kafka for events and notifications
- **Data ownership**: Each service owns its database; never share schemas across services
- **API contracts**: Define OpenAPI specs before implementation; version APIs explicitly

**Service communication patterns:**
```
Synchronous (DAPR Service Invocation):
User Service → [DAPR] → Order Service
- Use for: Lookups, immediate validation, strong consistency
- Tradeoff: Tight coupling, cascading failures

Asynchronous (Kafka/Pub-Sub):
Order Service --[event]--> Kafka --[consumed by]--> Billing Service
- Use for: Notifications, eventual consistency, decoupling
- Tradeoff: Eventual consistency complexity
```

**Circuit breaker pattern:** Implement with tenacity or resilience4j to prevent cascading failures
```python
from tenacity import stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_downstream_service():
    # Handle timeout and exceptions
```

### 3. Implementing Event Streaming with Kafka

**When to use:** Designing event-driven architectures, handling high-volume messaging, or decoupling services.

**Key design decisions:**
- **Schema format**: Use Avro or Protobuf for schema evolution
- **Partitioning**: Number of partitions = expected throughput / 1MB per second (typical throughput)
- **Replication factor**: Minimum 3 for production (tolerance for 2 broker failures)
- **Consumer groups**: Each service is a consumer group; allows multiple consumers per group
- **Error handling**: Dead-letter topics (DLT) for failed messages

**Event schema example (Avro-style):**
```json
{
  "type": "record",
  "namespace": "com.orders",
  "name": "OrderCreated",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "customerId", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "timestamp", "type": "long"}
  ]
}
```

**Consumer group configuration:**
- Consumer lag monitoring: Alert if lag > 1 minute
- Offset strategy: Use committed offsets for exactly-once semantics
- Partition assignment: Use range or round-robin based on processing order requirements

**Dead-letter handling:**
- Topic naming: `{topic}-dlt` (e.g., `order-events-dlt`)
- Retry logic: Exponential backoff (1s, 2s, 4s, 8s, 16s)
- Max retries: 5 attempts before DLT
- Monitoring: Alert on DLT message rate > 10 messages/minute

### 4. Configuring DAPR Integration

**When to use:** Implementing service-to-service communication, distributed state, or secrets management in Kubernetes.

**DAPR components:**
1. **Service Invocation**: Synchronous HTTP/gRPC calls between services
2. **Pub/Sub**: Asynchronous messaging (backed by Kafka, RabbitMQ, etc.)
3. **State Management**: Distributed state store (Redis, Cosmos, etc.)
4. **Secrets**: Encrypted secret storage (Vault, Keyvault, etc.)

**Service invocation configuration:**
```yaml
# dapr-service-invocation.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: servicebus
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-0.kafka-headless.default.svc.cluster.local:9092"
  - name: consumerGroup
    value: "my-service-consumer-group"
```

**Python SDK usage:**
```python
from dapr.client import DaprClient

# Service invocation
with DaprClient() as d:
    result = d.invoke_method('order-service', 'POST', '/orders', json=order_data)

# Pub/Sub
d.publish_event('order-pubsub', 'order-events', {'orderId': '123'})

# State management
d.save_state('statestore', 'user-session-123', session_data)
```

**Error handling:**
- Timeout: Set appropriate timeout values (default 30s)
- Retry: DAPR includes built-in exponential backoff
- Circuit breaker: Implement in service code for additional protection

### 5. Orchestrating with Kubernetes

**When to use:** Deploying microservices to production, managing resource allocation, configuring networking.

**Essential manifest components:**

**Deployment with resource limits and health checks:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: order-service:latest
        ports:
        - containerPort: 8000

        # Resource requests AND limits REQUIRED
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Health checks
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

        # Environment and secrets
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: connection-string
```

**Service exposure:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  type: ClusterIP  # Internal only
  selector:
    app: order-service
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

**Key Kubernetes decisions:**
- **Replicas**: Minimum 3 for production (1 for dev)
- **Resource requests**: Must be set based on load testing; no defaults
- **Liveness probes**: Restart unhealthy pods
- **Readiness probes**: Remove from traffic until ready
- **Service type**: ClusterIP for internal, LoadBalancer for external
- **Network policies**: Restrict pod-to-pod communication

### 6. Creating Helm Charts

**When to use:** Packaging applications for multiple environments (dev, staging, prod) with configuration management.

**Helm chart structure:**
```
order-service-chart/
├── Chart.yaml              # Metadata
├── values.yaml             # Default values
├── values-dev.yaml         # Dev overrides
├── values-prod.yaml        # Prod overrides
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secret.yaml
└── README.md
```

**Key features:**
- **Parameterization**: All environment-specific values in values.yaml
- **Inheritance**: values.yaml + values-prod.yaml merged at deploy time
- **Pre-install hooks**: For database migrations
- **Post-install hooks**: For seeding initial data
- **Chart versioning**: Semantic versioning (MAJOR.MINOR.PATCH)

**Deployment:**
```bash
# Development
helm install order-service ./order-service-chart -f values-dev.yaml

# Production
helm install order-service ./order-service-chart -f values-prod.yaml

# Upgrade
helm upgrade order-service ./order-service-chart -f values-prod.yaml
```

### 7. Managing Local Development with Minikube

**When to use:** Setting up local Kubernetes environment for development and testing.

**Initial setup:**
```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=50g

# Enable ingress and metrics
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable storage-provisioner

# Enable image build integration
eval $(minikube docker-env)
```

**Local Kafka setup with docker-compose:**
```yaml
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
```

**Local DAPR configuration:**
```bash
# Install DAPR CLI
dapr init --kubernetes

# Verify DAPR sidecar injection
kubectl get dapr-system
```

### 8. Ensuring Production Readiness

**Before deploying to production, verify:**

**Logging:**
- Structured JSON logging (not plaintext)
- Include: timestamp, level, service, request_id, message
- Log levels: DEBUG (development), INFO (standard), WARN (issues), ERROR (failures)

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'service': 'order-service',
            'message': record.getMessage()
        }
        return json.dumps(log_data)

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

**Distributed tracing:**
- Use OpenTelemetry with Jaeger backend
- Propagate trace IDs across service boundaries
- Export traces to Jaeger collector

**Metrics:**
- Expose Prometheus metrics on `/metrics`
- Track: request latency (p50/p95/p99), error rate, throughput
- Alert thresholds: p95 latency > 500ms, error rate > 1%

**Graceful shutdown:**
```python
import signal

async def shutdown_handler():
    print("Shutting down gracefully...")
    # Stop accepting new requests
    # Wait for in-flight requests to complete (timeout 30s)
    # Close database connections
    # Export final metrics

signal.signal(signal.SIGTERM, shutdown_handler)
```

**Health check endpoints:**
- `GET /health` → 200 OK if service is up
- `GET /ready` → 200 OK if service is ready for traffic
- Readiness checks database connectivity, DAPR availability

## Decision Matrix

| Scenario | Solution | Why |
|----------|----------|-----|
| "Get data from another service now" | DAPR Service Invocation | Strong consistency, immediate response |
| "Notify when something happens" | Kafka Pub/Sub | Loose coupling, asynchronous |
| "Store user session" | DAPR State Store | Distributed state, built-in serialization |
| "Manage secrets" | DAPR Secrets | Encrypted, no hardcoding |
| "Multiple environments" | Helm Charts | Parameterized, reusable |
| "Local testing" | Minikube + docker-compose | Feature parity with production |

## Error Handling Patterns

**Kafka message failures:**
- Route to DLT after max retries
- Log failure details for debugging
- Alert ops team on DLT message rate spike
- Implement manual replay mechanism

**DAPR sidecar issues:**
- Check sidecar logs: `kubectl logs <pod> -c daprd`
- Verify component configurations exist
- Test endpoints with DAPR diagnostic tools
- Implement fallback to direct service calls

**Database connection failures:**
- Use connection pooling (SQLAlchemy default: 10 connections)
- Implement exponential backoff on connection failures
- Monitor pool exhaustion (metric: `db_pool_size`)
- Alert on connections > 80% capacity

**Kubernetes pod crashes:**
- Check recent logs: `kubectl logs <pod> --previous`
- Verify resource limits aren't being exceeded
- Ensure health probes have correct configuration
- Check pod events: `kubectl describe pod <pod>`

## Quick Reference

**Run Pydantic validation:** Create models, call `.model_validate()`, handle ValidationError
**Configure Kafka:** Set replication=3, monitor consumer lag, implement DLT
**Deploy to Kubernetes:** Define resource requests/limits, add health probes, use Services
**Build Helm chart:** Parameterize values.yaml, separate environment configs, document
**Test locally:** Use Minikube + docker-compose, enable ingress, verify networking

## References

See `references/` for detailed patterns:
- `fastapi-patterns.md` - CRUD operation templates
- `kafka-configuration.md` - Topic design and consumer setup
- `kubernetes-deployment.md` - Manifest examples
- `helm-best-practices.md` - Chart structure and versioning
- `dapr-integration.md` - Service invocation and state patterns
- `production-readiness.md` - Logging, metrics, graceful shutdown
- `error-handling.md` - Failure scenarios and recovery
