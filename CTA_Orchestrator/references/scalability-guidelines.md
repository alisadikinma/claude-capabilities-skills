# Scalability Guidelines

## Scalability Dimensions

```
┌─────────────────────────────────────────┐
│         Horizontal Scaling              │
│  (Add more servers/instances)           │
├─────────────────────────────────────────┤
│         Vertical Scaling                │
│  (Increase server resources)            │
├─────────────────────────────────────────┤
│         Functional Scaling              │
│  (Split by features/services)           │
├─────────────────────────────────────────┤
│         Data Scaling                    │
│  (Partitioning, sharding, caching)      │
└─────────────────────────────────────────┘
```

---

## 1. Performance Targets

### Response Time Benchmarks

| Operation Type | Target (p95) | Acceptable (p99) | Action If Exceeded |
|----------------|--------------|------------------|-------------------|
| **Page Load** | < 1s | < 3s | Optimize frontend, CDN |
| **API Request** | < 200ms | < 500ms | Cache, optimize queries |
| **Database Query** | < 50ms | < 100ms | Add indexes, optimize |
| **Search Query** | < 100ms | < 300ms | Elasticsearch, caching |
| **Real-time Updates** | < 100ms | < 500ms | WebSocket optimization |
| **File Upload** | Varies | - | Chunked upload, CDN |

### Throughput Targets

| Scale | Users | Requests/Second | Strategy |
|-------|-------|-----------------|----------|
| **Small** | < 1K | < 10 | Single server |
| **Medium** | 1K-10K | 10-100 | Load balancing |
| **Large** | 10K-100K | 100-1K | Horizontal scaling |
| **Very Large** | 100K-1M | 1K-10K | Microservices, CDN |
| **Massive** | > 1M | > 10K | Global distribution |

---

## 2. Vertical Scaling

### When to Scale Vertically

**Good For:**
- ✅ Database servers (PostgreSQL, MySQL)
- ✅ In-memory caches (Redis)
- ✅ Stateful applications
- ✅ Quick wins before horizontal scaling
- ✅ Simplicity (no code changes)

**Bad For:**
- ❌ Web/API servers (limited by single machine)
- ❌ Long-term strategy (ceiling is low)
- ❌ High availability (single point of failure)

### Vertical Scaling Progression

```
Phase 1: Optimize First
    - Fix N+1 queries
    - Add database indexes
    - Implement caching
    - Optimize algorithms
    
Phase 2: Upgrade Resources
    - 2 vCPU → 4 vCPU
    - 4GB RAM → 8GB RAM
    - Standard disk → SSD
    
Phase 3: Specialized Hardware
    - 8 vCPU → 16 vCPU
    - 8GB RAM → 32GB RAM
    - Enable CPU optimizations
    
Phase 4: Plan Horizontal Scaling
    - Vertical scaling limits reached
    - Cost-benefit favors horizontal
```

### Cost vs Performance

| Instance Type | vCPU | RAM | Cost/Month | Use Case |
|---------------|------|-----|------------|----------|
| **t3.micro** | 2 | 1GB | $7 | Dev/test |
| **t3.small** | 2 | 2GB | $15 | Small apps |
| **t3.medium** | 2 | 4GB | $30 | Medium apps |
| **t3.large** | 2 | 8GB | $60 | Database |
| **m5.xlarge** | 4 | 16GB | $140 | High memory |
| **c5.2xlarge** | 8 | 16GB | $250 | CPU intensive |

**Optimization Tip:** Often 2x cost ≠ 2x performance. Test before upgrading.

---

## 3. Horizontal Scaling

### Stateless Application Design

**Requirements for Horizontal Scaling:**

```python
# ❌ Stateful (Cannot scale horizontally)
user_sessions = {}  # In-memory, lost on restart

def login(user_id):
    user_sessions[user_id] = {"logged_in": True}

# ✅ Stateless (Scales horizontally)
def login(user_id):
    redis.set(f"session:{user_id}", {"logged_in": True}, ex=3600)
```

**Checklist for Statelessness:**
- [ ] Session data in Redis/database (not in-memory)
- [ ] File uploads to S3/object storage (not local disk)
- [ ] Background jobs in queue (not in-app threads)
- [ ] Logs to centralized system (not local files)
- [ ] Configuration from environment (not local files)

### Load Balancing

**Load Balancer Algorithms:**

```
Round Robin:
    Server 1 → Server 2 → Server 3 → Server 1
    Simple, even distribution
    
Least Connections:
    Route to server with fewest active connections
    Better for long-running requests
    
IP Hash:
    Hash client IP → Always same server
    Session affinity without sticky sessions
    
Weighted:
    Server 1 (70%) → Server 2 (20%) → Server 3 (10%)
    For gradual rollouts or heterogeneous servers
```

**Implementation:**

