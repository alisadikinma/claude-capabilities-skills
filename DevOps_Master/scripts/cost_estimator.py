#!/usr/bin/env python3
"""
Terraform Cost Estimator

Estimates monthly cloud costs based on Terraform configurations
for AWS, GCP, and Azure resources.

Usage:
    python cost_estimator.py <terraform_directory>
    python cost_estimator.py ./terraform/production
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ResourceCost:
    resource_type: str
    resource_name: str
    monthly_cost: float
    details: str

class CostEstimator:
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.costs = []
        self.total_cost = 0.0
        
        # Simplified pricing (USD/month)
        # NOTE: These are approximate costs and should be updated regularly
        self.aws_pricing = {
            # EC2 instances (us-east-1 on-demand)
            't3.micro': 7.52,
            't3.small': 15.04,
            't3.medium': 30.08,
            't3.large': 60.16,
            't3.xlarge': 120.32,
            't3.2xlarge': 240.64,
            'm5.large': 70.08,
            'm5.xlarge': 140.16,
            'm5.2xlarge': 280.32,
            'c5.large': 62.05,
            'c5.xlarge': 124.10,
            'r5.large': 91.98,
            'r5.xlarge': 183.96,
            
            # RDS instances
            'db.t3.micro': 12.41,
            'db.t3.small': 24.82,
            'db.t3.medium': 49.64,
            'db.t3.large': 99.28,
            'db.m5.large': 124.56,
            'db.m5.xlarge': 249.12,
            'db.r5.large': 172.80,
            
            # EBS storage (per GB/month)
            'gp2': 0.10,
            'gp3': 0.08,
            'io1': 0.125,
            'io2': 0.125,
            
            # S3 storage (per GB/month)
            's3_standard': 0.023,
            's3_ia': 0.0125,
            's3_glacier': 0.004,
            
            # NAT Gateway
            'nat_gateway': 32.40,  # per gateway
            
            # Load Balancer
            'alb': 16.20,  # Application Load Balancer
            'nlb': 16.20,  # Network Load Balancer
            
            # ElastiCache
            'cache.t3.micro': 12.41,
            'cache.t3.small': 24.82,
            'cache.t3.medium': 49.64,
            'cache.m5.large': 124.56,
        }
        
        self.gcp_pricing = {
            # Compute Engine (n1-standard)
            'n1-standard-1': 24.27,
            'n1-standard-2': 48.55,
            'n1-standard-4': 97.09,
            'n1-standard-8': 194.18,
            
            # Cloud SQL
            'db-n1-standard-1': 46.71,
            'db-n1-standard-2': 93.42,
            'db-custom-2-7680': 88.80,
            
            # Persistent Disk (per GB/month)
            'pd-standard': 0.040,
            'pd-ssd': 0.170,
            
            # Cloud Storage (per GB/month)
            'standard': 0.020,
            'nearline': 0.010,
            'coldline': 0.004,
        }
        
        self.azure_pricing = {
            # Virtual Machines
            'Standard_B1s': 7.59,
            'Standard_B2s': 30.37,
            'Standard_D2s_v3': 70.08,
            'Standard_D4s_v3': 140.16,
            
            # SQL Database
            'Basic': 4.99,
            'S0': 15.00,
            'S1': 30.00,
            'P1': 465.00,
            
            # Storage (per GB/month)
            'standard': 0.0184,
            'premium': 0.15,
        }
    
    def estimate(self) -> float:
        """Estimate total monthly cost"""
        print(f"💰 Estimating costs for {self.directory}")
        print("=" * 60)
        
        self.estimate_aws_resources()
        self.estimate_gcp_resources()
        self.estimate_azure_resources()
        
        self.print_results()
        
        return self.total_cost
    
    def estimate_aws_resources(self):
        """Estimate AWS resource costs"""
        for tf_file in self.directory.glob('*.tf'):
            with open(tf_file, 'r') as f:
                content = f.read()
            
            # EC2 instances
            ec2_instances = re.findall(
                r'resource\s+"aws_instance"\s+"([^"]+)".*?instance_type\s*=\s*"([^"]+)".*?count\s*=\s*(\d+)',
                content,
                re.DOTALL
            )
            for name, instance_type, count in ec2_instances:
                cost = self.aws_pricing.get(instance_type, 0) * int(count)
                self.add_cost(
                    'aws_instance',
                    name,
                    cost,
                    f"{count}x {instance_type}"
                )
            
            # RDS instances
            rds_instances = re.findall(
                r'resource\s+"aws_db_instance"\s+"([^"]+)".*?instance_class\s*=\s*"([^"]+)"',
                content,
                re.DOTALL
            )
            for name, instance_class in rds_instances:
                cost = self.aws_pricing.get(instance_class, 0)
                # Check for Multi-AZ
                if 'multi_az = true' in content:
                    cost *= 2
                    details = f"{instance_class} (Multi-AZ)"
                else:
                    details = instance_class
                self.add_cost('aws_db_instance', name, cost, details)
            
            # EBS volumes
            ebs_volumes = re.findall(
                r'resource\s+"aws_ebs_volume"\s+"([^"]+)".*?size\s*=\s*(\d+).*?type\s*=\s*"([^"]+)"',
                content,
                re.DOTALL
            )
            for name, size, volume_type in ebs_volumes:
                cost = self.aws_pricing.get(volume_type, 0.10) * int(size)
                self.add_cost(
                    'aws_ebs_volume',
                    name,
                    cost,
                    f"{size}GB {volume_type}"
                )
            
            # S3 buckets (estimate 100GB per bucket)
            s3_buckets = re.findall(r'resource\s+"aws_s3_bucket"\s+"([^"]+)"', content)
            for name in s3_buckets:
                cost = self.aws_pricing['s3_standard'] * 100  # Assume 100GB
                self.add_cost(
                    'aws_s3_bucket',
                    name,
                    cost,
                    "~100GB (estimate)"
                )
            
            # NAT Gateways
            nat_gateways = re.findall(
                r'resource\s+"aws_nat_gateway"\s+"([^"]+)".*?count\s*=\s*(\d+)',
                content,
                re.DOTALL
            )
            for name, count in nat_gateways:
                cost = self.aws_pricing['nat_gateway'] * int(count)
                self.add_cost(
                    'aws_nat_gateway',
                    name,
                    cost,
                    f"{count}x NAT Gateway"
                )
            
            # Load Balancers
            alb_count = len(re.findall(r'resource\s+"aws_lb"\s+"([^"]+)".*?load_balancer_type\s*=\s*"application"', content, re.DOTALL))
            if alb_count:
                self.add_cost(
                    'aws_lb',
                    'alb',
                    self.aws_pricing['alb'] * alb_count,
                    f"{alb_count}x Application LB"
                )
            
            # ElastiCache
            elasticache = re.findall(
                r'resource\s+"aws_elasticache_replication_group"\s+"([^"]+)".*?node_type\s*=\s*"([^"]+)".*?num_cache_clusters\s*=\s*(\d+)',
                content,
                re.DOTALL
            )
            for name, node_type, num_nodes in elasticache:
                cost = self.aws_pricing.get(node_type, 0) * int(num_nodes)
                self.add_cost(
                    'aws_elasticache',
                    name,
                    cost,
                    f"{num_nodes}x {node_type}"
                )
    
    def estimate_gcp_resources(self):
        """Estimate GCP resource costs"""
        for tf_file in self.directory.glob('*.tf'):
            with open(tf_file, 'r') as f:
                content = f.read()
            
            # Compute instances
            instances = re.findall(
                r'resource\s+"google_compute_instance"\s+"([^"]+)".*?machine_type\s*=\s*"([^"]+)"',
                content,
                re.DOTALL
            )
            for name, machine_type in instances:
                cost = self.gcp_pricing.get(machine_type, 0)
                self.add_cost(
                    'google_compute_instance',
                    name,
                    cost,
                    machine_type
                )
            
            # Cloud SQL
            sql_instances = re.findall(
                r'resource\s+"google_sql_database_instance"\s+"([^"]+)".*?tier\s*=\s*"([^"]+)"',
                content,
                re.DOTALL
            )
            for name, tier in sql_instances:
                cost = self.gcp_pricing.get(tier, 0)
                self.add_cost(
                    'google_sql_database_instance',
                    name,
                    cost,
                    tier
                )
    
    def estimate_azure_resources(self):
        """Estimate Azure resource costs"""
        for tf_file in self.directory.glob('*.tf'):
            with open(tf_file, 'r') as f:
                content = f.read()
            
            # Virtual Machines
            vms = re.findall(
                r'resource\s+"azurerm_virtual_machine"\s+"([^"]+)".*?vm_size\s*=\s*"([^"]+)"',
                content,
                re.DOTALL
            )
            for name, vm_size in vms:
                cost = self.azure_pricing.get(vm_size, 0)
                self.add_cost(
                    'azurerm_virtual_machine',
                    name,
                    cost,
                    vm_size
                )
    
    def add_cost(self, resource_type: str, name: str, cost: float, details: str):
        """Add resource cost to total"""
        self.costs.append(ResourceCost(
            resource_type=resource_type,
            resource_name=name,
            monthly_cost=cost,
            details=details
        ))
        self.total_cost += cost
    
    def print_results(self):
        """Print cost estimate results"""
        if not self.costs:
            print("\n⚠️  No resources found or unable to estimate costs")
            print("=" * 60)
            return
        
        # Group by resource type
        by_type = {}
        for cost in self.costs:
            if cost.resource_type not in by_type:
                by_type[cost.resource_type] = []
            by_type[cost.resource_type].append(cost)
        
        print("\n📊 Cost Breakdown by Resource Type:")
        print("-" * 60)
        
        for resource_type in sorted(by_type.keys()):
            type_total = sum(c.monthly_cost for c in by_type[resource_type])
            print(f"\n{resource_type}:")
            for cost in by_type[resource_type]:
                print(f"  • {cost.resource_name}: ${cost.monthly_cost:.2f}/mo ({cost.details})")
            print(f"  Subtotal: ${type_total:.2f}/mo")
        
        print("\n" + "=" * 60)
        print(f"\n💵 ESTIMATED MONTHLY COST: ${self.total_cost:.2f}")
        print(f"💵 ESTIMATED ANNUAL COST:  ${self.total_cost * 12:.2f}")
        
        # Savings suggestions
        print("\n💡 Cost Optimization Suggestions:")
        if self.total_cost > 1000:
            print("  • Consider Reserved Instances for 1-3 year commitment (up to 72% savings)")
            print("  • Use Savings Plans for flexible commitment options")
        if any('t3' in c.details for c in self.costs):
            print("  • Consider Graviton instances (ARM) for 20% cost savings")
        if any('on-demand' in c.details.lower() for c in self.costs):
            print("  • Use Spot Instances for non-critical workloads (up to 90% savings)")
        
        print("\n⚠️  Note: These are estimates based on on-demand pricing.")
        print("    Actual costs may vary based on usage, data transfer, and other factors.")
        print("=" * 60)
        print()


def main():
    if len(sys.argv) != 2:
        print("Usage: python cost_estimator.py <terraform_directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)
    
    estimator = CostEstimator(directory)
    total = estimator.estimate()
    
    sys.exit(0)


if __name__ == '__main__':
    main()
