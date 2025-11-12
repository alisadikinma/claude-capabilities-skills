# PyTorch Training Pipeline

Complete end-to-end training pipeline with best practices for production ML.

## Full Training Script

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torch.cuda.amp import autocast, GradScaler
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import os
from pathlib import Path

class CustomDataset(Dataset):
    """Template dataset - replace with your data loading logic"""
    def __init__(self, data_path, transform=None):
        self.data_path = data_path
        self.transform = transform
        # Load your data here
        self.samples = []  # [(image, label), ...]
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        image, label = self.samples[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

class TrainingConfig:
    """Configuration for training"""
    # Data
    train_data_path = "data/train"
    val_data_path = "data/val"
    num_classes = 10
    
    # Training
    batch_size = 32
    num_epochs = 100
    learning_rate = 1e-3
    weight_decay = 1e-4
    
    # Hardware
    device = "cuda" if torch.cuda.is_available() else "cpu"
    num_workers = 4
    pin_memory = True
    
    # Optimization
    use_mixed_precision = True
    gradient_clip_val = 1.0
    
    # Checkpointing
    checkpoint_dir = "checkpoints"
    save_frequency = 5  # Save every N epochs
    
    # Early stopping
    patience = 10
    min_delta = 0.001

class Trainer:
    def __init__(self, model, config, train_loader, val_loader):
        self.model = model.to(config.device)
        self.config = config
        self.train_loader = train_loader
        self.val_loader = val_loader
        
        # Loss and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.AdamW(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer,
            T_max=config.num_epochs
        )
        
        # Mixed precision training
        self.scaler = GradScaler() if config.use_mixed_precision else None
        
        # Tensorboard
        self.writer = SummaryWriter(log_dir="runs/experiment")
        
        # Checkpointing
        Path(config.checkpoint_dir).mkdir(parents=True, exist_ok=True)
        
        # Early stopping
        self.best_val_loss = float('inf')
        self.patience_counter = 0
    
    def train_epoch(self, epoch):
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        pbar = tqdm(self.train_loader, desc=f"Epoch {epoch}")
        for batch_idx, (images, labels) in enumerate(pbar):
            images = images.to(self.config.device)
            labels = labels.to(self.config.device)
            
            self.optimizer.zero_grad()
            
            # Mixed precision training
            if self.scaler:
                with autocast():
                    outputs = self.model(images)
                    loss = self.criterion(outputs, labels)
                
                self.scaler.scale(loss).backward()
                
                # Gradient clipping
                if self.config.gradient_clip_val > 0:
                    self.scaler.unscale_(self.optimizer)
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(),
                        self.config.gradient_clip_val
                    )
                
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                
                if self.config.gradient_clip_val > 0:
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(),
                        self.config.gradient_clip_val
                    )
                
                self.optimizer.step()
            
            # Metrics
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            # Update progress bar
            pbar.set_postfix({
                'loss': total_loss / (batch_idx + 1),
                'acc': 100. * correct / total
            })
        
        avg_loss = total_loss / len(self.train_loader)
        accuracy = 100. * correct / total
        
        return avg_loss, accuracy
    
    def validate(self, epoch):
        """Validate the model"""
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in tqdm(self.val_loader, desc="Validation"):
                images = images.to(self.config.device)
                labels = labels.to(self.config.device)
                
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                
                total_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
        
        avg_loss = total_loss / len(self.val_loader)
        accuracy = 100. * correct / total
        
        return avg_loss, accuracy
    
    def save_checkpoint(self, epoch, val_loss, is_best=False):
        """Save model checkpoint"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'val_loss': val_loss,
            'config': self.config
        }
        
        if self.scaler:
            checkpoint['scaler_state_dict'] = self.scaler.state_dict()
        
        # Save regular checkpoint
        checkpoint_path = os.path.join(
            self.config.checkpoint_dir,
            f'checkpoint_epoch_{epoch}.pth'
        )
        torch.save(checkpoint, checkpoint_path)
        
        # Save best model
        if is_best:
            best_path = os.path.join(self.config.checkpoint_dir, 'best_model.pth')
            torch.save(checkpoint, best_path)
            print(f"💾 Saved best model with val_loss: {val_loss:.4f}")
    
    def train(self):
        """Main training loop"""
        print(f"🚀 Starting training on {self.config.device}")
        print(f"📊 Train samples: {len(self.train_loader.dataset)}")
        print(f"📊 Val samples: {len(self.val_loader.dataset)}")
        
        for epoch in range(1, self.config.num_epochs + 1):
            # Train
            train_loss, train_acc = self.train_epoch(epoch)
            
            # Validate
            val_loss, val_acc = self.validate(epoch)
            
            # Learning rate step
            self.scheduler.step()
            current_lr = self.scheduler.get_last_lr()[0]
            
            # Log to tensorboard
            self.writer.add_scalar('Loss/train', train_loss, epoch)
            self.writer.add_scalar('Loss/val', val_loss, epoch)
            self.writer.add_scalar('Accuracy/train', train_acc, epoch)
            self.writer.add_scalar('Accuracy/val', val_acc, epoch)
            self.writer.add_scalar('Learning_Rate', current_lr, epoch)
            
            # Print summary
            print(f"\n📈 Epoch {epoch}/{self.config.num_epochs}")
            print(f"   Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
            print(f"   Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
            print(f"   LR: {current_lr:.6f}")
            
            # Save checkpoint
            is_best = val_loss < self.best_val_loss
            if epoch % self.config.save_frequency == 0 or is_best:
                self.save_checkpoint(epoch, val_loss, is_best)
            
            # Early stopping
            if val_loss < self.best_val_loss - self.config.min_delta:
                self.best_val_loss = val_loss
                self.patience_counter = 0
            else:
                self.patience_counter += 1
                
                if self.patience_counter >= self.config.patience:
                    print(f"\n⚠️ Early stopping triggered after {epoch} epochs")
                    break
        
        self.writer.close()
        print("\n✅ Training completed!")

# Example usage
if __name__ == "__main__":
    # Initialize config
    config = TrainingConfig()
    
    # Create datasets and dataloaders
    train_dataset = CustomDataset(config.train_data_path)
    val_dataset = CustomDataset(config.val_data_path)
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=config.num_workers,
        pin_memory=config.pin_memory
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=config.num_workers,
        pin_memory=config.pin_memory
    )
    
    # Initialize model (replace with your architecture)
    from torchvision.models import resnet50
    model = resnet50(num_classes=config.num_classes)
    
    # Train
    trainer = Trainer(model, config, train_loader, val_loader)
    trainer.train()
```

## Key Features

- ✅ Mixed precision training (FP16)
- ✅ Gradient clipping
- ✅ Learning rate scheduling
- ✅ Checkpointing with best model tracking
- ✅ Early stopping
- ✅ Tensorboard logging
- ✅ Progress bars with tqdm

## Load Checkpoint

```python
def load_checkpoint(checkpoint_path, model, optimizer=None, scheduler=None):
    checkpoint = torch.load(checkpoint_path)
    
    model.load_state_dict(checkpoint['model_state_dict'])
    
    if optimizer:
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    
    if scheduler:
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
    
    return checkpoint['epoch'], checkpoint['val_loss']
```

## Distributed Training (Multi-GPU)

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup_distributed():
    dist.init_process_group(backend='nccl')
    local_rank = int(os.environ['LOCAL_RANK'])
    torch.cuda.set_device(local_rank)
    return local_rank

# In training script
local_rank = setup_distributed()
model = model.to(local_rank)
model = DDP(model, device_ids=[local_rank])

# Run with: torchrun --nproc_per_node=2 train.py
```