```nginx
# Nginx Load Balancer
upstream backend {
    least_conn;  # Algorithm
    server app1:8000 weight=3;
    server app2:8000 weight=2;
    server app3:8000 weight=1;
    
    # Health checks
    server app4:8000 backup;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Auto-Scaling

**Metrics-Based Scaling:**

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**Scaling Triggers:**

| Metric | Scale Up When | Scale Down When |
|--------|---------------|-----------------|
| **CPU Usage** | > 70% for 5 min | < 30% for 10 min |
| **Memory Usage** | > 80% for 5 min | < 40% for 10 min |
| **Request Queue** | > 100 pending | < 10 pending |
| **Response Time** | p95 > 500ms | p95 < 100ms |
| **Error Rate** | > 5% for 2 min | < 1% stable |

---

## 4. Database Scaling

### Query Optimization

**Common Issues & Solutions:**

```sql
-- ❌ N+1 Query Problem
SELECT * FROM posts;
-- Then for each post:
SELECT * FROM comments WHERE post_id = ?;

-- ✅ Solution: JOIN or eager loading
SELECT p.*, c.* FROM posts p
LEFT JOIN comments c ON p.id = c.post_id;

-- ❌ Missing Index
SELECT * FROM users WHERE email = 'user@example.com';
-- Full table scan: 10,000ms

-- ✅ Add Index
CREATE INDEX idx_users_email ON users(email);
-- Index lookup: 5ms
```

**Indexing Strategy:**

```
Index if:
- Column in WHERE clause (frequently)
- Column in JOIN condition
- Column in ORDER BY (with WHERE)
- Foreign keys

Don't over-index:
- Write performance penalty
- Storage overhead
- Maintenance cost
```

### Read Replicas

**Architecture:**

```
┌──────────────┐         ┌──────────────┐
│   Primary    │ Replicate│   Replica 1  │
│   (Writes)   ├────────>│   (Reads)    │
└──────────────┘         └──────────────┘
                         ┌──────────────┐
                         │   Replica 2  │
                         │   (Reads)    │
                         └──────────────┘
```

**Read/Write Split:**

```python
# Write to primary
def create_user(email, password):
    db_primary.execute(
        "INSERT INTO users (email, password) VALUES (?, ?)",
        (email, hash_password(password))
    )

# Read from replica
def get_user(email):
    return db_replica.query(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )
```

**Considerations:**
- Replication lag (typically < 100ms)
- Read-after-write consistency issues
- Solution: Read from primary for critical data

### Connection Pooling

```python
# ❌ Without pooling (slow, resource-intensive)
def query_db():
    conn = psycopg2.connect(...)  # New connection every time
    cursor = conn.cursor()
    cursor.execute("SELECT ...")
    conn.close()

# ✅ With pooling (fast, efficient)
from psycopg2.pool import ThreadedConnectionPool

pool = ThreadedConnectionPool(
    minconn=5,    # Minimum connections
    maxconn=20,   # Maximum connections
    host="...",
    database="..."
)

def query_db():
    conn = pool.getconn()  # Reuse existing connection
    cursor = conn.cursor()
    cursor.execute("SELECT ...")
    pool.putconn(conn)  # Return to pool
```

### Sharding (Horizontal Partitioning)

**Sharding Strategies:**

**1. Range-Based Sharding:**
```
Shard 1: User ID 1-1,000,000
Shard 2: User ID 1,000,001-2,000,000
Shard 3: User ID 2,000,001-3,000,000
```

**2. Hash-Based Sharding:**
```python
def get_shard(user_id):
    return hash(user_id) % num_shards
```

**3. Geographic Sharding:**
```
Shard US-East: US users
Shard EU: European users
Shard Asia: Asian users
```

**Implementation Considerations:**
- Cross-shard queries are expensive
- Resharding is complex
- Application-level logic needed
- Consider: Vitess (MySQL), Citus (PostgreSQL)

---

## 5. Caching Strategies

### Cache Hierarchy

```
1. Browser Cache (Static assets)
   ↓ miss
2. CDN Cache (Global edge)
   ↓ miss
3. Application Cache (In-memory)
   ↓ miss
4. Redis Cache (Distributed)
   ↓ miss
5. Database Query Cache
   ↓ miss
6. Database (Source of truth)
```

### Cache Sizing Guidelines

| Data Type | Cache Hit Rate Target | TTL |
|-----------|----------------------|-----|
| **Static Assets** | 95%+ | 1 year |
| **API Responses** | 70-80% | 5-60 min |
| **Database Queries** | 80-90% | 15-60 min |
| **Session Data** | 99%+ | Session lifetime |
| **User Profiles** | 90%+ | 1-24 hours |

### Cache Invalidation Patterns

```python
# 1. Time-based (TTL)
redis.setex("user:123", 3600, user_data)  # 1 hour

# 2. Event-based (On update)
def update_user(user_id, data):
    db.update(user_id, data)
    redis.delete(f"user:{user_id}")  # Invalidate

# 3. Version-based
def get_user(user_id):
    version = redis.get(f"user_version:{user_id}") or 0
    key = f"user:{user_id}:v{version}"
    # ...

def update_user(user_id, data):
    db.update(user_id, data)
    redis.incr(f"user_version:{user_id}")  # Bump version
```

### Cache Stampede Prevention

```python
import threading

lock = threading.Lock()
computing = set()

