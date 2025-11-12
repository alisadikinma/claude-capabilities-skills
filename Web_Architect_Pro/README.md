# Web_Architect_Pro

**Full-Stack Web Development with Production-Ready Templates**

Complete templates, configurations, and best practices for building modern web applications with React, Next.js, Vue.js, Laravel, FastAPI, Django, and more.

---

## 🎯 Purpose

Web_Architect_Pro provides:
- **Production-ready project templates** for 9+ frameworks
- **Complete testing setups** (Jest, Vitest, Playwright, Cypress, pytest)
- **Database configurations** (PostgreSQL, MySQL, MongoDB, Prisma)
- **API patterns** (REST, GraphQL, WebSocket)
- **Infrastructure setup** (Docker, Redis, message queues)
- **Best practices & troubleshooting** guides

---

## 📦 What's Inside

```
Web_Architect_Pro/
├── SKILL.md                          # Main documentation
├── assets/templates/
│   ├── Frontend/                     # 3 frameworks
│   │   ├── nextjs-project-structure.md
│   │   ├── react-project-structure.md
│   │   └── vue-project-structure.md
│   ├── Styling/
│   │   └── tailwind-setup.md
│   ├── Backend/                      # 6 frameworks
│   │   ├── express-api-structure.md
│   │   ├── nestjs-project-structure.md
│   │   ├── fastify-api-structure.md
│   │   ├── fastapi-structure.md
│   │   ├── django-structure.md
│   │   └── laravel-api-structure.md
│   ├── Databases/                    # 2 setups
│   │   ├── mongodb-setup.md
│   │   └── prisma-complete-setup.md
│   ├── API/                          # 3 patterns
│   │   ├── rest-api-best-practices.md
│   │   ├── graphql-setup.md
│   │   └── websocket-socketio-setup.md
│   ├── Infrastructure/               # 3 tools
│   │   ├── redis-caching-setup.md
│   │   ├── message-queue-bull-setup.md
│   │   └── docker-compose-setup.md
│   └── Testing/                      # 10 frameworks
│       ├── jest-setup.md
│       ├── vitest-setup.md
│       ├── playwright-setup.md
│       └── ... (7 more)
├── references/
│   ├── best-practices.md
│   ├── performance-optimization.md
│   ├── security-patterns.md
│   ├── troubleshooting.md
│   ├── tech-stack-guide.md
│   ├── architecture-patterns.md
│   ├── checklists/
│   │   ├── backend-security.md
│   │   ├── database-performance.md
│   │   └── frontend-optimization.md
│   └── examples/
│       ├── api-integration.md
│       ├── auth-implementation.md
│       └── state-management-patterns.md
└── scripts/
    ├── project_scaffolder.py
    ├── api_validator.py
    └── performance_analyzer.py
```

**Total:** 46 files

---

## 🚀 Quick Start

### Create Next.js 14 App

```
"Using Web_Architect_Pro, create a Next.js 14 project with TypeScript, Tailwind, App Router, and Prisma"
```

**Output:** Complete project structure with:
- ✅ TypeScript configuration
- ✅ Tailwind CSS + custom config
- ✅ App Router structure
- ✅ Prisma schema + client
- ✅ ESLint + Prettier
- ✅ API routes
- ✅ Environment variables

### Setup Laravel API

```
"Set up Laravel 11 REST API with JWT authentication and PostgreSQL using Web_Architect_Pro"
```

**Output:**
- ✅ Laravel project structure
- ✅ JWT auth middleware
- ✅ PostgreSQL connection
- ✅ API resource controllers
- ✅ Validation rules
- ✅ CORS configuration

### Add Testing

```
"Add Playwright E2E testing to my Next.js project"
```

**Output:**
- ✅ Playwright installation
- ✅ Test configuration
- ✅ Example tests
- ✅ CI integration

---

## 🎨 Supported Tech Stack

### Frontend (3)
| Framework | Use Case | Learning Curve |
|-----------|----------|----------------|
| **Next.js** | Full-stack React apps, SEO | Medium |
| **React** | SPA, complex UIs | Medium |
| **Vue.js** | Progressive apps, simple learning | Easy |

### Backend (6)
| Framework | Language | Use Case |
|-----------|----------|----------|
| **Express** | Node.js | Simple APIs, flexibility |
| **NestJS** | TypeScript | Enterprise apps, structure |
| **Fastify** | Node.js | High performance APIs |
| **FastAPI** | Python | ML APIs, async |
| **Django** | Python | Full-featured, admin panel |
| **Laravel** | PHP | Rapid development, ecosystem |

### Databases (5)
- **PostgreSQL** - Relational, ACID compliance
- **MySQL** - Relational, widely supported
- **SQLite** - Embedded, local development
- **MongoDB** - NoSQL, flexible schema
- **Prisma** - ORM, type-safe

