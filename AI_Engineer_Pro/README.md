# AI_Engineer_Pro

**AI/ML Engineering from Training to Production**

Complete templates and workflows for PyTorch/TensorFlow training, computer vision, NLP, model deployment, and vector databases. Perfect for PCB inspection, RAG systems, and production ML.

---

## 🎯 Purpose

AI_Engineer_Pro provides:
- **Training pipelines** (PyTorch, TensorFlow, MLflow)
- **Computer vision** (YOLOv8, object detection, classification)
- **NLP/LLM** (HuggingFace fine-tuning, RAG, inference optimization)
- **Model deployment** (FastAPI, Triton Inference Server, ONNX)
- **Vector databases** (pgvector, Pinecone, ChromaDB, Supabase)
- **Production best practices** (optimization, monitoring, MLOps)

---

## 📦 What's Inside

```
AI_Engineer_Pro/
├── SKILL.md                          # Main documentation
├── assets/templates/
│   ├── Training/                     # 3 files
│   │   ├── pytorch-training-pipeline.py
│   │   ├── tensorflow-training-pipeline.py
│   │   └── mlflow-experiment-setup.md
│   ├── ComputerVision/               # 3 files
│   │   ├── yolov8-detection-setup.md
│   │   ├── object-detection-pipeline.py
│   │   └── image-classification-setup.md
│   ├── NLP/                          # 3 files
│   │   ├── huggingface-finetuning.py
│   │   ├── llm-inference-setup.md
│   │   └── rag-pipeline-setup.md
│   ├── Deployment/                   # 3 files
│   │   ├── fastapi-model-serving.py
│   │   ├── triton-inference-server.md
│   │   └── onnx-optimization-guide.md
│   └── VectorDatabases/              # 4 files
│       ├── pgvector-setup.md
│       ├── pinecone-integration.py
│       ├── chromadb-setup.md
│       └── supabase-vector-setup.md
├── references/
│   ├── best-practices.md
│   ├── model-optimization-guide.md
│   ├── hardware-acceleration.md
│   ├── mlops-patterns.md
│   └── checklists/
│       ├── training-checklist.md
│       └── deployment-checklist.md
└── scripts/
    ├── model_profiler.py
    ├── inference_benchmarker.py
    └── dataset_validator.py
```

**Total:** 26 files

---

## 🚀 Quick Start

### Train YOLOv8 for PCB Defect Detection

```
"Using AI_Engineer_Pro, set up YOLOv8 training for PCB defect detection with 5 classes: scratch, crack, missing, solder_bridge, misalignment"
```

**Output:**
- ✅ YOLOv8 training script
- ✅ Dataset format (YOLO)
- ✅ Data augmentation config
- ✅ MLflow experiment tracking
- ✅ Model evaluation metrics
- ✅ Export to ONNX

### Build RAG System

```
"Create a RAG pipeline for PCB documentation Q&A using ChromaDB and sentence-transformers"
```

**Output:**
- ✅ Document chunking & embedding
- ✅ ChromaDB setup
- ✅ Retrieval function
- ✅ LLM integration (GPT/local)
- ✅ End-to-end query pipeline

### Deploy Model API

```
"Deploy my trained model as a FastAPI service with batch processing"
```

**Output:**
- ✅ FastAPI app structure
- ✅ Model loading & caching
- ✅ Batch inference endpoint
- ✅ Input validation
- ✅ Dockerfile
- ✅ Health check endpoint

---

## 🎨 Core Capabilities

### 1. Training Pipelines

**PyTorch:**
- Complete training loop with mixed precision (FP16)
- Gradient clipping & learning rate scheduling
- Checkpointing & early stopping
- TensorBoard logging
- Distributed training (multi-GPU)

**TensorFlow/Keras:**
- tf.data pipeline optimization
- Data augmentation layers
- Transfer learning (ResNet, EfficientNet)
- Model callbacks (checkpointing, LR reduction)
- TFLite conversion for edge

**MLflow:**
- Experiment tracking
- Hyperparameter logging
- Model registry
- Artifact storage
- Run comparison

### 2. Computer Vision

**Object Detection (YOLOv8):**
- Dataset preparation (YOLO format)
- Training & fine-tuning
- Hyperparameter tuning
- TensorRT optimization
- FastAPI deployment

**Image Classification:**
- Transfer learning (ResNet, EfficientNet, ViT)
- Data augmentation
- Class imbalance handling
- Confusion matrix analysis

**Use Cases:**
- PCB defect inspection
- Component recognition
- Quality control
- Visual inspection systems

### 3. NLP & LLMs

**Fine-tuning:**
- HuggingFace transformers
- LoRA & QLoRA (parameter-efficient)
- Text classification
- Named entity recognition

**Inference Optimization:**
- vLLM (fastest)
- Text Generation Inference (TGI)
- ONNX Runtime
- 4-bit quantization

**RAG (Retrieval-Augmented Generation):**
- Document chunking strategies
- Embedding generation
- Vector store integration
- Hybrid search (semantic + keyword)
- Context ranking

### 4. Model Deployment

**FastAPI:**
- REST API endpoints
- Async processing
- Batch inference
- Input validation
- Health checks
- Prometheus metrics

**Triton Inference Server:**
- Multi-model serving
- Dynamic batching
- GPU optimization
- Python backend support
- gRPC/HTTP protocols

**ONNX:**
- Model conversion (PyTorch/TF → ONNX)
- Quantization (INT8)
- Cross-platform deployment
- 2-3x speedup

### 5. Vector Databases