def get_expensive_data(key):
    # Check cache
    cached = redis.get(key)
    if cached:
        return cached
    
    # Prevent multiple computes
    if key in computing:
        time.sleep(0.1)  # Wait for other thread
        return get_expensive_data(key)  # Retry
    
    with lock:
        if key in computing:
            return None
        computing.add(key)
    
    try:
        # Compute expensive data
        data = compute_expensive_data()
        redis.setex(key, 3600, data)
        return data
    finally:
        computing.remove(key)
```

---

## 6. Content Delivery Network (CDN)

### What to Cache on CDN

**Highly Cacheable (Cache-Control: public, max-age=31536000):**
- CSS/JS with hash in filename
- Images, fonts, videos
- Versioned static assets

**Moderately Cacheable (Cache-Control: public, max-age=3600):**
- HTML pages (for logged-out users)
- API responses (public data)
- Thumbnails, resized images

**Never Cache:**
- User-specific data
- Admin pages
- Dynamic, personalized content
- API endpoints with authentication

### CDN Configuration

```nginx
# Cloudflare Page Rule Example
Cache Level: Cache Everything
Edge Cache TTL: 1 month
Browser Cache TTL: 1 year

# For versioned assets
/assets/app.abc123.js → Max cache
/assets/logo.png → Max cache

# For dynamic content
/api/* → Bypass cache
/user/* → Bypass cache
```

---

## 7. Asynchronous Processing

### When to Use Async

**Good Candidates:**
- Email sending
- Report generation
- Image processing
- Video encoding
- Data imports/exports
- Third-party API calls

**Implementation:**

```python
# Celery (Python)
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def send_email(to, subject, body):
    # Time-consuming email sending
    smtp.send(to, subject, body)

# Usage in web request
def register_user(email, password):
    user = create_user(email, password)
    
    # Don't block on email
    send_email.delay(email, "Welcome!", "...")
    
    return {"success": True}
```

### Queue Sizing

```
Queue Depth Thresholds:
< 10:     Normal
10-100:   Monitor
100-1000: Scale workers
> 1000:   Alert, urgent action

Worker Sizing:
Workers = Throughput_target / Task_duration

Example:
Need 1000 tasks/min
Task takes 6 seconds
Workers = 1000/10 = 100 workers
```

---

## 8. Microservices Scaling

### Service Decomposition

**When to Split:**
- Service > 10K LOC
- Team > 10 people
- Different scaling needs
- Different release cycles
- Clear bounded context

**Service Sizing Guidelines:**

| Metric | Target | Max |
|--------|--------|-----|
| **Lines of Code** | 1K-5K | 10K |
| **Team Size** | 2-5 | 8 |
| **Dependencies** | < 5 | 10 |
| **Database Tables** | < 20 | 50 |
| **API Endpoints** | 5-20 | 50 |

### Service Mesh Benefits

```
Without Service Mesh:
- Each service implements: retry, circuit breaker, metrics, tracing
- Duplicated logic
- Hard to update

With Service Mesh (Istio, Linkerd):
- Automatic: retry, circuit breaker, metrics, tracing
- Traffic management
- Security (mTLS)
```

---

## 9. Monitoring & Alerting

### Key Metrics (RED Method)

**Rate:**
- Requests per second
- Alert: Spike > 3x normal

**Errors:**
- Error rate percentage
- Alert: > 1% for 5 min

**Duration:**
- Response time (p50, p95, p99)
- Alert: p95 > threshold for 5 min

### Capacity Planning

```
Current Capacity Assessment:
- Peak RPS: 500
- Average CPU: 40%
- Average Memory: 60%
- Buffer: 20%

Growth Projection:
- User growth: 20% per quarter
- In 1 year: 2.5x load

Action Plan:
- Q2: Add 1 server
- Q3: Add 2 servers
- Q4: Implement caching (reduce load 30%)
```

---

## 10. Scalability Testing

### Load Testing

**k6 Example:**

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 500 },  // Spike to 500
    { duration: '5m', target: 500 },  // Stay at 500
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% < 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
  },
};

export default function () {
  let res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  sleep(1);
}
```

### Chaos Engineering

**Test Failure Scenarios:**
- Kill random pods/containers
- Inject network latency
- Simulate database failures
- Throttle API endpoints
- Fill disk space

**Tools:**
- Chaos Monkey (Netflix)
- Litmus Chaos (Kubernetes)
- Gremlin

---

## Scalability Checklist

### Before Scaling
- [ ] Profile application (find bottlenecks)
- [ ] Optimize queries (indexes, N+1)
- [ ] Implement caching
- [ ] Add monitoring
- [ ] Load test current system
- [ ] Document baseline metrics

### Scaling Strategy
- [ ] Start with vertical scaling (quick win)
- [ ] Add caching layer (Redis, CDN)
- [ ] Implement read replicas
- [ ] Horizontal scaling (stateless apps)
- [ ] Consider microservices (if needed)
- [ ] Database sharding (last resort)

### Post-Scaling
- [ ] Verify metrics improved
- [ ] Monitor for regressions
- [ ] Update runbooks
- [ ] Review costs
- [ ] Plan next scaling phase

---

**Key Principle:** Scale incrementally. Measure impact. Optimize before adding resources.
