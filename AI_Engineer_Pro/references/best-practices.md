# AI/ML Best Practices

## Model Development

**Data Quality**
- Aim for 1000+ samples per class minimum
- Balance class distribution (use augmentation/SMOTE)
- Split: 70% train, 15% val, 15% test
- Keep test set pristine (never train on it)

**Training**
- Start with pre-trained models (transfer learning)
- Use learning rate warmup (500-1000 steps)
- Monitor validation loss (early stopping patience=10-20)
- Save checkpoints every 5-10 epochs
- Use mixed precision (FP16) for 2x speedup

**Hyperparameters**
- Learning rate: 1e-5 to 1e-3 (fine-tuning: 1e-5 to 1e-4)
- Batch size: As large as GPU allows (16-64 typical)
- Epochs: 50-200 (with early stopping)
- Weight decay: 1e-4 to 1e-2 for regularization

## Evaluation

**Metrics**
- Classification: Accuracy, F1, Precision, Recall
- Detection: mAP, IoU, Precision-Recall curve
- Always use class-specific metrics (per-class F1)

**Validation Strategy**
- K-fold cross-validation for small datasets
- Stratified split to maintain class distribution
- Time-based split for production data

## Production

**Model Serving**
- Use ONNX or TorchScript for deployment
- Implement health checks and monitoring
- Version models (v1, v2, etc.)
- A/B test new models before full rollout

**Performance**
- Target <100ms latency for real-time
- Batch requests when possible (2-4x throughput)
- Use GPU for inference when available
- Cache frequent predictions

**Monitoring**
- Track inference latency (p50, p95, p99)
- Monitor prediction confidence distribution
- Alert on data drift (input distribution change)
- Log prediction errors for retraining

## Security

- Validate all inputs (size, format, content)
- Rate limit API endpoints
- Don't expose raw model outputs (filter sensitive info)
- Use authentication for production APIs

## Reproducibility

- Set random seeds (Python, NumPy, PyTorch)
- Version datasets (DVC, Git LFS)
- Log all hyperparameters (MLflow, W&B)
- Document data preprocessing steps
