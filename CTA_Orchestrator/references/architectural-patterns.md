# Architectural Patterns Reference Guide

## Table of Contents
1. Layered Architecture
2. Hexagonal Architecture (Ports & Adapters)
3. Clean Architecture
4. Domain-Driven Design (DDD)
5. CQRS (Command Query Responsibility Segregation)
6. Event Sourcing
7. Microservices Patterns
8. API Gateway Pattern
9. Backend for Frontend (BFF)
10. Strangler Fig Pattern

---

## 1. Layered Architecture

### Overview
Traditional N-tier architecture separating concerns into horizontal layers.

### Structure
```
┌─────────────────────────────┐
│   Presentation Layer        │
│   (UI, Controllers, API)    │
└──────────┬──────────────────┘
           │ depends on
┌──────────▼──────────────────┐
│   Business Logic Layer      │
│   (Services, Domain Logic)  │
└──────────┬──────────────────┘
           │ depends on
┌──────────▼──────────────────┐
│   Data Access Layer         │
│   (Repositories, ORM)       │
└──────────┬──────────────────┘
           │ depends on
┌──────────▼──────────────────┐
│   Database                  │
└─────────────────────────────┘
```

### Implementation Example (Laravel)

```php
// Presentation Layer (Controller)
class UserController extends Controller {
    public function __construct(
        private UserService $userService
    ) {}
    
    public function store(Request $request) {
        $user = $this->userService->createUser($request->validated());
        return response()->json($user, 201);
    }
}

// Business Logic Layer (Service)
class UserService {
    public function __construct(
        private UserRepository $userRepository
    ) {}
    
    public function createUser(array $data): User {
        // Business logic
        $data['password'] = Hash::make($data['password']);
        return $this->userRepository->create($data);
    }
}

// Data Access Layer (Repository)
class UserRepository {
    public function create(array $data): User {
        return User::create($data);
    }
}
```

### Pros & Cons

**Pros:**
- Simple to understand
- Clear separation of concerns
- Easy to test each layer
- Standard pattern, widely known

**Cons:**
- Can lead to tight coupling
- Changes ripple through layers
- Business logic can leak to other layers
- Database-centric design

**Best For:** Traditional web apps, CRUD applications, small-medium projects

---

## 2. Hexagonal Architecture (Ports & Adapters)

### Overview
Isolate core business logic from external concerns using ports (interfaces) and adapters (implementations).

### Structure
```
         External Systems
         (DB, API, UI)
               │
        ┌──────▼──────┐
        │   Adapters  │ (Implementations)
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │    Ports    │ (Interfaces)
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   Domain    │ (Core Logic)
        │   (Hexagon) │
        └─────────────┘
```

### Implementation Example (Python)

```python
# Port (Interface)
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

# Domain (Core Logic)
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def register_user(self, email: str, password: str) -> User:
        # Business logic (no knowledge of DB)
        if self.user_repository.find_by_email(email):
            raise ValueError("Email already exists")
        
        user = User(email=email, password=hash_password(password))
        return self.user_repository.save(user)

# Adapter (Implementation)
class PostgresUserRepository(UserRepository):
    def save(self, user: User) -> User:
        # PostgreSQL specific implementation
        db.session.add(user)
        db.session.commit()
        return user
    
    def find_by_email(self, email: str) -> Optional[User]:
        return db.session.query(User).filter_by(email=email).first()

# Alternative Adapter
class MongoUserRepository(UserRepository):
    def save(self, user: User) -> User:
        # MongoDB specific implementation
        return mongo_db.users.insert_one(user.to_dict())
```

### Pros & Cons

**Pros:**
- Business logic completely isolated
- Easy to swap implementations
- Highly testable (mock adapters)
- Technology-agnostic core

**Cons:**
- More initial complexity
- More code (interfaces + implementations)
- Can be overkill for simple apps

**Best For:** Complex domain logic, systems requiring multiple adapters, long-term maintainability

---

## 3. Clean Architecture

### Overview
Concentric circles with dependencies pointing inward. Combines ideas from Hexagonal, Onion, and other architectures.

### Structure
```
┌─────────────────────────────────────┐
│  Frameworks & Drivers (Web, DB)    │
│  ┌──────────────────────────────┐  │
│  │  Interface Adapters          │  │
│  │  (Controllers, Presenters)   │  │
│  │  ┌───────────────────────┐   │  │
│  │  │  Use Cases            │   │  │
│  │  │  (Application Logic)  │   │  │
│  │  │  ┌────────────────┐   │   │  │
│  │  │  │  Entities      │   │   │  │
│  │  │  │  (Domain)      │   │   │  │
│  │  │  └────────────────┘   │   │  │
│  │  └───────────────────────┘   │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
    Dependencies flow inward →
```

### Implementation Example

