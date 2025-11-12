"""
Inference Benchmarker
Measure inference performance for different batch sizes and configurations
"""

import torch
import time
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class InferenceBenchmarker:
    """Benchmark model inference performance"""
    
    def __init__(self, model, device='cuda', warmup_runs=10):
        self.model = model.to(device).eval()
        self.device = device
        self.warmup_runs = warmup_runs
    
    def benchmark_batch_sizes(self, input_shape: Tuple, batch_sizes: List[int], num_runs: int = 100):
        """
        Benchmark different batch sizes
        
        Returns:
            dict: {batch_size: {latency, throughput}}
        """
        results = {}
        
        for batch_size in batch_sizes:
            print(f"Benchmarking batch_size={batch_size}...")
            
            # Create input
            input_data = torch.randn(batch_size, *input_shape).to(self.device)
            
            # Warmup
            with torch.no_grad():
                for _ in range(self.warmup_runs):
                    _ = self.model(input_data)
            
            if self.device == 'cuda':
                torch.cuda.synchronize()
            
            # Benchmark
            times = []
            with torch.no_grad():
                for _ in range(num_runs):
                    start = time.time()
                    _ = self.model(input_data)
                    
                    if self.device == 'cuda':
                        torch.cuda.synchronize()
                    
                    times.append(time.time() - start)
            
            latency = np.mean(times) * 1000  # ms
            throughput = batch_size / np.mean(times)  # samples/sec
            
            results[batch_size] = {
                'latency_ms': latency,
                'throughput_samples_sec': throughput,
                'latency_per_sample_ms': latency / batch_size
            }
        
        return results
    
    def benchmark_precision(self, input_shape: Tuple, batch_size: int = 1, num_runs: int = 100):
        """Compare FP32 vs FP16 precision"""
        
        results = {}
        
        for dtype, dtype_name in [(torch.float32, 'FP32'), (torch.float16, 'FP16')]:
            print(f"Benchmarking {dtype_name}...")
            
            # Convert model
            model_typed = self.model.to(dtype)
            input_data = torch.randn(batch_size, *input_shape).to(self.device).to(dtype)
            
            # Warmup
            with torch.no_grad():
                for _ in range(self.warmup_runs):
                    _ = model_typed(input_data)
            
            if self.device == 'cuda':
                torch.cuda.synchronize()
            
            # Benchmark
            times = []
            with torch.no_grad():
                for _ in range(num_runs):
                    start = time.time()
                    _ = model_typed(input_data)
                    
                    if self.device == 'cuda':
                        torch.cuda.synchronize()
                    
                    times.append(time.time() - start)
            
            latency = np.mean(times) * 1000
            
            results[dtype_name] = {
                'latency_ms': latency,
                'speedup': 1.0  # Will be calculated
            }
        
        # Calculate speedup
        results['FP16']['speedup'] = results['FP32']['latency_ms'] / results['FP16']['latency_ms']
        
        return results
    
    def plot_results(self, batch_results):
        """Plot benchmark results"""
        batch_sizes = list(batch_results.keys())
        latencies = [batch_results[bs]['latency_ms'] for bs in batch_sizes]
        throughputs = [batch_results[bs]['throughput_samples_sec'] for bs in batch_sizes]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Latency plot
        ax1.plot(batch_sizes, latencies, marker='o')
        ax1.set_xlabel('Batch Size')
        ax1.set_ylabel('Latency (ms)')
        ax1.set_title('Latency vs Batch Size')
        ax1.grid(True)
        
        # Throughput plot
        ax2.plot(batch_sizes, throughputs, marker='o', color='orange')
        ax2.set_xlabel('Batch Size')
        ax2.set_ylabel('Throughput (samples/sec)')
        ax2.set_title('Throughput vs Batch Size')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('benchmark_results.png')
        print("Saved plot to benchmark_results.png")
        
        return fig

# Usage example
if __name__ == "__main__":
    from torchvision.models import resnet50
    
    # Initialize
    model = resnet50()
    benchmarker = InferenceBenchmarker(model, device='cuda')
    
    # Benchmark batch sizes
    batch_sizes = [1, 2, 4, 8, 16, 32]
    batch_results = benchmarker.benchmark_batch_sizes(
        input_shape=(3, 224, 224),
        batch_sizes=batch_sizes
    )
    
    print("\\n=== Batch Size Benchmark ===")
    for bs, res in batch_results.items():
        print(f"Batch {bs}: {res['latency_ms']:.2f}ms | {res['throughput_samples_sec']:.2f} samples/sec")
    
    # Benchmark precision
    precision_results = benchmarker.benchmark_precision(
        input_shape=(3, 224, 224),
        batch_size=1
    )
    
    print("\\n=== Precision Benchmark ===")
    for dtype, res in precision_results.items():
        print(f"{dtype}: {res['latency_ms']:.2f}ms (speedup: {res.get('speedup', 1.0):.2f}x)")
    
    # Plot results
    benchmarker.plot_results(batch_results)
