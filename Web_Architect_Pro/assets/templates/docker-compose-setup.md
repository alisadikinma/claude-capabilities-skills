# Docker & Docker Compose Setup - Containerization

**For:** Full-stack applications, microservices  
**Coverage:** Dockerfile, docker-compose, multi-stage builds, optimization  
**Tools:** Docker 24+, Docker Compose V2

---

## 📦 Installation

```bash
# Install Docker Desktop (macOS/Windows)
# Or Docker Engine (Linux)

# Verify installation
docker --version
docker compose version

# Docker Compose V2 (new syntax)
docker compose up
# vs V1 (old syntax)
docker-compose up
```

---

## 📂 Project Structure

```
project/
├── docker/
│   ├── nginx/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   ├── backend/
│   │   └── Dockerfile
│   └── frontend/
│       └── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .dockerignore
└── Makefile                  # Convenience commands
```

---

## 🐳 Dockerfile Examples

### Node.js Backend (Multi-stage Build)

```dockerfile
# docker/backend/Dockerfile

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Stage 3: Runner (Production)
FROM node:20-alpine AS runner
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nodejs

# Copy built files from builder
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs package*.json ./

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:4000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

# Start application
CMD ["node", "dist/index.js"]
```

### Node.js Development Dockerfile

```dockerfile
# docker/backend/Dockerfile.dev

FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source
COPY . .

# Expose port
EXPOSE 4000

# Development with hot reload
CMD ["npm", "run", "dev"]
```

### Next.js Frontend

```dockerfile
# docker/frontend/Dockerfile

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build with environment variables
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy built files
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### Python FastAPI

```dockerfile
# docker/backend/Dockerfile

FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Nginx (Reverse Proxy)

```dockerfile
# docker/nginx/Dockerfile

FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Copy SSL certificates (if any)
# COPY certs/ /etc/nginx/certs/

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

---

## 🎯 Docker Compose

### docker-compose.yml (Development)

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: project-postgres
    restart: unless-stopped
    ports:
      - '5432:5432'
    environment:
      POSTGRES_DB: ${DB_NAME:-myapp}
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U postgres']
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: project-redis
    restart: unless-stopped
    ports:
      - '6379:6379'
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 10s
      timeout: 3s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: project-backend
    restart: unless-stopped
    ports:
      - '4000:4000'
    environment:
      NODE_ENV: development
      PORT: 4000
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/myapp
      REDIS_URL: redis://redis:6379
      JWT_SECRET: ${JWT_SECRET:-dev-secret}
    volumes:
      - ./backend:/app
      - /app/node_modules
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: npm run dev

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: project-frontend
    restart: unless-stopped
    ports:
      - '3000:3000'
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:4000
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    depends_on:
      - backend

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: project-nginx
    restart: unless-stopped
    ports:
      - '80:80'
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: project-network
```

### docker-compose.prod.yml (Production)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U ${DB_USER}']
      interval: 30s
      timeout: 10s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - backend
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 30s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    restart: always
    environment:
      NODE_ENV: production
      PORT: 4000
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
      JWT_SECRET: ${JWT_SECRET}
    networks:
      - backend
      - frontend
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL}
    restart: always
    networks:
      - frontend
    depends_on:
      - backend
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

  nginx:
    build:
      context: ./docker/nginx
    restart: always
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/conf.d:/etc/nginx/conf.d
      - certbot_certs:/etc/letsencrypt
      - certbot_www:/var/www/certbot
    networks:
      - frontend
    depends_on:
      - frontend
      - backend

  # SSL Certificate Manager
  certbot:
    image: certbot/certbot
    volumes:
      - certbot_certs:/etc/letsencrypt
      - certbot_www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

volumes:
  postgres_data:
  redis_data:
  certbot_certs:
  certbot_www:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

---

## 📝 Configuration Files

### .dockerignore

