# MLflow Experiment Tracking Setup

Complete guide for experiment tracking, model versioning, and reproducibility with MLflow.

## Installation

```bash
pip install mlflow

# Start MLflow UI
mlflow ui --host 0.0.0.0 --port 5000
# Access at: http://localhost:5000
```

## Basic MLflow Integration

```python
import mlflow
import mlflow.pytorch  # or mlflow.tensorflow
from mlflow.tracking import MlflowClient

# Set tracking URI (local or remote)
mlflow.set_tracking_uri("http://localhost:5000")  # Or file://./mlruns for local

# Set experiment
mlflow.set_experiment("PCB_Defect_Detection")

# Start a run
with mlflow.start_run(run_name="yolov8_experiment_001"):
    
    # Log parameters
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 32)
    mlflow.log_param("epochs", 100)
    mlflow.log_param("model_architecture", "YOLOv8")
    mlflow.log_param("optimizer", "AdamW")
    
    # Train your model here
    # ...
    
    # Log metrics
    mlflow.log_metric("train_loss", 0.234, step=1)
    mlflow.log_metric("val_loss", 0.345, step=1)
    mlflow.log_metric("mAP", 0.856, step=1)
    
    # Log artifacts (files)
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.log_artifact("config.yaml")
    
    # Log model
    mlflow.pytorch.log_model(model, "model")
    # Or for TensorFlow:
    # mlflow.tensorflow.log_model(model, "model")
```

## Complete Training with MLflow

```python
import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm

class MLflowTrainer:
    def __init__(self, model, train_loader, val_loader, config):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config
        
        # Setup MLflow
        mlflow.set_tracking_uri(config.mlflow_uri)
        mlflow.set_experiment(config.experiment_name)
        
    def train(self):
        with mlflow.start_run(run_name=self.config.run_name) as run:
            
            # Log all hyperparameters
            mlflow.log_params({
                "learning_rate": self.config.learning_rate,
                "batch_size": self.config.batch_size,
                "num_epochs": self.config.num_epochs,
                "optimizer": self.config.optimizer,
                "model_architecture": self.config.model_name,
                "weight_decay": self.config.weight_decay,
                "dropout": self.config.dropout,
            })
            
            # Log system info
            mlflow.log_param("device", str(self.config.device))
            mlflow.log_param("num_gpus", torch.cuda.device_count())
            
            # Setup optimizer and criterion
            optimizer = torch.optim.AdamW(
                self.model.parameters(),
                lr=self.config.learning_rate,
                weight_decay=self.config.weight_decay
            )
            criterion = nn.CrossEntropyLoss()
            
            best_val_loss = float('inf')
            
            for epoch in range(self.config.num_epochs):
                # Training
                train_loss, train_acc = self.train_epoch(
                    epoch, optimizer, criterion
                )
                
                # Validation
                val_loss, val_acc = self.validate(epoch, criterion)
                
                # Log metrics per epoch
                mlflow.log_metrics({
                    "train_loss": train_loss,
                    "train_accuracy": train_acc,
                    "val_loss": val_loss,
                    "val_accuracy": val_acc,
                    "learning_rate": optimizer.param_groups[0]['lr']
                }, step=epoch)
                
                # Save best model
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    
                    # Log model to MLflow
                    mlflow.pytorch.log_model(
                        self.model,
                        "best_model",
                        registered_model_name=self.config.model_name
                    )
                    
                    # Log checkpoint locally too
                    torch.save({
                        'epoch': epoch,
                        'model_state_dict': self.model.state_dict(),
                        'optimizer_state_dict': optimizer.state_dict(),
                        'val_loss': val_loss,
                    }, 'best_checkpoint.pth')
                    
                    mlflow.log_artifact('best_checkpoint.pth')
            
            # Log final metrics
            mlflow.log_metric("best_val_loss", best_val_loss)
            
            # Log training artifacts
            self.log_artifacts()
            
            # Add tags
            mlflow.set_tags({
                "status": "completed",
                "framework": "pytorch",
                "task": "classification"
            })
            
            print(f"✅ MLflow Run ID: {run.info.run_id}")
    
    def train_epoch(self, epoch, optimizer, criterion):
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for images, labels in tqdm(self.train_loader, desc=f"Epoch {epoch}"):
            images = images.to(self.config.device)
            labels = labels.to(self.config.device)
            
            optimizer.zero_grad()
            outputs = self.model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
        
        avg_loss = total_loss / len(self.train_loader)
        accuracy = 100. * correct / total
        return avg_loss, accuracy
    
    def validate(self, epoch, criterion):
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in self.val_loader:
                images = images.to(self.config.device)
                labels = labels.to(self.config.device)
                
                outputs = self.model(images)
                loss = criterion(outputs, labels)
                
                total_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
        
        avg_loss = total_loss / len(self.val_loader)
        accuracy = 100. * correct / total
        return avg_loss, accuracy
    
    def log_artifacts(self):
        """Log additional artifacts like plots, configs"""
        # Log training plots
        # self.plot_metrics()
        # mlflow.log_artifact("training_curves.png")
        
        # Log config
        import json
        with open("config.json", "w") as f:
            json.dump(vars(self.config), f, indent=2)
        mlflow.log_artifact("config.json")
```

