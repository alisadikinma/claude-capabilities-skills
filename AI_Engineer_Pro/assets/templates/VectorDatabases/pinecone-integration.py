"""
Pinecone Cloud Vector Database Integration
Serverless vector search at scale
"""

from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Pinecone
pc = Pinecone(api_key="your-api-key")

# Create index
index_name = "pcb-defects"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # Match your embedding model
        metric="cosine",  # or "euclidean", "dotproduct"
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to index
index = pc.Index(index_name)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# ========================================
# Insert Vectors
# ========================================

# Single insert
documents = [
    {"id": "doc1", "text": "PCB scratch on component A", "metadata": {"type": "scratch", "severity": 3}},
    {"id": "doc2", "text": "Solder bridge detected", "metadata": {"type": "solder_bridge", "severity": 5}},
    {"id": "doc3", "text": "Missing component C12", "metadata": {"type": "missing", "severity": 4}},
]

# Generate embeddings
embeddings = model.encode([doc["text"] for doc in documents])

# Prepare vectors for upsert
vectors = [
    {
        "id": doc["id"],
        "values": emb.tolist(),
        "metadata": {
            "text": doc["text"],
            **doc["metadata"]
        }
    }
    for doc, emb in zip(documents, embeddings)
]

# Upsert to Pinecone
index.upsert(vectors=vectors)

# Batch upsert (for large datasets)
def batch_upsert(documents, batch_size=100):
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        
        # Generate embeddings
        texts = [doc["text"] for doc in batch]
        embeddings = model.encode(texts)
        
        # Prepare vectors
        vectors = [
            {
                "id": doc["id"],
                "values": emb.tolist(),
                "metadata": {"text": doc["text"], **doc.get("metadata", {})}
            }
            for doc, emb in zip(batch, embeddings)
        ]
        
        # Upsert
        index.upsert(vectors=vectors)
        print(f"Upserted batch {i//batch_size + 1}")

# ========================================
# Query (Similarity Search)
# ========================================

def search(query_text, top_k=5, filter_dict=None):
    """
    Search for similar vectors
    
    Args:
        query_text: Query string
        top_k: Number of results
        filter_dict: Metadata filter (e.g., {"type": "scratch"})
    """
    # Generate query embedding
    query_embedding = model.encode(query_text)
    
    # Search
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True,
        filter=filter_dict
    )
    
    return results

# Basic search
results = search("What are the defects on the PCB?", top_k=3)

for match in results['matches']:
    print(f"Score: {match['score']:.3f}")
    print(f"Text: {match['metadata']['text']}")
    print(f"Type: {match['metadata'].get('type', 'N/A')}")
    print("---")

# Search with filter
results = search(
    "PCB defects",
    top_k=5,
    filter_dict={"type": {"$eq": "scratch"}, "severity": {"$gte": 3}}
)

# ========================================
# Metadata Filtering
# ========================================

# Operators: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin

# Example filters
filter_examples = {
    "exact_match": {"type": {"$eq": "scratch"}},
    "not_equal": {"type": {"$ne": "missing"}},
    "greater_than": {"severity": {"$gt": 3}},
    "in_list": {"type": {"$in": ["scratch", "crack"]}},
    "and_condition": {
        "$and": [
            {"type": {"$eq": "scratch"}},
            {"severity": {"$gte": 4}}
        ]
    },
    "or_condition": {
        "$or": [
            {"type": "scratch"},
            {"type": "crack"}
        ]
    }
}

# ========================================
# Update & Delete
# ========================================

# Update metadata
index.update(
    id="doc1",
    set_metadata={"severity": 5, "inspected": True}
)

# Delete vector
index.delete(ids=["doc1"])

# Delete by filter
index.delete(filter={"type": {"$eq": "scratch"}})

# Delete all
index.delete(delete_all=True)

# ========================================
# Fetch Vectors
# ========================================

# Fetch by IDs
vectors = index.fetch(ids=["doc1", "doc2"])

for id, vector_data in vectors['vectors'].items():
    print(f"ID: {id}")
    print(f"Metadata: {vector_data['metadata']}")

# ========================================
# Stats
# ========================================

stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
print(f"Dimension: {stats['dimension']}")

# ========================================
# Namespaces (Multi-tenancy)
# ========================================

# Insert to namespace
index.upsert(
    vectors=vectors,
    namespace="customer_A"
)

# Query namespace
results = index.query(
    vector=query_embedding.tolist(),
    top_k=5,
    namespace="customer_A"
)

# Delete namespace
index.delete(delete_all=True, namespace="customer_A")

# ========================================
# Best Practices
# ========================================

class PineconeManager:
    """Production-ready Pinecone manager"""
    
    def __init__(self, api_key, index_name, embedding_model):
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(index_name)
        self.model = SentenceTransformer(embedding_model)
    
    def upsert_with_retry(self, vectors, max_retries=3):
        """Upsert with retry logic"""
        for attempt in range(max_retries):
            try:
                self.index.upsert(vectors=vectors)
                return True
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
        return False
    
    def search_with_cache(self, query, top_k=5, cache=None):
        """Search with caching"""
        if cache and query in cache:
            return cache[query]
        
        embedding = self.model.encode(query)
        results = self.index.query(
            vector=embedding.tolist(),
            top_k=top_k,
            include_metadata=True
        )
        
        if cache is not None:
            cache[query] = results
        
        return results

# ========================================
# Monitoring
# ========================================

# Check index health
index_info = pc.describe_index(index_name)
print(f"Status: {index_info.status['state']}")
print(f"Replicas: {index_info.status['replicas']}")

# Usage stats (from Pinecone dashboard)
# - Query latency
# - Request rate
# - Storage used

# Cost optimization
# - Use serverless for variable load
# - Use pod-based for predictable high load
# - Delete unused indexes

# ========================================
# Advantages
# ========================================

# ✅ Fully managed (no ops)
# ✅ Auto-scaling
# ✅ High performance (single-digit ms latency)
# ✅ Metadata filtering
# ✅ Namespaces for multi-tenancy
# ✅ Real-time updates
# ⚠️ Cost: ~$70/month for 100k vectors (serverless)
