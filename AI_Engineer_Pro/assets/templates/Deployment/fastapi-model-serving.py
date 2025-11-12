"""
FastAPI Model Serving
Production-ready REST API for ML model deployment
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import torch
import numpy as np
from PIL import Image
import io
from typing import List, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="PCB Defect Detection API",
    description="ML model serving for PCB inspection",
    version="1.0.0"
)

# Load model at startup
@app.on_event("startup")
async def load_model():
    global model, device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    logger.info(f"Loading model on {device}")
    
    # Load your model
    from ultralytics import YOLO
    model = YOLO('best.pt')
    
    # Warmup
    dummy_img = torch.rand(1, 3, 640, 640).to(device)
    # _ = model(dummy_img)
    
    logger.info("Model loaded successfully")

# Request/Response models
class PredictionResponse(BaseModel):
    detections: List[dict]
    count: int
    inference_time: float

class HealthResponse(BaseModel):
    status: str
    device: str
    model_loaded: bool

# Health check
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "device": str(device),
        "model_loaded": model is not None
    }

# Single image detection
@app.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    confidence: float = 0.5,
    iou_threshold: float = 0.45
):
    """
    Detect defects in uploaded PCB image
    
    Args:
        file: Image file (JPG, PNG)
        confidence: Confidence threshold (0-1)
        iou_threshold: IoU threshold for NMS
    """
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Convert to numpy
        img_array = np.array(image)
        
        # Inference
        import time
        start_time = time.time()
        
        results = model.predict(
            img_array,
            conf=confidence,
            iou=iou_threshold,
            verbose=False
        )
        
        inference_time = time.time() - start_time
        
        # Parse results
        detections = []
        if results and len(results) > 0:
            boxes = results[0].boxes
            for i in range(len(boxes)):
                detections.append({
                    'class_id': int(boxes.cls[i]),
                    'class_name': results[0].names[int(boxes.cls[i])],
                    'confidence': float(boxes.conf[i]),
                    'bbox': boxes.xyxy[i].tolist(),
                })
        
        return {
            'detections': detections,
            'count': len(detections),
            'inference_time': inference_time
        }
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Batch prediction
@app.post("/predict/batch")
async def predict_batch(files: List[UploadFile] = File(...)):
    """Batch inference on multiple images"""
    results = []
    
    for file in files:
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            img_array = np.array(image)
            
            predictions = model.predict(img_array, verbose=False)
            
            detections = []
            if predictions and len(predictions) > 0:
                boxes = predictions[0].boxes
                for i in range(len(boxes)):
                    detections.append({
                        'class_name': predictions[0].names[int(boxes.cls[i])],
                        'confidence': float(boxes.conf[i]),
                        'bbox': boxes.xyxy[i].tolist(),
                    })
            
            results.append({
                'filename': file.filename,
                'detections': detections,
                'count': len(detections)
            })
        
        except Exception as e:
            results.append({
                'filename': file.filename,
                'error': str(e)
            })
    
    return {'results': results, 'total_images': len(files)}

# Text classification endpoint (for NLP models)
class TextRequest(BaseModel):
    text: str
    max_length: Optional[int] = 512

@app.post("/classify/text")
async def classify_text(request: TextRequest):
    """Text classification endpoint"""
    # Implement your text classifier here
    return {"prediction": "defect", "confidence": 0.95}

# Get model info
@app.get("/model/info")
async def model_info():
    """Get model metadata"""
    return {
        "model_name": "YOLOv8",
        "version": "1.0",
        "classes": list(model.names.values()),
        "input_size": [640, 640],
        "device": str(device)
    }

# Prometheus metrics (optional)
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse

request_count = Counter('api_requests_total', 'Total API requests', ['endpoint', 'status'])
inference_time_hist = Histogram('inference_duration_seconds', 'Inference duration')

@app.get("/metrics")
async def metrics():
    return PlainTextResponse(generate_latest())

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        reload=False
    )

# ========================================
# Docker Deployment
# ========================================

"""
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
"""

# ========================================
# Client Example
# ========================================

"""
import requests

# Single prediction
with open('test.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f},
        params={'confidence': 0.5}
    )

print(response.json())

# Batch prediction
files = [
    ('files', open('img1.jpg', 'rb')),
    ('files', open('img2.jpg', 'rb')),
]

response = requests.post('http://localhost:8000/predict/batch', files=files)
print(response.json())
"""

# ========================================
# Load Testing
# ========================================

"""
# locust_test.py
from locust import HttpUser, task, between

class ModelAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def predict(self):
        files = {'file': open('test.jpg', 'rb')}
        self.client.post('/predict', files=files)

# Run: locust -f locust_test.py --host=http://localhost:8000
"""
