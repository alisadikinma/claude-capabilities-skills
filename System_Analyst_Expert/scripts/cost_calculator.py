#!/usr/bin/env python3
"""
Cloud Infrastructure Cost Calculator
Calculates and compares costs across AWS, GCP, and Azure for common infrastructure components.

Usage:
    python cost_calculator.py --config infra_config.yaml
    python cost_calculator.py --interactive
"""

import sys
import yaml
from typing import Dict, List
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ComputeInstance:
    """Compute instance specification."""
    vcpus: int
    ram_gb: int
    quantity: int = 1
    hours_per_month: int = 730  # 24*365/12


@dataclass
class Database:
    """Database specification."""
    engine: str  # postgres, mysql, mongodb
    storage_gb: int
    instance_class: str  # small, medium, large, xlarge
    multi_az: bool = False


@dataclass
class Storage:
    """Storage specification."""
    type: str  # object, block
    size_gb: int
    requests_per_month: int = 0


class CostCalculator:
    """Calculate infrastructure costs across cloud providers."""
    
    # Pricing data (USD, as of 2024)
    PRICING = {
        'aws': {
            'compute': {
                't3.small': {'vcpu': 2, 'ram': 2, 'price': 0.0208},
                't3.medium': {'vcpu': 2, 'ram': 4, 'price': 0.0416},
                't3.large': {'vcpu': 2, 'ram': 8, 'price': 0.0832},
                't3.xlarge': {'vcpu': 4, 'ram': 16, 'price': 0.1664},
                'm5.large': {'vcpu': 2, 'ram': 8, 'price': 0.096},
                'm5.xlarge': {'vcpu': 4, 'ram': 16, 'price': 0.192},
                'm5.2xlarge': {'vcpu': 8, 'ram': 32, 'price': 0.384},
                'c5.large': {'vcpu': 2, 'ram': 4, 'price': 0.085},
                'c5.xlarge': {'vcpu': 4, 'ram': 8, 'price': 0.17},
            },
            'database': {
                'postgres': {
                    'small': 0.017,  # db.t3.micro
                    'medium': 0.068,  # db.t3.large
                    'large': 0.272,  # db.m5.xlarge
                    'xlarge': 0.544,  # db.m5.2xlarge
                },
                'mysql': {
                    'small': 0.017,
                    'medium': 0.068,
                    'large': 0.272,
                    'xlarge': 0.544,
                },
            },
            'storage': {
                's3': 0.023,  # per GB/month
                'ebs': 0.10,  # gp3 per GB/month
            },
            'data_transfer': 0.09,  # per GB outbound
        },
        'gcp': {
            'compute': {
                'e2-small': {'vcpu': 2, 'ram': 2, 'price': 0.0201},
                'e2-medium': {'vcpu': 2, 'ram': 4, 'price': 0.0402},
                'e2-standard-2': {'vcpu': 2, 'ram': 8, 'price': 0.0670},
                'e2-standard-4': {'vcpu': 4, 'ram': 16, 'price': 0.1340},
                'n2-standard-2': {'vcpu': 2, 'ram': 8, 'price': 0.0970},
                'n2-standard-4': {'vcpu': 4, 'ram': 16, 'price': 0.1940},
                'n2-standard-8': {'vcpu': 8, 'ram': 32, 'price': 0.3880},
                'c2-standard-4': {'vcpu': 4, 'ram': 16, 'price': 0.2088},
            },
            'database': {
                'postgres': {
                    'small': 0.015,
                    'medium': 0.060,
                    'large': 0.240,
                    'xlarge': 0.480,
                },
                'mysql': {
                    'small': 0.015,
                    'medium': 0.060,
                    'large': 0.240,
                    'xlarge': 0.480,
                },
            },
            'storage': {
                'cloud_storage': 0.020,  # per GB/month
                'persistent_disk': 0.085,  # pd-ssd per GB/month
            },
            'data_transfer': 0.085,  # per GB outbound
        },
        'azure': {
            'compute': {
                'B1s': {'vcpu': 1, 'ram': 1, 'price': 0.0104},
                'B2s': {'vcpu': 2, 'ram': 4, 'price': 0.0416},
                'D2s_v3': {'vcpu': 2, 'ram': 8, 'price': 0.096},
                'D4s_v3': {'vcpu': 4, 'ram': 16, 'price': 0.192},
                'D8s_v3': {'vcpu': 8, 'ram': 32, 'price': 0.384},
                'F2s_v2': {'vcpu': 2, 'ram': 4, 'price': 0.085},
                'F4s_v2': {'vcpu': 4, 'ram': 8, 'price': 0.169},
            },
            'database': {
                'postgres': {
                    'small': 0.018,
                    'medium': 0.072,
                    'large': 0.288,
                    'xlarge': 0.576,
                },
                'mysql': {
                    'small': 0.018,
                    'medium': 0.072,
                    'large': 0.288,
                    'xlarge': 0.576,
                },
            },
            'storage': {
                'blob_storage': 0.0184,  # per GB/month
                'managed_disk': 0.12,  # premium SSD per GB/month
            },
            'data_transfer': 0.087,  # per GB outbound
        }
    }
    
    def __init__(self, config: Dict):
        self.config = config
        self.results = {}
    
    def calculate_all_providers(self) -> Dict:
        """Calculate costs for all providers."""
        providers = ['aws', 'gcp', 'azure']
        
        for provider in providers:
            self.results[provider] = self.calculate_provider(provider)
        
        return self.results
    
    def calculate_provider(self, provider: str) -> Dict:
        """Calculate costs for a single provider."""
        pricing = self.PRICING[provider]
        
        costs = {
            'compute': 0,
            'database': 0,
            'storage': 0,
            'data_transfer': 0,
            'total': 0,
        }
        
        # Compute costs
        if 'compute' in self.config:
            costs['compute'] = self._calculate_compute(provider, self.config['compute'])
        
        # Database costs
        if 'database' in self.config:
            costs['database'] = self._calculate_database(provider, self.config['database'])
        
        # Storage costs
        if 'storage' in self.config:
            costs['storage'] = self._calculate_storage(provider, self.config['storage'])
        
        # Data transfer costs
        if 'data_transfer_gb' in self.config:
            costs['data_transfer'] = self.config['data_transfer_gb'] * pricing['data_transfer']
        
        costs['total'] = sum(costs.values())
        
        return costs
    
    def _calculate_compute(self, provider: str, compute_config: List[Dict]) -> float:
        """Calculate compute costs."""
        pricing = self.PRICING[provider]['compute']
        total_cost = 0
        
        for instance in compute_config:
            instance_type = self._select_instance_type(
                provider,
                instance['vcpus'],
                instance['ram_gb']
            )
            
            if instance_type:
                hourly_price = pricing[instance_type]['price']
                hours = instance.get('hours_per_month', 730)
                quantity = instance.get('quantity', 1)
                
                cost = hourly_price * hours * quantity
                total_cost += cost
        
        return total_cost
    
    def _calculate_database(self, provider: str, db_config: List[Dict]) -> float:
        """Calculate database costs."""
        pricing = self.PRICING[provider]['database']
        total_cost = 0
        
        for db in db_config:
            engine = db['engine']
            instance_class = db['instance_class']
            storage_gb = db.get('storage_gb', 100)
            multi_az = db.get('multi_az', False)
            
            # Instance cost
            hourly_price = pricing[engine][instance_class]
            instance_cost = hourly_price * 730
            
            if multi_az:
                instance_cost *= 2
            
            # Storage cost (approximate)
            storage_cost = storage_gb * 0.10  # ~$0.10/GB across providers
            
            total_cost += instance_cost + storage_cost
        
        return total_cost
    
    def _calculate_storage(self, provider: str, storage_config: List[Dict]) -> float:
        """Calculate storage costs."""
        pricing = self.PRICING[provider]['storage']
        total_cost = 0
        
        for storage in storage_config:
            storage_type = storage['type']
            size_gb = storage['size_gb']
            
            # Map storage type to provider-specific naming
            if storage_type == 'object':
                if provider == 'aws':
                    price_per_gb = pricing['s3']
                elif provider == 'gcp':
                    price_per_gb = pricing['cloud_storage']
                else:  # azure
                    price_per_gb = pricing['blob_storage']
            else:  # block
                if provider == 'aws':
                    price_per_gb = pricing['ebs']
                elif provider == 'gcp':
                    price_per_gb = pricing['persistent_disk']
                else:  # azure
                    price_per_gb = pricing['managed_disk']
            
            total_cost += size_gb * price_per_gb
        
        return total_cost
    
    def _select_instance_type(self, provider: str, vcpus: int, ram_gb: int) -> str:
        """Select best matching instance type."""
        pricing = self.PRICING[provider]['compute']
        
        # Find instances that meet requirements
        candidates = []
        for instance_type, specs in pricing.items():
            if specs['vcpu'] >= vcpus and specs['ram'] >= ram_gb:
                candidates.append({
                    'type': instance_type,
                    'vcpu': specs['vcpu'],
                    'ram': specs['ram'],
                    'price': specs['price']
                })
        
        if not candidates:
            return None
        
        # Select cheapest option
        candidates.sort(key=lambda x: x['price'])
        return candidates[0]['type']
    
    def print_comparison(self):
        """Print cost comparison table."""
        print("\n" + "="*80)
        print("CLOUD INFRASTRUCTURE COST COMPARISON (USD/month)")
        print("="*80 + "\n")
        
        # Header
        print(f"{'Component':<20} {'AWS':>15} {'GCP':>15} {'Azure':>15}")
        print("-"*80)
        
        # Categories
        categories = ['compute', 'database', 'storage', 'data_transfer']
        
        for category in categories:
            aws_cost = self.results['aws'][category]
            gcp_cost = self.results['gcp'][category]
            azure_cost = self.results['azure'][category]
            
            print(f"{category.title():<20} ${aws_cost:>14.2f} ${gcp_cost:>14.2f} ${azure_cost:>14.2f}")
        
        # Total
        print("-"*80)
        aws_total = self.results['aws']['total']
        gcp_total = self.results['gcp']['total']
        azure_total = self.results['azure']['total']
        
        print(f"{'TOTAL':<20} ${aws_total:>14.2f} ${gcp_total:>14.2f} ${azure_total:>14.2f}")
        print("="*80)
        
        # Find cheapest
        costs = [
            ('AWS', aws_total),
            ('GCP', gcp_total),
            ('Azure', azure_total)
        ]
        costs.sort(key=lambda x: x[1])
        cheapest = costs[0]
        savings_vs_most_expensive = ((costs[2][1] - cheapest[1]) / costs[2][1]) * 100
        
        print(f"\n💰 Cheapest Provider: {cheapest[0]} (${cheapest[1]:.2f}/month)")
        print(f"💵 Potential Savings: ${costs[2][1] - cheapest[1]:.2f}/month ({savings_vs_most_expensive:.1f}%)")
        
        # Annual projection
        print(f"\n📊 Annual Projections:")
        for provider, monthly_cost in costs:
            annual_cost = monthly_cost * 12
            print(f"   {provider}: ${annual_cost:,.2f}/year")
        
        print()


