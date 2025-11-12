# Event-Driven Architecture Blueprint

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    Event Producers                           │
│  (Services that publish events)                              │
├──────────────┬───────────────┬───────────────┬───────────────┤
│ User Service │ Order Service │Payment Service│Email Service  │
└──────┬───────┴───────┬───────┴───────┬───────┴───────┬───────┘
       │               │               │               │
       │ Publish       │ Publish       │ Publish       │ Publish
       │ Events        │ Events        │ Events        │ Events
       │               │               │               │
       └───────────────┴───────┬───────┴───────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Message Broker    │
                    │  (Kafka / RabbitMQ  │
                    │   / NATS / Redis)   │
                    └──────────┬──────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
   Subscribe              Subscribe              Subscribe
       │                       │                       │
┌──────▼──────┐      ┌────────▼────────┐     ┌───────▼────────┐
│Notification │      │Analytics        │     │Audit Log       │
│Service      │      │Service          │     │Service         │
└─────────────┘      └─────────────────┘     └────────────────┘
```

## Message Broker Comparison

| Feature | RabbitMQ | Apache Kafka | Redis Streams | NATS |
|---------|----------|--------------|---------------|------|
| **Type** | Queue | Log | Stream | Queue/Stream |
| **Throughput** | Good (10K msg/s) | Excellent (100K+ msg/s) | Good (10K msg/s) | Excellent (100K+ msg/s) |
| **Persistence** | Yes | Yes | Yes | Optional |
| **Message Order** | Per queue | Per partition | Per stream | Optional |
| **Delivery Guarantee** | At-least-once | At-least-once | At-least-once | At-most-once |
| **Complexity** | Medium | High | Low | Low |
| **Clustering** | Yes | Native | Sentinel/Cluster | Native |
| **Best For** | Task queues | Event streaming | Simple pub/sub | Lightweight messaging |

### Selection Guide

```python
if need_simple_queue || low_volume:
    → RabbitMQ (easy to set up, AMQP standard)
    
elif need_high_throughput || event_sourcing || data_replay:
    → Kafka (distributed log, high throughput)
    
elif already_using_redis || simple_pubsub:
    → Redis Streams (minimal setup, good performance)
    
elif need_lightweight || cloud_native:
    → NATS (Go-based, very fast, simple)
```

## Event Patterns

### 1. Event Notification

**Use Case:** Notify other services when something happens

```
User Service: User registered
    → Publish: UserRegisteredEvent
    
Subscribers:
    - Email Service: Send welcome email
    - Analytics Service: Track new user
    - CRM Service: Create lead
```

**Implementation (Python):**
```python
# Event definition
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserRegisteredEvent:
    event_id: str
    user_id: str
    email: str
    username: str
    timestamp: datetime
    
    def to_dict(self):
        return {
            "event_id": self.event_id,
            "event_type": "user.registered",
            "data": {
                "user_id": self.user_id,
                "email": self.email,
                "username": self.username
            },
            "timestamp": self.timestamp.isoformat()
        }

# Publisher (User Service)
import pika
import json
import uuid

class EventPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='events',
            exchange_type='topic'
        )
    
    def publish(self, event: UserRegisteredEvent):
        self.channel.basic_publish(
            exchange='events',
            routing_key='user.registered',
            body=json.dumps(event.to_dict())
        )

