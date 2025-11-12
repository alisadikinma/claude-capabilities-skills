# Comprehensive Security Checklist

## Security Layers

```
┌─────────────────────────────────────────┐
│  1. Physical Security                   │
│     (Data centers, devices)             │
├─────────────────────────────────────────┤
│  2. Network Security                    │
│     (Firewalls, VPN, DDoS protection)   │
├─────────────────────────────────────────┤
│  3. Application Security                │
│     (Code, APIs, authentication)        │
├─────────────────────────────────────────┤
│  4. Data Security                       │
│     (Encryption, backup, access control)│
├─────────────────────────────────────────┤
│  5. Operational Security                │
│     (Monitoring, incident response)     │
└─────────────────────────────────────────┘
```

---

## 1. Authentication & Authorization

### Authentication

- [ ] **Password Security**
  - [ ] Minimum 8 characters (12+ recommended)
  - [ ] Require: uppercase, lowercase, number, special char
  - [ ] Use bcrypt/Argon2 for hashing (not MD5/SHA1)
  - [ ] Implement password strength meter
  - [ ] Check against breached password databases (Have I Been Pwned)
  - [ ] Rate limit login attempts (5 attempts / 15 min)
  - [ ] Account lockout after failed attempts
  - [ ] Notify users of suspicious login attempts

- [ ] **Multi-Factor Authentication (MFA)**
  - [ ] Support TOTP (Google Authenticator, Authy)
  - [ ] Support SMS (with warnings about SIM swapping)
  - [ ] Support backup codes
  - [ ] Require MFA for admin accounts
  - [ ] Consider mandatory MFA for sensitive operations

- [ ] **Session Management**
  - [ ] Generate cryptographically random session IDs
  - [ ] Set appropriate session timeout (15-30 min)
  - [ ] Implement absolute session timeout (24 hours)
  - [ ] Invalidate session on logout
  - [ ] Regenerate session ID after login
  - [ ] Store sessions securely (Redis with encryption)
  - [ ] Implement "Remember Me" securely (separate token)

- [ ] **JWT Token Security**
  - [ ] Use strong signing algorithm (HS256/RS256, not none)
  - [ ] Short expiry for access tokens (15-60 min)
  - [ ] Long expiry for refresh tokens (7-30 days)
  - [ ] Store tokens securely (httpOnly, secure cookies)
  - [ ] Implement token rotation
  - [ ] Validate token on every request
  - [ ] Implement token revocation mechanism
  - [ ] Check token expiry, issuer, audience

### Authorization

- [ ] **Access Control**
  - [ ] Implement principle of least privilege
  - [ ] Use Role-Based Access Control (RBAC)
  - [ ] Consider Attribute-Based Access Control (ABAC) for complex needs
  - [ ] Enforce authorization on server-side (never trust client)
  - [ ] Check permissions for every operation
  - [ ] Implement resource-level permissions (not just role-level)
  - [ ] Log all authorization failures

