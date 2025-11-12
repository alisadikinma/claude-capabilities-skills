# Web + Mobile + API Integration Blueprint

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                         │
├──────────────────────┬──────────────────────────────────┤
│   Web (Next.js)      │     Mobile (Flutter)             │
│   - SSR/SSG pages    │     - iOS/Android apps           │
│   - React components │     - Offline-first              │
│   - State management │     - Local storage              │
└──────────┬───────────┴──────────────┬───────────────────┘
           │                          │
           │    ┌────────────────────────────┐
           └────►   API Gateway / BFF       │
                │   - Rate limiting          │
                │   - Authentication         │
                │   - Request routing        │
                └─────────┬──────────────────┘
                          │
           ┌──────────────┼──────────────┬────────────────┐
           │              │              │                │
    ┌──────▼───────┐ ┌───▼────────┐ ┌──▼─────────┐ ┌───▼──────┐
    │    Auth      │ │   Users    │ │  Content   │ │Analytics │
    │   Service    │ │  Service   │ │  Service   │ │ Service  │
    └──────┬───────┘ └───┬────────┘ └──┬─────────┘ └───┬──────┘
           │             │              │               │
    ┌──────▼─────┐  ┌───▼─────┐   ┌───▼──────┐   ┌────▼─────┐
    │PostgreSQL  │  │PostgreSQL│   │PostgreSQL│   │InfluxDB  │
    │(Auth DB)   │  │(User DB) │   │(Content) │   │(Metrics) │
    └────────────┘  └──────────┘   └──────────┘   └──────────┘
           │
    ┌──────▼─────────────────────────────────┐
    │         Redis (Cache + Sessions)       │
    └────────────────────────────────────────┘
```

## Technology Stack

### Web Frontend (Next.js)
```yaml
framework: Next.js 14 (App Router)
language: TypeScript
state: Zustand / React Query
styling: Tailwind CSS
forms: React Hook Form + Zod
auth: NextAuth.js
api_client: Axios / Fetch with interceptors
```

### Mobile App (Flutter)
```yaml
framework: Flutter 3.x
language: Dart
state: BLoC / Riverpod
networking: Dio
local_db: Hive / Drift
auth: flutter_secure_storage
offline: Connectivity Plus + Queue
```

### Backend API
```yaml
framework: FastAPI (Python) or NestJS (Node.js)
database: PostgreSQL
cache: Redis
authentication: JWT + Refresh tokens
api_style: RESTful
documentation: OpenAPI (Swagger)
```

## API Design Patterns

### 1. RESTful API Structure

```
Base URL: https://api.example.com/v1

Endpoints:
POST   /auth/login              # Login
POST   /auth/refresh            # Refresh token
POST   /auth/logout             # Logout

GET    /users                   # List users (paginated)
GET    /users/:id               # Get user details
POST   /users                   # Create user
PUT    /users/:id               # Update user
DELETE /users/:id               # Delete user

GET    /posts                   # List posts (paginated, filtered)
GET    /posts/:id               # Get post details
POST   /posts                   # Create post
PUT    /posts/:id               # Update post
DELETE /posts/:id               # Delete post

GET    /posts/:id/comments      # Get post comments
POST   /posts/:id/comments      # Add comment

GET    /users/:id/posts         # Get user's posts
GET    /users/:id/followers     # Get user's followers
```

### 2. Authentication Flow

```
┌────────┐                  ┌────────────┐              ┌─────────┐
│ Client │                  │API Gateway │              │Auth Svc │
└───┬────┘                  └─────┬──────┘              └────┬────┘
    │                             │                          │
    │ POST /auth/login            │                          │
    ├────────────────────────────►│                          │
    │ {email, password}           │   Verify credentials     │
    │                             ├─────────────────────────►│
    │                             │                          │
    │                             │  {access_token,          │
    │                             │   refresh_token,         │
    │  {access_token,             │   expires_in}            │
    │   refresh_token}            │◄─────────────────────────┤
    │◄────────────────────────────┤                          │
    │                             │                          │
    │ Subsequent requests with    │                          │
    │ Authorization: Bearer TOKEN │                          │
    ├────────────────────────────►│                          │
    │                             │  Validate JWT            │
    │                             ├──────────┐               │
    │                             │          │               │
    │         Response            │◄─────────┘               │
    │◄────────────────────────────┤                          │
    │                             │                          │
    │ Token expired (401)         │                          │
    │◄────────────────────────────┤                          │
    │                             │                          │
    │ POST /auth/refresh          │                          │
    ├────────────────────────────►│                          │
    │ {refresh_token}             │   Verify refresh token   │
    │                             ├─────────────────────────►│
    │                             │                          │
    │  New access_token           │  New access_token        │
    │◄────────────────────────────┤◄─────────────────────────┤
```

### 3. Request/Response Format

**Standard Success Response:**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2025-01-11T10:00:00Z"
  }
}
```

**Paginated Response:**
```json
{
  "success": true,
  "data": [
    {"id": 1, "title": "Post 1"},
    {"id": 2, "title": "Post 2"}
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters"
      }
    ]
  }
}
```

## Implementation Examples

### Web (Next.js)

