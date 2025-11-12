# Architecture Patterns - Deep Dive

## Microservices Architecture

### When to Use
- **Team Size:** 50+ engineers across multiple teams
- **Domain Complexity:** Clear bounded contexts (DDD)
- **Release Cadence:** Independent deployment per service
- **Technology Diversity:** Polyglot persistence needs

### Service Decomposition Strategies

#### 1. By Business Capability (Recommended)
```
User Management Service
├── Authentication
├── Profile Management
├── Permissions & Roles
└── User Analytics

Order Service
├── Cart Management
├── Order Processing
├── Payment Integration
└── Order Tracking

Inventory Service
├── Stock Management
├── Warehouse Integration
├── Replenishment
└── Forecasting
```

#### 2. By Subdomain (DDD Approach)
```
Core Domain: Order Fulfillment
├── Order Service
├── Payment Service
├── Shipping Service

Supporting Domain: Customer Support
├── Ticket Service
├── Knowledge Base
├── Chat Service

Generic Domain: Notifications
├── Email Service
├── SMS Service
├── Push Notification Service
```

### Communication Patterns

#### Synchronous (REST/gRPC)
**Use When:**
- Immediate response required
- Request-response pattern
- Client needs to know outcome immediately

**Example:** User authentication, payment processing

```
Client → API Gateway → Auth Service → Database
       ← Response ←  ← Response ←
```

**Considerations:**
- Timeout handling (circuit breakers)
- Retry logic (exponential backoff)
- Fallback strategies
- Rate limiting

#### Asynchronous (Message Queue/Event Bus)
**Use When:**
- Fire-and-forget acceptable
- Multiple consumers need same data
- Decoupling services critical
- Eventual consistency acceptable

**Example:** Order placed → Inventory, Email, Analytics all notified

```
Order Service → Kafka Topic → [Inventory, Email, Analytics Services]
```

**Patterns:**
- Pub/Sub: Multiple subscribers per topic
- Queue: Single consumer per message
- Dead Letter Queue: Failed message handling

### Service Mesh

#### When to Adopt
- 20+ microservices
- Complex inter-service communication
- Observability requirements (tracing, metrics)
- Security requirements (mTLS, authorization)

#### Istio Implementation Pattern
```yaml
# Service-to-service communication
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
  - order-service
  http:
  - route:
    - destination:
        host: order-service
        subset: v2
      weight: 10
    - destination:
        host: order-service
        subset: v1
      weight: 90
  timeout: 5s
  retries:
    attempts: 3
    perTryTimeout: 2s
```

**Capabilities:**
- Traffic management (canary, blue-green)
- Circuit breaker & retry policies
- Distributed tracing (Jaeger integration)
- Security policies (mTLS, authorization)

## Event-Driven Architecture

### Core Concepts

#### Event Types
1. **Event Notification:** "Order placed" (thin event)
2. **Event-Carried State Transfer:** "Order placed with full order details"
3. **Event Sourcing:** All state changes stored as events

#### Event Schema Design
```json
{
  "eventId": "uuid",
  "eventType": "order.placed",
  "eventVersion": "1.0",
  "timestamp": "ISO-8601",
  "metadata": {
    "correlationId": "uuid",
    "causationId": "uuid",
    "userId": "uuid"
  },
  "payload": {
    "orderId": "uuid",
    "userId": "uuid",
    "items": [...],
    "totalAmount": 150.00
  }
}
```

### Event Sourcing Pattern

**Use Cases:**
- Audit trail required (financial, healthcare)
- Time-travel queries needed
- Complex business logic with rollback
- Multiple projections of same data

**Implementation:**
```
Command → Aggregate → Events → Event Store
                               ↓
                         Projections (Read Models)
```

**Example: Bank Account**
```
Events:
1. AccountOpened (balance: 0)
2. MoneyDeposited (amount: 1000)
3. MoneyWithdrawn (amount: 200)
4. MoneyDeposited (amount: 500)

Current State (projection): balance = 1300
Historical State (replay to event 2): balance = 1000
```

