"""
CLIP Zero-Shot Image Classification
Production-ready implementation for text-to-image and image-to-text retrieval.

Use cases:
- Product search by description or image
- Content moderation (classify images without training)
- Visual similarity search across text queries
"""

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List, Dict, Union
import numpy as np

class CLIPZeroShotClassifier:
    """
    Zero-shot image classifier using OpenAI CLIP.
    
    Supports:
    - Text-to-image retrieval
    - Image-to-text retrieval
    - Zero-shot classification with custom labels
    """
    
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        """
        Initialize CLIP model.
        
        Args:
            model_name: HuggingFace model ID
                - clip-vit-base-patch32: Fast, 150M params
                - clip-vit-large-patch14: Accurate, 430M params
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        
    def encode_images(self, images: List[Union[str, Image.Image]]) -> np.ndarray:
        """
        Generate embeddings for images.
        
        Args:
            images: List of image paths or PIL Images
            
        Returns:
            Normalized embeddings (batch_size, 512)
        """
        # Load images if paths provided
        pil_images = []
        for img in images:
            if isinstance(img, str):
                pil_images.append(Image.open(img).convert("RGB"))
            else:
                pil_images.append(img)
        
        # Process and encode
        inputs = self.processor(images=pil_images, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        
        # Normalize embeddings
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        return image_features.cpu().numpy()
    
    def encode_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for text descriptions.
        
        Args:
            texts: List of text descriptions
            
        Returns:
            Normalized embeddings (batch_size, 512)
        """
        inputs = self.processor(text=texts, return_tensors="pt", padding=True).to(self.device)
        
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        
        # Normalize embeddings
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        return text_features.cpu().numpy()
    
    def classify(
        self, 
        image: Union[str, Image.Image], 
        labels: List[str],
        prompt_template: str = "a photo of a {}"
    ) -> Dict[str, float]:
        """
        Zero-shot classification with custom labels.
        
        Args:
            image: Image path or PIL Image
            labels: List of class labels
            prompt_template: Template for text prompts
            
        Returns:
            Dictionary of {label: probability}
        """
        # Format text prompts
        texts = [prompt_template.format(label) for label in labels]
        
        # Get embeddings
        image_emb = self.encode_images([image])[0]
        text_embs = self.encode_texts(texts)
        
        # Compute similarities
        similarities = (image_emb @ text_embs.T) * 100.0  # Scale for softmax
        probs = torch.softmax(torch.tensor(similarities), dim=0).numpy()
        
        return {label: float(prob) for label, prob in zip(labels, probs)}
    
    def search_images(
        self, 
        query: str, 
        image_embeddings: np.ndarray,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search images using text query.
        
        Args:
            query: Text search query
            image_embeddings: Precomputed image embeddings
            top_k: Number of results to return
            
        Returns:
            List of {index, similarity} dicts
        """
        query_emb = self.encode_texts([query])[0]
        
        # Compute similarities
        similarities = image_embeddings @ query_emb
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        return [
            {"index": int(idx), "similarity": float(similarities[idx])}
            for idx in top_indices
        ]


# Example usage
if __name__ == "__main__":
    # Initialize classifier
    classifier = CLIPZeroShotClassifier()
    
    # Example 1: Zero-shot classification
    labels = ["cat", "dog", "bird", "car", "house"]
    results = classifier.classify("example.jpg", labels)
    print("Classification results:", results)
    
    # Example 2: Build image search index
    image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]
    image_embeddings = classifier.encode_images(image_paths)
    
    # Search with text query
    query = "red sports car"
    results = classifier.search_images(query, image_embeddings, top_k=3)
    print("Search results:", results)
    
    # Example 3: Batch processing for production
    # Process images in batches for GPU efficiency
    batch_size = 32
    all_embeddings = []
    
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i+batch_size]
        embeddings = classifier.encode_images(batch)
        all_embeddings.append(embeddings)
    
    all_embeddings = np.vstack(all_embeddings)
    print(f"Processed {len(all_embeddings)} images")


"""
Production Deployment Notes:

1. Model Optimization:
   - Convert to ONNX for 2x faster inference
   - Use TensorRT on NVIDIA GPUs for 4x speedup
   - Quantize to FP16 for 2x memory reduction

2. Scaling Strategy:
   - Precompute and cache embeddings in vector DB
   - Use batch inference for throughput
   - Deploy with FastAPI + GPU workers

3. Monitoring:
   - Track inference latency (target <50ms)
   - Monitor GPU utilization (>70%)
   - Log query distributions for drift detection

4. Prompt Engineering:
   - Test multiple templates: "a photo of a {}", "an image containing {}"
   - Use domain-specific prompts: "a product photo of {}" for e-commerce
   - Ensemble multiple prompts for robustness
"""
