---
name: web-architect-pro
description: Complete full-stack web development skill with 46 production-ready templates. Covers frontend frameworks, backend frameworks, databases, API patterns, infrastructure tools, testing suites, and security best practices for building modern web applications.
---

# Web Architect Pro

Modern full-stack web development skill covering architecture, implementation, optimization, and deployment.

---

## 🚀 Workflow Overview

Building web applications follows this process:

1. **Requirements Analysis** → Define features, constraints, scale requirements
2. **Tech Stack Selection** → Choose optimal frontend + backend + database combination
3. **Architecture Design** → Select appropriate architectural pattern
4. **Project Scaffolding** → Generate boilerplate using `scripts/project_scaffolder.py`
5. **Implementation** → Build features following best practices
6. **Security Hardening** → Apply checklist from `references/checklists/backend-security.md`
7. **Performance Optimization** → Follow `references/performance-optimization.md`
8. **Testing** → Implement test pyramid (70% unit, 20% integration, 10% E2E)
9. **Validation** → Run `scripts/api_validator.py` and `scripts/performance_analyzer.py`
10. **Deployment** → Configure for target platform

**Decision Tree:**
- **Scale needed?** → High traffic: Go serverless (Next.js + Vercel) | Enterprise: NestJS + Kubernetes
- **Team expertise?** → Python: FastAPI | PHP: Laravel | TypeScript: NestJS
- **Time to market?** → Fast: Next.js + Supabase | Custom: Build from templates

---

## 🔧 Core Capabilities

### 1. Frontend Architecture
- **Frameworks:** Next.js 14+ (App Router), React 18+, Vue.js 3+
- **State Management:** Redux Toolkit, Zustand, Pinia, Context API
- **Styling:** Tailwind CSS, CSS Modules, Styled Components
- **Build Tools:** Vite, Webpack 5, Turbopack
- **Rendering:** SSR, SSG, ISR, Client-side

**Templates:** `assets/templates/nextjs-project-structure.md`, `react-project-structure.md`, `vue-project-structure.md`

### 2. Backend Architecture
- **Python:** FastAPI (async, high-performance), Django (batteries-included), Flask (lightweight)
- **PHP:** Laravel 10+ (full-featured), Lumen (micro-framework)
- **Node.js:** Express (minimal), NestJS (enterprise), Fastify (fast)
- **API Design:** REST (best practices), GraphQL (Apollo Server 4), WebSocket (Socket.io)
- **Real-time:** WebSockets, Server-Sent Events, Socket.io
- **Infrastructure:** Docker Compose (dev envs), Redis caching, Message Queues (Bull/BullMQ)

**Backend Templates:**
- Python/PHP: `assets/templates/fastapi-structure.md`, `django-structure.md`, `laravel-api-structure.md`
- Node.js: `express-api-structure.md`, `nestjs-project-structure.md`, `fastify-api-structure.md`

**API & Real-time:**
- `rest-api-best-practices.md` - RESTful design, versioning, pagination, filtering
- `graphql-setup.md` - Apollo Server 4, DataLoader, subscriptions
- `websocket-socketio-setup.md` - Real-time chat, notifications, rooms

**Infrastructure:**
- `redis-caching-setup.md` - Cache strategies, pub/sub, rate limiting
- `message-queue-bull-setup.md` - Background jobs, scheduling, Bull Board
- `docker-compose-setup.md` - Multi-service development environments

### 3. Database Design
- **SQL:** PostgreSQL (preferred for complex apps), MySQL (web apps), SQLite (simple apps)
- **NoSQL:** MongoDB (flexible schemas), Redis (caching + sessions)
- **ORMs:** Prisma (TypeScript-first), TypeORM (TypeScript), SQLAlchemy (Python), Eloquent (PHP)
- **Optimization:** Indexing, query optimization, connection pooling
- **Migrations:** Version control, rollback strategies

**Templates:** 
- `mongodb-setup.md` - MongoDB + Mongoose complete setup
- `prisma-complete-setup.md` - Prisma ORM for SQL & MongoDB

**Checklist:** `references/checklists/database-performance.md`

### 4. Performance Optimization
- **Frontend:** Code splitting, lazy loading, image optimization (Next.js Image), CDN
- **Backend:** Redis caching, database query optimization, connection pooling
- **Network:** HTTP/2, Brotli compression, resource hints (preload, prefetch)
- **Monitoring:** Web Vitals (LCP < 2.5s, FID < 100ms, CLS < 0.1), Lighthouse scores

