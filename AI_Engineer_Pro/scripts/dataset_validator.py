"""
Dataset Validator
Validate training datasets for quality and consistency
"""

import os
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image
import json

class DatasetValidator:
    """Validate image classification/detection datasets"""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.issues = []
    
    def validate_structure(self, expected_splits=['train', 'val', 'test']):
        """Check if dataset has expected folder structure"""
        print("✓ Validating structure...")
        
        for split in expected_splits:
            split_path = self.dataset_path / split
            if not split_path.exists():
                self.issues.append(f"Missing split: {split}")
        
        return len(self.issues) == 0
    
    def validate_images(self, splits=['train', 'val']):
        """Validate image files"""
        print("✓ Validating images...")
        
        stats = {}
        
        for split in splits:
            split_path = self.dataset_path / split
            if not split_path.exists():
                continue
            
            image_files = list(split_path.rglob('*.jpg')) + list(split_path.rglob('*.png'))
            
            sizes = []
            corrupted = []
            
            for img_path in image_files:
                try:
                    img = Image.open(img_path)
                    sizes.append(img.size)
                    img.verify()  # Check for corruption
                except Exception as e:
                    corrupted.append(str(img_path))
            
            if corrupted:
                self.issues.append(f"{split}: {len(corrupted)} corrupted images")
            
            # Check size consistency
            if sizes:
                unique_sizes = set(sizes)
                if len(unique_sizes) > 1:
                    size_counts = Counter(sizes)
                    print(f"  {split}: Multiple image sizes found: {dict(size_counts)}")
            
            stats[split] = {
                'total_images': len(image_files),
                'corrupted': len(corrupted),
                'unique_sizes': len(unique_sizes),
                'most_common_size': Counter(sizes).most_common(1)[0] if sizes else None
            }
        
        return stats
    
    def validate_class_distribution(self, splits=['train', 'val']):
        """Check class balance"""
        print("✓ Validating class distribution...")
        
        distribution = {}
        
        for split in splits:
            split_path = self.dataset_path / split
            if not split_path.exists():
                continue
            
            class_counts = {}
            
            # For classification dataset (class folders)
            for class_folder in split_path.iterdir():
                if class_folder.is_dir():
                    class_name = class_folder.name
                    num_samples = len(list(class_folder.glob('*.jpg')) + list(class_folder.glob('*.png')))
                    class_counts[class_name] = num_samples
            
            if class_counts:
                total = sum(class_counts.values())
                min_class = min(class_counts.items(), key=lambda x: x[1])
                max_class = max(class_counts.items(), key=lambda x: x[1])
                
                imbalance_ratio = max_class[1] / min_class[1] if min_class[1] > 0 else float('inf')
                
                if imbalance_ratio > 3:
                    self.issues.append(
                        f"{split}: Class imbalance detected. "
                        f"{max_class[0]}={max_class[1]} vs {min_class[0]}={min_class[1]} "
                        f"(ratio: {imbalance_ratio:.2f})"
                    )
                
                distribution[split] = {
                    'classes': class_counts,
                    'total': total,
                    'num_classes': len(class_counts),
                    'min_samples': min_class[1],
                    'max_samples': max_class[1],
                    'imbalance_ratio': imbalance_ratio
                }
        
        return distribution
    
    def validate_split_sizes(self, min_train=100, min_val=20):
        """Check if splits have minimum samples"""
        print("✓ Validating split sizes...")
        
        for split, min_size in [('train', min_train), ('val', min_val)]:
            split_path = self.dataset_path / split
            if split_path.exists():
                num_images = len(list(split_path.rglob('*.jpg')) + list(split_path.rglob('*.png')))
                
                if num_images < min_size:
                    self.issues.append(f"{split}: Only {num_images} images (minimum: {min_size})")
        
        return len(self.issues) == 0
    
    def validate_labels(self, label_format='yolo'):
        """Validate label files for object detection"""
        print("✓ Validating labels...")
        
        if label_format == 'yolo':
            return self._validate_yolo_labels()
        
        return True
    
    def _validate_yolo_labels(self):
        """Validate YOLO format labels"""
        labels_path = self.dataset_path / 'labels' / 'train'
        
        if not labels_path.exists():
            self.issues.append("YOLO labels folder not found")
            return False
        
        label_files = list(labels_path.glob('*.txt'))
        
        for label_file in label_files:
            with open(label_file, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                parts = line.strip().split()
                
                if len(parts) != 5:
                    self.issues.append(
                        f"{label_file.name} line {i+1}: Expected 5 values, got {len(parts)}"
                    )
                    continue
                
                try:
                    class_id, x, y, w, h = map(float, parts)
                    
                    # Check if coordinates are normalized (0-1)
                    if not all(0 <= val <= 1 for val in [x, y, w, h]):
                        self.issues.append(
                            f"{label_file.name} line {i+1}: Coordinates not normalized"
                        )
                except ValueError:
                    self.issues.append(
                        f"{label_file.name} line {i+1}: Invalid values"
                    )
        
        return len(self.issues) == 0
    
    def generate_report(self):
        """Generate validation report"""
        print("\\n" + "="*50)
        print("DATASET VALIDATION REPORT")
        print("="*50)
        
        if not self.issues:
            print("✅ No issues found!")
        else:
            print(f"⚠️  Found {len(self.issues)} issues:\\n")
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue}")
        
        print("="*50)
        
        return len(self.issues) == 0

# Usage example
if __name__ == "__main__":
    validator = DatasetValidator('data/pcb_dataset')
    
    # Run validations
    validator.validate_structure()
    image_stats = validator.validate_images()
    class_dist = validator.validate_class_distribution()
    validator.validate_split_sizes(min_train=500, min_val=100)
    
    # Print statistics
    print("\\n=== Image Statistics ===")
    print(json.dumps(image_stats, indent=2))
    
    print("\\n=== Class Distribution ===")
    print(json.dumps(class_dist, indent=2))
    
    # Generate final report
    validator.generate_report()
