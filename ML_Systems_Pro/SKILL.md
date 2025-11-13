---
name: ml-systems-pro
description: |
  Production ML systems multi-modal CLIP similarity search MLOps feature store monitoring. Image-text fusion recommendation engine vector database hybrid search A/B testing. Use when: building ML system, similarity search engine, recommendation system, multi-modal AI, CLIP model, image search, cross-modal retrieval, embedding system, vector similarity, hybrid search, semantic search, MLOps pipeline, feature engineering, feature store, model serving, inference optimization, A/B testing, drift detection, model monitoring, production ML, scalable ML, real-time inference, batch processing, ML infrastructure.
---

# ML Systems Pro

Production-grade ML systems engineering covering multi-modal models, similarity engines, and enterprise MLOps workflows.

## Core Capabilities

### 1. Multi-Modal ML Systems
- CLIP-based image-text models
- Vision-language models (BLIP, LLaVA)
- Audio-visual fusion systems
- Cross-modal retrieval and search
- Multi-modal embeddings

### 2. Similarity Search Engines
- Embedding generation pipelines
- Vector similarity algorithms (cosine, euclidean, dot-product)
- Hybrid search (semantic + keyword + filters)
- Approximate nearest neighbor (ANN) search
- Recommendation systems

### 3. Production MLOps
- Feature stores (Feast, Tecton)
- Model monitoring and observability
- ML CI/CD pipelines
- A/B testing frameworks
- Data and model drift detection

### 4. Large-Scale ML Infrastructure
- Distributed model training
- Multi-model serving orchestration
- Caching and optimization strategies
- Auto-scaling inference systems

## Quick Start Templates

### Multi-Modal Systems
For cross-modal ML, see:
- `assets/templates/MultiModal/clip-image-text-search.py` - CLIP-based similarity search
- `assets/templates/MultiModal/multimodal-fusion-pipeline.py` - Audio-video-text fusion
- `assets/templates/MultiModal/cross-modal-retrieval-setup.md` - End-to-end retrieval system

### Similarity Engines
For similarity search, see:
- `assets/templates/SimilarityEngines/embedding-generation-pipeline.py` - Scalable embedding generation
- `assets/templates/SimilarityEngines/hybrid-search-engine.py` - Semantic + keyword search
- `assets/templates/SimilarityEngines/recommendation-system.py` - Collaborative filtering + embeddings
- `assets/templates/SimilarityEngines/ann-search-optimization.md` - HNSW, IVF, and LSH strategies

### MLOps Pipelines
For production ML, see:
- `assets/templates/MLOps/feature-store-setup.md` - Feast feature engineering
- `assets/templates/MLOps/model-monitoring-system.py` - Drift detection and alerting
- `assets/templates/MLOps/ml-cicd-pipeline.md` - Automated training and deployment

## References

### System Design
- `references/multimodal-architectures.md` - Design patterns for cross-modal systems
- `references/similarity-search-strategies.md` - Algorithm selection and optimization
- `references/production-ml-patterns.md` - MLOps best practices and anti-patterns

## Scripts

### Validation Tools
- `scripts/embedding_quality_analyzer.py` - Measure embedding quality and coverage
- `scripts/similarity_benchmarker.py` - Compare search algorithms performance

## Common Workflows

### CLIP-Based Image Search System

**Use Case**: E-commerce product search with natural language queries

1. **Generate embeddings**: Use CLIP to encode product images and descriptions
2. **Index vectors**: Store in vector database with metadata filters (category, price)
3. **Implement search**: Query with text, return similar images with ranking
4. **Optimize retrieval**: Use ANN algorithms (HNSW) for sub-50ms latency

**Architecture**:
```
User Query (text) → CLIP Text Encoder → Vector Search → Top-K Images
Product Images → CLIP Image Encoder → Vector Database
```

See `assets/templates/MultiModal/clip-image-text-search.py` for implementation.

### Multi-Modal Recommendation System

**Use Case**: Video streaming platform recommendations