# Subscriber (Email Service)
class EmailSubscriber:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='email_queue')
        self.channel.queue_bind(
            exchange='events',
            queue='email_queue',
            routing_key='user.registered'
        )
    
    def start(self):
        self.channel.basic_consume(
            queue='email_queue',
            on_message_callback=self.handle_user_registered,
            auto_ack=False
        )
        self.channel.start_consuming()
    
    def handle_user_registered(self, ch, method, properties, body):
        event = json.loads(body)
        
        try:
            # Send welcome email
            send_email(
                to=event['data']['email'],
                subject='Welcome!',
                template='welcome'
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            # Reject and requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
```

### 2. Event-Carried State Transfer

**Use Case:** Include all necessary data in event (avoid service-to-service calls)

```python
@dataclass
class OrderCreatedEvent:
    order_id: str
    user_id: str
    user_email: str  # Denormalized from User Service
    items: List[dict]
    total_amount: float
    shipping_address: dict
    timestamp: datetime
```

**Benefits:**
- Subscribers don't need to call other services
- Eventual consistency
- Better fault tolerance

**Trade-off:**
- Larger message size
- Data duplication

### 3. Event Sourcing

**Use Case:** Store all state changes as events (audit trail, replay capability)

```python
# Command
class CreateOrderCommand:
    def __init__(self, user_id: str, items: List[dict]):
        self.user_id = user_id
        self.items = items

# Events
@dataclass
class OrderCreatedEvent:
    order_id: str
    user_id: str
    items: List[dict]
    timestamp: datetime

@dataclass
class OrderPaidEvent:
    order_id: str
    payment_id: str
    amount: float
    timestamp: datetime

@dataclass
class OrderShippedEvent:
    order_id: str
    tracking_number: str
    timestamp: datetime

# Aggregate
class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.status = "pending"
        self.events = []
    
    def create(self, user_id: str, items: List[dict]):
        event = OrderCreatedEvent(
            order_id=self.order_id,
            user_id=user_id,
            items=items,
            timestamp=datetime.utcnow()
        )
        self.apply(event)
        self.events.append(event)
    
    def pay(self, payment_id: str, amount: float):
        if self.status != "pending":
            raise ValueError("Order already paid")
        
        event = OrderPaidEvent(
            order_id=self.order_id,
            payment_id=payment_id,
            amount=amount,
            timestamp=datetime.utcnow()
        )
        self.apply(event)
        self.events.append(event)
    
    def apply(self, event):
        if isinstance(event, OrderCreatedEvent):
            self.status = "pending"
        elif isinstance(event, OrderPaidEvent):
            self.status = "paid"
        elif isinstance(event, OrderShippedEvent):
            self.status = "shipped"
    
    @classmethod
    def from_events(cls, order_id: str, events: List):
        order = cls(order_id)
        for event in events:
            order.apply(event)
        return order
```

**Event Store:**
```python
class EventStore:
    def __init__(self, db):
        self.db = db
    
    def save_events(self, aggregate_id: str, events: List):
        for event in events:
            self.db.execute(
                """
                INSERT INTO events (aggregate_id, event_type, data, timestamp)
                VALUES (%s, %s, %s, %s)
                """,
                (aggregate_id, type(event).__name__, json.dumps(event.__dict__), event.timestamp)
            )
    
    def get_events(self, aggregate_id: str) -> List:
        rows = self.db.query(
            "SELECT event_type, data FROM events WHERE aggregate_id = %s ORDER BY timestamp",
            (aggregate_id,)
        )
        return [self._deserialize(row) for row in rows]
    
    def _deserialize(self, row):
        event_class = globals()[row['event_type']]
        return event_class(**json.loads(row['data']))
```

### 4. CQRS (Command Query Responsibility Segregation)

**Use Case:** Separate read and write models

```
Write Side (Command):                Read Side (Query):
┌──────────────┐                    ┌──────────────┐
│   Commands   │                    │   Queries    │
└──────┬───────┘                    └──────┬───────┘
       │                                   │
┌──────▼───────┐                    ┌──────▼───────┐
│ Command      │    Events          │ Query        │
│ Handlers     ├────────────────────►│ Handlers    │
└──────┬───────┘                    └──────┬───────┘
       │                                   │
┌──────▼───────┐                    ┌──────▼───────┐
│ Write DB     │                    │ Read DB      │
│ (Normalized) │                    │ (Denormalized│
└──────────────┘                    │ Optimized)   │
                                    └──────────────┘
```

**Implementation:**
```python
# Write side
class CreateOrderHandler:
    def __init__(self, event_store, event_publisher):
        self.event_store = event_store
        self.event_publisher = event_publisher
    
    def handle(self, command: CreateOrderCommand):
        # Create aggregate
        order = Order(str(uuid.uuid4()))
        order.create(command.user_id, command.items)
        
        # Save events
        self.event_store.save_events(order.order_id, order.events)
        
        # Publish events
        for event in order.events:
            self.event_publisher.publish(event)

# Read side (projection)
class OrderProjection:
    def __init__(self, db):
        self.db = db
    
    def handle_order_created(self, event: OrderCreatedEvent):
        self.db.execute(
            """
            INSERT INTO order_read_model (order_id, user_id, status, total)
            VALUES (%s, %s, 'pending', %s)
            """,
            (event.order_id, event.user_id, self._calculate_total(event.items))
        )
    
    def handle_order_paid(self, event: OrderPaidEvent):
        self.db.execute(
            "UPDATE order_read_model SET status = 'paid' WHERE order_id = %s",
            (event.order_id,)
        )
```

## Saga Pattern (Distributed Transactions)

### Choreography-Based Saga

**Use Case:** Distributed transaction across services

```
Order Service → Place Order
    ↓ (publish: OrderPlaced)
Payment Service → Process Payment
    ↓ (publish: PaymentProcessed)
Inventory Service → Reserve Items
    ↓ (publish: ItemsReserved)
Shipping Service → Create Shipment
    ↓ (publish: ShipmentCreated)

If any step fails, compensating transactions are triggered
```

**Implementation:**
```python
# Order Service
class OrderSaga:
    def __init__(self, event_publisher):
        self.publisher = event_publisher
    
    def start(self, order_data):
        # Step 1: Create order
        order = create_order(order_data)
        
        # Publish event
        self.publisher.publish(OrderPlacedEvent(
            order_id=order.id,
            user_id=order.user_id,
            amount=order.total,
            items=order.items
        ))

# Payment Service (Listener)
class PaymentSagaHandler:
    def handle_order_placed(self, event: OrderPlacedEvent):
        try:
            # Process payment
            payment = process_payment(event.user_id, event.amount)
            
            # Success: Publish success event
            self.publisher.publish(PaymentProcessedEvent(
                order_id=event.order_id,
                payment_id=payment.id
            ))
        except PaymentFailedError:
            # Failure: Publish failure event
            self.publisher.publish(PaymentFailedEvent(
                order_id=event.order_id,
                reason="Insufficient funds"
            ))

# Order Service (Compensation)
class OrderCompensationHandler:
    def handle_payment_failed(self, event: PaymentFailedEvent):
        # Cancel order
        cancel_order(event.order_id)
        
        # Publish cancellation
        self.publisher.publish(OrderCancelledEvent(
            order_id=event.order_id,
            reason=event.reason
        ))
```

### Orchestration-Based Saga

**Use Case:** Central coordinator manages saga

```python
class OrderSagaOrchestrator:
    def __init__(self):
        self.steps = [
            self.create_order,
            self.process_payment,
            self.reserve_inventory,
            self.create_shipment
        ]
        self.compensations = [
            self.cancel_order,
            self.refund_payment,
            self.release_inventory,
            None
        ]
    
    async def execute(self, order_data):
        executed_steps = []
        
        try:
            for step in self.steps:
                await step(order_data)
                executed_steps.append(step)
            
            return {"success": True}
        
        except Exception as e:
            # Compensate in reverse order
            for step in reversed(executed_steps):
                compensation_index = self.steps.index(step)
                compensation = self.compensations[compensation_index]
                if compensation:
                    await compensation(order_data)
            
            return {"success": False, "error": str(e)}
    
    async def create_order(self, data):
        # Call Order Service
        pass
    
    async def process_payment(self, data):
        # Call Payment Service
        pass
    
    async def cancel_order(self, data):
        # Compensating transaction
        pass
```

## Message Patterns

### 1. At-Most-Once Delivery

```python
# Fire and forget, no retry
publisher.publish(event, delivery_mode=1)  # Non-persistent
```

### 2. At-Least-Once Delivery

```python
# Retry until acknowledged
def publish_with_retry(event, max_retries=3):
    for attempt in range(max_retries):
        try:
            publisher.publish(event, delivery_mode=2)  # Persistent
            return
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 3. Exactly-Once Delivery (Idempotency)

```python
class IdempotentConsumer:
    def __init__(self, db):
        self.db = db
        self.processed_events = set()
    
    def handle(self, event):
        # Check if already processed
        if self.db.exists("processed_events", event.event_id):
            return  # Skip duplicate
        
        try:
            # Process event
            self.process_event(event)
            
            # Mark as processed
            self.db.insert("processed_events", {
                "event_id": event.event_id,
                "processed_at": datetime.utcnow()
            })
        except Exception as e:
            # Log and retry
            raise
```

## Monitoring & Observability

```python
from prometheus_client import Counter, Histogram

# Metrics
events_published = Counter('events_published_total', 'Events published', ['event_type'])
events_consumed = Counter('events_consumed_total', 'Events consumed', ['event_type'])
processing_time = Histogram('event_processing_seconds', 'Processing time', ['event_type'])

def publish_event(event):
    events_published.labels(event_type=event.__class__.__name__).inc()
    # ... publish logic

def consume_event(event):
    start = time.time()
    
    # Process
    handle_event(event)
    
    # Metrics
    processing_time.labels(event_type=event.__class__.__name__).observe(time.time() - start)
    events_consumed.labels(event_type=event.__class__.__name__).inc()
```

## Error Handling

### Dead Letter Queue

```python
def handle_message(message):
    max_retries = 3
    
    try:
        process_message(message)
        channel.basic_ack(delivery_tag=message.delivery_tag)
    except Exception as e:
        retry_count = message.headers.get('x-retry-count', 0)
        
        if retry_count < max_retries:
            # Requeue with incremented retry count
            channel.basic_publish(
                exchange='',
                routing_key=message.queue,
                body=message.body,
                properties=pika.BasicProperties(
                    headers={'x-retry-count': retry_count + 1}
                )
            )
            channel.basic_ack(delivery_tag=message.delivery_tag)
        else:
            # Send to dead letter queue
            channel.basic_publish(
                exchange='',
                routing_key='dead_letter_queue',
                body=message.body
            )
            channel.basic_ack(delivery_tag=message.delivery_tag)
```

---

**Estimated Costs (per month):**
- RabbitMQ (self-hosted): $50-100 (VPS)
- Kafka (self-hosted): $200-500 (3-node cluster)
- RabbitMQ (CloudAMQP): $19-99
- Kafka (Confluent Cloud): $100-500+
- Redis Streams: Included in Redis hosting
