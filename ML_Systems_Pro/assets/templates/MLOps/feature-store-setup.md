# Feature Store Setup with Feast

Complete guide for implementing production feature stores using Feast.

## What is a Feature Store?

**Problem:** ML features scattered across notebooks, databases, pipelines
**Solution:** Centralized feature management with online/offline serving

**Benefits:**
- **Consistency:** Same features for training and serving
- **Reusability:** Share features across teams and models
- **Governance:** Track feature lineage and ownership
- **Performance:** Optimized serving with caching

## Architecture

```
Data Sources → Feature Engineering → Feature Store
                                          ↓
                              ┌───────────┴───────────┐
                              ↓                       ↓
                        Online Store              Offline Store
                        (Redis, DynamoDB)         (S3, BigQuery)
                              ↓                       ↓
                        Real-time Serving      Batch Training
```

## Installation

```bash
pip install feast redis boto3 pandas pyarrow
```

## Basic Setup

### 1. Initialize Feast Project

```bash
feast init feature_repo
cd feature_repo
```

Project structure:
```
feature_repo/
├── feature_store.yaml   # Configuration
├── features.py          # Feature definitions
└── data/               # Local data (optional)
```

### 2. Configure Feature Store

**feature_store.yaml:**
```yaml
project: recommendation_system
registry: data/registry.db
provider: local
online_store:
  type: redis
  connection_string: localhost:6379
offline_store:
  type: file  # or 'bigquery', 'snowflake', 'redshift'
```

### 3. Define Entities and Features

**features.py:**
```python
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from datetime import timedelta

# Define entity (primary key)
user = Entity(
    name="user_id",
    value_type=ValueType.STRING,
    description="User identifier"
)

# Define feature source (where raw data comes from)
user_features_source = FileSource(
    path="data/user_features.parquet",
    event_timestamp_column="event_timestamp"
)

# Define feature view (transformation + metadata)
user_features = FeatureView(
    name="user_features",
    entities=["user_id"],
    ttl=timedelta(days=7),  # Feature freshness
    features=[
        Feature(name="age", dtype=ValueType.INT64),
        Feature(name="total_purchases", dtype=ValueType.INT64),
        Feature(name="avg_rating", dtype=ValueType.FLOAT),
        Feature(name="last_purchase_days_ago", dtype=ValueType.INT64),
    ],
    online=True,  # Enable online serving
    source=user_features_source,
    tags={"team": "recommendations"}
)
```

### 4. Apply Feature Definitions

```bash
feast apply
```

This registers features in the registry and creates necessary infrastructure.

## Feature Engineering Workflows

### Batch Feature Generation

```python
import pandas as pd
from datetime import datetime, timedelta

# Generate features from raw data
def compute_user_features(transactions_df):
    """
    Compute user features from transaction history.
    """
    user_features = transactions_df.groupby('user_id').agg({
        'amount': ['sum', 'mean', 'count'],
        'rating': 'mean',
        'timestamp': 'max'
    })
    
    user_features.columns = [
        'total_spent',
        'avg_spent',
        'total_purchases',
        'avg_rating',
        'last_purchase_timestamp'
    ]
    
    # Compute days since last purchase
    now = datetime.now()
    user_features['last_purchase_days_ago'] = (
        now - user_features['last_purchase_timestamp']
    ).dt.days
    
    user_features['event_timestamp'] = now
    
    return user_features.reset_index()

# Load raw data
transactions = pd.read_parquet('transactions.parquet')

# Compute features
user_features = compute_user_features(transactions)

# Save to feature source
user_features.to_parquet('data/user_features.parquet')
```

### Materialization (Online Store)

```python
from feast import FeatureStore
from datetime import datetime, timedelta

fs = FeatureStore(repo_path=".")

# Materialize features to online store
fs.materialize(
    start_date=datetime.now() - timedelta(days=7),
    end_date=datetime.now()
)
```

## Feature Retrieval

### Online Serving (Real-time)

