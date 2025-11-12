# Security Patterns & Implementation

**Last Updated:** 2025-01-11  
**Category:** Reference Guide

---

## 🔐 Authentication Patterns

### 1. JWT Authentication (Recommended)

**Implementation (FastAPI):**
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key-here-min-32-chars"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Login endpoint
@app.post("/auth/login")
async def login(credentials: LoginSchema):
    user = authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

# Protected endpoint
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    user_id = payload.get("sub")
    user = await db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.name}"}
```

**Frontend (React/Next.js):**
```typescript
// lib/auth.ts
import axios from 'axios';

interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

class AuthService {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  
  async login(email: string, password: string): Promise<void> {
    const response = await axios.post<AuthTokens>('/auth/login', {
      email,
      password
    });
    
    this.setTokens(response.data);
  }
  
  private setTokens(tokens: AuthTokens): void {
    this.accessToken = tokens.accessToken;
    this.refreshToken = tokens.refreshToken;
    localStorage.setItem('refreshToken', tokens.refreshToken);
    
    // Set auto-refresh before expiry
    const refreshTime = (tokens.expiresIn - 60) * 1000;
    setTimeout(() => this.refreshAccessToken(), refreshTime);
  }
  
  async refreshAccessToken(): Promise<void> {
    if (!this.refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const response = await axios.post<AuthTokens>('/auth/refresh', {
      refreshToken: this.refreshToken
    });
    
    this.setTokens(response.data);
  }
  
  getAccessToken(): string | null {
    return this.accessToken;
  }
  
  logout(): void {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('refreshToken');
  }
}

export const authService = new AuthService();

// Axios interceptor
axios.interceptors.request.use(
  (config) => {
    const token = authService.getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        await authService.refreshAccessToken();
        return axios(originalRequest);
      } catch (refreshError) {
        authService.logout();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
```

### 2. OAuth 2.0 Implementation

**Google OAuth (FastAPI):**
```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get('/auth/google/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth/google/callback')
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    
    # Find or create user
    user = await get_or_create_user(
        email=user_info['email'],
        name=user_info['name'],
        provider='google'
    )
    
    # Create JWT tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
```

---

## 🛡️ Authorization Patterns

### 1. Role-Based Access Control (RBAC)

**Database Schema:**
```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    resource VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL
);

CREATE TABLE role_permissions (
    role_id INTEGER REFERENCES roles(id),
    permission_id INTEGER REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id),
    role_id INTEGER REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
```

**Implementation (FastAPI):**
```python
from functools import wraps
from typing import List

class PermissionChecker:
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions
    
    async def __call__(self, current_user: User = Depends(get_current_user)):
        user_permissions = await get_user_permissions(current_user.id)
        
        for permission in self.required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission denied: {permission}"
                )
        
        return current_user

# Usage
@app.post("/posts")
async def create_post(
    post: PostCreate,
    user: User = Depends(PermissionChecker(["posts.create"]))
):
    return await create_post_service(post, user)
```

---

## 🔒 Input Validation & Sanitization

### 1. Backend Validation

**Pydantic Schemas (FastAPI):**
```python
from pydantic import BaseModel, EmailStr, validator, Field
import re

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: str = Field(..., min_length=2, max_length=100)
    
    @validator('password')
    def password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain digit')
        if not re.search(r'[!@#$%^&*()]', v):
            raise ValueError('Password must contain special char')
        return v
```

### 2. Frontend Validation

**Zod Schema (React/Next.js):**
```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z
    .string()
    .min(8, 'Min 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/\d/, 'Must contain digit')
    .regex(/[!@#$%^&*]/, 'Must contain special char'),
  name: z.string().min(2).max(100),
});

// Usage
const result = userSchema.safeParse(formData);
if (!result.success) {
  showErrors(result.error.errors);
}
```

---

## 🛡️ XSS Prevention

**Content Security Policy:**
```typescript
// Next.js middleware
export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
  );
  
  return response;
}
```

**HTML Sanitization:**
```typescript
import DOMPurify from 'isomorphic-dompurify';

const cleanHTML = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
  ALLOWED_ATTR: ['href']
});
```

---

## 🔐 CSRF Protection

**FastAPI:**
```python
from fastapi_csrf_protect import CsrfProtect

@app.post("/posts")
async def create_post(
    post: PostCreate,
    csrf_protect: CsrfProtect = Depends()
):
    csrf_protect.validate_csrf(request)
    return await create_post_service(post)
```

---

## 🔒 Rate Limiting

**FastAPI:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginSchema):
    pass
```

---

## 📋 Security Checklist

**Authentication & Authorization:**
- [ ] Passwords hashed with bcrypt (cost ≥ 10)
- [ ] JWT tokens with short expiry (15 min + refresh)
- [ ] Secure token storage (httpOnly cookies)
- [ ] RBAC/ABAC implemented
- [ ] OAuth 2.0 for third-party auth
- [ ] 2FA for sensitive operations

**Input Validation:**
- [ ] All inputs validated (frontend + backend)
- [ ] SQL injection prevention (ORM/parameterized)
- [ ] XSS prevention (CSP + sanitization)
- [ ] CSRF protection enabled
- [ ] File upload validation
- [ ] API request size limits

**Headers & Config:**
- [ ] HTTPS enforced
- [ ] HSTS header enabled
- [ ] X-Frame-Options set
- [ ] X-Content-Type-Options: nosniff
- [ ] CSP configured
- [ ] CORS with specific origins

**API Security:**
- [ ] Rate limiting (100 req/min)
- [ ] API keys for external access
- [ ] Request authentication
- [ ] Error messages sanitized
- [ ] Security event logging

---

**Last Updated:** 2025-01-11  
**Maintained by:** Ali Sadikin MA