### API Patterns (3)
- **REST** - Simple, cacheable, stateless
- **GraphQL** - Flexible queries, single endpoint
- **WebSocket** - Real-time, bidirectional

### Infrastructure (3)
- **Docker** - Containerization
- **Redis** - Caching, sessions
- **Bull/BullMQ** - Background jobs, queues

### Testing (10)
- **Frontend:** Jest, Vitest, Testing Library, Playwright, Cypress
- **Backend:** pytest, PHPUnit, Jest (Node.js)
- **Linting:** ESLint, Prettier, TypeScript

---

## 💡 Example Workflows

### Build E-Commerce Platform

**Stack:** Next.js + FastAPI + PostgreSQL + Redis

**1. Frontend (Next.js)**
```
Create Next.js 14 project structure with:
- Product listing pages (SSR)
- Shopping cart (client state)
- Checkout flow
- Admin dashboard
```

**2. Backend (FastAPI)**
```
Create FastAPI structure with:
- Product CRUD endpoints
- Order management
- Payment integration
- User authentication (JWT)
```

**3. Database (Prisma + PostgreSQL)**
```
Set up Prisma schema:
- User, Product, Order, OrderItem tables
- Relations and indexes
- Migrations
```

**4. Caching (Redis)**
```
Add Redis for:
- Product catalog cache
- User sessions
- Cart data
```

**5. Testing**
```
- Playwright for E2E checkout flow
- Jest for React components
- pytest for API endpoints
```

### Build SaaS Dashboard

**Stack:** Vue 3 + NestJS + MongoDB + WebSocket

**Frontend:** Vue 3 with Composition API, real-time updates  
**Backend:** NestJS with TypeORM, WebSocket gateway  
**Database:** MongoDB for flexible schema  
**Real-time:** Socket.io for live notifications

---

## 📊 Decision Guide

### Choose Frontend Framework

```
Need SEO & SSR? → Next.js
SPA with complex state? → React
Simple & fast learning? → Vue.js
```

### Choose Backend Framework

```
TypeScript + structure? → NestJS
Python + ML integration? → FastAPI
PHP + rapid dev? → Laravel
Simple & flexible? → Express
Performance critical? → Fastify
Full-featured? → Django
```

### Choose Database

```
Relational data + ACID? → PostgreSQL
Legacy support? → MySQL
Flexible schema? → MongoDB
Type-safe ORM? → Prisma
Local dev only? → SQLite
```

---

## 🎯 Best Practices

### Frontend
- Use TypeScript for type safety
- Implement code splitting & lazy loading
- Optimize images (next/image, lazy loading)
- Use React Server Components (Next.js 14)
- Implement proper error boundaries

### Backend
- Input validation on all endpoints
- Use DTO/Request validation classes
- Implement rate limiting
- Log errors with structured logging
- Use environment variables for secrets

### Database
- Index frequently queried columns
- Use connection pooling
- Implement query pagination
- Regular backups
- Monitor slow queries

### API
- Version your APIs (v1, v2)
- Use HTTP status codes correctly
- Implement CORS properly
- Rate limit by IP/user
- Document with OpenAPI/Swagger

---

## 🔧 Automation Scripts

### Project Scaffolder
```bash
python scripts/project_scaffolder.py --framework nextjs --template typescript
```

Creates complete project structure with best practices.

### API Validator
```bash
python scripts/api_validator.py --openapi openapi.yaml
```

Validates API endpoints against OpenAPI spec.

### Performance Analyzer
```bash
python scripts/performance_analyzer.py --url https://myapp.com
```

Analyzes frontend performance (Lighthouse metrics).

---

## 📚 Key References

- **best-practices.md** - General web development guidelines
- **performance-optimization.md** - Frontend & backend optimization
- **security-patterns.md** - Auth, CORS, XSS prevention
- **troubleshooting.md** - Common errors and solutions
- **architecture-patterns.md** - MVC, layered, hexagonal

---

## 🔗 Integration with Other Skills

**Works Well With:**
- **AI_Engineer_Pro** - Add AI features to web apps
- **DevOps_Master** - Deploy web applications
- **Mobile_Architect_Pro** - Build API for mobile + web
- **CTA_Orchestrator** - Architecture decisions

**Typical Flow:**
```
CTA_Orchestrator (decide stack)
         ↓
Web_Architect_Pro (build app)
         ↓
DevOps_Master (deploy)
```

---

## 📄 License

Part of SKILLS-CLAUDE project • MIT License

---

**Quick Links:**
- [Main README](../README.md)
- [SKILL.md](SKILL.md) - Full documentation
- [Project Status](../project_status.md)
