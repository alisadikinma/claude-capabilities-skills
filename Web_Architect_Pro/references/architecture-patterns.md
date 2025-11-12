# Architecture Patterns for Web Applications

Detailed architectural patterns dengan implementation guidance untuk berbagai skala aplikasi.

---

## 1. Layered Architecture (3-Tier)

### Overview

Most common pattern - separates application into three distinct layers.

```
┌─────────────────────────────────┐
│      Presentation Layer         │
│  (UI Components, Pages, Views)  │
│    Next.js, React, Vue          │
└─────────────────────────────────┘
          ↕ HTTP/API Calls
┌─────────────────────────────────┐
│      Application Layer          │
│   (Controllers, Services,       │
│    Business Logic, Use Cases)   │
└─────────────────────────────────┘
          ↕ Database Calls
┌─────────────────────────────────┐
│       Data Access Layer         │
│  (Repositories, ORM, Models)    │
│    Database, External APIs      │
└─────────────────────────────────┘
```

### When to Use

- ✅ 80% of web applications
- ✅ Clear separation of concerns needed
- ✅ Team size: 1-20 developers
- ✅ Traditional CRUD applications
- ✅ Moderate complexity

### Implementation

**Frontend Structure (Next.js):**
```
app/
├── (auth)/
│   ├── login/
│   └── register/
├── (dashboard)/
│   ├── layout.tsx
│   └── page.tsx
├── api/          # API routes
└── components/   # Shared components

lib/
├── api-client.ts    # API layer
├── stores/          # State management
└── utils/
```

**Backend Structure (FastAPI):**
```
app/
├── api/
│   └── v1/
│       ├── endpoints/   # Controllers
│       │   ├── users.py
│       │   └── posts.py
│       └── deps.py      # Dependencies
├── core/
│   ├── config.py        # Configuration
│   └── security.py      # Auth logic
├── models/              # Database models
├── schemas/             # Pydantic schemas
├── crud/                # Database operations
└── services/            # Business logic
```

### Pros & Cons

**Pros:**
- ✅ Easy to understand and maintain
- ✅ Clear separation of concerns
- ✅ Testable - each layer independent
- ✅ Scalable to medium size teams

**Cons:**
- ⚠️ Can become rigid over time
- ⚠️ Network calls between layers add latency
- ⚠️ May be over-engineered for simple apps

---

## 2. Feature-Based Architecture (Vertical Slices)

### Overview

Organize code by features rather than technical layers.

```
src/
├── features/
│   ├── authentication/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── api/
│   │   │   └── authApi.ts
│   │   ├── types/
│   │   │   └── user.types.ts
│   │   └── index.ts
│   ├── products/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── types/
│   └── orders/
│       ├── components/
│       ├── hooks/
│       ├── api/
│       └── types/
├── shared/
│   ├── components/
│   │   └── Button/
│   ├── hooks/
│   └── utils/
└── config/
```

### When to Use

- ✅ Large applications (50k+ LOC)
- ✅ Multiple teams working in parallel
- ✅ Complex business domains
- ✅ Frequent feature additions
- ✅ Clear feature boundaries

### Implementation Example

**Feature Module (products):**
```typescript
// features/products/api/productsApi.ts
export const productsApi = {
  getAll: () => fetch('/api/products'),
  getById: (id: string) => fetch(`/api/products/${id}`),
  create: (data: CreateProductDto) => fetch('/api/products', { method: 'POST', body: JSON.stringify(data) })
};

// features/products/hooks/useProducts.ts
export function useProducts() {
  const [products, setProducts] = useState([]);
  // ... logic specific to products feature
  return { products, loading, error, refetch };
}

// features/products/components/ProductList.tsx
export function ProductList() {
  const { products } = useProducts();
  return <div>{products.map(p => <ProductCard key={p.id} {...p} />)}</div>;
}

// features/products/index.ts
export { ProductList, ProductCard } from './components';
export { useProducts } from './hooks';
export * from './types';
```

### Pros & Cons

**Pros:**
- ✅ Scales to large codebases
- ✅ Teams can work independently
- ✅ Easy to add/remove features
- ✅ Clear ownership per feature
- ✅ Less cross-cutting concerns

**Cons:**
- ⚠️ More initial setup needed
- ⚠️ Shared code must be carefully managed
- ⚠️ Can duplicate code if not careful

---

## 3. API-First Architecture (Backend for Frontend)

### Overview

Backend API serves multiple frontends (web, mobile, desktop).

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Next.js    │────▶│              │     │              │
│   (Web)      │     │   FastAPI    │────▶│ PostgreSQL   │
└──────────────┘     │  REST API    │     │  (Database)  │
                     │              │     └──────────────┘
┌──────────────┐     │              │
│   Flutter    │────▶│              │
│   (Mobile)   │     └──────────────┘
└──────────────┘
                     
┌──────────────┐     
│   Electron   │────▶ Same API
│   (Desktop)  │
└──────────────┘
```

### When to Use

- ✅ Multi-platform applications (web + mobile)
- ✅ Need API for third-party integrations
- ✅ Separate frontend and backend teams
- ✅ API will be public or semi-public

### Implementation

**API Layer (FastAPI):**
```python
# Versioned API structure
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   └── orders.py
│   │   └── router.py
│   └── v2/  # Future version
├── models/
├── schemas/
│   ├── v1/
│   │   └── user.py  # V1 schema
│   └── v2/
└── services/
```

**OpenAPI Spec:**
```yaml
openapi: 3.0.0
info:
  title: Product API
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

