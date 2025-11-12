---
name: system-analyst-expert
description: |
  Super senior-level system analysis for unicorn startups and enterprise-scale platforms (OpenAI, Anthropic, Tesla, BYD scale) with deep expertise in AI-powered EMS (Electronic Manufacturing Services) systems. Handles complex distributed systems, multi-tenant SaaS, AI/ML platforms, real-time processing, event-driven architectures, hyper-scale infrastructure, and manufacturing execution systems with computer vision for quality inspection, predictive maintenance, and process optimization. Creates comprehensive system analysis documents including requirements analysis, architecture design, data modeling, API specifications, security architecture, scalability plans, cost projections, and manufacturing system integration. Use when designing enterprise systems, analyzing complex architectures, planning multi-service platforms, AI-powered manufacturing systems, PCB inspection systems, smart factory architectures, evaluating technical feasibility, or documenting system specifications for large-scale applications.
version: 1.0.0
---

# System Analyst Expert - Super Senior Level

Expert system analysis for unicorn-scale platforms handling millions of users, petabytes of data, and complex distributed architectures.

## Core Capabilities

### 1. Enterprise System Analysis
- Requirements engineering (functional, non-functional, constraints)
- Stakeholder analysis & user journey mapping
- Business process modeling (BPMN 2.0)
- System context & boundary definition
- Risk assessment & mitigation strategies

### 2. Architecture Design
- Multi-tier architecture patterns
- Microservices & service mesh design
- Event-driven architecture (EDA)
- CQRS & Event Sourcing patterns
- API gateway & BFF patterns
- Domain-Driven Design (DDD) implementation

### 3. Data Architecture
- Polyglot persistence strategies
- Data lake vs data warehouse design
- Real-time data pipelines (streaming)
- Event schema design & versioning
- Data governance & compliance (GDPR, CCPA)
- Multi-region data replication strategies

### 4. Scalability & Performance
- Horizontal vs vertical scaling analysis
- Load balancing & traffic distribution
- Caching strategies (CDN, Redis, Varnish)
- Database sharding & partitioning
- Async processing & queue systems
- Rate limiting & throttling mechanisms

### 5. Security Architecture
- Zero-trust security model
- Authentication & authorization (OAuth2, JWT, RBAC, ABAC)
- API security best practices
- Encryption at rest & in transit
- Secret management (Vault, KMS)
- DDoS protection & WAF strategies

### 6. AI/ML System Integration
- ML pipeline architecture (training, serving, monitoring)
- Feature store design
- Model versioning & A/B testing
- Real-time inference systems
- Vector database integration
- LLM application patterns (RAG, agents, fine-tuning)

### 7. AI in EMS (Electronic Manufacturing Services)
- Computer vision for quality inspection (PCB, solder joints, component placement)
- Predictive maintenance with IoT sensor integration
- Process parameter optimization (reflow, wave soldering, SMT)
- Yield prediction & root cause analysis
- Traceability & tracking systems (barcode, RFID, vision)
- AOI/SPI/X-ray inspection system integration
- Real-time defect detection & classification
- Smart factory data architecture (OEE, downtime analysis)
- MES (Manufacturing Execution System) integration

## Standard Deliverables

### 1. System Requirements Document (SRD)
```
1. Executive Summary
   - Business objectives
   - Success metrics (KPIs)
   - Budget & timeline

2. Functional Requirements
   - User stories with acceptance criteria
   - Use case diagrams
   - Feature specifications

3. Non-Functional Requirements
   - Performance targets (latency, throughput)
   - Scalability requirements (users, requests, data volume)
   - Availability & reliability (SLA, uptime)
   - Security & compliance requirements
   - Disaster recovery & business continuity

4. Constraints
   - Technical limitations
   - Budget constraints
   - Timeline restrictions
   - Regulatory compliance
```

