# Supabase Vector Database (pgvector)

Complete setup for vector similarity search using Supabase + pgvector for RAG, semantic search, and recommendations.

## Quick Setup

### 1. Enable pgvector

```sql
-- In Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Create Documents Table

```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  embedding vector(1536),  -- OpenAI ada-002
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Critical: Add vector index
CREATE INDEX ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### 3. Similarity Search Function

```sql
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
RETURNS TABLE (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

## Backend Integration

### Python (FastAPI)

```python
from supabase import create_client
import openai

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai.api_key = OPENAI_API_KEY

def generate_embedding(text: str):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def semantic_search(query: str, limit: int = 10):
    embedding = generate_embedding(query)
    
    result = supabase.rpc('match_documents', {
        'query_embedding': embedding,
        'match_threshold': 0.7,
        'match_count': limit
    }).execute()
    
    return result.data
```

### TypeScript (Next.js)

```typescript
import { createClient } from '@supabase/supabase-js';
import OpenAI from 'openai';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

export async function semanticSearch(query: string, limit = 10) {
  // Generate embedding
  const response = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: query
  });
  
  const embedding = response.data[0].embedding;
  
  // Search
  const { data } = await supabase.rpc('match_documents', {
    query_embedding: embedding,
    match_threshold: 0.7,
    match_count: limit
  });
  
  return data;
}
```

## RAG Pattern

```python
from openai import OpenAI

client = OpenAI()

def rag_response(user_query: str):
    # 1. Retrieve context
    context_docs = semantic_search(user_query, limit=3)
    context = "\n\n".join([doc['content'] for doc in context_docs])
    
    # 2. Generate response
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "Answer based on context provided."},
            {"role": "user", "content": f"Context:\n{context}\n\nQ: {user_query}"}
        ]
    )
    
    return {
        "answer": response.choices[0].message.content,
        "sources": context_docs
    }
```

## Best Practices

- **Chunk size**: 300-500 chars for QA, 1000-1500 for documents
- **Overlap**: 10-20% of chunk size
- **Threshold**: 0.75 for balanced precision/recall
- **Index**: Use ivfflat for <1M vectors, hnsw for >1M

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-12
