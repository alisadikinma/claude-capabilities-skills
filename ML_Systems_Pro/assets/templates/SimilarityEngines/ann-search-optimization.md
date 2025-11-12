# Approximate Nearest Neighbor (ANN) Search Optimization

Complete guide for optimizing vector similarity search at scale using ANN algorithms.

## Why ANN Search?

**Exact Search (Brute Force):**
- Compares query against ALL vectors
- 100% accuracy
- O(n) complexity - slow for large datasets
- Works up to ~100K vectors

**Approximate Search (ANN):**
- Uses indexing structures to skip most vectors
- 95-99% accuracy (configurable)
- O(log n) to O(1) complexity
- Scales to billions of vectors

## Algorithm Comparison

| Algorithm | Speed | Accuracy | Memory | Best For |
|-----------|-------|----------|--------|----------|
| **HNSW** | Fast | High (98%) | High | General purpose, <100M vectors |
| **IVF** | Medium | Medium (95%) | Medium | Large datasets, GPU acceleration |
| **LSH** | Very Fast | Low (90%) | Low | Ultra-fast retrieval, sparse data |
| **ScaNN** | Very Fast | High (97%) | Medium | Google-scale search |
| **Product Quantization** | Fast | Medium | Very Low | Memory-constrained environments |

## HNSW (Hierarchical Navigable Small World)

**Best General-Purpose ANN Algorithm**

### Concepts

HNSW builds a multi-layer graph where:
- Top layers: Sparse, for long-distance jumps
- Bottom layer: Dense, for precise search
- Navigation: Start at top, descend to bottom

### Parameters

```python
import faiss

dimension = 512
M = 16  # Number of connections per node
ef_construction = 200  # Construction search depth
ef_search = 50  # Query search depth

# Create HNSW index
index = faiss.IndexHNSWFlat(dimension, M)
index.hnsw.efConstruction = ef_construction

# Add vectors
index.add(vectors.astype(np.float32))

# Search
index.hnsw.efSearch = ef_search
distances, indices = index.search(query_vectors, k=10)
```

### Parameter Tuning

**M (connections per node):**
- Higher M = Better accuracy, more memory, slower build
- Recommended: 16-32 for most cases
- Use 64+ for critical accuracy needs

**efConstruction (build-time search):**
- Higher = Better index quality, slower build
- Recommended: 100-400
- Use 400+ for production indexes

**efSearch (query-time search):**
- Higher = Better accuracy, slower search
- Start with efSearch = M
- Increase until accuracy target met

### Benchmarking

```python
import time
import numpy as np

def benchmark_hnsw(index, queries, k=10):
    """Benchmark HNSW accuracy and speed."""
    
    # Test different efSearch values
    ef_values = [10, 20, 50, 100, 200]
    
    for ef in ef_values:
        index.hnsw.efSearch = ef
        
        # Measure latency
        start = time.time()
        distances, indices = index.search(queries, k)
        latency = (time.time() - start) / len(queries) * 1000  # ms
        
        # Measure accuracy (if you have ground truth)
        # accuracy = compute_recall(indices, ground_truth)
        
        print(f"efSearch={ef}: {latency:.2f}ms per query")
```

### Memory Usage

```
Memory = n_vectors * M * 2 * 4 bytes (for connections)
        + n_vectors * dimension * 4 bytes (for vectors)

Example: 1M vectors, 512 dim, M=16
= 1M * 16 * 2 * 4 + 1M * 512 * 4
= 128 MB + 2048 MB = 2.2 GB
```

## IVF (Inverted File Index)

**Best for Large Datasets with GPU**

### Concepts

IVF partitions vectors into clusters (Voronoi cells):
1. K-means clustering during build
2. Assign each vector to nearest cluster
3. At query time, search only nearest clusters

### Implementation

```python
import faiss

dimension = 512
n_list = 100  # Number of clusters
n_probe = 10  # Clusters to search

# Create IVF index
quantizer = faiss.IndexFlatL2(dimension)
index = faiss.IndexIVFFlat(quantizer, dimension, n_list)

# Train on sample (required for IVF)
index.train(training_vectors)

# Add vectors
index.add(vectors)

# Search
index.nprobe = n_probe
distances, indices = index.search(queries, k=10)
```

### Parameter Tuning

**n_list (number of clusters):**
- Rule of thumb: `n_list = sqrt(n_vectors)`
- Too few: Each cluster too large, slow search
- Too many: Poor clustering, reduced accuracy
- Recommended: 100-10,000

