# CI/CD Reference Guide

Comprehensive guide for continuous integration and deployment pipelines using GitLab CI, GitHub Actions, and deployment strategies.

## Table of Contents
1. [GitLab Pipelines](#gitlab-pipelines)
2. [GitHub Workflows](#github-workflows)
3. [Deployment Strategies](#deployment-strategies)
4. [Secret Management](#secret-management)
5. [Artifact Management](#artifact-management)
6. [Testing in CI/CD](#testing-in-cicd)
7. [Docker Build Optimization](#docker-build-optimization)
8. [Multi-Environment Deployments](#multi-environment-deployments)
9. [Rollback Mechanisms](#rollback-mechanisms)
10. [Troubleshooting](#troubleshooting)

---

## GitLab Pipelines

### Basic Pipeline Structure

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

before_script:
  - echo "Pipeline started for $CI_COMMIT_SHORT_SHA"

build:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - develop

unit-tests:
  stage: test
  image: node:18-alpine
  script:
    - npm ci
    - npm run test:unit
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
    expire_in: 1 week

integration-tests:
  stage: test
  image: node:18-alpine
  services:
    - postgres:15-alpine
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test_user
    POSTGRES_PASSWORD: test_pass
    DATABASE_URL: postgresql://test_user:test_pass@postgres:5432/test_db
  script:
    - npm ci
    - npm run test:integration
  only:
    - main
    - merge_requests

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context staging-cluster
    - kubectl set image deployment/myapp myapp=$IMAGE_TAG -n staging
    - kubectl rollout status deployment/myapp -n staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context production-cluster
    - kubectl set image deployment/myapp myapp=$IMAGE_TAG -n production
    - kubectl rollout status deployment/myapp -n production
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main
```

### Advanced GitLab Pipeline

```yaml
# .gitlab-ci.yml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG

stages:
  - validate
  - build
  - test
  - security
  - deploy
  - post-deploy

variables:
  FF_USE_FASTZIP: "true"
  CACHE_COMPRESSION_LEVEL: "fastest"
  DOCKER_BUILDKIT: 1
  
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
    - .npm/

# Validate stage
lint:
  stage: validate
  image: node:18-alpine
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run lint
  allow_failure: false

dockerfile-lint:
  stage: validate
  image: hadolint/hadolint:latest-alpine
  script:
    - hadolint Dockerfile
  allow_failure: true

# Build stage
build-image:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    # Multi-platform build
    - docker buildx create --use
    - docker buildx build 
        --platform linux/amd64,linux/arm64
        --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
        --tag $CI_REGISTRY_IMAGE:latest
        --cache-from type=registry,ref=$CI_REGISTRY_IMAGE:buildcache
        --cache-to type=registry,ref=$CI_REGISTRY_IMAGE:buildcache,mode=max
        --push
        .
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG

# Test stage
unit-test:
  stage: test
  image: node:18-alpine
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run test:unit -- --coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
    expire_in: 1 week

e2e-test:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0-focal
  services:
    - name: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
      alias: app
  variables:
    BASE_URL: http://app:3000
  script:
    - npm ci --cache .npm --prefer-offline
    - npx playwright test
  artifacts:
    when: on_failure
    paths:
      - playwright-report/
      - test-results/
    expire_in: 1 week
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure

# Security stage
container-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy image 
        --severity HIGH,CRITICAL
        --exit-code 1
        --no-progress
        $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  allow_failure: false

sast:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config=auto --json --output=sast-report.json
  artifacts:
    reports:
      sast: sast-report.json
  allow_failure: true

dependency-scan:
  stage: security
  image: node:18-alpine
  script:
    - npm audit --audit-level=high
  allow_failure: true

# Deploy stages
.deploy-template: &deploy-template
  image: bitnami/kubectl:latest
  before_script:
    - echo $KUBECONFIG_BASE64 | base64 -d > /tmp/kubeconfig
    - export KUBECONFIG=/tmp/kubeconfig
  script:
    - kubectl set image deployment/myapp 
        myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA 
        -n $NAMESPACE
    - kubectl rollout status deployment/myapp -n $NAMESPACE --timeout=5m
  after_script:
    - rm -f /tmp/kubeconfig

deploy:staging:
  <<: *deploy-template
  stage: deploy
  variables:
    NAMESPACE: staging
  environment:
    name: staging
    url: https://staging.example.com
    on_stop: stop:staging
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual

deploy:production:
  <<: *deploy-template
  stage: deploy
  variables:
    NAMESPACE: production
  environment:
    name: production
    url: https://example.com
    on_stop: stop:production
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
    - if: $CI_COMMIT_TAG
  retry:
    max: 1

stop:staging:
  <<: *deploy-template
  stage: deploy
  variables:
    NAMESPACE: staging
    GIT_STRATEGY: none
  script:
    - kubectl scale deployment/myapp --replicas=0 -n staging
  environment:
    name: staging
    action: stop
  when: manual

stop:production:
  <<: *deploy-template
  stage: deploy
  variables:
    NAMESPACE: production
    GIT_STRATEGY: none
  script:
    - kubectl scale deployment/myapp --replicas=0 -n production
  environment:
    name: production
    action: stop
  when: manual

# Post-deploy verification
smoke-test:
  stage: post-deploy
  image: curlimages/curl:latest
  script:
    - |
      for i in {1..30}; do
        if curl -f -s -o /dev/null $ENVIRONMENT_URL/health; then
          echo "Health check passed"
          exit 0
        fi
        echo "Waiting for app to be ready... ($i/30)"
        sleep 10
      done
      echo "Health check failed"
      exit 1
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Rollback job
rollback:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - echo $KUBECONFIG_BASE64 | base64 -d > /tmp/kubeconfig
    - export KUBECONFIG=/tmp/kubeconfig
    - kubectl rollout undo deployment/myapp -n production
    - kubectl rollout status deployment/myapp -n production
  environment:
    name: production
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### GitLab CI/CD Features

#### Parallel Jobs
```yaml
test:
  stage: test
  parallel:
    matrix:
      - NODE_VERSION: ['16', '18', '20']
        OS: ['alpine', 'bullseye']
  image: node:${NODE_VERSION}-${OS}
  script:
    - npm ci
    - npm test
```

#### Dynamic Child Pipelines
```yaml
generate-config:
  stage: build
  script:
    - python generate_pipeline.py > generated-config.yml
  artifacts:
    paths:
      - generated-config.yml

trigger-child-pipeline:
  stage: deploy
  trigger:
    include:
      - artifact: generated-config.yml
        job: generate-config
```

#### Scheduled Pipelines
```yaml
# Run nightly security scans
nightly-security-scan:
  stage: security
  script:
    - trivy image --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:latest
  only:
    - schedules
```

---

## GitHub Workflows

### Basic Workflow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  test:
    runs-on: ubuntu-latest
    needs: build
    
    strategy:
      matrix:
        node-version: [16, 18, 20]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json

  deploy-staging:
    runs-on: ubuntu-latest
    needs: [build, test]
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBECONFIG_STAGING }}

      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:develop-${{ github.sha }} \
            -n staging
          kubectl rollout status deployment/myapp -n staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: [build, test]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBECONFIG_PRODUCTION }}

      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main-${{ github.sha }} \
            -n production
          kubectl rollout status deployment/myapp -n production

      - name: Health check
        run: |
          sleep 30
          curl -f https://example.com/health || exit 1
```

### Advanced GitHub Workflow

```yaml
# .github/workflows/advanced-ci-cd.yml
name: Advanced CI/CD

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'
      
      - run: npm ci
      - run: npm run lint
      
      - name: Lint Dockerfile
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile

  build:
    runs-on: ubuntu-latest
    needs: lint
    permissions:
      contents: read
      packages: write
      security-events: write
    
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
      
      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true
          sbom: true
      
      - name: Scan image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  test:
    runs-on: ubuntu-latest
    needs: build
    
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    strategy:
      matrix:
        node-version: [18, 20]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:unit
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379
      
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unittests
          name: codecov-${{ matrix.node-version }}

  e2e:
    runs-on: ubuntu-latest
    needs: build
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'
      
      - name: Install Playwright
        run: |
          npm ci
          npx playwright install --with-deps
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Upload Playwright report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7

  security:
    runs-on: ubuntu-latest
    needs: build
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run SAST
        uses: returntocorp/semgrep-action@v1
        with:
          config: auto
      
      - name: Dependency review
        uses: actions/dependency-review-action@v3
        if: github.event_name == 'pull_request'
      
      - name: Check for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  deploy-staging:
    runs-on: ubuntu-latest
    needs: [build, test, e2e, security]
    if: github.ref == 'refs/heads/develop' && github.event_name == 'push'
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name staging-cluster --region us-east-1
      
      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:develop-${{ github.sha }} \
            -n staging
          kubectl rollout status deployment/myapp -n staging --timeout=5m
      
      - name: Smoke test
        run: |
          sleep 30
          curl -f https://staging.example.com/health || exit 1
      
      - name: Notify Slack
        uses: 8398a7/action-slack@v3
        if: always()
        with:
          status: ${{ job.status }}
          text: 'Staging deployment ${{ job.status }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}

  deploy-production:
    runs-on: ubuntu-latest
    needs: [build, test, e2e, security]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment:
      name: production
      url: https://example.com
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name production-cluster --region us-east-1
      
      - name: Blue-Green Deployment
        run: |
          # Deploy to green environment
          kubectl set image deployment/myapp-green \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main-${{ github.sha }} \
            -n production
          kubectl rollout status deployment/myapp-green -n production --timeout=5m
          
          # Switch traffic to green
          kubectl patch service myapp -n production -p '{"spec":{"selector":{"version":"green"}}}'
          
          # Wait and validate
          sleep 60
          curl -f https://example.com/health || exit 1
      
      - name: Create GitHub Release
        if: startsWith(github.ref, 'refs/tags/')
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
      
      - name: Notify Slack
        uses: 8398a7/action-slack@v3
        if: always()
        with:
          status: ${{ job.status }}
          text: 'Production deployment ${{ job.status }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy Workflow

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      cluster-name:
        required: true
        type: string
      namespace:
        required: true
        type: string
      image-tag:
        required: true
        type: string
    secrets:
      AWS_ACCESS_KEY_ID:
        required: true
      AWS_SECRET_ACCESS_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.environment }}
    
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name ${{ inputs.cluster-name }} --region us-east-1
      
      - name: Deploy
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ inputs.image-tag }} \
            -n ${{ inputs.namespace }}
          kubectl rollout status deployment/myapp -n ${{ inputs.namespace }}
```

Use reusable workflow:
```yaml
# .github/workflows/main.yml
jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
      cluster-name: staging-cluster
      namespace: staging
      image-tag: ${{ needs.build.outputs.image-tag }}
    secrets:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## Deployment Strategies

### Rolling Update

**Gradual replacement of old pods with new ones.**

```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Max 2 extra pods during update
      maxUnavailable: 1  # Max 1 pod down during update
```

**CI/CD Pipeline:**
```yaml
deploy:
  script:
    - kubectl apply -f deployment.yaml
    - kubectl rollout status deployment/myapp
    - |
      if ! kubectl rollout status deployment/myapp; then
        kubectl rollout undo deployment/myapp
        exit 1
      fi
```

**Pros:**
- Zero downtime
- Gradual rollout (can catch issues early)
- Easy rollback

**Cons:**
- Both versions running simultaneously
- Not suitable for breaking changes

### Blue-Green Deployment

**Two identical environments, switch traffic between them.**

```yaml
# Blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 5
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0

---
# Green deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 5
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: myapp
        image: myapp:v2.0

---
# Service (switch selector to change active version)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change to 'green' to switch
  ports:
  - port: 80
    targetPort: 8080
```

**CI/CD Pipeline:**
```bash
#!/bin/bash
# blue-green-deploy.sh

# Get current active version
CURRENT=$(kubectl get service myapp -o jsonpath='{.spec.selector.version}')
if [ "$CURRENT" == "blue" ]; then
  NEW="green"
  OLD="blue"
else
  NEW="blue"
  OLD="green"
fi

echo "Current: $OLD, Deploying to: $NEW"

# Deploy to inactive environment
kubectl set image deployment/myapp-$NEW myapp=$IMAGE_TAG
kubectl rollout status deployment/myapp-$NEW

# Run smoke tests
kubectl port-forward deployment/myapp-$NEW 8080:8080 &
PF_PID=$!
sleep 5

if curl -f http://localhost:8080/health; then
  echo "Health check passed"
else
  echo "Health check failed"
  kill $PF_PID
  exit 1
fi
kill $PF_PID

# Switch traffic
kubectl patch service myapp -p "{\"spec\":{\"selector\":{\"version\":\"$NEW\"}}}"

echo "Traffic switched to $NEW"
echo "Old version ($OLD) still running for rollback"
```

**Pros:**
- Instant switchover
- Easy rollback (switch back)
- Full environment testing before switch

**Cons:**
- Requires 2x resources
- Database migrations complex

### Canary Deployment

**Gradually shift traffic to new version.**

```yaml
# Stable version (90%)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  template:
    metadata:
      labels:
        app: myapp
        version: stable
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0

---
# Canary version (10%)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: myapp
        version: canary
    spec:
      containers:
      - name: myapp
        image: myapp:v2.0

---
# Service (routes to both)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp  # Matches both stable and canary
  ports:
  - port: 80
    targetPort: 8080
```

**Progressive Canary with Flagger:**
```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  service:
    port: 80
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
    webhooks:
    - name: load-test
      url: http://load-tester.test/
      timeout: 5s
      metadata:
        cmd: "hey -z 1m -q 10 -c 2 http://myapp.production/"
```

**Manual Canary Script:**
```bash
#!/bin/bash
# canary-deploy.sh

# Deploy canary with 10% traffic
kubectl apply -f deployment-canary.yaml
kubectl scale deployment myapp-canary --replicas=1
kubectl scale deployment myapp-stable --replicas=9

echo "Canary deployed with 10% traffic"
echo "Monitoring metrics for 10 minutes..."

# Monitor error rate
for i in {1..10}; do
  ERROR_RATE=$(kubectl exec -it prometheus-0 -- \
    promtool query instant \
    'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))')
  
  echo "Minute $i: Error rate $ERROR_RATE"
  
  if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
    echo "Error rate too high! Rolling back..."
    kubectl scale deployment myapp-canary --replicas=0
    exit 1
  fi
  
  sleep 60
done

# Gradually increase canary traffic
for weight in 25 50 75 100; do
  CANARY_REPLICAS=$((weight / 10))
  STABLE_REPLICAS=$((10 - CANARY_REPLICAS))
  
  kubectl scale deployment myapp-canary --replicas=$CANARY_REPLICAS
  kubectl scale deployment myapp-stable --replicas=$STABLE_REPLICAS
  
  echo "Canary at ${weight}% traffic"
  sleep 300  # Wait 5 minutes
done

# Full rollout
kubectl scale deployment myapp-stable --replicas=0
kubectl scale deployment myapp-canary --replicas=10
echo "Canary promoted to stable"
```

**Pros:**
- Minimal blast radius
- Real production testing
- Data-driven decisions

**Cons:**
- Complex monitoring required
- Longer deployment time
- Requires traffic splitting

### Recreate (Downtime)

**Stop old version, start new version.**

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  strategy:
    type: Recreate
```

**Use Cases:**
- Development environments
- Maintenance windows
- Breaking database changes

---

## Secret Management

### GitLab CI Variables

```yaml
# Project Settings > CI/CD > Variables
# Add variables:
# - KUBECONFIG_BASE64 (Protected, Masked)
# - DATABASE_URL (Protected, Masked)
# - AWS_ACCESS_KEY_ID (Protected, Masked)

deploy:
  script:
    - echo $KUBECONFIG_BASE64 | base64 -d > /tmp/kubeconfig
    - export KUBECONFIG=/tmp/kubeconfig
    - kubectl create secret generic app-secrets \
        --from-literal=database-url=$DATABASE_URL \
        --dry-run=client -o yaml | kubectl apply -f -
```

### GitHub Actions Secrets

```yaml
# Repository Settings > Secrets and variables > Actions
# Add secrets:
# - KUBECONFIG_STAGING
# - KUBECONFIG_PRODUCTION
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY

deploy:
  steps:
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        kubeconfig: ${{ secrets.KUBECONFIG_PRODUCTION }}
    
    - name: Create Kubernetes secret
      run: |
        kubectl create secret generic app-secrets \
          --from-literal=api-key=${{ secrets.API_KEY }} \
          --dry-run=client -o yaml | kubectl apply -f -
```

### External Secrets Operator

```yaml
# Install External Secrets Operator
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace

# Configure AWS Secrets Manager backend
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secretsmanager
  namespace: production
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa

# Create ExternalSecret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-url
    remoteRef:
      key: prod/app/database-url
  - secretKey: api-key
    remoteRef:
      key: prod/app/api-key
```

---

## Artifact Management

### Docker Image Versioning

```bash
# Semantic versioning
docker tag myapp:latest myapp:1.2.3
docker tag myapp:latest myapp:1.2
docker tag myapp:latest myapp:1

# Git commit SHA
docker tag myapp:latest myapp:${GIT_COMMIT_SHA}

# Branch + SHA
docker tag myapp:latest myapp:main-${GIT_COMMIT_SHA}

# Date + SHA
docker tag myapp:latest myapp:$(date +%Y%m%d)-${GIT_COMMIT_SHA}
```

### Multi-Registry Push

```yaml
# GitLab CI
build:
  script:
    # Push to GitLab Registry
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    
    # Push to Docker Hub
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA dockerhub/myapp:$CI_COMMIT_SHA
    - docker login -u $DOCKERHUB_USER -p $DOCKERHUB_TOKEN
    - docker push dockerhub/myapp:$CI_COMMIT_SHA
    
    # Push to AWS ECR
    - aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $ECR_REGISTRY/myapp:$CI_COMMIT_SHA
    - docker push $ECR_REGISTRY/myapp:$CI_COMMIT_SHA
```

### Artifact Retention

```yaml
# GitLab Container Registry cleanup
# Project Settings > Packages and registries > Container Registry
# Cleanup policies:
# - Keep most recent: 10 tags
# - Keep tags matching: ^v\d+\.\d+\.\d+$
# - Older than: 30 days
# - Cadence: Every week

# GitHub Actions
# Retention period: 90 days (default)
# Configure in repository settings
```

---

## Testing in CI/CD

### Unit Tests
```yaml
unit-tests:
  stage: test
  image: node:18-alpine
  script:
    - npm ci
    - npm run test:unit -- --coverage --reporters=default --reporters=jest-junit
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```

### Integration Tests
```yaml
integration-tests:
  stage: test
  services:
    - postgres:15-alpine
    - redis:7-alpine
  variables:
    DATABASE_URL: postgresql://test:test@postgres:5432/testdb
    REDIS_URL: redis://redis:6379
  script:
    - npm ci
    - npm run db:migrate
    - npm run test:integration
```

### E2E Tests
```yaml
e2e-tests:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0-focal
  script:
    - npm ci
    - npx playwright test
  artifacts:
    when: on_failure
    paths:
      - playwright-report/
      - test-results/
```

### Load Tests
```yaml
load-test:
  stage: post-deploy
  image: grafana/k6:latest
  script:
    - k6 run --vus 100 --duration 5m loadtest.js
  artifacts:
    reports:
      load_performance: k6-results.json
```

---

## Docker Build Optimization

### BuildKit Cache
```yaml
build:
  script:
    - export DOCKER_BUILDKIT=1
    - docker build 
        --cache-from $CI_REGISTRY_IMAGE:buildcache
        --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
        --build-arg BUILDKIT_INLINE_CACHE=1
        .
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:buildcache
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:buildcache
```

### Multi-Stage Build
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/main.js"]
```

---

## Multi-Environment Deployments

### Environment-Specific Configs
```yaml
# config/dev.yaml
replicas: 1
resources:
  requests:
    cpu: 100m
    memory: 128Mi

# config/staging.yaml
replicas: 2
resources:
  requests:
    cpu: 250m
    memory: 256Mi

# config/production.yaml
replicas: 5
resources:
  requests:
    cpu: 500m
    memory: 512Mi
```

### Kustomize
```yaml
# base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest

# overlays/production/kustomization.yaml
bases:
- ../../base
patchesStrategicMerge:
- deployment-patch.yaml
replicas:
- name: myapp
  count: 5
images:
- name: myapp
  newTag: v1.2.3
```

### Helm
```yaml
# values-dev.yaml
replicaCount: 1
resources:
  limits:
    cpu: 500m
    memory: 512Mi

# values-prod.yaml
replicaCount: 5
resources:
  limits:
    cpu: 2000m
    memory: 2Gi

# Deploy
helm upgrade --install myapp ./chart \
  -f values-prod.yaml \
  --namespace production
```

---

## Rollback Mechanisms

### Kubernetes Rollout
```bash
# View rollout history
kubectl rollout history deployment/myapp

# Rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=3
```

### GitLab CI Rollback Job
```yaml
rollback:
  stage: deploy
  script:
    - kubectl rollout undo deployment/myapp -n production
    - kubectl rollout status deployment/myapp -n production
  when: manual
  only:
    - main
```

### GitHub Actions Rollback
```yaml
rollback:
  runs-on: ubuntu-latest
  environment: production
  steps:
    - name: Rollback deployment
      run: |
        kubectl rollout undo deployment/myapp -n production
        kubectl rollout status deployment/myapp -n production
```

---

## Troubleshooting

### Pipeline Failures

**Docker Build Fails**
```bash
# Check Docker daemon
docker info

# Clear build cache
docker builder prune -af

# Check Dockerfile syntax
hadolint Dockerfile
```

**kubectl Connection Issues**
```bash
# Verify kubeconfig
kubectl cluster-info

# Check credentials
kubectl auth can-i get pods

# Test connection
kubectl get nodes
```

**Secret Not Found**
```bash
# Verify secret exists
kubectl get secrets -n <namespace>

# Check secret data
kubectl get secret <name> -o yaml

# Recreate secret
kubectl delete secret <name>
kubectl create secret generic <name> --from-literal=key=value
```

---

**Best Practices:**
- Always run tests before deployment
- Use semantic versioning for images
- Implement health checks
- Monitor deployments
- Have rollback plan
- Secure secrets properly
- Document runbooks

**Next Steps:**
- Read terraform.md for infrastructure
- Read monitoring.md for observability
- Read docker.md for container optimization