1. **Feature extraction**: Extract visual (frames), audio (spectrograms), text (subtitles)
2. **Fusion strategy**: Early fusion (concatenate features) or late fusion (ensemble predictions)
3. **Similarity scoring**: Combine content-based (embeddings) + collaborative filtering (user interactions)
4. **Real-time serving**: Cache popular items, batch predictions for new content

See `assets/templates/SimilarityEngines/recommendation-system.py` for starter code.

### Production ML Monitoring

**Use Case**: Detect model degradation in production

1. **Feature store**: Centralize feature engineering with Feast
2. **Prediction logging**: Store inputs, outputs, timestamps, metadata
3. **Drift detection**: Monitor statistical drift (KS test, PSI) and performance metrics
4. **Alerting**: Trigger retraining when accuracy drops >5% or drift score exceeds threshold

**Monitoring Stack**:
```
Model Predictions → Kafka → Monitoring Service → Prometheus/Grafana
Ground Truth (delayed) → Accuracy Calculator → Alert Manager
```

See `assets/templates/MLOps/model-monitoring-system.py` for monitoring pipeline.

## Decision Trees

### Choose Multi-Modal Architecture
```
Need real-time inference? → CLIP (pre-trained, fast)
Custom domain (medical, industrial)? → Train vision-language model (BLIP, LLaVA)
Audio + video fusion? → Late fusion with separate encoders
Multiple modalities (3+)? → Transformer-based fusion (cross-attention)
```

### Choose Similarity Algorithm
```
Small dataset (<100K)? → Exact search (brute-force cosine)
Medium dataset (100K-10M)? → HNSW or IVF
Large dataset (>10M)? → Product quantization + IVF
High-dimensional sparse? → LSH (locality-sensitive hashing)
Need filters (category, date)? → Hybrid search with pre-filtering
```

### Choose Feature Store
```
Real-time features (<100ms)? → Redis or DynamoDB online store
Batch features (daily)? → S3 + Parquet offline store
Complex feature engineering? → Feast with custom transformations
Existing data warehouse? → Tecton with Snowflake/BigQuery
```

## Integration Patterns

### Multi-Modal Search Pipeline
```python
# CLIP-based image-text search
query = "red leather jacket"
query_embedding = clip_model.encode_text(query)

results = vector_db.search(
    vector=query_embedding,
    filters={"category": "clothing", "price_range": "50-200"},
    top_k=20
)
```

### Hybrid Search (Semantic + Keyword)
```python
# Combine vector similarity with keyword matching
semantic_results = vector_db.search(embedding, top_k=100)
keyword_results = elasticsearch.search(query, top_k=100)

final_results = rerank(
    semantic_results, 
    keyword_results, 
    weights=[0.7, 0.3]
)
```

### Real-Time Feature Store
```python
# Feast feature retrieval
from feast import FeatureStore

fs = FeatureStore(repo_path=".")
features = fs.get_online_features(
    entity_rows=[{"user_id": 123}],
    features=["user_profile:age", "user_profile:interests"]
).to_dict()
```

## Performance Optimization

### Embedding Generation at Scale
- **Batch processing**: Process 1K+ items per batch
- **GPU optimization**: Use FP16 mixed precision
- **Caching**: Store precomputed embeddings in Redis
- **Async processing**: Use Celery for background jobs

### Vector Search Latency
- **Index tuning**: HNSW M=16, efConstruction=200
- **Pre-filtering**: Apply metadata filters before vector search
- **Approximate search**: Trade 1-2% accuracy for 10x speed
- **Sharding**: Distribute vectors across multiple nodes

### Model Serving Throughput
- **Batching**: Accumulate requests for 10-50ms, batch predict
- **Model quantization**: INT8 for 2-3x throughput boost
- **Multi-model serving**: Use Triton for GPU sharing
- **Caching**: Cache predictions for popular queries (TTL 1-24hrs)

See `references/similarity-search-strategies.md` for detailed optimization techniques.

## Troubleshooting

