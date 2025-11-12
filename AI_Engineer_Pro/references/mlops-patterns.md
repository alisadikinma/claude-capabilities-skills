# MLOps Patterns

## CI/CD for ML

**Pipeline Stages**
1. Data validation → 2. Training → 3. Evaluation → 4. Deployment

**GitLab CI Example**
```yaml
stages:
  - test
  - train
  - deploy

train:
  stage: train
  script:
    - python train.py
    - python evaluate.py
  artifacts:
    paths:
      - model.pt
      - metrics.json

deploy:
  stage: deploy
  script:
    - docker build -t model:v1 .
    - kubectl apply -f deployment.yaml
  only:
    - main
```

## Model Versioning

**DVC (Data Version Control)**
```bash
dvc init
dvc add data/train.csv
dvc add models/model.pt
git add data/train.csv.dvc models/model.pt.dvc
git commit -m "Add data and model"
```

**MLflow Model Registry**
```python
mlflow.register_model("runs:/run_id/model", "pcb_detector")
mlflow.transition_model_version_stage("pcb_detector", 1, "Production")
```

## A/B Testing

```python
# Route 10% to new model
if random.random() < 0.1:
    result = model_v2.predict(input)
else:
    result = model_v1.predict(input)
```

## Monitoring

**Key Metrics**
- Inference latency (p50, p95, p99)
- Throughput (requests/second)
- Model accuracy (live validation sample)
- Resource usage (CPU, GPU, memory)

**Data Drift Detection**
```python
from evidently import ColumnMapping
from evidently.metrics import DataDriftTable

report = DataDriftTable()
report.calculate(reference_data, current_data, column_mapping)
```

## Retraining Triggers

- Performance drops below threshold
- New labeled data available (weekly/monthly)
- Data distribution changes (drift detected)
- Manual trigger for experiments

## Deployment Patterns

**Shadow Mode**: Run new model alongside old, compare outputs
**Canary**: Route 5-10% traffic to new model
**Blue-Green**: Switch all traffic at once (easy rollback)