## Model Registry

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
model_name = "PCB_Defect_Detector"
model_uri = f"runs:/{run_id}/model"

registered_model = mlflow.register_model(
    model_uri=model_uri,
    name=model_name
)

# Transition model to production
client.transition_model_version_stage(
    name=model_name,
    version=registered_model.version,
    stage="Production"
)

# Load production model
model = mlflow.pytorch.load_model(
    model_uri=f"models:/{model_name}/Production"
)
```

## Compare Experiments

```python
import pandas as pd

# Search runs
experiment_id = mlflow.get_experiment_by_name("PCB_Defect_Detection").experiment_id
runs = mlflow.search_runs(experiment_ids=[experiment_id])

# Filter by metric
best_runs = runs.sort_values("metrics.val_loss").head(5)

print("Top 5 runs by validation loss:")
print(best_runs[["run_id", "metrics.val_loss", "metrics.val_accuracy", "params.learning_rate"]])

# Get specific run details
run_id = best_runs.iloc[0]["run_id"]
run_data = mlflow.get_run(run_id).data

print(f"\nBest run parameters:")
for param, value in run_data.params.items():
    print(f"  {param}: {value}")
```

## Hyperparameter Tuning with MLflow

```python
import mlflow
from itertools import product

# Define hyperparameter grid
param_grid = {
    'learning_rate': [1e-4, 1e-3, 1e-2],
    'batch_size': [16, 32, 64],
    'dropout': [0.3, 0.5, 0.7]
}

# Grid search
for lr, bs, dropout in product(*param_grid.values()):
    with mlflow.start_run(run_name=f"lr_{lr}_bs_{bs}_dropout_{dropout}"):
        # Log parameters
        mlflow.log_params({
            'learning_rate': lr,
            'batch_size': bs,
            'dropout': dropout
        })
        
        # Train model with these params
        config = TrainingConfig(
            learning_rate=lr,
            batch_size=bs,
            dropout=dropout
        )
        
        val_loss = train_model(config)
        
        # Log result
        mlflow.log_metric("val_loss", val_loss)

# Find best parameters
best_run = mlflow.search_runs(
    experiment_ids=[experiment_id],
    order_by=["metrics.val_loss ASC"],
    max_results=1
)
print(f"Best parameters: {best_run.iloc[0]['params']}")
```

## Autologging (Automatic Tracking)

```python
# PyTorch autologging
mlflow.pytorch.autolog(
    log_every_n_epoch=1,
    log_models=True,
    disable=False,
    exclusive=True
)

# TensorFlow autologging
mlflow.tensorflow.autolog(
    every_n_iter=100,
    log_models=True
)

# Train as usual - metrics logged automatically
trainer.train()
```

## Remote Tracking Server

```bash
# Start MLflow server with backend store
mlflow server \
    --backend-store-uri postgresql://user:password@localhost/mlflow \
    --default-artifact-root s3://my-mlflow-bucket \
    --host 0.0.0.0 \
    --port 5000

# In code, connect to remote server
mlflow.set_tracking_uri("http://mlflow-server.com:5000")
```

## Best Practices

1. **Naming**: Use descriptive experiment and run names
2. **Parameters**: Log ALL hyperparameters for reproducibility
3. **Metrics**: Log both training and validation metrics
4. **Artifacts**: Save confusion matrices, training curves, model configs
5. **Tags**: Add tags for filtering (e.g., "baseline", "production")
6. **Model Registry**: Use for versioning and deployment tracking
7. **Comparison**: Regularly compare runs to identify best models

## Integration with Weights & Biases (Alternative)

```python
import wandb

# Initialize
wandb.init(
    project="PCB_Defect_Detection",
    config={
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 100
    }
)

# Log metrics
wandb.log({"train_loss": loss, "val_accuracy": acc})

# Log model
wandb.save("best_model.pth")

# Finish run
wandb.finish()
```
