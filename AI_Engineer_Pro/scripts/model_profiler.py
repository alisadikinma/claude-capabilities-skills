"""
Model Profiler
Analyze model performance, memory, and computational requirements
"""

import torch
import time
import numpy as np
from thop import profile, clever_format

def profile_model(model, input_shape=(1, 3, 640, 640), device='cuda'):
    """
    Profile PyTorch model
    
    Args:
        model: PyTorch model
        input_shape: Input tensor shape
        device: 'cuda' or 'cpu'
    
    Returns:
        dict: Profiling results
    """
    model = model.to(device)
    model.eval()
    
    # Create dummy input
    dummy_input = torch.randn(input_shape).to(device)
    
    # 1. FLOPs and Parameters
    flops, params = profile(model, inputs=(dummy_input,), verbose=False)
    flops, params = clever_format([flops, params], "%.3f")
    
    # 2. Memory usage
    torch.cuda.reset_peak_memory_stats()
    with torch.no_grad():
        _ = model(dummy_input)
    
    memory_allocated = torch.cuda.max_memory_allocated() / 1024**2  # MB
    memory_reserved = torch.cuda.max_memory_reserved() / 1024**2
    
    # 3. Inference time
    warmup_runs = 10
    benchmark_runs = 100
    
    # Warmup
    with torch.no_grad():
        for _ in range(warmup_runs):
            _ = model(dummy_input)
    
    # Benchmark
    if device == 'cuda':
        torch.cuda.synchronize()
    
    times = []
    with torch.no_grad():
        for _ in range(benchmark_runs):
            start = time.time()
            _ = model(dummy_input)
            
            if device == 'cuda':
                torch.cuda.synchronize()
            
            times.append(time.time() - start)
    
    latency_mean = np.mean(times) * 1000  # ms
    latency_std = np.std(times) * 1000
    throughput = 1 / np.mean(times)  # FPS
    
    # 4. Layer-wise profiling
    layer_times = {}
    
    def hook_fn(name):
        def hook(module, input, output):
            start = time.time()
            return output
        return hook
    
    # Results
    results = {
        'flops': flops,
        'params': params,
        'memory_allocated_mb': f"{memory_allocated:.2f}",
        'memory_reserved_mb': f"{memory_reserved:.2f}",
        'latency_mean_ms': f"{latency_mean:.2f}",
        'latency_std_ms': f"{latency_std:.2f}",
        'throughput_fps': f"{throughput:.2f}",
        'input_shape': input_shape,
        'device': device
    }
    
    return results

def compare_models(models_dict, input_shape=(1, 3, 640, 640)):
    """Compare multiple models"""
    import pandas as pd
    
    results = []
    for name, model in models_dict.items():
        print(f"Profiling {name}...")
        profile_results = profile_model(model, input_shape)
        profile_results['model'] = name
        results.append(profile_results)
    
    df = pd.DataFrame(results)
    return df

# Usage example
if __name__ == "__main__":
    from torchvision.models import resnet50, efficientnet_b0
    
    # Single model
    model = resnet50()
    results = profile_model(model, input_shape=(1, 3, 224, 224))
    
    print("\\n=== Model Profile ===")
    for key, value in results.items():
        print(f"{key}: {value}")
    
    # Compare models
    models = {
        'ResNet50': resnet50(),
        'EfficientNet-B0': efficientnet_b0()
    }
    
    df = compare_models(models, input_shape=(1, 3, 224, 224))
    print("\\n=== Model Comparison ===")
    print(df.to_string())
