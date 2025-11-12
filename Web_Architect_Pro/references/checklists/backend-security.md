# Backend Security Checklist

**Priority:** CRITICAL  
**Review:** Before every deployment  
**Last Updated:** 2025-01-11

---

## 🔐 Authentication & Authorization

### Password Security
- [ ] Bcrypt/Argon2 for password hashing (min cost factor 12)
- [ ] Minimum password length 8 characters
- [ ] Password complexity requirements enforced
- [ ] Brute-force protection (rate limiting)
- [ ] No password in logs or error messages
- [ ] Password reset with secure tokens (expire in 1 hour)

### JWT Implementation
- [ ] Secret key minimum 256 bits
- [ ] Access token expiry ≤ 15 minutes
- [ ] Refresh token implemented (7-30 days)
- [ ] Token stored in httpOnly cookies (not localStorage)
- [ ] Algorithm specified (RS256 or HS256)
- [ ] Token blacklist for logout

**Example (FastAPI):**
```python
from datetime import timedelta
from jose import jwt

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"exp": expire, "type": "access", **data}
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

### Authorization
- [ ] RBAC (Role-Based Access Control) implemented
- [ ] Permission checks on every endpoint
- [ ] Principle of least privilege applied
- [ ] Admin actions logged and auditable
- [ ] Resource ownership validated

---

## 🛡️ Input Validation & Sanitization

### Validation
- [ ] All inputs validated (type, format, range)
- [ ] Pydantic/Laravel validation used
- [ ] File upload validation (type, size, content)
- [ ] SQL injection prevented (parameterized queries)
- [ ] NoSQL injection prevented

**Example (Laravel):**
```php
$request->validate([
    'email' => 'required|email|max:255',
    'age' => 'required|integer|min:18|max:120',
    'file' => 'required|file|mimes:jpg,png|max:2048',
]);
```

### XSS Prevention
- [ ] HTML escaped in output
- [ ] Content-Security-Policy header set
- [ ] Sanitize user-generated content
- [ ] Avoid innerHTML, use textContent
- [ ] Validate URLs for redirects

---

## 🌐 API Security

### Rate Limiting
- [ ] Rate limits per IP (100 req/min)
- [ ] Rate limits per user (1000 req/hour)
- [ ] Exponential backoff for failed attempts
- [ ] 429 status code returned

**Example (FastAPI):**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/users")
@limiter.limit("100/minute")
async def list_users():
    ...
```

### CORS Configuration
- [ ] Specific origins allowed (not *)
- [ ] Credentials allowed only when needed
- [ ] Preflight requests handled
- [ ] Exposed headers limited

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Request Security
- [ ] Request size limited (10MB default)
- [ ] Timeout configured (30s default)
- [ ] JSON payload validated
- [ ] Content-Type verified

---

## 🔒 Database Security

### Connection Security
- [ ] Encrypted connections (SSL/TLS)
- [ ] Connection pooling configured
- [ ] Credentials in environment variables
- [ ] Database user has minimal permissions

### Query Security
- [ ] ORM/prepared statements used (no raw SQL)
- [ ] Parameterized queries only
- [ ] Stored procedures for sensitive operations
- [ ] Query logging disabled in production

**Example (SQLAlchemy):**
```python
# ✅ Good - parameterized
user = db.query(User).filter(User.email == email).first()

# ❌ Bad - vulnerable to injection
user = db.execute(f"SELECT * FROM users WHERE email='{email}'")
```

---

## 📝 Error Handling & Logging

### Error Messages
- [ ] Generic error messages to clients
- [ ] Detailed errors in logs only
- [ ] No stack traces in production
- [ ] No sensitive data in errors

**Example:**
```python
try:
    user = authenticate(email, password)
except Exception as e:
    logger.error(f"Auth failed: {e}")  # ✅ Log details
    raise HTTPException(status_code=401, detail="Invalid credentials")  # ✅ Generic
```

### Logging
- [ ] Security events logged (login, permission denied)
- [ ] Logs rotated and archived
- [ ] Logs sanitized (no passwords/tokens)
- [ ] Anomaly detection configured
- [ ] SIEM integration (if applicable)

