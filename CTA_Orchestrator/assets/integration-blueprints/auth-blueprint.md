# Authentication & Authorization Blueprint

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                            │
│  (Web App / Mobile App / Third-party Apps)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ 1. Login / API Key
                        │
             ┌──────────▼──────────┐
             │   API Gateway       │
             │  - Rate limiting    │
             │  - CORS             │
             └──────────┬──────────┘
                        │
                        │ 2. Validate Token / API Key
                        │
             ┌──────────▼──────────┐
             │  Auth Middleware    │
             │  - JWT validation   │
             │  - Permission check │
             └──────────┬──────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
    ┌─────▼──────┐ ┌───▼─────┐ ┌─────▼──────┐
    │  User Svc  │ │ Auth Svc│ │Resource Svc│
    └─────┬──────┘ └───┬─────┘ └─────┬──────┘
          │            │             │
    ┌─────▼────────────▼─────────────▼─────┐
    │         PostgreSQL / Redis           │
    │  - Users, roles, permissions         │
    │  - Tokens, sessions                  │
    └──────────────────────────────────────┘
```

## Authentication Methods Comparison

| Method | Stateless | Scalability | Security | Use Case |
|--------|-----------|-------------|----------|----------|
| **Session Cookies** | ❌ | Low | Good | Traditional web apps |
| **JWT** | ✅ | High | Good | SPA, Mobile, Microservices |
| **OAuth 2.0** | ✅ | High | Excellent | Third-party integrations |
| **API Keys** | ✅ | High | Medium | Service-to-service |
| **SAML** | ❌ | Medium | Excellent | Enterprise SSO |
| **WebAuthn** | ✅ | High | Excellent | Passwordless auth |

## 1. JWT-Based Authentication

### Token Structure

```
Access Token (Short-lived: 15-60 min):
{
  "user_id": "123",
  "email": "user@example.com",
  "roles": ["user"],
  "exp": 1641234567,
  "iat": 1641230967
}

