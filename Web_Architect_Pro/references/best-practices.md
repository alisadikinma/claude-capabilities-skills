# Web Development Best Practices

**Last Updated:** 2025-01-11  
**Category:** Reference Guide

---

## 📂 Project Structure

### Frontend (Next.js/React)
```
src/
├── app/                    # Next.js 14 App Router
│   ├── (auth)/            # Route groups
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/
│   │   ├── settings/
│   │   └── profile/
│   ├── api/               # API routes
│   │   └── webhooks/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/                # Reusable UI components
│   ├── features/          # Feature-specific components
│   └── layouts/           # Layout components
├── lib/
│   ├── api.ts            # API client
│   ├── utils.ts          # Utilities
│   └── validations.ts    # Zod schemas
├── hooks/                 # Custom hooks
├── store/                 # State management
├── types/                 # TypeScript types
└── config/               # App configuration
```

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   └── posts.py
│   │   │   └── router.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── main.py
├── tests/
├── alembic/              # Migrations
└── requirements.txt
```

---

## 🎨 Code Style

### TypeScript/JavaScript

**Use explicit types:**
```typescript
// ✅ Good
interface User {
  id: number;
  name: string;
  email: string;
}

const fetchUser = async (id: number): Promise<User> => {
  // ...
}

// ❌ Bad
const fetchUser = async (id: any): Promise<any> => {
  // ...
}
```

**Use const for immutability:**
```typescript
// ✅ Good
const MAX_RETRIES = 3;
const users = ['john', 'jane'];

// ❌ Bad
var MAX_RETRIES = 3;
let users = ['john', 'jane'];
```

---

**Last Updated:** 2025-01-11  
**Maintained by:** Ali Sadikin MA