**pgvector (PostgreSQL):**
- SQL database integration
- Cosine/L2 distance search
- Metadata filtering with SQL
- ACID compliance

**Pinecone (Cloud):**
- Serverless, auto-scaling
- High performance (<50ms)
- Metadata filtering
- Namespaces for multi-tenancy

**ChromaDB (Local):**
- Embedded database
- Easy local development
- Multi-modal support
- Good for <100k vectors

**Supabase (pgvector):**
- Managed PostgreSQL
- Built-in auth & RLS
- Real-time subscriptions
- Free tier available

---

## 💡 Example Workflows

### PCB Defect Inspection System

**Requirements:**
- Detect 7 defect types
- Real-time inference (30 FPS)
- Deploy on Jetson Orin NX

**Implementation:**

**1. Data Preparation**
```python
python scripts/dataset_validator.py --path data/pcb_dataset
```

**2. Training**
```
Train YOLOv8m model:
- 640x640 resolution
- Augmentation: flip, rotate, contrast
- 100 epochs with early stopping
- MLflow tracking
```

**3. Optimization**
```
Export to ONNX → TensorRT
- INT8 quantization
- Target: <20ms latency
```

**4. Deployment**
```
FastAPI on Jetson:
- Batch size: 4
- Redis caching
- Prometheus monitoring
```

### Document Q&A with RAG

**Requirements:**
- Answer questions about PCB specifications
- Use internal documentation
- Update docs in real-time

**Implementation:**

**1. Document Processing**
```
- Load PDFs/Markdown
- Chunk: 500 tokens, 50 overlap
- Generate embeddings (all-MiniLM-L6-v2)
```

**2. Vector Store**
```
Use Supabase pgvector:
- Store embeddings + metadata
- Enable full-text search
- Row-level security
```

**3. RAG Pipeline**
```
Query → Embed → Search → Rank → Generate
- Retrieve top 3 chunks
- Re-rank with cross-encoder
- Generate with GPT-4/local LLM
```

**4. API**
```
FastAPI endpoints:
- /query (Q&A)
- /add_document (update KB)
- /search (semantic search)
```

---

## 📊 Decision Guide

### Choose Training Framework

```
Research & flexibility? → PyTorch
Production deployment? → TensorFlow
Edge devices? → TensorFlow Lite
```

### Choose Object Detection

```
Real-time (>30 FPS)? → YOLOv8
Highest accuracy? → Faster R-CNN
Edge devices? → YOLOv8 nano/small
```

### Choose Vector Database

```
SQL compatibility? → pgvector/Supabase
Cloud-native? → Pinecone
Local development? → ChromaDB
Multi-modal? → Weaviate
```

### Choose Deployment

```
Single model? → FastAPI + ONNX
Multiple models? → Triton Inference Server
Serverless? → AWS SageMaker
Edge? → TensorRT / TF Lite
```

---

## 🎯 Best Practices

### Training
- Start with pre-trained models
- Use 70/15/15 train/val/test split
- Enable mixed precision (FP16)
- Monitor validation loss
- Use early stopping (patience=10-20)

### Data
- Minimum 1000 samples per class
- Balance classes (augmentation if needed)
- Validate data quality
- Version datasets (DVC)

### Deployment
- Optimize models (ONNX/quantization)
- Target <100ms latency
- Implement health checks
- Monitor inference time
- Cache frequent predictions

### MLOps
- Track all experiments (MLflow)
- Version models
- A/B test before rollout
- Monitor data drift
- Schedule retraining

---

## 🔧 Automation Scripts

### Model Profiler
```bash
python scripts/model_profiler.py --model best.pt --input-shape 1,3,640,640
```
**Output:** FLOPs, params, memory, latency

### Inference Benchmarker
```bash
python scripts/inference_benchmarker.py --model best.pt --batch-sizes 1,2,4,8
```
**Output:** Latency vs batch size, throughput

### Dataset Validator
```bash
python scripts/dataset_validator.py --path data/pcb --format yolo
```
**Output:** Data quality report, issues found

---

## 📚 Key References

- **best-practices.md** - Model development guidelines
- **model-optimization-guide.md** - Quantization, pruning, distillation
- **hardware-acceleration.md** - GPU, TensorRT, edge deployment
- **mlops-patterns.md** - CI/CD, versioning, monitoring

---

## 🔗 Integration with Other Skills

**Works Well With:**
- **Web_Architect_Pro** - Add AI to web apps
- **ML_Systems_Pro** - Advanced multi-modal systems
- **DevOps_Master** - Model deployment & scaling
- **Mobile_Architect_Pro** - Edge AI on mobile

**Typical Flow:**
```
AI_Engineer_Pro (train model)
         ↓
ONNX optimization
         ↓
FastAPI deployment
         ↓
DevOps_Master (Kubernetes)
```

---

## 🎓 Learning Path

**Beginner:**
1. Start with image classification (transfer learning)
2. Use provided templates
3. Deploy with FastAPI

**Intermediate:**
1. Train object detection (YOLOv8)
2. Build RAG system
3. Optimize with ONNX

**Advanced:**
1. Multi-GPU training
2. Triton Inference Server
3. Production monitoring & retraining

---

## 📄 License

Part of SKILLS-CLAUDE project • MIT License

---

**Quick Links:**
- [Main README](../README.md)
- [SKILL.md](SKILL.md) - Full documentation
- [ML_Systems_Pro](../ML_Systems_Pro/README.md) - Advanced ML systems
- [Project Status](../project_status.md)
