---
name: devops-master
description: |
  Docker Kubernetes CI/CD Terraform infrastructure DevOps automation deployment monitoring. Container orchestration GitHub Actions GitLab pipeline cloud AWS Azure GCP deployment. Use when: DevOps setup, Docker containerization, Kubernetes cluster, CI/CD pipeline, GitHub Actions workflow, GitLab CI, Jenkins pipeline, infrastructure as code, Terraform, cloud deployment, AWS ECS EKS, Azure AKS, GCP GKE, container orchestration, monitoring Prometheus Grafana, logging ELK stack, security scanning, Trivy Snyk, deployment strategy, blue-green canary, infrastructure automation, cloud architecture.
---

# DevOps Master Skill

Comprehensive DevOps workflows for containerization, orchestration, infrastructure automation, and production deployment across cloud platforms.

## Core Capabilities

### 1. Container Orchestration
- Docker multi-stage builds and optimization
- Kubernetes cluster setup and management
- Helm chart development and deployment
- Service mesh configuration (Istio, Linkerd)
- Container security and scanning

### 2. CI/CD Pipelines
- GitLab CI/CD pipeline design
- GitHub Actions workflows
- Multi-stage deployment strategies
- Automated testing integration
- Artifact management and versioning

### 3. Infrastructure as Code
- Terraform modules for multi-cloud
- Ansible playbooks for configuration
- CloudFormation templates (AWS)
- ARM templates (Azure)
- Deployment Manager (GCP)

### 4. Monitoring & Observability
- Prometheus metrics collection
- Grafana dashboard creation
- ELK/EFK stack setup
- Distributed tracing (Jaeger, Zipkin)
- Alerting and incident response

### 5. Cloud Deployment
- AWS: ECS, EKS, Lambda, RDS
- GCP: GKE, Cloud Run, Cloud SQL
- Azure: AKS, App Service, Cosmos DB
- Multi-cloud architecture patterns
- Cost optimization strategies

## Quick Start Workflows

### Deploy Containerized Application

**Step 1: Containerize Application**
```bash
# Review Dockerfile best practices
Read {baseDir}/references/docker.md section "Multi-Stage Builds"

# Build optimized image
docker build -t myapp:v1.0 .
docker scan myapp:v1.0  # Security scan
```

**Step 2: Setup Kubernetes Cluster**
```bash
# For production setup, see detailed guide
Read {baseDir}/references/kubernetes.md section "Production Cluster Setup"

# Quick local setup
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**Step 3: Configure CI/CD**
```bash
# Choose pipeline based on platform
# GitLab CI: Read {baseDir}/references/cicd.md section "GitLab Pipelines"
# GitHub Actions: Read {baseDir}/references/cicd.md section "GitHub Workflows"

# Deploy pipeline config
cp {baseDir}/assets/templates/gitlab-ci.yml .gitlab-ci.yml
# or
cp {baseDir}/assets/templates/github-workflow.yml .github/workflows/deploy.yml
```

### Infrastructure Provisioning

**Step 1: Plan Infrastructure**
```bash
# Review Terraform best practices
Read {baseDir}/references/terraform.md section "Module Design"

# Initialize and plan
terraform init
terraform plan -out=tfplan
```

**Step 2: Validate Configuration**
```bash
# Run validation script
python {baseDir}/scripts/validate_terraform.py ./terraform/

# Check cost estimation
python {baseDir}/scripts/cost_estimator.py ./terraform/
```

**Step 3: Apply Infrastructure**
```bash
# Apply with approval
terraform apply tfplan

# Configure monitoring
Read {baseDir}/references/monitoring.md section "Auto-Discovery"
```

### Setup Monitoring Stack

**Step 1: Deploy Prometheus**
```bash
# Use Helm chart with custom values
Read {baseDir}/references/monitoring.md section "Prometheus Setup"

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  -f {baseDir}/assets/templates/prometheus-values.yaml
```

**Step 2: Configure Grafana Dashboards**
```bash
# Import pre-built dashboards
kubectl apply -f {baseDir}/assets/templates/grafana-dashboards.yaml

