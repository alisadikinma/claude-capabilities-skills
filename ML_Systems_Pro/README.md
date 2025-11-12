# ML Systems Pro

**Production-grade ML systems engineering for multi-modal models, similarity engines, and enterprise MLOps.**

## Overview

ML_Systems_Pro extends Claude's capabilities for building production ML systems beyond basic training. It covers:

- **Multi-modal ML**: CLIP, BLIP, vision-language models, cross-modal retrieval
- **Similarity Engines**: Embedding systems, vector search, hybrid search, recommendations
- **Production MLOps**: Feature stores, monitoring, CI/CD, drift detection, A/B testing

## When to Use This Skill

Use ML_Systems_Pro when you need to:
- Build image-text search systems with CLIP
- Design multi-modal recommendation engines
- Implement production-grade similarity search
- Set up feature stores (Feast, Tecton)
- Monitor model performance and detect drift
- Optimize large-scale vector search
- Build real-time ML inference systems

For basic ML training and deployment, use **AI_Engineer_Pro** instead.

## Quick Start

### Multi-Modal Image Search
```python
# See: assets/templates/MultiModal/clip-image-text-search.py
query = "red leather jacket"
results = search_engine.search(query, filters={"category": "clothing"})
```

### Hybrid Similarity Search
```python
# See: assets/templates/SimilarityEngines/hybrid-search-engine.py
results = hybrid_search(
    query="machine learning books",
    semantic_weight=0.7,
    keyword_weight=0.3
)
```

### Feature Store Setup
```python
# See: assets/templates/MLOps/feature-store-setup.md
features = fs.get_online_features(
    entity_rows=[{"user_id": 123}],
    features=["user_profile:age", "user_profile:interests"]
)
```

## File Structure

```
ML_Systems_Pro/
├── SKILL.md                          # Main skill documentation
├── README.md                         # This file
├── assets/templates/
│   ├── MultiModal/                   # CLIP, BLIP, fusion systems
│   ├── SimilarityEngines/            # Vector search, recommendations
│   └── MLOps/                        # Feature stores, monitoring
├── references/                       # Deep-dive guides
└── scripts/                          # Validation tools
```

## Key Features

### 1. Multi-Modal ML
- **CLIP Integration**: Image-text similarity search
- **Vision-Language Models**: BLIP, LLaVA for captioning and VQA
- **Audio-Visual Fusion**: Combine multiple modalities
- **Cross-Modal Retrieval**: Search images with text, videos with audio

### 2. Similarity Search
- **Embedding Pipelines**: Generate and store embeddings at scale
- **Vector Algorithms**: HNSW, IVF, LSH for fast nearest neighbor search
- **Hybrid Search**: Combine semantic + keyword + filters
- **Recommendations**: Collaborative filtering + content-based

### 3. Production MLOps
- **Feature Stores**: Feast and Tecton for feature management
- **Model Monitoring**: Drift detection, performance tracking
- **CI/CD Pipelines**: Automated training and deployment
- **A/B Testing**: Compare model versions in production

## Common Use Cases

### E-Commerce Search
Build visual search where users query with text or images:
```
"show me red dresses under $100" → Image results ranked by similarity
```

### Video Recommendations
Multi-modal recommendation combining visual, audio, and text features:
```
Watch history + Preferences → Similar videos with cross-modal fusion
```

### Production Model Monitoring
Detect when models degrade due to data drift:
```
Model Predictions → Monitoring → Alert if accuracy drops >5%
```

## Integration Examples

### With Vector Databases
```python
# Index embeddings in pgvector/Pinecone/ChromaDB
embeddings = model.encode(items)
vector_db.upsert(vectors=embeddings, metadata=metadata)
```

### With Web APIs
```python
# FastAPI endpoint for similarity search
@app.post("/search")
async def search(query: str):
    embedding = encoder.encode(query)
    results = vector_db.search(embedding, top_k=20)
    return results
```

### With Streaming Data
```python
# Real-time feature updates
producer.send("features", {
    "user_id": 123,
    "feature": "last_purchase_time",
    "value": timestamp
})
```

## Templates Available

### Multi-Modal (3 files)
1. `clip-image-text-search.py` - CLIP-based similarity search
2. `multimodal-fusion-pipeline.py` - Audio-video-text fusion
3. `cross-modal-retrieval-setup.md` - End-to-end retrieval system

### Similarity Engines (4 files)
1. `embedding-generation-pipeline.py` - Scalable embedding generation
2. `hybrid-search-engine.py` - Semantic + keyword search
3. `recommendation-system.py` - Collaborative filtering + embeddings
4. `ann-search-optimization.md` - HNSW, IVF, and LSH strategies

### MLOps (3 files)
1. `feature-store-setup.md` - Feast feature engineering
2. `model-monitoring-system.py` - Drift detection and alerting
3. `ml-cicd-pipeline.md` - Automated training and deployment

## References

- `multimodal-architectures.md` - Design patterns for cross-modal systems
- `similarity-search-strategies.md` - Algorithm selection and optimization
- `production-ml-patterns.md` - MLOps best practices and anti-patterns

## Scripts

- `embedding_quality_analyzer.py` - Measure embedding quality and coverage
- `similarity_benchmarker.py` - Compare search algorithms performance

## Performance Targets

- **Search latency**: <50ms for ANN search with 10M vectors
- **Embedding generation**: 1K+ items/batch on single GPU
- **Cache hit rate**: >80% for popular queries
- **Model serving**: 100+ QPS per GPU instance

## Tech Stack

### Multi-Modal Models
- CLIP, BLIP, LLaVA, ImageBind
- sentence-transformers, transformers

### Vector Databases
- pgvector, Pinecone, ChromaDB, Weaviate, Milvus

### MLOps Tools
- Feast, Tecton (feature stores)
- MLflow, Weights & Biases (experiment tracking)
- Prometheus, Grafana (monitoring)
- Airflow, Prefect (orchestration)

## Best Practices

1. **Normalize embeddings**: L2 norm = 1 for cosine similarity
2. **Batch predictions**: 10-50ms batching window for throughput
3. **Cache aggressively**: Redis for popular items (80%+ hit rate)
4. **Monitor drift**: Check feature distributions weekly
5. **Use ANN search**: Exact search only for <100K vectors
6. **Hybrid search**: Combine semantic + keyword for best results

## Troubleshooting

### Poor Search Quality
- Fine-tune embeddings on domain data
- Increase embedding dimensions (512 → 768)
- Implement hybrid search with keyword fallback
- Add metadata filtering

### High Latency
- Switch to approximate search (HNSW)
- Reduce vector dimensions with PCA
- Implement caching layer
- Use pre-filtering

### Model Degradation
- Monitor for data drift (KS test, PSI)
- Retrain on recent data (30-90 days)
- Check ground truth quality
- Validate feature engineering

## Related Skills

- **AI_Engineer_Pro**: Basic ML training and deployment
- **Web_Architect_Pro**: Web API integration
- **DevOps_Master**: Infrastructure and scaling

## Contributing

Improvements welcome for:
- New multi-modal architectures
- Advanced similarity algorithms
- MLOps patterns and tools
- Performance optimization techniques

---

**Version**: 1.0.0  
**Status**: ✅ Complete  
**Last Updated**: January 2025
