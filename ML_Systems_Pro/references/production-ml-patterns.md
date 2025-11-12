# Production ML Patterns and Anti-Patterns

Battle-tested patterns for deploying and maintaining ML systems in production.

## Architecture Patterns

### Pattern 1: Prediction Service with Fallback

**Problem:** ML model fails or is slow
**Solution:** Graceful degradation with fallback

```python
class PredictionService:
    def __init__(self, primary_model, fallback_model=None):
        self.primary = primary_model
        self.fallback = fallback_model or SimpleHeuristic()
        self.timeout = 100  # ms
    
    def predict(self, features):
        try:
            # Try primary model with timeout
            result = self.primary.predict(features, timeout=self.timeout)
            return result, "primary"
        except TimeoutError:
            logger.warning("Primary model timeout, using fallback")
            return self.fallback.predict(features), "fallback"
        except Exception as e:
            logger.error(f"Primary model failed: {e}")
            return self.fallback.predict(features), "fallback"
```

**Benefits:**
- Always returns a result
- Monitors fallback usage rate
- Simple heuristics often 80% as good

### Pattern 2: Shadow Deployment

**Problem:** Test new model without affecting users
**Solution:** Run new model alongside old, log both

```python
class ShadowDeployment:
    def __init__(self, prod_model, shadow_model):
        self.prod = prod_model
        self.shadow = shadow_model
        self.shadow_enabled = True
    
    def predict(self, features):
        # Production prediction
        prod_result = self.prod.predict(features)
        
        # Shadow prediction (async)
        if self.shadow_enabled:
            threading.Thread(
                target=self._shadow_predict,
                args=(features, prod_result)
            ).start()
        
        return prod_result
    
    def _shadow_predict(self, features, prod_result):
        try:
            shadow_result = self.shadow.predict(features)
            
            # Log for analysis
            log_comparison(
                prod=prod_result,
                shadow=shadow_result,
                features=features
            )
        except Exception as e:
            logger.error(f"Shadow prediction failed: {e}")
```

**Benefits:**
- Zero risk to production
- Real-world performance data
- Catch edge cases before rollout

### Pattern 3: Model Ensemble with Voting

**Problem:** Single model has biases/weaknesses
**Solution:** Combine multiple models

```python
class ModelEnsemble:
    def __init__(self, models, weights=None):
        self.models = models
        self.weights = weights or [1.0 / len(models)] * len(models)
    
    def predict(self, features):
        predictions = []
        
        for model, weight in zip(self.models, self.weights):
            pred = model.predict(features)
            predictions.append(pred * weight)
        
        # Weighted average
        return sum(predictions) / sum(self.weights)
```

**Voting Strategies:**
- **Soft voting:** Average probabilities
- **Hard voting:** Majority class
- **Stacking:** Meta-model on predictions

### Pattern 4: Feature Store Integration

**Problem:** Training-serving skew
**Solution:** Centralized feature engineering

```python
from feast import FeatureStore

class FeatureStoreModel:
    def __init__(self, model, feature_store):
        self.model = model
        self.fs = feature_store
    
    def predict(self, entity_id):
        # Get features from store (same as training)
        features = self.fs.get_online_features(
            entity_rows=[{"user_id": entity_id}],
            features=["user_features:age", "user_features:total_purchases"]
        ).to_dict()
        
        # Predict
        return self.model.predict(features)
```

**Benefits:**
- No feature drift
- Reusable features
- Point-in-time correctness

### Pattern 5: Batch Prediction with Caching

**Problem:** Real-time predictions too expensive
**Solution:** Pre-compute and cache

```python
class BatchPredictionCache:
    def __init__(self, model, cache_ttl=3600):
        self.model = model
        self.cache = redis.Redis()
        self.cache_ttl = cache_ttl
    
    def predict(self, item_id):
        # Check cache
        cache_key = f"pred:{item_id}"
        cached = self.cache.get(cache_key)
        
        if cached:
            return pickle.loads(cached)
        
        # Predict and cache
        prediction = self.model.predict(item_id)
        self.cache.setex(cache_key, self.cache_ttl, pickle.dumps(prediction))
        
        return prediction
    
    def batch_refresh(self, item_ids):
        """Refresh cache for popular items."""
        predictions = self.model.predict_batch(item_ids)
        
        for item_id, pred in zip(item_ids, predictions):
            cache_key = f"pred:{item_id}"
            self.cache.setex(cache_key, self.cache_ttl, pickle.dumps(pred))
```

## Data Patterns

### Pattern 6: Online Learning with Delayed Feedback

**Problem:** Ground truth arrives hours/days later
**Solution:** Buffer predictions, update when labels arrive

