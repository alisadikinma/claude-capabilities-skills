#!/usr/bin/env python3
"""
API Validator - Web_Architect_Pro
Validate OpenAPI schemas and test endpoints

Usage:
    python api_validator.py validate openapi.yaml
    python api_validator.py test http://localhost:8000
"""

import sys
import json
import yaml
import requests
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def load_spec(file_path: str):
    path = Path(file_path)
    if not path.exists():
        print(f"{Colors.RED}File not found: {file_path}{Colors.RESET}")
        sys.exit(1)
    
    with open(path, 'r') as f:
        if path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        return json.load(f)

def validate_spec(spec):
    errors = []
    
    if 'openapi' not in spec:
        errors.append("Missing 'openapi' version")
    
    if 'info' not in spec:
        errors.append("Missing 'info' section")
    else:
        if 'title' not in spec['info']:
            errors.append("Missing 'info.title'")
        if 'version' not in spec['info']:
            errors.append("Missing 'info.version'")
    
    if 'paths' not in spec:
        errors.append("Missing 'paths' section")
    
    return errors

def validate_endpoints(spec):
    issues = []
    
    for path, methods in spec.get('paths', {}).items():
        for method, endpoint in methods.items():
            if method.startswith('x-'):
                continue
            
            if 'operationId' not in endpoint:
                issues.append({
                    'level': 'warning',
                    'path': path,
                    'method': method,
                    'message': 'Missing operationId'
                })
            
            if 'responses' not in endpoint:
                issues.append({
                    'level': 'error',
                    'path': path,
                    'method': method,
                    'message': 'Missing responses'
                })
    
    return issues

def print_issues(issues):
    if not issues:
        print(f"\n{Colors.GREEN}✓ No issues{Colors.RESET}")
        return
    
    errors = [i for i in issues if i['level'] == 'error']
    warnings = [i for i in issues if i['level'] == 'warning']
    
    if errors:
        print(f"\n{Colors.RED}Errors ({len(errors)}):{Colors.RESET}")
        for issue in errors:
            print(f"  {issue['method'].upper()} {issue['path']}: {issue['message']}")
    
    if warnings:
        print(f"\n{Colors.YELLOW}Warnings ({len(warnings)}):{Colors.RESET}")
        for issue in warnings:
            print(f"  {issue['method'].upper()} {issue['path']}: {issue['message']}")

def validate_command(file_path: str):
    print(f"\n{Colors.BLUE}Validating: {file_path}{Colors.RESET}")
    
    spec = load_spec(file_path)
    
    # Structure
    errors = validate_spec(spec)
    if errors:
        print(f"\n{Colors.RED}Validation failed:{Colors.RESET}")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print(f"{Colors.GREEN}✓ Structure OK{Colors.RESET}")
    
    # Endpoints
    issues = validate_endpoints(spec)
    print_issues(issues)
    
    if any(i['level'] == 'error' for i in issues):
        sys.exit(1)
    
    print(f"\n{Colors.GREEN}✅ Validation passed{Colors.RESET}")

def test_command(base_url: str):
    print(f"\n{Colors.BLUE}Testing API: {base_url}{Colors.RESET}\n")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"{Colors.GREEN}✓ API is healthy{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠ Status: {response.status_code}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.RESET}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python api_validator.py validate <file>")
        print("  python api_validator.py test <url>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'validate' and len(sys.argv) >= 3:
        validate_command(sys.argv[2])
    elif command == 'test' and len(sys.argv) >= 3:
        test_command(sys.argv[2])
    else:
        print(f"{Colors.RED}Invalid command{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
