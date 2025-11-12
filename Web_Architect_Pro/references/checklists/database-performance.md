# Database Performance Checklist

**Target:** Query response time < 100ms (p95)  
**Last Updated:** 2025-01-11

---

## 📊 Indexing Strategy

### Primary Indexes
- [ ] Primary key on every table
- [ ] Auto-increment integers for primary keys
- [ ] UUID/ULID only when distributed systems require it

### Secondary Indexes
- [ ] Indexes on foreign keys
- [ ] Indexes on frequently queried columns
- [ ] Composite indexes for multi-column WHERE clauses
- [ ] Index column order optimized (high cardinality first)

**Example:**
```sql
-- ✅ Good - composite index
CREATE INDEX idx_users_email_status ON users(email, status);

-- Query benefits from index
SELECT * FROM users WHERE email = 'test@ex.com' AND status = 'active';
```

### Index Maintenance
- [ ] Unused indexes removed
- [ ] Index usage monitored (pg_stat_user_indexes)
- [ ] Duplicate indexes eliminated
- [ ] Index bloat checked regularly

**Check Index Usage (PostgreSQL):**
```sql
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY schemaname, tablename;
```

---

## 🔍 Query Optimization

### N+1 Query Problem
- [ ] Eager loading used (SELECT with JOINs)
- [ ] ORM queries reviewed (EXPLAIN)
- [ ] Batch loading for related records

**Example (SQLAlchemy):**
```python
# ❌ Bad - N+1 query
users = db.query(User).all()
for user in users:
    print(user.posts)  # Separate query per user

# ✅ Good - eager loading
users = db.query(User).options(joinedload(User.posts)).all()
```

**Example (Laravel):**
```php
// ❌ Bad - N+1
$users = User::all();
foreach ($users as $user) {
    echo $user->posts;  // Separate query
}

// ✅ Good - eager loading
$users = User::with('posts')->get();
```

### Query Analysis
- [ ] EXPLAIN ANALYZE run on slow queries
- [ ] Sequential scans eliminated where possible
- [ ] Query execution plan reviewed
- [ ] Query cache utilized

**PostgreSQL EXPLAIN:**
```sql
EXPLAIN ANALYZE
SELECT u.name, COUNT(p.id) 
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.status = 'active'
GROUP BY u.id;
```

---

## 🗂️ Schema Design

### Table Design
- [ ] Normalization appropriate (3NF for transactional)
- [ ] Denormalization only when justified
- [ ] VARCHAR size reasonable (not VARCHAR(255) everywhere)
- [ ] ENUM/CHECK constraints for fixed values
- [ ] JSON columns only when truly dynamic

**Example:**
```sql
-- ✅ Good - appropriate data types
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'draft')),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Relationships
- [ ] Foreign keys with ON DELETE/UPDATE rules
- [ ] Many-to-many with junction tables
- [ ] Self-referencing FKs for hierarchies
- [ ] Cascading deletes considered carefully

---

## 💾 Caching Strategy

### Query Caching
- [ ] Redis for frequently accessed data
- [ ] Cache keys with versioning
- [ ] Cache invalidation strategy defined
- [ ] TTL configured per data type

**Example (FastAPI + Redis):**
```python
import redis
from functools import wraps

redis_client = redis.Redis()