```python
class OnlineLearner:
    def __init__(self, model):
        self.model = model
        self.buffer = deque(maxlen=10000)
    
    def predict(self, features):
        prediction = self.model.predict(features)
        
        # Store for future learning
        self.buffer.append({
            'timestamp': datetime.now(),
            'features': features,
            'prediction': prediction,
            'ground_truth': None
        })
        
        return prediction
    
    def update_ground_truth(self, prediction_id, label):
        """Called when true label becomes available."""
        for item in self.buffer:
            if item['prediction_id'] == prediction_id:
                item['ground_truth'] = label
                break
        
        # Retrain when enough labeled data
        if self._should_retrain():
            self._retrain()
    
    def _retrain(self):
        labeled_data = [
            (item['features'], item['ground_truth'])
            for item in self.buffer
            if item['ground_truth'] is not None
        ]
        
        X, y = zip(*labeled_data)
        self.model.partial_fit(X, y)
```

### Pattern 7: Data Versioning

**Problem:** Can't reproduce old model
**Solution:** Version everything (data, code, config)

```python
import dvc.api
import mlflow

class VersionedPipeline:
    def __init__(self, data_version, code_version):
        self.data_version = data_version
        self.code_version = code_version
    
    def load_data(self):
        # Load specific data version
        with dvc.api.open(
            'data/training.parquet',
            rev=self.data_version
        ) as f:
            return pd.read_parquet(f)
    
    def train(self):
        with mlflow.start_run():
            # Log versions
            mlflow.log_param("data_version", self.data_version)
            mlflow.log_param("code_version", self.code_version)
            
            # Train
            data = self.load_data()
            model = train_model(data)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            return model
```

### Pattern 8: Synthetic Data Augmentation

**Problem:** Limited training data
**Solution:** Generate synthetic examples

```python
class DataAugmenter:
    def augment_text(self, text):
        """Text augmentation strategies."""
        strategies = [
            self.synonym_replacement,
            self.back_translation,
            self.random_deletion,
            self.random_swap
        ]
        
        augmented = []
        for strategy in strategies:
            augmented.append(strategy(text))
        
        return augmented
    
    def augment_image(self, image):
        """Image augmentation strategies."""
        return [
            self.random_crop(image),
            self.color_jitter(image),
            self.horizontal_flip(image),
            self.rotation(image)
        ]
```

## Monitoring Patterns

### Pattern 9: Multi-Level Monitoring

**Problem:** Don't know why model fails
**Solution:** Monitor at all levels

```python
class MLMonitoring:
    def __init__(self):
        # System metrics
        self.cpu_usage = Gauge('model_cpu_usage')
        self.memory_usage = Gauge('model_memory_mb')
        
        # Model metrics
        self.prediction_latency = Histogram('prediction_latency_ms')
        self.prediction_count = Counter('predictions_total')
        
        # Data metrics
        self.input_drift = Gauge('input_feature_drift', ['feature'])
        self.output_distribution = Histogram('prediction_distribution')
        
        # Business metrics
        self.conversion_rate = Gauge('conversion_rate')
        self.revenue_impact = Counter('revenue_attributed_dollars')
    
    @self.prediction_latency.time()
    def predict(self, features):
        # Increment counter
        self.prediction_count.inc()
        
        # Check input drift
        self._check_drift(features)
        
        # Predict
        result = self.model.predict(features)
        
        # Track output
        self.output_distribution.observe(result)
        
        return result
```

**Monitor Stack:**
1. **Infrastructure:** CPU, memory, disk
2. **Application:** Latency, throughput, errors
3. **Model:** Accuracy, drift, confidence
4. **Business:** Revenue, conversions, engagement

### Pattern 10: Automated Alerting

**Problem:** Model degrades silently
**Solution:** Proactive alerts with thresholds

```python
class AutomatedAlerting:
    def __init__(self):
        self.thresholds = {
            'accuracy': 0.85,
            'latency_p99': 200,  # ms
            'error_rate': 0.05,
            'drift_score': 0.1
        }
    
    def check_metrics(self, metrics):
        alerts = []
        
        # Check accuracy
        if metrics['accuracy'] < self.thresholds['accuracy']:
            alerts.append({
                'severity': 'high',
                'metric': 'accuracy',
                'value': metrics['accuracy'],
                'threshold': self.thresholds['accuracy']
            })
        
        # Check latency
        if metrics['latency_p99'] > self.thresholds['latency_p99']:
            alerts.append({
                'severity': 'medium',
                'metric': 'latency_p99',
                'value': metrics['latency_p99'],
                'threshold': self.thresholds['latency_p99']
            })
        
        # Send alerts
        for alert in alerts:
            self.send_alert(alert)
    
    def send_alert(self, alert):
        if alert['severity'] == 'high':
            send_pagerduty(alert)
        else:
            send_slack(alert)
```

## Testing Patterns

### Pattern 11: Property-Based Testing

**Problem:** Can't test all edge cases
**Solution:** Test invariants with random inputs

```python
from hypothesis import given, strategies as st

class ModelTests:
    @given(st.floats(min_value=0, max_value=1))
    def test_prediction_range(self, input_value):
        """Predictions should be between 0 and 1."""
        pred = self.model.predict([[input_value]])
        assert 0 <= pred <= 1
    
    @given(st.lists(st.floats(), min_size=10, max_size=10))
    def test_prediction_consistency(self, features):
        """Same input should give same output."""
        pred1 = self.model.predict([features])
        pred2 = self.model.predict([features])
        assert pred1 == pred2
```

