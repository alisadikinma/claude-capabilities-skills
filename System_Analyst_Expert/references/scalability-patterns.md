# Scalability Patterns - High-Performance Systems

## Horizontal vs Vertical Scaling

**Vertical Scaling (Scale Up):**
- Add more CPU/RAM to single server
- Limits: Physical hardware limits, single point of failure
- Use when: Stateful applications, legacy monoliths

**Horizontal Scaling (Scale Out):**
- Add more servers
- Benefits: No theoretical limit, fault tolerance
- Use when: Stateless services, microservices

---

## Load Balancing

### Algorithms

**Round Robin:**
```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A (repeat)
```

**Least Connections:**
```
Server A: 5 active connections
Server B: 3 active connections
Server C: 7 active connections
→ Route new request to Server B
```

**IP Hash (Sticky Sessions):**
```python
def get_server(client_ip):
    server_index = hash(client_ip) % num_servers
    return servers[server_index]
```

### Layer 4 vs Layer 7 Load Balancing

**Layer 4 (Transport):**
- Routes based on IP + port
- Fast (no content inspection)
- Use: TCP/UDP traffic

**Layer 7 (Application):**
- Routes based on HTTP headers, URL path, cookies
- Slower (parses HTTP)
- Use: API gateways, content-based routing

**Example (Nginx):**
```nginx
upstream backend {
    least_conn;  # Load balancing algorithm
    server backend1.example.com:8080 weight=3;
    server backend2.example.com:8080 weight=2;
    server backend3.example.com:8080 backup;  # Only if others fail
}

server {
    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout invalid_header http_500;
    }
}
```

---

## Caching Strategies

### Cache-Aside (Lazy Loading)

```python
def get_user(user_id):
    # 1. Check cache
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # 2. Cache miss → query DB
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    
    # 3. Populate cache (TTL: 1 hour)
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    
    return user
```

### Write-Through Cache

```python
def update_user(user_id, data):
    # 1. Update database
    db.execute("UPDATE users SET ... WHERE id = %s", user_id, data)
    
    # 2. Update cache immediately
    redis.setex(f"user:{user_id}", 3600, json.dumps(data))
```

### Write-Behind Cache (Deferred Write)

```python
def update_user(user_id, data):
    # 1. Update cache immediately
    redis.setex(f"user:{user_id}", 3600, json.dumps(data))
    
    # 2. Queue DB write (async)
    queue.enqueue(update_database, user_id, data)
```

### Cache Invalidation Strategies

**Time-Based (TTL):**
```python
redis.setex(key, ttl_seconds, value)
```

**Event-Based:**
```python
# On user update
def on_user_updated(user_id):
    redis.delete(f"user:{user_id}")
    redis.delete(f"user:{user_id}:orders")  # Related caches
```

**Cache Stampede Prevention:**
```python
def get_with_lock(key, fetch_fn):
    cached = redis.get(key)
    if cached:
        return cached
    
    # Acquire lock to prevent multiple fetches
    lock_key = f"lock:{key}"
    if redis.setnx(lock_key, 1):
        redis.expire(lock_key, 10)  # 10-second lock
        
        try:
            value = fetch_fn()
            redis.setex(key, 3600, value)
            return value
        finally:
            redis.delete(lock_key)
    else:
        # Wait for lock holder to populate cache
        time.sleep(0.1)
        return get_with_lock(key, fetch_fn)
```

---

## Database Scaling

### Read Replicas

```
Primary (Write): 1 server
Read Replicas: 3 servers

Application Logic:
- Writes → Primary
- Reads → Load balance across replicas
```

**Replication Lag Handling:**
```python
def update_user(user_id, data):
    # Write to primary
    db_primary.execute("UPDATE users SET ... WHERE id = %s", user_id, data)
    
    # Read from primary for consistency (read-after-write)
    return db_primary.query("SELECT * FROM users WHERE id = %s", user_id)

def list_users():
    # Read from replica (eventual consistency acceptable)
    return db_replica.query("SELECT * FROM users")
```

### Sharding (Horizontal Partitioning)

**By User ID:**
```python
def get_shard(user_id):
    shard_count = 16
    shard_id = user_id % shard_count
    return database_connections[shard_id]

def get_user(user_id):
    shard = get_shard(user_id)
    return shard.query("SELECT * FROM users WHERE id = %s", user_id)
```

**Challenges:**
- Cross-shard queries expensive
- Rebalancing shards difficult
- Hotspot shards (uneven distribution)

**Consistent Hashing (Better):**
```python
import hashlib

def get_shard_consistent(user_id, num_shards=16):
    hash_val = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16)
    return hash_val % num_shards
```

---

## Message Queues & Async Processing

### Use Cases

**Background Jobs:**
```python
# Synchronous (blocks request)
def send_email(user_id):
    email = get_user_email(user_id)
    smtp.send(email, "Welcome!")  # 2 seconds
    return {"status": "sent"}

# Asynchronous (returns immediately)
from celery import Celery
celery_app = Celery('tasks', broker='redis://localhost')

@celery_app.task
def send_email_async(user_id):
    email = get_user_email(user_id)
    smtp.send(email, "Welcome!")

def signup_user(user_data):
    user_id = create_user(user_data)
    send_email_async.delay(user_id)  # Queue for background processing
    return {"user_id": user_id, "status": "created"}
```

### Queue Patterns

**Point-to-Point (Work Queue):**
```
Producer → Queue → Consumer 1
                 → Consumer 2 (one consumer gets each message)
```

**Publish-Subscribe:**
```
Publisher → Topic → Subscriber 1 (gets all messages)
                 → Subscriber 2 (gets all messages)
```

