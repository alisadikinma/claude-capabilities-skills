"""
Embedding Quality Analyzer
==========================

Comprehensive tool for analyzing embedding quality, coverage, and distribution.

Use Cases:
- Evaluate embedding models before deployment
- Compare different embedding models
- Identify problematic embeddings
- Analyze semantic clustering

Requirements:
    pip install sentence-transformers scikit-learn umap-learn matplotlib seaborn
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import pdist, squareform


class EmbeddingQualityAnalyzer:
    """
    Analyze embedding quality across multiple dimensions.
    
    Metrics:
    - Coverage: How well embeddings span the space
    - Separation: Distance between clusters
    - Isotropy: Uniformity of direction distribution
    - Intrinsic dimension: Effective dimensionality
    """
    
    def __init__(self, embeddings: np.ndarray, labels: List[str] = None):
        """
        Initialize analyzer.
        
        Args:
            embeddings: Embedding matrix (N, D)
            labels: Optional labels for each embedding
        """
        self.embeddings = embeddings
        self.labels = labels
        self.n_samples, self.dimension = embeddings.shape
    
    def analyze_all(self) -> Dict:
        """
        Run all quality checks.
        
        Returns:
            Dict with all analysis results
        """
        results = {
            'basic_stats': self.compute_basic_stats(),
            'coverage': self.analyze_coverage(),
            'isotropy': self.analyze_isotropy(),
            'intrinsic_dimension': self.estimate_intrinsic_dimension(),
            'clustering_quality': self.analyze_clustering(),
            'outliers': self.detect_outliers()
        }
        
        return results
    
    def compute_basic_stats(self) -> Dict:
        """Compute basic embedding statistics."""
        norms = np.linalg.norm(self.embeddings, axis=1)
        
        # Pairwise similarities
        similarities = cosine_similarity(self.embeddings)
        np.fill_diagonal(similarities, 0)  # Exclude self-similarity
        
        return {
            'num_embeddings': self.n_samples,
            'dimension': self.dimension,
            'norm_mean': float(np.mean(norms)),
            'norm_std': float(np.std(norms)),
            'norm_min': float(np.min(norms)),
            'norm_max': float(np.max(norms)),
            'similarity_mean': float(np.mean(similarities)),
            'similarity_std': float(np.std(similarities)),
            'similarity_min': float(np.min(similarities)),
            'similarity_max': float(np.max(similarities))
        }
    
    def analyze_coverage(self) -> Dict:
        """
        Analyze how well embeddings cover the space.
        
        Good coverage means embeddings use the full space, not clustered.
        """
        # 1. Variance along principal components
        pca = PCA()
        pca.fit(self.embeddings)
        
        explained_variance = pca.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance)
        
        # 2. Average pairwise distance
        distances = pdist(self.embeddings, metric='euclidean')
        avg_distance = np.mean(distances)
        
        # 3. Convex hull volume (for low-D projection)
        if self.dimension > 3:
            # Project to 3D
            pca_3d = PCA(n_components=3)
            projected = pca_3d.fit_transform(self.embeddings)
        else:
            projected = self.embeddings
        
        from scipy.spatial import ConvexHull
        try:
            hull = ConvexHull(projected)
            hull_volume = hull.volume
        except:
            hull_volume = None
        
        return {
            'explained_variance_top10': explained_variance[:10].tolist(),
            'variance_for_95pct': int(np.argmax(cumulative_variance >= 0.95) + 1),
            'avg_pairwise_distance': float(avg_distance),
            'convex_hull_volume': float(hull_volume) if hull_volume else None
        }
    
    def analyze_isotropy(self) -> Dict:
        """
        Analyze isotropy (uniformity of directions).
        
        Anisotropic embeddings have preferred directions (bad).
        Isotropic embeddings uniformly span all directions (good).
        """
        # 1. Variance of dimension-wise means (should be low)
        dim_means = np.mean(self.embeddings, axis=0)
        mean_variance = float(np.var(dim_means))
        
        # 2. Variance of dimension-wise stds (should be low)
        dim_stds = np.std(self.embeddings, axis=0)
        std_variance = float(np.var(dim_stds))
        
        # 3. Self-similarity distribution (should be centered at 0)
        similarities = cosine_similarity(self.embeddings)
        np.fill_diagonal(similarities, 0)
        
        avg_self_similarity = float(np.mean(similarities))
        
        # 4. Isotropy score (closer to 1 = more isotropic)
        # Based on "On the Sentence Embeddings from BERT for Semantic Textual Similarity"
        centered = self.embeddings - np.mean(self.embeddings, axis=0)
        cov = np.cov(centered.T)
        eigenvalues = np.linalg.eigvalsh(cov)
        
        # Isotropy = min_eig / max_eig
        isotropy_score = float(eigenvalues.min() / eigenvalues.max())
        
        return {
            'mean_variance': mean_variance,
            'std_variance': std_variance,
            'avg_self_similarity': avg_self_similarity,
            'isotropy_score': isotropy_score,
            'is_isotropic': isotropy_score > 0.5  # Threshold
        }
    
    def estimate_intrinsic_dimension(self) -> Dict:
        """
        Estimate intrinsic dimensionality.
        
        Even high-D embeddings may lie on lower-D manifold.
        """
        # 1. PCA explained variance approach
        pca = PCA()
        pca.fit(self.embeddings)
        
        explained_var = pca.explained_variance_ratio_
        cumsum = np.cumsum(explained_var)
        
        dim_90pct = int(np.argmax(cumsum >= 0.90) + 1)
        dim_95pct = int(np.argmax(cumsum >= 0.95) + 1)
        dim_99pct = int(np.argmax(cumsum >= 0.99) + 1)
        
        # 2. Participation ratio
        # PR = (sum of eigenvalues)^2 / sum of squared eigenvalues
        eigenvalues = pca.explained_variance_
        participation_ratio = (
            np.sum(eigenvalues) ** 2 / np.sum(eigenvalues ** 2)
        )
        
        return {
            'nominal_dimension': self.dimension,
            'intrinsic_dim_90pct': dim_90pct,
            'intrinsic_dim_95pct': dim_95pct,
            'intrinsic_dim_99pct': dim_99pct,
            'participation_ratio': float(participation_ratio),
            'efficiency_ratio': float(dim_95pct / self.dimension)
        }
    
    def analyze_clustering(self, n_clusters: int = 10) -> Dict:
        """
        Analyze clustering quality.
        
        Args:
            n_clusters: Number of clusters for KMeans
        """
        from sklearn.metrics import silhouette_score, calinski_harabasz_score
        
        # K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(self.embeddings)
        
        # Silhouette score (-1 to 1, higher is better)
        silhouette = silhouette_score(self.embeddings, cluster_labels)
        
        # Calinski-Harabasz score (higher is better)
        calinski = calinski_harabasz_score(self.embeddings, cluster_labels)
        
        # Inertia (lower is better)
        inertia = kmeans.inertia_
        
        # Cluster sizes
        unique, counts = np.unique(cluster_labels, return_counts=True)
        cluster_sizes = dict(zip(unique.tolist(), counts.tolist()))
        
        return {
            'n_clusters': n_clusters,
            'silhouette_score': float(silhouette),
            'calinski_harabasz_score': float(calinski),
            'inertia': float(inertia),
            'cluster_sizes': cluster_sizes,
            'min_cluster_size': int(counts.min()),
            'max_cluster_size': int(counts.max()),
            'cluster_size_std': float(counts.std())
        }
    
    def detect_outliers(self, threshold: float = 3.0) -> Dict:
        """
        Detect outlier embeddings.
        
        Args:
            threshold: Z-score threshold for outliers
        """
        # 1. Norm-based outliers
        norms = np.linalg.norm(self.embeddings, axis=1)
        norm_mean = np.mean(norms)
        norm_std = np.std(norms)
        norm_z_scores = np.abs((norms - norm_mean) / norm_std)
        
        norm_outliers = np.where(norm_z_scores > threshold)[0]
        
        # 2. Isolation-based outliers (avg similarity)
        similarities = cosine_similarity(self.embeddings)
        np.fill_diagonal(similarities, 0)
        avg_similarities = np.mean(similarities, axis=1)
        
        sim_mean = np.mean(avg_similarities)
        sim_std = np.std(avg_similarities)
        sim_z_scores = np.abs((avg_similarities - sim_mean) / sim_std)
        
        isolation_outliers = np.where(sim_z_scores > threshold)[0]
        
        # Combined outliers
        combined_outliers = np.union1d(norm_outliers, isolation_outliers)
        
        return {
            'n_outliers': len(combined_outliers),
            'outlier_ratio': float(len(combined_outliers) / self.n_samples),
            'outlier_indices': combined_outliers.tolist()[:100],  # First 100
            'norm_outliers': len(norm_outliers),
            'isolation_outliers': len(isolation_outliers)
        }
    
    def visualize(self, method: str = 'pca', save_path: str = None):
        """
        Visualize embeddings in 2D.
        
        Args:
            method: 'pca', 'tsne', or 'umap'
            save_path: Optional path to save figure
        """
        if method == 'pca':
            reducer = PCA(n_components=2)
        elif method == 'tsne':
            reducer = TSNE(n_components=2, random_state=42)
        elif method == 'umap':
            import umap
            reducer = umap.UMAP(n_components=2, random_state=42)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Reduce dimensions
        reduced = reducer.fit_transform(self.embeddings)
        
        # Plot
        plt.figure(figsize=(10, 8))
        
        if self.labels is not None:
            # Color by labels
            unique_labels = list(set(self.labels))
            colors = plt.cm.tab20(np.linspace(0, 1, len(unique_labels)))
            
            for label, color in zip(unique_labels, colors):
                mask = [l == label for l in self.labels]
                plt.scatter(
                    reduced[mask, 0],
                    reduced[mask, 1],
                    c=[color],
                    label=label,
                    alpha=0.6
                )
            plt.legend()
        else:
            plt.scatter(reduced[:, 0], reduced[:, 1], alpha=0.6)
        
        plt.title(f'Embedding Visualization ({method.upper()})')
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def print_report(self):
        """Print comprehensive analysis report."""
        results = self.analyze_all()
        
        print("=" * 60)
        print("EMBEDDING QUALITY ANALYSIS REPORT")
        print("=" * 60)
        
        print("\n📊 BASIC STATISTICS")
        print("-" * 60)
        stats = results['basic_stats']
        print(f"Embeddings: {stats['num_embeddings']:,}")
        print(f"Dimensions: {stats['dimension']}")
        print(f"Norm: {stats['norm_mean']:.3f} ± {stats['norm_std']:.3f}")
        print(f"Similarity: {stats['similarity_mean']:.3f} ± {stats['similarity_std']:.3f}")
        
        print("\n🌍 COVERAGE ANALYSIS")
        print("-" * 60)
        coverage = results['coverage']
        print(f"Dimensions for 95% variance: {coverage['variance_for_95pct']}")
        print(f"Avg pairwise distance: {coverage['avg_pairwise_distance']:.3f}")
        
        print("\n⚖️ ISOTROPY ANALYSIS")
        print("-" * 60)
        isotropy = results['isotropy']
        print(f"Isotropy score: {isotropy['isotropy_score']:.3f}")
        print(f"Is isotropic: {'✓ Yes' if isotropy['is_isotropic'] else '✗ No'}")
        print(f"Avg self-similarity: {isotropy['avg_self_similarity']:.3f}")
        
        print("\n📐 DIMENSIONALITY")
        print("-" * 60)
        dim = results['intrinsic_dimension']
        print(f"Nominal dimension: {dim['nominal_dimension']}")
        print(f"Intrinsic dim (95% var): {dim['intrinsic_dim_95pct']}")
        print(f"Efficiency ratio: {dim['efficiency_ratio']:.1%}")
        
        print("\n🎯 CLUSTERING QUALITY")
        print("-" * 60)
        clustering = results['clustering_quality']
        print(f"Silhouette score: {clustering['silhouette_score']:.3f}")
        print(f"Cluster size range: {clustering['min_cluster_size']}-{clustering['max_cluster_size']}")
        
        print("\n⚠️ OUTLIERS")
        print("-" * 60)
        outliers = results['outliers']
        print(f"Outliers detected: {outliers['n_outliers']} ({outliers['outlier_ratio']:.1%})")
        
        print("\n" + "=" * 60)


# Example usage
if __name__ == "__main__":
    from sentence_transformers import SentenceTransformer
    
    # Generate sample embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    texts = [
        "Machine learning is amazing",
        "Deep learning powers AI",
        "Python is great for data science",
        "I love programming",
        "Neural networks are powerful"
    ] * 20  # 100 samples
    
    embeddings = model.encode(texts)
    
    # Analyze
    analyzer = EmbeddingQualityAnalyzer(embeddings, labels=texts[:100])
    analyzer.print_report()
    
    # Visualize
    analyzer.visualize(method='pca', save_path='embeddings_pca.png')
