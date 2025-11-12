# System Analyst Expert - Super Senior Level

**Enterprise system analysis for unicorn-scale platforms with deep AI/ML and EMS manufacturing expertise.**

## 🎯 What This Skill Provides

Transform Claude into a super senior system analyst capable of:

1. **Enterprise System Design**
   - Distributed systems architecture (microservices, event-driven, CQRS)
   - Multi-tenant SaaS platforms
   - Real-time data processing pipelines
   - Hyper-scale infrastructure (millions of users)

2. **AI/ML System Integration**
   - ML pipeline architecture (training, serving, monitoring)
   - LLM application patterns (RAG, agents, fine-tuning)
   - Computer vision systems for manufacturing
   - Real-time inference optimization

3. **AI in EMS Manufacturing** ⭐
   - Computer vision for PCB quality inspection
   - Complete pipeline: labeling → training → production deployment
   - AOI (Automated Optical Inspection) machine integration
   - Defect detection systems (YOLOv8, edge deployment)
   - MES integration & production monitoring

4. **Comprehensive Documentation**
   - System Requirements Documents (SRD)
   - System Architecture Documents (SAD)
   - API specifications (OpenAPI 3.0)
   - Cost & capacity planning
   - Architecture Decision Records (ADRs)

## 📁 Skill Structure

```
System_Analyst_Expert/
├── SKILL.md                        # Main skill documentation
├── references/
│   ├── architecture-patterns.md   # Microservices, EDA, CQRS, DDD
│   ├── ai-ems-manufacturing.md    # Computer vision for PCB inspection ⭐
│   ├── requirements-engineering.md # User stories, acceptance criteria
│   ├── data-modeling.md           # ERD, normalization, indexing
│   ├── security-architecture.md   # OAuth2, JWT, encryption
│   ├── cost-optimization.md       # Cloud cost strategies
│   └── scalability-patterns.md    # Caching, sharding, load balancing
├── assets/templates/
│   ├── srd_template.md            # System Requirements Document
│   ├── fsd_template.md            # Functional Specification Document ⭐
│   ├── sad_template.md            # System Architecture Document
│   ├── adr_template.md            # Architecture Decision Record
│   └── openapi_template.yaml      # API Specification
└── scripts/
    ├── generate_srd.py            # Auto-generate SRD skeleton
    ├── validate_openapi.py        # Validate API specs
    ├── cost_calculator.py         # Infrastructure cost calculator
    └── diagram_generator.py       # Architecture diagram generator
```

## 🚀 Quick Start

### Use Case 1: Enterprise System Design
```
Design a multi-tenant SaaS platform for 1M+ users with real-time collaboration,
supporting microservices architecture with event-driven communication.
```

Claude will:
- Analyze requirements (functional, non-functional, constraints)
- Design architecture (microservices, API gateway, event bus)
- Create data architecture (database selection, caching, replication)
- Document security architecture (OAuth2, JWT, encryption)
- Produce System Requirements Document (SRD)
- Produce System Architecture Document (SAD)

### Use Case 2: AI-Powered PCB Inspection System ⭐
```
Design an AI-powered AOI system for PCB defect detection in EMS manufacturing.
Requirements:
- Real-time inspection (<2 sec per board)
- 99.5%+ defect capture rate
- Computer vision with YOLOv8
- Edge deployment on NVIDIA Jetson
- MES integration for traceability
```

Claude will:
- Design complete computer vision pipeline
- Specify data collection & labeling workflow (CVAT, Roboflow)
- Define training pipeline (YOLOv8, hyperparameters, augmentation)
- Plan edge deployment architecture (TensorRT, Jetson Orin)
- Design MES integration (REST API, MQTT, dashboards)
- Create cost analysis (cameras, compute, labeling)
- Produce comprehensive technical specifications

**Deep Expertise in:**
- PCB defect types (solder joints, component placement, polarity)
- Labeling tools & strategies (CVAT, quality control)
- YOLOv8 training for manufacturing (augmentation, optimization)
- Production deployment (AOI machines, camera integration)
- Model maintenance (drift detection, retraining triggers)

