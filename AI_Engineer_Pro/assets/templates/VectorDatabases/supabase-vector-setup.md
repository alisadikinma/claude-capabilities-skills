# Supabase Vector Database (pgvector)

Supabase with pgvector extension for vector similarity search with PostgreSQL.

## Setup

### 1. Enable pgvector Extension

```sql
-- In Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Create Table

```sql
CREATE TABLE pcb_embeddings (
  id BIGSERIAL PRIMARY KEY,
  content TEXT,
  metadata JSONB,
  embedding VECTOR(384)  -- Dimension based on your model
);

-- Create index for fast similarity search
CREATE INDEX ON pcb_embeddings 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

## Python Integration

```python
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Supabase
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# ========================================
# Insert Embeddings
# ========================================

def insert_document(content: str, metadata: dict = None):
    """Insert document with embedding"""
    
    # Generate embedding
    embedding = model.encode(content).tolist()
    
    # Insert to Supabase
    data = supabase.table('pcb_embeddings').insert({
        'content': content,
        'metadata': metadata or {},
        'embedding': embedding
    }).execute()
    
    return data

# Batch insert
documents = [
    {
        "content": "PCB scratch on component A",
        "metadata": {"type": "scratch", "severity": 3}
    },
    {
        "content": "Solder bridge detected",
        "metadata": {"type": "solder_bridge", "severity": 5}
    }
]

for doc in documents:
    insert_document(doc['content'], doc['metadata'])

# ========================================
# Similarity Search
# ========================================

def search_similar(query: str, limit: int = 5, metadata_filter: dict = None):
    """
    Search for similar documents
    
    Args:
        query: Search query
        limit: Number of results
        metadata_filter: JSON filter (e.g., {"type": "scratch"})
    """
    
    # Generate query embedding
    query_embedding = model.encode(query).tolist()
    
    # Build RPC call
    # Note: Need to create a custom function in Supabase
    result = supabase.rpc(
        'match_documents',
        {
            'query_embedding': query_embedding,
            'match_threshold': 0.7,
            'match_count': limit
        }
    ).execute()
    
    return result.data

# ========================================
# Create RPC Function in Supabase
# ========================================

"""
-- Run this in Supabase SQL Editor

CREATE OR REPLACE FUNCTION match_documents (
  query_embedding VECTOR(384),
  match_threshold FLOAT,
  match_count INT
)
RETURNS TABLE (
  id BIGINT,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    pcb_embeddings.id,
    pcb_embeddings.content,
    pcb_embeddings.metadata,
    1 - (pcb_embeddings.embedding <=> query_embedding) AS similarity
  FROM pcb_embeddings
  WHERE 1 - (pcb_embeddings.embedding <=> query_embedding) > match_threshold
  ORDER BY pcb_embeddings.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
"""

# ========================================
# Search with Metadata Filter
# ========================================

"""
-- Enhanced RPC function with metadata filter

CREATE OR REPLACE FUNCTION match_documents_filtered (
  query_embedding VECTOR(384),
  filter_metadata JSONB,
  match_count INT
)
RETURNS TABLE (
  id BIGINT,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    pcb_embeddings.id,
    pcb_embeddings.content,
    pcb_embeddings.metadata,
    1 - (pcb_embeddings.embedding <=> query_embedding) AS similarity
  FROM pcb_embeddings
  WHERE metadata @> filter_metadata
  ORDER BY pcb_embeddings.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
"""

# Usage with filter
def search_with_filter(query: str, metadata_filter: dict, limit: int = 5):
    query_embedding = model.encode(query).tolist()
    
    result = supabase.rpc(
        'match_documents_filtered',
        {
            'query_embedding': query_embedding,
            'filter_metadata': metadata_filter,
            'match_count': limit
        }
    ).execute()
    
    return result.data

# Example
results = search_with_filter(
    "PCB defects",
    metadata_filter={"type": "scratch"},
    limit=5
)

# ========================================
# Update Embeddings
# ========================================

def update_document(doc_id: int, content: str = None, metadata: dict = None):
    """Update document"""
    
    update_data = {}
    
    if content:
        update_data['content'] = content
        update_data['embedding'] = model.encode(content).tolist()
    
    if metadata:
        update_data['metadata'] = metadata
    
    result = supabase.table('pcb_embeddings').update(
        update_data
    ).eq('id', doc_id).execute()
    
    return result

# ========================================
# Delete Documents
# ========================================

def delete_document(doc_id: int):
    """Delete by ID"""
    result = supabase.table('pcb_embeddings').delete().eq('id', doc_id).execute()
    return result

def delete_by_metadata(metadata_filter: dict):
    """Delete by metadata"""
    # First get matching IDs
    docs = supabase.table('pcb_embeddings').select('id').match(metadata_filter).execute()
    
    ids = [doc['id'] for doc in docs.data]
    
    # Delete
    result = supabase.table('pcb_embeddings').delete().in_('id', ids).execute()
    return result

# ========================================
# Hybrid Search (Semantic + Keyword)
# ========================================

"""
-- Create full-text search index
CREATE INDEX pcb_content_search_idx ON pcb_embeddings 
USING GIN (to_tsvector('english', content));
"""

def hybrid_search(query: str, limit: int = 10):
    """Combine vector similarity + full-text search"""
    
    # 1. Vector search
    query_embedding = model.encode(query).tolist()
    vector_results = supabase.rpc(
        'match_documents',
        {
            'query_embedding': query_embedding,
            'match_threshold': 0.5,
            'match_count': limit * 2
        }
    ).execute()
    
    # 2. Full-text search
    text_results = supabase.table('pcb_embeddings').select('*').text_search(
        'content',
        query
    ).limit(limit * 2).execute()
    
    # 3. Merge and deduplicate
    combined = {}
    
    for doc in vector_results.data:
        combined[doc['id']] = {**doc, 'vector_score': doc['similarity']}
    
    for doc in text_results.data:
        if doc['id'] in combined:
            combined[doc['id']]['text_match'] = True
        else:
            combined[doc['id']] = {**doc, 'text_match': True}
    
    # Sort by combined score
    results = sorted(
        combined.values(),
        key=lambda x: x.get('vector_score', 0) + (0.3 if x.get('text_match') else 0),
        reverse=True
    )[:limit]
    
    return results

# ========================================
# Production Class
# ========================================

class SupabaseVectorDB:
    """Production-ready Supabase vector database manager"""
    
    def __init__(self, url: str, key: str, embedding_model: str = 'all-MiniLM-L6-v2'):
        self.supabase = create_client(url, key)
        self.model = SentenceTransformer(embedding_model)
        self.table = 'pcb_embeddings'
    
    def upsert(self, id: int, content: str, metadata: dict = None):
        """Insert or update"""
        embedding = self.model.encode(content).tolist()
        
        # Check if exists
        existing = self.supabase.table(self.table).select('id').eq('id', id).execute()
        
        if existing.data:
            # Update
            return self.supabase.table(self.table).update({
                'content': content,
                'metadata': metadata or {},
                'embedding': embedding
            }).eq('id', id).execute()
        else:
            # Insert
            return self.supabase.table(self.table).insert({
                'id': id,
                'content': content,
                'metadata': metadata or {},
                'embedding': embedding
            }).execute()
    
    def search(self, query: str, limit: int = 5, threshold: float = 0.7):
        """Semantic search"""
        query_embedding = self.model.encode(query).tolist()
        
        return self.supabase.rpc(
            'match_documents',
            {
                'query_embedding': query_embedding,
                'match_threshold': threshold,
                'match_count': limit
            }
        ).execute().data
    
    def delete_all(self):
        """Delete all documents"""
        return self.supabase.table(self.table).delete().neq('id', 0).execute()

# Usage
db = SupabaseVectorDB(SUPABASE_URL, SUPABASE_KEY)
db.upsert(1, "PCB defect detected", {"type": "scratch"})
results = db.search("What defects are there?", limit=5)
```

## Advantages

- ✅ Managed PostgreSQL (no ops)
- ✅ Built-in auth & Row Level Security
- ✅ Real-time subscriptions
- ✅ Auto-generated REST API
- ✅ Free tier: 500MB database
- ✅ Integrates with existing Supabase project
- ✅ SQL access for complex queries

## Use Cases

- Laravel + Supabase projects
- Multi-tenant applications (RLS)
- Real-time vector search
- Combined relational + vector data
