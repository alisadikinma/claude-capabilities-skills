"""
Production Model Monitoring System
==================================

Comprehensive monitoring for ML models in production including drift detection,
performance tracking, and automated alerting.

Use Cases:
- Detect model degradation
- Track data drift
- Monitor prediction quality
- Alert on anomalies

Requirements:
    pip install pandas numpy scikit-learn scipy prometheus-client evidently
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from scipy.stats import ks_2samp
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from prometheus_client import Counter, Histogram, Gauge
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MonitoringConfig:
    """Configuration for model monitoring."""
    drift_threshold: float = 0.05  # p-value for KS test
    performance_threshold: float = 0.05  # Max acceptable drop
    window_size: int = 1000  # Predictions to accumulate before check
    alert_email: str = "ml-team@company.com"
    

class ModelMonitor:
    """
    Production model monitoring system.
    
    Features:
    - Data drift detection (KS test, PSI)
    - Performance monitoring
    - Prediction distribution tracking
    - Automated alerting
    """
    
    def __init__(self, config: MonitoringConfig = None):
        """
        Initialize model monitor.
        
        Args:
            config: MonitoringConfig instance
        """
        self.config = config or MonitoringConfig()
        
        # Storage for predictions and features
        self.predictions: List[Dict] = []
        self.reference_data: Optional[pd.DataFrame] = None
        
        # Prometheus metrics
        self.prediction_counter = Counter(
            'model_predictions_total',
            'Total predictions made'
        )
        
        self.prediction_latency = Histogram(
            'model_prediction_latency_seconds',
            'Prediction latency'
        )
        
        self.drift_score = Gauge(
            'model_drift_score',
            'Data drift score',
            ['feature']
        )
        
        self.performance_metric = Gauge(
            'model_performance',
            'Model performance metric',
            ['metric']
        )
    
    def set_reference_data(self, data: pd.DataFrame, target_col: str = None):
        """
        Set reference data for drift detection.
        
        Args:
            data: Training or validation dataset
            target_col: Target column name (optional)
        """
        self.reference_data = data.copy()
        self.target_col = target_col
        logger.info(f"Set reference data: {len(data)} rows, {len(data.columns)} features")
    
    def log_prediction(
        self,
        features: Dict,
        prediction: float,
        ground_truth: Optional[float] = None,
        prediction_time: float = None,
        metadata: Dict = None
    ):
        """
        Log a prediction for monitoring.
        
        Args:
            features: Input features dict
            prediction: Model prediction
            ground_truth: Actual label (if available)
            prediction_time: Inference latency in seconds
            metadata: Additional metadata
        """
        record = {
            'timestamp': datetime.now(),
            'features': features,
            'prediction': prediction,
            'ground_truth': ground_truth,
            'prediction_time': prediction_time,
            'metadata': metadata or {}
        }
        
        self.predictions.append(record)
        
        # Update Prometheus metrics
        self.prediction_counter.inc()
        if prediction_time:
            self.prediction_latency.observe(prediction_time)
        
        # Check if monitoring should run
        if len(self.predictions) >= self.config.window_size:
            self._run_monitoring_checks()
    
    def _run_monitoring_checks(self):
        """Run all monitoring checks."""
        logger.info(f"Running monitoring checks on {len(self.predictions)} predictions")
        
        # Convert predictions to DataFrame
        current_data = self._predictions_to_dataframe()
        
        # 1. Data Drift Detection
        if self.reference_data is not None:
            drift_results = self._detect_data_drift(current_data)
            if drift_results['has_drift']:
                self._alert_drift(drift_results)
        
        # 2. Performance Monitoring
        if any(p['ground_truth'] is not None for p in self.predictions):
            performance_results = self._monitor_performance(current_data)
            if performance_results['degraded']:
                self._alert_performance(performance_results)
        
        # 3. Prediction Distribution
        distribution_results = self._check_prediction_distribution(current_data)
        if distribution_results['anomalous']:
            self._alert_distribution(distribution_results)
        
        # Clear processed predictions (keep last 10% for overlap)
        keep_count = int(len(self.predictions) * 0.1)
        self.predictions = self.predictions[-keep_count:]
    
    def _predictions_to_dataframe(self) -> pd.DataFrame:
        """Convert predictions list to DataFrame."""
        features_list = [p['features'] for p in self.predictions]
        df = pd.DataFrame(features_list)
        
        df['prediction'] = [p['prediction'] for p in self.predictions]
        df['ground_truth'] = [p.get('ground_truth') for p in self.predictions]
        df['timestamp'] = [p['timestamp'] for p in self.predictions]
        
        return df
    
    def _detect_data_drift(self, current_data: pd.DataFrame) -> Dict:
        """
        Detect data drift using Kolmogorov-Smirnov test.
        
        Args:
            current_data: Current production data
            
        Returns:
            Dict with drift detection results
        """
        drift_results = {
            'has_drift': False,
            'drifted_features': [],
            'drift_scores': {}
        }
        
        for col in self.reference_data.columns:
            if col == self.target_col or col not in current_data.columns:
                continue
            
            # Skip non-numeric columns
            if not pd.api.types.is_numeric_dtype(current_data[col]):
                continue
            
            # KS test
            ref_values = self.reference_data[col].dropna()
            cur_values = current_data[col].dropna()
            
            if len(ref_values) == 0 or len(cur_values) == 0:
                continue
            
            statistic, p_value = ks_2samp(ref_values, cur_values)
            
            drift_results['drift_scores'][col] = {
                'statistic': statistic,
                'p_value': p_value
            }
            
            # Update Prometheus metric
            self.drift_score.labels(feature=col).set(statistic)
            
            # Check threshold
            if p_value < self.config.drift_threshold:
                drift_results['has_drift'] = True
                drift_results['drifted_features'].append(col)
                logger.warning(
                    f"Drift detected in feature '{col}': "
                    f"p-value={p_value:.4f}, statistic={statistic:.4f}"
                )
        
        return drift_results
    
    def _calculate_psi(
        self,
        reference: np.ndarray,
        current: np.ndarray,
        bins: int = 10
    ) -> float:
        """
        Calculate Population Stability Index (PSI).
        
        PSI < 0.1: No significant change
        0.1 <= PSI < 0.2: Moderate change
        PSI >= 0.2: Significant change
        """
        # Create bins
        min_val = min(reference.min(), current.min())
        max_val = max(reference.max(), current.max())
        bin_edges = np.linspace(min_val, max_val, bins + 1)
        
        # Calculate distributions
        ref_counts, _ = np.histogram(reference, bins=bin_edges)
        cur_counts, _ = np.histogram(current, bins=bin_edges)
        
        # Add small constant to avoid division by zero
        ref_percents = (ref_counts + 1e-6) / (len(reference) + bins * 1e-6)
        cur_percents = (cur_counts + 1e-6) / (len(current) + bins * 1e-6)
        
        # Calculate PSI
        psi = np.sum((cur_percents - ref_percents) * np.log(cur_percents / ref_percents))
        
        return psi
    
    def _monitor_performance(self, current_data: pd.DataFrame) -> Dict:
        """
        Monitor model performance metrics.
        
        Args:
            current_data: Current predictions with ground truth
            
        Returns:
            Dict with performance results
        """
        # Filter rows with ground truth
        valid_data = current_data[current_data['ground_truth'].notna()]
        
        if len(valid_data) == 0:
            return {'degraded': False, 'reason': 'No ground truth available'}
        
        y_true = valid_data['ground_truth'].values
        y_pred = valid_data['prediction'].values
        
        # Calculate metrics (assuming binary classification)
        y_pred_binary = (y_pred > 0.5).astype(int)
        
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred_binary),
            'precision': precision_score(y_true, y_pred_binary, zero_division=0),
            'recall': recall_score(y_true, y_pred_binary, zero_division=0),
            'f1': f1_score(y_true, y_pred_binary, zero_division=0)
        }
        
        # Update Prometheus metrics
        for metric_name, value in metrics.items():
            self.performance_metric.labels(metric=metric_name).set(value)
        
        # Check for degradation
        # This would compare against historical performance
        # For demo, we check if metrics are below absolute thresholds
        degraded = any(v < 0.7 for v in metrics.values())
        
        return {
            'degraded': degraded,
            'metrics': metrics,
            'sample_size': len(valid_data)
        }
    
    def _check_prediction_distribution(self, current_data: pd.DataFrame) -> Dict:
        """
        Check for anomalous prediction distributions.
        
        Args:
            current_data: Current predictions
            
        Returns:
            Dict with distribution check results
        """
        predictions = current_data['prediction'].values
        
        results = {
            'anomalous': False,
            'statistics': {
                'mean': float(np.mean(predictions)),
                'std': float(np.std(predictions)),
                'min': float(np.min(predictions)),
                'max': float(np.max(predictions)),
                'median': float(np.median(predictions))
            }
        }
        
        # Check for anomalies
        # Example: Check if >95% predictions are same value
        unique_ratio = len(np.unique(predictions)) / len(predictions)
        if unique_ratio < 0.05:
            results['anomalous'] = True
            results['reason'] = f"Low diversity: {unique_ratio:.2%} unique predictions"
            logger.warning(f"Anomalous prediction distribution: {results['reason']}")
        
        return results
    
    def _alert_drift(self, drift_results: Dict):
        """Send alert for data drift."""
        message = f"Data drift detected!\n"
        message += f"Drifted features: {', '.join(drift_results['drifted_features'])}\n\n"
        
        for feature in drift_results['drifted_features']:
            scores = drift_results['drift_scores'][feature]
            message += f"{feature}: p-value={scores['p_value']:.4f}\n"
        
        logger.error(message)
        # In production: send email, Slack, PagerDuty, etc.
    
    def _alert_performance(self, performance_results: Dict):
        """Send alert for performance degradation."""
        message = f"Model performance degraded!\n"
        message += f"Metrics:\n"
        
        for metric, value in performance_results['metrics'].items():
            message += f"  {metric}: {value:.4f}\n"
        
        logger.error(message)
    
    def _alert_distribution(self, distribution_results: Dict):
        """Send alert for anomalous distributions."""
        message = f"Anomalous prediction distribution detected!\n"
        message += f"Reason: {distribution_results.get('reason', 'Unknown')}\n"
        
        logger.error(message)
    
    def get_monitoring_report(self) -> Dict:
        """
        Generate monitoring report.
        
        Returns:
            Dict with monitoring statistics
        """
        if not self.predictions:
            return {'status': 'No predictions logged'}
        
        current_data = self._predictions_to_dataframe()
        
        report = {
            'total_predictions': len(self.predictions),
            'time_range': {
                'start': min(p['timestamp'] for p in self.predictions),
                'end': max(p['timestamp'] for p in self.predictions)
            },
            'prediction_stats': {
                'mean': float(current_data['prediction'].mean()),
                'std': float(current_data['prediction'].std()),
                'min': float(current_data['prediction'].min()),
                'max': float(current_data['prediction'].max())
            }
        }
        
        # Add drift info if reference data available
        if self.reference_data is not None:
            drift_results = self._detect_data_drift(current_data)
            report['drift'] = drift_results
        
        # Add performance if ground truth available
        if any(p['ground_truth'] is not None for p in self.predictions):
            performance_results = self._monitor_performance(current_data)
            report['performance'] = performance_results
        
        return report


# Example usage
if __name__ == "__main__":
    # Initialize monitor
    config = MonitoringConfig(
        drift_threshold=0.05,
        performance_threshold=0.05,
        window_size=100
    )
    monitor = ModelMonitor(config)
    
    # Set reference data (training set)
    reference_data = pd.DataFrame({
        'feature_1': np.random.normal(0, 1, 1000),
        'feature_2': np.random.normal(5, 2, 1000),
        'target': np.random.binomial(1, 0.3, 1000)
    })
    monitor.set_reference_data(reference_data, target_col='target')
    
    # Simulate predictions
    for i in range(150):
        # Simulate drift after 100 predictions
        if i < 100:
            features = {
                'feature_1': np.random.normal(0, 1),
                'feature_2': np.random.normal(5, 2)
            }
        else:
            # Introduce drift
            features = {
                'feature_1': np.random.normal(2, 1),  # Mean shifted
                'feature_2': np.random.normal(5, 3)   # Variance increased
            }
        
        prediction = np.random.random()
        ground_truth = np.random.binomial(1, 0.3)
        
        monitor.log_prediction(
            features=features,
            prediction=prediction,
            ground_truth=ground_truth,
            prediction_time=0.015
        )
    
    # Get monitoring report
    report = monitor.get_monitoring_report()
    print("\n=== Monitoring Report ===")
    print(f"Total predictions: {report['total_predictions']}")
    print(f"Drift detected: {report.get('drift', {}).get('has_drift', False)}")
    if 'drift' in report and report['drift']['has_drift']:
        print(f"Drifted features: {report['drift']['drifted_features']}")