def load_config(config_path: str) -> Dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def interactive_mode():
    """Interactive configuration builder."""
    print("🔧 Interactive Infrastructure Cost Calculator\n")
    
    config = {
        'compute': [],
        'database': [],
        'storage': [],
        'data_transfer_gb': 0
    }
    
    # Compute instances
    print("1. COMPUTE INSTANCES")
    num_instances = int(input("   How many instance types? "))
    
    for i in range(num_instances):
        print(f"\n   Instance #{i+1}:")
        vcpus = int(input("   - vCPUs: "))
        ram_gb = int(input("   - RAM (GB): "))
        quantity = int(input("   - Quantity: "))
        
        config['compute'].append({
            'vcpus': vcpus,
            'ram_gb': ram_gb,
            'quantity': quantity
        })
    
    # Databases
    print("\n2. DATABASES")
    num_dbs = int(input("   How many databases? "))
    
    for i in range(num_dbs):
        print(f"\n   Database #{i+1}:")
        engine = input("   - Engine (postgres/mysql): ")
        instance_class = input("   - Size (small/medium/large/xlarge): ")
        storage_gb = int(input("   - Storage (GB): "))
        
        config['database'].append({
            'engine': engine,
            'instance_class': instance_class,
            'storage_gb': storage_gb
        })
    
    # Storage
    print("\n3. STORAGE")
    num_storage = int(input("   How many storage types? "))
    
    for i in range(num_storage):
        print(f"\n   Storage #{i+1}:")
        storage_type = input("   - Type (object/block): ")
        size_gb = int(input("   - Size (GB): "))
        
        config['storage'].append({
            'type': storage_type,
            'size_gb': size_gb
        })
    
    # Data transfer
    print("\n4. DATA TRANSFER")
    config['data_transfer_gb'] = int(input("   Outbound data transfer (GB/month): "))
    
    return config


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Calculate cloud infrastructure costs')
    parser.add_argument('--config', help='Path to infrastructure config (YAML)')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive:
        config = interactive_mode()
    elif args.config:
        config = load_config(args.config)
    else:
        print("Error: Provide --config or use --interactive mode")
        sys.exit(1)
    
    # Calculate costs
    calculator = CostCalculator(config)
    calculator.calculate_all_providers()
    calculator.print_comparison()


if __name__ == '__main__':
    main()
