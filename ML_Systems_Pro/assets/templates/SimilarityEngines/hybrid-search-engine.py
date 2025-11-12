"""
Hybrid Search Engine
===================

Combine semantic (vector) search with keyword (BM25) search for best results.
Implements multiple fusion strategies and metadata filtering.

Use Cases:
- E-commerce product search
- Document retrieval
- Content discovery
- Knowledge base search

Requirements:
    pip install sentence-transformers faiss-cpu rank-bm25 redis numpy
"""

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from rank_bm25 import BM25Okapi
from typing import List, Dict, Optional, Tuple
import re
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Search result with score and metadata."""
    id: str
    text: str
    score: float
    metadata: Dict


class HybridSearchEngine:
    """
    Hybrid search combining semantic and keyword search.
    
    Fusion Strategies:
    - Weighted: w1 * semantic_score + w2 * keyword_score
    - RRF (Reciprocal Rank Fusion): 1 / (k + rank)
    - CombMNZ: sum(scores) * count(non_zero_scores)
    """
    
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        fusion_strategy: str = "weighted",  # "weighted", "rrf", "combmnz"
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3,
        device: str = "cpu"
    ):
        """
        Initialize hybrid search engine.
        
        Args:
            model_name: Sentence transformer model
            fusion_strategy: Score fusion method
            semantic_weight: Weight for semantic search (0-1)
            keyword_weight: Weight for keyword search (0-1)
            device: 'cuda' or 'cpu'
        """
        self.model = SentenceTransformer(model_name, device=device)
        self.fusion_strategy = fusion_strategy
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight
        
        # Storage
        self.items: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self.vector_index: Optional[faiss.Index] = None
        self.bm25: Optional[BM25Okapi] = None
        self.tokenized_corpus: List[List[str]] = []
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization for BM25."""
        # Lowercase and split on non-alphanumeric
        tokens = re.findall(r'\w+', text.lower())
        return tokens
    
    def add_items(
        self,
        items: List[Dict],
        text_field: str = "text",
        batch_size: int = 32
    ):
        """
        Add items to search index.
        
        Args:
            items: List of dicts with text and metadata
            text_field: Field name containing text
            batch_size: Batch size for encoding
        """
        self.items = items
        texts = [item[text_field] for item in items]
        
        # Generate embeddings
        print("Generating embeddings...")
        self.embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        # Build vector index
        print("Building FAISS index...")
        dimension = self.embeddings.shape[1]
        self.vector_index = faiss.IndexFlatIP(dimension)  # Inner product
        self.vector_index.add(self.embeddings.astype(np.float32))
        
        # Build BM25 index
        print("Building BM25 index...")
        self.tokenized_corpus = [self._tokenize(text) for text in texts]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        
        print(f"Indexed {len(items)} items")
    
    def _semantic_search(
        self,
        query: str,
        top_k: int = 100
    ) -> List[Tuple[int, float]]:
        """
        Perform semantic search.
        
        Returns:
            List of (index, score) tuples
        """
        query_embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        scores, indices = self.vector_index.search(
            query_embedding.reshape(1, -1).astype(np.float32),
            top_k
        )
        
        return [(int(idx), float(score)) for idx, score in zip(indices[0], scores[0])]
    
    def _keyword_search(
        self,
        query: str,
        top_k: int = 100
    ) -> List[Tuple[int, float]]:
        """
        Perform BM25 keyword search.
        
        Returns:
            List of (index, score) tuples
        """
        query_tokens = self._tokenize(query)
        scores = self.bm25.get_scores(query_tokens)
        
        # Get top K indices
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        return [(int(idx), float(scores[idx])) for idx in top_indices]
    
    def _fuse_weighted(
        self,
        semantic_results: List[Tuple[int, float]],
        keyword_results: List[Tuple[int, float]]
    ) -> List[Tuple[int, float]]:
        """Weighted score fusion."""
        scores = {}
        
        # Normalize semantic scores (already 0-1 from cosine)
        for idx, score in semantic_results:
            scores[idx] = self.semantic_weight * score
        
        # Normalize keyword scores
        keyword_scores = [s for _, s in keyword_results]
        max_keyword = max(keyword_scores) if keyword_scores else 1.0
        
        for idx, score in keyword_results:
            normalized = score / max_keyword if max_keyword > 0 else 0
            if idx in scores:
                scores[idx] += self.keyword_weight * normalized
            else:
                scores[idx] = self.keyword_weight * normalized
        
        # Sort by combined score
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results
    
    def _fuse_rrf(
        self,
        semantic_results: List[Tuple[int, float]],
        keyword_results: List[Tuple[int, float]],
        k: int = 60
    ) -> List[Tuple[int, float]]:
        """Reciprocal Rank Fusion."""
        scores = {}
        
        # Semantic ranks
        for rank, (idx, _) in enumerate(semantic_results, 1):
            scores[idx] = 1 / (k + rank)
        
        # Keyword ranks
        for rank, (idx, _) in enumerate(keyword_results, 1):
            if idx in scores:
                scores[idx] += 1 / (k + rank)
            else:
                scores[idx] = 1 / (k + rank)
        
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results
    
    def _fuse_combmnz(
        self,
        semantic_results: List[Tuple[int, float]],
        keyword_results: List[Tuple[int, float]]
    ) -> List[Tuple[int, float]]:
        """CombMNZ: sum(scores) * count(non_zero)."""
        scores = {}
        counts = {}
        
        # Normalize and combine
        semantic_dict = dict(semantic_results)
        keyword_dict = dict(keyword_results)
        
        # Normalize keyword scores
        max_keyword = max(keyword_dict.values()) if keyword_dict else 1.0
        
        all_indices = set(semantic_dict.keys()) | set(keyword_dict.keys())
        
        for idx in all_indices:
            sem_score = semantic_dict.get(idx, 0)
            kw_score = keyword_dict.get(idx, 0) / max_keyword if max_keyword > 0 else 0
            
            scores[idx] = sem_score + kw_score
            counts[idx] = int(sem_score > 0) + int(kw_score > 0)
        
        # Apply CombMNZ formula
        final_scores = {idx: scores[idx] * counts[idx] for idx in scores}
        
        sorted_results = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        filters: Optional[Dict] = None,
        search_top_k: int = 100
    ) -> List[SearchResult]:
        """
        Hybrid search with fusion.
        
        Args:
            query: Search query
            top_k: Number of final results
            filters: Metadata filters
            search_top_k: Candidates to fetch before fusion
            
        Returns:
            List of SearchResult objects
        """
        # Perform both searches
        semantic_results = self._semantic_search(query, search_top_k)
        keyword_results = self._keyword_search(query, search_top_k)
        
        # Fuse results
        if self.fusion_strategy == "weighted":
            fused = self._fuse_weighted(semantic_results, keyword_results)
        elif self.fusion_strategy == "rrf":
            fused = self._fuse_rrf(semantic_results, keyword_results)
        elif self.fusion_strategy == "combmnz":
            fused = self._fuse_combmnz(semantic_results, keyword_results)
        else:
            raise ValueError(f"Unknown fusion strategy: {self.fusion_strategy}")
        
        # Apply filters and format results
        results = []
        for idx, score in fused:
            item = self.items[idx]
            
            # Apply metadata filters
            if filters:
                match = all(
                    item.get(k) == v for k, v in filters.items()
                )
                if not match:
                    continue
            
            results.append(SearchResult(
                id=str(idx),
                text=item.get("text", ""),
                score=score,
                metadata={k: v for k, v in item.items() if k != "text"}
            ))
            
            if len(results) >= top_k:
                break
        
        return results


