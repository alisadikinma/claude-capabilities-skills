# Caching Strategy Decision Tree

## Primary Decision Flow

```
START: What caching strategy should I use?
  │
  ├─ What are you caching?
  │   ├─ Database queries ───────────────────────> Redis / Application cache
  │   ├─ Static assets (CSS, JS, images) ───────> CDN
  │   ├─ API responses ─────────────────────────> Redis / HTTP cache
  │   ├─ User sessions ─────────────────────────> Redis / Memcached
  │   ├─ Computed results ──────────────────────> Application cache / Redis
  │   └─ Full pages ────────────────────────────> Varnish / Nginx / CDN
  │
  ├─ Update frequency?
  │   ├─ Static (rarely changes) ───────────────> CDN + Long TTL
  │   ├─ Dynamic (frequent updates) ────────────> Redis + Short TTL
  │   ├─ Real-time (constant changes) ──────────> No cache / Cache-aside
  │   └─ Scheduled updates ─────────────────────> Cache warming
  │
  ├─ Data consistency requirements?
  │   ├─ Strong consistency ────────────────────> Cache-aside + Low TTL
  │   ├─ Eventual consistency ──────────────────> Write-through / Write-behind
  │   └─ Stale data acceptable ─────────────────> Long TTL
  │
  └─ Scale?
      ├─ Single server ─────────────────────────> Application cache (in-memory)
      ├─ Multi-server ──────────────────────────> Redis / Memcached (distributed)
      └─ Global users ──────────────────────────> CDN + Redis
```

## Cache Types Comparison

| Type | Speed | Persistence | Distributed | Complexity | Use Case |
|------|-------|-------------|-------------|------------|----------|
| **Application Cache** | ⭐⭐⭐⭐⭐ | ❌ | ❌ | Low | Single-server apps |
| **Redis** | ⭐⭐⭐⭐⭐ | ✅ | ✅ | Medium | Distributed apps |
| **Memcached** | ⭐⭐⭐⭐⭐ | ❌ | ✅ | Low | Simple key-value |
| **CDN** | ⭐⭐⭐⭐⭐ | ✅ | ✅ | Low | Static assets |
| **HTTP Cache** | ⭐⭐⭐⭐ | ❌ | ❌ | Low | Browser/proxy cache |
| **Database Query Cache** | ⭐⭐⭐ | ✅ | ❌ | Low | DB-level optimization |

## 1. Application-Level Caching

### In-Memory Cache

**When to Use:**
- ✅ Single-server applications
- ✅ Small datasets (< 1GB)
- ✅ No shared state needed
- ✅ Ultra-fast access required (< 1ms)

**When NOT to Use:**
- ❌ Multi-server deployment
- ❌ Need persistence
- ❌ Large datasets
- ❌ Need cache sharing across instances

**Implementation Examples:**

**PHP (Laravel):**
```php
// Array cache (not persistent)
Cache::store('array')->put('key', 'value', 60);

// File cache (persistent, single-server)
Cache::put('user_' . $userId, $userData, 3600);

// Remember pattern
$users = Cache::remember('active_users', 600, function() {
    return User::where('active', true)->get();
});
```

**Python (Flask/Django):**
```python
# Simple dictionary cache
cache = {}

def get_user(user_id):
    if user_id in cache:
        return cache[user_id]
    
    user = db.query(User).get(user_id)
    cache[user_id] = user
    return user

# Or use functools.lru_cache
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_computation(n):
    return sum(range(n))
```

**Node.js:**
```javascript
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 });

// Set cache
cache.set('key', { some: 'data' });

// Get cache
const value = cache.get('key');

// With TTL
cache.set('temp_key', 'data', 60); // 60 seconds
```

---

## 2. Redis Caching

### When to Use Redis

**Perfect For:**
- ✅ Distributed applications (multi-server)
- ✅ Session storage
- ✅ Leaderboards / rankings
- ✅ Rate limiting
- ✅ Pub/sub messaging
- ✅ Queue systems

**Advanced Data Structures:**
- Strings, Lists, Sets, Sorted Sets
- Hashes, Bitmaps, HyperLogLogs
- Streams, Geospatial indexes

### Redis Caching Patterns

**1. Cache-Aside (Lazy Loading)**
```python
def get_user(user_id):
    # Try cache first
    cached = redis.get(f'user:{user_id}')
    if cached:
        return json.loads(cached)
    
    # Cache miss, fetch from DB
    user = db.query(User).get(user_id)
    
    # Store in cache
    redis.setex(
        f'user:{user_id}',
        3600,  # TTL: 1 hour
        json.dumps(user)
    )
    
    return user
```

**Pros:** Simple, only cache what's needed
**Cons:** Cache miss penalty, stale data possible

**2. Write-Through**
```python
def update_user(user_id, data):
    # Update database
    db.query(User).filter_by(id=user_id).update(data)
    db.commit()
    
    # Immediately update cache
    user = db.query(User).get(user_id)
    redis.setex(f'user:{user_id}', 3600, json.dumps(user))
    
    return user
```

