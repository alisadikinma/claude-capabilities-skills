# Training Checklist

## Pre-Training

- [ ] Dataset prepared and validated
  - [ ] Minimum 1000 samples per class
  - [ ] Classes balanced or augmented
  - [ ] Train/val/test split (70/15/15)
  - [ ] No data leakage between splits
- [ ] Data augmentation configured
- [ ] Model architecture selected
- [ ] Baseline performance established
- [ ] Hyperparameters defined
- [ ] Logging/tracking setup (MLflow/W&B)
- [ ] GPU available and tested

## During Training

- [ ] Monitor training loss (decreasing)
- [ ] Monitor validation loss (not increasing)
- [ ] Check for overfitting (train vs val gap)
- [ ] Learning rate appropriate (not too high/low)
- [ ] Batch size reasonable for GPU memory
- [ ] Checkpoints saving correctly
- [ ] Early stopping configured (patience=10-20)

## Post-Training

- [ ] Best model saved
- [ ] Evaluation on test set complete
- [ ] Per-class metrics reviewed
- [ ] Confusion matrix analyzed
- [ ] Model exported (ONNX/TorchScript)
- [ ] Training artifacts logged
- [ ] Results documented