def cache_result(ttl=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(ttl=600)  # 10 minutes
async def get_products():
    return db.query(Product).all()
```

### Database Query Cache
- [ ] MySQL query cache configured (if using MySQL < 8.0)
- [ ] PostgreSQL shared_buffers optimized
- [ ] Result set caching at application level

---

## 🔗 Connection Pooling

### Pool Configuration
- [ ] Connection pool size appropriate
- [ ] Max overflow configured
- [ ] Idle connection timeout set
- [ ] Connection validation (pool_pre_ping)

**Example (SQLAlchemy):**
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,           # Base connections
    max_overflow=40,        # Additional under load
    pool_pre_ping=True,     # Verify connection health
    pool_recycle=3600,      # Recycle after 1 hour
    echo=False
)
```

**Example (Laravel):**
```php
// config/database.php
'connections' => [
    'mysql' => [
        'pool' => [
            'min_connections' => 5,
            'max_connections' => 20,
        ],
    ],
],
```

---

## 📈 Pagination & Limits

### Query Limits
- [ ] Default LIMIT on all list queries
- [ ] Maximum page size enforced (100 items)
- [ ] Cursor-based pagination for large datasets
- [ ] COUNT queries optimized or estimated

**Offset Pagination (Small datasets):**
```sql
SELECT * FROM products
WHERE status = 'active'
ORDER BY id
LIMIT 20 OFFSET 40;  -- Page 3
```

**Cursor Pagination (Large datasets):**
```sql
SELECT * FROM products
WHERE id > :last_id
ORDER BY id
LIMIT 20;
```

---

## 🗜️ Data Types & Storage

### Optimal Data Types
- [ ] INT instead of BIGINT when appropriate
- [ ] DECIMAL for money (not FLOAT)
- [ ] TIMESTAMP with timezone
- [ ] TEXT instead of unlimited VARCHAR
- [ ] BOOLEAN instead of TINYINT

**Size Comparison:**
```sql
-- Storage optimization
SMALLINT    -- 2 bytes  (–32,768 to 32,767)
INTEGER     -- 4 bytes  (–2B to 2B)
BIGINT      -- 8 bytes  (huge range)

-- ✅ Use smallest appropriate type
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    status SMALLINT DEFAULT 0,  -- Limited values
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🔄 Transaction Management

### Transaction Best Practices
- [ ] Keep transactions short
- [ ] Avoid long-running queries in transactions
- [ ] Use appropriate isolation level
- [ ] Rollback on errors

**Example (FastAPI):**
```python
from sqlalchemy.orm import Session

def create_order(db: Session, order_data: dict):
    try:
        # Start transaction
        order = Order(**order_data)
        db.add(order)
        
        # Update inventory
        product = db.query(Product).filter_by(id=order.product_id).first()
        product.stock -= order.quantity
        
        db.commit()
        return order
    except Exception as e:
        db.rollback()
        raise
```

---

## 🧹 Maintenance Tasks

### Regular Maintenance
- [ ] VACUUM (PostgreSQL) scheduled weekly
- [ ] ANALYZE run after bulk updates
- [ ] Table statistics updated
- [ ] Old data archived or partitioned
- [ ] Slow query log reviewed

**PostgreSQL Maintenance:**
```sql
-- Vacuum and analyze
VACUUM ANALYZE users;

-- Check table bloat
SELECT
  schemaname, tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## 📊 Monitoring & Metrics

### Key Metrics to Monitor
- [ ] Query execution time (p50, p95, p99)
- [ ] Slow query log analyzed
- [ ] Connection pool usage
- [ ] Cache hit ratio
- [ ] Lock contention
- [ ] Replication lag (if applicable)

**Slow Query Log (PostgreSQL):**
```sql
-- Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = 100;  -- Log > 100ms
SELECT pg_reload_conf();

-- Find slowest queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

---

## 🎯 Performance Targets

| Metric | Target | Alert |
|--------|--------|-------|
| Query time (p95) | < 100ms | > 500ms |
| Query time (p99) | < 500ms | > 1s |
| Connection pool usage | < 80% | > 90% |
| Cache hit ratio | > 90% | < 70% |
| Replication lag | < 1s | > 5s |
| Table scans | Minimal | Frequent |

---

## 🚀 Quick Wins

1. **Add indexes on foreign keys** - Instant JOIN speed improvement
2. **Enable query caching** - Reduce DB load by 30-50%
3. **Increase connection pool** - Eliminate wait times
4. **Use eager loading** - Eliminate N+1 queries
5. **Add WHERE clause to COUNT(*)** - Avoid full table scans

---

## 🔧 Database-Specific Tips

### PostgreSQL
- [ ] Use JSONB (not JSON) for better indexing
- [ ] Create partial indexes for filtered queries
- [ ] Use EXPLAIN (ANALYZE, BUFFERS) for detailed analysis
- [ ] Enable pg_stat_statements extension

### MySQL
- [ ] InnoDB for transactional tables
- [ ] Proper character set (utf8mb4)
- [ ] Query cache disabled in MySQL 8.0+ (use Redis)
- [ ] Partition large tables by date/range

---

**Last Updated:** 2025-01-11  
**Review Frequency:** Weekly for slow queries, Monthly for indexes
