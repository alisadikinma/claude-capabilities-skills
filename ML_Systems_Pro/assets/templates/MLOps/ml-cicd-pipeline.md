# ML CI/CD Pipeline Setup

Complete guide for implementing continuous integration and deployment pipelines for ML models.

## Overview

Traditional CI/CD + ML-specific components:

```
Code Changes → CI Pipeline → Model Training → Validation → CD Pipeline → Deployment
     ↓             ↓              ↓              ↓            ↓             ↓
  Git Push    Unit Tests    Hyperparameter   Performance  A/B Test    Production
               Lint         Optimization      Benchmarks   Deploy      Monitoring
```

## CI Pipeline (Continuous Integration)

### 1. Code Quality Checks

**.github/workflows/ml-ci.yml:**
```yaml
name: ML CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install flake8 black mypy pytest
      
      - name: Lint with flake8
        run: flake8 src/ --max-line-length=100
      
      - name: Format check with black
        run: black --check src/
      
      - name: Type check with mypy
        run: mypy src/ --ignore-missing-imports
  
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run unit tests
        run: pytest tests/unit/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          file: ./coverage.xml
```

### 2. Data Validation

**tests/test_data_validation.py:**
```python
import pytest
import pandas as pd
from great_expectations.dataset import PandasDataset

def test_training_data_schema():
    """Validate training data schema."""
    df = pd.read_parquet('data/training.parquet')
    dataset = PandasDataset(df)
    
    # Check required columns exist
    expected_columns = ['feature_1', 'feature_2', 'target']
    assert all(col in df.columns for col in expected_columns)
    
    # Check data types
    assert dataset.expect_column_values_to_be_of_type('feature_1', 'float64').success
    assert dataset.expect_column_values_to_be_of_type('target', 'int64').success

def test_training_data_quality():
    """Validate training data quality."""
    df = pd.read_parquet('data/training.parquet')
    dataset = PandasDataset(df)
    
    # Check for nulls
    assert dataset.expect_column_values_to_not_be_null('feature_1').success
    assert dataset.expect_column_values_to_not_be_null('target').success
    
    # Check ranges
    assert dataset.expect_column_values_to_be_between(
        'feature_1', min_value=-10, max_value=10
    ).success
    
    # Check distributions
    assert dataset.expect_column_mean_to_be_between(
        'feature_1', min_value=-1, max_value=1
    ).success
```

### 3. Model Training Tests

**tests/test_model_training.py:**
```python
import pytest
import numpy as np
from src.model import train_model, predict

def test_model_overfitting():
    """Check model doesn't overfit on small dataset."""
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    
    model = train_model(X, y)
    
    # Training accuracy shouldn't be 100% (sign of overfitting)
    train_acc = model.score(X, y)
    assert train_acc < 0.99, "Model may be overfitting"

def test_model_reproducibility():
    """Ensure model training is reproducible."""
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    
    model1 = train_model(X, y, random_state=42)
    model2 = train_model(X, y, random_state=42)
    
    pred1 = predict(model1, X)
    pred2 = predict(model2, X)
    
    assert np.allclose(pred1, pred2), "Training is not reproducible"
```

## CD Pipeline (Continuous Deployment)

### 1. Automated Training

**training_pipeline.py:**
```python
import mlflow
from sklearn.model_selection import train_test_split
from src.data import load_data
from src.model import train_model, evaluate_model

def run_training_pipeline():
    """
    Automated training pipeline with MLflow tracking.
    """
    # Start MLflow run
    with mlflow.start_run():
        # Load data
        X, y = load_data('data/training.parquet')
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Log data info
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("val_size", len(X_val))
        
        # Train model
        model = train_model(X_train, y_train)
        
        # Evaluate
        metrics = evaluate_model(model, X_val, y_val)
        for metric_name, value in metrics.items():
            mlflow.log_metric(metric_name, value)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Model trained with metrics: {metrics}")
        return model, metrics

if __name__ == "__main__":
    run_training_pipeline()
```

### 2. Model Validation Gates