**Pros:** Cache always up-to-date
**Cons:** Higher write latency, cache write might fail

**3. Write-Behind (Write-Back)**
```python
def update_user(user_id, data):
    # Update cache immediately
    redis.setex(f'user:{user_id}', 3600, json.dumps(data))
    
    # Queue database update (async)
    queue.enqueue('update_user_db', user_id, data)
    
    return data
```

**Pros:** Fast writes, reduced DB load
**Cons:** Risk of data loss, eventual consistency

**4. Refresh-Ahead**
```python
def get_user(user_id):
    cached = redis.get(f'user:{user_id}')
    ttl = redis.ttl(f'user:{user_id}')
    
    # If cache expires soon, refresh in background
    if ttl < 600:  # Less than 10 minutes left
        queue.enqueue('refresh_user_cache', user_id)
    
    if cached:
        return json.loads(cached)
    
    # Fallback to DB
    return fetch_from_db(user_id)
```

**Pros:** Prevents cache misses for hot data
**Cons:** Additional complexity, might cache unnecessary data

### Redis Use Cases

**Session Store:**
```python
# Store session
redis.setex(f'session:{session_id}', 1800, json.dumps(session_data))

# Get session
session = json.loads(redis.get(f'session:{session_id}'))
```

**Rate Limiting:**
```python
def is_rate_limited(user_id, limit=100, window=3600):
    key = f'rate_limit:{user_id}'
    current = redis.incr(key)
    
    if current == 1:
        redis.expire(key, window)
    
    return current > limit
```

**Leaderboard:**
```python
# Add score
redis.zadd('leaderboard', {user_id: score})

# Get top 10
top_users = redis.zrevrange('leaderboard', 0, 9, withscores=True)

# Get user rank
rank = redis.zrevrank('leaderboard', user_id)
```

---

## 3. CDN Caching

### When to Use CDN

**Perfect For:**
- ✅ Static assets (JS, CSS, images, videos)
- ✅ Global user base
- ✅ High-traffic websites
- ✅ Reduce origin server load
- ✅ Improve page load times

**Popular CDN Providers:**
- Cloudflare (free tier available)
- AWS CloudFront
- Fastly
- Bunny CDN (affordable)
- Vercel Edge Network

### CDN Caching Strategy

**Cache Headers:**
```http
# Long TTL for versioned assets (1 year)
Cache-Control: public, max-age=31536000, immutable
# For: app.abc123.js, style.def456.css

# Medium TTL for semi-static content (1 day)
Cache-Control: public, max-age=86400
# For: logo.png, homepage images

# Short TTL for dynamic content (5 minutes)
Cache-Control: public, max-age=300, s-maxage=300
# For: API responses, personalized content

# No cache for private/sensitive data
Cache-Control: private, no-cache, no-store, must-revalidate
# For: User profiles, auth tokens
```

**Cache Invalidation:**
```bash
# Option 1: Versioned URLs (recommended)
/assets/app.v1.js   → v2 released → /assets/app.v2.js
# Old URL naturally expires, no manual purge needed

# Option 2: Cache purge (requires CDN API)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer {api_token}" \
  -d '{"files":["https://example.com/style.css"]}'

# Option 3: Cache tags (Cloudflare/Fastly)
Cache-Tag: product-123, category-electronics
# Later: Purge all tags matching "product-123"
```

### CDN Cost Optimization

| Provider | Free Tier | Bandwidth Cost (per GB) | Best For |
|----------|-----------|------------------------|----------|
| **Cloudflare** | Unlimited | Free (Pro: $20/month) | Most use cases |
| **AWS CloudFront** | 1TB/month (12 months) | $0.085-0.25 | AWS ecosystem |
| **Bunny CDN** | None | $0.01-0.03 | Budget-conscious |
| **Fastly** | $50 credit | $0.12 | Enterprise, edge compute |
| **Vercel** | 100GB | Included in plans | Next.js apps |

---

## 4. HTTP Caching

### Browser Cache

**Cache-Control Directives:**
```http
# Public cache (CDN, proxy, browser)
Cache-Control: public, max-age=3600

# Private cache (browser only)
Cache-Control: private, max-age=3600

# No cache (always revalidate)
Cache-Control: no-cache

# No store (don't cache at all)
Cache-Control: no-store

# Immutable (never revalidate)
Cache-Control: public, max-age=31536000, immutable

# Stale-while-revalidate (serve stale, update async)
Cache-Control: max-age=3600, stale-while-revalidate=86400
```

### Conditional Requests (ETag)

```http
# Server sends ETag
HTTP/1.1 200 OK
ETag: "abc123"
Cache-Control: max-age=3600
Content-Type: application/json

{"data": "..."}

# Client revalidates with If-None-Match
GET /api/data
If-None-Match: "abc123"

# If not modified:
HTTP/1.1 304 Not Modified
ETag: "abc123"
# (No body, browser uses cached version)

# If modified:
HTTP/1.1 200 OK
ETag: "xyz789"
{"data": "new data"}
```