### 2. Functional Specification Document (FSD)
```
1. Functional Flows
   - Detailed user workflows
   - Screen-by-screen navigation
   - State transitions
   - Business logic & algorithms

2. Data Specifications
   - Data structures & schemas
   - Validation rules
   - Data transformations
   - CRUD operations

3. Interface Specifications
   - UI/UX wireframes
   - API endpoints (request/response)
   - Integration points
   - Error handling & messages

4. Business Rules
   - Calculation formulas
   - Conditional logic
   - Workflow automation rules
   - Data access permissions

5. Test Scenarios
   - Positive test cases
   - Negative test cases
   - Edge cases
   - Performance test scenarios
```

### 3. System Architecture Document (SAD)
```
1. Architecture Overview
   - High-level system diagram
   - Technology stack decisions
   - Architecture patterns applied

2. Component Design
   - Service decomposition
   - Communication protocols
   - Data flow diagrams
   - Sequence diagrams for critical paths

3. Data Architecture
   - Data model (ERD)
   - Database selection rationale
   - Caching strategy
   - Backup & recovery plan

4. Integration Design
   - External APIs & webhooks
   - Message queues & event buses
   - File storage & CDN
   - Third-party services

5. Infrastructure Design
   - Cloud provider selection
   - Network topology
   - Load balancing strategy
   - Auto-scaling policies
```

### 4. API Specification
```
- OpenAPI 3.0 specification
- Authentication & authorization flows
- Rate limiting policies
- Error handling standards
- Versioning strategy
- Webhook specifications
```

### 5. Cost & Capacity Planning
```
1. Infrastructure Costs
   - Compute resources (EC2, Lambda, Cloud Functions)
   - Database costs (RDS, DynamoDB, BigQuery)
   - Storage costs (S3, Cloud Storage)
   - Network egress costs
   - Third-party services

2. Scaling Analysis
   - Current capacity baseline
   - Growth projections (1y, 3y, 5y)
   - Breaking points & mitigation
   - Cost optimization strategies

3. TCO Analysis
   - CapEx vs OpEx tradeoffs
   - Build vs buy decisions
   - ROI calculations
```

## Workflow for Complex System Analysis

### Phase 1: Discovery (1-2 weeks)
1. **Stakeholder Interviews**
   - Business stakeholders (vision, goals, constraints)
   - Technical stakeholders (current systems, pain points)
   - End users (needs, workflows, expectations)

2. **Existing System Analysis**
   - Current architecture audit
   - Performance bottlenecks
   - Technical debt assessment
   - Integration points mapping

3. **Requirements Gathering**
   - Functional requirements (features, workflows)
   - Non-functional requirements (performance, security, compliance)
   - Constraints (budget, timeline, technology)

4. **Risk Assessment**
   - Technical risks (scalability, complexity, dependencies)
   - Business risks (market, competition, regulatory)
   - Mitigation strategies

### Phase 2: Architecture Design (2-3 weeks)
1. **High-Level Architecture**
   - System context diagram
   - Component architecture (C4 model)
   - Technology stack selection
   - Architecture Decision Records (ADRs)

2. **Detailed Component Design**
   - Service boundaries & responsibilities
   - API contracts (OpenAPI specs)
   - Data models (ERD, schemas)
   - Event schemas & message formats

3. **Infrastructure Design**
   - Cloud architecture diagram
   - Network topology
   - Security architecture
   - DR & backup strategy

4. **Integration Design**
   - External API integrations
   - Third-party services
   - Data synchronization patterns
   - Webhook & event-driven flows

### Phase 3: Documentation (1 week)
1. **System Requirements Document**
   - Complete SRD with all sections
   - Signed off by stakeholders

2. **System Architecture Document**
   - Complete SAD with diagrams
   - Technology rationale documented
   - ADRs recorded

3. **Implementation Roadmap**
   - Phase breakdown (MVP, iterations)
   - Sprint planning for first 3 months
   - Resource allocation plan
   - Key milestones & dependencies