# Example usage
if __name__ == "__main__":
    # Sample data
    items = [
        {
            "text": "Machine learning is a subset of artificial intelligence",
            "category": "AI",
            "date": "2024-01-15"
        },
        {
            "text": "Deep learning uses neural networks with multiple layers",
            "category": "AI",
            "date": "2024-02-20"
        },
        {
            "text": "Python is a popular programming language for data science",
            "category": "Programming",
            "date": "2024-03-10"
        },
        {
            "text": "Neural networks are inspired by the human brain",
            "category": "AI",
            "date": "2024-01-25"
        },
        {
            "text": "TensorFlow and PyTorch are deep learning frameworks",
            "category": "Tools",
            "date": "2024-02-15"
        }
    ] * 100  # Expand for testing
    
    # Test different fusion strategies
    strategies = ["weighted", "rrf", "combmnz"]
    
    for strategy in strategies:
        print(f"\n{'='*60}")
        print(f"Testing {strategy.upper()} fusion strategy")
        print('='*60)
        
        # Initialize engine
        engine = HybridSearchEngine(
            fusion_strategy=strategy,
            semantic_weight=0.7,
            keyword_weight=0.3
        )
        
        # Index items
        engine.add_items(items, text_field="text")
        
        # Search
        query = "deep neural networks for AI"
        results = engine.search(
            query,
            top_k=5,
            filters={"category": "AI"}
        )
        
        print(f"\nQuery: '{query}'")
        print(f"Filter: category='AI'\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. Score: {result.score:.4f}")
            print(f"   Text: {result.text[:80]}...")
            print(f"   Metadata: {result.metadata}\n")
