# n8n Production Deployment Guide

Enterprise-grade deployment strategies for scalable n8n workflows.

## Architecture Options

### Single Instance (Development/Small Scale)

```
┌─────────────────────────────────┐
│   n8n Single Instance           │
│   ├─ Webhooks                   │
│   ├─ Triggers                   │
│   ├─ Workflow Execution         │
│   └─ UI                         │
├─────────────────────────────────┤
│   SQLite/PostgreSQL             │
└─────────────────────────────────┘

Suitable for:
- Development
- Testing
- < 10k executions/month
- Small teams (1-5 users)
```

### Queue Mode (Production/High Scale)

```
┌──────────────────┐      ┌──────────────────┐
│  Load Balancer   │─────→│  Main Instance   │  Webhooks + Triggers
└──────────────────┘      │  (Queue Producer)│
                          └─────────┬────────┘
                                    │
                          ┌─────────▼────────┐
                          │   Redis Queue    │
                          └─────────┬────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
        ┌───────▼──────┐   ┌───────▼──────┐   ┌───────▼──────┐
        │  Worker 1    │   │  Worker 2    │   │  Worker 3    │
        │ Concurrency:10│   │ Concurrency:10│   │ Concurrency:10│
        └──────────────┘   └──────────────┘   └──────────────┘
                                    │
                          ┌─────────▼────────┐
                          │   PostgreSQL     │  Shared State
                          └──────────────────┘

Suitable for:
- Production
- > 10k executions/month
- High availability required
- Multiple teams
```

---

## Environment Configuration

### Essential Variables

```bash
# Core Settings (REQUIRED)
N8N_ENCRYPTION_KEY=<32-byte-random>  # openssl rand -base64 32
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
N8N_EDITOR_BASE_URL=https://n8n.yourdomain.com

# Execution Mode
EXECUTIONS_MODE=queue  # "regular" for single instance, "queue" for production

# Database (PostgreSQL REQUIRED for queue mode)
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=postgres
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n
DB_POSTGRESDB_PASSWORD=<strong-password>
DB_POSTGRESDB_POOL_SIZE=10  # Increase from default 2

# Queue Mode (Redis REQUIRED)
QUEUE_BULL_REDIS_HOST=redis
QUEUE_BULL_REDIS_PORT=6379
QUEUE_BULL_REDIS_DB=0
QUEUE_BULL_REDIS_USERNAME=default  # Optional
QUEUE_BULL_REDIS_PASSWORD=<redis-password>  # Optional

# Monitoring & Health Checks
QUEUE_HEALTH_CHECK_ACTIVE=true
N8N_PUSH_BACKEND=websocket  # Default since v1.0

# Security
N8N_SKIP_AUTH_ON_OAUTH_CALLBACK=false
N8N_RESTRICT_FILE_ACCESS_TO=/data/files
N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
N8N_RUNNERS_ENABLED=true  # Task runner isolation (v2.0+)

# Optimization
N8N_DIAGNOSTICS_ENABLED=false  # Disable telemetry
N8N_GRACEFUL_SHUTDOWN_TIMEOUT=30  # Seconds
```

### File-Based Secrets (RECOMMENDED)

```bash
# Environment with _FILE suffix
N8N_ENCRYPTION_KEY_FILE=/run/secrets/n8n_encryption_key
DB_POSTGRESDB_PASSWORD_FILE=/run/secrets/db_password
QUEUE_BULL_REDIS_PASSWORD_FILE=/run/secrets/redis_password

# Mount secrets from external storage
# Docker Swarm: /run/secrets/
# Kubernetes: /var/run/secrets/
```

---

## Docker Deployment

### Docker Compose (Production)

