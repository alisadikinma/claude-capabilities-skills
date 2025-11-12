# Similarity Search Strategies

Comprehensive guide for implementing and optimizing similarity search systems at scale.

## Fundamentals

### Similarity Metrics

**Cosine Similarity** (most common for embeddings):
```python
similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Or with L2-normalized vectors:
similarity = np.dot(a, b)  # Faster!
```

**Euclidean Distance:**
```python
distance = np.linalg.norm(a - b)
# Lower = more similar
```

**Dot Product:**
```python
similarity = np.dot(a, b)
# For non-normalized vectors
```

**When to Use Which:**
- **Cosine:** Embeddings (sentence-transformers, CLIP)
- **Euclidean:** Low-dimensional data, spatial coordinates
- **Dot Product:** Large embeddings with magnitude info

## Search Algorithms

### 1. Exact Search (Brute Force)

**Implementation:**
```python
import numpy as np

def exact_search(query, database, top_k=10):
    """
    O(n) complexity - compares against all vectors.
    """
    # Assume L2-normalized vectors
    similarities = database @ query  # (N,) array
    top_indices = np.argpartition(-similarities, top_k)[:top_k]
    top_indices = top_indices[np.argsort(-similarities[top_indices])]
    
    return top_indices, similarities[top_indices]
```

**When to Use:**
- Database < 100K vectors
- Need 100% accuracy
- Low query volume

### 2. HNSW (Hierarchical Navigable Small World)

**Best General-Purpose Algorithm**

```python
import faiss

dimension = 512
M = 16  # Connections per node
ef_construction = 200
ef_search = 50

index = faiss.IndexHNSWFlat(dimension, M)
index.hnsw.efConstruction = ef_construction
index.add(vectors)

index.hnsw.efSearch = ef_search
distances, indices = index.search(queries, k=10)
```

**Tuning Guide:**
| Parameter | Low | Medium | High | Effect |
|-----------|-----|--------|------|--------|
| M | 8 | 16 | 32 | Accuracy, memory |
| efConstruction | 100 | 200 | 400 | Index quality, build time |
| efSearch | 20 | 50 | 200 | Query accuracy, latency |

**Performance Profile:**
- Build: O(n log n)
- Query: O(log n)
- Memory: 2-3x vector size
- Accuracy: 95-99%

### 3. IVF (Inverted File Index)

**Best for GPU Acceleration**

```python
import faiss

nlist = 1000  # Number of clusters
nprobe = 10   # Clusters to search

quantizer = faiss.IndexFlatL2(dimension)
index = faiss.IndexIVFFlat(quantizer, dimension, nlist)

# Train (required)
index.train(training_vectors)
index.add(vectors)

# Search
index.nprobe = nprobe
distances, indices = index.search(queries, k=10)
```

**Tuning Guide:**
- nlist = sqrt(n_vectors) as starting point
- nprobe = 1-10% of nlist
- Higher nprobe = better accuracy, slower search

**GPU Acceleration:**
```python
res = faiss.StandardGpuResources()
gpu_index = faiss.index_cpu_to_gpu(res, 0, cpu_index)
# 10-100x faster on large datasets
```

### 4. Product Quantization (PQ)

**Best for Memory Constraints**

```python
import faiss

m = 64        # Subvectors
nbits = 8     # Bits per subquantizer

index = faiss.IndexPQ(dimension, m, nbits)
index.train(training_vectors)
index.add(vectors)

distances, indices = index.search(queries, k=10)
```

**Compression:**
- 512D float32 = 2KB
- PQ (m=64, nbits=8) = 64 bytes
- **32x compression!**

**Accuracy Trade-off:**
- 5-10% accuracy loss
- Combine with IVF for speed + compression

## Hybrid Search Strategies

### 1. Semantic + Keyword

**Reciprocal Rank Fusion (RRF):**
```python
def reciprocal_rank_fusion(semantic_results, keyword_results, k=60):
    """
    Combine rankings from different search methods.
    """
    scores = {}
    
    for rank, (doc_id, _) in enumerate(semantic_results, 1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    
    for rank, (doc_id, _) in enumerate(keyword_results, 1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

**Weighted Fusion:**
```python
def weighted_fusion(semantic_results, keyword_results, alpha=0.7):
    """
    Weighted combination of normalized scores.
    """
    scores = {}
    
    # Normalize semantic scores
    max_sem = max(s for _, s in semantic_results)
    for doc_id, score in semantic_results:
        scores[doc_id] = alpha * (score / max_sem)
    
    # Normalize keyword scores
    max_kw = max(s for _, s in keyword_results)
    for doc_id, score in keyword_results:
        scores[doc_id] = scores.get(doc_id, 0) + (1 - alpha) * (score / max_kw)
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### 2. Two-Stage Search