**Challenges:**
- Event versioning (schema evolution)
- Snapshot strategy (performance)
- Eventual consistency handling
- Event replay complexity

## CQRS (Command Query Responsibility Segregation)

### Pattern Overview
```
Write Side (Commands):
Client → Command Handler → Write Model (normalized) → Event Store

Read Side (Queries):
Event Store → Event Handlers → Read Models (denormalized) → Query API → Client
```

### When to Use
- Read/write patterns very different
- Write side complex validation
- Read side needs multiple projections
- High read:write ratio (10:1+)

### Example: E-commerce Product Catalog

**Write Model:**
```sql
-- Normalized for consistency
products (id, name, category_id, created_at, updated_at)
categories (id, name, parent_id)
prices (product_id, currency, amount, valid_from)
inventory (product_id, warehouse_id, quantity)
```

**Read Model 1: Product Search**
```json
// Denormalized for fast queries
{
  "productId": "uuid",
  "name": "Wireless Mouse",
  "category": "Electronics > Accessories",
  "price": {
    "USD": 29.99,
    "EUR": 27.50
  },
  "inventory": {
    "total": 150,
    "available": 145
  },
  "searchableText": "wireless mouse electronics accessories"
}
```

**Read Model 2: Admin Dashboard**
```json
{
  "productId": "uuid",
  "name": "Wireless Mouse",
  "sales": {
    "today": 15,
    "thisWeek": 87,
    "thisMonth": 324
  },
  "inventory": {
    "warehouse1": 75,
    "warehouse2": 70
  },
  "priceHistory": [...]
}
```

## Domain-Driven Design (DDD)

### Strategic Design

#### Bounded Contexts
```
E-Commerce Platform:

Sales Context:
├── Entities: Order, OrderItem, Cart
├── Value Objects: Money, Address
├── Aggregates: Order (root), OrderItem
└── Domain Events: OrderPlaced, OrderShipped

Inventory Context:
├── Entities: Product, Stock
├── Value Objects: SKU, Quantity
├── Aggregates: Product (root)
└── Domain Events: StockUpdated, LowStockAlert

Shipping Context:
├── Entities: Shipment, Package
├── Value Objects: TrackingNumber, DeliveryAddress
├── Aggregates: Shipment (root)
└── Domain Events: ShipmentDispatched, Delivered
```

#### Context Mapping
```
Sales Context → Inventory Context (Anti-Corruption Layer)
├── Sales uses "Product" (own model)
├── Inventory uses "StockItem" (own model)
└── Translator maps between models

Sales Context ← Shipping Context (Customer-Supplier)
├── Sales creates Shipment requests
└── Shipping fulfills requests
```

### Tactical Design

#### Aggregate Pattern
```python
# Order Aggregate (enforces invariants)
class Order:
    def __init__(self, order_id, customer_id):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = []
        self.status = OrderStatus.PENDING
    
    def add_item(self, product_id, quantity, price):
        # Invariant: Max 50 items per order
        if len(self.items) >= 50:
            raise DomainException("Order exceeds max items")
        
        # Invariant: Quantity must be positive
        if quantity <= 0:
            raise DomainException("Invalid quantity")
        
        self.items.append(OrderItem(product_id, quantity, price))
        self._raise_event(ItemAddedToOrder(...))
    
    def place_order(self):
        # Invariant: Order must have items
        if not self.items:
            raise DomainException("Cannot place empty order")
        
        # Invariant: Can only place pending orders
        if self.status != OrderStatus.PENDING:
            raise DomainException("Order already placed")
        
        self.status = OrderStatus.PLACED
        self._raise_event(OrderPlaced(...))
```

**Aggregate Rules:**
- One aggregate root per aggregate
- External references by ID only
- Invariants enforced within boundary
- Transactions within single aggregate