---

## 5. Database Query Caching

### MySQL Query Cache (Deprecated in MySQL 8.0)

**Modern Alternatives:**
1. **Application-level caching** (Redis)
2. **Result set caching** (custom implementation)
3. **Materialized views** (precomputed queries)

### PostgreSQL Approach

**Materialized Views:**
```sql
-- Create materialized view
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
    user_id,
    COUNT(*) as post_count,
    MAX(created_at) as last_post
FROM posts
GROUP BY user_id;

-- Refresh periodically (via cron)
REFRESH MATERIALIZED VIEW user_stats;

-- Query the cached result
SELECT * FROM user_stats WHERE user_id = 123;
```

---

## Caching Strategies Comparison

| Strategy | Consistency | Complexity | Performance | Use Case |
|----------|-------------|------------|-------------|----------|
| **Cache-Aside** | Eventual | Low | Good | General purpose |
| **Write-Through** | Strong | Medium | Medium | Critical data |
| **Write-Behind** | Eventual | High | Excellent | High write load |
| **Refresh-Ahead** | Eventual | High | Excellent | Predictable hot data |
| **Read-Through** | Eventual | Medium | Good | Simplified reads |

## Cache Invalidation Strategies

**1. TTL-Based (Time-based)**
```python
# Simple: Cache expires after X seconds
redis.setex('key', 3600, 'value')  # Expires in 1 hour
```
**Pros:** Simple, automatic cleanup  
**Cons:** Stale data possible, cache miss at expiry

**2. Event-Based (Write invalidation)**
```python
def update_user(user_id, data):
    db.update(user_id, data)
    redis.delete(f'user:{user_id}')  # Invalidate cache
```
**Pros:** Always fresh data  
**Cons:** More complex, need to track all cache keys

**3. Tag-Based**
```python
# Set cache with tags
cache.set('product_123', data, tags=['products', 'category_electronics'])

# Invalidate by tag
cache.invalidate_tag('products')  # Clears all products
```
**Pros:** Flexible, group invalidation  
**Cons:** More complex implementation

**4. Version-Based**
```python
def get_user(user_id):
    version = redis.get(f'user_version:{user_id}') or 0
    key = f'user:{user_id}:v{version}'
    
    cached = redis.get(key)
    if cached:
        return cached
    
    # Fetch and cache
    data = fetch_from_db(user_id)
    redis.setex(key, 3600, data)
    return data

def update_user(user_id, data):
    db.update(user_id, data)
    redis.incr(f'user_version:{user_id}')  # Bump version
```
**Pros:** No need to delete old cache  
**Cons:** More storage usage

## Cache Warming Strategies

**1. Eager Loading (On Deploy)**
```python
# Warm cache on application startup
def warm_cache():
    popular_users = db.query(User).filter(User.followers > 10000).all()
    for user in popular_users:
        redis.setex(f'user:{user.id}', 3600, json.dumps(user))
```

**2. Scheduled Refresh**
```python
# Cron job: Refresh cache every hour
@cron.schedule('0 * * * *')  # Every hour
def refresh_top_products():
    products = db.query(Product).order_by(Product.sales.desc()).limit(100)
    for product in products:
        redis.setex(f'product:{product.id}', 7200, json.dumps(product))
```

**3. Predictive Warming**
```python
# Warm cache based on user behavior
def on_user_visit(user_id):
    # Warm their data + related data
    asyncio.create_task(warm_user_data(user_id))
```

## Cache Sizing Guidelines

| App Size | Redis Memory | Eviction Policy | Use Case |
|----------|--------------|-----------------|----------|
| **Small** | 256MB-1GB | allkeys-lru | < 10K users |
| **Medium** | 2-8GB | allkeys-lru | 10K-100K users |
| **Large** | 16-64GB | allkeys-lru | 100K-1M users |
| **Enterprise** | 128GB+ | volatile-lru + sharding | 1M+ users |

**Eviction Policies:**
- `allkeys-lru`: Evict least recently used keys
- `volatile-lru`: Evict least recently used keys with TTL
- `allkeys-lfu`: Evict least frequently used keys
- `noeviction`: Return errors when memory full

## Monitoring & Debugging

**Redis Metrics to Track:**
```bash
# Hit rate
redis-cli INFO stats | grep keyspace_hits
redis-cli INFO stats | grep keyspace_misses

# Memory usage
redis-cli INFO memory | grep used_memory_human

# Evictions
redis-cli INFO stats | grep evicted_keys
```

**Target Metrics:**
- Cache hit rate: > 80%
- Cache miss rate: < 20%
- Eviction rate: < 5% of operations

**Common Issues:**
1. **Low hit rate**: TTL too short, keys not predictable
2. **High evictions**: Redis undersized, need more memory
3. **Stale data**: TTL too long, poor invalidation

---

**Key Principle:** Start with simple cache-aside + Redis, add CDN for static assets, optimize based on metrics.

**Review Trigger Points:**
- Hit rate < 70%
- Response time degradation
- High DB load
- Eviction rate > 10%
