# Hardware Acceleration

## GPU Optimization

**CUDA Best Practices**
- Use pinned memory for faster data transfer
- Overlap compute and data transfer
- Use CUDA streams for concurrent operations
- Enable TF32 on Ampere GPUs

**Multi-GPU Training**
```python
# DataParallel (simple)
model = nn.DataParallel(model, device_ids=[0, 1, 2, 3])

# DistributedDataParallel (faster)
model = nn.parallel.DistributedDataParallel(model)
```

## TensorRT (NVIDIA)

**Conversion**
```python
import torch_tensorrt

# Compile with TensorRT
trt_model = torch_tensorrt.compile(
    model,
    inputs=[torch.randn(1, 3, 640, 640).cuda()],
    enabled_precisions={torch.float16},
)

# 2-5x faster inference
```

## Edge Deployment

**Jetson Orin NX** (PCB Inspection)
- 100 TOPS AI performance
- YOLOv8 at 60+ FPS (640x640)
- TensorRT optimization essential
- Power efficiency: 10-25W

**Raspberry Pi** (Not recommended for CV)
- Too slow for real-time detection
- Use for control logic only

**Intel NCS2/Movidius**
- 1 TOPS, good for lightweight models
- OpenVINO optimization required

## Cloud GPUs

| GPU | Memory | Price/hr | Use Case |
|-----|--------|----------|----------|
| T4 | 16GB | $0.35 | Inference |
| A10G | 24GB | $1.01 | Training/Inference |
| A100 | 40GB | $3.06 | Large model training |
| H100 | 80GB | $4.76 | Very large models |

## Benchmark Tools

```bash
# NVIDIA tools
nvidia-smi  # GPU monitoring
nvprof  # Profiling
nsys  # System profiling

# PyTorch profiler
with torch.profiler.profile() as prof:
    model(input)
print(prof.key_averages().table())
```
