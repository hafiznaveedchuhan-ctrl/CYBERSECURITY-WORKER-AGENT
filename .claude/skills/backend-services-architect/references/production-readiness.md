# Production Readiness Checklist

## Logging Implementation

**Structured JSON Logging:**
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Format logs as JSON for ELK/Loki ingestion"""

    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'service': 'order-service',
            'version': '1.0.0',
        }

        # Add exception info if present
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        # Add custom fields
        if hasattr(record, 'correlation_id'):
            log_record['correlation_id'] = record.correlation_id
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id

        return json.dumps(log_record)

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# Usage
logger.info('Order processed', extra={
    'correlation_id': 'abc-123',
    'order_id': '456',
    'user_id': '789'
})
```

**Logging Levels:**
```python
logger.debug('Variable value: x=%s', x)        # Development only
logger.info('User logged in', extra={...})     # Important events
logger.warning('Slow query: %dms', duration)   # Potential issues
logger.error('Payment failed', exc_info=True)  # Errors (won't crash)
logger.critical('Database down!')              # Must fix now (crash likely)
```

## Distributed Tracing with OpenTelemetry

**Instrumentation Setup:**
```python
from opentelemetry import trace, metrics
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name='jaeger-collector',
    agent_port=6831,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Instrument SQLAlchemy
SQLAlchemyInstrumentor().instrument(
    engine=engine,
    service=os.getenv('SERVICE_NAME', 'order-service')
)

# Manual span creation
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span('process_order') as span:
    span.set_attribute('order_id', '123')
    span.set_attribute('customer_id', '456')

    try:
        result = process_order()
        span.set_attribute('status', 'success')
    except Exception as e:
        span.set_attribute('status', 'error')
        span.record_exception(e)
        raise
```

## Prometheus Metrics

**Metrics Export:**
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Response
import time

# Define metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

active_orders = Gauge(
    'orders_processing',
    'Number of orders being processed'
)

db_connection_pool = Gauge(
    'db_pool_connections',
    'Number of active database connections'
)

# Middleware to collect metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response

# Expose metrics endpoint
@app.get('/metrics')
async def metrics():
    return Response(
        content=generate_latest(),
        media_type='text/plain; version=0.0.4'
    )
```

**Alert Rules (Prometheus):**
```yaml
groups:
- name: order-service
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
    for: 5m
    annotations:
      summary: "High error rate in order-service"
      description: "Error rate > 1% for 5 minutes"

  - alert: HighLatency
    expr: histogram_quantile(0.95, http_request_duration_seconds) > 0.5
    for: 5m
    annotations:
      summary: "High latency in order-service"
      description: "p95 latency > 500ms"

  - alert: LowAvailability
    expr: kube_pod_status_ready{pod=~"order-service.*"} < 3
    for: 1m
    annotations:
      summary: "Low availability in order-service"
      description: "Less than 3 pods ready"
```

## Health Checks

**Implementation:**
```python
from sqlalchemy import text
import httpx

@app.get('/health', status_code=200)
async def health_check():
    """Liveness probe - is service running?"""
    return {
        'status': 'healthy',
        'service': 'order-service',
        'timestamp': datetime.utcnow().isoformat()
    }

@app.get('/ready', status_code=200)
async def readiness_check():
    """Readiness probe - can service accept traffic?"""
    checks = {
        'database': False,
        'cache': False,
        'dapr': False
    }

    try:
        # Check database
        async with db.connect() as conn:
            await conn.execute(text("SELECT 1"))
            checks['database'] = True
    except Exception as e:
        logger.error(f'Database check failed: {e}')

    try:
        # Check cache (Redis)
        async with redis.client() as client:
            await client.ping()
            checks['cache'] = True
    except Exception as e:
        logger.error(f'Cache check failed: {e}')

    try:
        # Check DAPR sidecar
        async with httpx.AsyncClient() as client:
            response = await client.get('http://localhost:3500/v1.0/metadata')
            checks['dapr'] = response.status_code == 200
    except Exception as e:
        logger.error(f'DAPR check failed: {e}')

    # All checks must pass for readiness
    if all(checks.values()):
        return {
            'status': 'ready',
            'checks': checks
        }
    else:
        raise HTTPException(
            status_code=503,
            detail=f'Service not ready: {checks}'
        )
```

## Graceful Shutdown

**Signal Handling:**
```python
import signal
import asyncio
from contextlib import asynccontextmanager

# Track in-flight requests
in_flight_requests = set()

@asynccontextmanager
async def track_request():
    """Context manager to track active requests"""
    request_id = id(asyncio.current_task())
    in_flight_requests.add(request_id)
    try:
        yield
    finally:
        in_flight_requests.discard(request_id)

# Middleware to track requests
@app.middleware("http")
async def track_requests_middleware(request, call_next):
    async with track_request():
        return await call_next(request)

async def shutdown_handler():
    """Handle SIGTERM gracefully"""
    logger.info('Shutdown signal received, stopping gracefully...')

    # Stop accepting new requests
    app.state.accepting_requests = False

    # Wait for in-flight requests (with timeout)
    deadline = asyncio.get_event_loop().time() + 30  # 30 seconds
    while in_flight_requests:
        if asyncio.get_event_loop().time() > deadline:
            logger.warning('Timeout waiting for requests to complete')
            break
        await asyncio.sleep(0.1)

    # Close database connections
    await db.dispose()

    # Close cache connections
    redis.connection_pool.disconnect()

    # Export final metrics
    logger.info('Graceful shutdown complete')

@app.get('/shutdown')
async def shutdown():
    """Manual shutdown endpoint (for testing)"""
    asyncio.create_task(shutdown_handler())
    return {'status': 'shutting down'}

# Register signal handler
loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGTERM, shutdown_handler)
```

## Production Deployment Verification

**Pre-Deployment Checklist:**
- [ ] All environment variables documented in `.env.example`
- [ ] Secrets stored in cluster secret management (not in code/config)
- [ ] Logging configured to output JSON to stdout
- [ ] Health check endpoints implemented (`/health`, `/ready`)
- [ ] Graceful shutdown implemented (30-60s drain period)
- [ ] Metrics exported on `/metrics` endpoint
- [ ] Trace context propagated across services
- [ ] Error handling covers all external dependencies
- [ ] Database connection pooling configured
- [ ] Request timeouts configured (all external calls)
- [ ] Circuit breaker pattern implemented for critical dependencies
- [ ] API rate limiting implemented if needed
- [ ] Request validation using Pydantic
- [ ] CORS properly configured (not `*` in production)
- [ ] Security headers set (HSTS, CSP, etc.)

**Load Testing Before Production:**
```bash
# Using k6
k6 run - <<EOF
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50,
  duration: '5m',
};

export default function() {
  let res = http.get('http://order-service/orders');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'latency < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
EOF
```

**Monitoring in Production:**
```yaml
# Prometheus scrape config
- job_name: 'order-service'
  kubernetes_sd_configs:
  - role: pod
    namespaces:
      names:
      - microservices
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    action: keep
    regex: true
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    action: replace
    target_label: __metrics_path__
    regex: (.+)
  - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
    action: replace
    regex: ([^:]+)(?::\d+)?;(\d+)
    replacement: $1:$2
    target_label: __address__
```

## Feature Flags for Gradual Rollout

```python
from enum import Enum

class FeatureFlags(str, Enum):
    NEW_PAYMENT_ENGINE = "new_payment_engine"
    ADVANCED_ANALYTICS = "advanced_analytics"

def is_feature_enabled(flag: FeatureFlags, user_id: str = None) -> bool:
    """Check if feature is enabled"""
    # In production, fetch from feature flag service
    feature_config = feature_flag_service.get(flag)

    if feature_config.rollout_percentage == 100:
        return True

    if user_id and feature_config.enabled_users:
        return user_id in feature_config.enabled_users

    if feature_config.rollout_percentage > 0:
        # Percentage-based rollout
        return hash(user_id) % 100 < feature_config.rollout_percentage

    return False

# Usage in code
@app.post('/process-payment')
async def process_payment(payment: PaymentRequest):
    if is_feature_enabled(FeatureFlags.NEW_PAYMENT_ENGINE, user_id=payment.user_id):
        return await new_payment_engine.process(payment)
    else:
        return await legacy_payment_engine.process(payment)
```
