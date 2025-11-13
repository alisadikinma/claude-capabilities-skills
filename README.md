# SKILLS-CLAUDE

**Professional AI Development Skills for Claude Code**

A curated collection of specialized skills that transform Claude from a general-purpose AI into domain-specific experts. Each skill provides comprehensive workflows, templates, references, and automation scripts for production-grade development.

---

## 📦 Available Skills

| Skill | Status | Files | Coverage |
|-------|--------|-------|----------|
| **CTA_Orchestrator** | ✅ Complete | 18 | Meta-layer coordination & architecture decisions |
| **Web_Architect_Pro** | ✅ Complete | 46 | Full-stack web development (React, Next.js, Laravel, FastAPI) |
| **AI_Engineer_Pro** | ✅ Complete | 26 | AI/ML training, CV, NLP, deployment, vector databases |
| **ML_Systems_Pro** | ✅ Complete | 15 | Multi-modal ML, similarity engines, production MLOps |
| **System_Analyst_Expert** | ✅ Complete | 18 | Requirements, FSD, documentation, validation, AI in EMS |
| **Mobile_Architect_Pro** | ✅ Complete | 25 | Flutter, React Native, Xamarin, Ionic, Kotlin, native integration |
| **DevOps_Master** | ⏳ Planned | ~20 | Docker, Kubernetes, CI/CD, infrastructure as code |

**Progress:** 6 of 7 skills (86%) • **Total Files:** 148

---

## 🎯 What Are Skills?

Skills are modular, self-contained packages that provide:

1. **Specialized Workflows** - Multi-step procedures for specific domains
2. **Production Templates** - Ready-to-use code scaffolding and configurations
3. **Best Practices** - Industry-standard patterns and guidelines
4. **Automation Scripts** - Python tools for repetitive tasks
5. **Comprehensive References** - Deep-dive documentation and troubleshooting

Think of them as **expert knowledge modules** that Claude loads on-demand.

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/alisadikinma/claude-capabilities-skills.git
cd SKILLS-CLAUDE