**File: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: n8n
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n"]
      interval: 5s
      timeout: 5s
      retries: 10
    restart: unless-stopped

  # Redis Queue
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass "$(cat /run/secrets/redis_password)"
    secrets:
      - redis_password
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  # Main Instance (Webhooks + Triggers)
  n8n-main:
    image: n8nio/n8n:latest
    environment:
      - N8N_ENCRYPTION_KEY_FILE=/run/secrets/n8n_encryption_key
      - N8N_HOST=0.0.0.0
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - N8N_EDITOR_BASE_URL=https://n8n.yourdomain.com
      - EXECUTIONS_MODE=queue
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD_FILE=/run/secrets/db_password
      - DB_POSTGRESDB_POOL_SIZE=10
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
      - QUEUE_BULL_REDIS_DB=0
      - QUEUE_BULL_REDIS_PASSWORD_FILE=/run/secrets/redis_password
      - QUEUE_HEALTH_CHECK_ACTIVE=true
      - N8N_DIAGNOSTICS_ENABLED=false
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    secrets:
      - n8n_encryption_key
      - db_password
      - redis_password
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  # Worker Instances (Scale horizontally)
  n8n-worker-1:
    image: n8nio/n8n:latest
    command: worker --concurrency=10
    environment:
      - N8N_ENCRYPTION_KEY_FILE=/run/secrets/n8n_encryption_key
      - EXECUTIONS_MODE=queue
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD_FILE=/run/secrets/db_password
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
      - QUEUE_BULL_REDIS_DB=0
      - QUEUE_BULL_REDIS_PASSWORD_FILE=/run/secrets/redis_password
      - QUEUE_HEALTH_CHECK_ACTIVE=true
    volumes:
      - n8n_data:/home/node/.n8n
    secrets:
      - n8n_encryption_key
      - db_password
      - redis_password
    depends_on:
      - n8n-main
    restart: unless-stopped

  n8n-worker-2:
    image: n8nio/n8n:latest
    command: worker --concurrency=10
    environment:
      # Same as worker-1
    volumes:
      - n8n_data:/home/node/.n8n
    secrets:
      - n8n_encryption_key
      - db_password
      - redis_password
    depends_on:
      - n8n-main
    restart: unless-stopped

  n8n-worker-3:
    image: n8nio/n8n:latest
    command: worker --concurrency=10
    environment:
      # Same as worker-1
    volumes:
      - n8n_data:/home/node/.n8n
    secrets:
      - n8n_encryption_key
      - db_password
      - redis_password
    depends_on:
      - n8n-main
    restart: unless-stopped

volumes:
  n8n_data:
  postgres_data:

secrets:
  n8n_encryption_key:
    file: ./secrets/n8n_encryption_key.txt
  db_password:
    file: ./secrets/db_password.txt
  redis_password:
    file: ./secrets/redis_password.txt