```python
# Entities (Domain)
class User:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    
    def validate(self):
        if not self.email:
            raise ValueError("Email required")

# Use Cases (Application Logic)
class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, request: RegisterUserRequest) -> User:
        # Validate
        if self.user_repository.exists_by_email(request.email):
            raise ValueError("User exists")
        
        # Create entity
        user = User(request.email, hash_password(request.password))
        user.validate()
        
        # Save
        return self.user_repository.save(user)

# Interface Adapters (Controllers)
class UserController:
    def __init__(self, register_use_case: RegisterUserUseCase):
        self.register_use_case = register_use_case
    
    def register(self, request):
        user = self.register_use_case.execute(
            RegisterUserRequest(
                email=request.json['email'],
                password=request.json['password']
            )
        )
        return jsonify({"id": user.id, "email": user.email})

# Frameworks & Drivers
# (Flask, FastAPI, Django, etc.)
```

### Dependency Rule
- Source code dependencies point inward
- Inner circles know nothing about outer circles
- Data formats should not cross boundaries unchanged

### Pros & Cons

**Pros:**
- Maximum testability
- Framework independence
- UI independence
- Database independence
- Clear separation of concerns

**Cons:**
- Steep learning curve
- Lots of boilerplate
- Can be over-engineered for simple apps

**Best For:** Enterprise applications, complex domains, long-term projects (5+ years)

---

## 4. Domain-Driven Design (DDD)

### Overview
Focus on the core domain and domain logic, using ubiquitous language and bounded contexts.

### Key Concepts

**1. Bounded Context**
```
E-commerce System:
┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐
│ Sales Context   │  │Shipping Context  │  │Billing Context  │
│                 │  │                  │  │                 │
│ - Product       │  │- Shipment        │  │- Invoice        │
│ - Order         │  │- Package         │  │- Payment        │
│ - Customer      │  │- DeliveryAddress │  │- BillingAddress │
└─────────────────┘  └──────────────────┘  └─────────────────┘
```

**2. Aggregates & Entities**
```python
# Aggregate Root
class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
    
    def add_item(self, product: Product, quantity: int):
        # Business rule: Max 10 items per order
        if len(self.items) >= 10:
            raise ValueError("Order cannot have more than 10 items")
        
        item = OrderItem(product, quantity)
        self.items.append(item)
    
    def place(self):
        # Business rule: Order must have items
        if not self.items:
            raise ValueError("Cannot place empty order")
        
        self.status = OrderStatus.PLACED
        self._emit_event(OrderPlacedEvent(self.order_id))

# Entity (part of Order aggregate)
class OrderItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
    
    def total(self) -> float:
        return self.product.price * self.quantity

# Value Object
class Money:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency
    
    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
```

**3. Domain Services**
```python
class PricingService:
    def calculate_order_total(self, order: Order) -> Money:
        # Complex pricing logic that doesn't belong to any entity
        subtotal = sum(item.total() for item in order.items)
        discount = self._calculate_discount(order)
        tax = self._calculate_tax(subtotal - discount)
        return Money(subtotal - discount + tax, "USD")
```

**4. Repositories**
```python
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    @abstractmethod
    def find_by_customer(self, customer_id: str) -> List[Order]:
        pass
```

### Strategic Design Patterns

**Context Mapping:**
```
┌─────────────────┐         ┌──────────────────┐
│  Sales Context  │         │Inventory Context │
│                 │         │                  │
│  - Order        │◄────────┤ - Stock          │
│  - Product      │  ACL    │ - Warehouse      │
└─────────────────┘         └──────────────────┘

ACL = Anti-Corruption Layer
(Translation between contexts)
```

### Pros & Cons

**Pros:**
- Aligns code with business
- Ubiquitous language
- Handles complex domains well
- Clear boundaries

**Cons:**
- High complexity
- Requires domain expertise
- Steep learning curve
- Overkill for CRUD apps

**Best For:** Complex business domains, enterprise systems, long-term projects

---

## 5. CQRS (Command Query Responsibility Segregation)

### Overview
Separate read and write models for better scalability and optimization.

### Structure
```
        Command (Write)              Query (Read)
              │                          │
    ┌─────────▼──────────┐    ┌─────────▼──────────┐
    │Command Handlers    │    │Query Handlers      │
    │(Business Logic)    │    │(Read Logic)        │
    └─────────┬──────────┘    └─────────┬──────────┘
              │                          │
    ┌─────────▼──────────┐    ┌─────────▼──────────┐
    │Write Database      │    │Read Database       │
    │(Normalized)        │    │(Denormalized)      │
    └─────────┬──────────┘    └──────────▲─────────┘
              │                          │
              └──────────Events──────────┘
```

### Implementation Example

