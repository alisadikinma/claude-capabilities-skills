"""
Multi-Modal Fusion Pipeline
===========================

Combine multiple modalities (visual, audio, text) for enhanced predictions.
Supports early fusion (concatenate features) and late fusion (ensemble predictions).

Use Cases:
- Video content classification
- Multi-modal sentiment analysis
- Healthcare diagnostics (images + clinical notes)
- Autonomous driving (camera + lidar + GPS)

Requirements:
    pip install torch torchvision torchaudio transformers librosa opencv-python
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
from typing import Dict, List, Optional, Tuple
import numpy as np


class MultiModalFusionModel(nn.Module):
    """
    Multi-modal fusion model supporting early and late fusion strategies.
    
    Fusion Strategies:
    - Early Fusion: Concatenate features before final layers
    - Late Fusion: Separate predictions, then ensemble
    - Cross-Attention: Attention-based fusion between modalities
    """
    
    def __init__(
        self,
        vision_encoder: str = "microsoft/resnet-50",
        text_encoder: str = "bert-base-uncased",
        audio_dim: int = 128,
        fusion_type: str = "early",  # "early", "late", or "attention"
        num_classes: int = 10,
        dropout: float = 0.3
    ):
        """
        Initialize multi-modal fusion model.
        
        Args:
            vision_encoder: HuggingFace vision model name
            text_encoder: HuggingFace text model name
            audio_dim: Audio feature dimension
            fusion_type: Fusion strategy ("early", "late", "attention")
            num_classes: Number of output classes
            dropout: Dropout rate
        """
        super().__init__()
        
        self.fusion_type = fusion_type
        
        # Vision encoder
        self.vision_model = AutoModel.from_pretrained(vision_encoder)
        vision_dim = self.vision_model.config.hidden_sizes[-1]
        
        # Text encoder
        self.text_model = AutoModel.from_pretrained(text_encoder)
        self.text_tokenizer = AutoTokenizer.from_pretrained(text_encoder)
        text_dim = self.text_model.config.hidden_size
        
        # Audio encoder (simple MLP for demo)
        self.audio_encoder = nn.Sequential(
            nn.Linear(audio_dim, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 256)
        )
        audio_encoded_dim = 256
        
        # Fusion layers
        if fusion_type == "early":
            # Concatenate all features
            combined_dim = vision_dim + text_dim + audio_encoded_dim
            self.fusion_layer = nn.Sequential(
                nn.Linear(combined_dim, 512),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(512, num_classes)
            )
            
        elif fusion_type == "late":
            # Separate classifiers for each modality
            self.vision_classifier = nn.Linear(vision_dim, num_classes)
            self.text_classifier = nn.Linear(text_dim, num_classes)
            self.audio_classifier = nn.Linear(audio_encoded_dim, num_classes)
            
            # Learnable ensemble weights
            self.ensemble_weights = nn.Parameter(torch.ones(3) / 3)
            
        elif fusion_type == "attention":
            # Cross-attention fusion
            self.cross_attention = nn.MultiheadAttention(
                embed_dim=512,
                num_heads=8,
                dropout=dropout
            )
            
            # Project features to same dimension
            self.vision_proj = nn.Linear(vision_dim, 512)
            self.text_proj = nn.Linear(text_dim, 512)
            self.audio_proj = nn.Linear(audio_encoded_dim, 512)
            
            self.fusion_layer = nn.Sequential(
                nn.Linear(512, 256),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(256, num_classes)
            )
    
    def forward(
        self,
        images: torch.Tensor,
        texts: List[str],
        audio_features: torch.Tensor,
        return_features: bool = False
    ) -> torch.Tensor:
        """
        Forward pass through multi-modal fusion model.
        
        Args:
            images: Image tensor (batch_size, 3, H, W)
            texts: List of text strings
            audio_features: Audio features (batch_size, audio_dim)
            return_features: Return intermediate features
            
        Returns:
            Predictions (batch_size, num_classes)
        """
        # Extract vision features
        vision_out = self.vision_model(pixel_values=images)
        vision_features = vision_out.last_hidden_state.mean(dim=1)  # Global avg pool
        
        # Extract text features
        text_inputs = self.text_tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        ).to(images.device)
        text_out = self.text_model(**text_inputs)
        text_features = text_out.last_hidden_state[:, 0, :]  # [CLS] token
        
        # Extract audio features
        audio_encoded = self.audio_encoder(audio_features)
        
        # Fusion
        if self.fusion_type == "early":
            # Concatenate features
            combined = torch.cat([vision_features, text_features, audio_encoded], dim=1)
            logits = self.fusion_layer(combined)
            
        elif self.fusion_type == "late":
            # Separate predictions
            vision_logits = self.vision_classifier(vision_features)
            text_logits = self.text_classifier(text_features)
            audio_logits = self.audio_classifier(audio_encoded)
            
            # Weighted ensemble
            weights = F.softmax(self.ensemble_weights, dim=0)
            logits = (
                weights[0] * vision_logits +
                weights[1] * text_logits +
                weights[2] * audio_logits
            )
            
        elif self.fusion_type == "attention":
            # Project to common dimension
            vision_proj = self.vision_proj(vision_features).unsqueeze(0)
            text_proj = self.text_proj(text_features).unsqueeze(0)
            audio_proj = self.audio_proj(audio_encoded).unsqueeze(0)
            
            # Stack modalities (seq_len=3, batch_size, embed_dim)
            stacked = torch.cat([vision_proj, text_proj, audio_proj], dim=0)
            
            # Cross-attention
            attended, _ = self.cross_attention(stacked, stacked, stacked)
            
            # Average attended features
            fused = attended.mean(dim=0)
            
            logits = self.fusion_layer(fused)
        
        if return_features:
            return logits, {
                "vision": vision_features,
                "text": text_features,
                "audio": audio_encoded
            }
        
        return logits


class MultiModalDataset(torch.utils.data.Dataset):
    """Dataset for multi-modal data."""
    
    def __init__(
        self,
        image_paths: List[str],
        texts: List[str],
        audio_features: np.ndarray,
        labels: np.ndarray,
        transform=None
    ):
        """
        Initialize multi-modal dataset.
        
        Args:
            image_paths: List of image file paths
            texts: List of text strings
            audio_features: Audio features array (N, audio_dim)
            labels: Labels array (N,)
            transform: Image transformations
        """
        self.image_paths = image_paths
        self.texts = texts
        self.audio_features = torch.from_numpy(audio_features).float()
        self.labels = torch.from_numpy(labels).long()
        self.transform = transform
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        from PIL import Image
        
        # Load image
        image = Image.open(self.image_paths[idx]).convert("RGB")
        if self.transform:
            image = self.transform(image)
        
        return {
            "image": image,
            "text": self.texts[idx],
            "audio": self.audio_features[idx],
            "label": self.labels[idx]
        }


def train_multimodal_model(
    model: MultiModalFusionModel,
    train_loader: torch.utils.data.DataLoader,
    val_loader: torch.utils.data.DataLoader,
    num_epochs: int = 10,
    learning_rate: float = 1e-4,
    device: str = "cuda"
):
    """
    Train multi-modal fusion model.
    
    Args:
        model: MultiModalFusionModel instance
        train_loader: Training data loader
        val_loader: Validation data loader
        num_epochs: Number of training epochs
        learning_rate: Learning rate
        device: Device to train on
    """
    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()
    
    best_val_acc = 0.0
    
    for epoch in range(num_epochs):
        # Training
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for batch in train_loader:
            images = batch["image"].to(device)
            texts = batch["text"]
            audio = batch["audio"].to(device)
            labels = batch["label"].to(device)
            
            optimizer.zero_grad()
            
            logits = model(images, texts, audio)
            loss = criterion(logits, labels)
            
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = logits.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()
        
        train_acc = 100.0 * train_correct / train_total
        
        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for batch in val_loader:
                images = batch["image"].to(device)
                texts = batch["text"]
                audio = batch["audio"].to(device)
                labels = batch["label"].to(device)
                
                logits = model(images, texts, audio)
                loss = criterion(logits, labels)
                
                val_loss += loss.item()
                _, predicted = logits.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
        
        val_acc = 100.0 * val_correct / val_total
        
        print(f"Epoch {epoch+1}/{num_epochs}")
        print(f"Train Loss: {train_loss/len(train_loader):.4f}, Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss/len(val_loader):.4f}, Acc: {val_acc:.2f}%")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), "best_multimodal_model.pt")
            print(f"Saved best model (Val Acc: {val_acc:.2f}%)")


# Example usage
if __name__ == "__main__":
    # Initialize model with attention fusion
    model = MultiModalFusionModel(
        vision_encoder="microsoft/resnet-50",
        text_encoder="bert-base-uncased",
        audio_dim=128,
        fusion_type="attention",  # Try "early", "late", or "attention"
        num_classes=10,
        dropout=0.3
    )
    
    # Example forward pass
    images = torch.randn(4, 3, 224, 224)  # Batch of 4 images
    texts = ["sample text 1", "sample text 2", "sample text 3", "sample text 4"]
    audio = torch.randn(4, 128)  # Audio features
    
    logits = model(images, texts, audio)
    print(f"Output shape: {logits.shape}")  # (4, 10)
    
    # For training, create DataLoader with MultiModalDataset
    # train_multimodal_model(model, train_loader, val_loader, num_epochs=10)