```
# Dependencies
node_modules
npm-debug.log
package-lock.json
yarn.lock

# Build outputs
dist
build
.next
out

# Environment
.env
.env.local
.env*.local

# IDE
.vscode
.idea
*.swp
*.swo

# Git
.git
.gitignore

# Docs
README.md
*.md
docs

# Tests
coverage
.nyc_output
__tests__

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# OS
.DS_Store
Thumbs.db
```

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

    upstream backend {
        server backend:4000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        listen 80;
        server_name localhost;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        # Backend API
        location /api {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket
        location /socket.io {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

---

## 🚀 Commands & Usage

### Makefile

```makefile
.PHONY: help build up down logs shell clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build all containers
	docker compose build

up: ## Start all containers
	docker compose up -d

down: ## Stop all containers
	docker compose down

logs: ## View logs
	docker compose logs -f

restart: ## Restart all containers
	docker compose restart

shell-backend: ## Shell into backend container
	docker compose exec backend sh

shell-frontend: ## Shell into frontend container
	docker compose exec frontend sh

clean: ## Remove all containers and volumes
	docker compose down -v
	docker system prune -f

prod-up: ## Start production stack
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down: ## Stop production stack
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down
```

### Common Commands

```bash
# Development
docker compose up -d              # Start all services
docker compose down               # Stop all services
docker compose logs -f backend    # View backend logs
docker compose exec backend sh    # Shell into backend

# Build & rebuild
docker compose build              # Build all services
docker compose build --no-cache   # Build without cache
docker compose up -d --build      # Rebuild and start

# View status
docker compose ps                 # List containers
docker compose top                # Show running processes

# Database operations
docker compose exec postgres psql -U postgres -d myapp

# Redis operations
docker compose exec redis redis-cli

# Clean up
docker compose down -v            # Remove volumes
docker system prune -a            # Clean everything
```

---

## 🎯 Best Practices

### 1. Multi-stage Builds

```dockerfile
# Separate dependencies, build, and runtime
FROM node:20 AS deps
# ... install deps

FROM node:20 AS builder
# ... build app

FROM node:20-alpine AS runner
# ... run app (smallest image)
```

### 2. Layer Caching

```dockerfile
# Copy package files first (changes less often)
COPY package*.json ./
RUN npm ci

# Copy source code last (changes more often)
COPY . .
```

### 3. Use .dockerignore

```
node_modules
.git
.env
*.log
```

### 4. Non-root User

```dockerfile
RUN adduser --system --uid 1001 appuser
USER appuser
```

### 5. Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:4000/health || exit 1
```

### 6. Environment Variables

```yaml
# docker-compose.yml
environment:
  - NODE_ENV=${NODE_ENV:-development}
  - DATABASE_URL=${DATABASE_URL}
```

### 7. Named Volumes

```yaml
volumes:
  postgres_data:    # Named volume (persistent)
  - /app/node_modules  # Anonymous volume
```

---

## 📊 Monitoring

### View Resource Usage

```bash
# Container stats
docker stats

# Specific container
docker stats project-backend

# View logs with timestamps
docker compose logs -f --timestamps backend
```

### Docker Compose Profiles

```yaml
# docker-compose.yml
services:
  monitoring:
    image: prom/prometheus
    profiles: ["monitoring"]

# Start with profile
docker compose --profile monitoring up -d
```

---

## 🔧 Debugging

```bash
# View container logs
docker compose logs backend

# Execute command in running container
docker compose exec backend npm run test

# Debug with shell
docker compose run --rm backend sh

# Check container health
docker compose ps
docker inspect project-backend

# View container processes
docker compose top backend
```

---

## 🚀 Production Deployment

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml myapp

# Scale service
docker service scale myapp_backend=5

# View services
docker stack services myapp
```

### Kubernetes (Brief)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: myregistry/backend:latest
        ports:
        - containerPort: 4000
```

---

## ✅ Checklist

**Development:**
- [ ] Multi-stage Dockerfile
- [ ] .dockerignore configured
- [ ] docker-compose.yml setup
- [ ] Hot reload working
- [ ] Volumes for node_modules

**Production:**
- [ ] Optimized image size
- [ ] Non-root user
- [ ] Health checks
- [ ] Resource limits
- [ ] Secrets management
- [ ] SSL/TLS certificates
- [ ] Logging configured
- [ ] Monitoring setup

**Security:**
- [ ] No secrets in Dockerfile
- [ ] Use official base images
- [ ] Scan for vulnerabilities
- [ ] Network isolation
- [ ] Read-only containers where possible

---

## 🐛 Common Issues

**Issue:** Port already in use  
**Fix:** `docker compose down` or change port mapping

**Issue:** Volume permission errors  
**Fix:** Use named volumes, set correct user in Dockerfile

**Issue:** Build cache not working  
**Fix:** Order COPY commands correctly, use .dockerignore

**Issue:** Large image size  
**Fix:** Use multi-stage builds, alpine images

---

**Ready for:** Containerized development & deployment  
**Next:** Run `make up` to start all services
