# Data Modeling - Best Practices Guide

## Entity Relationship Diagram (ERD) Design

### Normalization Forms

**1NF (First Normal Form):**
- Atomic values (no repeating groups)
- Each column contains single value
- Unique row identifier (primary key)

**2NF (Second Normal Form):**
- Must be in 1NF
- No partial dependencies (all non-key attributes depend on entire primary key)

**3NF (Third Normal Form):**
- Must be in 2NF
- No transitive dependencies (non-key attributes don't depend on other non-key attributes)

**Example:**
```sql
-- ❌ Not Normalized (1NF violation)
CREATE TABLE orders (
    order_id INT,
    items TEXT  -- "item1,item2,item3" (repeating group)
);

-- ✅ Normalized (3NF)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    total_amount DECIMAL,
    created_at TIMESTAMP
);

CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(id),
    quantity INT,
    unit_price DECIMAL
);
```

---

## Denormalization Strategies

**When to Denormalize:**
- Read-heavy workloads (10:1 read:write ratio)
- Query performance critical
- Joining multiple tables too expensive

**Common Patterns:**
```sql
-- Denormalized: Store computed total
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    total_amount DECIMAL,  -- Denormalized (sum of order_items)
    item_count INT         -- Denormalized (count of order_items)
);

-- Maintain with triggers or application logic
```

---

## Index Design

**B-Tree Indexes (Default):**
- Use for: Equality, range queries, sorting
- Column cardinality: High (many unique values)

**Hash Indexes:**
- Use for: Exact matches only
- No range queries

**Composite Indexes:**
```sql
-- Query: WHERE user_id = X AND created_at > Y ORDER BY created_at
CREATE INDEX idx_user_created ON orders(user_id, created_at);

-- Column order matters: Most selective first
```

**Covering Indexes:**
```sql
-- Include all columns needed by query (avoid table lookup)
CREATE INDEX idx_user_status_covering ON orders(user_id, status)
INCLUDE (total_amount, created_at);
```

---

## Partitioning Strategies

**Horizontal Partitioning (Sharding):**
```sql
-- By range (time-based)
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

-- By hash (user_id)
CREATE TABLE orders_shard_0 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
```

**Vertical Partitioning:**
```sql
-- Hot columns (frequently accessed)
CREATE TABLE users_hot (
    user_id INT PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(100)
);

-- Cold columns (rarely accessed)
CREATE TABLE users_cold (
    user_id INT PRIMARY KEY REFERENCES users_hot(user_id),
    bio TEXT,
    preferences JSONB
);
```

---

## Data Types Best Practices

**PostgreSQL:**
```sql
-- ✅ Good choices
uuid            -- For distributed IDs
timestamp       -- With time zone
jsonb           -- JSON with indexing (not json)
text            -- No length limit (not varchar without length)
bigserial       -- Auto-increment 64-bit

-- ❌ Avoid
varchar without length  -- Use text instead
float/real              -- Use numeric for money
timestamp without tz    -- Always use 'with time zone'
```

**MySQL:**
```sql
-- ✅ Good choices
BIGINT UNSIGNED AUTO_INCREMENT
VARCHAR(255)         -- Explicit length
DECIMAL(10,2)        -- For currency
DATETIME(6)          -- Microsecond precision
JSON                 -- MySQL 5.7+

-- ❌ Avoid
FLOAT/DOUBLE for money
TEXT for short strings (<255 chars)
ENUM (use lookup tables instead)
```

---

## Referential Integrity

**Foreign Key Constraints:**
```sql
-- ON DELETE / ON UPDATE options
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id)
        ON DELETE CASCADE      -- Delete items when order deleted
        ON UPDATE CASCADE,     -- Update if order ID changes
    product_id INT REFERENCES products(id)
        ON DELETE RESTRICT     -- Prevent delete if referenced
);
```

**Soft Deletes:**
```sql
-- Instead of DELETE, mark as deleted
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP NULL;
CREATE INDEX idx_users_not_deleted ON users(id) WHERE deleted_at IS NULL;

-- Queries always filter
SELECT * FROM users WHERE deleted_at IS NULL;
```

---

## JSON/JSONB for Flexible Schemas

**When to Use:**
- Schema evolves frequently
- Attributes vary per entity
- Storing metadata/settings

**PostgreSQL JSONB:**
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    attributes JSONB  -- Flexible schema
);

