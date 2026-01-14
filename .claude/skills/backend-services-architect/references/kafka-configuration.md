# Kafka Configuration Guide

## Topic Design

**Topic naming convention:**
```
{service}.{domain}.{event-type}
Examples:
  order.events.created
  order.events.completed
  payment.events.processed
  billing.events.invoice-generated
```

**Topic configuration parameters:**
```bash
# Create topic with optimal settings
kafka-topics.sh --create \
  --topic order.events.created \
  --partitions 3 \
  --replication-factor 3 \
  --config retention.ms=604800000 \
  --config compression.type=snappy \
  --config min.insync.replicas=2
```

**Key configuration decisions:**
- **Partitions**: 1 partition per 1MB/sec expected throughput
- **Replication factor**: 3 for production (tolerates 2 broker failures)
- **min.insync.replicas**: 2 (ensures durability with replication=3)
- **Retention**: 7 days default (adjust based on requirements)
- **Compression**: snappy (good balance of CPU and compression ratio)

## Consumer Group Setup

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'order.events.created',
    bootstrap_servers=['kafka:9092'],
    group_id='billing-service-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),

    # Offset management
    auto_offset_reset='earliest',  # Start from beginning if no offset
    enable_auto_commit=False,  # Manual commit for exactly-once
    max_poll_records=100,  # Process in batches
    session_timeout_ms=30000,
)

for message in consumer:
    try:
        order_event = message.value
        process_order(order_event)
        consumer.commit()  # Commit only after successful processing
    except Exception as e:
        logger.error(f'Error processing message: {e}')
        # Don't commit - message will be reprocessed
```

## Producer Configuration

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),

    # Reliability settings
    acks='all',  # Wait for all replicas
    retries=3,
    max_in_flight_requests_per_connection=1,  # Maintain order

    # Performance
    batch_size=16384,
    linger_ms=10,
)

try:
    future = producer.send(
        'order.events.created',
        value={
            'orderId': '123',
            'amount': 99.99,
            'timestamp': time.time()
        }
    )
    record_metadata = future.get(timeout=10)
    logger.info(f'Message sent to partition {record_metadata.partition}')
except Exception as e:
    logger.error(f'Failed to send message: {e}')
```

## Dead-Letter Topic Pattern

```python
def process_with_dlq(message, max_retries=5):
    """Process message with DLQ fallback"""
    retry_count = message.headers.get(b'retry-count', b'0')
    retry_count = int(retry_count.decode()) + 1

    try:
        # Process the message
        handle_payment(message.value)
        logger.info(f'Message processed successfully')
    except Exception as e:
        if retry_count < max_retries:
            logger.warning(f'Retry {retry_count}/{max_retries}: {e}')
            # Republish with incremented retry count
            producer.send(
                'order.events.created',
                value=message.value,
                headers=[(b'retry-count', str(retry_count).encode())]
            )
        else:
            # Send to DLQ after max retries
            logger.error(f'Message failed after {max_retries} retries: {e}')
            producer.send(
                'order.events.created-dlt',
                value=message.value,
                headers=[(b'original-error', str(e).encode())]
            )

# Monitoring consumer lag
def monitor_consumer_lag(group_id, topic):
    """Check consumer lag for alerting"""
    from kafka.admin import KafkaAdminClient

    admin = KafkaAdminClient(bootstrap_servers=['kafka:9092'])
    lag = admin.list_consumer_group_offsets(group_id)

    for partition, offset in lag.items():
        committed = offset.offset
        log_size = get_partition_log_size(topic, partition)
        lag_messages = log_size - committed

        if lag_messages > 10000:  # Alert if lag > 10k messages
            logger.warning(f'High consumer lag: {lag_messages} messages')
```

## Schema Evolution with Avro

```python
from confluent_kafka import Producer, Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroProducer, AvroConsumer

schema_registry = SchemaRegistryClient({'url': 'http://schema-registry:8081'})

# Producer
avro_producer = AvroProducer(
    {'bootstrap.servers': 'kafka:9092'},
    schema_registry_client=schema_registry
)

order_event = {
    'orderId': '123',
    'customerId': '456',
    'amount': 99.99
}

avro_producer.produce(
    topic='order.events.created',
    value=order_event,
    value_schema=order_created_schema
)

# Consumer automatically handles schema evolution
avro_consumer = AvroConsumer(
    {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'billing-service'
    },
    schema_registry_client=schema_registry
)

avro_consumer.subscribe(['order.events.created'])
msg = avro_consumer.poll()
print(msg.value())  # Automatically deserialized with compatible schema
```

## Monitoring Checklist

- [ ] Consumer lag (alert if > 1 min behind)
- [ ] DLQ message rate (alert if > 10 msgs/min)
- [ ] Producer error rate (alert if > 0.1%)
- [ ] Broker disk usage (alert if > 80%)
- [ ] Partition imbalance (alert if any partition > 20% difference)
