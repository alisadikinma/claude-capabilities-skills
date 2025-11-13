# Monitoring Reference Guide

Comprehensive guide for observability stack with Prometheus, Grafana, ELK, distributed tracing, and alerting.

## Table of Contents
1. [Prometheus Setup](#prometheus-setup)
2. [Grafana Dashboards](#grafana-dashboards)
3. [Custom Metrics](#custom-metrics)
4. [Alert Manager](#alert-manager)
5. [ELK Stack](#elk-stack)
6. [Distributed Tracing](#distributed-tracing)
7. [Auto-Discovery](#auto-discovery)
8. [SLI/SLO/SLA](#slislosla)
9. [Troubleshooting](#troubleshooting)

---

## Prometheus Setup

### Installation with Helm

```bash
# Add Prometheus community Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack (includes Prometheus, Grafana, Alertmanager)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
  --set grafana.adminPassword=admin123
```

### Custom Prometheus Values

```yaml
# prometheus-values.yaml
prometheus:
  prometheusSpec:
    retention: 30d
    retentionSize: "45GB"
    
    resources:
      requests:
        cpu: 500m
        memory: 2Gi
      limits:
        cpu: 2000m
        memory: 4Gi
    
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: fast-ssd
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 50Gi
    
    # External labels for federation/remote write
    externalLabels:
      cluster: production
      region: us-east-1
    
    # Scrape interval
    scrapeInterval: 30s
    evaluationInterval: 30s
    
    # Service monitors
    serviceMonitorSelector:
      matchLabels:
        prometheus: kube-prometheus
    
    # Pod monitors
    podMonitorSelector:
      matchLabels:
        prometheus: kube-prometheus
    
    # Additional scrape configs
    additionalScrapeConfigs:
    - job_name: 'kubernetes-nodes'
      kubernetes_sd_configs:
      - role: node
      relabel_configs:
      - source_labels: [__address__]
        regex: '(.*):10250'
        replacement: '${1}:9100'
        target_label: __address__
    
    # Remote write to long-term storage
    remoteWrite:
    - url: "https://prometheus-remote-storage.example.com/api/v1/write"
      basicAuth:
        username:
          name: prometheus-remote-storage-secret
          key: username
        password:
          name: prometheus-remote-storage-secret
          key: password

alertmanager:
  alertmanagerSpec:
    retention: 120h
    
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 256Mi
    
    storage:
      volumeClaimTemplate:
        spec:
          storageClassName: fast-ssd
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 10Gi

grafana:
  adminPassword: changeme
  
  persistence:
    enabled: true
    storageClassName: fast-ssd
    size: 10Gi
  
  resources:
    requests:
      cpu: 250m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi
  
  # Additional datasources
  additionalDataSources:
  - name: Loki
    type: loki
    url: http://loki:3100
    access: proxy
    isDefault: false
  
  - name: Jaeger
    type: jaeger
    url: http://jaeger-query:16686
    access: proxy
  
  # Pre-installed dashboards
  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
      - name: 'default'
        orgId: 1
        folder: ''
        type: file
        disableDeletion: false
        editable: true
        options:
          path: /var/lib/grafana/dashboards/default
  
  dashboards:
    default:
      kubernetes-cluster:
        gnetId: 7249
        revision: 1
        datasource: Prometheus
      node-exporter:
        gnetId: 1860
        revision: 27
        datasource: Prometheus

# Node exporter for node metrics
nodeExporter:
  enabled: true

# Kube-state-metrics for Kubernetes object metrics
kubeStateMetrics:
  enabled: true
```

### Prometheus Configuration

```yaml
# prometheus-config.yaml
global:
  scrape_interval: 30s
  evaluation_interval: 30s
  external_labels:
    cluster: 'production'
    replica: '$(HOSTNAME)'

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - alertmanager:9093

# Load rules
rule_files:
  - /etc/prometheus/rules/*.yml

# Scrape configurations
scrape_configs:
  # Kubernetes API server
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
    - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
    - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
      action: keep
      regex: default;kubernetes;https

  # Kubernetes nodes
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
    - role: node
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
    - action: labelmap
      regex: __meta_kubernetes_node_label_(.+)

  # Kubernetes pods
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
    - role: pod
    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
      action: replace
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
      target_label: __address__
    - action: labelmap
      regex: __meta_kubernetes_pod_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_pod_name]
      action: replace
      target_label: kubernetes_pod_name

  # Service monitors
  - job_name: 'kubernetes-service-endpoints'
    kubernetes_sd_configs:
    - role: endpoints
    relabel_configs:
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
      action: replace
      target_label: __scheme__
      regex: (https?)
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
      action: replace
      target_label: __address__
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
```

---

## Grafana Dashboards

### Kubernetes Cluster Dashboard

```json
{
  "dashboard": {
    "title": "Kubernetes Cluster Overview",
    "tags": ["kubernetes", "cluster"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Cluster CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(container_cpu_usage_seconds_total[5m])) by (node)",
            "legendFormat": "{{node}}"
          }
        ],
        "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "Cluster Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(container_memory_working_set_bytes) by (node) / 1024^3",
            "legendFormat": "{{node}}"
          }
        ],
        "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "Pod Count by Namespace",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(kube_pod_info) by (namespace)",
            "legendFormat": "{{namespace}}"
          }
        ],
        "gridPos": {"x": 0, "y": 8, "w": 12, "h": 8}
      },
      {
        "title": "Failed Pods",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(kube_pod_status_phase{phase=\"Failed\"})"
          }
        ],
        "gridPos": {"x": 12, "y": 8, "w": 6, "h": 4}
      },
      {
        "title": "Pending Pods",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(kube_pod_status_phase{phase=\"Pending\"})"
          }
        ],
        "gridPos": {"x": 18, "y": 8, "w": 6, "h": 4}
      }
    ]
  }
}
```

### Application Performance Dashboard

```json
{
  "dashboard": {
    "title": "Application Performance",
    "tags": ["application", "performance"],
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service, status)",
            "legendFormat": "{{service}} - {{status}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (service) / sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ],
        "alert": {
          "name": "High Error Rate",
          "conditions": [
            {
              "evaluator": {"type": "gt", "params": [0.05]},
              "query": {"params": ["A", "5m", "now"]}
            }
          ]
        }
      },
      {
        "title": "Response Time (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Active Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(http_connections_active) by (service)",
            "legendFormat": "{{service}}"
          }
        ]
      }
    ]
  }
}
```

### Database Performance Dashboard

```json
{
  "dashboard": {
    "title": "PostgreSQL Performance",
    "panels": [
      {
        "title": "Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "pg_stat_database_numbackends{datname=\"myapp\"}",
            "legendFormat": "Active Connections"
          },
          {
            "expr": "pg_settings_max_connections",
            "legendFormat": "Max Connections"
          }
        ]
      },
      {
        "title": "Query Duration (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(pg_stat_statements_total_time_bucket[5m]))",
            "legendFormat": "p95"
          }
        ]
      },
      {
        "title": "Cache Hit Ratio",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(pg_stat_database_blks_hit) / (sum(pg_stat_database_blks_hit) + sum(pg_stat_database_blks_read)) * 100"
          }
        ]
      },
      {
        "title": "Database Size",
        "type": "graph",
        "targets": [
          {
            "expr": "pg_database_size_bytes{datname=\"myapp\"} / 1024^3",
            "legendFormat": "Size (GB)"
          }
        ]
      }
    ]
  }
}
```

---

## Custom Metrics

### Application Instrumentation (Node.js)

```javascript
// metrics.js
const client = require('prom-client');

// Create a Registry
const register = new client.Registry();

// Default metrics (CPU, memory, etc.)
client.collectDefaultMetrics({ register });

// Custom counter
const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [register]
});

// Custom histogram
const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.1, 0.5, 1, 2, 5],
  registers: [register]
});

// Custom gauge
const activeConnections = new client.Gauge({
  name: 'http_connections_active',
  help: 'Number of active HTTP connections',
  registers: [register]
});

// Middleware
function metricsMiddleware(req, res, next) {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    
    httpRequestsTotal.inc({
      method: req.method,
      route: req.route?.path || req.path,
      status: res.statusCode
    });
    
    httpRequestDuration.observe({
      method: req.method,
      route: req.route?.path || req.path,
      status: res.statusCode
    }, duration);
  });
  
  next();
}

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

module.exports = { metricsMiddleware, activeConnections };
```

### Application Instrumentation (Python)

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
from flask import Response
import time

# Custom metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1, 2, 5]
)

active_connections = Gauge(
    'http_connections_active',
    'Active HTTP connections'
)

# Middleware
def metrics_middleware(app):
    @app.before_request
    def before_request():
        request.start_time = time.time()
        active_connections.inc()
    
    @app.after_request
    def after_request(response):
        duration = time.time() - request.start_time
        
        http_requests_total.labels(
            method=request.method,
            endpoint=request.endpoint,
            status=response.status_code
        ).inc()
        
        http_request_duration.labels(
            method=request.method,
            endpoint=request.endpoint
        ).observe(duration)
        
        active_connections.dec()
        
        return response

# Metrics endpoint
@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')
```

### ServiceMonitor for Custom App

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp-metrics
  namespace: production
  labels:
    prometheus: kube-prometheus
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

---

## Alert Manager

### Alertmanager Configuration

```yaml
# alertmanager-config.yaml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/XXX/YYY/ZZZ'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  routes:
  - match:
      severity: critical
    receiver: 'pagerduty'
    continue: true
  - match:
      severity: warning
    receiver: 'slack'
  - match:
      alertname: DeadMansSwitch
    receiver: 'null'

receivers:
- name: 'default'
  slack_configs:
  - channel: '#alerts'
    title: 'Alert: {{ .GroupLabels.alertname }}'
    text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

- name: 'slack'
  slack_configs:
  - channel: '#alerts'
    title: '{{ .GroupLabels.alertname }}'
    text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
    send_resolved: true

- name: 'pagerduty'
  pagerduty_configs:
  - service_key: 'YOUR_PAGERDUTY_KEY'
    description: '{{ .GroupLabels.alertname }}'

- name: 'email'
  email_configs:
  - to: 'alerts@example.com'
    from: 'prometheus@example.com'
    smarthost: 'smtp.gmail.com:587'
    auth_username: 'prometheus@example.com'
    auth_password: 'password'
    headers:
      Subject: 'Alert: {{ .GroupLabels.alertname }}'

- name: 'null'

inhibit_rules:
- source_match:
    severity: 'critical'
  target_match:
    severity: 'warning'
  equal: ['alertname', 'cluster', 'service']
```

### Alert Rules

```yaml
# alert-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: application-alerts
  namespace: monitoring
spec:
  groups:
  - name: application
    interval: 30s
    rules:
    # High error rate
    - alert: HighErrorRate
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
        /
        sum(rate(http_requests_total[5m])) by (service)
        > 0.05
      for: 5m
      labels:
        severity: critical
        team: backend
      annotations:
        summary: "High error rate on {{ $labels.service }}"
        description: "{{ $labels.service }} has error rate of {{ $value | humanizePercentage }}"
        runbook_url: "https://runbooks.example.com/high-error-rate"
    
    # High latency
    - alert: HighLatency
      expr: |
        histogram_quantile(0.95,
          sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
        ) > 2
      for: 10m
      labels:
        severity: warning
        team: backend
      annotations:
        summary: "High latency on {{ $labels.service }}"
        description: "{{ $labels.service }} p95 latency is {{ $value }}s"
    
    # Pod crashes
    - alert: PodCrashLooping
      expr: |
        rate(kube_pod_container_status_restarts_total[15m]) > 0
      for: 5m
      labels:
        severity: critical
        team: platform
      annotations:
        summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
        description: "Pod has restarted {{ $value }} times in the last 15 minutes"
    
    # Database connections
    - alert: DatabaseConnectionsHigh
      expr: |
        pg_stat_database_numbackends{datname="myapp"}
        /
        pg_settings_max_connections
        > 0.8
      for: 5m
      labels:
        severity: warning
        team: database
      annotations:
        summary: "Database connections are high"
        description: "Database has {{ $value | humanizePercentage }} of max connections"
    
    # Disk space
    - alert: DiskSpaceLow
      expr: |
        (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) < 0.1
      for: 5m
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "Disk space low on {{ $labels.instance }}"
        description: "Only {{ $value | humanizePercentage }} disk space remaining"
    
    # Memory usage
    - alert: HighMemoryUsage
      expr: |
        (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) > 0.9
      for: 10m
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "High memory usage on {{ $labels.instance }}"
        description: "Memory usage is {{ $value | humanizePercentage }}"
    
    # SSL certificate expiry
    - alert: SSLCertificateExpiringSoon
      expr: |
        probe_ssl_earliest_cert_expiry - time() < 86400 * 7
      for: 1h
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "SSL certificate expiring soon"
        description: "Certificate for {{ $labels.instance }} expires in {{ $value | humanizeDuration }}"
```

---

## ELK Stack

### Elasticsearch Setup

```yaml
# elasticsearch-values.yaml
clusterName: "elasticsearch"
nodeGroup: "master"

replicas: 3
minimumMasterNodes: 2

esJavaOpts: "-Xmx2g -Xms2g"

resources:
  requests:
    cpu: "1000m"
    memory: "3Gi"
  limits:
    cpu: "2000m"
    memory: "4Gi"

volumeClaimTemplate:
  accessModes: ["ReadWriteOnce"]
  storageClassName: "fast-ssd"
  resources:
    requests:
      storage: 100Gi

esConfig:
  elasticsearch.yml: |
    cluster.name: "production-logs"
    network.host: 0.0.0.0
    
    # Security
    xpack.security.enabled: true
    xpack.security.transport.ssl.enabled: true
    xpack.security.transport.ssl.verification_mode: certificate
    xpack.security.transport.ssl.keystore.path: /usr/share/elasticsearch/config/certs/elastic-certificates.p12
    xpack.security.transport.ssl.truststore.path: /usr/share/elasticsearch/config/certs/elastic-certificates.p12
    
    # Index lifecycle management
    xpack.ilm.enabled: true
```

### Fluentd Configuration

```yaml
# fluentd-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    <filter kubernetes.**>
      @type kubernetes_metadata
      @id filter_kube_metadata
    </filter>

    <filter kubernetes.**>
      @type parser
      key_name log
      reserve_data true
      <parse>
        @type json
      </parse>
    </filter>

    <match kubernetes.**>
      @type elasticsearch
      @id out_es
      host elasticsearch.logging.svc.cluster.local
      port 9200
      scheme https
      ssl_verify false
      user elastic
      password ${ELASTICSEARCH_PASSWORD}
      
      logstash_format true
      logstash_prefix kubernetes
      
      <buffer>
        @type file
        path /var/log/fluentd-buffers/kubernetes.system.buffer
        flush_mode interval
        retry_type exponential_backoff
        flush_thread_count 2
        flush_interval 5s
        retry_forever true
        retry_max_interval 30
        chunk_limit_size 2M
        queue_limit_length 8
        overflow_action block
      </buffer>
    </match>
```

### Kibana Dashboards

```json
{
  "title": "Application Logs",
  "timeRestore": true,
  "timeFrom": "now-15m",
  "timeTo": "now",
  "kibanaSavedObjectMeta": {
    "searchSourceJSON": {
      "query": {
        "query_string": {
          "query": "kubernetes.namespace_name:production AND kubernetes.labels.app:myapp",
          "analyze_wildcard": true
        }
      },
      "filter": [
        {
          "query": {
            "match": {
              "log_level": {
                "query": "error",
                "type": "phrase"
              }
            }
          }
        }
      ]
    }
  }
}
```

---

## Distributed Tracing

### Jaeger Installation

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
        server-urls: http://elasticsearch.logging.svc.cluster.local:9200
        index-prefix: jaeger
    esIndexCleaner:
      enabled: true
      numberOfDays: 7
      schedule: "55 23 * * *"
  ingress:
    enabled: true
    annotations:
      kubernetes.io/ingress.class: nginx
    hosts:
    - jaeger.example.com
EOF
```

### Application Instrumentation (OpenTelemetry)

```javascript
// tracing.js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'myapp',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
  }),
  traceExporter: new JaegerExporter({
    endpoint: 'http://jaeger-collector.observability.svc.cluster.local:14268/api/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

process.on('SIGTERM', () => {
  sdk.shutdown()
    .then(() => console.log('Tracing terminated'))
    .catch((error) => console.log('Error terminating tracing', error))
    .finally(() => process.exit(0));
});
```

---

## Auto-Discovery

### Kubernetes Service Discovery

Prometheus automatically discovers:
- Kubernetes API server
- Kubernetes nodes
- Kubernetes pods (with annotations)
- Kubernetes services (with annotations)

**Pod Annotations for Scraping:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  containers:
  - name: myapp
    image: myapp:v1
    ports:
    - containerPort: 8080
      name: metrics
```

### Dynamic Targets with Consul

```yaml
scrape_configs:
- job_name: 'consul-services'
  consul_sd_configs:
  - server: 'consul.service.consul:8500'
    datacenter: 'dc1'
  relabel_configs:
  - source_labels: [__meta_consul_service]
    target_label: job
  - source_labels: [__meta_consul_tags]
    regex: '.*,metrics,.*'
    action: keep
```

---

## SLI/SLO/SLA

### Service Level Indicators (SLI)

```yaml
# Example SLIs
- name: availability
  query: |
    sum(rate(http_requests_total{status!~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m]))

- name: latency
  query: |
    histogram_quantile(0.95,
      sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
    )

- name: error_rate
  query: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m]))
```

### Service Level Objectives (SLO)

```yaml
# SLO definitions
slos:
- name: availability
  target: 99.9  # 99.9% uptime
  window: 30d
  
- name: latency_p95
  target: 500   # p95 < 500ms
  window: 7d
  
- name: error_rate
  target: 1     # < 1% errors
  window: 7d
```

### Error Budget Alerts

```yaml
- alert: ErrorBudgetBurn
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{status!~"5.."}[1h]))
        /
        sum(rate(http_requests_total[1h]))
      )
    ) > (1 - 0.999) * 14.4  # 14.4x burn rate for 99.9% SLO
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Error budget burning too fast"
    description: "At current rate, monthly error budget will be exhausted in {{ $value | humanizeDuration }}"
```

---

## Troubleshooting

### Prometheus Issues

**Prometheus OOM:**
```bash
# Increase memory limits
kubectl edit statefulset prometheus-prometheus-kube-prometheus-prometheus -n monitoring

# Reduce retention period
--set prometheus.prometheusSpec.retention=15d
```

**High cardinality:**
```bash
# Check series count
curl http://prometheus:9090/api/v1/status/tsdb | jq '.data.seriesCountByMetricName' | sort -t: -k2 -nr | head

# Drop high-cardinality metrics
metric_relabel_configs:
- source_labels: [__name__]
  regex: 'high_cardinality_metric.*'
  action: drop
```

### Missing Metrics

```bash
# Check targets
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Visit http://localhost:9090/targets

# Check service discovery
# Visit http://localhost:9090/service-discovery

# Verify ServiceMonitor
kubectl get servicemonitor -n production
kubectl describe servicemonitor myapp-metrics -n production
```

---

**Best Practices:**
- Retention: 30 days for Prometheus, longer for long-term storage
- Scrape interval: 30s (balance between freshness and cardinality)
- Alert on symptoms, not causes
- Define SLOs and error budgets
- Use dashboards for different audiences
- Implement distributed tracing for microservices

**Next Steps:**
- Read kubernetes.md for K8s metrics
- Read cicd.md for deployment monitoring
- Read docker.md for container metrics