# Skills are ready to use - no installation needed
# Each skill is self-contained in its directory
```

### Using a Skill

**Option 1: Direct Reference**
```
Hey Claude, use the Mobile_Architect_Pro skill to help me build a Flutter app with BLoC pattern
```

**Option 2: Read Skill Documentation**
```
Read D:\Projects\SKILLS-CLAUDE\Mobile_Architect_Pro\SKILL.md and help me choose between Flutter and React Native
```

**Option 3: Browse Templates**
```
Show me available templates in Mobile_Architect_Pro for Flutter projects
```

---

## 📁 Repository Structure

```
SKILLS-CLAUDE/
├── README.md                          # This file
├── project_status.md                  # Detailed project tracking
│
├── CTA_Orchestrator/                  # Meta-coordination skill
│   ├── README.md
│   ├── SKILL.md
│   ├── assets/
│   ├── references/
│   └── scripts/
│
├── Web_Architect_Pro/                 # Full-stack web development
│   ├── README.md
│   ├── SKILL.md
│   ├── assets/templates/
│   │   ├── Frontend/
│   │   ├── Backend/
│   │   ├── Databases/
│   │   └── Testing/
│   ├── references/
│   └── scripts/
│
├── AI_Engineer_Pro/                   # AI/ML engineering
│   ├── README.md
│   ├── SKILL.md
│   ├── assets/templates/
│   │   ├── Training/
│   │   ├── ComputerVision/
│   │   ├── NLP/
│   │   ├── Deployment/
│   │   └── VectorDatabases/
│   ├── references/
│   └── scripts/
│
├── Mobile_Architect_Pro/              # Cross-platform mobile development
│   ├── README.md
│   ├── SKILL.md
│   ├── assets/templates/
│   │   └── TEMPLATES.md (Flutter, RN, Xamarin, Ionic, Kotlin)
│   ├── references/
│   │   ├── flutter.md
│   │   ├── react-native.md
│   │   ├── xamarin.md
│   │   ├── ionic.md
│   │   └── kotlin.md
│   └── scripts/
│       ├── analyze_deps.py
│       └── scaffold.py
│
└── [Additional skills...]
```

### Skill Structure

Each skill follows this pattern:

```
skill-name/
├── README.md              # Skill overview and quick start
├── SKILL.md               # Main skill documentation (loaded by Claude)
├── assets/                # Output-ready files
│   └── templates/         # Code scaffolding and configs
├── references/            # Deep documentation (loaded as needed)
│   └── checklists/        # Verification checklists
└── scripts/               # Automation tools (Python/Bash)
```

---

## 💡 Use Cases

### 🎨 Web Development
```
"Create a Next.js 14 app with TypeScript, Tailwind, and Prisma using Web_Architect_Pro"
```
→ Generates complete project structure with best practices

### 🤖 AI/ML Engineering
```
"Set up YOLOv8 training pipeline for PCB defect detection using AI_Engineer_Pro"
```
→ Provides training code, augmentation, MLflow tracking, and deployment

### 🏗️ System Architecture
```
"Design microservices architecture for e-commerce platform using CTA_Orchestrator"
```
→ Analyzes requirements, recommends tech stack, creates integration blueprints

### 📱 Mobile Development
```
"Build Flutter app with BLoC pattern and offline-first architecture using Mobile_Architect_Pro"
```
→ Complete Flutter project with state management, data persistence, and platform integration

### 🔬 Production ML Systems
```
"Build a multi-modal image-text search engine using ML_Systems_Pro"
```
→ CLIP-based architecture, vector search, production deployment

### 📋 System Analysis
```
"Generate comprehensive FSD for inventory management system using System_Analyst_Expert"
```
→ Complete functional specification with ERD, API specs, and acceptance criteria

---

## 🔧 Available Templates

### Web Development
- **Frontend:** Next.js, React, Vue.js
- **Backend:** Express, NestJS, Fastify, FastAPI, Django, Laravel
- **Databases:** PostgreSQL, MySQL, MongoDB, Prisma
- **Testing:** Jest, Vitest, Playwright, Cypress, pytest

### AI/ML Engineering
- **Training:** PyTorch, TensorFlow, MLflow
- **Computer Vision:** YOLOv8, object detection, classification
- **NLP:** HuggingFace transformers, LLM fine-tuning, RAG
- **Deployment:** FastAPI, Triton Inference Server, ONNX
- **Vector DBs:** pgvector, Pinecone, ChromaDB, Supabase

### Mobile Development
- **Flutter:** BLoC, Provider, Riverpod architectures
- **React Native:** Redux Toolkit, Context API, native modules
- **Xamarin/MAUI:** MVVM, Prism, .NET MAUI
- **Ionic:** Angular/React/Vue with Capacitor
- **Kotlin:** Jetpack Compose, Clean Architecture, Hilt DI

### ML Systems
- **Multi-Modal:** CLIP search, fusion pipelines, cross-modal retrieval
- **Similarity:** Embedding generation, hybrid search, recommendations
- **MLOps:** Feature stores, monitoring, CI/CD pipelines

### System Analysis
- **Documents:** SRD, FSD, SAD, ADR, OpenAPI specs
- **AI/Manufacturing:** Computer vision for PCB inspection
- **Architecture:** Microservices, event-driven, CQRS, DDD

### DevOps (Coming Soon)
- Docker, Kubernetes, Terraform
- CI/CD pipelines (GitLab, GitHub Actions)
- Monitoring (Prometheus, Grafana)

---

## 📊 Skill Comparison

| Need | Use This Skill |
|------|----------------|
| Coordinate multiple skills | CTA_Orchestrator |
| Build web applications | Web_Architect_Pro |
| Train ML models | AI_Engineer_Pro |
| Build production ML systems | ML_Systems_Pro |
| Write specifications & requirements | System_Analyst_Expert |
| Mobile app development | Mobile_Architect_Pro |
| Infrastructure & deployment | DevOps_Master |

---

## 🎓 Learning Path

**Beginner:**
1. Start with Web_Architect_Pro (familiar territory)
2. Use templates to understand patterns
3. Explore references for deep dives

**Intermediate:**
1. Combine skills (Web + AI_Engineer_Pro)
2. Build mobile apps with Mobile_Architect_Pro
3. Use automation scripts

**Advanced:**
1. Leverage CTA_Orchestrator for complex systems
2. Integrate ML_Systems_Pro for production ML
3. Build end-to-end solutions with multiple skills

---

## 📝 Documentation

- **[Project Status](project_status.md)** - Detailed tracking and roadmap
- **Individual Skill READMEs** - Quick start for each skill
- **SKILL.md Files** - Comprehensive skill documentation
- **Reference Docs** - Deep-dive guides and best practices

---

## 🤝 Contributing

Skills are designed for:
- **Developers** building production systems
- **Teams** standardizing workflows
- **Companies** scaling AI development

**Feedback Welcome:**
- Found a bug? Open an issue
- Have a suggestion? Submit a PR
- Need a new skill? Propose it in discussions

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Ali Sadikin MA**
- UN-UNCTAD Alibaba Fellow | Google Certified PM | AI Project Manager
- AI Generalist • 17+ years experience
- Portfolio: www.alisadikinma.com
- Location: Batam, Indonesia

---

## 🔗 Quick Links

- [Project Status](project_status.md)
- [CTA_Orchestrator](CTA_Orchestrator/README.md)
- [Web_Architect_Pro](Web_Architect_Pro/README.md)
- [AI_Engineer_Pro](AI_Engineer_Pro/README.md)
- [ML_Systems_Pro](ML_Systems_Pro/README.md)
- [System_Analyst_Expert](System_Analyst_Expert/README.md)
- [Mobile_Architect_Pro](Mobile_Architect_Pro/README.md)

---

**Last Updated:** January 13, 2025  
**Version:** 1.1.0  
**Status:** 🟢 Active Development (6/7 skills complete, 86%)
