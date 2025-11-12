# Multi-Modal Architecture Patterns

Comprehensive guide for designing and implementing multi-modal ML systems.

## What is Multi-Modal ML?

Systems that process and combine multiple types of data:
- **Vision + Language:** CLIP, BLIP, Flamingo
- **Audio + Vision:** Audio-visual speech recognition
- **Text + Structured:** Tables + descriptions for QA
- **3+ Modalities:** ImageBind (6 modalities)

## Core Concepts

### 1. Modality Encoders

Each modality needs specialized encoding:

```python
# Vision: CNN or Vision Transformer
vision_encoder = torchvision.models.resnet50(pretrained=True)

# Text: Transformer
text_encoder = AutoModel.from_pretrained("bert-base-uncased")

# Audio: Spectrogram + CNN
audio_encoder = torchaudio.models.Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base")
```

### 2. Shared Embedding Space

Map different modalities to common space:

```python
# Project to shared dimension
vision_proj = nn.Linear(vision_dim, shared_dim)
text_proj = nn.Linear(text_dim, shared_dim)

# L2 normalize for cosine similarity
vision_emb = F.normalize(vision_proj(vision_features), dim=-1)
text_emb = F.normalize(text_proj(text_features), dim=-1)

# Contrastive learning
similarity = vision_emb @ text_emb.T  # Batch x Batch matrix
```

### 3. Fusion Strategies

How to combine modalities:

**Early Fusion:** Concatenate raw/encoded features
```python
combined = torch.cat([vision_features, text_features], dim=-1)
output = classifier(combined)
```

**Late Fusion:** Separate predictions, then ensemble
```python
vision_logits = vision_classifier(vision_features)
text_logits = text_classifier(text_features)
final_logits = 0.6 * vision_logits + 0.4 * text_logits
```

**Cross-Attention:** Modalities attend to each other
```python
# Text attends to vision
text_attended = cross_attention(
    query=text_features,
    key=vision_features,
    value=vision_features
)
```

## Architecture Patterns

### Pattern 1: CLIP-Style Contrastive Learning

**Use Case:** Image-text retrieval, zero-shot classification

**Architecture:**
```
Images → Vision Encoder → Vision Embeddings
                               ↓
                         Contrastive Loss
                               ↓
Texts → Text Encoder → Text Embeddings
```

**Implementation:**
```python
class CLIPModel(nn.Module):
    def __init__(self, vision_encoder, text_encoder, embed_dim=512):
        super().__init__()
        self.vision_encoder = vision_encoder
        self.text_encoder = text_encoder
        
        # Projection heads
        self.vision_proj = nn.Linear(vision_encoder.output_dim, embed_dim)
        self.text_proj = nn.Linear(text_encoder.output_dim, embed_dim)
        
        # Learnable temperature
        self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))
    
    def forward(self, images, texts):
        # Encode
        vision_features = self.vision_encoder(images)
        text_features = self.text_encoder(texts)
        
        # Project and normalize
        vision_embeds = F.normalize(self.vision_proj(vision_features), dim=-1)
        text_embeds = F.normalize(self.text_proj(text_features), dim=-1)
        
        # Contrastive loss
        logits = vision_embeds @ text_embeds.T * self.logit_scale.exp()
        
        # Symmetric cross-entropy
        labels = torch.arange(len(images), device=images.device)
        loss_i2t = F.cross_entropy(logits, labels)
        loss_t2i = F.cross_entropy(logits.T, labels)
        
        return (loss_i2t + loss_t2i) / 2
```

**Training Strategy:**
- Batch size: 256-32,768 (larger = better)
- Temperature: 0.07 (learnable)
- Optimizer: AdamW with cosine schedule
- Data augmentation: Random crop, color jitter

### Pattern 2: Vision-Language Generation (BLIP, Flamingo)

**Use Case:** Image captioning, visual question answering

**Architecture:**
```
Image → Vision Encoder → Vision Tokens
                            ↓
                    Cross-Attention
                            ↓
Text → Text Decoder → Generated Text
```

**Implementation:**
```python
class VisionLanguageModel(nn.Module):
    def __init__(self, vision_encoder, text_decoder):
        super().__init__()
        self.vision_encoder = vision_encoder
        self.text_decoder = text_decoder
        
        # Cross-attention in decoder
        self.cross_attention_layers = nn.ModuleList([
            nn.MultiheadAttention(embed_dim=768, num_heads=12)
            for _ in range(12)
        ])
    
    def forward(self, images, text_tokens):
        # Encode image to patch tokens
        vision_tokens = self.vision_encoder(images)  # (B, N, D)
        
        # Generate text with cross-attention to vision
        text_embeds = self.text_decoder.embed_tokens(text_tokens)
        
        for layer in self.cross_attention_layers:
            # Self-attention on text
            text_embeds = layer(text_embeds, text_embeds, text_embeds)
            
            # Cross-attention to vision
            text_embeds = layer(text_embeds, vision_tokens, vision_tokens)
        
        logits = self.text_decoder.lm_head(text_embeds)
        return logits
```