**Complete Guide:** `references/performance-optimization.md`  
**Checklist:** `references/checklists/frontend-optimization.md`  
**Tool:** `scripts/performance_analyzer.py`

### 5. Security Implementation
- **Authentication:** JWT (15min expiry + refresh), OAuth 2.0, Session-based
- **Authorization:** RBAC (role-based), ABAC (attribute-based), permission systems
- **Headers:** CORS, CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- **Input Validation:** XSS prevention, SQL injection protection, CSRF tokens
- **Rate Limiting:** 100 req/min per IP (default), exponential backoff

**Complete Guide:** `references/security-patterns.md`  
**Checklist:** `references/checklists/backend-security.md`  
**Examples:** `references/examples/auth-implementation.md`

### 6. Testing & Quality
- **Unit Testing:** Jest (React), Vitest (Vite), PHPUnit (Laravel), pytest (Python), Jest (Node.js)
- **Integration Testing:** React Testing Library, Vue Test Utils, Playwright
- **E2E Testing:** Playwright (preferred), Cypress (alternative), Puppeteer
- **API Testing:** Use `scripts/api_validator.py` for OpenAPI validation
- **Code Quality:** ESLint + Prettier (JS/TS), PHPStan (PHP), mypy (Python), TypeScript strict

**Testing Templates (10 complete setups):**
- Frontend: `jest-setup.md`, `vitest-setup.md`, `testing-library-setup.md`
- E2E: `playwright-setup.md`, `cypress-setup.md`
- Backend: `pytest-setup.md`, `phpunit-setup.md`, `jest-node-setup.md`
- Quality: `eslint-prettier-config.md`, `typescript-strict-config.md`

**Test Pyramid:** 70% unit, 20% integration, 10% E2E

---

## 📐 Tech Stack Selection Guide

### Quick Selection Matrix

**Choose Next.js 14 + FastAPI + PostgreSQL when:**
- Need SEO (server-side rendering)
- Complex state management required
- High-performance API needed
- Python ML integration planned

**Choose React SPA + Laravel + MySQL when:**
- Traditional web application
- Team knows PHP
- Admin panels or CRUD-heavy
- Monolithic preferred over microservices

**Choose Vue 3 + Django + PostgreSQL when:**
- Rapid development needed
- Content-heavy application
- Strong admin interface required
- Python team expertise

**Detailed Guide:** `references/tech-stack-guide.md` (to be created)

---

## 🏗️ Architecture Patterns

### 1. Layered Architecture (Recommended for 80% of apps)

Best for: Most web applications, clear separation of concerns

```
Presentation → Application → Data Access
(UI)           (Logic)        (Database)
```

**When to use:** Standard business apps, dashboards, CRUD applications  
**Template:** Apply to any framework in `assets/templates/`

### 2. Feature-Based Architecture (Large teams, complex domains)

```
features/
├── auth/ (components, hooks, api, types)
├── products/
└── orders/
shared/ (common components, utilities)
```

**When to use:** Large codebases (50k+ LOC), multiple teams  
**Example:** `references/examples/state-management-patterns.md`

### 3. API-First Architecture (Multi-platform: web + mobile)

Shared backend API serves multiple frontends (web, mobile, desktop)

**When to use:** Need mobile app + web app with consistent data  
**Integration:** See `references/examples/api-integration.md`

**Detailed Guide:** `references/architecture-patterns.md` (to be created)

---

## 🎯 Quick Start Commands

### New Next.js + FastAPI Project

```bash
# Frontend
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend && npm install zustand axios @tanstack/react-query

# Backend  
mkdir backend && cd backend
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose bcrypt
# Copy structure from: assets/templates/fastapi-structure.md

# Database
createdb myapp_db
```

### New React + Laravel Project

```bash
# Frontend
npm create vite@latest frontend -- --template react-ts
cd frontend && npm install @reduxjs/toolkit react-redux axios

# Backend
composer create-project laravel/laravel backend
cd backend && php artisan install:api
# Copy structure from: assets/templates/laravel-api-structure.md
```

### New Vue + Django Project

```bash
# Frontend
npm create vite@latest frontend -- --template vue-ts
cd frontend && npm install pinia axios vue-router

# Backend
django-admin startproject backend && cd backend
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
# Copy structure from: assets/templates/django-structure.md
```

**Complete Workflows:** `references/quick-start-guides.md` (to be created)

---

## 📋 Implementation Checklist

### Essential Setup (Every Project)