### Pros & Cons

**Pros:**
- ✅ Single source of truth (API)
- ✅ Consistent data across platforms
- ✅ Frontend flexibility (swap frameworks)
- ✅ Better separation of concerns
- ✅ API can be monetized

**Cons:**
- ⚠️ More network round trips
- ⚠️ Need API versioning strategy
- ⚠️ Two deployments to manage
- ⚠️ CORS configuration needed

---

## 4. Microservices Architecture

### Overview

Application split into small, independent services.

```
┌────────────────┐
│   API Gateway  │
│   (Kong/NGINX) │
└────────────────┘
       ↕
  ┌────┴────┬────────┬────────┐
  ↓         ↓        ↓        ↓
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Auth  │ │User  │ │Order │ │Pay   │
│Service│ │Service│ │Service│ │Service│
└──────┘ └──────┘ └──────┘ └──────┘
  ↓         ↓        ↓        ↓
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Auth  │ │User  │ │Order │ │Pay   │
│  DB  │ │  DB  │ │  DB  │ │  DB  │
└──────┘ └──────┘ └──────┘ └──────┘
```

### When to Use

- ✅ Team size > 20 developers
- ✅ Multiple independent business domains
- ✅ Different scaling needs per service
- ✅ Polyglot persistence needed
- ✅ Organizational boundaries

### Implementation

**Service Structure (NestJS):**
```
auth-service/
├── src/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   └── strategies/
│   ├── users/
│   └── main.ts
├── Dockerfile
└── package.json

user-service/
├── src/
│   ├── users/
│   │   ├── users.controller.ts
│   │   └── users.service.ts
│   └── main.ts
├── Dockerfile
└── package.json

order-service/
├── src/
│   ├── orders/
│   └── main.ts
├── Dockerfile
└── package.json
```

**API Gateway (Kong):**
```yaml
services:
  - name: auth-service
    url: http://auth-service:3001
    routes:
      - name: auth-route
        paths:
          - /api/auth

  - name: user-service
    url: http://user-service:3002
    routes:
      - name: user-route
        paths:
          - /api/users
```

### Pros & Cons

**Pros:**
- ✅ Independent deployment per service
- ✅ Technology flexibility
- ✅ Scales horizontally easily
- ✅ Team autonomy
- ✅ Fault isolation

**Cons:**
- ⚠️ High operational complexity
- ⚠️ Distributed system challenges
- ⚠️ Network latency between services
- ⚠️ Difficult testing
- ⚠️ Data consistency challenges

---

## 5. Serverless Architecture

### Overview

Application runs on Function-as-a-Service platforms.

```
┌────────────────┐
│   Next.js App  │
│   (Vercel)     │
└────────────────┘
       ↕
┌────────────────┐
│  API Gateway   │
│  (AWS/Vercel)  │
└────────────────┘
       ↕
┌────────────────┐
│   Functions    │
│  (Serverless)  │
└────────────────┘
       ↕
┌────────────────┐
│   Database     │
│  (Supabase)    │
└────────────────┘
```

### When to Use

- ✅ Variable/unpredictable traffic
- ✅ Event-driven applications
- ✅ Cost optimization priority
- ✅ Rapid prototyping
- ✅ Startup/MVP stage

### Implementation

**Vercel Serverless Functions:**
```typescript
// api/users.ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(
  req: VercelRequest,
  res: VercelResponse
) {
  if (req.method === 'GET') {
    const users = await db.users.findMany();
    return res.status(200).json(users);
  }
  
  res.status(405).json({ error: 'Method not allowed' });
}
```

**AWS Lambda (Node.js):**
```javascript
exports.handler = async (event) => {
  const { httpMethod, body } = event;
  
  if (httpMethod === 'POST') {
    const user = JSON.parse(body);
    await saveUser(user);
    return {
      statusCode: 201,
      body: JSON.stringify(user)
    };
  }
};
```

### Pros & Cons

**Pros:**
- ✅ Pay per execution (cost efficient)
- ✅ Auto-scaling built-in
- ✅ No server management
- ✅ Fast deployment

**Cons:**
- ⚠️ Cold starts (latency)
- ⚠️ Vendor lock-in
- ⚠️ Limited execution time
- ⚠️ Debugging challenges
- ⚠️ Complex local development

---

## Architecture Selection Matrix

| Pattern | Team Size | Complexity | Scale | Cost | Maintenance |
|---------|-----------|------------|-------|------|-------------|
| **Layered** | 1-20 | Low-Medium | Medium | Low | Low |
| **Feature-Based** | 10-50 | Medium-High | High | Medium | Medium |
| **API-First** | 5-30 | Medium | High | Medium | Medium |
| **Microservices** | 20+ | Very High | Very High | High | High |
| **Serverless** | 1-10 | Low | Variable | Very Low | Very Low |

---

**Last Updated:** 2025-01-11