**API Client Setup:**
```typescript
// lib/api-client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
});

// Request interceptor (add auth token)
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor (handle token refresh)
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try refresh
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const { data } = await axios.post('/auth/refresh', {
            refresh_token: refreshToken,
          });
          localStorage.setItem('access_token', data.access_token);
          // Retry original request
          return apiClient(error.config);
        } catch {
          // Refresh failed, logout
          localStorage.clear();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

**React Query Integration:**
```typescript
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';

export function useUsers(page = 1) {
  return useQuery({
    queryKey: ['users', page],
    queryFn: async () => {
      const { data } = await apiClient.get(`/users?page=${page}`);
      return data;
    },
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (userData) => {
      const { data } = await apiClient.post('/users', userData);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### Mobile (Flutter)

**API Client Setup:**
```dart
// lib/services/api_client.dart
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiClient {
  final Dio _dio;
  final FlutterSecureStorage _storage;

  ApiClient()
      : _dio = Dio(BaseOptions(
          baseUrl: 'https://api.example.com/v1',
          connectTimeout: Duration(seconds: 10),
        )),
        _storage = const FlutterSecureStorage() {
    _setupInterceptors();
  }

  void _setupInterceptors() {
    // Request interceptor (add token)
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await _storage.read(key: 'access_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          // Token expired, refresh
          final refreshed = await _refreshToken();
          if (refreshed) {
            // Retry request
            final options = error.requestOptions;
            final token = await _storage.read(key: 'access_token');
            options.headers['Authorization'] = 'Bearer $token';
            final response = await _dio.fetch(options);
            return handler.resolve(response);
          } else {
            // Refresh failed, logout
            await _storage.deleteAll();
            // Navigate to login
          }
        }
        handler.next(error);
      },
    ));
  }

  Future<bool> _refreshToken() async {
    try {
      final refreshToken = await _storage.read(key: 'refresh_token');
      final response = await _dio.post('/auth/refresh', data: {
        'refresh_token': refreshToken,
      });
      
      await _storage.write(
        key: 'access_token',
        value: response.data['access_token'],
      );
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<List<User>> getUsers({int page = 1}) async {
    final response = await _dio.get('/users', queryParameters: {'page': page});
    return (response.data['data'] as List)
        .map((json) => User.fromJson(json))
        .toList();
  }
}
```

**Offline Queue Implementation:**
```dart
// lib/services/offline_queue.dart
import 'package:hive/hive.dart';

class OfflineQueue {
  static const String boxName = 'pending_requests';
  
  Future<void> enqueue(PendingRequest request) async {
    final box = await Hive.openBox<PendingRequest>(boxName);
    await box.add(request);
  }
  
  Future<void> processQueue() async {
    final box = await Hive.openBox<PendingRequest>(boxName);
    final requests = box.values.toList();
    
    for (final request in requests) {
      try {
        await _executeRequest(request);
        await box.delete(request.key);
      } catch (e) {
        // Keep in queue for retry
      }
    }
  }
  
  Future<void> _executeRequest(PendingRequest request) async {
    final dio = Dio();
    await dio.request(
      request.url,
      data: request.body,
      options: Options(method: request.method),
    );
  }
}

@HiveType(typeId: 1)
class PendingRequest extends HiveObject {
  @HiveField(0)
  String method;
  
  @HiveField(1)
  String url;
  
  @HiveField(2)
  Map<String, dynamic>? body;
  
  @HiveField(3)
  DateTime timestamp;
  
  PendingRequest({
    required this.method,
    required this.url,
    this.body,
    required this.timestamp,
  });
}
```

## Backend (FastAPI)

**Main Application:**
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, posts

app = FastAPI(title="API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])

@app.get("/")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
```

**Authentication Router:**
```python
# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime, timedelta
import jwt

router = APIRouter()

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 3600,
        }
    }

@router.post("/refresh")
def refresh_token(request: RefreshRequest):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["sub"]
        
        new_access_token = create_access_token(user_id)
        
        return {
            "success": True,
            "data": {
                "access_token": new_access_token,
                "token_type": "bearer",
                "expires_in": 3600,
            }
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
```

## Performance Optimization

### 1. Caching Strategy
- **API responses:** Redis (5-15 min TTL)
- **Static assets:** CDN (1 year TTL)
- **Database queries:** Redis + cache-aside pattern

### 2. Rate Limiting
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(redis)

@app.get("/api/resource", dependencies=[Depends(RateLimiter(times=100, seconds=60))])
def get_resource():
    return {"data": "..."}
```

### 3. Pagination Best Practices
- Default: 20 items per page
- Max: 100 items per page
- Use cursor-based for large datasets

## Security Checklist

- [ ] HTTPS enforced
- [ ] JWT with short expiry (15-60 min)
- [ ] Refresh tokens with rotation
- [ ] Rate limiting per IP/user
- [ ] Input validation (Zod/Pydantic)
- [ ] SQL injection prevention (ORM)
- [ ] XSS prevention (sanitize outputs)
- [ ] CORS properly configured
- [ ] API keys for third-party access
- [ ] Audit logging for sensitive operations

---

**Estimated Costs (per month):**
- Dev: $100-200 (VPS + Redis)
- Production: $300-800 (Load balancer + Redis + DB)
