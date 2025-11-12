# YOLOv8 Object Detection Setup

Complete guide for PCB component detection and defect inspection using YOLOv8.

## Installation

```bash
pip install ultralytics opencv-python pillow
```

## Quick Start - PCB Defect Detection

```python
from ultralytics import YOLO
import cv2

# Load pre-trained model
model = YOLO('yolov8n.pt')  # nano (fastest)
# model = YOLO('yolov8s.pt')  # small
# model = YOLO('yolov8m.pt')  # medium
# model = YOLO('yolov8l.pt')  # large
# model = YOLO('yolov8x.pt')  # extra large (most accurate)

# Train on custom PCB dataset
results = model.train(
    data='pcb_defects.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='pcb_defect_detector'
)

# Inference
results = model.predict('pcb_test.jpg', conf=0.5)

# Visualize
annotated = results[0].plot()
cv2.imwrite('result.jpg', annotated)
```

## Dataset Format (YOLO Format)

### Directory Structure
```
pcb_dataset/
├── images/
│   ├── train/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   ├── val/
│   │   ├── img100.jpg
│   │   └── ...
│   └── test/
│       └── ...
└── labels/
    ├── train/
    │   ├── img001.txt  # Same name as image
    │   ├── img002.txt
    │   └── ...
    ├── val/
    │   └── ...
    └── test/
        └── ...
```

### Label Format (one line per object)
```
# Format: class_id center_x center_y width height (normalized 0-1)
0 0.512 0.345 0.234 0.156  # scratch
1 0.789 0.567 0.098 0.123  # missing_component
2 0.234 0.890 0.156 0.089  # solder_bridge
```

### Dataset Config (pcb_defects.yaml)
```yaml
# Dataset paths
path: /path/to/pcb_dataset
train: images/train
val: images/val
test: images/test

# Class names
names:
  0: scratch
  1: crack
  2: missing_component
  3: solder_bridge
  4: short_circuit
  5: open_circuit
  6: misalignment
  7: excess_solder
```

## Complete Training Script

```python
from ultralytics import YOLO
import torch
from pathlib import Path

class YOLOv8Trainer:
    def __init__(self, model_size='n', data_yaml='pcb_defects.yaml'):
        """
        model_size: 'n' (nano), 's' (small), 'm' (medium), 'l' (large), 'x' (xlarge)
        """
        self.model = YOLO(f'yolov8{model_size}.pt')
        self.data_yaml = data_yaml
    
    def train(self, 
              epochs=100, 
              imgsz=640, 
              batch=16,
              device=0,  # GPU device, or 'cpu'
              project='runs/detect',
              name='pcb_detector',
              **kwargs):
        """
        Train YOLOv8 model
        
        Common kwargs:
        - patience: Early stopping patience (default: 50)
        - save_period: Save checkpoint every N epochs
        - cache: Cache images in RAM ('ram') or disk ('disk')
        - workers: Number of dataloader workers
        - pretrained: Use pretrained weights (default: True)
        - optimizer: 'SGD', 'Adam', 'AdamW', 'RMSProp'
        - lr0: Initial learning rate (default: 0.01)
        - momentum: SGD momentum (default: 0.937)
        - weight_decay: Optimizer weight decay (default: 0.0005)
        - mosaic: Use mosaic augmentation (default: 1.0)
        - mixup: Use mixup augmentation (default: 0.0)
        - augment: Enable augmentation (default: True)
        """
        
        results = self.model.train(
            data=self.data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            device=device,
            project=project,
            name=name,
            exist_ok=False,
            verbose=True,
            **kwargs
        )
        
        return results
    
    def validate(self, **kwargs):
        """Validate model on validation set"""
        metrics = self.model.val(**kwargs)
        
        print(f"\n📊 Validation Metrics:")
        print(f"   mAP50: {metrics.box.map50:.4f}")
        print(f"   mAP50-95: {metrics.box.map:.4f}")
        print(f"   Precision: {metrics.box.mp:.4f}")
        print(f"   Recall: {metrics.box.mr:.4f}")
        
        return metrics
    
    def predict(self, source, conf=0.25, iou=0.7, save=True, **kwargs):
        """
        Run inference
        
        source: Image file, folder, URL, or video
        conf: Confidence threshold (0-1)
        iou: NMS IoU threshold
        save: Save annotated images
        
        Common kwargs:
        - imgsz: Inference image size
        - show: Display results
        - save_txt: Save results as .txt
        - save_conf: Save confidence in txt labels
        - line_width: Bounding box line width
        - visualize: Visualize model features
        """
        
        results = self.model.predict(
            source=source,
            conf=conf,
            iou=iou,
            save=save,
            **kwargs
        )
        
        return results
    
    def export(self, format='onnx', **kwargs):
        """
        Export model to different formats
        
        formats: onnx, torchscript, tensorflow, coreml, tflite, etc.
        """
        path = self.model.export(format=format, **kwargs)
        print(f"✅ Model exported to: {path}")
        return path

# Training example
if __name__ == "__main__":
    trainer = YOLOv8Trainer(model_size='m', data_yaml='pcb_defects.yaml')
    
    # Train
    results = trainer.train(
        epochs=100,
        imgsz=640,
        batch=16,
        device=0,
        name='pcb_defect_v1',
        patience=20,
        save_period=10,
        cache='ram',
        optimizer='AdamW',
        lr0=0.001,
        augment=True,
        mosaic=1.0
    )
    
    # Validate
    metrics = trainer.validate()
    
    # Export to ONNX
    trainer.export(format='onnx', imgsz=640)
```