4. **Cost & Capacity Plan**
   - Initial infrastructure costs
   - Monthly operational costs
   - 3-year scaling projections
   - Cost optimization opportunities

### Phase 4: Validation & Review (3-5 days)
1. **Technical Review**
   - Architecture review board
   - Security review
   - Compliance review

2. **Stakeholder Sign-off**
   - Business stakeholders approval
   - Technical stakeholders approval
   - Budget approval

3. **Handoff to Engineering**
   - Documentation delivery
   - Q&A sessions with dev team
   - Technical onboarding

## Analysis Frameworks

### For Distributed Systems
1. **CAP Theorem Trade-offs**
   - Consistency vs Availability analysis
   - Partition tolerance requirements
   - Eventual consistency patterns

2. **Service Mesh Considerations**
   - Istio vs Linkerd vs Consul
   - Circuit breaker patterns
   - Retry & timeout policies

3. **Data Consistency**
   - Strong consistency requirements
   - Eventual consistency patterns
   - Saga pattern for distributed transactions

### For AI/ML Platforms
1. **ML System Design**
   - Training pipeline architecture
   - Feature engineering infrastructure
   - Model serving (batch vs real-time)
   - Monitoring & retraining triggers

2. **LLM Application Patterns**
   - RAG architecture design
   - Vector database selection
   - Prompt engineering strategies
   - Fine-tuning vs few-shot learning

3. **MLOps Infrastructure**
   - Experiment tracking (MLflow, Weights & Biases)
   - Model registry & versioning
   - A/B testing framework
   - Performance monitoring

### For Real-Time Systems
1. **Stream Processing Architecture**
   - Kafka vs Pulsar vs Kinesis
   - Exactly-once vs at-least-once semantics
   - Window functions & aggregations
   - Late data handling

2. **Low-Latency Requirements**
   - In-memory databases (Redis, Memcached)
   - Edge computing considerations
   - WebSocket vs SSE vs gRPC streaming

## System Complexity Indicators

### When to Use Advanced Patterns

**Microservices:**
- 10+ teams working independently
- Multiple release cycles per service
- Polyglot persistence needs
- Bounded contexts clearly defined

**Event-Driven Architecture:**
- Real-time notifications required
- Async processing dominates
- Complex state machines
- Multiple consumers per event

**CQRS + Event Sourcing:**
- Complex business logic with audit trail
- Time-travel queries needed
- Multiple read models required
- High write throughput with eventual consistency acceptable

**Service Mesh:**
- 20+ microservices
- Complex retry/circuit breaker logic
- Observability across services critical
- mTLS required everywhere

## Key Metrics & SLA Definitions

### Performance Targets
```
Latency:
- P50: <100ms (median)
- P95: <500ms (95th percentile)
- P99: <1000ms (99th percentile)

Throughput:
- Requests per second (RPS)
- Transactions per second (TPS)
- Concurrent users

Database:
- Query execution time
- Connection pool utilization
- Replication lag
```

### Availability & Reliability
```
SLA Tiers:
- 99.9% ("three nines"): 43.2 min downtime/month
- 99.95%: 21.6 min downtime/month
- 99.99% ("four nines"): 4.3 min downtime/month
- 99.999% ("five nines"): 26 sec downtime/month

Disaster Recovery:
- RPO (Recovery Point Objective): Max data loss acceptable
- RTO (Recovery Time Objective): Max downtime acceptable
```

### Scalability Metrics
```
Horizontal Scalability:
- Linear scaling factor (e.g., 2x servers = 1.8x throughput)
- Auto-scaling trigger thresholds

Vertical Scalability:
- CPU/memory utilization targets
- Database connection limits
```

## Reference Documentation

For detailed methodologies and templates:

- **[Requirements Engineering](references/requirements-engineering.md)** - User stories, acceptance criteria, use cases
- **[Architecture Patterns](references/architecture-patterns.md)** - Microservices, EDA, CQRS, DDD deep dives
- **[Data Modeling](references/data-modeling.md)** - ERD design, normalization, denormalization strategies
- **[Security Architecture](references/security-architecture.md)** - OAuth2, JWT, zero-trust, encryption best practices
- **[Cost Optimization](references/cost-optimization.md)** - Cloud cost strategies, reserved instances, spot instances
- **[Scalability Patterns](references/scalability-patterns.md)** - Caching, sharding, load balancing deep dives
- **[AI/ML System Design](references/ai-ml-system-design.md)** - ML pipelines, feature stores, model serving
- **[AI in EMS Manufacturing](references/ai-ems-manufacturing.md)** - Computer vision inspection, predictive maintenance, smart factory systems

## Templates & Assets

Available in `assets/`:
- System Requirements Document template (Markdown + Mermaid diagrams)
- Functional Specification Document template (Markdown + Mermaid diagrams)
- System Architecture Document template
- API Specification template (OpenAPI 3.0)
- Cost & Capacity Planning spreadsheet
- Architecture Decision Record (ADR) template
- C4 Model diagram templates (Mermaid)

## Scripts & Automation

Available in `scripts/`:
- `generate_srd.py` - Auto-generate SRD skeleton from interview notes
- `validate_openapi.py` - Validate OpenAPI 3.0 specifications
- `cost_calculator.py` - Calculate infrastructure costs across cloud providers
- `diagram_generator.py` - Generate architecture diagrams from YAML configs

## Best Practices

1. **Start with Business Value** - Every technical decision must trace back to business outcomes
2. **Design for Failure** - Assume components will fail; design resilience from day one
3. **Measure Everything** - Instrument from the start; observability is not optional
4. **Document Decisions** - Use ADRs to capture why, not just what
5. **Cost-Aware Design** - Every architecture decision has cost implications
6. **Security by Design** - Security is not a feature to add later
7. **Iterative Approach** - Don't over-engineer; validate with MVPs
8. **Vertical Slice Testing** - Test full user journeys end-to-end early

## Common Pitfalls to Avoid

1. **Premature Microservices** - Start monolithic, split when team/domain boundaries clear
2. **Over-Engineering** - Don't build for 1M users when you have 100
3. **Technology Hype** - Choose proven tech over bleeding edge
4. **Ignoring Data Gravity** - Data locality & transfer costs matter at scale
5. **Underestimating Observability** - Logs, metrics, traces from day one
6. **Skipping Load Testing** - Performance under load reveals hidden issues
7. **Poor API Versioning** - Breaking changes destroy integrations

## Example Use Cases

### Unicorn Startup Scenarios

**AI/ML Platform (OpenAI scale):**
- Multi-tenant LLM serving (isolation, rate limiting, cost tracking)
- Real-time model inference with sub-100ms latency
- Vector database for 10B+ embeddings
- Fine-tuning pipelines for enterprise customers
- Usage-based billing & quota enforcement

**Electric Vehicle Platform (Tesla scale):**
- Real-time vehicle telemetry (millions of cars, 1Hz updates)
- Over-the-air firmware updates (delta patches, rollback safety)
- Fleet management & analytics
- Autonomous driving data pipeline (PB-scale)
- Predictive maintenance models

**E-commerce Platform (Shopify scale):**
- Multi-tenant SaaS (isolation, custom domains, white-label)
- Real-time inventory synchronization
- Payment gateway integrations (global)
- Search & recommendation engine (ML-powered)
- Fraud detection (real-time scoring)

**Social Media Platform (Twitter scale):**
- Real-time feed generation (personalized, <100ms)
- Graph database for social connections
- Content moderation (ML + human review)
- Real-time analytics & trending topics
- Media processing pipeline (images, videos)

---

**Implementation Philosophy:** Super senior system analysts don't just design systems—they architect the future. Every decision balances business value, technical feasibility, scalability, security, and cost. The best architectures are simple, evolvable, and defensible with data.