### Use Case 3: AI/ML Platform Architecture
```
Design ML training and serving infrastructure for an AI company
handling 10M+ API requests/day with real-time inference.
```

Claude will:
- Design ML pipeline (feature store, training, serving)
- Plan infrastructure (Kubernetes, GPU clusters, auto-scaling)
- Design monitoring & observability (MLflow, Prometheus, Grafana)
- Create cost optimization strategy (spot instances, model caching)
- Document MLOps workflows (CI/CD, A/B testing, rollback)

## 🎓 When to Use This Skill

**Trigger Phrases:**
- "Design a system for..."
- "Analyze the architecture of..."
- "Create system requirements for..."
- "Design AI-powered inspection system..."
- "PCB defect detection pipeline..."
- "AOI machine integration..."
- "Computer vision for manufacturing..."
- "YOLOv8 training for production..."

**Use When:**
- Designing enterprise-scale systems (100K+ users)
- Planning AI/ML infrastructure
- Architecting real-time data pipelines
- Evaluating technical feasibility
- Creating comprehensive documentation (SRD, SAD)
- **Designing computer vision systems for manufacturing**
- **Planning PCB inspection AI pipelines**
- **Integrating AI with AOI machines**

## 📊 Deliverables

### Standard Documents
1. **System Requirements Document (SRD)**
   - Executive summary
   - Functional requirements (user stories, use cases)
   - Non-functional requirements (performance, scalability, security)
   - Constraints (budget, timeline, technology)

2. **Functional Specification Document (FSD)** ⭐
   - Detailed user workflows (screen-by-screen)
   - Business rules & calculation logic
   - Data specifications (schemas, validations, transformations)
   - API contracts (request/response with examples)
   - Error handling & edge cases
   - Test scenarios (positive, negative, edge cases)

3. **System Architecture Document (SAD)**
   - Architecture overview (diagrams, tech stack)
   - Component design (services, APIs, data models)
   - Infrastructure design (cloud, network, DR)
   - Integration design (APIs, events, webhooks)

3. **API Specification**
   - OpenAPI 3.0 specification
   - Authentication & authorization flows
   - Rate limiting & error handling
   - Versioning strategy

4. **Cost & Capacity Planning**
   - Infrastructure costs (compute, storage, network)
   - Scaling analysis (growth projections, breaking points)
   - TCO analysis (CapEx vs OpEx, build vs buy)

### AI/EMS Specific Deliverables
1. **Computer Vision Pipeline Design**
   - Data collection strategy (cameras, lighting, image specs)
   - Labeling workflow (tools, team structure, quality control)
   - Training pipeline (model selection, hyperparameters, augmentation)
   - Validation strategy (metrics, test sets, production validation)

2. **AOI System Specifications**
   - Edge deployment architecture (hardware, software stack)
   - Camera integration (GigE Vision, GenICam)
   - Real-time inference pipeline (<50ms latency)
   - MES integration (APIs, data flow, dashboards)

3. **Production Implementation Plan**
   - Phase 1: Proof of concept (labeling 1K images, baseline model)
   - Phase 2: Production pilot (10K images, optimized model, 1 AOI machine)
   - Phase 3: Full deployment (all AOI machines, continuous learning)
   - Success metrics (DCR, FCR, FPY, cost savings)

## 🏭 Deep Dive: AI in EMS Manufacturing

This skill includes **extensive expertise in Computer Vision for PCB inspection**, covering the complete pipeline from labeling to production deployment.

### Coverage Areas

**1. PCB Defect Detection**
- 20+ defect types (solder joints, component placement, polarity, contamination)
- Visual characteristics & detection strategies
- Industry-standard acceptance criteria

**2. Data Collection & Labeling**
- Camera setup (5MP+ industrial cameras, LED lighting, positioning)
- Labeling tools comparison (CVAT, Roboflow, LabelImg)
- Annotation guidelines (tight boxing, multi-defect handling, edge cases)
- Team structure (annotators, QA, workflow)
- Quality control (inter-annotator agreement, expert review)

**3. Model Training Pipeline**
- YOLOv8 for real-time inspection (model variants, hardware requirements)
- Dataset preparation (YOLO format, data.yaml, augmentation)
- Hyperparameter tuning (learning rate, batch size, augmentation config)
- Training monitoring (TensorBoard, loss curves, mAP progression)
- Model optimization (quantization INT8, pruning, TensorRT)