```python
from feast import FeatureStore

fs = FeatureStore(repo_path=".")

# Get features for inference
entity_rows = [
    {"user_id": "user_123"},
    {"user_id": "user_456"}
]

features = fs.get_online_features(
    entity_rows=entity_rows,
    features=[
        "user_features:age",
        "user_features:total_purchases",
        "user_features:avg_rating"
    ]
).to_dict()

print(features)
# {
#   'user_id': ['user_123', 'user_456'],
#   'age': [25, 32],
#   'total_purchases': [10, 45],
#   'avg_rating': [4.5, 4.8]
# }
```

### Offline Serving (Training)

```python
from feast import FeatureStore
import pandas as pd

fs = FeatureStore(repo_path=".")

# Entity dataframe with timestamps (for point-in-time joins)
entity_df = pd.DataFrame({
    "user_id": ["user_123", "user_456"],
    "event_timestamp": [
        datetime(2024, 1, 15),
        datetime(2024, 1, 16)
    ]
})

# Get historical features (point-in-time correct)
training_df = fs.get_historical_features(
    entity_df=entity_df,
    features=[
        "user_features:age",
        "user_features:total_purchases",
        "user_features:avg_rating"
    ]
).to_df()

print(training_df)
```

## Advanced Features

### 1. Feature Transformations

```python
from feast import FeatureView
from feast.types import Float32, Int64

# On-demand transformations (computed at serving time)
@on_demand_feature_view(
    features=[
        Feature("user_lifetime_value", Float32),
    ],
    inputs={
        "user_features": FeatureView(name="user_features")
    }
)
def user_ltv(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute lifetime value from base features.
    """
    features_df["user_lifetime_value"] = (
        features_df["total_spent"] * 1.2  # Apply business logic
    )
    return features_df
```

### 2. Stream Features (Real-time)

```python
from feast import PushSource, FeatureView

# Define push source for streaming features
user_activity_push_source = PushSource(
    name="user_activity_push_source",
    batch_source=user_activity_file_source  # Fallback
)

# Feature view using streaming source
user_activity_features = FeatureView(
    name="user_activity_features",
    entities=["user_id"],
    ttl=timedelta(minutes=5),  # Short TTL for real-time
    features=[
        Feature(name="clicks_last_5min", dtype=ValueType.INT64),
        Feature(name="pages_viewed", dtype=ValueType.INT64)
    ],
    online=True,
    source=user_activity_push_source
)

# Push real-time updates
fs.push("user_activity_push_source", df)
```

### 3. Feature Validation

```python
from great_expectations.dataset import PandasDataset

def validate_features(df: pd.DataFrame) -> bool:
    """
    Validate feature quality before materialization.
    """
    dataset = PandasDataset(df)
    
    # Check for nulls
    assert dataset.expect_column_values_to_not_be_null("age").success
    
    # Check ranges
    assert dataset.expect_column_values_to_be_between(
        "age", min_value=0, max_value=120
    ).success
    
    # Check distributions
    assert dataset.expect_column_mean_to_be_between(
        "avg_rating", min_value=1.0, max_value=5.0
    ).success
    
    return True
```

## Production Patterns

### 1. Feature Pipeline with Airflow

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def compute_and_materialize_features():
    """
    Compute features and materialize to online store.
    """
    # Compute features
    features = compute_user_features(load_transactions())
    
    # Validate
    validate_features(features)
    
    # Save to offline store
    features.to_parquet('data/user_features.parquet')
    
    # Materialize to online store
    fs = FeatureStore(repo_path=".")
    fs.materialize(
        start_date=datetime.now() - timedelta(hours=1),
        end_date=datetime.now()
    )

dag = DAG(
    'feature_pipeline',
    schedule_interval='@hourly',
    start_date=datetime(2024, 1, 1)
)

compute_task = PythonOperator(
    task_id='compute_features',
    python_callable=compute_and_materialize_features,
    dag=dag
)
```

### 2. FastAPI Feature Serving

```python
from fastapi import FastAPI
from feast import FeatureStore
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()
fs = FeatureStore(repo_path=".")

