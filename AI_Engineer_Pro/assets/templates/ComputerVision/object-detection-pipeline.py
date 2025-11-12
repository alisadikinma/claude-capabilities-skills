"""
Complete Object Detection Pipeline
End-to-end workflow from data prep to deployment
"""

import torch
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
import json

class ObjectDetectionPipeline:
    """Complete detection pipeline for PCB inspection"""
    
    def __init__(self, model_path: str, config_path: str = None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_model(model_path)
        self.config = self.load_config(config_path) if config_path else {}
        
    def load_model(self, model_path: str):
        """Load trained model"""
        if model_path.endswith('.pt'):  # YOLOv8
            from ultralytics import YOLO
            model = YOLO(model_path)
        elif model_path.endswith('.pth'):  # PyTorch
            model = torch.load(model_path, map_location=self.device)
            model.eval()
        else:
            raise ValueError(f"Unsupported model format: {model_path}")
        return model
    
    def load_config(self, config_path: str) -> Dict:
        """Load detection config"""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def preprocess_image(self, image: np.ndarray, target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
        """Preprocess image for inference"""
        # Resize while maintaining aspect ratio
        h, w = image.shape[:2]
        scale = min(target_size[0] / h, target_size[1] / w)
        new_h, new_w = int(h * scale), int(w * scale)
        
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        # Pad to target size
        padded = np.full((target_size[0], target_size[1], 3), 114, dtype=np.uint8)
        padded[:new_h, :new_w] = resized
        
        return padded
    
    def detect(self, image: np.ndarray, conf_threshold: float = 0.5, iou_threshold: float = 0.45) -> List[Dict]:
        """Run object detection"""
        
        # Preprocess
        processed = self.preprocess_image(image)
        
        # Inference
        results = self.model.predict(processed, conf=conf_threshold, iou=iou_threshold, verbose=False)
        
        # Parse results
        detections = []
        if results and len(results) > 0:
            boxes = results[0].boxes
            for i in range(len(boxes)):
                detections.append({
                    'class_id': int(boxes.cls[i]),
                    'class_name': results[0].names[int(boxes.cls[i])],
                    'confidence': float(boxes.conf[i]),
                    'bbox': boxes.xyxy[i].tolist(),  # [x1, y1, x2, y2]
                })
        
        return detections
    
    def visualize(self, image: np.ndarray, detections: List[Dict], output_path: str = None) -> np.ndarray:
        """Draw bounding boxes on image"""
        annotated = image.copy()
        
        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            conf = det['confidence']
            label = f"{det['class_name']}: {conf:.2f}"
            
            # Color based on defect type
            color = self._get_color(det['class_name'])
            
            # Draw box and label
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Label background
            (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(annotated, (x1, y1 - text_h - 10), (x1 + text_w, y1), color, -1)
            cv2.putText(annotated, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        if output_path:
            cv2.imwrite(output_path, annotated)
        
        return annotated
    
    def _get_color(self, class_name: str) -> Tuple[int, int, int]:
        """Get color for defect type"""
        colors = {
            'scratch': (0, 255, 255),      # Yellow
            'crack': (0, 0, 255),          # Red
            'missing': (255, 0, 0),        # Blue
            'solder': (0, 255, 0),         # Green
            'misalignment': (255, 0, 255), # Magenta
        }
        for key, color in colors.items():
            if key in class_name.lower():
                return color
        return (128, 128, 128)  # Gray for unknown
    
    def batch_detect(self, image_folder: str, output_folder: str, conf_threshold: float = 0.5):
        """Batch detection on folder"""
        image_folder = Path(image_folder)
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        
        results_list = []
        
        for img_path in image_folder.glob('*.jpg'):
            print(f"Processing: {img_path.name}")
            
            # Load and detect
            image = cv2.imread(str(img_path))
            detections = self.detect(image, conf_threshold=conf_threshold)
            
            # Visualize
            output_path = output_folder / f"annotated_{img_path.name}"
            self.visualize(image, detections, str(output_path))
            
            # Save results
            results_list.append({
                'image': img_path.name,
                'detections': detections
            })
        
        # Save JSON results
        with open(output_folder / 'detections.json', 'w') as f:
            json.dump(results_list, f, indent=2)
        
        print(f"✅ Processed {len(results_list)} images")
        return results_list
    
    def filter_by_confidence(self, detections: List[Dict], min_conf: float = 0.7) -> List[Dict]:
        """Filter detections by confidence"""
        return [d for d in detections if d['confidence'] >= min_conf]
    
    def filter_by_class(self, detections: List[Dict], classes: List[str]) -> List[Dict]:
        """Filter detections by class names"""
        return [d for d in detections if d['class_name'] in classes]
    
    def nms_filter(self, detections: List[Dict], iou_threshold: float = 0.45) -> List[Dict]:
        """Non-Maximum Suppression for overlapping boxes"""
        if not detections:
            return []
        
        boxes = np.array([d['bbox'] for d in detections])
        scores = np.array([d['confidence'] for d in detections])
        
        x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
        areas = (x2 - x1) * (y2 - y1)
        order = scores.argsort()[::-1]
        
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            
            w = np.maximum(0, xx2 - xx1)
            h = np.maximum(0, yy2 - yy1)
            inter = w * h
            iou = inter / (areas[i] + areas[order[1:]] - inter)
            
            inds = np.where(iou <= iou_threshold)[0]
            order = order[inds + 1]
        
        return [detections[i] for i in keep]

# Example usage
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = ObjectDetectionPipeline(model_path='best.pt')
    
    # Single image detection
    image = cv2.imread('test_pcb.jpg')
    detections = pipeline.detect(image, conf_threshold=0.5)
    
    print(f"Found {len(detections)} defects:")
    for det in detections:
        print(f"  - {det['class_name']}: {det['confidence']:.2f}")
    
    # Visualize
    pipeline.visualize(image, detections, 'output.jpg')
    
    # Batch processing
    pipeline.batch_detect('test_images/', 'results/', conf_threshold=0.6)