**4. Production Deployment**
- Edge deployment (NVIDIA Jetson Orin, Intel NUC, industrial PCs)
- Inference server (Flask API, <50ms latency)
- Camera integration (GenICam, GigE Vision drivers)
- Production workflow (main inspection loop, GPIO signals, barcode scanning)
- MES integration (REST API, MQTT, real-time dashboards)

**5. Model Maintenance**
- Drift detection (Kolmogorov-Smirnov test, confidence distribution)
- Retraining triggers (monthly, performance degradation, new products)
- Continuous improvement (production feedback loop)

**6. Success Metrics**
- Technical: mAP@0.5 >90%, inference <50ms, DCR >99%, FCR <5%
- Business: labor reduction 80%, rework cost -70%, yield +3-5%

### Real-World Example

```
Project: AI-Powered AOI System for Smartphone PCB Assembly

Requirements:
- Inspect 500 boards/hour (2 sec per board including conveyor movement)
- Detect 15 defect types with >99% recall on critical defects
- Reduce false call rate from 18% (traditional AOI) to <5%
- Edge deployment on existing AOI machines (upgrade, not replace)
- Full traceability with defect image storage

Solution:
- Camera: 5MP Basler (GigE) with 4-zone LED ring light
- Dataset: 15K labeled images (10K train, 3K val, 2K test)
- Model: YOLOv8s fine-tuned, quantized to INT8 TensorRT
- Hardware: NVIDIA Jetson Orin Nano (8GB) per AOI machine
- Inference: 35ms average, 640x640 input resolution
- Deployment: 12 AOI machines on SMT line
- MES: REST API integration for real-time statistics

Results (vs Traditional AOI):
- Defect Capture Rate: 99.3% (vs 87%)
- False Call Rate: 4.2% (vs 18%)
- Inspection Speed: 1.8 sec/board (vs 3.5 sec)
- First Pass Yield: +4.7 percentage points
- Rework Cost: -$120K/year per line
- ROI: 8 months payback period
```

## 🔧 Tools & Technologies

**Supported Platforms:**
- Cloud: AWS, GCP, Azure
- Containers: Docker, Kubernetes
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- Message Queues: Kafka, RabbitMQ, Pulsar
- ML Frameworks: PyTorch, TensorFlow, YOLOv8
- **Computer Vision:** YOLOv8, OpenCV, TensorRT, ONNX
- **Edge Hardware:** NVIDIA Jetson, Intel NUC, Coral TPU
- **Labeling Tools:** CVAT, Roboflow, LabelImg
- **AOI Integration:** GenICam, GigE Vision, industrial cameras

## 📈 Example Workflows

### Workflow 1: Design Microservices Architecture
```
User: "Design a microservices architecture for an e-commerce platform
      handling 1M daily orders with real-time inventory synchronization."

Claude:
1. Analyzes requirements (functional, non-functional, constraints)
2. Designs service decomposition (Order, Payment, Inventory, Shipping)
3. Selects communication patterns (REST for sync, Kafka for async)
4. Designs data architecture (PostgreSQL per service, Redis caching)
5. Creates API specifications (OpenAPI 3.0)
6. Documents infrastructure (Kubernetes, load balancers, auto-scaling)
7. Produces complete SRD + SAD documents
```

### Workflow 2: Computer Vision for PCB Inspection ⭐
```
User: "I need an AI system to detect solder defects on PCBs in real-time
      during SMT production. We have 4 AOI machines processing 300 boards/hour."

Claude:
1. Analyzes defect types (insufficient solder, bridges, cold joints, etc)
2. Designs data collection (5MP cameras, lighting, 20K images needed)
3. Plans labeling workflow (CVAT, 10 annotators, 2 weeks timeline)
4. Specifies training pipeline (YOLOv8s, TensorRT INT8 optimization)
5. Designs edge deployment (Jetson Orin per AOI machine)
6. Creates camera integration code (GenICam, real-time capture)
7. Plans MES integration (REST API, inspection results, dashboards)
8. Calculates ROI (labeling cost, hardware cost, labor savings)
9. Produces complete technical specification with code samples
```