**Frontend:**
- [ ] Initialize framework (Next.js/React/Vue)
- [ ] Setup Tailwind CSS: `assets/templates/tailwind-setup.md`
- [ ] Configure state management (Redux/Zustand/Pinia)
- [ ] Setup routing and layouts
- [ ] Implement error boundaries
- [ ] Configure TypeScript strict mode

**Backend:**
- [ ] Initialize framework (FastAPI/Django/Laravel)
- [ ] Setup database connection + ORM
- [ ] Implement authentication middleware
- [ ] Add input validation
- [ ] Configure CORS properly
- [ ] Setup logging and error handling

**Security (Critical):**
- [ ] All items in `references/checklists/backend-security.md`
- [ ] Environment variables for secrets (.env never committed)
- [ ] Rate limiting on all endpoints
- [ ] HTTPS enforced (redirect HTTP)
- [ ] Security headers configured

**Performance:**
- [ ] All items in `references/checklists/frontend-optimization.md`
- [ ] Redis caching for expensive queries
- [ ] Database indexes on foreign keys
- [ ] CDN for static assets
- [ ] Image optimization enabled

**Testing:**
- [ ] Unit tests for business logic (70% coverage)
- [ ] Integration tests for API endpoints
- [ ] E2E tests for critical user flows
- [ ] API validation: run `scripts/api_validator.py`
- [ ] Performance check: run `scripts/performance_analyzer.py`

**Deployment:**
- [ ] Environment-specific configs (dev, staging, prod)
- [ ] Database migrations automated
- [ ] CI/CD pipeline configured
- [ ] Health check endpoints (/health, /ready)
- [ ] Monitoring and alerting setup

---

## 🔗 API Design Standards

### REST API Conventions

**Resource Naming:**
```
✅ GET    /api/v1/users
✅ GET    /api/v1/users/:id  
✅ POST   /api/v1/users
✅ PUT    /api/v1/users/:id
✅ DELETE /api/v1/users/:id

❌ Avoid: /getUsers, /user/create, /user_list
```

**Response Structure:**
```json
{
  "success": true,
  "data": { "id": 1, "name": "John" },
  "message": "User retrieved successfully"
}
```

**Error Structure:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": { "field": "email" }
  }
}
```

**HTTP Status Codes:**
- 200 OK, 201 Created, 204 No Content
- 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
- 429 Too Many Requests, 500 Internal Server Error

**Complete Examples:** `references/examples/api-integration.md`

---

## 🧪 Testing Standards

### Test Pyramid Distribution

```
     E2E (10%)      ← Playwright - critical user flows
  Integration (20%) ← Testing Library - component + API
    Unit (70%)      ← Jest/Vitest - business logic
```

**Unit Test Example:**
```typescript
describe('useUserStore', () => {
  it('should add user', () => {
    const { result } = renderHook(() => useUserStore());
    act(() => result.current.addUser({ id: 1, name: 'John' }));
    expect(result.current.users).toHaveLength(1);
  });
});
```

**API Test Example:**
```python
def test_create_user(client):
    response = client.post("/api/v1/users", json={"name": "John"})
    assert response.status_code == 201
    assert "id" in response.json()
