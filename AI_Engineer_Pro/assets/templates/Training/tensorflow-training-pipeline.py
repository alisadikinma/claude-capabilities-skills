# TensorFlow/Keras Training Pipeline

Complete training pipeline with TensorFlow 2.x and Keras best practices.

## Full Training Script

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
import numpy as np
from pathlib import Path
import json
from datetime import datetime

class TrainingConfig:
    """Configuration for training"""
    # Data
    train_data_path = "data/train"
    val_data_path = "data/val"
    num_classes = 10
    image_size = (224, 224)
    
    # Training
    batch_size = 32
    num_epochs = 100
    learning_rate = 1e-3
    
    # Augmentation
    use_augmentation = True
    
    # Checkpointing
    checkpoint_dir = "checkpoints"
    log_dir = "logs"
    
    # Early stopping
    patience = 10
    min_delta = 0.001
    
    # Mixed precision
    use_mixed_precision = True

def create_model(num_classes, image_size=(224, 224)):
    """Create a simple CNN model"""
    inputs = keras.Input(shape=(*image_size, 3))
    
    # Feature extraction
    x = layers.Conv2D(32, 3, activation='relu', padding='same')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)
    
    x = layers.Conv2D(64, 3, activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)
    
    x = layers.Conv2D(128, 3, activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)
    
    # Classification head
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = keras.Model(inputs, outputs)
    return model

def create_transfer_learning_model(num_classes, base_model_name='ResNet50'):
    """Create model using transfer learning"""
    # Load pre-trained base model
    base_models = {
        'ResNet50': keras.applications.ResNet50,
        'MobileNetV2': keras.applications.MobileNetV2,
        'EfficientNetB0': keras.applications.EfficientNetB0,
    }
    
    base_model = base_models[base_model_name](
        include_top=False,
        weights='imagenet',
        input_shape=(224, 224, 3)
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Add custom head
    inputs = keras.Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = keras.Model(inputs, outputs)
    return model

def create_data_pipeline(data_path, config, is_training=True):
    """Create tf.data pipeline for efficient data loading"""
    
    # Load dataset from directory
    dataset = keras.utils.image_dataset_from_directory(
        data_path,
        image_size=config.image_size,
        batch_size=config.batch_size,
        shuffle=is_training,
        label_mode='categorical' if config.num_classes > 2 else 'binary'
    )
    
    # Data augmentation (only for training)
    if is_training and config.use_augmentation:
        data_augmentation = keras.Sequential([
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.2),
            layers.RandomZoom(0.2),
            layers.RandomContrast(0.2),
        ])
        dataset = dataset.map(
            lambda x, y: (data_augmentation(x, training=True), y),
            num_parallel_calls=tf.data.AUTOTUNE
        )
    
    # Normalization
    normalization = layers.Rescaling(1./255)
    dataset = dataset.map(
        lambda x, y: (normalization(x), y),
        num_parallel_calls=tf.data.AUTOTUNE
    )
    
    # Performance optimization
    dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    
    return dataset

class CustomCallback(callbacks.Callback):
    """Custom callback for additional logging"""
    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        print(f"\n📊 Epoch {epoch + 1} Summary:")
        print(f"   Train Loss: {logs.get('loss', 0):.4f} | Train Acc: {logs.get('accuracy', 0) * 100:.2f}%")
        print(f"   Val Loss: {logs.get('val_loss', 0):.4f} | Val Acc: {logs.get('val_accuracy', 0) * 100:.2f}%")