- [ ] **API Security**
  - [ ] Authenticate all API requests
  - [ ] Use API keys for service-to-service
  - [ ] Implement rate limiting per user/IP
  - [ ] Validate all input parameters
  - [ ] Return generic error messages (don't leak info)
  - [ ] Use HTTPS for all API endpoints
  - [ ] Implement request signing for sensitive operations

---

## 2. Input Validation & Sanitization

### General Input Validation

- [ ] **Validate All Inputs**
  - [ ] Whitelist allowed characters (not blacklist)
  - [ ] Validate data type, length, format, range
  - [ ] Reject unexpected input early
  - [ ] Use parameterized queries (prevent SQL injection)
  - [ ] Validate on both client and server
  - [ ] Sanitize before storing and displaying

- [ ] **SQL Injection Prevention**
  - [ ] Use ORM with parameterized queries
  - [ ] Never concatenate user input into SQL
  - [ ] Use prepared statements
  - [ ] Limit database user privileges
  - [ ] Escape special characters if raw SQL needed
  
  ```python
  # ❌ Vulnerable
  query = f"SELECT * FROM users WHERE email = '{email}'"
  
  # ✅ Safe (Parameterized)
  query = "SELECT * FROM users WHERE email = %s"
  cursor.execute(query, (email,))
  
  # ✅ Safe (ORM)
  User.objects.filter(email=email)
  ```

- [ ] **XSS Prevention**
  - [ ] Escape HTML output
  - [ ] Use Content Security Policy (CSP)
  - [ ] Sanitize user-generated HTML (DOMPurify)
  - [ ] Use templating engines with auto-escaping
  - [ ] Set X-XSS-Protection header
  
  ```python
  # ❌ Vulnerable
  html = f"<div>{user_input}</div>"
  
  # ✅ Safe (Escaped)
  from html import escape
  html = f"<div>{escape(user_input)}</div>"
  ```

- [ ] **Command Injection Prevention**
  - [ ] Avoid system calls with user input
  - [ ] Use libraries instead of shell commands
  - [ ] If shell needed, validate and escape input
  - [ ] Run with least privileges

- [ ] **Path Traversal Prevention**
  - [ ] Validate file paths
  - [ ] Use allowlist of allowed files
  - [ ] Reject paths with "../"
  - [ ] Use secure file operations
  
  ```python
  # ❌ Vulnerable
  file_path = f"/uploads/{user_filename}"
  
  # ✅ Safe
  import os
  safe_name = os.path.basename(user_filename)
  file_path = os.path.join("/uploads", safe_name)
  ```

---

## 3. Data Security

### Encryption

- [ ] **Data in Transit**
  - [ ] Use TLS 1.3 (minimum TLS 1.2)
  - [ ] HTTPS for all pages (not just login)
  - [ ] HTTP Strict Transport Security (HSTS)
  - [ ] Certificate from trusted CA
  - [ ] Proper certificate validation
  - [ ] Strong cipher suites only

- [ ] **Data at Rest**
  - [ ] Encrypt sensitive data in database
  - [ ] Encrypt backups
  - [ ] Encrypt disk volumes
  - [ ] Use strong encryption (AES-256)
  - [ ] Secure key management (KMS, Vault)
  - [ ] Rotate encryption keys periodically

- [ ] **Sensitive Data Handling**
  - [ ] Never log passwords, tokens, credit cards
  - [ ] Mask PII in logs (email → e***@example.com)
  - [ ] Minimize data collection (only what's needed)
  - [ ] Secure deletion (overwrite, not just delete flag)
  - [ ] Encrypt sensitive fields separately

### Data Privacy

- [ ] **GDPR Compliance** (if EU users)
  - [ ] Obtain explicit consent
  - [ ] Allow data access requests
  - [ ] Allow data deletion requests
  - [ ] Data portability (export user data)
  - [ ] Privacy policy clearly stated
  - [ ] Cookie consent banner
  - [ ] Data breach notification (72 hours)
  - [ ] Appoint Data Protection Officer (if required)

- [ ] **PII Protection**
  - [ ] Minimize PII collection
  - [ ] Encrypt PII at rest
  - [ ] Limit access to PII
  - [ ] Audit access to PII
  - [ ] Anonymize data for analytics

---

## 4. Network Security

- [ ] **Firewall Configuration**
  - [ ] Allow only necessary ports
  - [ ] Block direct database access from internet
  - [ ] Use VPN for admin access
  - [ ] Implement Web Application Firewall (WAF)
  - [ ] Configure security groups properly

- [ ] **DDoS Protection**
  - [ ] Use CDN (Cloudflare, AWS Shield)
  - [ ] Rate limiting at multiple layers
  - [ ] Monitor traffic patterns
  - [ ] Have DDoS response plan

- [ ] **Network Segmentation**
  - [ ] Separate production from development
  - [ ] Isolate sensitive services
  - [ ] Use private subnets for databases
  - [ ] Implement zero-trust architecture

---

## 5. Application Security

### Secure Headers

- [ ] **HTTP Security Headers**
  ```
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=()
  ```

- [ ] **CORS Configuration**
  - [ ] Whitelist specific origins (not '*')
  - [ ] Validate Origin header
  - [ ] Limit allowed methods
  - [ ] Credentials only for trusted origins

### File Upload Security

- [ ] **Upload Validation**
  - [ ] Validate file type (not just extension)
  - [ ] Check file content (magic bytes)
  - [ ] Limit file size (prevent DoS)
  - [ ] Scan for malware
  - [ ] Store outside web root
  - [ ] Use random filenames
  - [ ] Serve with proper Content-Type
  - [ ] Consider signed URLs (S3)

### Dependency Security

- [ ] **Third-Party Libraries**
  - [ ] Keep dependencies updated
  - [ ] Scan for known vulnerabilities (Snyk, OWASP)
  - [ ] Review security advisories
  - [ ] Pin dependency versions
  - [ ] Use Software Bill of Materials (SBOM)
  - [ ] Minimize dependencies
  - [ ] Audit before adding new dependencies

### Code Security

- [ ] **Secure Coding Practices**
  - [ ] Code reviews (security focus)
  - [ ] Static analysis (SonarQube, ESLint)
  - [ ] Secrets scanning (GitGuardian, TruffleHog)
  - [ ] No hardcoded secrets
  - [ ] Use environment variables
  - [ ] Implement error handling (don't expose internals)
  - [ ] Log security events
  - [ ] Principle of least privilege in code

---

## 6. Infrastructure Security

### Cloud Security

- [ ] **AWS/GCP/Azure**
  - [ ] Enable MFA on root account
  - [ ] Use IAM roles (not long-lived credentials)
  - [ ] Principle of least privilege for IAM
  - [ ] Enable CloudTrail/Cloud Audit logging
  - [ ] Encrypt data at rest (S3, RDS, etc.)
  - [ ] Enable VPC flow logs
  - [ ] Use private subnets for databases
  - [ ] Enable GuardDuty / Security Center
  - [ ] Regular security audits

### Container Security

- [ ] **Docker Security**
  - [ ] Use official base images
  - [ ] Scan images for vulnerabilities
  - [ ] Don't run as root user
  - [ ] Minimize image layers
  - [ ] Use multi-stage builds
  - [ ] Sign images
  - [ ] Keep base images updated
  - [ ] Limit container capabilities

- [ ] **Kubernetes Security**
  - [ ] Enable RBAC
  - [ ] Use Network Policies
  - [ ] Pod Security Policies
  - [ ] Secrets management (Sealed Secrets, Vault)
  - [ ] Image scanning in CI/CD
  - [ ] Regular security audits (kube-bench)

### Server Security

- [ ] **Linux Server Hardening**
  - [ ] Keep system updated
  - [ ] Disable unnecessary services
  - [ ] Configure firewall (iptables, ufw)
  - [ ] SSH key-only authentication
  - [ ] Disable root login
  - [ ] Fail2ban for brute force protection
  - [ ] Regular security updates
  - [ ] Audit logs monitoring

---

## 7. Monitoring & Incident Response

### Monitoring

- [ ] **Security Monitoring**
  - [ ] Log all authentication attempts
  - [ ] Log authorization failures
  - [ ] Monitor for unusual patterns
  - [ ] Alert on suspicious activities
  - [ ] Centralized logging (ELK, Splunk)
  - [ ] Log retention policy (90+ days)
  - [ ] Protect logs from tampering

- [ ] **Metrics to Monitor**
  - [ ] Failed login attempts spike
  - [ ] Unusual API call patterns
  - [ ] High error rates
  - [ ] Slow response times (potential DDoS)
  - [ ] Unusual database queries
  - [ ] Large data exports

### Incident Response

- [ ] **Incident Response Plan**
  - [ ] Document response procedures
  - [ ] Assign response team roles
  - [ ] Define escalation path
  - [ ] Maintain incident playbooks
  - [ ] Regular drills and simulations
  - [ ] Post-incident review process
  - [ ] Communication plan

- [ ] **Breach Response Checklist**
  1. Contain the breach
  2. Assess the scope
  3. Preserve evidence
  4. Notify stakeholders
  5. Remediate vulnerabilities
  6. Notify users (if PII affected)
  7. Notify authorities (GDPR: 72 hours)
  8. Post-mortem and improvements

---

## 8. Compliance & Auditing

### Compliance Requirements

- [ ] **GDPR** (EU users)
  - [ ] Data processing agreement
  - [ ] Privacy by design
  - [ ] Consent management
  - [ ] Right to erasure
  - [ ] Data breach notification

- [ ] **HIPAA** (Healthcare data in US)
  - [ ] Business Associate Agreement
  - [ ] PHI encryption
  - [ ] Access controls
  - [ ] Audit logs
  - [ ] Incident response

- [ ] **PCI DSS** (Payment cards)
  - [ ] Use payment processor (Stripe, PayPal)
  - [ ] Don't store card data
  - [ ] If storing: Full PCI compliance
  - [ ] Regular security scans

- [ ] **SOC 2** (Enterprise customers)
  - [ ] Security controls documentation
  - [ ] Regular audits
  - [ ] Vendor management
  - [ ] Change management

### Security Auditing

- [ ] **Regular Audits**
  - [ ] Quarterly vulnerability scans
  - [ ] Annual penetration testing
  - [ ] Code security reviews
  - [ ] Dependency audits
  - [ ] Access reviews (remove unused accounts)
  - [ ] Log reviews

---

## 9. Development Security (DevSecOps)

### Secure SDLC

- [ ] **Development Phase**
  - [ ] Security requirements gathering
  - [ ] Threat modeling
  - [ ] Secure design review
  - [ ] Security training for developers

- [ ] **Implementation Phase**
  - [ ] Secure coding guidelines
  - [ ] Code reviews (security focus)
  - [ ] Static analysis (SAST)
  - [ ] Secrets scanning

- [ ] **Testing Phase**
  - [ ] Security testing
  - [ ] Dynamic analysis (DAST)
  - [ ] Dependency scanning (SCA)
  - [ ] Penetration testing

- [ ] **Deployment Phase**
  - [ ] Security scanning in CI/CD
  - [ ] Infrastructure as Code scanning
  - [ ] Container scanning
  - [ ] Configuration validation

### CI/CD Security

- [ ] **Pipeline Security**
  - [ ] Secrets management (not in code)
  - [ ] Signed commits
  - [ ] Branch protection
  - [ ] Security gates (block on vulnerabilities)
  - [ ] Audit trail of deployments
  - [ ] Separate prod credentials

---

## 10. Third-Party Security

### Vendor Management

- [ ] **Third-Party Services**
  - [ ] Security assessment before integration
  - [ ] Data Processing Agreement
  - [ ] SOC 2 / ISO 27001 certification
  - [ ] Regular vendor reviews
  - [ ] Data access minimization
  - [ ] Exit strategy

### API Integrations

- [ ] **External APIs**
  - [ ] Use API keys, not passwords
  - [ ] Store credentials securely
  - [ ] Implement retry with backoff
  - [ ] Validate responses
  - [ ] Handle failures gracefully
  - [ ] Monitor for suspicious usage

---

## Security Testing Checklist

### Manual Testing

- [ ] Try SQL injection on all inputs
- [ ] Try XSS on all text fields
- [ ] Test authentication bypass
- [ ] Test authorization (horizontal/vertical)
- [ ] Test session management
- [ ] Test file upload vulnerabilities
- [ ] Test password reset flow
- [ ] Test rate limiting

### Automated Testing

- [ ] OWASP ZAP / Burp Suite scan
- [ ] Dependency vulnerability scan
- [ ] Container image scan
- [ ] Infrastructure scan (Terraform, CloudFormation)
- [ ] Secrets scanning (git history)

---

## Security Metrics

### KPIs to Track

- Mean time to patch vulnerabilities
- Number of vulnerabilities by severity
- Failed authentication attempts
- Security incidents per month
- Time to detect incidents (MTTD)
- Time to respond to incidents (MTTR)
- Percentage of systems patched
- Security training completion rate

### Security Scorecard

```
Critical Vulnerabilities:     0   ✅
High Vulnerabilities:         2   ⚠️
Medium Vulnerabilities:       15  ⚠️
Low Vulnerabilities:          45  ℹ️

MFA Enabled (Admin):          100% ✅
MFA Enabled (Users):          35%  ⚠️
Systems Patched (Last 30d):   95%  ✅
Security Training:            100% ✅
```

---

**Review Frequency:**
- Critical systems: Weekly
- All systems: Monthly
- Full audit: Quarterly
- Penetration test: Annually

**Responsibility:**
Everyone is responsible for security, but designate:
- Security Champion per team
- Security Officer (overall responsibility)
- Incident Response Team
