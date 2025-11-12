# Cross-Modal Retrieval System Setup

Complete guide for building production cross-modal retrieval systems that enable searching across different modalities (e.g., find images using text, find videos using audio).

## Architecture Overview

```
Query (any modality) → Encoder → Embedding Space → Vector Search → Results (different modality)
```

**Key Components:**
1. **Encoders**: Transform each modality into shared embedding space
2. **Shared Embedding Space**: Common representation for all modalities
3. **Vector Database**: Store and search embeddings efficiently
4. **Ranking**: Re-rank results using cross-encoder or business logic

## Use Cases

- **Text → Image**: "Show me sunset images" → Beach photos
- **Image → Text**: Upload product photo → Related descriptions
- **Audio → Video**: Hum a tune → Music videos with that melody
- **Video → Text**: Upload video clip → Similar articles/descriptions

## Model Selection

### Text-Image Retrieval
```python
# CLIP: Best for general-purpose text-image search
from transformers import CLIPModel, CLIPProcessor

model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

# BLIP: Better for detailed image understanding
from transformers import BlipModel, BlipProcessor

model = BlipModel.from_pretrained("Salesforce/blip-image-captioning-large")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
```

### Audio-Visual Retrieval
```python
# ImageBind: Supports 6 modalities (image, text, audio, depth, thermal, IMU)
import torch
from imagebind import data as imagebind_data
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType

model = imagebind_model.imagebind_huge(pretrained=True)
model.eval()
```

## Implementation Steps

### 1. Encode All Items

**For Images:**
```python
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def encode_images(image_paths, batch_size=32):
    embeddings = []
    
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i+batch_size]
        images = [Image.open(p).convert("RGB") for p in batch]
        
        inputs = processor(images=images, return_tensors="pt")
        with torch.no_grad():
            features = model.get_image_features(**inputs)
            # L2 normalize
            features = features / features.norm(dim=-1, keepdim=True)
            embeddings.append(features.cpu().numpy())
    
    return np.vstack(embeddings)
```

**For Text:**
```python
def encode_texts(texts, batch_size=32):
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        
        inputs = processor(text=batch, return_tensors="pt", padding=True)
        with torch.no_grad():
            features = model.get_text_features(**inputs)
            features = features / features.norm(dim=-1, keepdim=True)
            embeddings.append(features.cpu().numpy())
    
    return np.vstack(embeddings)
```

### 2. Store in Vector Database

**Using FAISS (Local):**
```python
import faiss
import numpy as np

# Create index
dimension = embeddings.shape[1]  # 512 for CLIP-base
index = faiss.IndexFlatIP(dimension)  # Inner product = cosine similarity

# Add embeddings
index.add(embeddings.astype(np.float32))

# Save index
faiss.write_index(index, "image_embeddings.index")
```

**Using Pinecone (Cloud):**
```python
import pinecone

# Initialize
pinecone.init(api_key="YOUR_API_KEY", environment="us-west1-gcp")
index = pinecone.Index("cross-modal-search")

# Upsert embeddings
vectors = [
    (str(i), emb.tolist(), {"path": path, "type": "image"})
    for i, (emb, path) in enumerate(zip(embeddings, image_paths))
]

index.upsert(vectors=vectors, batch_size=100)
```

**Using pgvector (PostgreSQL):**
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

engine = create_engine("postgresql://user:pass@localhost/dbname")
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    modality = Column(String)  # "image", "text", "audio"
    embedding = Column(Vector(512))

Base.metadata.create_all(engine)

# Insert items
from sqlalchemy.orm import Session
session = Session(engine)

for path, emb in zip(image_paths, embeddings):
    item = Item(path=path, modality="image", embedding=emb.tolist())
    session.add(item)

session.commit()
```

### 3. Query Across Modalities

**Text Query → Image Results:**
```python
def search_images_by_text(query_text, top_k=10):
    # Encode query
    query_emb = encode_texts([query_text])[0]
    
    # Search FAISS
    scores, indices = index.search(
        query_emb.reshape(1, -1).astype(np.float32),
        top_k
    )
    
    results = [
        {"path": image_paths[idx], "score": float(score)}
        for score, idx in zip(scores[0], indices[0])
    ]
    
    return results

# Usage
results = search_images_by_text("red sports car", top_k=5)
```

**Image Query → Text Results:**
```python
def search_texts_by_image(image_path, top_k=10):
    # Encode query image
    query_emb = encode_images([image_path])[0]
    
    # Search text embeddings
    scores, indices = text_index.search(
        query_emb.reshape(1, -1).astype(np.float32),
        top_k
    )
    
    results = [
        {"text": texts[idx], "score": float(score)}
        for score, idx in zip(scores[0], indices[0])
    ]
    
    return results
```

### 4. Hybrid Search (Semantic + Keyword)

Combine vector similarity with traditional keyword search for best results:

```python
from rank_bm25 import BM25Okapi
import numpy as np