```python
# Commands (Write)
class CreateOrderCommand:
    def __init__(self, user_id: str, items: List[dict]):
        self.user_id = user_id
        self.items = items

class CreateOrderHandler:
    def __init__(self, repository, event_bus):
        self.repository = repository
        self.event_bus = event_bus
    
    def handle(self, command: CreateOrderCommand):
        # Create aggregate
        order = Order(user_id=command.user_id)
        for item in command.items:
            order.add_item(item['product_id'], item['quantity'])
        
        # Save to write DB
        self.repository.save(order)
        
        # Publish events
        self.event_bus.publish(OrderCreatedEvent(order.id, order.user_id))

# Queries (Read)
class GetOrderQuery:
    def __init__(self, order_id: str):
        self.order_id = order_id

class GetOrderQueryHandler:
    def __init__(self, read_db):
        self.read_db = read_db
    
    def handle(self, query: GetOrderQuery):
        # Query optimized read model
        return self.read_db.query(
            "SELECT * FROM order_view WHERE id = ?",
            query.order_id
        )

# Event Handler (Sync read model)
class OrderProjection:
    def handle_order_created(self, event: OrderCreatedEvent):
        # Update denormalized read model
        self.read_db.execute(
            """
            INSERT INTO order_view (id, user_id, status, created_at)
            VALUES (?, ?, 'pending', NOW())
            """,
            (event.order_id, event.user_id)
        )
```

### Pros & Cons

**Pros:**
- Optimized reads and writes separately
- Scalability (scale read/write independently)
- Multiple read models for different uses
- Clear separation

**Cons:**
- Eventual consistency
- More complexity
- Need event synchronization
- Data duplication

**Best For:** High-traffic systems, read-heavy applications, complex reporting needs

---

## 6. Event Sourcing

### Overview
Store all state changes as a sequence of events, not just current state.

### Structure
```
Commands → Aggregate → Events → Event Store
                           ↓
                      Projections
                           ↓
                      Read Models
```

### Implementation Example

```python
# Events
@dataclass
class OrderCreatedEvent:
    order_id: str
    user_id: str
    timestamp: datetime

@dataclass
class ItemAddedEvent:
    order_id: str
    product_id: str
    quantity: int
    timestamp: datetime

# Aggregate
class Order:
    def __init__(self):
        self.id = None
        self.items = []
        self.uncommitted_events = []
    
    def create(self, order_id: str, user_id: str):
        event = OrderCreatedEvent(order_id, user_id, datetime.now())
        self._apply(event)
        self.uncommitted_events.append(event)
    
    def add_item(self, product_id: str, quantity: int):
        event = ItemAddedEvent(self.id, product_id, quantity, datetime.now())
        self._apply(event)
        self.uncommitted_events.append(event)
    
    def _apply(self, event):
        if isinstance(event, OrderCreatedEvent):
            self.id = event.order_id
        elif isinstance(event, ItemAddedEvent):
            self.items.append({'product_id': event.product_id, 'qty': event.quantity})
    
    @classmethod
    def from_events(cls, events):
        order = cls()
        for event in events:
            order._apply(event)
        return order

# Event Store
class EventStore:
    def save(self, aggregate_id: str, events: List):
        for event in events:
            self.db.insert('events', {
                'aggregate_id': aggregate_id,
                'event_type': type(event).__name__,
                'data': json.dumps(event.__dict__),
                'timestamp': event.timestamp
            })
    
    def get_events(self, aggregate_id: str) -> List:
        rows = self.db.query(
            "SELECT * FROM events WHERE aggregate_id = ? ORDER BY timestamp",
            aggregate_id
        )
        return [self._deserialize(row) for row in rows]
```

### Pros & Cons

**Pros:**
- Complete audit trail
- Temporal queries (state at any time)
- Event replay capability
- Natural fit for event-driven systems

**Cons:**
- Higher complexity
- Storage overhead
- Event schema evolution challenges
- Learning curve

**Best For:** Financial systems, audit-critical apps, event-driven architectures

---

## 7. Microservices Patterns

### Decomposition Patterns

**By Business Capability:**
```
E-commerce → User Management
           → Product Catalog
           → Order Management
           → Payment Processing
           → Shipping
```

**By Subdomain (DDD):**
```
Core Domain:    Order Processing, Pricing
Supporting:     User Management, Notifications
Generic:        Authentication, Logging
```

### Communication Patterns

**Synchronous (REST/gRPC):**
- Request-response
- Tight coupling
- Immediate consistency

**Asynchronous (Events):**
- Publish-subscribe
- Loose coupling
- Eventual consistency

### Data Management Patterns

**Database per Service:**
```
Service A → Database A
Service B → Database B
```

**Shared Database (Anti-pattern):**
```
Service A ↘
          → Shared Database
Service B ↗
```

**Saga Pattern (Distributed Transactions):**
- Choreography: Event-driven coordination
- Orchestration: Central coordinator

---

## Pattern Selection Matrix

| Pattern | Complexity | Testability | Maintainability | Best For |
|---------|------------|-------------|-----------------|----------|
| **Layered** | Low | Good | Good | Traditional apps |
| **Hexagonal** | Medium | Excellent | Excellent | Adapter flexibility |
| **Clean** | High | Excellent | Excellent | Long-term projects |
| **DDD** | Very High | Excellent | Excellent | Complex domains |
| **CQRS** | High | Good | Good | Read-heavy systems |
| **Event Sourcing** | Very High | Good | Good | Audit-critical |
| **Microservices** | Very High | Good | Medium | Large teams, scale |

---

**References:**
- Martin Fowler: Patterns of Enterprise Application Architecture
- Eric Evans: Domain-Driven Design
- Robert C. Martin: Clean Architecture
- Chris Richardson: Microservices Patterns
