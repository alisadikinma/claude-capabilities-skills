# Security Architecture - Enterprise Best Practices

## Zero Trust Security Model

**Principle:** Never trust, always verify

**Key Tenets:**
1. Verify explicitly (authenticate + authorize every request)
2. Least privilege access (minimum necessary permissions)
3. Assume breach (segment network, monitor everything)

---

## Authentication & Authorization

### OAuth 2.0 + OpenID Connect

**Authorization Code Flow (Web Apps):**
```
1. User → App: Click "Login"
2. App → Auth Server: Redirect with client_id, redirect_uri, scope
3. User → Auth Server: Enter credentials
4. Auth Server → App: Authorization code
5. App → Auth Server: Exchange code for access_token (+ id_token)
6. App → API: Request with Bearer token
```

**JWT Token Structure:**
```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user123",
    "iss": "https://auth.example.com",
    "aud": "https://api.example.com",
    "exp": 1735689600,
    "iat": 1735686000,
    "scope": "read write"
  },
  "signature": "..."
}
```

**Token Validation:**
```javascript
// 1. Verify signature (RS256 with public key)
// 2. Check expiration (exp > now)
// 3. Validate issuer (iss matches expected)
// 4. Validate audience (aud matches API)
// 5. Check scope (user has required permissions)
```

### Role-Based Access Control (RBAC)

```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE  -- admin, editor, viewer
);

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    resource VARCHAR(100),  -- users, posts, orders
    action VARCHAR(50)      -- create, read, update, delete
);

CREATE TABLE role_permissions (
    role_id INT REFERENCES roles(id),
    permission_id INT REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
    user_id INT REFERENCES users(id),
    role_id INT REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
```

**Authorization Check:**
```python
def has_permission(user_id, resource, action):
    query = """
        SELECT COUNT(*) FROM user_roles ur
        JOIN role_permissions rp ON ur.role_id = rp.role_id
        JOIN permissions p ON rp.permission_id = p.id
        WHERE ur.user_id = %s
          AND p.resource = %s
          AND p.action = %s
    """
    return execute(query, user_id, resource, action) > 0
```

---

## Encryption

### Encryption at Rest

**Database Encryption (PostgreSQL):**
```bash
# Enable TDE (Transparent Data Encryption)
initdb -D /var/lib/postgresql/data --data-checksums
pg_ctl -D /var/lib/postgresql/data -o "--ssl=on" start
```

**Application-Level Encryption (Sensitive Fields):**
```python
from cryptography.fernet import Fernet

# Generate key (store in AWS KMS / Vault)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt before storing
encrypted_ssn = cipher.encrypt(b"123-45-6789")
db.execute("INSERT INTO users (ssn_encrypted) VALUES (%s)", encrypted_ssn)

# Decrypt when needed
ssn = cipher.decrypt(encrypted_ssn).decode()
```

### Encryption in Transit

**TLS 1.3 Configuration (Nginx):**
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.3;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384';
    ssl_prefer_server_ciphers on;
    
    # HSTS (force HTTPS)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

---

## Secret Management

### AWS Secrets Manager

```python
import boto3

secrets_client = boto3.client('secretsmanager')

# Store secret
secrets_client.create_secret(
    Name='db-password',
    SecretString='SuperSecurePassword123!'
)

# Retrieve secret
response = secrets_client.get_secret_value(SecretId='db-password')
db_password = response['SecretString']
```

### HashiCorp Vault

```bash
# Store secret
vault kv put secret/database username=admin password=pass123

# Retrieve secret
vault kv get -field=password secret/database
```

**Never:**
- Hard-code secrets in code
- Commit secrets to Git
- Store secrets in environment variables (logs)

---

## API Security

### Rate Limiting

