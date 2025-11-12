---
name: AI_Engineer_Pro
description: Comprehensive AI/ML engineering skill for training, deployment, and optimization of machine learning models. Use when Claude needs to work with: (1) PyTorch or TensorFlow training pipelines, (2) Computer vision tasks (object detection, image classification, PCB defect inspection), (3) NLP/LLM fine-tuning and inference, (4) RAG systems and vector databases (pgvector, Pinecone, ChromaDB), (5) Model deployment (FastAPI, Triton Inference Server, ONNX), (6) Model optimization and inference acceleration, (7) MLOps workflows and experiment tracking
---

# AI Engineer Pro

Comprehensive AI/ML engineering skill covering model training, computer vision, NLP, deployment, and production optimization.

## Core Capabilities

### 1. Training Pipelines
- PyTorch and TensorFlow workflows
- Distributed training strategies
- Hyperparameter optimization
- Experiment tracking with MLflow/W&B

### 2. Computer Vision
- Object detection (YOLOv8, Faster R-CNN)
- Image classification and segmentation
- PCB defect inspection systems
- Custom dataset preparation

### 3. Natural Language Processing
- LLM fine-tuning (LoRA, QLoRA)
- Transformer models with HuggingFace
- Text generation and classification
- RAG (Retrieval-Augmented Generation) systems

### 4. Model Deployment
- FastAPI model serving
- ONNX optimization and conversion
- Triton Inference Server setup
- Batch and real-time inference

### 5. Vector Databases
- pgvector (PostgreSQL extension)
- Pinecone cloud vector DB
- ChromaDB local/embedded DB
- Embedding generation and indexing

## Quick Start Templates

### Training Setup
For model training pipelines, see:
- `assets/templates/Training/pytorch-training-pipeline.py` - Complete PyTorch training loop
- `assets/templates/Training/tensorflow-training-pipeline.py` - TensorFlow/Keras training
- `assets/templates/Training/mlflow-experiment-setup.md` - Experiment tracking

### Computer Vision
For vision tasks, see:
- `assets/templates/ComputerVision/yolov8-detection-setup.md` - YOLOv8 object detection
- `assets/templates/ComputerVision/object-detection-pipeline.py` - End-to-end detection pipeline
- `assets/templates/ComputerVision/image-classification-setup.md` - Classification workflows

### NLP & LLMs
For language tasks, see:
- `assets/templates/NLP/huggingface-finetuning.py` - Fine-tune transformers
- `assets/templates/NLP/llm-inference-setup.md` - LLM inference optimization
- `assets/templates/NLP/rag-pipeline-setup.md` - RAG system implementation

### Deployment
For production deployment, see:
- `assets/templates/Deployment/fastapi-model-serving.py` - FastAPI REST API
- `assets/templates/Deployment/triton-inference-server.md` - Triton setup
- `assets/templates/Deployment/onnx-optimization-guide.md` - ONNX conversion

### Vector Databases
For similarity search, see:
- `assets/templates/VectorDatabases/pgvector-setup.md` - PostgreSQL with pgvector
- `assets/templates/VectorDatabases/pinecone-integration.py` - Pinecone cloud setup
- `assets/templates/VectorDatabases/chromadb-setup.md` - ChromaDB local usage

## References

### Best Practices
- `references/best-practices.md` - Model development guidelines
- `references/model-optimization-guide.md` - Performance tuning strategies
- `references/hardware-acceleration.md` - GPU/TPU optimization

### MLOps
- `references/mlops-patterns.md` - Production ML workflows
- `references/checklists/training-checklist.md` - Pre-training verification
- `references/checklists/deployment-checklist.md` - Production readiness

## Scripts

### Utilities
- `scripts/model_profiler.py` - Analyze model performance and bottlenecks
- `scripts/inference_benchmarker.py` - Measure inference latency and throughput
- `scripts/dataset_validator.py` - Validate training data quality