## API Gateway Patterns

### Backend for Frontend (BFF)
```
Mobile App → Mobile BFF API → Microservices
Web App → Web BFF API → Microservices
Admin Portal → Admin BFF API → Microservices
```

**Why BFF:**
- Mobile needs compact responses (bandwidth)
- Web needs richer data (fast network)
- Admin needs different permissions
- Avoid over-fetching/under-fetching

**Example:**
```javascript
// Mobile BFF (compact response)
GET /api/mobile/product/123
{
  "id": "123",
  "name": "Wireless Mouse",
  "price": 29.99,
  "imageUrl": "thumb_150x150.jpg"
}

// Web BFF (rich response)
GET /api/web/product/123
{
  "id": "123",
  "name": "Wireless Mouse",
  "description": "...",
  "price": 29.99,
  "images": ["full_1.jpg", "full_2.jpg"],
  "reviews": [...],
  "recommendations": [...]
}
```

### GraphQL Gateway
**Use When:**
- Clients need flexible queries
- Multiple data sources aggregation
- Real-time subscriptions needed

**Strengths:**
- Single endpoint
- Client-defined responses
- Strong typing
- Real-time (subscriptions)

**Challenges:**
- N+1 query problem
- Caching complexity
- Query cost management
- Learning curve

## Saga Pattern (Distributed Transactions)

### Choreography-Based Saga
```
Order Service → OrderPlaced event → Kafka
                                     ↓
Inventory Service (reserves stock) → StockReserved event
                                     ↓
Payment Service (charges card) → PaymentCompleted event
                                     ↓
Shipping Service (creates shipment) → ShipmentCreated event
```

**Compensation Flow (if Payment fails):**
```
Payment Service → PaymentFailed event → Kafka
                                        ↓
Inventory Service (releases stock) → StockReleased event
                                        ↓
Order Service (cancels order) → OrderCancelled event
```

### Orchestration-Based Saga
```
Order Orchestrator:
1. Send "ReserveStock" command → Inventory Service
2. Wait for response
3. If success, send "ProcessPayment" command → Payment Service
4. Wait for response
5. If success, send "CreateShipment" command → Shipping Service
6. If any failure, trigger compensation
```

**When to Use:**
- Choreography: Simple flows, decoupled services
- Orchestration: Complex flows, centralized control

## Performance Optimization Patterns

### Caching Strategies

#### 1. Cache-Aside (Lazy Loading)
```python
def get_user(user_id):
    # Check cache first
    cached_user = redis.get(f"user:{user_id}")
    if cached_user:
        return json.loads(cached_user)
    
    # Cache miss, fetch from DB
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    
    # Populate cache
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    
    return user
```

#### 2. Write-Through Cache
```python
def update_user(user_id, data):
    # Update database
    db.execute("UPDATE users SET ... WHERE id = ?", user_id, data)
    
    # Update cache immediately
    redis.setex(f"user:{user_id}", 3600, json.dumps(data))
```

#### 3. Cache Invalidation Strategies
- **TTL:** Time-based expiration (simple, stale data possible)
- **Event-Based:** Invalidate on write events (complex, consistent)
- **Versioning:** Cache key includes version (safe, more storage)

### Database Sharding

#### Horizontal Sharding (by User ID)
```
Users 1-1M → Shard 1
Users 1M-2M → Shard 2
Users 2M-3M → Shard 3

Routing: user_id % shard_count = shard_id
```

**Challenges:**
- Cross-shard queries (expensive)
- Rebalancing (hotspot shards)
- Transactions across shards

#### Vertical Sharding (by Table)
```
User Database: users, profiles, preferences
Order Database: orders, order_items, payments
Product Database: products, categories, reviews
```

---

**Key Takeaway:** Architecture patterns are tools, not dogma. Choose based on actual requirements, team size, and complexity—not hype. Start simple, evolve as needed.
