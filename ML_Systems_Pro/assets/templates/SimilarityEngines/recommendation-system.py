"""
Multi-Strategy Recommendation System
====================================

Combine collaborative filtering, content-based filtering, and embedding-based
recommendations for optimal results.

Use Cases:
- E-commerce product recommendations
- Content discovery (articles, videos, music)
- Social media feed ranking
- Personalized search results

Requirements:
    pip install sentence-transformers faiss-cpu pandas numpy scikit-learn implicit
"""

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Tuple, Optional
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import implicit


class RecommendationEngine:
    """
    Multi-strategy recommendation system.
    
    Strategies:
    1. Collaborative Filtering (user-item interactions)
    2. Content-Based (item embeddings)
    3. Hybrid (weighted combination)
    """
    
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        cf_weight: float = 0.4,
        content_weight: float = 0.6
    ):
        """
        Initialize recommendation engine.
        
        Args:
            model_name: Model for content embeddings
            cf_weight: Weight for collaborative filtering
            content_weight: Weight for content-based recommendations
        """
        self.model = SentenceTransformer(model_name)
        self.cf_weight = cf_weight
        self.content_weight = content_weight
        
        # Data storage
        self.items: List[Dict] = []
        self.item_embeddings: Optional[np.ndarray] = None
        self.vector_index: Optional[faiss.Index] = None
        
        # Collaborative filtering
        self.user_item_matrix: Optional[csr_matrix] = None
        self.cf_model: Optional[implicit.als.AlternatingLeastSquares] = None
        self.user_mapping: Dict[str, int] = {}
        self.item_mapping: Dict[str, int] = {}
        self.reverse_item_mapping: Dict[int, str] = {}
    
    def add_items(
        self,
        items: List[Dict],
        text_field: str = "description"
    ):
        """
        Add items with content features.
        
        Args:
            items: List of items with text descriptions
            text_field: Field containing item description
        """
        self.items = items
        
        # Generate content embeddings
        texts = [item[text_field] for item in items]
        print("Generating item embeddings...")
        self.item_embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        # Build vector index
        dimension = self.item_embeddings.shape[1]
        self.vector_index = faiss.IndexFlatIP(dimension)
        self.vector_index.add(self.item_embeddings.astype(np.float32))
        
        print(f"Indexed {len(items)} items")
    
    def train_collaborative_filtering(
        self,
        interactions: pd.DataFrame,
        user_col: str = "user_id",
        item_col: str = "item_id",
        rating_col: str = "rating",
        factors: int = 100,
        iterations: int = 20,
        regularization: float = 0.01
    ):
        """
        Train collaborative filtering model.
        
        Args:
            interactions: DataFrame with user-item interactions
            user_col: User ID column
            item_col: Item ID column
            rating_col: Rating/interaction strength column
            factors: Number of latent factors
            iterations: Training iterations
            regularization: L2 regularization
        """
        print("Training collaborative filtering model...")
        
        # Create user and item mappings
        unique_users = interactions[user_col].unique()
        unique_items = interactions[item_col].unique()
        
        self.user_mapping = {uid: idx for idx, uid in enumerate(unique_users)}
        self.item_mapping = {iid: idx for idx, iid in enumerate(unique_items)}
        self.reverse_item_mapping = {idx: iid for iid, idx in self.item_mapping.items()}
        
        # Create user-item matrix
        user_indices = interactions[user_col].map(self.user_mapping)
        item_indices = interactions[item_col].map(self.item_mapping)
        ratings = interactions[rating_col].values
        
        self.user_item_matrix = csr_matrix(
            (ratings, (user_indices, item_indices)),
            shape=(len(unique_users), len(unique_items))
        )
        
        # Train ALS model
        self.cf_model = implicit.als.AlternatingLeastSquares(
            factors=factors,
            iterations=iterations,
            regularization=regularization
        )
        self.cf_model.fit(self.user_item_matrix)
        
        print(f"Trained on {len(unique_users)} users and {len(unique_items)} items")
    
    def _content_based_recommendations(
        self,
        item_id: str,
        top_k: int = 10,
        exclude_items: List[str] = None
    ) -> List[Tuple[str, float]]:
        """
        Get content-based recommendations.
        
        Args:
            item_id: Reference item ID
            top_k: Number of recommendations
            exclude_items: Items to exclude from results
            
        Returns:
            List of (item_id, score) tuples
        """
        # Find item index
        item_idx = None
        for idx, item in enumerate(self.items):
            if item.get("id") == item_id:
                item_idx = idx
                break
        
        if item_idx is None:
            return []
        
        # Get item embedding
        item_embedding = self.item_embeddings[item_idx:item_idx+1]
        
        # Search similar items
        scores, indices = self.vector_index.search(
            item_embedding.astype(np.float32),
            top_k + 1 + len(exclude_items or [])
        )
        
        # Format results
        recommendations = []
        exclude_set = set(exclude_items or [])
        
        for score, idx in zip(scores[0], indices[0]):
            item = self.items[idx]
            item_id = item.get("id")
            
            # Skip self and excluded items
            if idx == item_idx or item_id in exclude_set:
                continue
            
            recommendations.append((item_id, float(score)))
            
            if len(recommendations) >= top_k:
                break
        
        return recommendations
    
    def _collaborative_recommendations(
        self,
        user_id: str,
        top_k: int = 10,
        exclude_items: List[str] = None
    ) -> List[Tuple[str, float]]:
        """
        Get collaborative filtering recommendations.
        
        Args:
            user_id: User ID
            top_k: Number of recommendations
            exclude_items: Items to exclude
            
        Returns:
            List of (item_id, score) tuples
        """
        if self.cf_model is None:
            return []
        
        user_idx = self.user_mapping.get(user_id)
        if user_idx is None:
            return []
        
        # Get recommendations from ALS
        item_indices, scores = self.cf_model.recommend(
            user_idx,
            self.user_item_matrix[user_idx],
            N=top_k + len(exclude_items or []),
            filter_already_liked_items=True
        )
        
        # Convert to item IDs
        recommendations = []
        exclude_set = set(exclude_items or [])
        
        for item_idx, score in zip(item_indices, scores):
            item_id = self.reverse_item_mapping.get(item_idx)
            if item_id and item_id not in exclude_set:
                recommendations.append((item_id, float(score)))
            
            if len(recommendations) >= top_k:
                break
        
        return recommendations
    
    def recommend(
        self,
        user_id: Optional[str] = None,
        item_id: Optional[str] = None,
        top_k: int = 10,
        exclude_items: List[str] = None,
        strategy: str = "hybrid"  # "hybrid", "collaborative", "content"
    ) -> List[Dict]:
        """
        Get recommendations using specified strategy.
        
        Args:
            user_id: User ID (for collaborative filtering)
            item_id: Item ID (for content-based)
            top_k: Number of recommendations
            exclude_items: Items to exclude
            strategy: Recommendation strategy
            
        Returns:
            List of recommended items with scores
        """
        if strategy == "collaborative":
            if user_id is None:
                raise ValueError("user_id required for collaborative filtering")
            
            recommendations = self._collaborative_recommendations(
                user_id, top_k, exclude_items
            )
        
        elif strategy == "content":
            if item_id is None:
                raise ValueError("item_id required for content-based recommendations")
            
            recommendations = self._content_based_recommendations(
                item_id, top_k, exclude_items
            )
        
        elif strategy == "hybrid":
            # Combine both strategies
            cf_recs = []
            content_recs = []
            
            if user_id and self.cf_model:
                cf_recs = self._collaborative_recommendations(
                    user_id, top_k * 2, exclude_items
                )
            
            if item_id:
                content_recs = self._content_based_recommendations(
                    item_id, top_k * 2, exclude_items
                )
            
            # Merge with weighted scores
            combined_scores = {}
            
            for item_id, score in cf_recs:
                combined_scores[item_id] = self.cf_weight * score
            
            for item_id, score in content_recs:
                if item_id in combined_scores:
                    combined_scores[item_id] += self.content_weight * score
                else:
                    combined_scores[item_id] = self.content_weight * score
            
            # Sort by combined score
            recommendations = sorted(
                combined_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_k]
        
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        # Format results with item details
        results = []
        for item_id, score in recommendations:
            # Find item details
            item_details = next(
                (item for item in self.items if item.get("id") == item_id),
                None
            )
            
            if item_details:
                results.append({
                    "item_id": item_id,
                    "score": score,
                    "title": item_details.get("title", ""),
                    "description": item_details.get("description", "")[:100],
                    "category": item_details.get("category", "")
                })
        
        return results
    
    def explain_recommendation(
        self,
        user_id: str,
        item_id: str
    ) -> Dict:
        """
        Explain why an item was recommended.
        
        Args:
            user_id: User ID
            item_id: Recommended item ID
            
        Returns:
            Explanation with contributing factors
        """
        explanation = {
            "item_id": item_id,
            "factors": []
        }
        
        # Collaborative filtering reason
        if self.cf_model and user_id in self.user_mapping:
            user_idx = self.user_mapping[user_id]
            
            # Get user's interaction history
            user_interactions = self.user_item_matrix[user_idx].toarray()[0]
            interacted_items = np.where(user_interactions > 0)[0]
            
            explanation["factors"].append({
                "type": "collaborative",
                "reason": f"Users with similar preferences also liked this",
                "based_on": f"{len(interacted_items)} past interactions"
            })
        
        # Content-based reason
        item_details = next(
            (item for item in self.items if item.get("id") == item_id),
            None
        )
        
        if item_details:
            explanation["factors"].append({
                "type": "content",
                "reason": f"Similar to items you've viewed",
                "category": item_details.get("category", "unknown")
            })
        
        return explanation