### Pattern 12: Metamorphic Testing

**Problem:** Don't have ground truth
**Solution:** Test relations between inputs/outputs

```python
def test_translation_invariance(self, model):
    """Model should be invariant to language translation."""
    text_en = "I love this product"
    text_es = translate(text_en, target_lang="es")
    
    pred_en = model.predict(text_en)
    pred_es = model.predict(text_es)
    
    # Predictions should be similar
    assert abs(pred_en - pred_es) < 0.1

def test_monotonicity(self, model):
    """Higher price should decrease purchase probability."""
    base_features = {'price': 100, 'rating': 4.5}
    high_price = {'price': 200, 'rating': 4.5}
    
    pred_base = model.predict(base_features)
    pred_high = model.predict(high_price)
    
    assert pred_high < pred_base
```

## Anti-Patterns

### Anti-Pattern 1: No Baseline

**Problem:** Can't tell if ML model is better than simple rule
**Solution:** Always compare against baseline

```python
# BAD: Deploy ML model without baseline
accuracy = 0.87  # Is this good?

# GOOD: Compare against simple baseline
baseline_accuracy = always_predict_majority_class()  # 0.60
ml_accuracy = 0.87  # 27% improvement!
```

### Anti-Pattern 2: Training-Serving Skew

**Problem:** Different preprocessing in training vs serving
**Solution:** Reuse exact same code

```python
# BAD: Duplicate preprocessing logic
def preprocess_training(data):
    return data.fillna(0).apply(lambda x: x / x.max())

def preprocess_serving(data):
    return data.fillna(0) / data.max()  # DIFFERENT!

# GOOD: Single preprocessing function
def preprocess(data):
    return data.fillna(0).apply(lambda x: x / x.max())

# Use in both training and serving
preprocessor = pickle.load('preprocessor.pkl')
```

### Anti-Pattern 3: Ignoring Data Drift

**Problem:** Model degrades over time
**Solution:** Monitor input distributions

```python
# BAD: Set and forget
model.deploy()

# GOOD: Monitor and retrain
monitor = DataDriftMonitor(reference_data=training_data)

for batch in production_data:
    drift_score = monitor.check_drift(batch)
    
    if drift_score > threshold:
        retrain_model(recent_data)
```

### Anti-Pattern 4: Overfitting to Validation Set

**Problem:** Tuning hyperparameters on validation = leakage
**Solution:** Separate validation and test sets

```python
# BAD: Tune on validation, report validation accuracy
best_model = tune_hyperparameters(train, validation)
print(f"Accuracy: {best_model.score(validation)}")  # WRONG!

# GOOD: Tune on validation, report test accuracy
best_model = tune_hyperparameters(train, validation)
print(f"Accuracy: {best_model.score(test)}")  # Honest
```

### Anti-Pattern 5: Not Logging Predictions

**Problem:** Can't debug failures
**Solution:** Log everything

```python
# BAD: Just return prediction
return model.predict(features)

# GOOD: Log prediction with context
prediction = model.predict(features)

log_prediction(
    timestamp=datetime.now(),
    user_id=user_id,
    features=features,
    prediction=prediction,
    model_version="v1.2.3"
)

return prediction
```

### Anti-Pattern 6: Premature Optimization

**Problem:** Complex distributed system for small model
**Solution:** Start simple, scale when needed

```python
# BAD: Kubernetes + Kafka + Redis for 10 QPS
deploy_on_kubernetes_cluster()

# GOOD: Single EC2 instance with Flask
@app.route('/predict')
def predict():
    return model.predict(request.json)

# Scale only when needed (>100 QPS)
```

## Production Checklist

**Before Deployment:**
- [ ] Baseline comparison shows improvement
- [ ] Model tested on held-out test set
- [ ] Training-serving preprocessing is identical
- [ ] Fallback strategy implemented
- [ ] Monitoring and alerting configured
- [ ] A/B test plan ready
- [ ] Rollback procedure documented

**After Deployment:**
- [ ] Monitor accuracy daily
- [ ] Check for data drift weekly
- [ ] Review false positives/negatives
- [ ] Retrain monthly (or when drift detected)
- [ ] Update documentation
- [ ] Analyze business impact

## Key Principles

1. **Start Simple:** Deploy a baseline before ML
2. **Monitor Everything:** Metrics at all levels
3. **Test Continuously:** CI/CD for ML
4. **Version Everything:** Data, code, models
5. **Fail Gracefully:** Always have a fallback
6. **Iterate Fast:** A/B test, learn, improve
7. **Maintain Reproducibility:** Pin versions, save artifacts
8. **Document Decisions:** Why this model, threshold, approach

## Further Reading

- *Building Machine Learning Powered Applications* (Emmanuel Ameisen)
- *Designing Machine Learning Systems* (Chip Huyen)
- *Reliable Machine Learning* (Cathy Chen, Niall Murphy, Google)
