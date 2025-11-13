# Kubernetes Reference Guide

Comprehensive guide for Kubernetes cluster management, workload orchestration, and production deployments.

## Table of Contents
1. [Production Cluster Setup](#production-cluster-setup)
2. [Workload Management](#workload-management)
3. [Networking](#networking)
4. [Storage](#storage)
5. [Security Best Practices](#security-best-practices)
6. [Microservices Architecture](#microservices-architecture)
7. [Auto-Scaling](#auto-scaling)
8. [Service Mesh](#service-mesh)
9. [Observability](#observability)
10. [Troubleshooting](#troubleshooting)

---

## Production Cluster Setup

### Managed Kubernetes Services

#### AWS EKS
```bash
# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Create cluster
eksctl create cluster \
  --name production-cluster \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 10 \
  --managed \
  --with-oidc \
  --ssh-access \
  --ssh-public-key my-key

# Enable IRSA (IAM Roles for Service Accounts)
eksctl create iamserviceaccount \
  --name ebs-csi-controller-sa \
  --namespace kube-system \
  --cluster production-cluster \
  --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --approve

# Configure kubectl
aws eks update-kubeconfig --region us-west-2 --name production-cluster
```

#### GCP GKE
```bash
# Create cluster with autopilot (Google manages nodes)
gcloud container clusters create-auto production-cluster \
  --region us-central1 \
  --release-channel regular

# Or standard cluster with more control
gcloud container clusters create production-cluster \
  --region us-central1 \
  --num-nodes 3 \
  --node-locations us-central1-a,us-central1-b,us-central1-c \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 10 \
  --enable-autorepair \
  --enable-autoupgrade \
  --enable-ip-alias \
  --network default \
  --subnetwork default \
  --enable-stackdriver-kubernetes \
  --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver

# Get credentials
gcloud container clusters get-credentials production-cluster --region us-central1
```

#### Azure AKS
```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# Create cluster
az aks create \
  --resource-group myResourceGroup \
  --name production-cluster \
  --node-count 3 \
  --enable-addons monitoring \
  --enable-managed-identity \
  --enable-cluster-autoscaler \
  --min-count 2 \
  --max-count 10 \
  --node-vm-size Standard_DS2_v2 \
  --network-plugin azure \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group myResourceGroup --name production-cluster
```

### Self-Managed Cluster (kubeadm)

#### Prerequisites
- 3+ Ubuntu 20.04 nodes (1 control plane, 2+ workers)
- 2 CPUs, 2GB RAM minimum per node
- Network connectivity between nodes
- Unique hostname, MAC address, product_uuid per node

#### Control Plane Setup
```bash
# On control plane node
sudo kubeadm init \
  --pod-network-cidr=192.168.0.0/16 \
  --control-plane-endpoint="control-plane:6443" \
  --upload-certs

# Configure kubectl for root
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Install CNI (Calico)
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# Verify control plane
kubectl get nodes
kubectl get pods -n kube-system
```

#### Worker Nodes Setup
```bash
# On each worker node (run the join command from kubeadm init output)
sudo kubeadm join control-plane:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>

# Verify from control plane
kubectl get nodes
```

#### High Availability Control Plane
```bash
# Setup load balancer for control plane (HAProxy/NGINX)
# /etc/haproxy/haproxy.cfg
frontend k8s-api
  bind *:6443
  mode tcp
  option tcplog
  default_backend k8s-api

backend k8s-api
  mode tcp
  option tcp-check
  balance roundrobin
  server master1 10.0.0.11:6443 check
  server master2 10.0.0.12:6443 check
  server master3 10.0.0.13:6443 check

# Initialize first control plane
kubeadm init \
  --control-plane-endpoint="lb.example.com:6443" \
  --upload-certs \
  --pod-network-cidr=192.168.0.0/16

# Join additional control planes
kubeadm join lb.example.com:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane \
  --certificate-key <cert-key>
```

### Cluster Configuration Best Practices

#### Resource Planning
```yaml
# Small cluster (dev/staging)
- Control plane: 2 vCPU, 4GB RAM
- Workers: 2 vCPU, 4GB RAM (3+ nodes)

# Medium cluster (production)
- Control plane: 4 vCPU, 8GB RAM
- Workers: 4 vCPU, 16GB RAM (5+ nodes)

# Large cluster (enterprise)
- Control plane: 8 vCPU, 16GB RAM (HA: 3+ nodes)
- Workers: 8 vCPU, 32GB RAM (10+ nodes)
```

#### Cluster Hardening
```bash
# 1. Enable audit logging
# /etc/kubernetes/manifests/kube-apiserver.yaml
- --audit-policy-file=/etc/kubernetes/audit-policy.yaml
- --audit-log-path=/var/log/kubernetes/audit.log
- --audit-log-maxage=30
- --audit-log-maxbackup=10
- --audit-log-maxsize=100

# 2. Restrict anonymous access
- --anonymous-auth=false

# 3. Enable RBAC
- --authorization-mode=Node,RBAC

# 4. Secure kubelet
# /var/lib/kubelet/config.yaml
authentication:
  anonymous:
    enabled: false
  webhook:
    enabled: true
authorization:
  mode: Webhook
```

---

## Workload Management

### Deployments

#### Basic Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web
    tier: frontend
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
        tier: frontend
        version: v1.2.0
    spec:
      containers:
      - name: web
        image: myapp:v1.2.0
        ports:
        - containerPort: 8080
          name: http
          protocol: TCP
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: tmp
        emptyDir: {}
      - name: config
        configMap:
          name: app-config
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web
              topologyKey: kubernetes.io/hostname
```

#### Deployment Strategies

**Rolling Update (Default)**
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 1 extra pod during update
      maxUnavailable: 0  # No downtime
```

**Recreate (Downtime Acceptable)**
```yaml
spec:
  strategy:
    type: Recreate  # Kill all old pods, then create new
```

**Blue-Green (Manual)**
```bash
# Deploy green version
kubectl apply -f deployment-green.yaml

# Switch service to green
kubectl patch service web-app -p '{"spec":{"selector":{"version":"v2"}}}'

# Delete blue after validation
kubectl delete deployment web-app-blue
```

**Canary (Manual or with Flagger)**
```yaml
# 90% stable, 10% canary
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-stable
spec:
  replicas: 9
  # ... stable version

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-canary
spec:
  replicas: 1
  # ... canary version
```

### StatefulSets

Use for stateful applications (databases, message queues).

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: database
spec:
  serviceName: postgres
  replicas: 3
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
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 10Gi
```

**StatefulSet Features:**
- Stable network identities (postgres-0, postgres-1, postgres-2)
- Stable persistent storage (one PVC per pod)
- Ordered deployment and scaling
- Ordered updates

### DaemonSets

Run one pod per node (monitoring agents, log collectors).

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        resources:
          requests:
            memory: "200Mi"
            cpu: "100m"
          limits:
            memory: "400Mi"
            cpu: "200m"
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

### Jobs and CronJobs

#### One-Time Job
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: database-migration
spec:
  backoffLimit: 3
  ttlSecondsAfterFinished: 86400  # Cleanup after 24h
  template:
    spec:
      restartPolicy: OnFailure
      containers:
      - name: migrate
        image: myapp:v1.2.0
        command: ["python", "manage.py", "migrate"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
```

#### Scheduled CronJob
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-database
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: backup
            image: postgres:15-alpine
            command:
            - /bin/sh
            - -c
            - |
              pg_dump -h postgres.database.svc.cluster.local \
                      -U admin \
                      -d myapp \
                      -F c \
                      -f /backup/backup-$(date +%Y%m%d-%H%M%S).dump
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: backup-pvc
```

---

## Networking

### Services

#### ClusterIP (Internal Only)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    protocol: TCP
  sessionAffinity: ClientIP  # Optional: sticky sessions
```

#### NodePort (External Access via Node IP)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-nodeport
spec:
  type: NodePort
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080  # Accessible at <NodeIP>:30080
```

#### LoadBalancer (Cloud Provider)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-loadbalancer
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"  # AWS NLB
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 8080
  loadBalancerSourceRanges:  # Restrict access
  - 10.0.0.0/8
```

#### Headless Service (StatefulSet)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  clusterIP: None  # Headless
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```

### Ingress

#### NGINX Ingress Controller
```bash
# Install NGINX Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Verify installation
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

#### Basic Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
```

#### Advanced Ingress (Rate Limiting, Auth)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: advanced-ingress
  annotations:
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/limit-rps: "10"
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required'
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://trusted.com"
    nginx.ingress.kubernetes.io/enable-cors: "true"
spec:
  ingressClassName: nginx
  # ... rest of config
```

### Network Policies

#### Default Deny All
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

#### Allow Specific Traffic
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:  # Allow DNS
    - namespaceSelector:
        matchLabels:
          name: kube-system
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

### CNI Plugins

#### Calico (Most Popular)
```bash
# Install Calico
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# Enable IP-in-IP or VXLAN
kubectl patch felixconfiguration default --type merge -p '{"spec":{"ipipEnabled":true}}'
```

**Features:**
- Network policies
- BGP routing
- IP-in-IP encapsulation
- VXLAN overlay

#### Cilium (eBPF-Based)
```bash
# Install Cilium CLI
curl -L --remote-name-all https://github.com/cilium/cilium-cli/releases/latest/download/cilium-linux-amd64.tar.gz
tar xzvfC cilium-linux-amd64.tar.gz /usr/local/bin

# Install Cilium
cilium install

# Verify
cilium status
```

**Features:**
- High performance (eBPF)
- Advanced network policies (L7)
- Service mesh capabilities
- Hubble observability

---

## Storage

### PersistentVolumes and PersistentVolumeClaims

#### Static Provisioning
```yaml
# PersistentVolume (admin creates)
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    server: nfs-server.example.com
    path: /exports/data

---
# PersistentVolumeClaim (user requests)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-nfs
  namespace: production
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```

#### Dynamic Provisioning
```yaml
# StorageClass
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-east-1:123456789012:key/abcd-1234"
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer

---
# PVC (automatically creates PV)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 20Gi
```

### Storage Providers

#### AWS EBS
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: aws-ebs-gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
allowVolumeExpansion: true
```

#### GCP Persistent Disk
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gcp-pd-ssd
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
  replication-type: regional-pd
allowVolumeExpansion: true
```

#### Azure Disk
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-premium
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_LRS
  kind: Managed
allowVolumeExpansion: true
```

#### NFS
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs
provisioner: example.com/nfs
parameters:
  server: nfs-server.example.com
  path: /exports
```

---

## Security Best Practices

### RBAC (Role-Based Access Control)

#### ClusterRole (Cluster-Wide)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-pods-global
subjects:
- kind: Group
  name: pod-readers
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

#### Role (Namespace-Scoped)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
  namespace: production
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["pods", "deployments", "jobs", "cronjobs", "services", "configmaps"]
  verbs: ["get", "list", "watch", "create", "update", "patch"]
- apiGroups: [""]
  resources: ["pods/log", "pods/exec"]
  verbs: ["get", "create"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: production
subjects:
- kind: User
  name: alice@example.com
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: ci-cd-deployer
  namespace: production
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

#### Service Account
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: production

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["secrets", "configmaps"]
  verbs: ["get"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
  namespace: production
subjects:
- kind: ServiceAccount
  name: app-service-account
  namespace: production
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

### Pod Security Standards

#### Baseline Policy (Kubernetes 1.25+)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

#### Restricted Security Context
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        image: myapp:v1
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir: {}
```

### Secrets Management

#### Kubernetes Secrets (Base64 Encoded)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: production
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: cGFzc3dvcmQ=
```

#### External Secrets Operator (AWS Secrets Manager)
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets
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

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: SecretStore
  target:
    name: db-credentials
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: prod/database
      property: username
  - secretKey: password
    remoteRef:
      key: prod/database
      property: password
```

#### HashiCorp Vault Integration
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: vault-auth
  namespace: production

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-vault
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "myapp"
        vault.hashicorp.com/agent-inject-secret-database: "secret/data/database"
        vault.hashicorp.com/agent-inject-template-database: |
          {{- with secret "secret/data/database" -}}
          export DB_USER="{{ .Data.data.username }}"
          export DB_PASS="{{ .Data.data.password }}"
          {{- end }}
    spec:
      serviceAccountName: vault-auth
      containers:
      - name: app
        image: myapp:v1
        command: ["/bin/sh", "-c"]
        args:
        - source /vault/secrets/database && ./app
```

### Image Security

#### Image Pull Secrets
```bash
# Create secret
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=myuser \
  --docker-password=mypass \
  --docker-email=myemail@example.com

# Use in pod
spec:
  imagePullSecrets:
  - name: regcred
  containers:
  - name: app
    image: myuser/private-image:v1
```

#### Image Scanning (Trivy Operator)
```bash
# Install Trivy Operator
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/trivy-operator/main/deploy/static/trivy-operator.yaml

# View vulnerability reports
kubectl get vulnerabilityreports -A
```

---

## Microservices Architecture

### Service Discovery Pattern
```yaml
# Service A (Frontend)
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 3000

---
# Service B (Backend API)
apiVersion: v1
kind: Service
metadata:
  name: backend-api
spec:
  selector:
    app: backend
  ports:
  - port: 8080
    targetPort: 8080

---
# Frontend deployment connects via DNS
# Service name: backend-api.production.svc.cluster.local
# Or short form: backend-api (same namespace)
```

### Circuit Breaker Pattern (Istio)
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: backend-circuit-breaker
spec:
  host: backend-api
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 40
```

### Retry Policy (Istio)
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: backend-retry
spec:
  hosts:
  - backend-api
  http:
  - route:
    - destination:
        host: backend-api
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: 5xx,reset,connect-failure,refused-stream
```

### Rate Limiting
```yaml
# Using NGINX Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ratelimit
  annotations:
    nginx.ingress.kubernetes.io/limit-rps: "10"
    nginx.ingress.kubernetes.io/limit-burst-multiplier: "5"
spec:
  # ... rest of config
```

### Distributed Tracing (Jaeger)
```bash
# Install Jaeger Operator
kubectl create namespace observability
kubectl apply -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.49.0/jaeger-operator.yaml -n observability

# Create Jaeger instance
kubectl apply -f - <<EOF
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger
  namespace: observability
spec:
  strategy: production
  storage:
    type: elasticsearch
    options:
      es:
        server-urls: http://elasticsearch:9200
EOF
```

---

## Auto-Scaling

### Horizontal Pod Autoscaler (HPA)

#### CPU-Based Scaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

#### Memory-Based Scaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: memory-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cache-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### Custom Metrics (Prometheus)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: custom-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  minReplicas: 2
  maxReplicas: 50
  metrics:
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  - type: External
    external:
      metric:
        name: queue_messages_ready
        selector:
          matchLabels:
            queue: "tasks"
      target:
        type: AverageValue
        averageValue: "30"
```

### Vertical Pod Autoscaler (VPA)

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  updatePolicy:
    updateMode: "Auto"  # Auto, Recreate, Initial, Off
  resourcePolicy:
    containerPolicies:
    - containerName: web
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2
        memory: 2Gi
      controlledResources:
      - cpu
      - memory
```

### Cluster Autoscaler

#### AWS
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler-config
  namespace: kube-system
data:
  cluster-autoscaler-config.yaml: |
    workerGroups:
    - name: standard-workers
      minSize: 2
      maxSize: 10
      instanceType: t3.medium
```

#### GCP
```bash
# Enable autoscaling on node pool
gcloud container clusters update production-cluster \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 10 \
  --node-pool standard-workers
```

---

## Service Mesh

### Istio Installation
```bash
# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.20.0

# Install with default profile
istioctl install --set profile=demo -y

# Label namespace for automatic sidecar injection
kubectl label namespace production istio-injection=enabled

# Verify installation
kubectl get pods -n istio-system
```

### Traffic Management

#### Virtual Service (Routing)
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: backend-routes
spec:
  hosts:
  - backend-api
  http:
  - match:
    - headers:
        version:
          exact: v2
    route:
    - destination:
        host: backend-api
        subset: v2
  - route:
    - destination:
        host: backend-api
        subset: v1
      weight: 90
    - destination:
        host: backend-api
        subset: v2
      weight: 10

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: backend-subsets
spec:
  host: backend-api
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

#### Gateway (External Traffic)
```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: public-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: myapp-tls
    hosts:
    - myapp.example.com

---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp-vs
spec:
  hosts:
  - myapp.example.com
  gateways:
  - public-gateway
  http:
  - match:
    - uri:
        prefix: /api
    route:
    - destination:
        host: backend-api
        port:
          number: 8080
```

### Security (mTLS)

#### Peer Authentication (Enforce mTLS)
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # STRICT, PERMISSIVE, DISABLE
```

#### Authorization Policy
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: frontend-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: frontend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/ingress"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

---

## Observability

### Metrics (Prometheus)
```bash
# Install Prometheus using Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# Access Prometheus UI
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Default credentials: admin / prom-operator
```

### Application Metrics
```yaml
# ServiceMonitor for custom app metrics
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: backend-metrics
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### Logging (EFK Stack)

#### Install Elasticsearch
```bash
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch \
  --namespace logging \
  --create-namespace \
  --set replicas=3 \
  --set resources.requests.memory=2Gi
```

#### Install Fluentd (DaemonSet)
```yaml
# Already shown in DaemonSet section
```

#### Install Kibana
```bash
helm install kibana elastic/kibana \
  --namespace logging \
  --set service.type=LoadBalancer
```

---

## Troubleshooting

### Pod Issues

#### Pod Stuck in Pending
```bash
# Check pod events
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# 1. Insufficient resources
kubectl top nodes
kubectl describe nodes

# 2. Unbound PVC
kubectl get pvc -n <namespace>

# 3. Node selector mismatch
kubectl get nodes --show-labels
```

#### Pod CrashLoopBackOff
```bash
# Check logs
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous

# Check pod events
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# - Application error (check logs)
# - Liveness probe failing
# - Missing dependencies (database, external service)
```

#### ImagePullBackOff
```bash
# Check image pull secret
kubectl get secret regcred -n <namespace>

# Verify image exists
docker pull <image>

# Check service account
kubectl get serviceaccount default -n <namespace> -o yaml
```

### Network Issues

#### Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints <service-name> -n <namespace>

# Test from within cluster
kubectl run test-pod --image=busybox:1.28 --rm -it -- /bin/sh
wget -O- http://service-name.namespace.svc.cluster.local

# Check NetworkPolicies
kubectl get networkpolicies -n <namespace>
```

#### DNS Not Working
```bash
# Test DNS resolution
kubectl run -it --rm debug --image=busybox:1.28 --restart=Never -- nslookup kubernetes.default

# Check CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### Performance Issues

#### High Memory Usage
```bash
# Check pod metrics
kubectl top pods -n <namespace>

# Check resource limits
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 Limits

# Identify memory leak
kubectl exec -it <pod-name> -n <namespace> -- top
```

#### Slow Response Times
```bash
# Check HPA status
kubectl get hpa -n <namespace>

# Check pod readiness
kubectl get pods -n <namespace>

# Check ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller
```

### Storage Issues

#### PVC Not Binding
```bash
# Check PVC status
kubectl get pvc -n <namespace>

# Check available PVs
kubectl get pv

# Check StorageClass
kubectl get storageclass
kubectl describe storageclass <sc-name>

# Check provisioner logs (cloud-specific)
kubectl logs -n kube-system <csi-provisioner-pod>
```

---

## Best Practices Checklist

### Deployment
- [ ] Resource requests and limits set
- [ ] Liveness and readiness probes configured
- [ ] Multiple replicas for high availability
- [ ] Pod anti-affinity for spreading
- [ ] PodDisruptionBudget configured
- [ ] Rolling update strategy with maxUnavailable: 0
- [ ] Image tag is specific version (not `latest`)
- [ ] Run as non-root user
- [ ] Read-only root filesystem
- [ ] Security context configured

### Networking
- [ ] Services use ClusterIP unless external access needed
- [ ] Ingress configured for external access
- [ ] TLS/SSL certificates configured
- [ ] NetworkPolicies restrict traffic
- [ ] Rate limiting configured
- [ ] CORS configured if applicable

### Storage
- [ ] PVCs use StorageClass with appropriate performance
- [ ] ReclaimPolicy set correctly (Delete vs Retain)
- [ ] Backups configured for stateful data
- [ ] Volume expansion enabled if needed

### Security
- [ ] RBAC roles follow least privilege
- [ ] Pod Security Standards enforced
- [ ] Secrets management solution in place
- [ ] Image scanning enabled
- [ ] Network policies configured
- [ ] Audit logging enabled
- [ ] No hardcoded credentials

### Observability
- [ ] Metrics exposed and scraped by Prometheus
- [ ] Logs aggregated to central system
- [ ] Distributed tracing configured
- [ ] Dashboards created in Grafana
- [ ] Alerts configured for critical metrics
- [ ] Runbooks documented

---

**Next Steps:**
- Read terraform.md for infrastructure provisioning
- Read cicd.md for deployment automation
- Read monitoring.md for advanced observability