# For custom metrics, see
Read {baseDir}/references/monitoring.md section "Custom Metrics"
```

**Step 3: Setup Alerting**
```bash
# Configure alert rules
kubectl apply -f {baseDir}/assets/templates/alert-rules.yaml

# Integrate with incident management
Read {baseDir}/references/monitoring.md section "Alert Manager"
```

## Key Workflows

### 1. Microservices Deployment

**Scenario:** Deploy multiple microservices with service mesh

**Process:**
1. Review microservices architecture patterns
   - Read {baseDir}/references/kubernetes.md section "Microservices Architecture"
2. Create namespace and resource quotas
3. Deploy services with Helm
4. Configure Istio/Linkerd service mesh
5. Setup ingress and traffic routing
6. Implement circuit breakers and retries
7. Configure distributed tracing

**Validation:**
- All pods running: `kubectl get pods -n <namespace>`
- Service mesh healthy: `istioctl analyze`
- Traffic routing works: Test endpoints
- Metrics flowing: Check Prometheus targets

### 2. Blue-Green Deployment

**Scenario:** Zero-downtime production deployment

**Process:**
1. Review deployment strategies
   - Read {baseDir}/references/cicd.md section "Deployment Strategies"
2. Deploy new version (green environment)
3. Run smoke tests on green
4. Validate metrics and logs
5. Switch traffic from blue to green
6. Monitor for issues
7. Keep blue environment for rollback

**Rollback Plan:**
- If issues detected within 15min: Switch traffic to blue
- If persistent errors: Scale down green, investigate
- Document rollback decision in incident report

### 3. Auto-Scaling Configuration

**Scenario:** Handle variable load with HPA and cluster autoscaler

**Process:**
1. Review scaling best practices
   - Read {baseDir}/references/kubernetes.md section "Auto-Scaling"
2. Configure Horizontal Pod Autoscaler (HPA)
   ```yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: myapp-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: myapp
     minReplicas: 2
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```
3. Enable cluster autoscaler for node scaling
4. Set pod disruption budgets
5. Configure resource requests/limits
6. Test scaling behavior with load tests
7. Monitor scaling metrics in Grafana

**Validation:**
- HPA responds to load: `kubectl get hpa`
- Nodes scale up/down: `kubectl get nodes`
- No pod evictions: Check events
- Costs stay within budget: Run cost analysis script

### 4. Multi-Cloud Deployment

**Scenario:** Deploy application across AWS, GCP, and Azure

**Process:**
1. Review multi-cloud architecture
   - Read {baseDir}/references/terraform.md section "Multi-Cloud Modules"
2. Design unified Terraform modules
3. Provision infrastructure on each cloud
4. Setup global load balancing
5. Configure cross-region replication
6. Implement disaster recovery
7. Setup unified monitoring

**Key Considerations:**
- Use cloud-agnostic services where possible
- Implement abstraction layers for cloud-specific APIs
- Centralize logging and metrics
- Plan for data sovereignty requirements
- Monitor costs across all providers

### 5. Security Hardening

**Scenario:** Implement security best practices for production clusters

**Process:**
1. Review security checklist
   - Read {baseDir}/references/kubernetes.md section "Security Best Practices"
2. Enable RBAC with least privilege
3. Implement network policies
4. Setup Pod Security Standards
5. Configure secrets management (Vault, Sealed Secrets)
6. Enable audit logging
7. Scan images for vulnerabilities
8. Implement runtime security (Falco)
9. Setup security monitoring and alerts

**Validation:**
- Run security audit: `python {baseDir}/scripts/security_audit.py`
- Check pod security: `kubectl get psp`
- Verify network policies: Test connectivity
- Review audit logs: Check for unauthorized access

## Tool Integration

### Docker
- Multi-stage builds for size optimization
- BuildKit for faster builds
- Docker Compose for local development
- Registry mirroring and caching
- Image signing and verification

**For details:** Read {baseDir}/references/docker.md

### Kubernetes
- Cluster provisioning (kubeadm, kops, managed services)
- Workload management (Deployments, StatefulSets, DaemonSets)
- Networking (CNI plugins, Ingress, Service Mesh)
- Storage (PV, PVC, StorageClasses)
- Security (RBAC, NetworkPolicies, PodSecurityPolicies)

**For details:** Read {baseDir}/references/kubernetes.md

### Terraform
- Module design patterns
- State management (remote backends)
- Workspaces for environments
- Provider configuration
- Import existing infrastructure

**For details:** Read {baseDir}/references/terraform.md

### CI/CD Platforms
- Pipeline design patterns
- Secret management
- Artifact versioning
- Deployment gates
- Rollback mechanisms

**For details:** Read {baseDir}/references/cicd.md

### Monitoring Tools
- Prometheus metric collection
- Grafana visualization
- Alert configuration
- Log aggregation (ELK/EFK)
- Distributed tracing

**For details:** Read {baseDir}/references/monitoring.md

## Automation Scripts

### Terraform Validator
```bash
python {baseDir}/scripts/validate_terraform.py <terraform_dir>
```
Validates Terraform configurations for best practices, security issues, and cost optimization opportunities.

### Cost Estimator
```bash
python {baseDir}/scripts/cost_estimator.py <terraform_dir>
```
Estimates monthly cloud costs based on Terraform configurations across AWS, GCP, and Azure.

### Security Audit
```bash
python {baseDir}/scripts/security_audit.py <cluster_context>
```
Audits Kubernetes cluster for security misconfigurations, generates report with remediation steps.

### Health Check
```bash
python {baseDir}/scripts/health_check.py <namespace>
```
Comprehensive health check for deployed applications, including pods, services, ingress, and dependencies.

## Decision Trees

### Container Orchestration Platform
```
Need container orchestration?
├─ Yes
│  ├─ Simple application (1-5 services)?
│  │  ├─ Use Docker Compose (local/dev)
│  │  └─ Use AWS ECS / Cloud Run (production)
│  ├─ Complex microservices (5+ services)?
│  │  └─ Use Kubernetes
│  │     ├─ Cloud provider? → Managed K8s (EKS/GKE/AKS)
│  │     └─ On-prem? → Self-managed (kubeadm/kops)
│  └─ Serverless workloads?
│     └─ Use Lambda / Cloud Functions / Azure Functions
└─ No → Use traditional VMs or bare metal
```

### CI/CD Platform Choice
```
Existing version control?
├─ GitLab → Use GitLab CI
├─ GitHub → Use GitHub Actions
├─ Bitbucket → Use Bitbucket Pipelines
└─ Jenkins → Migrate or enhance existing setup