### Workflow 3: ML Platform Design
```
User: "Design ML infrastructure for training and serving 100+ models
      with 10M API requests per day and A/B testing capabilities."

Claude:
1. Designs ML pipeline (feature store, training cluster, serving)
2. Selects infrastructure (Kubernetes, GPU nodes, auto-scaling)
3. Plans experiment tracking (MLflow, model registry, versioning)
4. Designs serving architecture (TensorFlow Serving, load balancing)
5. Creates A/B testing framework (traffic splitting, metrics collection)
6. Documents monitoring (Prometheus, Grafana, alerting)
7. Estimates costs (GPU instances, storage, network egress)
8. Produces MLOps workflows (CI/CD, deployment, rollback)
```

## 💡 Pro Tips

1. **Start with Business Value**
   - Every technical decision must trace back to business outcomes
   - Quantify impact: cost savings, revenue increase, risk reduction

2. **Design for Failure**
   - Assume components will fail
   - Implement circuit breakers, retries, fallbacks
   - Plan disaster recovery from day one

3. **Measure Everything**
   - Instrument services with metrics (latency, throughput, errors)
   - Observability is not optional at scale

4. **Iterate with MVPs**
   - Don't over-engineer for future scale
   - Validate with minimum viable product first
   - Scale based on actual data, not assumptions

5. **For AI/Manufacturing Projects:**
   - Start with small pilot (1 AOI machine, 1 product)
   - Validate labeling quality before large-scale annotation
   - Test in production with fallback to manual inspection
   - Measure business impact (DCR, FCR, cost savings)

## 📚 Reference Documents

Comprehensive deep dives available in `references/`:

- **[Architecture Patterns](references/architecture-patterns.md)** - Microservices, EDA, CQRS, DDD, Service Mesh, Saga patterns (300 lines)
- **[AI in EMS Manufacturing](references/ai-ems-manufacturing.md)** - Complete computer vision pipeline for PCB inspection ⭐⭐⭐ (1,200 lines)
- **[Requirements Engineering](references/requirements-engineering.md)** - User stories, acceptance criteria, use cases, validation (400 lines)
- **[Data Modeling](references/data-modeling.md)** - ERD design, normalization, indexing, optimization (350 lines)
- **[Security Architecture](references/security-architecture.md)** - OAuth2, JWT, zero-trust, encryption, compliance (300 lines)
- **[Cost Optimization](references/cost-optimization.md)** - Cloud cost strategies, reserved instances, FinOps (280 lines)
- **[Scalability Patterns](references/scalability-patterns.md)** - Caching, sharding, load balancing, auto-scaling (350 lines)

**Templates in `assets/templates/`:**
- **srd_template.md** - System Requirements Document template
- **fsd_template.md** - Functional Specification Document template ⭐ (700 lines with examples)
- **sad_template.md** - System Architecture Document template
- **adr_template.md** - Architecture Decision Record template
- **openapi_template.yaml** - API Specification template

## 🎯 Success Metrics

**For Enterprise Systems:**
- Architecture clarity: All stakeholders understand design
- Feasibility validated: POC demonstrates critical paths
- Cost predictable: TCO within 10% of estimates
- Timeline realistic: Roadmap accounts for dependencies

**For AI/Manufacturing Projects:**
- Defect Capture Rate: >99% (critical defects)
- False Call Rate: <5% (vs 15-20% traditional)
- Inspection Speed: <2 seconds per board
- ROI: <12 months payback period
- Model deployed to production successfully

## 🤝 Complementary Skills

Works well with:
- **AI_Engineer_Pro** - For implementing ML models and pipelines
- **Web_Architect_Pro** - For web-based dashboards and APIs
- **CTA_Orchestrator** - For coordinating multiple technical domains
- **DevOps_Master** - For infrastructure automation and CI/CD

## 📄 License

MIT License - Part of claude-capabilities-skills collection

---

**Version:** 1.0.0  
**Last Updated:** January 12, 2025  
**Author:** Ali Sadikin MA  
**Status:** ✅ Production Ready (with emphasis on AI/EMS Manufacturing)