# Example usage
if __name__ == "__main__":
    # Sample items
    items = [
        {"id": "1", "title": "Neural Networks", "description": "Introduction to deep learning", "category": "AI"},
        {"id": "2", "title": "Python Basics", "description": "Learn Python programming", "category": "Programming"},
        {"id": "3", "title": "Machine Learning", "description": "ML algorithms explained", "category": "AI"},
        {"id": "4", "title": "Data Structures", "description": "Algorithms and data structures", "category": "CS"},
        {"id": "5", "title": "Computer Vision", "description": "Image processing with ML", "category": "AI"},
    ]
    
    # Sample interactions
    interactions = pd.DataFrame({
        "user_id": ["user1", "user1", "user2", "user2", "user3"],
        "item_id": ["1", "3", "1", "5", "2"],
        "rating": [5.0, 4.0, 5.0, 4.5, 3.0]
    })
    
    # Initialize engine
    engine = RecommendationEngine(cf_weight=0.4, content_weight=0.6)
    
    # Add items
    engine.add_items(items, text_field="description")
    
    # Train collaborative filtering
    engine.train_collaborative_filtering(interactions)
    
    # Get recommendations
    print("\n=== Hybrid Recommendations for user1 ===")
    recs = engine.recommend(user_id="user1", top_k=3, strategy="hybrid")
    for rec in recs:
        print(f"{rec['title']} (score: {rec['score']:.3f})")
    
    print("\n=== Content-Based Recommendations for item 1 ===")
    recs = engine.recommend(item_id="1", top_k=3, strategy="content")
    for rec in recs:
        print(f"{rec['title']} (score: {rec['score']:.3f})")
    
    print("\n=== Explanation ===")
    explanation = engine.explain_recommendation("user1", "5")
    print(f"Why recommend {explanation['item_id']}:")
    for factor in explanation["factors"]:
        print(f"  - {factor['reason']}")