```

**Generate Secrets:**
```bash
mkdir -p secrets
openssl rand -base64 32 > secrets/n8n_encryption_key.txt
openssl rand -base64 24 > secrets/db_password.txt
openssl rand -base64 24 > secrets/redis_password.txt
chmod 600 secrets/*
```

**Start Services:**
```bash
docker-compose up -d

# Scale workers
docker-compose up -d --scale n8n-worker-1=5
```

### Docker Resource Recommendations

**Based on n8n Cloud Tiers:**

```yaml
# Starter (Small workloads)
services:
  n8n-main:
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.25'
        reservations:
          memory: 128M
          cpus: '0.1'

# Pro (Medium workloads)
services:
  n8n-main:
    deploy:
      resources:
        limits:
          memory: 500M
          cpus: '0.5'
        reservations:
          memory: 250M
          cpus: '0.25'

# Enterprise (Large workloads)
services:
  n8n-main:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2'
        reservations:
          memory: 1G
          cpus: '1'
```

---

## Kubernetes Deployment

### Kubernetes Manifests

**Namespace:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: n8n-production
```

**Secrets:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: n8n-secrets
  namespace: n8n-production
type: Opaque
data:
  encryption-key: <base64-encoded-key>
  db-password: <base64-encoded-password>
  redis-password: <base64-encoded-password>
```

**PostgreSQL StatefulSet:**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: n8n-production
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: n8n
        - name: POSTGRES_USER
          value: n8n
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: n8n-secrets
              key: db-password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1"
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 20Gi
```

**n8n Main Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n-main
  namespace: n8n-production
spec:
  replicas: 1
  selector:
    matchLabels:
      app: n8n-main
  template:
    metadata:
      labels:
        app: n8n-main
    spec:
      containers:
      - name: n8n
        image: n8nio/n8n:latest
        ports:
        - containerPort: 5678
        env:
        - name: N8N_ENCRYPTION_KEY
          valueFrom:
            secretKeyRef:
              name: n8n-secrets
              key: encryption-key
        - name: EXECUTIONS_MODE
          value: "queue"
        - name: DB_TYPE
          value: "postgresdb"
        - name: DB_POSTGRESDB_HOST
          value: "postgres"
        - name: DB_POSTGRESDB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: n8n-secrets
              key: db-password
        # ... (other env vars)
        resources:
          requests:
            memory: "256Mi"
            cpu: "500m"
          limits:
            memory: "512Mi"
            cpu: "1"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 5678
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /healthz
            port: 5678
          initialDelaySeconds: 30
          periodSeconds: 10
```

**n8n Worker Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n-worker
  namespace: n8n-production
spec:
  replicas: 3  # Scale horizontally
  selector:
    matchLabels:
      app: n8n-worker
  template:
    metadata:
      labels:
        app: n8n-worker
    spec:
      containers:
      - name: n8n-worker
        image: n8nio/n8n:latest
        command: ["n8n", "worker", "--concurrency=10"]
        env:
        # Same as main, but no port exposure
        resources:
          requests:
            memory: "256Mi"
            cpu: "500m"
          limits:
            memory: "512Mi"
            cpu: "1"
```

**HorizontalPodAutoscaler (Workers):**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: n8n-worker-hpa
  namespace: n8n-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: n8n-worker
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## Execution Data Management

### Pruning Configuration

```bash
# Enable automatic pruning
EXECUTIONS_DATA_PRUNE=true

# Max age (hours)
EXECUTIONS_DATA_PRUNE_MAX_AGE=336  # 14 days

# Max count
EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000

# Prune frequency (cron)
EXECUTIONS_DATA_PRUNE_TIMEOUT=3600  # 1 hour
```

### Execution Settings (Per Workflow)

**Workflow Settings:**
```javascript
{
  settings: {
    executionTimeout: 3600,  // 1 hour max
    saveDataErrorExecution: "all",      // Save on error
    saveDataSuccessExecution: "none",   // Don't save on success (saves storage)
    saveExecutionProgress: false,        // Don't save intermediate (saves latency)
    saveManualExecutions: true,         // Save manual test runs
    timezone: "America/New_York",
    executionOrder: "v1"                // Use latest execution order
  }
}
```

**Best Practices:**
- **High-volume workflows:** `saveDataSuccessExecution: "none"`
- **Critical workflows:** `saveDataErrorExecution: "all"`
- **Long-running workflows:** Set appropriate `executionTimeout`

---

## Monitoring & Alerts

### Health Check Endpoints

**Main Instance:**
```bash
# Overall health
GET /healthz
Response: { "status": "ok" }

# Readiness (DB + Redis check)
GET /healthz/readiness
Response: { 
  "status": "ok",
  "database": "connected",
  "redis": "connected"
}
```

**Worker Instance:**
```bash
# Worker up status
GET /healthz
Response: { "status": "ok", "worker": true }

# Worker readiness
GET /healthz/readiness
Response: { "status": "ok", "worker": true, "queueConnected": true }
```

### Error Workflows

**Create Error Handler:**
```javascript
// Error Trigger Node
{
  type: "n8n-nodes-base.errorTrigger",
  name: "On Error"
}

// Extract Error Data
{
  type: "n8n-nodes-base.code",
  code: `
    const error = $input.first().json.error;
    const execution = $input.first().json.execution;
    
    return [{
      json: {
        workflowName: execution.workflow.name,
        workflowId: execution.workflow.id,
        executionId: execution.id,
        errorMessage: error.message,
        errorStack: error.stack,
        lastNode: execution.lastNodeExecuted,
        timestamp: new Date().toISOString()
      }
    }];
  `
}

// Alert Team
{
  type: "n8n-nodes-base.slack",
  resource: "message",
  operation: "post",
  channel: "#alerts",
  text: `🚨 Workflow Error
  
  *Workflow:* {{ $json.workflowName }}
  *Execution:* {{ $json.executionId }}
  *Error:* {{ $json.errorMessage }}
  *Node:* {{ $json.lastNode }}
  *Time:* {{ $json.timestamp }}
  
  <https://n8n.example.com/execution/{{ $json.executionId }}|View Execution>`
}

// Log to Database
{
  type: "n8n-nodes-base.postgres",
  operation: "insert",
  table: "error_logs",
  columns: "workflow_id,execution_id,error_message,created_at"
}
```

### Prometheus Metrics (Coming Soon)

n8n v2.x will include Prometheus metrics endpoint for:
- Execution counts
- Execution duration
- Queue depths
- Worker utilization

---

## Cost Optimization

### Execution-Based Pricing

**n8n Cloud Pricing:**
```
Starter:  $20/month  → 2,500 executions
Pro:      $50/month  → 25,000 executions
Enterprise: Custom   → Unlimited

Self-Hosted: FREE (infrastructure costs only)
```

### Self-Hosted Cost Breakdown

**Small Deployment (10k executions/month):**
```
VPS (2 CPU, 4GB RAM): $20/month (Hetzner)
PostgreSQL: Included
Redis: Included
Total: $20/month

vs. n8n Cloud Starter: $20/month
→ Cost parity, but more control
```

**Medium Deployment (100k executions/month):**
```
VPS (4 CPU, 8GB RAM): $40/month
PostgreSQL RDS: $25/month
Redis: $10/month
Total: $75/month

vs. n8n Cloud Pro: $200/month (4x Pro plans)
→ Save $125/month (62% savings)
```

**Large Deployment (1M executions/month):**
```
Kubernetes Cluster: $200/month
Managed PostgreSQL: $100/month
Managed Redis: $50/month
Total: $350/month

vs. Competitors (Zapier/Make): $5,000+/month
→ Save $4,650/month (93% savings)
```

### External Service Costs

**Typical AI Workflow (10 posts/day):**
```
OpenAI GPT-4o-mini: $6/month (300 posts × $0.02)
Leonardo AI: $14/month (300 images)
MongoDB Atlas: Free (512MB)
Email (SendGrid): Free (100/day)

Total: $20/month for complete automation
```

---

## Security Checklist

### Pre-Production

- [ ] `N8N_ENCRYPTION_KEY` set (never change after first use)
- [ ] Secrets stored externally (not in env vars)
- [ ] File permissions enforced (`N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`)
- [ ] File access restricted (`N8N_RESTRICT_FILE_ACCESS_TO=/data`)
- [ ] OAuth callback authentication enabled
- [ ] Task runner isolation enabled (v2.0+)

### Database Security

- [ ] PostgreSQL uses strong password
- [ ] Connection pooling configured (avoid exhaustion)
- [ ] SSL/TLS enabled for remote connections
- [ ] Regular backups automated
- [ ] Backup encryption enabled

### Network Security

- [ ] n8n behind reverse proxy (Nginx/Traefik)
- [ ] HTTPS enforced (Let's Encrypt)
- [ ] Webhook endpoints authenticated
- [ ] API access restricted (IP whitelist)
- [ ] Rate limiting configured

### Access Control

- [ ] Strong admin password
- [ ] RBAC configured (Enterprise)
- [ ] Audit logs enabled (Enterprise)
- [ ] Session timeout configured
- [ ] 2FA enabled (Enterprise)

---

## Deployment Checklist

### Infrastructure

- [ ] PostgreSQL deployed & tested
- [ ] Redis deployed & tested
- [ ] Secrets generated & stored securely
- [ ] Environment variables configured
- [ ] Storage volumes provisioned
- [ ] Backups automated

### n8n Configuration

- [ ] Main instance deployed
- [ ] Worker instances deployed (3+ recommended)
- [ ] Health checks passing
- [ ] Webhooks accessible
- [ ] SSL/TLS configured
- [ ] Error workflows configured

### Testing

- [ ] Manual trigger workflows work
- [ ] Schedule triggers fire correctly
- [ ] Webhooks respond
- [ ] Queue processing works
- [ ] Error handling triggers
- [ ] Execution pruning works

### Monitoring

- [ ] Health check monitoring
- [ ] Error alerts configured
- [ ] Execution logs accessible
- [ ] Performance metrics tracked
- [ ] Cost monitoring setup

---

## Quick Reference

**Start Docker Compose:**
```bash
docker-compose up -d
```

**View Logs:**
```bash
docker-compose logs -f n8n-main
docker-compose logs -f n8n-worker-1
```

**Scale Workers:**
```bash
docker-compose up -d --scale n8n-worker=5
```

**Health Check:**
```bash
curl https://n8n.example.com/healthz
```

**Database Backup:**
```bash
docker exec postgres pg_dump -U n8n n8n > backup.sql
```

---

**Resources:**
- **n8n Deployment Docs**: https://docs.n8n.io/hosting/
- **Docker Hub**: https://hub.docker.com/r/n8nio/n8n
- **Community**: https://community.n8n.io/c/hosting-configuration/