**Stage 1: Fast ANN (high recall)**
```python
# Get 100 candidates quickly
coarse_results = hnsw_index.search(query, k=100)
```

**Stage 2: Precise Re-ranking (high precision)**
```python
# Re-rank with expensive model
candidates = vectors[coarse_results]
precise_scores = cross_encoder.predict([(query, c) for c in candidates])
final_indices = np.argsort(-precise_scores)[:10]
```

**Benefits:**
- 10x speed vs exact cross-encoder on all docs
- 99%+ accuracy vs exact search

### 3. Filtered Search

**Pre-filtering (before vector search):**
```python
def filtered_search(query, filters, top_k=10):
    """
    Apply filters before vector search.
    Fast when filter is selective (<10% of data).
    """
    # Filter by metadata
    filtered_indices = [
        i for i, item in enumerate(items)
        if item['category'] == filters['category']
    ]
    
    # Search only filtered subset
    filtered_vectors = vectors[filtered_indices]
    similarities = filtered_vectors @ query
    
    top_k_in_filtered = np.argsort(-similarities)[:top_k]
    return filtered_indices[top_k_in_filtered]
```

**Post-filtering (after vector search):**
```python
def postfiltered_search(query, filters, top_k=10):
    """
    Filter after vector search.
    Fast when filter is not selective (>50% of data).
    """
    # Fetch more candidates
    candidates = index.search(query, k=top_k * 3)
    
    # Filter results
    filtered = [
        c for c in candidates
        if items[c]['category'] == filters['category']
    ]
    
    return filtered[:top_k]
```

## Optimization Techniques

### 1. Query Batching

```python
def batch_search(queries, batch_size=32, top_k=10):
    """
    Process multiple queries together.
    10-50x faster than individual queries.
    """
    results = []
    
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]
        batch_results = index.search(np.vstack(batch), k=top_k)
        results.extend(batch_results)
    
    return results
```

### 2. Result Caching

```python
import redis
import hashlib

cache = redis.Redis()

def cached_search(query, top_k=10, ttl=3600):
    """
    Cache search results for popular queries.
    """
    # Generate cache key
    query_hash = hashlib.md5(query.tobytes()).hexdigest()
    cache_key = f"search:{query_hash}:{top_k}"
    
    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return pickle.loads(cached)
    
    # Perform search
    results = index.search(query, k=top_k)
    
    # Cache results
    cache.setex(cache_key, ttl, pickle.dumps(results))
    
    return results
```

### 3. Query Expansion

```python
def expand_query(query, expansion_model, top_expansions=3):
    """
    Add related terms to improve recall.
    """
    # Generate expansions
    expansions = expansion_model.predict(query, k=top_expansions)
    
    # Combine query with expansions
    expanded_queries = [query] + expansions
    
    # Search with each, combine results
    all_results = []
    for q in expanded_queries:
        results = search(q, top_k=20)
        all_results.extend(results)
    
    # Deduplicate and rerank
    unique_results = deduplicate(all_results)
    return rerank(unique_results, original_query=query)[:10]
```

### 4. Dimensionality Reduction

```python
from sklearn.decomposition import PCA

# Reduce 768D → 256D (3x memory savings)
pca = PCA(n_components=256)
pca.fit(training_embeddings)

# Transform vectors
reduced_vectors = pca.transform(vectors)

# 1-2% accuracy loss, 3x faster search
```

## Multi-Vector Search

### Representing Documents as Multiple Vectors

**ColBERT-style:**
```python
def encode_document_multitoken(document, model):
    """
    Each token gets an embedding.
    """
    tokens = tokenize(document)
    token_embeddings = model.encode(tokens)  # (num_tokens, dim)
    return token_embeddings

def multivector_search(query, doc_embeddings_list, top_k=10):
    """
    MaxSim: Max similarity between query and any doc token.
    """
    query_emb = model.encode(query)
    
    scores = []
    for doc_embeddings in doc_embeddings_list:
        # Max similarity over all token pairs
        similarities = query_emb @ doc_embeddings.T
        max_sim = similarities.max()
        scores.append(max_sim)
    
    top_indices = np.argsort(-np.array(scores))[:top_k]
    return top_indices
```

**Benefits:**
- Better for long documents
- More nuanced matching
- Higher accuracy (+5-10%)

**Costs:**
- 10-100x more vectors to store
- Slower search (can optimize with IVF)

## Evaluation Strategies

### 1. Recall@K

```python
def compute_recall_at_k(predicted, ground_truth, k=10):
    """
    Proportion of relevant items in top-K.
    """
    recall_scores = []
    
    for pred, truth in zip(predicted, ground_truth):
        relevant_in_topk = len(set(pred[:k]) & set(truth))
        recall = relevant_in_topk / min(k, len(truth))
        recall_scores.append(recall)
    
    return np.mean(recall_scores)
```