---

## 🔑 Secrets Management

### Environment Variables
- [ ] All secrets in .env (not in code)
- [ ] .env in .gitignore
- [ ] Different secrets per environment
- [ ] Secrets rotation plan
- [ ] No hardcoded API keys

### Production Secrets
- [ ] Vault/AWS Secrets Manager used
- [ ] Secrets encrypted at rest
- [ ] Access to secrets audited
- [ ] Automatic rotation enabled

---

## 🌐 HTTP Headers

### Security Headers
```nginx
# ✅ Essential security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' https:; script-src 'self';" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

- [ ] X-Frame-Options: SAMEORIGIN
- [ ] X-Content-Type-Options: nosniff
- [ ] X-XSS-Protection: 1; mode=block
- [ ] Referrer-Policy configured
- [ ] Content-Security-Policy set
- [ ] HSTS enabled (HTTPS only)

---

## 🔐 HTTPS & TLS

### SSL/TLS Configuration
- [ ] TLS 1.2+ only (disable TLS 1.0, 1.1)
- [ ] Strong cipher suites only
- [ ] Valid SSL certificate (Let's Encrypt/paid)
- [ ] Certificate auto-renewal configured
- [ ] HTTP redirects to HTTPS (301)
- [ ] HSTS header with long max-age

---

## 📧 Email Security

### Email Sending
- [ ] SPF record configured
- [ ] DKIM signing enabled
- [ ] DMARC policy set
- [ ] Email rate limiting
- [ ] HTML emails sanitized

### Email Verification
- [ ] Email verification required for signup
- [ ] Secure tokens for verification (UUID)
- [ ] Tokens expire after 24 hours
- [ ] Resend verification rate limited

---

## 🗄️ Session Management

### Session Security
- [ ] Secure session cookies (httpOnly, secure, sameSite)
- [ ] Session IDs regenerated after login
- [ ] Sessions timeout after inactivity (30 min)
- [ ] Concurrent session limits
- [ ] Session data encrypted

```python
response.set_cookie(
    key="session_id",
    value=session_id,
    httponly=True,
    secure=True,
    samesite="lax",
    max_age=1800  # 30 minutes
)
```

---

## 🔍 Security Monitoring

### Monitoring & Alerts
- [ ] Failed login attempts monitored
- [ ] Unusual API activity detected
- [ ] Rate limit violations logged
- [ ] SQL injection attempts alerted
- [ ] File upload anomalies detected

### Vulnerability Scanning
- [ ] Dependency scanning (npm audit, pip-audit)
- [ ] OWASP Top 10 tested
- [ ] Penetration testing scheduled
- [ ] Security patches applied promptly

---

## 📋 Deployment Checklist

Before going live:
- [ ] All secrets moved to vault
- [ ] Debug mode disabled
- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Error logging configured
- [ ] Database backups automated
- [ ] Incident response plan ready

---

## 🚨 Common Vulnerabilities

### OWASP Top 10 Checklist
1. **A01 Broken Access Control** - [ ] Fixed
2. **A02 Cryptographic Failures** - [ ] Fixed
3. **A03 Injection** - [ ] Fixed
4. **A04 Insecure Design** - [ ] Fixed
5. **A05 Security Misconfiguration** - [ ] Fixed
6. **A06 Vulnerable Components** - [ ] Fixed
7. **A07 ID & Auth Failures** - [ ] Fixed
8. **A08 Software & Data Integrity** - [ ] Fixed
9. **A09 Security Logging Failures** - [ ] Fixed
10. **A10 Server-Side Request Forgery** - [ ] Fixed

---

## 🛠️ Security Tools

### Recommended Tools
- **Dependency Scanning:** Snyk, Dependabot
- **SAST:** SonarQube, Semgrep
- **DAST:** OWASP ZAP, Burp Suite
- **Secrets Scanning:** GitGuardian, TruffleHog
- **Container Scanning:** Trivy, Clair

---

**Last Updated:** 2025-01-11  
**Compliance:** OWASP Top 10, GDPR considerations
