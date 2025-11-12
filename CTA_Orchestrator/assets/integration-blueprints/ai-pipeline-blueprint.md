# AI/ML Pipeline Integration Blueprint

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      Client Layer                            │
│  (Web App / Mobile App / API Consumer)                       │
└───────────────────────────┬──────────────────────────────────┘
                            │
                 ┌──────────▼───────────┐
                 │    API Gateway       │
                 │  - Rate limiting     │
                 │  - Auth              │
                 │  - Load balancing    │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │  AI Inference API    │
                 │  (FastAPI)           │
                 │  - Request validation│
                 │  - Response format   │
                 └──────────┬───────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    ┌─────▼──────┐   ┌──────▼───────┐  ┌─────▼──────┐
    │Pre-process │   │  Model Serve │  │Post-process│
    │  Pipeline  │   │  (PyTorch/   │  │  Pipeline  │
    │  - Resize  │   │   ONNX)      │  │  - Format  │
    │  - Normalize│   │  - Inference │  │  - Filter  │
    └─────┬──────┘   └──────┬───────┘  └─────┬──────┘
          │                 │                 │
          │         ┌───────▼────────┐        │
          │         │  Model Cache   │        │
          │         │  (Redis/Local) │        │
          │         └────────────────┘        │
          │                                   │
    ┌─────▼───────────────────────────────────▼────┐
    │          Result Storage / Database            │
    │  - PostgreSQL (metadata, results)             │
    │  - S3 / MinIO (images, videos)                │
    │  - pgvector (embeddings)                      │
    └──────────────────────────────────────────────┘
```

## Technology Stack

```yaml
model_framework: PyTorch / TensorFlow
inference_runtime: ONNX Runtime / TensorRT
api_framework: FastAPI
model_serving: TorchServe / TF Serving / Custom
preprocessing: OpenCV / Pillow / torchvision
vector_db: pgvector / Pinecone / Weaviate
object_storage: S3 / MinIO
cache: Redis
monitoring: Prometheus + Grafana
```

## Pipeline Stages

### 1. Data Ingestion

**Input Formats:**
- Images: JPEG, PNG, WebP
- Video: MP4, AVI
- Text: Plain text, JSON
- Audio: WAV, MP3

**Validation:**
```python
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

async def validate_image(file: UploadFile):
    # Check file size (max 10MB)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large")
    
    # Check image format
    try:
        image = Image.open(io.BytesIO(contents))
        if image.format not in ['JPEG', 'PNG', 'WebP']:
            raise HTTPException(400, "Unsupported format")
        return image
    except:
        raise HTTPException(400, "Invalid image file")
```

### 2. Preprocessing Pipeline

**Image Preprocessing:**
```python
import cv2
import numpy as np
from torchvision import transforms