-- Index JSONB fields
CREATE INDEX idx_products_brand ON products
    USING GIN ((attributes->'brand'));

-- Query JSONB
SELECT * FROM products
WHERE attributes->>'brand' = 'Apple'
  AND (attributes->>'price')::numeric < 1000;
```

---

## Audit Trails & Versioning

**Audit Table Pattern:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(100),
    updated_by INT,
    updated_at TIMESTAMP
);

CREATE TABLE users_audit (
    audit_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    old_values JSONB,
    new_values JSONB,
    changed_by INT,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Trigger to populate audit table
CREATE TRIGGER users_audit_trigger
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_changes();
```

**Temporal Tables (SQL Server, PostgreSQL):**
```sql
-- PostgreSQL temporal tables (example)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL,
    valid_from TIMESTAMP DEFAULT NOW(),
    valid_to TIMESTAMP DEFAULT 'infinity'
);

-- Query historical data
SELECT * FROM products
WHERE valid_from <= '2024-01-01'
  AND valid_to > '2024-01-01';
```

---

## Database Per Service (Microservices)

**Pattern:**
- Each microservice owns its database
- No direct database access between services
- Communication via APIs/events

**Benefits:**
- Independent scaling
- Technology diversity
- Isolation (failure containment)

**Challenges:**
- Distributed transactions (use Saga pattern)
- Data duplication
- Cross-service queries expensive

---

## Connection Pooling

**Why:**
- Opening connections expensive
- Limit max concurrent connections

**Configuration (PgBouncer example):**
```ini
[databases]
mydb = host=localhost port=5432 dbname=production

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
reserve_pool_size = 5
```

**Application-Level (Node.js pg):**
```javascript
const { Pool } = require('pg');

const pool = new Pool({
    host: 'localhost',
    port: 5432,
    database: 'mydb',
    user: 'user',
    password: 'pass',
    max: 20,           // Max connections
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
});
```

---

## Query Optimization

**EXPLAIN ANALYZE:**
```sql
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name;

-- Look for:
-- - Seq Scan (bad for large tables, add index)
-- - High cost numbers
-- - Many rows filtered
```

**Common Optimizations:**
```sql
-- ❌ Bad: Function on indexed column
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- ✅ Good: Sargable query
SELECT * FROM orders WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';

-- ❌ Bad: SELECT *
SELECT * FROM orders WHERE user_id = 123;

-- ✅ Good: Select only needed columns
SELECT order_id, total_amount, created_at FROM orders WHERE user_id = 123;

-- ❌ Bad: N+1 queries
for order in orders:
    user = get_user(order.user_id)  -- DB query per order

-- ✅ Good: Eager loading
orders = get_orders_with_users()  -- Single JOIN query
```

---

## Migration Strategies

**Zero-Downtime Schema Changes:**
```
1. Additive changes first (add column, nullable)
2. Deploy application code (uses new column optionally)
3. Backfill data (batch UPDATE)
4. Deploy code (requires new column)
5. Remove old column (later, after validation)
```

**Backward-Compatible Migrations:**
```sql
-- Step 1: Add new column (nullable)
ALTER TABLE users ADD COLUMN email_verified BOOLEAN NULL;

-- Step 2: Backfill (in batches)
UPDATE users SET email_verified = TRUE WHERE email IS NOT NULL;

-- Step 3: Add NOT NULL constraint (after backfill complete)
ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;
```

---

## Best Practices Summary

1. **Normalize first, denormalize for performance** (measure before optimizing)
2. **Index wisely** (every index costs writes, helps reads)
3. **Use foreign keys** (enforce integrity at DB level)
4. **Plan for scale** (partitioning, sharding strategies)
5. **Monitor query performance** (slow query logs, EXPLAIN)
6. **Use connection pooling** (don't exhaust connections)
7. **Version schema changes** (migration scripts in version control)
8. **Test migrations** (on staging with production-like data)
9. **Document decisions** (why this data type, why this index)
10. **Backup & test restores** (regular drills)