### Multi-Modal Issues
**Symptom**: Poor cross-modal retrieval accuracy
- Verify embeddings are normalized (L2 norm = 1)
- Check modality balance (image vs text weights)
- Fine-tune on domain-specific data
- Increase embedding dimensions (512 → 768)

**Symptom**: Slow multi-modal inference
- Use ONNX for encoder optimization
- Batch encode multiple items together
- Cache popular item embeddings
- Consider distilled models (DistilCLIP)

### Similarity Search Issues
**Symptom**: Irrelevant search results
- Tune similarity threshold (e.g., cosine > 0.7)
- Implement hybrid search with keyword fallback
- Add metadata filtering (category, date)
- Retrain embeddings on domain data

**Symptom**: High search latency (>200ms)
- Switch to approximate search (HNSW)
- Reduce vector dimensions with PCA
- Use pre-filtering before vector search
- Implement result caching

### MLOps Issues
**Symptom**: Model performance degrading
- Check for data drift (feature distributions)
- Verify ground truth labels are correct
- Monitor prediction confidence scores
- Retrain on recent data (last 30-90 days)

**Symptom**: Feature store latency
- Cache frequently accessed features in Redis
- Pre-aggregate features (hourly/daily)
- Use online store for real-time, offline for batch
- Partition large feature tables

## Architecture Patterns

### Multi-Modal Retrieval System
```
Query (text/image) → Encoder → Embedding
    ↓
Vector Database (10M+ items)
    ↓
ANN Search (HNSW)
    ↓
Re-ranking (cross-encoder)
    ↓
Top-K Results
```

### Production ML Pipeline
```
Raw Data → Feature Store → Model Training
    ↓              ↓              ↓
Monitoring ← Model Serving ← Model Registry
    ↓
Drift Detection → Auto-Retrain
```

### Hybrid Search Engine
```
User Query
    ├─→ Text Encoder → Vector Search (semantic)
    └─→ Keyword Parser → Elasticsearch (keyword)
         ↓
    Result Fusion (RRF or learned ranking)
         ↓
    Final Ranked Results
```

## Production Considerations

### Scalability
- **Horizontal scaling**: Shard vectors across multiple nodes
- **Auto-scaling**: Scale inference pods based on request rate
- **Load balancing**: Use consistent hashing for cache hits
- **Data partitioning**: Partition by category or time range

### Reliability
- **Fallback strategies**: Keyword search when vector search fails
- **Circuit breakers**: Timeout after 500ms, return cached results
- **Redundancy**: Replicate vector indices across availability zones
- **Graceful degradation**: Return approximate results if exact search times out

### Cost Optimization
- **Spot instances**: Use for batch embedding generation
- **Model caching**: Reduce GPU inference with Redis cache
- **Quantization**: INT8 models for 50% memory savings
- **Cold storage**: Archive old embeddings to S3 Glacier

### Security
- **Input validation**: Sanitize user queries to prevent injection
- **Rate limiting**: Throttle requests to prevent abuse
- **Encryption**: Encrypt embeddings at rest and in transit
- **Access control**: Implement RBAC for feature store and models

## Monitoring Metrics

### Model Performance
- **Accuracy**: Track precision, recall, F1 on holdout set
- **Latency**: P50, P95, P99 inference times
- **Throughput**: Requests per second, batch sizes
- **Error rate**: Failed predictions, timeouts

### System Health
- **Resource usage**: CPU, GPU, memory utilization
- **Cache hit rate**: Redis cache effectiveness (target >80%)
- **Queue depth**: Async processing backlog
- **Database latency**: Vector search response times

### Business Metrics
- **Search relevance**: Click-through rate, conversion rate
- **User engagement**: Time on page, bounce rate
- **Revenue impact**: GMV, average order value
- **Cost per request**: Infrastructure costs per 1K requests

## Next Steps

For basic ML training and deployment, see **AI_Engineer_Pro** skill.

For web application integration, see **Web_Architect_Pro** skill.

For mobile app integration, see **Mobile_Architect_Pro** skill.
