# Image Classification Setup

Quick setup for image classification tasks (defect classification, component recognition).

## PyTorch Classification

```python
import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import os

# Dataset
class ImageClassificationDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = sorted(os.listdir(root_dir))
        self.class_to_idx = {cls: i for i, cls in enumerate(self.classes)}
        
        self.samples = []
        for cls in self.classes:
            cls_folder = os.path.join(root_dir, cls)
            for img_name in os.listdir(cls_folder):
                self.samples.append((os.path.join(cls_folder, img_name), self.class_to_idx[cls]))
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, label

# Transforms
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Model (Transfer Learning)
model = models.resnet50(pretrained=True)
num_classes = 5  # Change to your number of classes
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Or use EfficientNet
# from efficientnet_pytorch import EfficientNet
# model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=num_classes)

# Training loop (see pytorch-training-pipeline.py for complete version)
```

## TensorFlow Classification

```python
import tensorflow as tf
from tensorflow.keras import layers, models, applications

# Data pipeline
train_ds = tf.keras.utils.image_dataset_from_directory(
    'data/train',
    image_size=(224, 224),
    batch_size=32,
    label_mode='categorical'
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    'data/val',
    image_size=(224, 224),
    batch_size=32,
    label_mode='categorical'
)

# Augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
])

# Transfer learning model
base_model = applications.ResNet50(
    include_top=False,
    weights='imagenet',
    input_shape=(224, 224, 3)
)
base_model.trainable = False

model = models.Sequential([
    data_augmentation,
    layers.Rescaling(1./255),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(train_ds, validation_data=val_ds, epochs=20)
```

## Inference

```python
# Load model
model = torch.load('best_model.pth')
model.eval()

# Predict
def predict(image_path, model, transform):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(image)
        probs = torch.softmax(output, dim=1)
        conf, pred = torch.max(probs, 1)
    
    return pred.item(), conf.item()

# Usage
class_idx, confidence = predict('test.jpg', model, val_transform)
print(f"Predicted class: {class_idx} with confidence: {confidence:.2f}")
```

## Key Models for PCB Inspection

| Model | Params | Accuracy | Speed | Use Case |
|-------|--------|----------|-------|----------|
| ResNet50 | 25M | High | Medium | General classification |
| EfficientNet-B0 | 5M | High | Fast | Edge deployment |
| MobileNetV2 | 3.5M | Medium | Very Fast | Real-time mobile |
| Vision Transformer | 86M | Very High | Slow | High accuracy priority |
