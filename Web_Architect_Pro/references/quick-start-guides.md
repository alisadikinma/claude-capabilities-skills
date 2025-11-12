# Quick Start Guides

Complete workflows untuk setup berbagai tech stack combinations dengan command lengkap.

---

## 1. Next.js 14 + FastAPI + PostgreSQL

**Best For:** Modern SaaS, SEO-critical apps, ML integration

### Prerequisites
```bash
node >= 18.0.0
python >= 3.11
postgresql >= 15
```

### Frontend Setup (Next.js 14)

**Create Project:**
```bash
npx create-next-app@latest my-app --typescript --tailwind --app
cd my-app
```

**Install Dependencies:**
```bash
npm install zustand axios @tanstack/react-query
npm install -D @types/node
```

**Project Structure:**
```
my-app/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/
│   │   └── page.tsx
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   └── shared/
├── lib/
│   ├── api.ts
│   ├── stores/
│   └── utils/
└── public/
```

**API Client Setup (`lib/api.ts`):**
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

**Environment Variables (`.env.local`):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Run Development Server:**
```bash
npm run dev
```

---

### Backend Setup (FastAPI)

**Create Virtual Environment:**
```bash
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**Install Dependencies:**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
pip install pydantic-settings
```

**Project Structure:**
```bash
mkdir -p app/{api/v1/endpoints,core,crud,models,schemas}
touch app/{__init__,main,database}.py
touch app/core/{config,security}.py
touch app/api/v1/{router,deps}.py
```

**Complete Structure:**
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── users.py
│   │       │   └── auth.py
│   │       ├── router.py
│   │       └── deps.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── __init__.py
│   │   └── crud_user.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── __init__.py
│   ├── main.py
│   └── database.py
├── alembic/
├── venv/
├── .env
└── requirements.txt
```

**Main Application (`app/main.py`):**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**Configuration (`app/core/config.py`):**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My App"
    DATABASE_URL: str = "postgresql://user:password@localhost/myapp"
    SECRET_KEY: str = "your-secret-key-here"
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
```

**Environment Variables (`.env`):**
```env
PROJECT_NAME=MyApp
DATABASE_URL=postgresql://myapp_user:password@localhost/myapp_db
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_ORIGINS=["http://localhost:3000"]
```

**Run Server:**
```bash
uvicorn app.main:app --reload --port 8000
```

---

### Database Setup (PostgreSQL)

**Create Database:**
```bash
# Linux/Mac
sudo -u postgres psql

# Windows (as postgres user)
psql -U postgres
```

**SQL Commands:**
```sql
CREATE DATABASE myapp_db;
CREATE USER myapp_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;
\q
```

**Initialize Alembic:**
```bash
cd backend
alembic init alembic
```

**Update `alembic.ini`:**
```ini
sqlalchemy.url = postgresql://myapp_user:secure_password_here@localhost/myapp_db
```

**Create First Migration:**
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

### Deployment

**Vercel (Frontend):**
```bash
cd my-app
vercel
```

**Railway (Backend + Database):**
```bash
cd backend
railway init
railway up
```

---

## 2. React 18 + Laravel 10 + MySQL

**Best For:** Traditional business apps, admin panels, PHP teams

### Frontend Setup (React + Vite)

**Create Project:**
```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
```

**Install Dependencies:**
```bash
npm install @reduxjs/toolkit react-redux axios react-router-dom
npm install -D @types/react-router-dom
```

**Run Development:**
```bash
npm run dev
```

---

### Backend Setup (Laravel 10)

**Create Project:**
```bash
composer create-project laravel/laravel backend
cd backend
```

**Install API Dependencies:**
```bash
composer require laravel/sanctum
php artisan install:api
```

**Configure CORS (`config/cors.php`):**
```php
return [
    'paths' => ['api/*', 'sanctum/csrf-cookie'],
    'allowed_origins' => ['http://localhost:5173'],
    'allowed_methods' => ['*'],
    'allowed_headers' => ['*'],
    'supports_credentials' => true,
];
```

**Database Configuration (`.env`):**
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=myapp_db
DB_USERNAME=root
DB_PASSWORD=your_password
```

**Create Database:**
```bash
mysql -u root -p
CREATE DATABASE myapp_db;
```

**Run Migrations:**
```bash
php artisan migrate
```

**Start Server:**
```bash
php artisan serve
```

---

## 3. Vue 3 + Django 4 + PostgreSQL

**Best For:** Content platforms, Python teams, strong admin needs

### Frontend Setup (Vue 3)

**Create Project:**
```bash
npm create vite@latest frontend -- --template vue-ts
cd frontend
```

**Install Dependencies:**
```bash
npm install pinia axios vue-router
npm install -D @types/node
```

**Run Development:**
```bash
npm run dev
```

---

### Backend Setup (Django 4)

**Create Project:**
```bash
django-admin startproject backend
cd backend
```

**Install Dependencies:**
```bash
pip install djangorestframework djangorestframework-simplejwt
pip install django-cors-headers psycopg2-binary
```

**Update `settings.py`:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myapp_db',
        'USER': 'myapp_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

**Run Migrations:**
```bash
python manage.py migrate
```

**Create Superuser:**
```bash
python manage.py createsuperuser
```

**Start Server:**
```bash
python manage.py runserver
```

---

## 4. Next.js + NestJS + PostgreSQL

**Best For:** Enterprise apps, TypeScript end-to-end, microservices

### Frontend Setup (Same as #1)

See Next.js setup in section 1.

---

### Backend Setup (NestJS)

**Create Project:**
```bash
npm i -g @nestjs/cli
nest new backend
cd backend
```

**Install Dependencies:**
```bash
npm install @nestjs/typeorm typeorm pg
npm install @nestjs/passport passport passport-jwt
npm install @nestjs/jwt bcrypt
npm install -D @types/passport-jwt @types/bcrypt
```

**Generate Modules:**
```bash
nest g module users
nest g module auth
nest g controller users
nest g service users
nest g service auth
```

**Database Configuration (`app.module.ts`):**
```typescript
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'myapp_user',
      password: 'password',
      database: 'myapp_db',
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      synchronize: true, // Don't use in production
    }),
  ],
})
export class AppModule {}
```

**Run Development:**
```bash
npm run start:dev
```

---

## 5. Serverless (Next.js + Supabase)

**Best For:** MVP, startups, variable traffic

### Setup Next.js

Same as section 1, but skip backend setup.

---

### Setup Supabase

**Install Supabase Client:**
```bash
npm install @supabase/supabase-js
```

**Create Supabase Client (`lib/supabase.ts`):**
```typescript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseKey);
```

**Environment Variables (`.env.local`):**
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

**Usage Example:**
```typescript
// Fetch data
const { data, error } = await supabase
  .from('users')
  .select('*');

// Insert data
const { data, error } = await supabase
  .from('users')
  .insert({ name: 'John', email: 'john@example.com' });

// Authentication
const { user, error } = await supabase.auth.signUp({
  email: 'user@email.com',
  password: 'password',
});
```

**Deploy:**
```bash
vercel
```

---

## Common Next Steps (All Stacks)

### Add Authentication

**JWT Implementation:** See `references/examples/auth-implementation.md`

### Add Testing

**Frontend:**
```bash
npm install -D vitest @testing-library/react
```

**Backend (Python):**
```bash
pip install pytest pytest-asyncio httpx
```

**Backend (Node.js):**
```bash
npm install -D jest @types/jest
```

### Add Docker

**Create `docker-compose.yml`:**
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp_db
      POSTGRES_USER: myapp_user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Run:**
```bash
docker-compose up -d
```

---

**Last Updated:** 2025-01-11
