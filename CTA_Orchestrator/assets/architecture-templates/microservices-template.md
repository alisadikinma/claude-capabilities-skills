# Microservices Architecture Template

## Overview
Microservices architecture decomposes applications into independently deployable services, each handling a specific business capability.

## When to Use
- **Scalability**: Different services need different scaling strategies
- **Team Structure**: Multiple teams working independently
- **Technology Diversity**: Different services need different tech stacks
- **Deployment Independence**: Need to deploy services independently

## Architecture Components

### Service Boundaries
```
┌─────────────────┐
│  API Gateway    │
│  (Kong/Nginx)   │
└────────┬────────┘
         │
    ┌────┴────┬─────────┬─────────┬──────────┐
    ▼         ▼         ▼         ▼          ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌───────┐
│User  │ │Order │ │Payment│ │Product││Notif  │
│Service│ │Service│ │Service│ │Service││Service│
└──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └───┬───┘
   │        │        │        │          │
   └────────┴────────┴────────┴──────────┘
                     │
            ┌────────┴────────┐
            ▼                 ▼
       ┌─────────┐      ┌──────────┐
       │PostgreSQL│      │ Redis    │
       │(Primary) │      │ (Cache)  │
       └─────────┘      └──────────┘
```

### Technology Stack Recommendation

**API Gateway**
- Kong (feature-rich, plugin ecosystem)
- Nginx + OpenResty (lightweight, Lua scripting)
- AWS API Gateway (managed service)

**Service Communication**
- Synchronous: REST/gRPC
- Asynchronous: RabbitMQ, Kafka, NATS

**Service Discovery**
- Consul (service mesh)
- Kubernetes built-in (in K8s environment)
- etcd (distributed config)

**Database Per Service**
- Each service has its own database
- Use event sourcing for data consistency
- Implement saga pattern for distributed transactions

## Implementation Checklist

### Phase 1: Service Identification
- [ ] Define service boundaries by business capability
- [ ] Identify service dependencies
- [ ] Design inter-service communication contracts
- [ ] Plan data ownership per service

### Phase 2: Infrastructure Setup
- [ ] Setup API Gateway
- [ ] Configure service discovery
- [ ] Setup message broker (if async needed)
- [ ] Configure distributed tracing (Jaeger, Zipkin)
- [ ] Setup centralized logging (ELK, Grafana Loki)

### Phase 3: Service Development
- [ ] Implement health check endpoints
- [ ] Add circuit breakers (Hystrix, Resilience4j)
- [ ] Implement retry logic with exponential backoff
- [ ] Add monitoring and metrics (Prometheus)
- [ ] Implement distributed tracing

### Phase 4: Deployment
- [ ] Containerize each service (Docker)
- [ ] Setup orchestration (Kubernetes, Docker Swarm)
- [ ] Configure auto-scaling policies
- [ ] Setup CI/CD pipelines per service
- [ ] Implement blue-green or canary deployments

## Service Template Structure

```
service-name/
├── src/
│   ├── api/          # REST/gRPC endpoints
│   ├── domain/       # Business logic
│   ├── repository/   # Data access
│   └── events/       # Event handlers
├── tests/
│   ├── unit/
│   └── integration/
├── config/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── prod.yaml
├── Dockerfile
├── docker-compose.yml
└── k8s/
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

## Common Patterns

### 1. API Gateway Pattern
- Single entry point for all clients
- Handles authentication, rate limiting, routing
- Aggregates responses from multiple services

### 2. Service Registry Pattern
- Services register themselves on startup
- Clients discover services dynamically
- Health checks for service availability

### 3. Circuit Breaker Pattern
- Prevent cascading failures
- Fast fail on service unavailability
- Automatic recovery when service recovers

### 4. Saga Pattern
- Distributed transactions across services
- Compensating transactions on failure
- Choreography vs Orchestration approaches

### 5. Event Sourcing
- Store state changes as events
- Rebuild state by replaying events
- Audit trail and temporal queries

## Anti-Patterns to Avoid

❌ **Distributed Monolith**: Services too tightly coupled  
❌ **Chatty Services**: Too many inter-service calls  
❌ **Shared Database**: Services accessing same database  
❌ **No API Versioning**: Breaking changes without versioning  
❌ **Missing Observability**: No logging/monitoring/tracing

## Performance Considerations

- **Latency**: Network calls add latency
- **Data Consistency**: Eventual consistency vs strong consistency
- **Network Failures**: Implement retry and timeout strategies
- **Resource Overhead**: Each service needs separate resources

## Cost Implications

**Higher Costs**:
- More infrastructure (servers, databases, monitoring)
- Increased operational complexity
- Higher development time initially

**Cost Optimization**:
- Container orchestration for resource efficiency
- Horizontal pod autoscaling
- Reserved instances for predictable workloads
- Spot instances for non-critical services

## Migration Strategy (Monolith → Microservices)

1. **Strangler Fig Pattern**
   - Gradually extract services from monolith
   - Route new features to new services
   - Migrate old features incrementally

2. **Database Decomposition**
   - Start with schema separation
   - Use views for backwards compatibility
   - Migrate to separate databases per service

3. **Testing Strategy**
   - Contract testing (Pact)
   - End-to-end testing in staging
   - Chaos engineering for resilience

## Success Metrics

- Service independence: <10% coupling between services
- Deployment frequency: Multiple deploys per day per service
- Mean time to recovery (MTTR): <15 minutes
- Service availability: 99.9% uptime per service
- API latency: p95 <200ms through gateway

---

**Related Skills**: Web_Architect_Pro, DevOps_Master
**Complexity**: High
**Team Size**: 5+ developers recommended
