# DevOps Master Skill

**Comprehensive DevOps workflows for containerization, orchestration, infrastructure automation, and production deployment.**

## Overview

DevOps Master provides enterprise-grade guidance for:
- **Container Orchestration**: Docker, Kubernetes, Helm
- **CI/CD Pipelines**: GitLab CI, GitHub Actions
- **Infrastructure as Code**: Terraform, Ansible
- **Monitoring & Observability**: Prometheus, Grafana, ELK
- **Cloud Deployment**: AWS, GCP, Azure
- **Security & Compliance**: Scanning, auditing, best practices

## Quick Start

### 1. Container Deployment
```bash
# Read Docker best practices
Read references/docker.md

# Build optimized image
docker build -t myapp:v1.0 .

# Deploy to Kubernetes
kubectl apply -f assets/templates/k8s-deployment.yaml
```

### 2. Setup CI/CD Pipeline
```bash
# For GitLab
cp assets/templates/gitlab-ci.yml .gitlab-ci.yml

# For GitHub Actions
cp assets/templates/github-workflow.yml .github/workflows/deploy.yml
```

### 3. Infrastructure Provisioning
```bash
# Validate Terraform
python scripts/validate_terraform.py ./terraform/

# Estimate costs
python scripts/cost_estimator.py ./terraform/

# Apply infrastructure
terraform init
terraform plan
terraform apply
```

### 4. Setup Monitoring
```bash
# Install Prometheus + Grafana
helm install prometheus prometheus-community/kube-prometheus-stack \
  -f assets/templates/prometheus-values.yaml \
  --namespace monitoring \
  --create-namespace
```

## Core Capabilities

### Container Orchestration
- Multi-stage Docker builds
- Kubernetes production deployments
- Helm chart management
- Service mesh (Istio, Linkerd)

### CI/CD Automation
- Automated testing pipelines
- Security scanning integration
- Blue-green deployments
- Canary releases
- Automated rollbacks

### Infrastructure as Code
- Terraform modules (AWS, GCP, Azure)
- State management with remote backends
- Multi-cloud deployments
- Cost optimization

### Monitoring & Alerting
- Prometheus metrics collection
- Grafana dashboards
- ELK stack for logging
- Distributed tracing (Jaeger)
- Custom alerting rules

## Files Structure

```
DevOps_Master/
├── SKILL.md                    # Main skill documentation
├── README.md                   # This file
├── references/                 # Deep-dive guides
│   ├── docker.md              # Container optimization
│   ├── kubernetes.md          # K8s production setup
│   ├── cicd.md                # Pipeline design
│   ├── terraform.md           # Multi-cloud IaC
│   └── monitoring.md          # Observability stack
├── scripts/                    # Automation tools
│   ├── validate_terraform.py  # Config validation
│   ├── cost_estimator.py      # Cost analysis
│   ├── security_audit.py      # Security scanning
│   └── health_check.py        # App health checks
└── assets/templates/           # Production configs
    ├── Dockerfile             # Multi-stage build
    ├── gitlab-ci.yml          # GitLab pipeline
    ├── github-workflow.yml    # GitHub Actions
    ├── prometheus-values.yaml # Monitoring setup
    └── k8s-deployment.yaml    # K8s manifests
```

## Key Workflows

### Microservices Deployment
1. Review architecture patterns
2. Create namespace and quotas
3. Deploy services with Helm
4. Configure service mesh
5. Setup ingress and routing
6. Implement observability

### Blue-Green Deployment
1. Deploy new version (green)
2. Run smoke tests
3. Validate metrics
4. Switch traffic
5. Monitor for issues
6. Keep blue for rollback

### Auto-Scaling Setup
1. Configure HPA (Horizontal Pod Autoscaler)
2. Enable cluster autoscaler
3. Set pod disruption budgets
4. Configure resource limits
5. Test scaling behavior
6. Monitor metrics

### Security Hardening
1. Enable RBAC with least privilege
2. Implement network policies
3. Configure Pod Security Standards
4. Setup secrets management
5. Enable audit logging
6. Scan images for vulnerabilities
7. Implement runtime security

## Automation Scripts

### Terraform Validator
```bash
python scripts/validate_terraform.py ./terraform/production
```
Checks for:
- Security misconfigurations
- Missing best practices
- Cost optimization opportunities
- Hardcoded credentials

### Cost Estimator
```bash
python scripts/cost_estimator.py ./terraform/production
```
Provides:
- Monthly cost breakdown by resource
- Annual cost projections
- Optimization suggestions
- Multi-cloud pricing

