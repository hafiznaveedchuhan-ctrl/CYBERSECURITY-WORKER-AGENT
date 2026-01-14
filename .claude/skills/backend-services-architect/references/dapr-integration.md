# DAPR Integration Patterns

## Service Invocation Setup

**DAPR Component Configuration (Kubernetes):**
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: orderservice
  namespace: default
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis:6379
  - name: redisPassword
    value: ""
  - name: maxConnections
    value: "10"
  - name: consumerID
    value: "service-a"
  - name: actorStateStore
    value: "true"
```

**Sidecar Configuration:**
```bash
# Kubernetes sidecar injection (automatic via admission controller)
daprd \
  --app-id order-service \
  --app-port 8000 \
  --dapr-http-port 3500 \
  --dapr-grpc-port 50001 \
  --components-path ./components \
  --log-level info
```

**Service Invocation Example (Python):**
```python
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem

# Synchronous invocation
with DaprClient() as d:
    response = d.invoke_method(
        'payment-service',           # Target service app-id
        'POST',                       # HTTP method
        '/process-payment',           # Endpoint
        json={'orderId': '123', 'amount': 99.99},
        timeout=10
    )
    result = response.json()
    logger.info(f'Payment processed: {result}')
```

**Error Handling:**
```python
from dapr.clients.exceptions import DaprInvocationError

try:
    response = d.invoke_method(
        'payment-service',
        'POST',
        '/process-payment',
        json=payment_data,
        timeout=10
    )
except DaprInvocationError as e:
    logger.error(f'Service invocation failed: {e.message}')
    # Implement fallback or retry logic
except TimeoutError:
    logger.error('Service invocation timeout')
    # Implement circuit breaker
```

## Pub/Sub Configuration

**Kafka Pub/Sub Component:**
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: order-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-broker-0.kafka.default.svc.cluster.local:9092,kafka-broker-1.kafka.default.svc.cluster.local:9092"
  - name: consumerGroup
    value: "order-service-group"
  - name: authRequired
    value: "false"
  - name: maxMessageBytes
    value: "1000000"
  - name: version
    value: "3.0.0"
```

**Publisher:**
```python
# Publish event
d.publish_event(
    pubsub_name='order-pubsub',
    topic_name='order.events',
    publish_data={
        'orderId': '123',
        'customerId': '456',
        'amount': 99.99,
        'timestamp': datetime.utcnow().isoformat()
    }
)

# With retry policy
import asyncio
from tenacity import stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
async def publish_with_retry(pubsub_name, topic, data):
    d.publish_event(pubsub_name, topic, data)
```

**Subscriber:**
```python
from dapr import DaprClient
from dapr.ext.grpc import App
import logging

app = App()
logger = logging.getLogger(__name__)

# Subscribe to topic
@app.subscribe(pubsub_name='order-pubsub', topic_name='order.events')
def order_event_handler(event: dict) -> None:
    try:
        order_id = event.get('orderId')
        customer_id = event.get('customerId')
        amount = event.get('amount')

        logger.info(f'Processing order {order_id}')

        # Process the order
        process_order(order_id, customer_id, amount)

        # Return 200 to acknowledge successful processing
    except Exception as e:
        logger.error(f'Failed to process order: {e}')
        # Raise to trigger retry/DLQ
        raise

if __name__ == '__main__':
    app.run(port=8000)
```

## State Management

**State Store Component:**
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: order-statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis.default.svc.cluster.local:6379
  - name: redisPassword
    value: ""
  - name: enableTLS
    value: "false"
```

**State Operations:**
```python
from dapr.clients import DaprClient

# Save state
with DaprClient() as d:
    state = {
        'orderId': '123',
        'status': 'processing',
        'lastUpdated': datetime.utcnow().isoformat()
    }

    d.save_state(
        store_name='order-statestore',
        key='order-123',
        value=state
    )

# Retrieve state
state = d.get_state(
    store_name='order-statestore',
    key='order-123'
)

if state.data:
    order_status = json.loads(state.data)
    logger.info(f'Order status: {order_status}')

# Delete state
d.delete_state(
    store_name='order-statestore',
    key='order-123'
)

# State transactions
from dapr.clients.grpc._state import StateItem

state_items = [
    StateItem(
        key='order-123',
        value={'status': 'completed'},
        etag='abc123'  # For optimistic concurrency
    )
]

d.execute_state_transaction(
    store_name='order-statestore',
    operations=state_items
)
```

## Secrets Management

**Secrets Component:**
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretmanager.local.file
  version: v1
  metadata:
  - name: secretsFile
    value: "/etc/dapr/secrets/secrets.json"
```

**Retrieving Secrets:**
```python
# Get secret
secret = d.get_secret(
    store_name='kubernetes-secrets',
    key='database-password',
    metadata={}
)

connection_string = f"postgresql://user:{secret.secret.get('password')}@db:5432/mydb"
```

## Retry and Timeout Policies

**Configuring retry in manifest:**
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: order-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: consumerGroup
    value: "order-service"
  - name: maxRetries
    value: "3"
  - name: retryAfterMs
    value: "1000"  # 1 second initial, exponential backoff
```

**Configurable timeouts:**
```python
# Adjust timeout per invocation
response = d.invoke_method(
    app_id='payment-service',
    method='POST',
    method_invoke_url='/process',
    json=data,
    timeout=30  # seconds
)

# Circuit breaker pattern for cascading failures
from tenacity import stop_after_attempt, wait_exponential, retry

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def call_with_circuit_breaker(app_id, method, url, data):
    return d.invoke_method(app_id, method, url, json=data, timeout=5)
```

## DAPR Sidecar Debugging

```bash
# Check DAPR logs
kubectl logs <pod-name> -c daprd

# Check if DAPR is running
kubectl get pods -l app=dapr-sidecar

# Test DAPR API
kubectl port-forward <pod-name> 3500:3500

# From another terminal
curl http://localhost:3500/v1.0/invoke/payment-service/method/health

# Check component status
curl http://localhost:3500/v1.0/metadata

# List subscriptions
curl http://localhost:3500/v1.0/subscribe

# DAPR CLI
dapr invoke --app-id payment-service --method /health
dapr publish --pubsub order-pubsub --topic order.events --data '{"id":"123"}'
dapr state get --store-name mystore --key mykey
```

## Production Checklist

- [ ] DAPR sidecar resource requests/limits set
- [ ] Service invocation timeout configured (default 30s)
- [ ] Pub/Sub consumer group configured per service
- [ ] Dead-letter topics configured for failed messages
- [ ] State store persistence enabled (not in-memory)
- [ ] Secrets management integrated with cluster secret store
- [ ] Circuit breaker implemented for critical calls
- [ ] Retry policies configured with exponential backoff
- [ ] Correlation IDs propagated through DAPR calls
- [ ] Monitoring and alerting on DAPR metrics configured