### 2. Mean Reciprocal Rank (MRR)

```python
def compute_mrr(predicted, ground_truth):
    """
    Average of 1/rank of first relevant item.
    """
    mrr_scores = []
    
    for pred, truth in zip(predicted, ground_truth):
        for rank, doc_id in enumerate(pred, 1):
            if doc_id in truth:
                mrr_scores.append(1 / rank)
                break
        else:
            mrr_scores.append(0)
    
    return np.mean(mrr_scores)
```

### 3. nDCG (Normalized Discounted Cumulative Gain)

```python
def compute_ndcg(predicted, relevance_scores, k=10):
    """
    Position-weighted relevance metric.
    """
    dcg = sum(
        rel / np.log2(i + 2)
        for i, rel in enumerate(relevance_scores[:k])
    )
    
    ideal_scores = sorted(relevance_scores, reverse=True)
    idcg = sum(
        rel / np.log2(i + 2)
        for i, rel in enumerate(ideal_scores[:k])
    )
    
    return dcg / idcg if idcg > 0 else 0
```

## Production Patterns

### 1. Sharded Search

```python
class ShardedIndex:
    """
    Distribute vectors across multiple shards.
    """
    def __init__(self, num_shards=4):
        self.shards = [faiss.IndexFlatIP(dimension) for _ in range(num_shards)]
        self.num_shards = num_shards
    
    def add(self, vectors):
        # Distribute vectors across shards
        for i, vector in enumerate(vectors):
            shard_id = i % self.num_shards
            self.shards[shard_id].add(vector.reshape(1, -1))
    
    def search(self, query, k=10):
        # Search all shards in parallel
        all_results = []
        
        for shard in self.shards:
            distances, indices = shard.search(query, k=k)
            all_results.append((distances[0], indices[0]))
        
        # Merge results
        merged = merge_results(all_results, k)
        return merged
```

### 2. Incremental Updates

```python
class IncrementalIndex:
    """
    Support adding vectors without full rebuild.
    """
    def __init__(self):
        self.main_index = faiss.IndexHNSWFlat(dimension, M=16)
        self.buffer = []
        self.buffer_limit = 10000
    
    def add(self, vector):
        self.buffer.append(vector)
        
        # Merge buffer when full
        if len(self.buffer) >= self.buffer_limit:
            self.merge_buffer()
    
    def merge_buffer(self):
        buffer_array = np.vstack(self.buffer)
        self.main_index.add(buffer_array)
        self.buffer = []
    
    def search(self, query, k=10):
        # Search main index
        main_results = self.main_index.search(query, k=k)
        
        # Search buffer (brute force)
        if self.buffer:
            buffer_array = np.vstack(self.buffer)
            buffer_results = exact_search(query, buffer_array, k=k)
            
            # Merge results
            return merge_results([main_results, buffer_results], k)
        
        return main_results
```

### 3. Blue-Green Deployment

```python
class BlueGreenIndex:
    """
    Zero-downtime index updates.
    """
    def __init__(self):
        self.blue_index = load_index("blue.index")
        self.green_index = None
        self.active = "blue"
    
    def rebuild_index(self, new_vectors):
        """
        Build new index without affecting live traffic.
        """
        # Build green index
        self.green_index = faiss.IndexHNSWFlat(dimension, M=16)
        self.green_index.add(new_vectors)
        
        # Validate green index
        assert validate_index(self.green_index)
        
        # Atomic switch
        self.active = "green"
        
        # Clean up old index
        del self.blue_index
        self.blue_index = self.green_index
        self.green_index = None
        self.active = "blue"
    
    def search(self, query, k=10):
        if self.active == "blue":
            return self.blue_index.search(query, k)
        else:
            return self.green_index.search(query, k)
```

## Troubleshooting Guide

### Low Recall
1. Increase efSearch (HNSW) or nprobe (IVF)
2. Check embedding quality (cosine sim distribution)
3. Verify L2 normalization
4. Try exact search on sample to isolate issue

### High Latency
1. Reduce efSearch or nprobe
2. Use GPU (IVF)
3. Add caching layer
4. Batch queries
5. Consider PQ compression

### High Memory Usage
1. Use Product Quantization
2. Reduce embedding dimensions (PCA)
3. Shard across machines
4. Use mmap for on-disk storage

### Inconsistent Results
1. Set random seeds
2. Use deterministic build
3. Check for race conditions in multi-threaded code
4. Verify vector normalization

## Next Steps

1. **Baseline:** Start with exact search
2. **Scale:** Add HNSW when > 100K vectors
3. **Optimize:** Profile and optimize bottlenecks
4. **Monitor:** Track recall, latency, memory
5. **Iterate:** A/B test algorithm changes
