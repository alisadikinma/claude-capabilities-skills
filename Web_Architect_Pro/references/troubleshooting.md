# Troubleshooting Guide

**Last Updated:** 2025-01-11  
**Category:** Reference Guide

---

## 🐛 Common Frontend Issues

### 1. Build Errors

**Issue: "Module not found"**
```bash
Error: Module not found: Can't resolve '@/components/Button'
```

**Solutions:**
```typescript
// Check tsconfig.json paths
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}

// Clear cache
rm -rf node_modules .next
npm install
```

**Issue: "Out of Memory"**
```bash
# Increase Node memory
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

### 2. Hydration Errors

**Issue: Content mismatch**
```typescript
// ❌ Problem
<div>{new Date().toString()}</div>

// ✅ Solution
const [date, setDate] = useState('');
useEffect(() => {
  setDate(new Date().toString());
}, []);
```

### 3. Performance Issues

**Debug re-renders:**
```typescript
function useWhyDidYouUpdate(name, props) {
  const previousProps = useRef();
  
  useEffect(() => {
    if (previousProps.current) {
      const changedProps = {};
      Object.keys(props).forEach(key => {
        if (previousProps.current[key] !== props[key]) {
          changedProps[key] = {
            from: previousProps.current[key],
            to: props[key]
          };
        }
      });
      
      if (Object.keys(changedProps).length) {
        console.log('[why-did-you-update]', name, changedProps);
      }
    }
    
    previousProps.current = props;
  });
}
```

---

## 💾 Common Backend Issues

### 1. Database Connection

**Issue: Connection pool exhausted**
```python
# ✅ Solution: Use context manager
def get_users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        return result.fetchall()

# Configure pool
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True
)
```

### 2. N+1 Query Problem

**Detection:**
```python
# Enable logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# ❌ Problem
users = db.query(User).all()
for user in users:
    posts = user.posts  # N queries!
```

**Solutions:**
```python
# ✅ Eager loading
from sqlalchemy.orm import joinedload

users = db.query(User).options(
    joinedload(User.posts)
).all()
```

### 3. Slow Queries

**Diagnosis:**
```sql
-- PostgreSQL
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';
```

**Solutions:**
```sql
-- Add indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Select specific columns
SELECT id, name, email FROM users;

-- Add pagination
SELECT * FROM posts LIMIT 20 OFFSET 0;
```

### 4. CORS Issues

**FastAPI:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🚀 Deployment Issues

### 1. Docker Build Failures

```dockerfile
# .dockerignore
node_modules
.next
.git
.env.local

# Multi-stage build
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS runner
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
CMD ["npm", "start"]
```

### 2. Environment Variables

```typescript
// Validate on startup
const requiredEnvVars = ['DATABASE_URL', 'JWT_SECRET'];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing: ${envVar}`);
  }
}
```

---

## 🔍 Debugging Tips

### 1. Structured Logging

```python
import json
from datetime import datetime

logger.info(json.dumps({
    'event': 'user_login',
    'user_id': user.id,
    'timestamp': datetime.utcnow().isoformat()
}))
```

### 2. Performance Profiling

**React Profiler:**
```typescript
import { Profiler } from 'react';

function onRender(id, phase, actualDuration) {
  console.log(`${id} took ${actualDuration}ms`);
}

<Profiler id="App" onRender={onRender}>
  <App />
</Profiler>
```

---

**Last Updated:** 2025-01-11  
**Maintained by:** Ali Sadikin MA
