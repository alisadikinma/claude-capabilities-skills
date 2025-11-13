#!/usr/bin/env python3
"""
Terraform Configuration Validator

Validates Terraform configurations for best practices, security issues,
and potential cost optimization opportunities.

Usage:
    python validate_terraform.py <terraform_directory>
    python validate_terraform.py ./terraform/production
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

class TerraformValidator:
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.errors = []
        self.warnings = []
        self.suggestions = []
        
    def validate(self) -> bool:
        """Run all validation checks"""
        print(f"🔍 Validating Terraform configuration in {self.directory}")
        print("=" * 60)
        
        self.check_directory_structure()
        self.check_terraform_files()
        self.check_security_issues()
        self.check_cost_optimization()
        self.check_best_practices()
        
        self.print_results()
        
        return len(self.errors) == 0
    
    def check_directory_structure(self):
        """Check for recommended directory structure"""
        required_files = ['main.tf', 'variables.tf', 'outputs.tf']
        recommended_files = ['versions.tf', 'terraform.tfvars.example', 'README.md']
        
        for file in required_files:
            if not (self.directory / file).exists():
                self.errors.append(f"Missing required file: {file}")
        
        for file in recommended_files:
            if not (self.directory / file).exists():
                self.warnings.append(f"Missing recommended file: {file}")
    
    def check_terraform_files(self):
        """Validate Terraform syntax and structure"""
        tf_files = list(self.directory.glob('*.tf'))
        
        if not tf_files:
            self.errors.append("No .tf files found in directory")
            return
        
        for tf_file in tf_files:
            self.validate_file_syntax(tf_file)
    
    def validate_file_syntax(self, file_path: Path):
        """Check individual Terraform file for issues"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for hardcoded credentials
        if re.search(r'password\s*=\s*["\'](?!var\.)[^"\']+["\']', content):
            self.errors.append(f"{file_path.name}: Hardcoded password detected")
        
        if re.search(r'access_key\s*=\s*["\'][^"\']+["\']', content):
            self.errors.append(f"{file_path.name}: Hardcoded AWS access key detected")
        
        # Check for provider version constraints
        if 'provider "' in content and 'version' not in content:
            self.warnings.append(f"{file_path.name}: Provider version not pinned")
        
        # Check for resource naming
        if re.search(r'resource\s+"[^"]+"\s+"[^"]*test[^"]*"', content, re.IGNORECASE):
            self.warnings.append(f"{file_path.name}: Resource name contains 'test'")
        
        # Check for missing tags
        resources_without_tags = re.findall(
            r'resource\s+"(aws_[^"]+)"\s+"[^"]+"\s*\{[^}]*?(?!tags\s*=)',
            content,
            re.DOTALL
        )
        for resource_type in set(resources_without_tags):
            if resource_type in ['aws_instance', 'aws_s3_bucket', 'aws_ebs_volume']:
                self.warnings.append(
                    f"{file_path.name}: {resource_type} missing tags"
                )
    
    def check_security_issues(self):
        """Check for common security misconfigurations"""
        security_checks = [
            {
                'pattern': r'publicly_accessible\s*=\s*true',
                'message': 'Database with publicly_accessible = true',
                'severity': 'error'
            },
            {
                'pattern': r'cidr_blocks\s*=\s*\["0\.0\.0\.0/0"\]',
                'message': 'Security group allows 0.0.0.0/0 (entire internet)',
                'severity': 'warning'
            },
            {
                'pattern': r'storage_encrypted\s*=\s*false',
                'message': 'Storage encryption disabled',
                'severity': 'warning'
            },
            {
                'pattern': r'enable_https_traffic_only\s*=\s*false',
                'message': 'HTTPS-only traffic not enforced',
                'severity': 'warning'
            },
            {
                'pattern': r'skip_final_snapshot\s*=\s*true',
                'message': 'Final snapshot disabled (data loss risk)',
                'severity': 'warning'
            }
        ]
        
        for tf_file in self.directory.glob('*.tf'):
            with open(tf_file, 'r') as f:
                content = f.read()
            
            for check in security_checks:
                if re.search(check['pattern'], content):
                    msg = f"{tf_file.name}: {check['message']}"
                    if check['severity'] == 'error':
                        self.errors.append(msg)
                    else:
                        self.warnings.append(msg)
    
    def check_cost_optimization(self):
        """Suggest cost optimization opportunities"""
        cost_checks = [
            {
                'pattern': r'instance_type\s*=\s*"[tm][234]\.(micro|small)"',
                'message': 'Consider using graviton instances for cost savings'
            },
            {
                'pattern': r'capacity_type\s*=\s*"ON_DEMAND"',
                'message': 'Consider SPOT instances for non-critical workloads'
            },
            {
                'pattern': r'storage_type\s*=\s*"io1"',
                'message': 'Consider gp3 instead of io1 for cost savings'
            },
            {
                'pattern': r'multi_az\s*=\s*false',
                'message': 'Multi-AZ disabled (consider for production)'
            }
        ]
        
        for tf_file in self.directory.glob('*.tf'):
            with open(tf_file, 'r') as f:
                content = f.read()
            
            for check in cost_checks:
                if re.search(check['pattern'], content):
                    self.suggestions.append(f"{tf_file.name}: {check['message']}")
    
    def check_best_practices(self):
        """Check Terraform best practices"""
        # Check for remote backend
        has_backend = False
        for tf_file in self.directory.glob('*.tf'):
            with open(tf_file, 'r') as f:
                if 'backend "' in f.read():
                    has_backend = True
                    break
        
        if not has_backend:
            self.warnings.append("No remote backend configured")
        
        # Check for variable descriptions
        variables_file = self.directory / 'variables.tf'
        if variables_file.exists():
            with open(variables_file, 'r') as f:
                content = f.read()
                variables = re.findall(r'variable\s+"([^"]+)"', content)
                for var in variables:
                    if not re.search(
                        f'variable\\s+"{var}".*?description\\s*=',
                        content,
                        re.DOTALL
                    ):
                        self.warnings.append(
                            f"Variable '{var}' missing description"
                        )
        
        # Check for output descriptions
        outputs_file = self.directory / 'outputs.tf'
        if outputs_file.exists():
            with open(outputs_file, 'r') as f:
                content = f.read()
                outputs = re.findall(r'output\s+"([^"]+)"', content)
                for output in outputs:
                    if not re.search(
                        f'output\\s+"{output}".*?description\\s*=',
                        content,
                        re.DOTALL
                    ):
                        self.warnings.append(
                            f"Output '{output}' missing description"
                        )
    
    def print_results(self):
        """Print validation results"""
        print("\n" + "=" * 60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.suggestions:
            print(f"\n💡 SUGGESTIONS ({len(self.suggestions)}):")
            for suggestion in self.suggestions:
                print(f"  • {suggestion}")
        
        print("\n" + "=" * 60)
        
        if not self.errors and not self.warnings:
            print("\n✅ Validation passed! No issues found.")
        elif not self.errors:
            print("\n✅ Validation passed with warnings.")
        else:
            print(f"\n❌ Validation failed with {len(self.errors)} error(s).")
        
        print()


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_terraform.py <terraform_directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)
    
    validator = TerraformValidator(directory)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