**Example (Kafka):**
```python
from kafka import KafkaProducer, KafkaConsumer

# Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('order-events', b'{"order_id": 123, "status": "placed"}')

# Consumer
consumer = KafkaConsumer('order-events', bootstrap_servers='localhost:9092')
for message in consumer:
    process_order_event(message.value)
```

---

## CDN (Content Delivery Network)

### Benefits

- Reduced latency (serve from edge locations)
- Reduced origin server load
- DDoS protection

### Cache Control Headers

```http
Cache-Control: public, max-age=31536000, immutable  # 1 year (static assets)
Cache-Control: private, max-age=3600  # 1 hour (user-specific)
Cache-Control: no-cache  # Revalidate every time
Cache-Control: no-store  # Never cache (sensitive data)
```

### CloudFront Configuration

```json
{
  "Origins": [
    {
      "DomainName": "origin.example.com",
      "OriginPath": "/assets"
    }
  ],
  "DefaultCacheBehavior": {
    "TargetOriginId": "origin",
    "ViewerProtocolPolicy": "redirect-to-https",
    "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",  # CachingOptimized
    "Compress": true
  }
}
```

---

## Connection Pooling

### Database Connection Pool

**Why:**
- Opening connections expensive (TCP handshake, authentication)
- Limit concurrent connections to DB

**Configuration (Python SQLAlchemy):**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=20,           # Normal pool size
    max_overflow=10,        # Extra connections if pool exhausted
    pool_timeout=30,        # Wait 30s for connection
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True      # Verify connection before use
)
```

---

## Auto-Scaling

### Metrics-Based Scaling

**CPU-Based:**
```yaml
# AWS Auto Scaling Policy
TargetTrackingScalingPolicyConfiguration:
  TargetValue: 70.0
  PredefinedMetricSpecification:
    PredefinedMetricType: ASGAverageCPUUtilization
```

**Request-Based:**
```yaml
TargetTrackingScalingPolicyConfiguration:
  TargetValue: 1000  # 1000 requests per target
  PredefinedMetricSpecification:
    PredefinedMetricType: ALBRequestCountPerTarget
```

### Scheduled Scaling

```yaml
# Scale up before business hours
ScheduledAction:
  - ScheduleName: scale-up-morning
    Recurrence: "0 8 * * MON-FRI"  # 8 AM weekdays
    MinSize: 10
    MaxSize: 50
    DesiredCapacity: 20
  
  - ScheduleName: scale-down-evening
    Recurrence: "0 20 * * *"  # 8 PM daily
    MinSize: 3
    MaxSize: 10
    DesiredCapacity: 5
```

---

## Rate Limiting & Throttling

### Token Bucket Algorithm

```python
import time
from redis import Redis

redis_client = Redis()

def allow_request(user_id, bucket_size=100, refill_rate=10):
    """
    bucket_size: Max tokens in bucket
    refill_rate: Tokens added per second
    """
    key = f"rate_limit:{user_id}"
    now = time.time()
    
    # Get current state
    data = redis_client.hgetall(key)
    if not data:
        tokens = bucket_size
        last_refill = now
    else:
        tokens = float(data[b'tokens'])
        last_refill = float(data[b'last_refill'])
    
    # Refill tokens based on time elapsed
    time_elapsed = now - last_refill
    tokens = min(bucket_size, tokens + (time_elapsed * refill_rate))
    
    # Check if request allowed
    if tokens >= 1:
        tokens -= 1
        redis_client.hmset(key, {'tokens': tokens, 'last_refill': now})
        redis_client.expire(key, 3600)
        return True
    else:
        return False  # Rate limit exceeded
```

---

## Circuit Breaker Pattern

```python
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = 1  # Normal operation
    OPEN = 2    # Failing, reject requests
    HALF_OPEN = 3  # Testing if recovered

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker OPEN")
        
        try:
            result = func(*args, **kwargs)
            
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            
            raise e

# Usage
cb = CircuitBreaker(failure_threshold=3, timeout=30)
result = cb.call(external_api_call, param1, param2)
```

---

## Performance Benchmarks

### Load Testing (k6)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp-up to 100 users
    { duration: '5m', target: 100 },   // Stay at 100 users
    { duration: '2m', target: 200 },   // Ramp-up to 200 users
    { duration: '5m', target: 200 },   // Stay at 200 users
    { duration: '2m', target: 0 },     // Ramp-down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],   // Error rate < 1%
  },
};

export default function () {
  let res = http.get('https://api.example.com/users');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

---

## Scalability Checklist

**Application:**
- [ ] Stateless services (enable horizontal scaling)
- [ ] Async processing (queues for heavy tasks)
- [ ] Connection pooling (DB, HTTP clients)
- [ ] Circuit breakers (prevent cascade failures)

**Caching:**
- [ ] CDN for static assets
- [ ] Redis for application cache
- [ ] Database query cache

**Database:**
- [ ] Read replicas (scale reads)
- [ ] Sharding (scale writes)
- [ ] Indexes optimized

**Infrastructure:**
- [ ] Load balancer (distribute traffic)
- [ ] Auto-scaling (handle traffic spikes)
- [ ] Multi-AZ deployment (fault tolerance)

**Monitoring:**
- [ ] Performance metrics (latency, throughput)
- [ ] Resource utilization (CPU, memory, network)
- [ ] Error rates & alerting
- [ ] Load testing (quarterly)

---

**Key Insight:** Premature optimization is root of all evil, but planning for scale from day one prevents costly rewrites. Design for 10x, build for 2x.