def train_model(config):
    """Main training function"""
    
    # Enable mixed precision
    if config.use_mixed_precision:
        policy = tf.keras.mixed_precision.Policy('mixed_float16')
        tf.keras.mixed_precision.set_global_policy(policy)
        print("✅ Mixed precision enabled")
    
    # Create directories
    Path(config.checkpoint_dir).mkdir(parents=True, exist_ok=True)
    Path(config.log_dir).mkdir(parents=True, exist_ok=True)
    
    # Load data
    print("📂 Loading datasets...")
    train_dataset = create_data_pipeline(config.train_data_path, config, is_training=True)
    val_dataset = create_data_pipeline(config.val_data_path, config, is_training=False)
    
    # Create model
    print("🏗️ Building model...")
    model = create_model(config.num_classes, config.image_size)
    # Or use transfer learning:
    # model = create_transfer_learning_model(config.num_classes, 'ResNet50')
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=config.learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=5, name='top_5_accuracy')]
    )
    
    # Model summary
    model.summary()
    
    # Callbacks
    callback_list = [
        # Model checkpointing
        callbacks.ModelCheckpoint(
            filepath=f"{config.checkpoint_dir}/best_model.h5",
            monitor='val_loss',
            save_best_only=True,
            save_weights_only=False,
            verbose=1
        ),
        
        # Save weights separately
        callbacks.ModelCheckpoint(
            filepath=f"{config.checkpoint_dir}/weights_epoch_{{epoch:02d}}_val_loss_{{val_loss:.4f}}.h5",
            monitor='val_loss',
            save_best_only=False,
            save_weights_only=True,
            save_freq='epoch'
        ),
        
        # Early stopping
        callbacks.EarlyStopping(
            monitor='val_loss',
            patience=config.patience,
            min_delta=config.min_delta,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Learning rate scheduling
        callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        
        # TensorBoard
        callbacks.TensorBoard(
            log_dir=f"{config.log_dir}/{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            histogram_freq=1,
            write_graph=True,
            update_freq='epoch'
        ),
        
        # CSV Logger
        callbacks.CSVLogger(
            f"{config.log_dir}/training_log.csv",
            separator=',',
            append=False
        ),
        
        # Custom callback
        CustomCallback()
    ]
    
    # Train model
    print("\n🚀 Starting training...")
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=config.num_epochs,
        callbacks=callback_list,
        verbose=1
    )
    
    # Save final model
    model.save(f"{config.checkpoint_dir}/final_model.h5")
    
    # Save training history
    with open(f"{config.log_dir}/history.json", 'w') as f:
        json.dump(history.history, f, indent=2)
    
    print("\n✅ Training completed!")
    return model, history

def evaluate_model(model, test_data_path, config):
    """Evaluate model on test set"""
    print("\n📊 Evaluating model...")
    
    test_dataset = create_data_pipeline(test_data_path, config, is_training=False)
    
    results = model.evaluate(test_dataset, verbose=1)
    print(f"\n✅ Test Loss: {results[0]:.4f}")
    print(f"✅ Test Accuracy: {results[1] * 100:.2f}%")
    
    return results

# Example usage
if __name__ == "__main__":
    # Initialize config
    config = TrainingConfig()
    
    # Train model
    model, history = train_model(config)
    
    # Evaluate on test set (optional)
    # evaluate_model(model, "data/test", config)
    
    # Load saved model
    # loaded_model = keras.models.load_model("checkpoints/best_model.h5")
```

## Fine-tuning Pre-trained Model

```python
def fine_tune_model(model, train_dataset, val_dataset, config):
    """Fine-tune a pre-trained model"""
    
    # Unfreeze base model layers
    model.layers[1].trainable = True  # Assuming base_model is at index 1
    
    # Freeze early layers, train later layers
    for layer in model.layers[1].layers[:-30]:  # Freeze all except last 30 layers
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-5),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=20,
        callbacks=[
            callbacks.EarlyStopping(patience=5, restore_best_weights=True),
            callbacks.ReduceLROnPlateau(patience=3, factor=0.5)
        ]
    )
    
    return model, history
```

## Convert to TensorFlow Lite

```python
def convert_to_tflite(model, output_path="model.tflite"):
    """Convert Keras model to TFLite for edge deployment"""
    
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Optimization options
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    # For INT8 quantization (requires representative dataset)
    # converter.representative_dataset = representative_data_gen
    # converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    
    tflite_model = converter.convert()
    
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"✅ TFLite model saved to {output_path}")
```

## Distributed Training Strategy

```python
# Multi-GPU training
strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    model = create_model(config.num_classes, config.image_size)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=config.learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

# Train as usual
model.fit(train_dataset, validation_data=val_dataset, epochs=config.num_epochs)
```

## Key Features

- ✅ Mixed precision training
- ✅ Data augmentation pipeline
- ✅ Transfer learning support
- ✅ Multiple callbacks (checkpointing, early stopping, LR scheduling)
- ✅ TensorBoard logging
- ✅ TFLite conversion for edge deployment
- ✅ Multi-GPU support