class FeatureRequest(BaseModel):
    user_ids: List[str]
    features: List[str]

@app.post("/features")
async def get_features(request: FeatureRequest) -> Dict:
    """
    Serve features via REST API.
    """
    entity_rows = [{"user_id": uid} for uid in request.user_ids]
    
    features = fs.get_online_features(
        entity_rows=entity_rows,
        features=request.features
    ).to_dict()
    
    return features

# Usage:
# curl -X POST http://localhost:8000/features \
#   -H "Content-Type: application/json" \
#   -d '{"user_ids": ["user_123"], "features": ["user_features:age"]}'
```

### 3. Feature Monitoring

```python
import logging
from prometheus_client import Counter, Histogram

# Metrics
feature_requests = Counter(
    'feature_requests_total',
    'Total feature requests',
    ['feature_view']
)

feature_latency = Histogram(
    'feature_latency_seconds',
    'Feature retrieval latency',
    ['feature_view']
)

@feature_latency.time()
def get_features_monitored(entity_rows, features):
    """
    Get features with monitoring.
    """
    feature_requests.inc()
    
    try:
        result = fs.get_online_features(entity_rows, features)
        return result
    except Exception as e:
        logging.error(f"Feature retrieval failed: {e}")
        raise
```

## Multi-Cloud Setup

### AWS (S3 + DynamoDB)

```yaml
# feature_store.yaml
project: ml_platform
registry: s3://my-bucket/feast/registry.db
provider: aws

online_store:
  type: dynamodb
  region: us-west-2

offline_store:
  type: file
  path: s3://my-bucket/feast/offline-store/
```

### GCP (BigQuery + Firestore)

```yaml
# feature_store.yaml
project: ml_platform
registry: gs://my-bucket/feast/registry.db
provider: gcp

online_store:
  type: datastore
  project_id: my-gcp-project

offline_store:
  type: bigquery
  project_id: my-gcp-project
  dataset: feast_features
```

## Best Practices

### 1. Feature Naming Convention
```
<entity>_<aggregation>_<window>_<unit>

Examples:
- user_total_purchases_30_days
- product_avg_rating_90_days
- session_click_count_5_minutes
```

### 2. Feature Documentation
```python
user_features = FeatureView(
    name="user_features",
    description="User demographics and behavior features",
    entities=["user_id"],
    features=[
        Feature(
            name="age",
            dtype=ValueType.INT64,
            labels={"pii": "true", "team": "growth"}
        )
    ],
    tags={"version": "v1", "owner": "ml-team"}
)
```

### 3. Feature Versioning
```python
# Version 1
user_features_v1 = FeatureView(name="user_features_v1", ...)

# Version 2 (with breaking changes)
user_features_v2 = FeatureView(name="user_features_v2", ...)

# Gradually migrate models from v1 to v2
```

### 4. Point-in-Time Correctness
```python
# Always use event_timestamp for training
entity_df = pd.DataFrame({
    "user_id": user_ids,
    "event_timestamp": prediction_timestamps  # CRITICAL
})

training_df = fs.get_historical_features(
    entity_df=entity_df,
    features=features
).to_df()
```

## Troubleshooting

### Issue: Features Not Found in Online Store
**Solution:**
1. Check materialization: `feast materialize`
2. Verify TTL hasn't expired
3. Check Redis/DynamoDB connectivity
4. Verify entity keys match exactly

### Issue: Slow Feature Retrieval
**Solution:**
1. Add indexes on entity columns
2. Use Redis instead of DynamoDB for online store
3. Batch feature requests
4. Cache features at application level

### Issue: Training-Serving Skew
**Solution:**
1. Use same feature definitions for training and serving
2. Ensure point-in-time correctness with `event_timestamp`
3. Monitor feature distributions in production
4. Add feature validation pipelines

## Next Steps

1. **Start Simple:** Begin with 5-10 core features
2. **Iterate:** Add features as models improve
3. **Monitor:** Track feature freshness and quality
4. **Document:** Maintain feature catalog and ownership
5. **Govern:** Implement access controls and lineage tracking