### Security Auditor
```bash
python scripts/security_audit.py production-cluster
```
Audits:
- RBAC configurations
- Network policies
- Pod security standards
- Secrets management
- Image vulnerabilities

### Health Checker
```bash
python scripts/health_check.py production
```
Checks:
- Pod health status
- Deployment readiness
- Service endpoints
- Ingress configuration
- PVC bindings

## Templates

### Dockerfile
Production-ready multi-stage build with:
- Alpine base images
- Non-root user
- Security best practices
- Health checks

### CI/CD Pipelines
Complete pipelines with:
- Linting and validation
- Automated testing
- Security scanning
- Multi-environment deployment
- Rollback capabilities

### Kubernetes Manifests
Production deployments with:
- Resource limits
- Health probes
- Security contexts
- Anti-affinity rules
- ConfigMaps and Secrets

### Monitoring Configs
Observability stack with:
- Prometheus scraping
- Grafana dashboards
- Alert rules
- Log aggregation

## Best Practices

### Containers
- Use multi-stage builds
- Run as non-root user
- Scan for vulnerabilities
- Pin specific versions
- Minimize image layers

### Kubernetes
- Set resource requests/limits
- Configure health probes
- Implement pod disruption budgets
- Use namespace isolation
- Enable RBAC

### Infrastructure
- Use modules for reusability
- Store state remotely with locking
- Version control all IaC files
- Tag resources for cost tracking
- Review changes in PRs

### CI/CD
- Fail fast with validation
- Run tests in parallel
- Implement deployment gates
- Automate rollbacks
- Monitor pipeline performance

### Monitoring
- Collect metrics at all layers
- Set up alerts with severity levels
- Implement SLOs and error budgets
- Use dashboards for different audiences
- Retain logs per compliance needs

## Decision Trees

### Container Platform
- Simple (1-5 services) → Docker Compose / ECS / Cloud Run
- Complex (5+ services) → Kubernetes (EKS/GKE/AKS)
- Serverless workloads → Lambda / Cloud Functions

### CI/CD Platform
- GitLab → GitLab CI
- GitHub → GitHub Actions
- Bitbucket → Bitbucket Pipelines
- Existing Jenkins → Migrate or enhance

### Monitoring Solution
- Metrics only → Prometheus + Grafana
- Logs + Metrics → ELK + Prometheus
- APM + Tracing → Jaeger + Prometheus
- All-in-one → DataDog / New Relic

## Common Issues & Solutions

### Pods Pending
- Check: `kubectl describe pod <name>`
- Causes: Insufficient resources, node selector mismatch, PVC not bound
- Solution: Scale cluster or adjust requests

### High Cloud Costs
- Run: `python scripts/cost_estimator.py`
- Causes: Over-provisioning, expensive regions, no auto-scaling
- Solution: Right-size instances, use spot, implement autoscaling

### Pipeline Failures
- Check logs and secrets
- Causes: Dependency mismatches, missing credentials, flaky tests
- Solution: Lock versions, verify secrets, improve test stability

## Success Metrics

Track these KPIs:
- **Deployment Frequency**: Daily to production
- **Lead Time**: <1 hour commit to production
- **MTTR**: <30 minutes to restore
- **Change Failure Rate**: <15% cause incidents
- **Infrastructure Cost**: Trending downward
- **Security Score**: >90% on audits
- **Uptime**: >99.9% availability

## Getting Started Checklist

Before production:
- [ ] Images scanned for vulnerabilities
- [ ] Resource requests/limits set
- [ ] Health probes configured
- [ ] Auto-scaling enabled
- [ ] Monitoring and alerting configured
- [ ] CI/CD pipeline tested
- [ ] Security policies enabled
- [ ] Backup and DR tested
- [ ] Cost alerts configured
- [ ] Documentation updated
- [ ] Load testing completed
- [ ] Secrets management implemented
- [ ] Logging aggregation configured
- [ ] Performance baselines established
- [ ] Incident response plan documented

## Support & Resources

- **Docker**: references/docker.md
- **Kubernetes**: references/kubernetes.md
- **CI/CD**: references/cicd.md
- **Terraform**: references/terraform.md
- **Monitoring**: references/monitoring.md

## License

MIT License - See main repository LICENSE file

---

**Remember**: DevOps is about culture and practices, not just tools. Focus on automation, collaboration, and continuous improvement.

**Version**: 1.0.0  
**Last Updated**: January 2025
