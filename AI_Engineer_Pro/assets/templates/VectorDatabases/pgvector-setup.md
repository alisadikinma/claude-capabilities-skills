# pgvector Setup

PostgreSQL extension for vector similarity search.

## Installation

```bash
# Install PostgreSQL 15+
sudo apt install postgresql-15

# Install pgvector
cd /tmp
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

## Enable Extension

```sql
CREATE EXTENSION vector;
```

## Create Table

```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Connect
conn = psycopg2.connect(
    host="localhost",
    database="vectordb",
    user="postgres",
    password="password"
)

# Register vector type
register_vector(conn)

# Create table
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE pcb_documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(384)  -- Dimension matches your model
    )
""")

# Create index for fast search
cursor.execute("""
    CREATE INDEX ON pcb_documents 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100)
""")

conn.commit()
```

## Insert Embeddings

```python
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions

# Generate embeddings
documents = [
    "PCB scratch defect on component A",
    "Solder bridge between pins 3 and 4",
    "Missing capacitor C12 on board"
]

embeddings = model.encode(documents)

# Insert
for doc, emb in zip(documents, embeddings):
    cursor.execute(
        "INSERT INTO pcb_documents (content, embedding) VALUES (%s, %s)",
        (doc, emb.tolist())
    )

conn.commit()
```

## Similarity Search

```python
# Query
query = "What defects are on the PCB?"
query_embedding = model.encode(query)

# Cosine similarity search
cursor.execute("""
    SELECT content, 1 - (embedding <=> %s::vector) AS similarity
    FROM pcb_documents
    ORDER BY embedding <=> %s::vector
    LIMIT 5
""", (query_embedding.tolist(), query_embedding.tolist()))

results = cursor.fetchall()

for content, similarity in results:
    print(f"[{similarity:.3f}] {content}")
```

## Distance Operators

```sql
-- Cosine distance (0 = identical, 2 = opposite)
embedding <=> query_vector

-- L2 distance (Euclidean)
embedding <-> query_vector

-- Inner product
embedding <#> query_vector
```

## With Metadata Filtering

```python
cursor.execute("""
    CREATE TABLE pcb_images (
        id SERIAL PRIMARY KEY,
        image_path TEXT,
        defect_type TEXT,
        severity INTEGER,
        embedding vector(512)
    )
""")

# Search with filter
cursor.execute("""
    SELECT image_path, defect_type, 1 - (embedding <=> %s::vector) AS similarity
    FROM pcb_images
    WHERE defect_type = 'scratch' AND severity > 3
    ORDER BY embedding <=> %s::vector
    LIMIT 10
""", (query_embedding.tolist(), query_embedding.tolist()))
```

## Using SQLAlchemy

```python
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(Vector(384))

# Create engine
engine = create_engine('postgresql://user:pass@localhost/vectordb')
Base.metadata.create_all(engine)

# Insert
from sqlalchemy.orm import Session

with Session(engine) as session:
    doc = Document(content="PCB defect", embedding=embedding.tolist())
    session.add(doc)
    session.commit()

# Query
from sqlalchemy import select, func

with Session(engine) as session:
    results = session.execute(
        select(Document)
        .order_by(Document.embedding.cosine_distance(query_embedding))
        .limit(5)
    ).scalars().all()
```

## Performance Tuning

```sql
-- Increase memory for faster searches
SET maintenance_work_mem = '2GB';

-- Create HNSW index (faster, more accurate)
CREATE INDEX ON pcb_documents 
USING hnsw (embedding vector_cosine_ops);

-- Analyze table
ANALYZE pcb_documents;
```

## Advantages

- ✅ SQL database (ACID compliance)
- ✅ Join with relational data
- ✅ Mature backup/replication
- ✅ No extra infrastructure
- ✅ Good for < 1M vectors
