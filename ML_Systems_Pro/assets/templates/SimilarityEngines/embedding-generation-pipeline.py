"""
Scalable Embedding Generation Pipeline
======================================

Production-ready pipeline for generating embeddings at scale with batching,
caching, and distributed processing support.

Use Cases:
- Generate embeddings for millions of products/documents
- Periodic re-embedding for content updates
- Real-time embedding for new items
- Multi-language and multi-modal embeddings

Requirements:
    pip install torch sentence-transformers redis celery tqdm
"""

import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Union
import redis
import pickle
from tqdm import tqdm
from celery import Celery
import hashlib
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmbeddingConfig:
    """Configuration for embedding generation."""
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size: int = 64
    max_length: int = 512
    normalize: bool = True
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    cache_enabled: bool = True
    cache_ttl: int = 86400 * 7  # 7 days
    redis_host: str = "localhost"
    redis_port: int = 6379


class EmbeddingGenerator:
    """
    Scalable embedding generator with caching and batching.
    
    Features:
    - Automatic batching for throughput
    - Redis caching to avoid recomputation
    - GPU/CPU support with automatic device selection
    - Progress tracking for large datasets
    - Multi-language support
    """
    
    def __init__(self, config: EmbeddingConfig = None):
        """
        Initialize embedding generator.
        
        Args:
            config: EmbeddingConfig instance
        """
        self.config = config or EmbeddingConfig()
        
        # Load model
        logger.info(f"Loading model: {self.config.model_name}")
        self.model = SentenceTransformer(self.config.model_name)
        self.model.to(self.config.device)
        
        # Initialize cache
        if self.config.cache_enabled:
            self.cache = redis.Redis(
                host=self.config.redis_host,
                port=self.config.redis_port,
                decode_responses=False
            )
            logger.info("Redis cache enabled")
        else:
            self.cache = None
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key from text."""
        # Use hash to keep keys short and consistent
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"emb:{self.config.model_name}:{text_hash}"
    
    def _get_cached_embedding(self, text: str) -> Optional[np.ndarray]:
        """Retrieve embedding from cache."""
        if not self.cache:
            return None
        
        key = self._get_cache_key(text)
        cached = self.cache.get(key)
        
        if cached:
            return pickle.loads(cached)
        
        return None
    
    def _cache_embedding(self, text: str, embedding: np.ndarray):
        """Store embedding in cache."""
        if not self.cache:
            return
        
        key = self._get_cache_key(text)
        self.cache.setex(
            key,
            self.config.cache_ttl,
            pickle.dumps(embedding)
        )
    
    def encode_single(self, text: str) -> np.ndarray:
        """
        Encode single text into embedding.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        # Check cache first
        cached = self._get_cached_embedding(text)
        if cached is not None:
            return cached
        
        # Generate embedding
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=self.config.normalize,
            device=self.config.device
        )
        
        # Cache result
        self._cache_embedding(text, embedding)
        
        return embedding
    
    def encode_batch(
        self,
        texts: List[str],
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Encode batch of texts with caching.
        
        Args:
            texts: List of text strings
            show_progress: Show tqdm progress bar
            
        Returns:
            Embeddings array (N, embedding_dim)
        """
        embeddings = []
        uncached_texts = []
        uncached_indices = []
        
        # Check cache
        for idx, text in enumerate(texts):
            cached = self._get_cached_embedding(text)
            if cached is not None:
                embeddings.append(cached)
            else:
                uncached_texts.append(text)
                uncached_indices.append(idx)
        
        # Generate uncached embeddings
        if uncached_texts:
            logger.info(
                f"Generating {len(uncached_texts)}/{len(texts)} embeddings "
                f"(cache hit: {len(embeddings)}/{len(texts)})"
            )
            
            uncached_embeddings = self.model.encode(
                uncached_texts,
                batch_size=self.config.batch_size,
                convert_to_numpy=True,
                normalize_embeddings=self.config.normalize,
                device=self.config.device,
                show_progress_bar=show_progress
            )
            
            # Cache new embeddings
            for text, emb in zip(uncached_texts, uncached_embeddings):
                self._cache_embedding(text, emb)
            
            # Merge with cached
            for idx, emb in zip(uncached_indices, uncached_embeddings):
                embeddings.insert(idx, emb)
        
        return np.array(embeddings)
    
    def encode_large_dataset(
        self,
        texts: List[str],
        output_file: str = None,
        checkpoint_interval: int = 10000
    ) -> np.ndarray:
        """
        Encode very large datasets with checkpointing.
        
        Args:
            texts: List of text strings
            output_file: Optional file to save embeddings
            checkpoint_interval: Save checkpoint every N items
            
        Returns:
            Embeddings array
        """
        all_embeddings = []
        
        for i in tqdm(range(0, len(texts), checkpoint_interval)):
            batch = texts[i:i+checkpoint_interval]
            embeddings = self.encode_batch(batch, show_progress=False)
            all_embeddings.append(embeddings)
            
            # Save checkpoint
            if output_file:
                checkpoint_file = f"{output_file}.checkpoint_{i}"
                np.save(checkpoint_file, np.vstack(all_embeddings))
                logger.info(f"Saved checkpoint: {checkpoint_file}")
        
        final_embeddings = np.vstack(all_embeddings)
        
        # Save final result
        if output_file:
            np.save(output_file, final_embeddings)
            logger.info(f"Saved final embeddings: {output_file}")
        
        return final_embeddings
    
    def encode_multilingual(
        self,
        texts: List[str],
        languages: List[str] = None
    ) -> np.ndarray:
        """
        Encode multilingual texts.
        
        Args:
            texts: List of text strings in various languages
            languages: Optional language codes for each text
            
        Returns:
            Embeddings array
        """
        # Use multilingual model if not already
        if "multilingual" not in self.config.model_name.lower():
            logger.warning(
                f"Model {self.config.model_name} may not support multilingual. "
                "Consider using 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'"
            )
        
        return self.encode_batch(texts)


# Celery task for distributed processing
app = Celery("embedding_tasks", broker="redis://localhost:6379/0")

@app.task
def generate_embeddings_async(
    texts: List[str],
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
) -> List[bytes]:
    """
    Celery task for async embedding generation.
    
    Args:
        texts: List of text strings
        model_name: Model identifier
        
    Returns:
        List of pickled embeddings
    """
    config = EmbeddingConfig(model_name=model_name)
    generator = EmbeddingGenerator(config)
    embeddings = generator.encode_batch(texts, show_progress=False)
    
    # Pickle each embedding
    return [pickle.dumps(emb) for emb in embeddings]


class DistributedEmbeddingGenerator:
    """
    Distributed embedding generation using Celery.
    
    Scale embedding generation across multiple workers.
    """
    
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 1000
    ):
        """
        Initialize distributed generator.
        
        Args:
            model_name: Model identifier
            chunk_size: Items per worker task
        """
        self.model_name = model_name
        self.chunk_size = chunk_size
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encode texts using distributed workers.
        
        Args:
            texts: List of text strings
            
        Returns:
            Embeddings array
        """
        # Split into chunks
        chunks = [
            texts[i:i+self.chunk_size]
            for i in range(0, len(texts), self.chunk_size)
        ]
        
        logger.info(f"Submitting {len(chunks)} tasks to Celery workers")
        
        # Submit tasks
        tasks = [
            generate_embeddings_async.delay(chunk, self.model_name)
            for chunk in chunks
        ]
        
        # Collect results
        all_embeddings = []
        for task in tqdm(tasks, desc="Collecting results"):
            result = task.get()  # Wait for task completion
            embeddings = [pickle.loads(emb) for emb in result]
            all_embeddings.extend(embeddings)
        
        return np.array(all_embeddings)


# Example usage
if __name__ == "__main__":
    # Initialize generator
    config = EmbeddingConfig(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        batch_size=64,
        cache_enabled=True
    )
    generator = EmbeddingGenerator(config)
    
    # Single text encoding
    text = "Machine learning is transforming industries"
    embedding = generator.encode_single(text)
    print(f"Single embedding shape: {embedding.shape}")
    
    # Batch encoding
    texts = [
        "Artificial intelligence is the future",
        "Deep learning powers modern AI",
        "Neural networks mimic the human brain",
    ] * 100  # 300 texts
    
    embeddings = generator.encode_batch(texts, show_progress=True)
    print(f"Batch embeddings shape: {embeddings.shape}")
    
    # Large dataset encoding with checkpoints
    large_texts = texts * 100  # 30,000 texts
    large_embeddings = generator.encode_large_dataset(
        large_texts,
        output_file="large_embeddings.npy",
        checkpoint_interval=10000
    )
    print(f"Large dataset embeddings shape: {large_embeddings.shape}")
    
    # Distributed processing (requires Celery workers running)
    # Start workers: celery -A embedding_generation worker --loglevel=info
    # distributed_gen = DistributedEmbeddingGenerator(chunk_size=1000)
    # distributed_embeddings = distributed_gen.encode(large_texts)
