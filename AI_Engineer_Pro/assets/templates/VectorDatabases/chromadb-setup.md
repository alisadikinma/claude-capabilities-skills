# ChromaDB Setup

Open-source embedding database for local/embedded use.

## Installation

```bash
pip install chromadb
```

## Basic Usage

```python
import chromadb
from chromadb.utils import embedding_functions

# Initialize (in-memory)
client = chromadb.Client()

# Or persistent
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.create_collection(
    name="pcb_defects",
    metadata={"description": "PCB inspection database"}
)

# Add documents
collection.add(
    documents=[
        "PCB scratch on component A",
        "Solder bridge between pins",
        "Missing capacitor C12"
    ],
    metadatas=[
        {"type": "scratch", "severity": 3},
        {"type": "solder_bridge", "severity": 5},
        {"type": "missing", "severity": 4}
    ],
    ids=["doc1", "doc2", "doc3"]
)

# Query
results = collection.query(
    query_texts=["What defects are on the PCB?"],
    n_results=3
)

print(results)
```

## Custom Embeddings

```python
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Custom embedding function
def custom_embedding_function(texts):
    return model.encode(texts).tolist()

# Create collection with custom embeddings
collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=custom_embedding_function
)

# Add with pre-computed embeddings
embeddings = model.encode(documents)

collection.add(
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas,
    ids=ids
)
```

## Filtering

```python
# Query with metadata filter
results = collection.query(
    query_texts=["PCB defects"],
    n_results=5,
    where={"type": "scratch"},  # Exact match
    where_document={"$contains": "component"}  # Text search
)

# Complex filters
results = collection.query(
    query_texts=["defects"],
    where={
        "$and": [
            {"severity": {"$gte": 3}},
            {"type": {"$in": ["scratch", "crack"]}}
        ]
    }
)
```

## Update & Delete

```python
# Update
collection.update(
    ids=["doc1"],
    documents=["Updated text"],
    metadatas=[{"type": "scratch", "severity": 5}]
)

# Delete
collection.delete(ids=["doc1"])

# Delete by filter
collection.delete(where={"type": "scratch"})
```

## Multi-modal (Images)

```python
from chromadb.utils.data_loaders import ImageLoader

# Image collection
image_collection = client.create_collection(
    name="pcb_images",
    data_loader=ImageLoader()
)

# Add images
image_collection.add(
    uris=["path/to/img1.jpg", "path/to/img2.jpg"],
    ids=["img1", "img2"]
)

# Query with image
results = image_collection.query(
    query_uris=["path/to/query.jpg"],
    n_results=5
)
```

## Get Collection

```python
# List collections
collections = client.list_collections()

# Get existing collection
collection = client.get_collection("pcb_defects")

# Get all items
all_items = collection.get()
```

## Advantages

- ✅ Open source, free
- ✅ Easy local development
- ✅ Can run embedded (no server)
- ✅ Simple API
- ⚠️ Best for <100k vectors