**.github/workflows/ml-cd.yml:**
```yaml
name: ML CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  train-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Train model
        run: python training_pipeline.py
      
      - name: Validate model performance
        run: python validate_model.py --min-accuracy 0.85
      
      - name: Validate model size
        run: |
          python -c "import os; size = os.path.getsize('model.pkl'); \
          assert size < 100_000_000, f'Model too large: {size} bytes'"
      
      - name: Validate inference latency
        run: python benchmark_latency.py --max-latency-ms 100

  deploy-staging:
    needs: train-and-validate
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          # Deploy model to staging environment
          aws s3 cp model.pkl s3://ml-models/staging/model.pkl
          kubectl set image deployment/model-server \
            model-container=myregistry/model:${{ github.sha }} \
            -n staging
  
  integration-tests:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - name: Run integration tests
        run: pytest tests/integration/ --staging-url=https://staging.api.com
  
  deploy-production:
    needs: integration-tests
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production (canary)
        run: |
          # Deploy to 10% of traffic
          kubectl patch deployment model-server \
            -p '{"spec":{"replicas":1}}' -n production-canary
          
          # Monitor for 1 hour
          sleep 3600
          
          # If metrics good, full rollout
          kubectl patch deployment model-server \
            -p '{"spec":{"replicas":10}}' -n production
```

### 3. Model Registry Integration

**register_model.py:**
```python
import mlflow
from mlflow.tracking import MlflowClient

def register_model(run_id: str, model_name: str):
    """
    Register model in MLflow Model Registry.
    """
    client = MlflowClient()
    
    # Create model URI
    model_uri = f"runs:/{run_id}/model"
    
    # Register model
    result = mlflow.register_model(model_uri, model_name)
    
    # Transition to staging
    client.transition_model_version_stage(
        name=model_name,
        version=result.version,
        stage="Staging"
    )
    
    print(f"Registered {model_name} version {result.version}")
    return result

# Usage in CI/CD
if __name__ == "__main__":
    import sys
    run_id = sys.argv[1]
    register_model(run_id, "fraud_detection_model")
```

## A/B Testing Deployment

### 1. Gradual Rollout

**deployment.yaml:**
```yaml
# Canary deployment (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: model-server
      version: canary
  template:
    metadata:
      labels:
        app: model-server
        version: canary
    spec:
      containers:
      - name: model-container
        image: myregistry/model:v2
        resources:
          limits:
            memory: "2Gi"
            cpu: "1000m"

---
# Stable deployment (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: model-server
      version: stable
  template:
    metadata:
      labels:
        app: model-server
        version: stable
    spec:
      containers:
      - name: model-container
        image: myregistry/model:v1
```

### 2. Automated A/B Test Analysis

**ab_test_analysis.py:**
```python
import pandas as pd
from scipy import stats

def analyze_ab_test(canary_metrics: dict, stable_metrics: dict):
    """
    Analyze A/B test results.
    
    Returns True if canary is statistically better.
    """
    # Extract metrics
    canary_acc = canary_metrics['accuracy']
    stable_acc = stable_metrics['accuracy']
    
    canary_n = canary_metrics['sample_size']
    stable_n = stable_metrics['sample_size']
    
    # Z-test for proportions
    pooled_p = (canary_acc * canary_n + stable_acc * stable_n) / (canary_n + stable_n)
    pooled_se = (pooled_p * (1 - pooled_p) * (1/canary_n + 1/stable_n)) ** 0.5
    
    z_score = (canary_acc - stable_acc) / pooled_se
    p_value = 1 - stats.norm.cdf(z_score)
    
    # Decision criteria
    is_better = (canary_acc > stable_acc) and (p_value < 0.05)
    
    print(f"Canary accuracy: {canary_acc:.4f}")
    print(f"Stable accuracy: {stable_acc:.4f}")
    print(f"Z-score: {z_score:.4f}, p-value: {p_value:.4f}")
    print(f"Decision: {'PROMOTE' if is_better else 'REJECT'}")
    
    return is_better

# Usage
canary = {'accuracy': 0.87, 'sample_size': 10000}
stable = {'accuracy': 0.85, 'sample_size': 90000}

if analyze_ab_test(canary, stable):
    # Promote canary to full production
    subprocess.run(['kubectl', 'scale', 'deployment/model-canary', '--replicas=10'])
    subprocess.run(['kubectl', 'scale', 'deployment/model-stable', '--replicas=0'])
```

