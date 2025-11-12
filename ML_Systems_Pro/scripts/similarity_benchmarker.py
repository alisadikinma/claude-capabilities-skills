"""
Similarity Search Benchmarker
=============================

Comprehensive benchmarking tool for comparing similarity search algorithms.

Use Cases:
- Compare HNSW vs IVF vs exact search
- Find optimal parameters (M, efSearch, nprobe)
- Measure recall vs latency trade-offs
- Production capacity planning

Requirements:
    pip install faiss-cpu numpy pandas matplotlib tqdm
"""

import time
import numpy as np
import pandas as pd
import faiss
from typing import Dict, List, Tuple
from dataclasses import dataclass
from tqdm import tqdm
import matplotlib.pyplot as plt


@dataclass
class BenchmarkResult:
    """Results from a benchmark run."""
    algorithm: str
    parameters: Dict
    recall_at_10: float
    recall_at_100: float
    queries_per_second: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    index_size_mb: float
    build_time_seconds: float


class SimilarityBenchmarker:
    """
    Benchmark similarity search algorithms.
    
    Supports:
    - Exact search (brute force)
    - HNSW
    - IVF (Inverted File Index)
    - IVF + PQ (Product Quantization)
    """
    
    def __init__(
        self,
        database: np.ndarray,
        queries: np.ndarray,
        ground_truth: np.ndarray = None
    ):
        """
        Initialize benchmarker.
        
        Args:
            database: Database vectors (N, D)
            queries: Query vectors (Q, D)
            ground_truth: Ground truth indices (Q, K) - optional
        """
        self.database = database.astype(np.float32)
        self.queries = queries.astype(np.float32)
        self.n_vectors, self.dimension = database.shape
        self.n_queries = len(queries)
        
        # Compute ground truth if not provided
        if ground_truth is None:
            print("Computing ground truth with exact search...")
            self.ground_truth = self._compute_ground_truth()
        else:
            self.ground_truth = ground_truth
    
    def _compute_ground_truth(self, k: int = 100) -> np.ndarray:
        """Compute ground truth using exact search."""
        index = faiss.IndexFlatIP(self.dimension)
        index.add(self.database)
        
        _, indices = index.search(self.queries, k)
        return indices
    
    def benchmark_exact(self) -> BenchmarkResult:
        """Benchmark exact search (brute force)."""
        print("\nBenchmarking Exact Search...")
        
        # Build index
        build_start = time.time()
        index = faiss.IndexFlatIP(self.dimension)
        index.add(self.database)
        build_time = time.time() - build_start
        
        # Measure search performance
        latencies = []
        for query in tqdm(self.queries, desc="Searching"):
            start = time.time()
            index.search(query.reshape(1, -1), k=10)
            latencies.append((time.time() - start) * 1000)  # ms
        
        # Compute metrics
        qps = 1000 / np.mean(latencies)
        
        return BenchmarkResult(
            algorithm="Exact",
            parameters={},
            recall_at_10=1.0,
            recall_at_100=1.0,
            queries_per_second=qps,
            latency_p50_ms=np.percentile(latencies, 50),
            latency_p95_ms=np.percentile(latencies, 95),
            latency_p99_ms=np.percentile(latencies, 99),
            index_size_mb=self.database.nbytes / 1024 / 1024,
            build_time_seconds=build_time
        )
    
    def benchmark_hnsw(
        self,
        M_values: List[int] = [16, 32],
        ef_construction_values: List[int] = [200, 400],
        ef_search_values: List[int] = [50, 100, 200]
    ) -> List[BenchmarkResult]:
        """
        Benchmark HNSW with different parameters.
        
        Args:
            M_values: Connections per node
            ef_construction_values: Build-time search depth
            ef_search_values: Query-time search depth
        """
        results = []
        
        for M in M_values:
            for ef_construction in ef_construction_values:
                print(f"\nBuilding HNSW (M={M}, efConstruction={ef_construction})...")
                
                # Build index
                build_start = time.time()
                index = faiss.IndexHNSWFlat(self.dimension, M)
                index.hnsw.efConstruction = ef_construction
                index.add(self.database)
                build_time = time.time() - build_start
                
                # Test different search parameters
                for ef_search in ef_search_values:
                    print(f"  Testing efSearch={ef_search}...")
                    index.hnsw.efSearch = ef_search
                    
                    # Search
                    latencies = []
                    all_indices = []
                    
                    for query in self.queries:
                        start = time.time()
                        _, indices = index.search(query.reshape(1, -1), k=100)
                        latencies.append((time.time() - start) * 1000)
                        all_indices.append(indices[0])
                    
                    all_indices = np.array(all_indices)
                    
                    # Compute recall
                    recall_10 = self._compute_recall(all_indices, self.ground_truth, k=10)
                    recall_100 = self._compute_recall(all_indices, self.ground_truth, k=100)
                    
                    # QPS
                    qps = 1000 / np.mean(latencies)
                    
                    results.append(BenchmarkResult(
                        algorithm="HNSW",
                        parameters={'M': M, 'efConstruction': ef_construction, 'efSearch': ef_search},
                        recall_at_10=recall_10,
                        recall_at_100=recall_100,
                        queries_per_second=qps,
                        latency_p50_ms=np.percentile(latencies, 50),
                        latency_p95_ms=np.percentile(latencies, 95),
                        latency_p99_ms=np.percentile(latencies, 99),
                        index_size_mb=(self.database.nbytes / 1024 / 1024) * 1.2,  # Approximate
                        build_time_seconds=build_time
                    ))
        
        return results
    
    def benchmark_ivf(
        self,
        nlist_values: List[int] = [100, 1000],
        nprobe_values: List[int] = [1, 10, 50]
    ) -> List[BenchmarkResult]:
        """
        Benchmark IVF with different parameters.
        
        Args:
            nlist_values: Number of clusters
            nprobe_values: Clusters to search
        """
        results = []
        
        for nlist in nlist_values:
            print(f"\nBuilding IVF (nlist={nlist})...")
            
            # Build index
            build_start = time.time()
            quantizer = faiss.IndexFlatIP(self.dimension)
            index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
            
            # Train
            index.train(self.database)
            index.add(self.database)
            build_time = time.time() - build_start
            
            # Test different search parameters
            for nprobe in nprobe_values:
                print(f"  Testing nprobe={nprobe}...")
                index.nprobe = nprobe
                
                # Search
                latencies = []
                all_indices = []
                
                for query in self.queries:
                    start = time.time()
                    _, indices = index.search(query.reshape(1, -1), k=100)
                    latencies.append((time.time() - start) * 1000)
                    all_indices.append(indices[0])
                
                all_indices = np.array(all_indices)
                
                # Compute recall
                recall_10 = self._compute_recall(all_indices, self.ground_truth, k=10)
                recall_100 = self._compute_recall(all_indices, self.ground_truth, k=100)
                
                # QPS
                qps = 1000 / np.mean(latencies)
                
                results.append(BenchmarkResult(
                    algorithm="IVF",
                    parameters={'nlist': nlist, 'nprobe': nprobe},
                    recall_at_10=recall_10,
                    recall_at_100=recall_100,
                    queries_per_second=qps,
                    latency_p50_ms=np.percentile(latencies, 50),
                    latency_p95_ms=np.percentile(latencies, 95),
                    latency_p99_ms=np.percentile(latencies, 99),
                    index_size_mb=self.database.nbytes / 1024 / 1024,
                    build_time_seconds=build_time
                ))
        
        return results
    
    def benchmark_ivfpq(
        self,
        nlist: int = 1000,
        m: int = 64,
        nbits: int = 8,
        nprobe_values: List[int] = [1, 10, 50]
    ) -> List[BenchmarkResult]:
        """
        Benchmark IVF + Product Quantization.
        
        Args:
            nlist: Number of clusters
            m: Number of subvectors
            nbits: Bits per subquantizer
            nprobe_values: Clusters to search
        """
        results = []
        
        print(f"\nBuilding IVF+PQ (nlist={nlist}, m={m}, nbits={nbits})...")
        
        # Build index
        build_start = time.time()
        quantizer = faiss.IndexFlatIP(self.dimension)
        index = faiss.IndexIVFPQ(quantizer, self.dimension, nlist, m, nbits)
        
        # Train and add
        index.train(self.database)
        index.add(self.database)
        build_time = time.time() - build_start
        
        # Test different search parameters
        for nprobe in nprobe_values:
            print(f"  Testing nprobe={nprobe}...")
            index.nprobe = nprobe
            
            # Search
            latencies = []
            all_indices = []
            
            for query in self.queries:
                start = time.time()
                _, indices = index.search(query.reshape(1, -1), k=100)
                latencies.append((time.time() - start) * 1000)
                all_indices.append(indices[0])
            
            all_indices = np.array(all_indices)
            
            # Compute recall
            recall_10 = self._compute_recall(all_indices, self.ground_truth, k=10)
            recall_100 = self._compute_recall(all_indices, self.ground_truth, k=100)
            
            # QPS
            qps = 1000 / np.mean(latencies)
            
            # Compressed size
            compressed_size = (self.n_vectors * m * nbits / 8) / 1024 / 1024
            
            results.append(BenchmarkResult(
                algorithm="IVF+PQ",
                parameters={'nlist': nlist, 'm': m, 'nbits': nbits, 'nprobe': nprobe},
                recall_at_10=recall_10,
                recall_at_100=recall_100,
                queries_per_second=qps,
                latency_p50_ms=np.percentile(latencies, 50),
                latency_p95_ms=np.percentile(latencies, 95),
                latency_p99_ms=np.percentile(latencies, 99),
                index_size_mb=compressed_size,
                build_time_seconds=build_time
            ))
        
        return results
    
    def _compute_recall(
        self,
        predicted: np.ndarray,
        ground_truth: np.ndarray,
        k: int = 10
    ) -> float:
        """
        Compute recall@k.
        
        Args:
            predicted: Predicted indices (Q, K')
            ground_truth: Ground truth indices (Q, K'')
            k: Number of results to consider
        """
        recalls = []
        
        for pred, truth in zip(predicted, ground_truth):
            pred_k = set(pred[:k])
            truth_k = set(truth[:k])
            
            recall = len(pred_k & truth_k) / len(truth_k)
            recalls.append(recall)
        
        return np.mean(recalls)
    
    def run_all_benchmarks(self) -> pd.DataFrame:
        """Run all benchmarks and return results DataFrame."""
        all_results = []
        
        # Exact search
        all_results.append(self.benchmark_exact())
        
        # HNSW
        all_results.extend(self.benchmark_hnsw())
        
        # IVF
        all_results.extend(self.benchmark_ivf())
        
        # IVF+PQ
        all_results.extend(self.benchmark_ivfpq())
        
        # Convert to DataFrame
        df = pd.DataFrame([vars(r) for r in all_results])
        
        return df
    
    def plot_results(self, results_df: pd.DataFrame, save_path: str = None):
        """
        Plot recall vs latency trade-offs.
        
        Args:
            results_df: Results DataFrame
            save_path: Optional path to save figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Recall@10 vs Latency
        ax = axes[0]
        for algo in results_df['algorithm'].unique():
            subset = results_df[results_df['algorithm'] == algo]
            ax.scatter(
                subset['latency_p50_ms'],
                subset['recall_at_10'],
                label=algo,
                s=100,
                alpha=0.7
            )
        
        ax.set_xlabel('Latency P50 (ms)')
        ax.set_ylabel('Recall@10')
        ax.set_title('Recall vs Latency Trade-off')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 2: QPS vs Memory
        ax = axes[1]
        for algo in results_df['algorithm'].unique():
            subset = results_df[results_df['algorithm'] == algo]
            ax.scatter(
                subset['index_size_mb'],
                subset['queries_per_second'],
                label=algo,
                s=100,
                alpha=0.7
            )
        
        ax.set_xlabel('Index Size (MB)')
        ax.set_ylabel('Queries Per Second')
        ax.set_title('Throughput vs Memory Usage')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()


# Example usage
if __name__ == "__main__":
    # Generate synthetic data
    np.random.seed(42)
    
    dimension = 128
    n_database = 10000
    n_queries = 100
    
    print(f"Generating {n_database:,} database vectors ({dimension}D)...")
    database = np.random.randn(n_database, dimension).astype(np.float32)
    database = database / np.linalg.norm(database, axis=1, keepdims=True)  # L2 normalize
    
    print(f"Generating {n_queries} query vectors...")
    queries = np.random.randn(n_queries, dimension).astype(np.float32)
    queries = queries / np.linalg.norm(queries, axis=1, keepdims=True)
    
    # Benchmark
    benchmarker = SimilarityBenchmarker(database, queries)
    results_df = benchmarker.run_all_benchmarks()
    
    # Print results
    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS")
    print("=" * 80)
    print(results_df.to_string(index=False))
    
    # Plot
    benchmarker.plot_results(results_df, save_path='benchmark_results.png')
    
    # Save to CSV
    results_df.to_csv('benchmark_results.csv', index=False)
    print("\nResults saved to benchmark_results.csv")