**n_probe (clusters to search):**
- Higher = Better accuracy, slower search
- Start with n_probe = 1% of n_list
- Increase until accuracy target met

### GPU Acceleration

```python
import faiss

# Create GPU index
res = faiss.StandardGpuResources()
gpu_index = faiss.index_cpu_to_gpu(res, 0, cpu_index)

# 10-100x faster than CPU for large datasets
distances, indices = gpu_index.search(queries, k=10)
```

## Product Quantization (PQ)

**Best for Memory-Constrained Environments**

### Concepts

Compress vectors by:
1. Split vector into sub-vectors
2. Quantize each sub-vector to nearest centroid
3. Store only centroid IDs (bytes vs floats)

**Compression:** 512D float32 = 2KB → 64 bytes (32x smaller)

### Implementation

```python
import faiss

dimension = 512
m = 64  # Number of sub-vectors
n_bits = 8  # Bits per centroid ID

# Create PQ index
index = faiss.IndexPQ(dimension, m, n_bits)

# Train and add
index.train(training_vectors)
index.add(vectors)

# Search (with some accuracy loss)
distances, indices = index.search(queries, k=10)
```

### Combining IVF + PQ

```python
# IVF for speed, PQ for compression
n_list = 1000
m = 64
n_bits = 8

quantizer = faiss.IndexFlatL2(dimension)
index = faiss.IndexIVFPQ(quantizer, dimension, n_list, m, n_bits)

index.train(training_vectors)
index.add(vectors)

index.nprobe = 10
distances, indices = index.search(queries, k=10)
```

## LSH (Locality-Sensitive Hashing)

**Best for Ultra-Fast Retrieval**

### Concepts

Use hash functions that map similar vectors to same buckets:
1. Hash vectors into buckets
2. Search only vectors in same bucket(s)
3. Trade accuracy for extreme speed

### Implementation (using FAISS)

```python
import faiss

dimension = 512
n_bits = 256  # Hash code length

# Create LSH index
index = faiss.IndexLSH(dimension, n_bits)

# Add vectors
index.add(vectors)

# Very fast search (but lower accuracy)
distances, indices = index.search(queries, k=10)
```

## ScaNN (Scalable Nearest Neighbors)

**Google's Production ANN Library**

### Installation

```bash
pip install scann
```

### Implementation

```python
import scann

# Build index
searcher = scann.scann_ops_pybind.builder(
    db=vectors,  # Database vectors
    num_neighbors=10,
    distance_measure="dot_product"
).tree(
    num_leaves=2000,
    num_leaves_to_search=100,
    training_sample_size=250000
).score_ah(
    dimensions_per_block=2,
    anisotropic_quantization_threshold=0.2
).reorder(100).build()

# Search
indices, distances = searcher.search_batched(queries)
```

### Advantages

- State-of-the-art speed/accuracy tradeoff
- Highly optimized for CPUs
- Used in Google production systems

## Optimization Strategies

### 1. Pre-Filtering Before ANN

Apply metadata filters BEFORE vector search:

```python
# Filter by category first
filtered_indices = [i for i, item in enumerate(items) 
                   if item['category'] == 'electronics']
filtered_vectors = vectors[filtered_indices]

# Then search
index_filtered = faiss.IndexFlatIP(dimension)
index_filtered.add(filtered_vectors)
distances, indices = index_filtered.search(query, k=10)

# Map back to original indices
original_indices = [filtered_indices[i] for i in indices[0]]
```

### 2. Hierarchical Search

Coarse search → Fine re-ranking:

```python
# Stage 1: Fast ANN (low accuracy, high recall)
index.hnsw.efSearch = 20
coarse_distances, coarse_indices = index.search(query, k=100)

# Stage 2: Exact re-ranking of candidates
candidates = vectors[coarse_indices[0]]
exact_distances = np.dot(candidates, query.T).squeeze()
top_k_indices = np.argsort(-exact_distances)[:10]

final_indices = coarse_indices[0][top_k_indices]
```

### 3. Quantization

Reduce precision for speed:

```python
# Float32 → Float16 (2x smaller, minimal accuracy loss)
vectors_fp16 = vectors.astype(np.float16)

# For search, still use float32 queries
index = faiss.IndexFlatIP(dimension)
index.add(vectors_fp16.astype(np.float32))
```

