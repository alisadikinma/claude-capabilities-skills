# Docker Reference Guide

Comprehensive guide for Docker containerization, optimization, and production best practices.

## Table of Contents
1. [Multi-Stage Builds](#multi-stage-builds)
2. [Image Optimization](#image-optimization)
3. [Security Best Practices](#security-best-practices)
4. [Docker Compose](#docker-compose)
5. [Registry Management](#registry-management)
6. [Networking](#networking)
7. [Storage & Volumes](#storage--volumes)
8. [Troubleshooting](#troubleshooting)

---

## Multi-Stage Builds

### Basic Pattern
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
USER node
CMD ["node", "dist/main.js"]
```

**Benefits:**
- Smaller final image (only runtime dependencies)
- Faster builds with layer caching
- No build tools in production image
- Better security (reduced attack surface)

### Python Application
```dockerfile
# Build stage with full Python
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY . .

# Production stage with slim Python
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app .
ENV PATH=/root/.local/bin:$PATH
USER nobody
CMD ["python", "app.py"]
```

### Go Application (Smallest Possible)
```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Production stage - scratch (0 MB base)
FROM scratch
COPY --from=builder /app/main /main
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 8080
CMD ["/main"]
```

**Result:** Final image ~5-10MB instead of 300MB+

### Java Application
```dockerfile
# Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

# Production stage
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## Image Optimization

### Size Reduction Techniques

#### 1. Use Alpine Base Images
```dockerfile
# Before: 1.2GB
FROM python:3.11

# After: 45MB
FROM python:3.11-alpine
```

**Trade-off:** Alpine uses musl libc instead of glibc. Some packages may have compatibility issues.

#### 2. Minimize Layers
```dockerfile
# Bad: 5 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get clean

# Good: 1 layer
RUN apt-get update && \
    apt-get install -y curl git vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

#### 3. Use .dockerignore
```
# .dockerignore
node_modules/
.git/
.env
*.md
tests/
coverage/
.DS_Store
*.log
```

**Impact:** Reduces build context size, faster builds, no sensitive files copied.

#### 4. Remove Unnecessary Files
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    # Build your app
    pip install -r requirements.txt && \
    # Clean up
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache
```

#### 5. Order Layers by Change Frequency
```dockerfile
# Dependencies change rarely - cache these layers
COPY package*.json ./
RUN npm ci

# Source code changes frequently - put at the end
COPY . .
RUN npm run build
```

### BuildKit Features

Enable BuildKit for faster builds:
```bash
export DOCKER_BUILDKIT=1
docker build .
```

#### Cache Mounts
```dockerfile
FROM python:3.11-alpine
WORKDIR /app

# Cache pip downloads
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

#### Secret Mounts (Don't Bake Secrets)
```dockerfile
# Mount secrets during build, don't copy into image
RUN --mount=type=secret,id=npm_token \
    echo "//registry.npmjs.org/:_authToken=$(cat /run/secrets/npm_token)" > .npmrc && \
    npm install && \
    rm .npmrc
```

Build with:
```bash
docker build --secret id=npm_token,src=$HOME/.npmrc .
```

---

## Security Best Practices

### 1. Run as Non-Root User
```dockerfile
FROM node:18-alpine

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app
COPY --chown=appuser:appgroup . .

# Switch to non-root
USER appuser

CMD ["node", "server.js"]
```

### 2. Scan Images for Vulnerabilities
```bash
# Using Docker Scout
docker scout cve myapp:latest

# Using Trivy
trivy image myapp:latest

# Using Snyk
snyk container test myapp:latest
```

**CI/CD Integration:**
```yaml
# .gitlab-ci.yml
security_scan:
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

### 3. Use Specific Image Versions
```dockerfile
# Bad: Version may change unexpectedly
FROM node:latest

# Good: Pin to specific version
FROM node:18.17.1-alpine3.18

# Better: Use digest for immutability
FROM node:18-alpine@sha256:abc123def456...
```

### 4. Minimize Attack Surface
```dockerfile
# Only install what you need
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Remove unnecessary setuid/setgid binaries
RUN find / -perm /6000 -type f -exec chmod a-s {} \; || true
```

### 5. Use Security Scanners in CI/CD
```bash
# Dockerfile linting
docker run --rm -i hadolint/hadolint < Dockerfile

# Runtime security
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy image myapp:latest
```

### 6. Read-Only Root Filesystem
```dockerfile
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:v1
        securityContext:
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir: {}
```

---

## Docker Compose

### Development Environment
```yaml
# docker-compose.yml
version: '3.9'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DB_HOST=postgres
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - backend

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - backend

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - backend

volumes:
  postgres_data:

networks:
  backend:
    driver: bridge
```

### Production-Like Staging
```yaml
version: '3.9'

services:
  app:
    image: myapp:${VERSION:-latest}
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Useful Commands
```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f app

# Scale service
docker-compose up -d --scale app=5

# Execute command in running container
docker-compose exec app sh

# Rebuild and restart
docker-compose up -d --build

# Stop and remove everything
docker-compose down -v
```

---

## Registry Management

### Docker Hub
```bash
# Login
docker login

# Tag image
docker tag myapp:latest username/myapp:v1.0

# Push
docker push username/myapp:v1.0

# Pull
docker pull username/myapp:v1.0
```

### Private Registry (Harbor, Nexus)
```bash
# Login to private registry
docker login registry.company.com

# Tag with registry URL
docker tag myapp:latest registry.company.com/myapp:v1.0

# Push
docker push registry.company.com/myapp:v1.0
```

### AWS ECR
```bash
# Get login password
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin \
    123456789012.dkr.ecr.us-east-1.amazonaws.com

# Tag
docker tag myapp:latest \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0

# Push
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0
```

### GCP Artifact Registry
```bash
# Configure authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Tag
docker tag myapp:latest \
    us-central1-docker.pkg.dev/project-id/repo-name/myapp:v1.0

# Push
docker push us-central1-docker.pkg.dev/project-id/repo-name/myapp:v1.0
```

### Azure Container Registry
```bash
# Login
az acr login --name myregistry

# Tag
docker tag myapp:latest myregistry.azurecr.io/myapp:v1.0

# Push
docker push myregistry.azurecr.io/myapp:v1.0
```

---

## Networking

### Bridge Network (Default)
```bash
# Create custom bridge network
docker network create --driver bridge mynetwork

# Connect container to network
docker run --network mynetwork --name app1 myapp:latest

# Containers can communicate by name
docker exec app1 ping app2
```

### Host Network
```dockerfile
# Use host's network stack (no isolation)
docker run --network host myapp:latest
```

**Use case:** Maximum performance, no port mapping overhead.

### Overlay Network (Swarm/Multi-Host)
```bash
# Create overlay network
docker network create --driver overlay --attachable myoverlay

# Spans multiple Docker hosts
docker service create --network myoverlay --name app myapp:latest
```

### Custom DNS
```yaml
# docker-compose.yml
services:
  app:
    dns:
      - 8.8.8.8
      - 8.8.4.4
    extra_hosts:
      - "api.internal:192.168.1.100"
```

---

## Storage & Volumes

### Volume Types

#### Named Volumes (Recommended for Persistence)
```bash
# Create volume
docker volume create mydata

# Use in container
docker run -v mydata:/app/data myapp:latest

# Inspect
docker volume inspect mydata

# Backup volume
docker run --rm -v mydata:/source -v $(pwd):/backup \
    alpine tar czf /backup/mydata-backup.tar.gz -C /source .
```

#### Bind Mounts (Host Directory)
```bash
# Mount host directory
docker run -v /host/path:/container/path myapp:latest

# Read-only mount
docker run -v /host/path:/container/path:ro myapp:latest
```

#### tmpfs Mounts (Memory-Based)
```bash
# Sensitive data that shouldn't persist
docker run --tmpfs /tmp:rw,size=100m myapp:latest
```

### Volume Drivers

#### Local Driver
```bash
docker volume create --driver local \
    --opt type=nfs \
    --opt o=addr=192.168.1.100,rw \
    --opt device=:/path/to/dir \
    nfs-volume
```

#### Cloud Volumes (AWS EBS, GCP PD)
```yaml
# Docker Swarm service with AWS EBS
services:
  app:
    image: myapp:latest
    volumes:
      - type: volume
        source: ebs-volume
        target: /data
        volume:
          driver: rexray/ebs

volumes:
  ebs-volume:
    driver: rexray/ebs
    driver_opts:
      size: 100
```

---

## Troubleshooting

### Container Debugging

#### View Logs
```bash
# Follow logs in real-time
docker logs -f container_name

# Last 100 lines
docker logs --tail 100 container_name

# Logs since specific time
docker logs --since 2024-01-01T00:00:00 container_name
```

#### Execute Commands in Running Container
```bash
# Interactive shell
docker exec -it container_name sh

# Run specific command
docker exec container_name cat /app/config.json

# As root user (for debugging only)
docker exec -u 0 -it container_name sh
```

#### Inspect Container
```bash
# Full container details (JSON)
docker inspect container_name

# Specific field
docker inspect -f '{{.NetworkSettings.IPAddress}}' container_name

# All environment variables
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' container_name
```

#### Copy Files From/To Container
```bash
# From container to host
docker cp container_name:/app/logs/error.log ./

# From host to container
docker cp ./config.json container_name:/app/config.json
```

### Build Issues

#### Cache Not Working
```bash
# Force rebuild without cache
docker build --no-cache -t myapp:latest .

# Specify cache-from for multi-stage builds
docker build --cache-from myapp:builder --cache-from myapp:latest -t myapp:new .
```

#### Build Context Too Large
```bash
# Check build context size
du -sh .

# Use .dockerignore
echo "node_modules/" >> .dockerignore
echo ".git/" >> .dockerignore
```

#### Multi-Platform Builds (ARM + x86)
```bash
# Enable buildx
docker buildx create --use

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 \
    -t myapp:latest --push .
```

### Performance Issues

#### High CPU/Memory Usage
```bash
# Monitor container stats
docker stats container_name

# Limit resources
docker run --cpus=0.5 --memory=512m myapp:latest
```

#### Slow Builds
1. Order Dockerfile layers by change frequency
2. Use BuildKit cache mounts
3. Use `.dockerignore` to reduce context
4. Parallelize multi-stage builds

#### Slow Container Startup
1. Use smaller base images (Alpine)
2. Reduce image layers
3. Optimize application initialization
4. Use healthchecks appropriately

### Network Issues

#### Container Can't Connect to Internet
```bash
# Check DNS resolution
docker exec container_name nslookup google.com

# Specify DNS servers
docker run --dns 8.8.8.8 --dns 8.8.4.4 myapp:latest
```

#### Containers Can't Communicate
```bash
# Verify both containers on same network
docker network inspect bridge

# Create custom network
docker network create mynetwork
docker network connect mynetwork container1
docker network connect mynetwork container2
```

### Storage Issues

#### Out of Disk Space
```bash
# Check disk usage
docker system df

# Remove unused data
docker system prune -a --volumes

# Remove specific items
docker image prune -a
docker volume prune
docker container prune
```

#### Volume Permission Issues
```dockerfile
# Match UID/GID with host user
RUN adduser -D -u 1000 appuser
USER appuser

# Or use root and chown volumes
RUN chown -R appuser:appuser /app/data
```

---

## Performance Optimization Checklist

- [ ] Use multi-stage builds
- [ ] Base image is Alpine or distroless
- [ ] .dockerignore file configured
- [ ] Layers ordered by change frequency
- [ ] BuildKit enabled for builds
- [ ] Cache mounts used for dependencies
- [ ] Image scanned for vulnerabilities
- [ ] Running as non-root user
- [ ] Resource limits set (CPU/memory)
- [ ] Healthchecks configured
- [ ] Logs sent to stdout/stderr
- [ ] Secrets not baked into image
- [ ] Image tagged with version (not `latest`)
- [ ] Image size <500MB for apps, <100MB for Go
- [ ] Build time <5 minutes

---

## Quick Reference

### Essential Commands
```bash
# Build
docker build -t myapp:v1 .

# Run
docker run -d -p 8080:80 --name myapp myapp:v1

# Stop
docker stop myapp

# Remove
docker rm myapp

# Logs
docker logs -f myapp

# Execute
docker exec -it myapp sh

# Inspect
docker inspect myapp

# Copy
docker cp myapp:/app/log.txt ./

# System cleanup
docker system prune -af --volumes
```

### Dockerfile Best Practices
1. Pin base image versions
2. Run as non-root user
3. Use multi-stage builds
4. Minimize layers (combine RUN commands)
5. Use .dockerignore
6. Order layers by change frequency
7. Don't install unnecessary packages
8. Scan for vulnerabilities
9. Set resource limits
10. Configure healthchecks

---

**Next Steps:**
- Read kubernetes.md for orchestration
- Read cicd.md for automated builds
- Read monitoring.md for observability