**Token Bucket Algorithm:**
```python
from redis import Redis
import time

redis_client = Redis()

def check_rate_limit(user_id, max_requests=100, window_seconds=60):
    key = f"rate_limit:{user_id}"
    current = redis_client.get(key)
    
    if current is None:
        redis_client.setex(key, window_seconds, 1)
        return True
    
    if int(current) < max_requests:
        redis_client.incr(key)
        return True
    
    return False  # Rate limit exceeded
```

**Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
X-RateLimit-Reset: 1735686000
```

### Input Validation

**SQL Injection Prevention:**
```python
# ❌ BAD: String concatenation
query = f"SELECT * FROM users WHERE email = '{email}'"  # Vulnerable

# ✅ GOOD: Parameterized queries
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))
```

**XSS Prevention:**
```javascript
// ❌ BAD: Directly inserting user input
element.innerHTML = userInput;

// ✅ GOOD: Use textContent or sanitize
element.textContent = userInput;
// Or use DOMPurify library
element.innerHTML = DOMPurify.sanitize(userInput);
```

---

## Web Application Firewall (WAF)

**AWS WAF Rules:**
```json
{
  "Name": "BlockSQLInjection",
  "Priority": 1,
  "Statement": {
    "ManagedRuleGroupStatement": {
      "VendorName": "AWS",
      "Name": "AWSManagedRulesSQLiRuleSet"
    }
  },
  "Action": {
    "Block": {}
  }
}
```

---

## Security Headers

**Essential Headers:**
```nginx
# Prevent clickjacking
add_header X-Frame-Options "DENY";

# XSS Protection
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";

# Content Security Policy
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'";

# HSTS
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";

# Referrer Policy
add_header Referrer-Policy "strict-origin-when-cross-origin";
```

---

## Compliance (GDPR, SOC 2)

**GDPR Requirements:**
- Right to access (user can request their data)
- Right to erasure ("right to be forgotten")
- Data portability (export in machine-readable format)
- Breach notification (72 hours)

**Implementation:**
```python
# Right to access
@app.route('/api/users/<user_id>/data-export')
def export_user_data(user_id):
    user_data = get_all_user_data(user_id)
    return jsonify(user_data), 200

# Right to erasure
@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    anonymize_user_data(user_id)  # Or hard delete
    return '', 204
```

---

## Security Monitoring

**SIEM (Security Information & Event Management):**
- Collect logs from all services
- Correlate events (detect attack patterns)
- Alert on suspicious activity

**AWS CloudWatch + GuardDuty:**
```python
import boto3

logs_client = boto3.client('logs')

# Log security event
logs_client.put_log_events(
    logGroupName='/security/audit',
    logStreamName='api-access',
    logEvents=[
        {
            'timestamp': int(time.time() * 1000),
            'message': json.dumps({
                'event': 'unauthorized_access_attempt',
                'user_id': user_id,
                'ip': request.remote_addr,
                'endpoint': request.path
            })
        }
    ]
)
```

---

## Penetration Testing

**OWASP Top 10 (2021):**
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Authentication Failures
8. Data Integrity Failures
9. Logging & Monitoring Failures
10. Server-Side Request Forgery (SSRF)

**Testing Checklist:**
- [ ] SQL injection (automated: sqlmap)
- [ ] XSS (automated: XSStrike)
- [ ] CSRF protection
- [ ] Authentication bypass
- [ ] Authorization flaws
- [ ] Sensitive data exposure
- [ ] API security (IDOR, rate limits)

---

## Best Practices Summary

1. **Defense in Depth** - Multiple layers (WAF, app, DB)
2. **Least Privilege** - Minimal permissions needed
3. **Encrypt Everything** - At rest, in transit
4. **Validate Input** - Never trust user input
5. **Use Secrets Manager** - Never hardcode secrets
6. **Monitor & Alert** - Log security events
7. **Regular Updates** - Patch vulnerabilities promptly
8. **Penetration Test** - Quarterly professional audits
9. **Security Training** - Educate developers
10. **Incident Response Plan** - Ready for breaches