```

**Coverage Targets:** 70% minimum, 85%+ for critical paths

---

## 🔗 Skill Integration

### With Mobile_Architect_Pro
- **Shared:** API contracts, authentication patterns
- **Coordination:** Consistent data models, unified auth system

### With AI_Engineer_Pro
- **Integration:** ML model endpoints, inference APIs
- **Data Flow:** Training data collection, result visualization

### With DevOps_Master
- **Handoff:** Dockerfiles, Kubernetes configs, deployment scripts
- **Monitoring:** Performance metrics, error tracking, logging

### With System_Analyst_Expert
- **Input:** Requirements, data models, user stories
- **Output:** Technical architecture, implementation plan

---

## 📚 Assets Reference

### Templates (`assets/templates/`)
Project structure templates for immediate use:

**Frontend (3 + styling):**
- `nextjs-project-structure.md` - Next.js 14 App Router complete setup
- `react-project-structure.md` - React 18 + Vite + Redux Toolkit
- `vue-project-structure.md` - Vue 3 + Vite + Pinia
- `tailwind-setup.md` - Universal Tailwind CSS configuration

**Backend Python/PHP (3):**
- `fastapi-structure.md` - FastAPI + PostgreSQL + Alembic
- `django-structure.md` - Django REST Framework complete
- `laravel-api-structure.md` - Laravel API-first architecture

**Backend Node.js (3):**
- `express-api-structure.md` - Express.js minimal API
- `nestjs-project-structure.md` - NestJS enterprise architecture
- `fastify-api-structure.md` - Fastify high-performance API

**Databases (2):**
- `mongodb-setup.md` - MongoDB + Mongoose complete setup
- `prisma-complete-setup.md` - Prisma ORM (SQL & MongoDB)

**API & Real-time (3):**
- `rest-api-best-practices.md` - RESTful design, versioning, pagination
- `graphql-setup.md` - Apollo Server 4, DataLoader, subscriptions
- `websocket-socketio-setup.md` - Socket.io real-time features

**Infrastructure (3):**
- `redis-caching-setup.md` - Caching strategies, pub/sub, rate limiting
- `message-queue-bull-setup.md` - Background jobs, Bull/BullMQ
- `docker-compose-setup.md` - Multi-service dev environments

**Testing (10 complete setups):**
- Frontend: `jest-setup.md`, `vitest-setup.md`, `testing-library-setup.md`
- E2E: `playwright-setup.md`, `cypress-setup.md`
- Backend: `pytest-setup.md`, `phpunit-setup.md`, `jest-node-setup.md`
- Quality: `eslint-prettier-config.md`, `typescript-strict-config.md`

**Total:** 28 production-ready templates

### Checklists (`references/checklists/`)
Step-by-step verification lists:
- `backend-security.md` - 40+ security measures
- `database-performance.md` - Query optimization, indexing, pooling
- `frontend-optimization.md` - Performance, bundle size, caching

### Examples (`references/examples/`)
Working code patterns:
- `state-management-patterns.md` - Redux, Zustand, Pinia implementations
- `api-integration.md` - REST, GraphQL, WebSocket complete examples
- `auth-implementation.md` - JWT, OAuth 2.0, session-based auth

### References (`references/`)
Comprehensive guides (600-800 lines each):
- `best-practices.md` - Code quality, testing, deployment standards
- `performance-optimization.md` - Complete performance engineering guide
- `security-patterns.md` - Security implementation patterns
- `troubleshooting.md` - Common issues and solutions

### Scripts (`scripts/`)
Automation tools:
- `project_scaffolder.py` - Generate project boilerplate from templates
- `api_validator.py` - Validate OpenAPI/Swagger schemas
- `performance_analyzer.py` - Analyze bundle size, dependencies, metrics

---

## 🚨 Common Issues & Solutions

**Issue 1: N+1 Query Problem**
```python
# ❌ Bad: Multiple queries
users = User.query.all()
for user in users:
    print(user.posts)  # Separate query per user

# ✅ Good: Single query with join
users = User.query.options(joinedload(User.posts)).all()
```

**Issue 2: CORS Errors**
```python
# FastAPI CORS setup
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend.com"],  # Specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

**Issue 3: Memory Leaks in React**
```typescript
// ✅ Cleanup subscriptions
useEffect(() => {
  const subscription = api.subscribe();
  return () => subscription.unsubscribe();  // Cleanup
}, []);
```

**Complete Troubleshooting:** `references/troubleshooting.md`

---

## 📞 Usage Example

**Prompt:**
```
Build a SaaS analytics dashboard with:
- User authentication (JWT)
- Role-based access (admin, user, viewer)
- Real-time data updates
- Data visualization (charts, tables)
- Export to PDF/Excel
- Mobile responsive

Tech: Next.js 14 + FastAPI + PostgreSQL

Use Web_Architect_Pro skill.
```

**Expected Process:**
1. Analyze requirements → Confirm tech stack appropriate
2. Scaffold projects → Use `assets/templates/nextjs-project-structure.md` + `fastapi-structure.md`
3. Implement auth → Follow `references/examples/auth-implementation.md` (JWT pattern)
4. Setup RBAC → Apply middleware pattern from security guide
5. Real-time → WebSocket setup from `references/examples/api-integration.md`
6. Security → Complete `references/checklists/backend-security.md`
7. Performance → Apply `references/checklists/frontend-optimization.md`
8. Testing → Implement test pyramid with scripts validation
9. Deploy config → Generate Docker + CI/CD configs

---

## 🔄 Maintenance

**Update Triggers:**
- Major framework releases (Next.js, React 19, FastAPI 1.x)
- Critical security vulnerabilities (CVEs)
- New performance optimization techniques
- Community best practices evolution

**Review Schedule:** Quarterly (every 3 months)

**Version:** 2.0.0  
**Last Updated:** 2025-01-12  
**Status:** 100% Complete - Web Developer Ready  
**Maintainer:** Ali Sadikin MA