## Monitoring & Rollback

### 1. Automated Monitoring

**monitor_deployment.py:**
```python
import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

def monitor_deployment(deployment: str, duration_minutes: int = 60):
    """
    Monitor deployment metrics and auto-rollback if issues detected.
    """
    registry = CollectorRegistry()
    error_rate = Gauge('deployment_error_rate', 'Error rate', registry=registry)
    
    start_time = time.time()
    
    while time.time() - start_time < duration_minutes * 60:
        # Fetch metrics from Prometheus
        metrics = fetch_prometheus_metrics(deployment)
        
        # Check error rate
        if metrics['error_rate'] > 0.05:  # 5% threshold
            print(f"ERROR: High error rate detected: {metrics['error_rate']:.2%}")
            rollback_deployment(deployment)
            return False
        
        # Check latency
        if metrics['p99_latency_ms'] > 200:  # 200ms threshold
            print(f"ERROR: High latency detected: {metrics['p99_latency_ms']}ms")
            rollback_deployment(deployment)
            return False
        
        # Update metrics
        error_rate.set(metrics['error_rate'])
        push_to_gateway('localhost:9091', job='deployment_monitor', registry=registry)
        
        time.sleep(60)  # Check every minute
    
    print("Deployment monitoring passed!")
    return True

def rollback_deployment(deployment: str):
    """Rollback to previous version."""
    print(f"Rolling back {deployment}...")
    subprocess.run(['kubectl', 'rollout', 'undo', f'deployment/{deployment}'])
```

### 2. Blue-Green Deployment

```yaml
# Blue deployment (current production)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-blue
  labels:
    version: blue
spec:
  replicas: 10
  template:
    spec:
      containers:
      - name: model-container
        image: myregistry/model:v1

---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-green
  labels:
    version: green
spec:
  replicas: 10
  template:
    spec:
      containers:
      - name: model-container
        image: myregistry/model:v2

---
# Service routes to blue initially
apiVersion: v1
kind: Service
metadata:
  name: model-service
spec:
  selector:
    version: blue  # Switch to 'green' after validation
  ports:
  - port: 80
    targetPort: 8000
```

## Best Practices

### 1. Version Everything
- Code (Git tags)
- Data (DVC, S3 versioning)
- Models (MLflow Model Registry)
- Docker images (semantic versioning)
- Dependencies (requirements.txt with pins)

### 2. Immutable Artifacts
- Docker images are immutable
- Models are versioned, not overwritten
- Training data snapshots are preserved

### 3. Automated Testing
- Unit tests for data processing
- Integration tests for API endpoints
- Performance benchmarks (latency, throughput)
- Model quality tests (accuracy, fairness)

### 4. Gradual Rollouts
- Canary: 10% traffic → monitor → full rollout
- Blue-green: Deploy to green → test → switch traffic
- Feature flags: Enable for subset of users

### 5. Observability
- Log all predictions with inputs/outputs
- Monitor drift, performance, latency
- Alert on anomalies
- Track business metrics (revenue, conversions)

## Troubleshooting

### Issue: Training Fails in CI
**Solution:**
- Check data availability in CI environment
- Verify GPU/CPU resources sufficient
- Use smaller dataset for CI (full dataset in CD)
- Cache dependencies to speed up builds

### Issue: Model Performance Degrades
**Solution:**
- Automated rollback to previous version
- Investigate data drift
- Retrain on recent data
- A/B test new model before full rollout

### Issue: Slow Deployments
**Solution:**
- Use Docker layer caching
- Pre-build base images
- Parallel deployment across regions
- Optimize model size (quantization, pruning)

## Next Steps

1. **Start Simple:** Deploy manually first, automate incrementally
2. **Add Monitoring:** Set up basic metrics before automation
3. **Gradual Automation:** CI first, then CD with manual approval
4. **Iterate:** Add more validation gates and tests over time
