# ONNX Optimization Guide

Convert and optimize models for cross-platform deployment.

## PyTorch to ONNX

```python
import torch

# Load PyTorch model
model = torch.load('model.pth')
model.eval()

# Dummy input
dummy_input = torch.randn(1, 3, 640, 640)

# Export
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    export_params=True,
    opset_version=17,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'output': {0: 'batch_size'}
    }
)
```

## TensorFlow to ONNX

```bash
pip install tf2onnx

python -m tf2onnx.convert --saved-model saved_model/ --output model.onnx
```

## Optimization

```python
import onnx
from onnxruntime.transformers.optimizer import optimize_model

# Load
model = onnx.load("model.onnx")

# Optimize
optimized_model = optimize_model(
    "model.onnx",
    model_type='bert',  # or 'gpt2', 'vit'
    num_heads=12,
    hidden_size=768,
    optimization_options=None
)

optimized_model.save_model_to_file("model_optimized.onnx")
```

## Quantization (INT8)

```python
from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic(
    "model.onnx",
    "model_int8.onnx",
    weight_type=QuantType.QUInt8
)
```

## Inference

```python
import onnxruntime as ort
import numpy as np

# Create session
session = ort.InferenceSession(
    "model.onnx",
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
)

# Prepare input
input_data = np.random.randn(1, 3, 640, 640).astype(np.float32)

# Run
outputs = session.run(
    None,
    {'input': input_data}
)

print(outputs[0].shape)
```

## Benchmarking

```python
import time

# Warmup
for _ in range(10):
    session.run(None, {'input': input_data})

# Benchmark
times = []
for _ in range(100):
    start = time.time()
    session.run(None, {'input': input_data})
    times.append(time.time() - start)

print(f"Avg latency: {np.mean(times)*1000:.2f}ms")
print(f"Throughput: {1/np.mean(times):.2f} FPS")
```

## Model Size Comparison

| Format | Size | Latency |
|--------|------|---------|
| PyTorch FP32 | 100MB | 50ms |
| ONNX FP32 | 95MB | 30ms |
| ONNX FP16 | 50MB | 20ms |
| ONNX INT8 | 25MB | 15ms |