**Training Strategy:**
- Pre-training: Image-text pairs with captioning objective
- Fine-tuning: Task-specific data (VQA, reasoning)
- Curriculum learning: Start with short captions, increase length

### Pattern 3: Multi-Modal Fusion for Classification

**Use Case:** Sentiment analysis (text+image), medical diagnosis (scan+notes)

**Architecture:**
```
Image → Vision Encoder → Vision Features
                              ↓
                         Fusion Layer
                              ↓
Text → Text Encoder → Text Features
           ↓
      Classifier
```

**Implementation:**
```python
class MultiModalClassifier(nn.Module):
    def __init__(self, num_classes, fusion_type='attention'):
        super().__init__()
        self.vision_encoder = torchvision.models.resnet50(pretrained=True)
        self.text_encoder = AutoModel.from_pretrained('bert-base-uncased')
        
        self.fusion_type = fusion_type
        
        if fusion_type == 'attention':
            # Gated attention fusion
            self.gate = nn.Sequential(
                nn.Linear(768 + 2048, 512),
                nn.Tanh(),
                nn.Linear(512, 1),
                nn.Sigmoid()
            )
        
        self.classifier = nn.Linear(768 + 2048, num_classes)
    
    def forward(self, images, text_input_ids):
        # Extract features
        vision_feats = self.vision_encoder(images)
        text_feats = self.text_encoder(text_input_ids).pooler_output
        
        # Fusion
        if self.fusion_type == 'concat':
            combined = torch.cat([vision_feats, text_feats], dim=-1)
        
        elif self.fusion_type == 'attention':
            concat = torch.cat([vision_feats, text_feats], dim=-1)
            gate = self.gate(concat)
            combined = gate * vision_feats + (1 - gate) * text_feats
        
        # Classify
        logits = self.classifier(combined)
        return logits
```

### Pattern 4: Audio-Visual Fusion

**Use Case:** Video understanding, speech recognition with visual context

**Architecture:**
```
Video Frames → Vision Encoder → Visual Features
                                      ↓
                               Temporal Fusion
                                      ↓
Audio → Audio Encoder → Audio Features
               ↓
           Predictions
```

**Implementation:**
```python
class AudioVisualModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        # Visual stream (per-frame)
        self.visual_encoder = torchvision.models.resnet50(pretrained=True)
        self.visual_temporal = nn.LSTM(2048, 512, bidirectional=True)
        
        # Audio stream
        self.audio_encoder = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=80, stride=16),
            nn.ReLU(),
            nn.Conv1d(64, 128, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        
        # Late fusion
        self.classifier = nn.Linear(1024 + 128, num_classes)
    
    def forward(self, video_frames, audio_waveform):
        # Process video frames
        B, T, C, H, W = video_frames.shape
        visual_feats = []
        for t in range(T):
            frame_feats = self.visual_encoder(video_frames[:, t])
            visual_feats.append(frame_feats)
        
        visual_feats = torch.stack(visual_feats, dim=1)
        visual_feats, _ = self.visual_temporal(visual_feats)
        visual_feats = visual_feats[:, -1, :]  # Last timestep
        
        # Process audio
        audio_feats = self.audio_encoder(audio_waveform).squeeze(-1)
        
        # Fuse and classify
        combined = torch.cat([visual_feats, audio_feats], dim=-1)
        logits = self.classifier(combined)
        return logits
```

## Design Decisions

### When to Use Early Fusion
- ✅ Modalities are tightly coupled (lip reading: video + audio)
- ✅ Simple baseline needed
- ❌ Different update frequencies
- ❌ Missing modalities at inference

### When to Use Late Fusion
- ✅ Modalities can work independently
- ✅ Different modalities available at different times
- ✅ Easy to add/remove modalities
- ❌ Limited cross-modal interaction

### When to Use Cross-Attention
- ✅ Need fine-grained alignment (VQA, image captioning)
- ✅ Variable-length inputs
- ✅ Large model capacity available
- ❌ Real-time inference needed (slower)

## Training Strategies

### 1. Staged Training