class ImagePreprocessor:
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size
        self.transform = transforms.Compose([
            transforms.Resize(target_size),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def preprocess(self, image):
        # Convert PIL to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply transformations
        tensor = self.transform(image)
        
        # Add batch dimension
        return tensor.unsqueeze(0)
```

**Text Preprocessing:**
```python
from transformers import AutoTokenizer

class TextPreprocessor:
    def __init__(self, model_name="bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def preprocess(self, text, max_length=512):
        return self.tokenizer(
            text,
            max_length=max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
```

### 3. Model Inference

**PyTorch Inference:**
```python
import torch
from typing import Dict, Any

class ModelInference:
    def __init__(self, model_path: str, device: str = "cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model = torch.load(model_path, map_location=self.device)
        self.model.eval()
    
    @torch.no_grad()
    def predict(self, input_tensor: torch.Tensor) -> Dict[str, Any]:
        input_tensor = input_tensor.to(self.device)
        
        # Inference
        output = self.model(input_tensor)
        
        # Post-process
        probabilities = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        
        return {
            "predicted_class": predicted.item(),
            "confidence": confidence.item(),
            "probabilities": probabilities.cpu().numpy().tolist()
        }
```

**ONNX Runtime (Faster):**
```python
import onnxruntime as ort
import numpy as np

class ONNXInference:
    def __init__(self, model_path: str):
        # Create inference session
        self.session = ort.InferenceSession(
            model_path,
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
        )
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
    
    def predict(self, input_tensor: np.ndarray) -> Dict[str, Any]:
        # Run inference
        outputs = self.session.run(
            [self.output_name],
            {self.input_name: input_tensor}
        )
        
        # Post-process
        probabilities = self.softmax(outputs[0])
        predicted_class = np.argmax(probabilities)
        confidence = probabilities[predicted_class]
        
        return {
            "predicted_class": int(predicted_class),
            "confidence": float(confidence),
            "probabilities": probabilities.tolist()
        }
    
    @staticmethod
    def softmax(x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum(axis=1, keepdims=True)
```

### 4. Post-processing & Results

**Result Formatting:**
```python
from datetime import datetime
from typing import Optional

class ResultFormatter:
    def __init__(self, class_labels: Dict[int, str]):
        self.class_labels = class_labels
    
    def format(
        self,
        prediction: Dict[str, Any],
        metadata: Optional[Dict] = None
    ) -> Dict:
        return {
            "success": True,
            "data": {
                "prediction": {
                    "class_id": prediction["predicted_class"],
                    "class_name": self.class_labels[prediction["predicted_class"]],
                    "confidence": round(prediction["confidence"], 4)
                },
                "top_predictions": self._get_top_k(
                    prediction["probabilities"],
                    k=3
                ),
                "metadata": metadata or {},
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    def _get_top_k(self, probabilities, k=3):
        probs = np.array(probabilities[0])
        top_k_indices = np.argsort(probs)[-k:][::-1]
        
        return [
            {
                "class_id": int(idx),
                "class_name": self.class_labels[int(idx)],
                "confidence": round(float(probs[idx]), 4)
            }
            for idx in top_k_indices
        ]
```

## FastAPI Implementation

**Main API:**
```python
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse
import redis
import json

app = FastAPI(title="AI Inference API", version="1.0.0")

# Initialize components
preprocessor = ImagePreprocessor()
model = ONNXInference("models/model.onnx")
formatter = ResultFormatter(class_labels={0: "cat", 1: "dog"})
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    try:
        # Validate input
        image = await validate_image(file)
        
        # Check cache
        image_hash = hash_image(image)
        cached = redis_client.get(f"prediction:{image_hash}")
        if cached:
            return json.loads(cached)
        
        # Preprocess
        input_tensor = preprocessor.preprocess(image)
        
        # Inference
        prediction = model.predict(input_tensor.numpy())
        
        # Format result
        result = formatter.format(prediction, metadata={
            "filename": file.filename,
            "content_type": file.content_type
        })
        
        # Cache result (1 hour TTL)
        redis_client.setex(
            f"prediction:{image_hash}",
            3600,
            json.dumps(result)
        )
        
        return result
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INFERENCE_ERROR",
                    "message": str(e)
                }
            }
        )

@app.post("/predict/batch")
async def predict_batch(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        result = await predict_image(file)
        results.append(result)
    return {"success": True, "data": results}
```

## Advanced Features

### 1. Model Versioning

```python
class ModelRegistry:
    def __init__(self):
        self.models = {}
    
    def register_model(self, name: str, version: str, model_path: str):
        key = f"{name}:{version}"
        self.models[key] = ONNXInference(model_path)
    
    def get_model(self, name: str, version: str = "latest"):
        key = f"{name}:{version}"
        return self.models.get(key)

# Usage
registry = ModelRegistry()
registry.register_model("classifier", "v1", "models/v1.onnx")
registry.register_model("classifier", "v2", "models/v2.onnx")

@app.post("/predict/image/{version}")
async def predict_with_version(
    version: str,
    file: UploadFile = File(...)
):
    model = registry.get_model("classifier", version)
    # ... inference logic
```

### 2. Batch Processing with Queue

```python
from celery import Celery
from typing import List

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def process_image_batch(image_urls: List[str]):
    results = []
    for url in image_urls:
        # Download image
        image = download_image(url)
        
        # Preprocess
        tensor = preprocessor.preprocess(image)
        
        # Inference
        prediction = model.predict(tensor.numpy())
        
        results.append({
            "url": url,
            "prediction": prediction
        })
    
    # Store results in database
    store_results(results)
    
    return results

# API endpoint
@app.post("/predict/batch/async")
async def predict_batch_async(image_urls: List[str]):
    task = process_image_batch.delay(image_urls)
    return {
        "success": True,
        "data": {
            "task_id": task.id,
            "status": "processing"
        }
    }

@app.get("/predict/batch/status/{task_id}")
async def get_batch_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "success": True,
        "data": {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.ready() else None
        }
    }
```

### 3. Vector Embeddings + Semantic Search

```python
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImageEmbedding(Base):
    __tablename__ = 'image_embeddings'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    embedding = Column(Vector(512))  # Assuming 512-dim embeddings

# Generate embeddings
def generate_embedding(image):
    # Use pre-trained model (ResNet, CLIP, etc.)
    with torch.no_grad():
        embedding = embedding_model(image)
    return embedding.cpu().numpy().flatten()

# Store embedding
@app.post("/embeddings/store")
async def store_embedding(file: UploadFile = File(...)):
    image = await validate_image(file)
    tensor = preprocessor.preprocess(image)
    
    # Generate embedding
    embedding = generate_embedding(tensor)
    
    # Store in database
    db_embedding = ImageEmbedding(
        filename=file.filename,
        embedding=embedding.tolist()
    )
    db.add(db_embedding)
    db.commit()
    
    return {"success": True, "id": db_embedding.id}

# Semantic search
@app.post("/embeddings/search")
async def search_similar(file: UploadFile = File(...), top_k: int = 5):
    image = await validate_image(file)
    tensor = preprocessor.preprocess(image)
    
    # Generate query embedding
    query_embedding = generate_embedding(tensor)
    
    # Search similar (cosine similarity)
    results = db.query(ImageEmbedding).order_by(
        ImageEmbedding.embedding.cosine_distance(query_embedding)
    ).limit(top_k).all()
    
    return {
        "success": True,
        "data": [
            {
                "id": r.id,
                "filename": r.filename,
                "similarity": cosine_similarity(query_embedding, r.embedding)
            }
            for r in results
        ]
    }
```

## Performance Optimization

### 1. Model Optimization

**Quantization (INT8):**
```python
import torch.quantization

# Post-training static quantization
model_fp32 = load_model()
model_fp32.eval()

# Fuse modules
model_fp32_fused = torch.quantization.fuse_modules(
    model_fp32,
    [['conv', 'bn', 'relu']]
)

# Prepare for quantization
model_fp32_prepared = torch.quantization.prepare(model_fp32_fused)

# Calibrate with sample data
with torch.no_grad():
    for data in calibration_data:
        model_fp32_prepared(data)

# Convert to quantized model
model_int8 = torch.quantization.convert(model_fp32_prepared)

# Result: 4x smaller model, 2-4x faster inference
```

**TensorRT Optimization (NVIDIA):**
```bash
# Convert ONNX to TensorRT
trtexec --onnx=model.onnx --saveEngine=model.trt --fp16

# Result: 2-5x faster on NVIDIA GPUs
```

### 2. Caching Strategy

```python
import hashlib
from functools import lru_cache

# Cache predictions
@lru_cache(maxsize=1000)
def get_cached_prediction(image_hash: str):
    return redis_client.get(f"pred:{image_hash}")

# Cache preprocessing
@lru_cache(maxsize=100)
def get_preprocessor():
    return ImagePreprocessor()
```

### 3. Batching for Throughput

```python
import asyncio
from collections import deque

class BatchInference:
    def __init__(self, model, batch_size=32, timeout=0.1):
        self.model = model
        self.batch_size = batch_size
        self.timeout = timeout
        self.queue = deque()
        self.processing = False
    
    async def predict(self, input_tensor):
        future = asyncio.Future()
        self.queue.append((input_tensor, future))
        
        if not self.processing:
            asyncio.create_task(self._process_batch())
        
        return await future
    
    async def _process_batch(self):
        self.processing = True
        await asyncio.sleep(self.timeout)  # Wait for batch to fill
        
        batch_inputs = []
        futures = []
        
        while self.queue and len(batch_inputs) < self.batch_size:
            input_tensor, future = self.queue.popleft()
            batch_inputs.append(input_tensor)
            futures.append(future)
        
        if batch_inputs:
            # Batch inference
            batch_tensor = torch.cat(batch_inputs)
            results = self.model.predict(batch_tensor)
            
            # Resolve futures
            for future, result in zip(futures, results):
                future.set_result(result)
        
        self.processing = False
```

## Monitoring & Logging

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency')
model_confidence = Gauge('model_confidence', 'Average confidence')

@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    start_time = time.time()
    
    try:
        # ... inference logic
        
        # Update metrics
        prediction_counter.inc()
        prediction_latency.observe(time.time() - start_time)
        model_confidence.set(prediction["confidence"])
        
        return result
    except Exception as e:
        # Log error
        logger.error(f"Prediction failed: {e}")
        raise
```

## Deployment Considerations

### GPU Requirements

| Model Type | GPU VRAM | Inference Speed | Cost/hour |
|------------|----------|-----------------|-----------|
| **Small (< 50MB)** | 2-4GB | 100-500 req/s | $0.50-1 |
| **Medium (50-500MB)** | 8-16GB | 50-200 req/s | $1-3 |
| **Large (> 500MB)** | 24-40GB | 10-50 req/s | $3-8 |

### Scaling Strategy

```
Small scale (< 100 req/s):
    → Single GPU server (RTX 4090 / T4)
    
Medium scale (100-1000 req/s):
    → Multiple GPU servers + Load balancer
    → Batch processing with queues
    
Large scale (> 1000 req/s):
    → Kubernetes + GPU node pools
    → Model serving framework (TorchServe / Triton)
    → Auto-scaling based on queue depth
```

---

**Estimated Costs (per month):**
- CPU-only inference: $100-300 (VPS)
- Single GPU (T4): $300-500 (cloud GPU)
- Multi-GPU setup: $1K-5K (depends on scale)