For details: Read {baseDir}/references/cicd.md section "Platform Selection"
```

### Monitoring Solution
```
Requirements?
├─ Metrics only → Prometheus + Grafana
├─ Logs + Metrics → ELK/EFK + Prometheus
├─ APM + Distributed Tracing → Jaeger/Zipkin + Prometheus
└─ All-in-one commercial → DataDog / New Relic

For setup: Read {baseDir}/references/monitoring.md
```

## Best Practices

### Container Images
1. Use multi-stage builds to reduce image size
2. Run containers as non-root user
3. Scan images for vulnerabilities
4. Pin base image versions (avoid `latest` tag)
5. Minimize layers and use .dockerignore
6. Sign images for supply chain security

### Kubernetes Deployments
1. Set resource requests and limits
2. Use liveness and readiness probes
3. Implement pod disruption budgets
4. Configure horizontal pod autoscaling
5. Use namespace isolation
6. Enable RBAC with least privilege
7. Implement network policies
8. Use secrets for sensitive data
9. Version all manifests in Git
10. Test in staging before production

### Infrastructure as Code
1. Use modules for reusable components
2. Store state remotely with locking
3. Separate environments with workspaces
4. Version control all IaC files
5. Run `terraform plan` before apply
6. Use variables for environment-specific values
7. Implement naming conventions
8. Tag all resources for cost tracking
9. Document module inputs and outputs
10. Review changes in pull requests

### CI/CD Pipelines
1. Fail fast with quick validation steps
2. Run tests in parallel when possible
3. Use caching for dependencies
4. Implement deployment gates
5. Automate rollbacks on failure
6. Version all artifacts
7. Separate build and deploy stages
8. Use secrets management tools
9. Implement audit logging
10. Monitor pipeline performance

### Monitoring & Alerting
1. Collect metrics at all layers (infra, app, business)
2. Set up alerts with clear severity levels
3. Implement SLOs and error budgets
4. Use dashboards for different audiences
5. Retain logs based on compliance requirements
6. Implement distributed tracing for microservices
7. Monitor costs and set budgets
8. Test alert channels regularly
9. Document runbooks for common alerts
10. Review and tune alerts periodically

## Common Issues & Solutions

### Issue: Pods Stuck in Pending State
**Diagnosis:**
```bash
kubectl describe pod <pod-name>
# Check Events section for reasons
```

**Common Causes:**
1. Insufficient resources (CPU/memory)
   - Scale cluster or adjust resource requests
2. Node selector/affinity not matched
   - Verify node labels match pod requirements
3. PVC not bound
   - Check PVC status and StorageClass

**Solution:** Read {baseDir}/references/kubernetes.md section "Troubleshooting"

### Issue: High Cloud Costs
**Diagnosis:**
```bash
python {baseDir}/scripts/cost_estimator.py ./terraform/
# Review cost breakdown by service
```

**Common Causes:**
1. Over-provisioned resources
2. Running resources in expensive regions
3. No auto-scaling configured
4. Unused resources not cleaned up

**Solution:** Read {baseDir}/references/terraform.md section "Cost Optimization"

### Issue: CI/CD Pipeline Failures
**Diagnosis:**
- Check pipeline logs for error messages
- Verify secrets and environment variables
- Test locally with same tool versions

**Common Causes:**
1. Dependency version mismatches
2. Missing secrets or credentials
3. Flaky tests
4. Rate limiting from external services

**Solution:** Read {baseDir}/references/cicd.md section "Troubleshooting"

## Progressive Enhancement

This skill uses progressive disclosure:
- **SKILL.md** (this file): Quick start and common workflows
- **references/**: Deep-dive guides loaded as needed
- **assets/templates/**: Production-ready configurations
- **scripts/**: Automation tools for repetitive tasks

Load additional resources based on your specific needs:
- Docker optimization → docker.md
- K8s production setup → kubernetes.md  
- Multi-cloud IaC → terraform.md
- Pipeline design → cicd.md
- Observability setup → monitoring.md

## Success Metrics

Track these KPIs:
- **Deployment Frequency:** Daily deployments to production
- **Lead Time:** <1 hour from commit to production
- **MTTR:** <30 minutes to restore service
- **Change Failure Rate:** <15% of deployments cause incidents
- **Infrastructure Cost:** Trend downward with optimization
- **Security Score:** >90% on security audits
- **Uptime:** >99.9% availability

## Getting Started Checklist

Before deploying to production:
- [ ] Docker images scanned for vulnerabilities
- [ ] Resource requests/limits set on all pods
- [ ] Liveness and readiness probes configured
- [ ] Horizontal pod autoscaling enabled
- [ ] Monitoring and alerting configured
- [ ] CI/CD pipeline tested with rollback
- [ ] Security policies enabled (RBAC, NetworkPolicy)
- [ ] Backup and disaster recovery tested
- [ ] Cost alerts configured
- [ ] Documentation updated (runbooks, architecture diagrams)
- [ ] Load testing completed
- [ ] Secrets management implemented
- [ ] Logging aggregation configured
- [ ] Performance baselines established
- [ ] Incident response plan documented

---

**Remember:** DevOps is about culture and practices, not just tools. Focus on automation, collaboration, and continuous improvement. Start small, iterate, and scale gradually.