Refresh Token (Long-lived: 7-30 days):
{
  "user_id": "123",
  "token_family": "abc123",  # For token rotation
  "exp": 1643826567,
  "iat": 1641230967
}
```

### Implementation (FastAPI)

**Token Generation:**
```python
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: str, token_family: str):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode(
        {"user_id": user_id, "token_family": token_family, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

**Login Endpoint:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uuid

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Validate credentials
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Generate tokens
    token_family = str(uuid.uuid4())
    access_token = create_access_token({
        "user_id": str(user.id),
        "email": user.email,
        "roles": [r.name for r in user.roles]
    })
    refresh_token = create_refresh_token(str(user.id), token_family)
    
    # Store refresh token (for rotation detection)
    store_refresh_token(user.id, token_family, refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["user_id"]
        token_family = payload["token_family"]
        
        # Check if token is revoked
        if is_token_revoked(user_id, token_family):
            raise HTTPException(401, "Token revoked")
        
        # Generate new access token
        user = db.query(User).get(user_id)
        new_access_token = create_access_token({
            "user_id": str(user.id),
            "email": user.email,
            "roles": [r.name for r in user.roles]
        })
        
        # Optional: Rotate refresh token
        new_refresh_token = create_refresh_token(user_id, token_family)
        store_refresh_token(user_id, token_family, new_refresh_token)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid refresh token")

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Revoke all tokens in this family
    revoke_token_family(payload["user_id"], payload.get("token_family"))
    
    return {"message": "Logged out successfully"}
```

**Authentication Dependency:**
```python
from fastapi import Depends, HTTPException, status

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(401, "Invalid token")
        
        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(401, "User not found")
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

# Usage in protected routes
@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }
```

## 2. Role-Based Access Control (RBAC)

### Database Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    resource VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL
);

CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id),
    role_id INTEGER REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE role_permissions (
    role_id INTEGER REFERENCES roles(id),
    permission_id INTEGER REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);

-- Example data
INSERT INTO roles (name, description) VALUES
    ('admin', 'Full system access'),
    ('user', 'Standard user access'),
    ('moderator', 'Content moderation access');

INSERT INTO permissions (name, resource, action) VALUES
    ('users.read', 'users', 'read'),
    ('users.create', 'users', 'create'),
    ('users.update', 'users', 'update'),
    ('users.delete', 'users', 'delete'),
    ('posts.read', 'posts', 'read'),
    ('posts.create', 'posts', 'create'),
    ('posts.delete', 'posts', 'delete');
```

### Authorization Middleware

```python
from functools import wraps
from typing import List

def require_permissions(required_permissions: List[str]):
    def decorator(func):
        @wraps(func)
        def wrapper(
            *args,
            current_user: User = Depends(get_current_user),
            db: Session = Depends(get_db),
            **kwargs
        ):
            # Get user permissions
            user_permissions = get_user_permissions(current_user.id, db)
            
            # Check if user has required permissions
            if not all(perm in user_permissions for perm in required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return func(*args, current_user=current_user, db=db, **kwargs)
        return wrapper
    return decorator

def get_user_permissions(user_id: int, db: Session) -> List[str]:
    # Get permissions from cache
    cached = redis.get(f"user_permissions:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Query database
    permissions = db.query(Permission.name).join(
        role_permissions, Permission.id == role_permissions.c.permission_id
    ).join(
        user_roles, role_permissions.c.role_id == user_roles.c.role_id
    ).filter(
        user_roles.c.user_id == user_id
    ).all()
    
    permission_list = [p.name for p in permissions]
    
    # Cache for 5 minutes
    redis.setex(
        f"user_permissions:{user_id}",
        300,
        json.dumps(permission_list)
    )
    
    return permission_list

# Usage
@router.delete("/users/{user_id}")
@require_permissions(["users.delete"])
def delete_user(user_id: int, current_user: User, db: Session):
    user = db.query(User).get(user_id)
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
```

## 3. OAuth 2.0 Integration

### Provider Configuration

```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

oauth.register(
    name='google',
    client_id='your-client-id',
    client_secret='your-client-secret',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

oauth.register(
    name='github',
    client_id='your-client-id',
    client_secret='your-client-secret',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'}
)

@router.get("/oauth/login/{provider}")
async def oauth_login(provider: str, request: Request):
    redirect_uri = request.url_for('oauth_callback', provider=provider)
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)

@router.get("/oauth/callback/{provider}")
async def oauth_callback(provider: str, request: Request, db: Session = Depends(get_db)):
    token = await oauth.create_client(provider).authorize_access_token(request)
    user_info = token.get('userinfo')
    
    # Find or create user
    user = db.query(User).filter(User.email == user_info['email']).first()
    if not user:
        user = User(
            email=user_info['email'],
            name=user_info.get('name'),
            oauth_provider=provider,
            oauth_id=user_info['sub']
        )
        db.add(user)
        db.commit()
    
    # Generate JWT tokens
    access_token = create_access_token({"user_id": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

## 4. API Key Authentication

**For service-to-service communication:**

```python
import secrets
import hashlib

def generate_api_key() -> tuple[str, str]:
    # Generate random key
    key = secrets.token_urlsafe(32)
    
    # Hash for storage
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    
    return key, key_hash

@router.post("/api-keys")
def create_api_key(
    name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate key
    key, key_hash = generate_api_key()
    
    # Store in database
    api_key = APIKey(
        user_id=current_user.id,
        name=name,
        key_hash=key_hash,
        created_at=datetime.utcnow()
    )
    db.add(api_key)
    db.commit()
    
    # Return plain key only once
    return {
        "api_key": key,
        "message": "Save this key, it won't be shown again"
    }

def verify_api_key(api_key: str = Header(None, alias="X-API-Key")):
    if not api_key:
        raise HTTPException(401, "API key missing")
    
    # Hash the provided key
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    # Look up in database
    db_key = db.query(APIKey).filter(APIKey.key_hash == key_hash).first()
    
    if not db_key:
        raise HTTPException(401, "Invalid API key")
    
    if not db_key.is_active:
        raise HTTPException(401, "API key revoked")
    
    # Update last used
    db_key.last_used_at = datetime.utcnow()
    db.commit()
    
    return db_key

# Usage
@router.get("/api/data")
def get_data(api_key: APIKey = Depends(verify_api_key)):
    return {"data": "..."}
```

## 5. Multi-Factor Authentication (MFA)

```python
import pyotp
import qrcode
from io import BytesIO

@router.post("/mfa/setup")
def setup_mfa(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Generate secret
    secret = pyotp.random_base32()
    
    # Store secret (encrypted)
    current_user.mfa_secret = encrypt(secret)
    current_user.mfa_enabled = False  # Not enabled until verified
    db.commit()
    
    # Generate QR code
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=current_user.email,
        issuer_name="YourApp"
    )
    
    qr = qrcode.make(totp_uri)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        "secret": secret,
        "qr_code": f"data:image/png;base64,{qr_code}"
    }

@router.post("/mfa/verify")
def verify_mfa(
    code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Decrypt secret
    secret = decrypt(current_user.mfa_secret)
    
    # Verify code
    totp = pyotp.TOTP(secret)
    if not totp.verify(code, valid_window=1):
        raise HTTPException(400, "Invalid MFA code")
    
    # Enable MFA
    current_user.mfa_enabled = True
    db.commit()
    
    return {"message": "MFA enabled successfully"}

@router.post("/login/mfa")
def login_with_mfa(
    credentials: LoginRequest,
    mfa_code: str,
    db: Session = Depends(get_db)
):
    # Verify credentials
    user = authenticate_user(credentials.email, credentials.password, db)
    
    if not user.mfa_enabled:
        raise HTTPException(400, "MFA not enabled")
    
    # Verify MFA code
    secret = decrypt(user.mfa_secret)
    totp = pyotp.TOTP(secret)
    if not totp.verify(mfa_code, valid_window=1):
        raise HTTPException(401, "Invalid MFA code")
    
    # Generate tokens
    access_token = create_access_token({"user_id": str(user.id)})
    
    return {"access_token": access_token}
```

## Security Best Practices

### 1. Token Refresh Rotation

```python
def rotate_refresh_token(old_token: str, db: Session):
    # Decode old token
    payload = jwt.decode(old_token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Check if already used (detect token reuse)
    if is_token_used(old_token):
        # Possible attack: Revoke entire token family
        revoke_token_family(payload["user_id"], payload["token_family"])
        raise HTTPException(401, "Token reuse detected")
    
    # Mark as used
    mark_token_used(old_token)
    
    # Issue new refresh token with new ID
    new_token = create_refresh_token(
        payload["user_id"],
        payload["token_family"]
    )
    
    return new_token
```

### 2. Rate Limiting

```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(redis)

@router.post("/login", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def login(...):
    # Max 5 login attempts per minute
    pass
```

### 3. Password Policies

```python
import re

def validate_password(password: str):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain uppercase letter")
    
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain lowercase letter")
    
    if not re.search(r"\d", password):
        raise ValueError("Password must contain digit")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain special character")
```

---

**Estimated Costs (per month):**
- Self-hosted auth: $0 (part of app server)
- Auth0: $0-240 (free tier → Pro)
- Firebase Auth: $0 (free for most use cases)
- AWS Cognito: $0.0055/MAU (Monthly Active Users)
