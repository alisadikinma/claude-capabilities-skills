# Model Optimization Guide

## Techniques

### 1. Quantization
**INT8 Quantization** (2-4x speedup, <1% accuracy loss)
```python
from torch.quantization import quantize_dynamic
quantized_model = quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)
```

### 2. Pruning
**Remove 30-50% weights** (2x speedup)
```python
import torch.nn.utils.prune as prune
prune.l1_unstructured(module, name="weight", amount=0.3)
```

### 3. Knowledge Distillation
Train small model from large model
- Student model: 10-50x smaller
- Retain 90-95% of teacher accuracy

### 4. Mixed Precision (FP16)
```python
from torch.cuda.amp import autocast, GradScaler
with autocast():
    output = model(input)
```

### 5. Model Compression
- Use MobileNet/EfficientNet architectures
- Reduce input resolution (640→416 for YOLO)
- Decrease model depth/width

## Hardware Acceleration

**NVIDIA GPU**
- TensorRT: 2-5x speedup
- CUDA graphs for static models
- Use Tensor Cores (mixed precision)

**Edge Devices**
- TensorFlow Lite for mobile
- ONNX Runtime for cross-platform
- CoreML for iOS

## Inference Optimization

**Batch Processing** (4x throughput)
```python
# Process 8 images at once
outputs = model(torch.stack([img1, img2, ..., img8]))
```

**Dynamic Batching**
- Group requests together (wait 10-100ms)
- Process batch at once

**Model Caching**
- Cache embeddings for common inputs
- Use Redis for distributed cache

## Latency Targets

| Use Case | Target Latency |
|----------|----------------|
| Real-time video | <33ms (30 FPS) |
| Interactive API | <100ms |
| Batch processing | <1s |