## Common Workflows

### Object Detection for PCB Inspection

1. **Prepare dataset**: Annotate PCB images with defects (scratches, cracks, missing components)
2. **Choose model**: YOLOv8 for real-time detection or Faster R-CNN for higher accuracy
3. **Train**: Use `pytorch-training-pipeline.py` with custom dataset
4. **Optimize**: Convert to ONNX for faster inference
5. **Deploy**: Serve via FastAPI for REST API access

See `assets/templates/ComputerVision/yolov8-detection-setup.md` for complete guide.

### RAG System for Document QA

1. **Embedding generation**: Use sentence-transformers for document chunks
2. **Vector storage**: Store in pgvector or Pinecone
3. **Retrieval**: Query similar documents using cosine similarity
4. **Generation**: Feed context to LLM for answer synthesis

See `assets/templates/NLP/rag-pipeline-setup.md` for implementation details.

### Model Deployment to Production

1. **Optimize**: Convert to ONNX or TorchScript
2. **API**: Wrap in FastAPI with input validation
3. **Scale**: Deploy with Triton for multi-model serving
4. **Monitor**: Track latency, throughput, and accuracy

See `assets/templates/Deployment/fastapi-model-serving.py` for starter code.

## Hardware Considerations

### GPU Acceleration
- **Training**: Use CUDA with PyTorch/TensorFlow
- **Inference**: FP16 or INT8 quantization for 2-4x speedup
- **Multi-GPU**: DistributedDataParallel for training

### Edge Deployment
- **Jetson Orin NX**: For PCB inspection systems
- **TensorRT**: Optimize models for NVIDIA devices
- **ONNX Runtime**: Cross-platform inference

See `references/hardware-acceleration.md` for detailed optimization strategies.

## Decision Trees

### Choose Training Framework
```
Need dynamic graphs or research flexibility? → PyTorch
Production deployment priority? → TensorFlow/Keras
Edge device deployment? → TensorFlow Lite or ONNX
```

### Choose Vector Database
```
Need SQL compatibility? → pgvector
Cloud-native with auto-scaling? → Pinecone
Local development or embedded? → ChromaDB
Multi-modal search? → Weaviate or Milvus
```

### Choose Deployment Strategy
```
Single model, low latency? → FastAPI + ONNX Runtime
Multiple models, high throughput? → Triton Inference Server
Serverless/auto-scaling? → AWS SageMaker or Google Vertex AI
Edge devices? → TensorRT or TF Lite
```

## Integration Patterns

### With Web Services
- Expose model via FastAPI REST endpoints
- Implement async processing for long-running inference
- Use Redis for result caching

### With Vector Databases
- Generate embeddings with sentence-transformers
- Store in pgvector/Pinecone with metadata filtering
- Implement hybrid search (semantic + keyword)

### With MLOps Platforms
- Track experiments with MLflow
- Version models with DVC or MLflow Model Registry
- Automate retraining pipelines with Airflow

## Troubleshooting

### Training Issues
**Symptom**: Training loss not decreasing
- Check learning rate (try 1e-4 to 1e-3)
- Verify data preprocessing and augmentation
- Inspect batch size (increase if GPU memory allows)

**Symptom**: Out of memory errors
- Reduce batch size
- Use gradient accumulation
- Enable mixed precision training (FP16)

### Inference Issues
**Symptom**: Slow inference time
- Convert model to ONNX
- Use quantization (INT8)
- Batch predictions when possible

**Symptom**: Poor accuracy in production
- Verify input preprocessing matches training
- Check for data drift
- Monitor prediction confidence scores

## Next Steps After Deployment

1. **Monitor**: Set up logging and metrics
2. **A/B Test**: Compare model versions
3. **Retrain**: Schedule periodic updates with new data
4. **Scale**: Add load balancing and auto-scaling

For production ML systems with multi-modal fusion and similarity engines, see the **ML_Systems_Pro** skill.