```python
# Stage 1: Train modality encoders separately
train_vision_encoder(image_data)
train_text_encoder(text_data)

# Stage 2: Freeze encoders, train fusion
vision_encoder.requires_grad_(False)
text_encoder.requires_grad_(False)
train_fusion_layer(paired_data)

# Stage 3: Fine-tune end-to-end
vision_encoder.requires_grad_(True)
text_encoder.requires_grad_(True)
finetune_all(paired_data, lr=1e-5)
```

### 2. Modality Dropout

Randomly drop modalities during training for robustness:

```python
def forward(self, images, texts, training=True):
    if training and random.random() < 0.3:
        # Drop vision
        vision_feats = torch.zeros_like(self.vision_encoder(images))
    else:
        vision_feats = self.vision_encoder(images)
    
    if training and random.random() < 0.3:
        # Drop text
        text_feats = torch.zeros_like(self.text_encoder(texts))
    else:
        text_feats = self.text_encoder(texts)
    
    return self.fusion(vision_feats, text_feats)
```

### 3. Hard Negative Mining

For contrastive learning:

```python
# Mine hard negatives (similar but not matching pairs)
with torch.no_grad():
    vision_embeds = model.vision_encoder(all_images)
    text_embeds = model.text_encoder(all_texts)
    similarity = vision_embeds @ text_embeds.T
    
    # Get top-K most similar but incorrect pairs
    hard_negatives = get_hard_negatives(similarity, labels, k=10)

# Train on original + hard negatives
loss = contrastive_loss(positives) + 0.5 * contrastive_loss(hard_negatives)
```

## Optimization Techniques

### 1. Memory Efficiency

**Gradient Checkpointing:**
```python
from torch.utils.checkpoint import checkpoint

class EfficientMultiModal(nn.Module):
    def forward(self, x):
        # Trade compute for memory
        x = checkpoint(self.heavy_layer_1, x)
        x = checkpoint(self.heavy_layer_2, x)
        return x
```

**Mixed Precision:**
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

with autocast():
    outputs = model(images, texts)
    loss = criterion(outputs, labels)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

### 2. Efficient Inference

**Knowledge Distillation:**
```python
# Distill large multi-modal model to smaller one
teacher_logits = teacher_model(images, texts)
student_logits = student_model(images, texts)

# KL divergence loss
distillation_loss = F.kl_div(
    F.log_softmax(student_logits / T, dim=-1),
    F.softmax(teacher_logits / T, dim=-1)
)
```

**Modality Pruning:**
```python
# Use only text for simple queries, add vision for complex
if query_complexity < threshold:
    return text_only_model(text)
else:
    return multimodal_model(text, image)
```

## Evaluation Metrics

### Cross-Modal Retrieval
- **R@K:** Recall at K (proportion of correct matches in top-K)
- **mAP:** Mean Average Precision
- **nDCG:** Normalized Discounted Cumulative Gain

### Generation
- **BLEU:** N-gram overlap (image captioning)
- **ROUGE:** Recall-based (summarization)
- **CIDEr:** Consensus-based metric
- **SPICE:** Semantic similarity

### Classification
- **Accuracy, F1:** Standard metrics
- **Per-modality ablation:** Test with each modality alone

## Common Pitfalls

### 1. Modality Imbalance
**Problem:** One modality dominates learning
**Solution:**
- Balance loss terms with weights
- Gradual unfreezing (train weak modality first)
- Modality-specific batch normalization

### 2. Misaligned Training/Inference
**Problem:** Model expects all modalities but some missing
**Solution:**
- Train with random modality dropout
- Separate models for different modality combinations
- Use default values for missing modalities

### 3. Overfitting on Small Paired Data
**Problem:** Large model, limited image-text pairs
**Solution:**
- Pre-train on large unpaired data
- Data augmentation for both modalities
- Use smaller model or adapter layers

## Production Considerations

### 1. Serving Strategy
```python
# Option 1: Encode offline, search online
pre_encoded_images = encode_all_images(image_db)
query_embedding = encode_text(user_query)
results = vector_search(query_embedding, pre_encoded_images)

# Option 2: Encode on-the-fly
results = multimodal_search(user_query, image_db)
```

### 2. Caching
```python
# Cache embeddings
@lru_cache(maxsize=10000)
def get_image_embedding(image_id):
    image = load_image(image_id)
    return vision_encoder(image)
```

### 3. Batch Processing
```python
# Batch encode for throughput
images_batch = stack_images(images_list)
embeddings = vision_encoder(images_batch)  # 100x faster than loop
```

## Next Steps

1. **Start Simple:** CLIP-style contrastive learning
2. **Experiment:** Try different fusion strategies
3. **Optimize:** Add efficiency techniques incrementally
4. **Monitor:** Track per-modality performance
5. **Iterate:** Improve based on production metrics
