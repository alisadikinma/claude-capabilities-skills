"""
CLIP-Based Image-Text Similarity Search System
==============================================

Production-ready implementation for image-text search using OpenAI's CLIP model.
Supports batch processing, caching, and vector database integration.

Use Cases:
- E-commerce visual search
- Content moderation
- Image tagging and organization
- Cross-modal retrieval

Requirements:
    pip install transformers torch pillow faiss-cpu redis sentence-transformers
"""

import torch
import faiss
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List, Dict, Tuple
import redis
import json
from pathlib import Path


class CLIPSearchEngine:
    """CLIP-based image-text similarity search engine."""
    
    def __init__(
        self,
        model_name: str = "openai/clip-vit-base-patch32",
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        cache_enabled: bool = True,
        redis_host: str = "localhost",
        redis_port: int = 6379
    ):
        """
        Initialize CLIP search engine.
        
        Args:
            model_name: HuggingFace model identifier
            device: 'cuda' or 'cpu'
            cache_enabled: Enable Redis caching for embeddings
            redis_host: Redis server host
            redis_port: Redis server port
        """
        self.device = device
        self.model = CLIPModel.from_pretrained(model_name).to(device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        
        # Initialize cache
        self.cache_enabled = cache_enabled
        if cache_enabled:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=False
            )
        
        # FAISS index for vector search
        self.index = None
        self.items = []  # Store item metadata
        
    def encode_text(self, texts: List[str]) -> np.ndarray:
        """
        Encode text queries into embeddings.
        
        Args:
            texts: List of text strings
            
        Returns:
            Normalized embeddings (batch_size, embedding_dim)
        """
        inputs = self.processor(
            text=texts,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)
        
        with torch.no_grad():
            embeddings = self.model.get_text_features(**inputs)
            # L2 normalization for cosine similarity
            embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
            
        return embeddings.cpu().numpy()
    
    def encode_images(self, image_paths: List[str]) -> np.ndarray:
        """
        Encode images into embeddings with caching.
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            Normalized embeddings (batch_size, embedding_dim)
        """
        embeddings = []
        uncached_paths = []
        uncached_indices = []
        
        # Check cache first
        for idx, path in enumerate(image_paths):
            if self.cache_enabled:
                cache_key = f"clip_emb:{path}"
                cached = self.redis_client.get(cache_key)
                if cached:
                    emb = np.frombuffer(cached, dtype=np.float32)
                    embeddings.append(emb)
                    continue
            
            uncached_paths.append(path)
            uncached_indices.append(idx)
        
        # Encode uncached images
        if uncached_paths:
            images = [Image.open(p).convert("RGB") for p in uncached_paths]
            inputs = self.processor(
                images=images,
                return_tensors="pt",
                padding=True
            ).to(self.device)
            
            with torch.no_grad():
                uncached_embeddings = self.model.get_image_features(**inputs)
                uncached_embeddings = uncached_embeddings / uncached_embeddings.norm(
                    dim=-1, keepdim=True
                )
                uncached_embeddings = uncached_embeddings.cpu().numpy()
            
            # Cache new embeddings
            if self.cache_enabled:
                for path, emb in zip(uncached_paths, uncached_embeddings):
                    cache_key = f"clip_emb:{path}"
                    self.redis_client.setex(
                        cache_key,
                        3600 * 24 * 7,  # 7 days TTL
                        emb.tobytes()
                    )
            
            # Merge cached and uncached
            for idx, emb in zip(uncached_indices, uncached_embeddings):
                embeddings.insert(idx, emb)
        
        return np.array(embeddings)
    
    def build_index(
        self,
        image_paths: List[str],
        metadata: List[Dict] = None,
        batch_size: int = 32
    ):
        """
        Build FAISS index from image embeddings.
        
        Args:
            image_paths: List of image file paths
            metadata: Optional metadata for each image
            batch_size: Batch size for encoding
        """
        all_embeddings = []
        
        # Process in batches
        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i+batch_size]
            embeddings = self.encode_images(batch_paths)
            all_embeddings.append(embeddings)
        
        all_embeddings = np.vstack(all_embeddings)
        
        # Create FAISS index (L2 distance = cosine for normalized vectors)
        dimension = all_embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product = cosine
        self.index.add(all_embeddings.astype(np.float32))
        
        # Store metadata
        self.items = [
            {
                "path": path,
                "metadata": meta if metadata else {}
            }
            for path, meta in zip(
                image_paths,
                metadata if metadata else [{}] * len(image_paths)
            )
        ]
        
        print(f"Built index with {len(image_paths)} images")
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        filters: Dict = None
    ) -> List[Dict]:
        """
        Search for similar images using text query.
        
        Args:
            query: Text search query
            top_k: Number of results to return
            filters: Optional metadata filters (e.g., {"category": "clothing"})
            
        Returns:
            List of results with scores and metadata
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Encode query
        query_embedding = self.encode_text([query])[0]
        
        # Search FAISS index
        scores, indices = self.index.search(
            query_embedding.reshape(1, -1).astype(np.float32),
            top_k * 2 if filters else top_k  # Fetch more for filtering
        )
        
        # Apply filters and format results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            item = self.items[idx]
            
            # Apply metadata filters
            if filters:
                match = all(
                    item["metadata"].get(k) == v
                    for k, v in filters.items()
                )
                if not match:
                    continue
            
            results.append({
                "path": item["path"],
                "score": float(score),
                "metadata": item["metadata"]
            })
            
            if len(results) >= top_k:
                break
        
        return results
    
    def save_index(self, path: str):
        """Save FAISS index and metadata to disk."""
        index_path = f"{path}.index"
        metadata_path = f"{path}.metadata.json"
        
        faiss.write_index(self.index, index_path)
        with open(metadata_path, 'w') as f:
            json.dump(self.items, f)
        
        print(f"Saved index to {index_path}")
    
    def load_index(self, path: str):
        """Load FAISS index and metadata from disk."""
        index_path = f"{path}.index"
        metadata_path = f"{path}.metadata.json"
        
        self.index = faiss.read_index(index_path)
        with open(metadata_path, 'r') as f:
            self.items = json.load(f)
        
        print(f"Loaded index with {len(self.items)} items")


# Example usage
if __name__ == "__main__":
    # Initialize search engine
    engine = CLIPSearchEngine(cache_enabled=True)
    
    # Build index from images
    image_paths = [
        "products/jacket_001.jpg",
        "products/jacket_002.jpg",
        "products/dress_001.jpg",
    ]
    
    metadata = [
        {"category": "clothing", "price": 89.99, "color": "red"},
        {"category": "clothing", "price": 129.99, "color": "black"},
        {"category": "clothing", "price": 79.99, "color": "blue"},
    ]
    
    engine.build_index(image_paths, metadata, batch_size=32)
    
    # Search with text query
    results = engine.search(
        query="red leather jacket",
        top_k=5,
        filters={"category": "clothing"}
    )
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['path']} (score: {result['score']:.3f})")
        print(f"   Metadata: {result['metadata']}")
    
    # Save for later use
    engine.save_index("clip_index")