class HybridCrossModalSearch:
    def __init__(self, semantic_weight=0.7):
        self.semantic_weight = semantic_weight
        self.keyword_weight = 1 - semantic_weight
        
        # BM25 for keyword matching
        self.bm25 = BM25Okapi(tokenized_corpus)
    
    def search(self, query, top_k=10):
        # Semantic search
        semantic_results = self.semantic_search(query, top_k * 2)
        
        # Keyword search
        keyword_results = self.keyword_search(query, top_k * 2)
        
        # Merge with weighted scores
        combined_scores = {}
        
        for result in semantic_results:
            combined_scores[result["id"]] = (
                self.semantic_weight * result["score"]
            )
        
        for result in keyword_results:
            if result["id"] in combined_scores:
                combined_scores[result["id"]] += (
                    self.keyword_weight * result["score"]
                )
            else:
                combined_scores[result["id"]] = (
                    self.keyword_weight * result["score"]
                )
        
        # Sort by combined score
        sorted_ids = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        return [{"id": id, "score": score} for id, score in sorted_ids]
```

## Advanced Techniques

### Re-Ranking with Cross-Encoder

Use a cross-encoder for more accurate ranking of top candidates:

```python
from sentence_transformers import CrossEncoder

# Initialize cross-encoder
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_results(query, candidates, top_k=10):
    # Get top 100 from vector search
    initial_results = vector_search(query, top_k=100)
    
    # Create pairs for cross-encoder
    pairs = [(query, candidate["text"]) for candidate in initial_results]
    
    # Score with cross-encoder
    scores = cross_encoder.predict(pairs)
    
    # Sort by cross-encoder score
    reranked = sorted(
        zip(initial_results, scores),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]
    
    return [
        {"text": result["text"], "score": float(score)}
        for result, score in reranked
    ]
```

### Metadata Filtering

Add metadata filters to narrow search space:

```python
def search_with_filters(query, filters, top_k=10):
    # Example filters: {"category": "electronics", "price_range": "100-500"}
    
    if using_pinecone:
        query_emb = encode_texts([query])[0]
        results = index.query(
            vector=query_emb.tolist(),
            top_k=top_k,
            filter={
                "category": {"$eq": filters.get("category")},
                "price": {"$gte": 100, "$lte": 500}
            }
        )
    
    elif using_pgvector:
        query_emb = encode_texts([query])[0]
        results = session.query(Item).filter(
            Item.category == filters.get("category"),
            Item.price.between(100, 500)
        ).order_by(
            Item.embedding.cosine_distance(query_emb)
        ).limit(top_k).all()
    
    return results
```

## Performance Optimization

### Batch Processing
```python
# Process 1000+ items per batch
batch_size = 1000
embeddings = []

for i in tqdm(range(0, len(items), batch_size)):
    batch = items[i:i+batch_size]
    batch_embeddings = encode_batch(batch)
    embeddings.append(batch_embeddings)
```

### Caching
```python
import redis
import pickle

cache = redis.Redis(host="localhost", port=6379)

def get_cached_embedding(item_id):
    cached = cache.get(f"emb:{item_id}")
    if cached:
        return pickle.loads(cached)
    return None

def cache_embedding(item_id, embedding, ttl=86400):
    cache.setex(
        f"emb:{item_id}",
        ttl,  # 24 hours
        pickle.dumps(embedding)
    )
```

### Approximate Search (HNSW)
```python
import faiss

# Use HNSW for faster approximate search
dimension = 512
M = 16  # Number of connections
ef_construction = 200

index = faiss.IndexHNSWFlat(dimension, M)
index.hnsw.efConstruction = ef_construction
index.add(embeddings.astype(np.float32))

# Search
index.hnsw.efSearch = 50  # Higher = more accurate, slower
scores, indices = index.search(query_emb, top_k)
```

## Production Deployment

### FastAPI Endpoint
```python
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    modality: str  # "text" or "image"
    top_k: int = 10

@app.post("/search")
async def search(request: SearchRequest):
    if request.modality == "text":
        results = search_by_text(request.query, request.top_k)
    elif request.modality == "image":
        results = search_by_image(request.query, request.top_k)
    
    return {"results": results}

@app.post("/search/image")
async def search_with_image(file: UploadFile, top_k: int = 10):
    # Save uploaded image
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    # Search
    results = search_texts_by_image(temp_path, top_k)
    
    return {"results": results}
```

### Monitoring
```python
import time
from prometheus_client import Counter, Histogram

search_counter = Counter("searches_total", "Total searches")
search_latency = Histogram("search_latency_seconds", "Search latency")

@search_latency.time()
def search(query, top_k):
    search_counter.inc()
    # ... search logic
    return results
```

## Troubleshooting

### Poor Cross-Modal Accuracy
- **Solution**: Fine-tune model on domain-specific data
- Use larger models (CLIP-large instead of CLIP-base)
- Increase embedding dimensions
- Try different fusion strategies

### High Latency
- **Solution**: Use approximate search (HNSW, IVF)
- Cache popular queries
- Batch encode items
- Use quantization (FP16 or INT8)

### Irrelevant Results
- **Solution**: Implement hybrid search (semantic + keyword)
- Add re-ranking with cross-encoder
- Use metadata filtering
- Tune similarity thresholds

## Next Steps

1. **Scale**: Distribute vectors across multiple nodes
2. **Monitor**: Track search quality and latency
3. **Optimize**: Profile bottlenecks, optimize encoders
4. **Iterate**: A/B test different models and strategies