## Data Augmentation

```python
# Built-in augmentation parameters in train()
results = model.train(
    data='pcb_defects.yaml',
    
    # Augmentation settings
    hsv_h=0.015,        # HSV-Hue augmentation
    hsv_s=0.7,          # HSV-Saturation augmentation
    hsv_v=0.4,          # HSV-Value augmentation
    degrees=0.0,        # Image rotation (+/- deg)
    translate=0.1,      # Image translation (+/- fraction)
    scale=0.5,          # Image scale (+/- gain)
    shear=0.0,          # Image shear (+/- deg)
    perspective=0.0,    # Image perspective (+/- fraction)
    flipud=0.0,         # Image flip up-down (probability)
    fliplr=0.5,         # Image flip left-right (probability)
    mosaic=1.0,         # Mosaic augmentation (probability)
    mixup=0.0,          # MixUp augmentation (probability)
    copy_paste=0.0,     # Copy-paste augmentation (probability)
)
```

## Advanced Inference

```python
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO('runs/detect/pcb_defect_v1/weights/best.pt')

# Batch inference
results = model.predict(['img1.jpg', 'img2.jpg', 'img3.jpg'])

# Process results
for i, result in enumerate(results):
    # Get boxes
    boxes = result.boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
    confidences = result.boxes.conf.cpu().numpy()
    class_ids = result.boxes.cls.cpu().numpy().astype(int)
    
    # Get class names
    names = result.names
    
    # Draw custom annotations
    img = result.orig_img.copy()
    for box, conf, cls_id in zip(boxes, confidences, class_ids):
        x1, y1, x2, y2 = box.astype(int)
        label = f"{names[cls_id]} {conf:.2f}"
        
        # Different colors for different defects
        color = (0, 255, 0) if cls_id == 0 else (0, 0, 255)
        
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, label, (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    cv2.imwrite(f'annotated_{i}.jpg', img)

# Video inference
results = model.predict('pcb_inspection_video.mp4', stream=True)

for result in results:
    annotated = result.plot()
    cv2.imshow('YOLOv8', annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
```

## Performance Optimization

### TensorRT (NVIDIA GPUs)
```bash
# Export to TensorRT
python -m ultralytics.yolo.engine.export model=best.pt format=engine device=0

# Use TensorRT model
model = YOLO('best.engine')
results = model.predict('test.jpg')
```

### ONNX Runtime
```python
# Export to ONNX
model.export(format='onnx', imgsz=640, simplify=True)

# Load and run with ONNX Runtime
import onnxruntime as ort

session = ort.InferenceSession('best.onnx', providers=['CUDAExecutionProvider'])
# Run inference...
```

## Multi-GPU Training

```bash
# Using DDP (Distributed Data Parallel)
yolo detect train data=pcb_defects.yaml model=yolov8m.pt epochs=100 device=0,1,2,3
```

## Hyperparameter Tuning

```python
from ultralytics import YOLO

model = YOLO('yolov8m.pt')

# Hyperparameter tuning
model.tune(
    data='pcb_defects.yaml',
    epochs=30,
    iterations=300,
    optimizer='AdamW',
    plots=True,
    save=True,
    val=True
)
```

## Deployment - FastAPI Server

```python
from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import cv2
import numpy as np
from io import BytesIO

app = FastAPI()
model = YOLO('best.pt')

@app.post("/detect/")
async def detect_defects(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Inference
    results = model.predict(img, conf=0.5)
    
    # Extract detections
    detections = []
    for box, conf, cls in zip(
        results[0].boxes.xyxy,
        results[0].boxes.conf,
        results[0].boxes.cls
    ):
        detections.append({
            'class': model.names[int(cls)],
            'confidence': float(conf),
            'bbox': box.tolist()
        })
    
    return {'detections': detections}

# Run: uvicorn app:app --host 0.0.0.0 --port 8000
```

## Key Benefits for PCB Inspection

- ✅ Real-time detection (60+ FPS on GPU)
- ✅ High accuracy (mAP > 90% with good data)
- ✅ Easy to train on custom datasets
- ✅ Multi-class defect detection
- ✅ Export to edge devices (Jetson, mobile)
- ✅ Active community and updates