### 4. Caching Popular Queries

```python
import redis
import pickle

cache = redis.Redis()

def search_with_cache(query, k=10):
    query_hash = hash(query.tobytes())
    cache_key = f"search:{query_hash}:{k}"
    
    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return pickle.loads(cached)
    
    # Perform search
    distances, indices = index.search(query, k)
    
    # Cache result (24 hour TTL)
    cache.setex(cache_key, 86400, pickle.dumps((distances, indices)))
    
    return distances, indices
```

## Performance Benchmarks

### Dataset: 1M vectors, 512 dimensions

| Algorithm | Build Time | QPS | Recall@10 | Memory |
|-----------|-----------|-----|-----------|---------|
| Exact | 0s | 50 | 100% | 2 GB |
| HNSW (M=16) | 5 min | 2000 | 98% | 2.2 GB |
| IVF (n_list=1000) | 2 min | 1500 | 95% | 2 GB |
| IVF+PQ | 3 min | 3000 | 92% | 128 MB |
| LSH | 1 min | 5000 | 88% | 256 MB |

**QPS = Queries Per Second**

## Algorithm Selection Decision Tree

```
Dataset size < 100K vectors?
  → Use exact search (IndexFlatIP)

Need highest accuracy (>98%)?
  → HNSW (M=32, efConstruction=400)

GPU available?
  → IVF on GPU (n_list=sqrt(n), n_probe=10)

Memory constrained?
  → IVF + PQ (m=64, n_bits=8)

Need extreme speed, ok with 90% accuracy?
  → LSH or ScaNN

Multiple billion vectors?
  → Distributed search (see production patterns)
```

## Monitoring and Debugging

### Measure Recall

```python
def compute_recall_at_k(predicted, ground_truth, k=10):
    """
    Compute recall@k.
    
    Args:
        predicted: ANN search results (N, k)
        ground_truth: Exact search results (N, k)
        k: Number of results
    """
    recall = 0
    for pred, truth in zip(predicted, ground_truth):
        overlap = len(set(pred[:k]) & set(truth[:k]))
        recall += overlap / k
    
    return recall / len(predicted)

# Usage
exact_indices = exact_index.search(queries, k=10)[1]
ann_indices = ann_index.search(queries, k=10)[1]
recall = compute_recall_at_k(ann_indices, exact_indices, k=10)
print(f"Recall@10: {recall:.2%}")
```

### Measure Latency Distribution

```python
import numpy as np

def benchmark_latency(index, queries, k=10, n_runs=100):
    """Measure P50, P95, P99 latencies."""
    latencies = []
    
    for _ in range(n_runs):
        start = time.time()
        index.search(queries, k)
        latency = (time.time() - start) / len(queries) * 1000
        latencies.append(latency)
    
    print(f"P50: {np.percentile(latencies, 50):.2f}ms")
    print(f"P95: {np.percentile(latencies, 95):.2f}ms")
    print(f"P99: {np.percentile(latencies, 99):.2f}ms")
```

## Common Issues

### Issue: Low Recall
**Solutions:**
- Increase efSearch (HNSW) or n_probe (IVF)
- Use higher M (HNSW) or more clusters (IVF)
- Check vector normalization (L2 norm = 1)
- Verify training set is representative (IVF)

### Issue: High Latency
**Solutions:**
- Reduce efSearch or n_probe
- Use quantization (PQ)
- Pre-filter before search
- Add caching layer
- Switch to GPU (IVF)

### Issue: High Memory Usage
**Solutions:**
- Use Product Quantization (IVF+PQ)
- Reduce M (HNSW)
- Consider LSH for extreme compression

### Issue: Inconsistent Results
**Solutions:**
- Set random seed for training (IVF)
- Use deterministic build (avoid parallel)
- Verify vectors are normalized consistently

## Production Checklist

- [ ] Benchmark recall vs latency tradeoff
- [ ] Test on production data distribution
- [ ] Monitor P99 latency (not just average)
- [ ] Implement graceful degradation (exact fallback)
- [ ] Add caching for popular queries
- [ ] Set up alerts for recall drops
- [ ] Version indexes with data changes
- [ ] Plan for index rebuilds (blue-green deployment)

## Next Steps

1. **Experiment**: Test algorithms on your data
2. **Tune**: Find optimal parameters for your accuracy/speed needs
3. **Monitor**: Track recall and latency in production
4. **Iterate**: Retune as data distribution changes
