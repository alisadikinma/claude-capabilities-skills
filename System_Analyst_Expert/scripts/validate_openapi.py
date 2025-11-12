#!/usr/bin/env python3
"""
OpenAPI 3.0 Specification Validator
Validates API specifications for completeness, security, and best practices.

Usage:
    python validate_openapi.py api_spec.yaml
    python validate_openapi.py api_spec.json --strict
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
import re


class OpenAPIValidator:
    """Validates OpenAPI 3.0 specifications."""
    
    def __init__(self, spec_path: str, strict: bool = False):
        self.spec_path = Path(spec_path)
        self.strict = strict
        self.spec = self._load_spec()
        self.errors = []
        self.warnings = []
        self.info_messages = []
    
    def _load_spec(self) -> Dict:
        """Load OpenAPI spec from YAML or JSON."""
        try:
            with open(self.spec_path, 'r', encoding='utf-8') as f:
                if self.spec_path.suffix in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                else:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            sys.exit(1)
    
    def validate(self) -> Tuple[bool, int, int]:
        """Run all validations. Returns (success, error_count, warning_count)."""
        print(f"🔍 Validating OpenAPI spec: {self.spec_path}\n")
        
        # Core validations
        self._validate_version()
        self._validate_info()
        self._validate_servers()
        self._validate_paths()
        self._validate_components()
        self._validate_security()
        
        # Best practices
        self._check_versioning()
        self._check_error_responses()
        self._check_pagination()
        self._check_rate_limiting()
        self._check_examples()
        
        # Results
        self._print_results()
        
        success = len(self.errors) == 0
        if self.strict:
            success = success and len(self.warnings) == 0
        
        return success, len(self.errors), len(self.warnings)
    
    def _validate_version(self):
        """Validate OpenAPI version."""
        version = self.spec.get('openapi', '')
        if not version.startswith('3.0'):
            self.errors.append("OpenAPI version must be 3.0.x")
        else:
            self.info_messages.append(f"✓ OpenAPI version: {version}")
    
    def _validate_info(self):
        """Validate info section."""
        info = self.spec.get('info', {})
        
        required_fields = ['title', 'version']
        for field in required_fields:
            if field not in info:
                self.errors.append(f"Missing required info.{field}")
        
        recommended_fields = ['description', 'contact', 'license']
        for field in recommended_fields:
            if field not in info:
                self.warnings.append(f"Missing recommended info.{field}")
        
        # Semantic versioning check
        version = info.get('version', '')
        if not re.match(r'^\d+\.\d+\.\d+', version):
            self.warnings.append(f"Version '{version}' doesn't follow semantic versioning (x.y.z)")
    
    def _validate_servers(self):
        """Validate servers section."""
        servers = self.spec.get('servers', [])
        
        if not servers:
            self.warnings.append("No servers defined")
            return
        
        for idx, server in enumerate(servers):
            if 'url' not in server:
                self.errors.append(f"Server #{idx} missing URL")
            
            url = server.get('url', '')
            if url.startswith('http://') and 'localhost' not in url:
                self.warnings.append(f"Server #{idx} uses HTTP (insecure): {url}")
    
    def _validate_paths(self):
        """Validate paths and operations."""
        paths = self.spec.get('paths', {})
        
        if not paths:
            self.errors.append("No paths defined")
            return
        
        self.info_messages.append(f"✓ Found {len(paths)} paths")
        
        for path, path_item in paths.items():
            # Path format check
            if not path.startswith('/'):
                self.errors.append(f"Path '{path}' must start with /")
            
            # Check operations
            operations = ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']
            for op in operations:
                if op in path_item:
                    self._validate_operation(path, op, path_item[op])
    
    def _validate_operation(self, path: str, method: str, operation: Dict):
        """Validate individual operation."""
        op_id = f"{method.upper()} {path}"
        
        # Required fields
        if 'responses' not in operation:
            self.errors.append(f"{op_id}: Missing responses")
        
        # Recommended fields
        if 'summary' not in operation:
            self.warnings.append(f"{op_id}: Missing summary")
        
        if 'operationId' not in operation:
            self.warnings.append(f"{op_id}: Missing operationId")
        
        if 'tags' not in operation:
            self.warnings.append(f"{op_id}: Missing tags")
        
        # Response codes
        responses = operation.get('responses', {})
        
        # Success response (2xx)
        has_success = any(str(code).startswith('2') for code in responses.keys())
        if not has_success:
            self.warnings.append(f"{op_id}: No success response (2xx) defined")
        
        # Error responses
        if method in ['post', 'put', 'patch']:
            if '400' not in responses:
                self.warnings.append(f"{op_id}: Missing 400 Bad Request response")
        
        if '500' not in responses:
            self.warnings.append(f"{op_id}: Missing 500 Internal Server Error response")
        
        # Request body validation
        if method in ['post', 'put', 'patch']:
            if 'requestBody' not in operation:
                self.warnings.append(f"{op_id}: Missing requestBody")
            else:
                self._validate_request_body(op_id, operation['requestBody'])
        
        # Parameters validation
        if 'parameters' in operation:
            self._validate_parameters(op_id, operation['parameters'])
    
    def _validate_request_body(self, op_id: str, request_body: Dict):
        """Validate request body."""
        if 'content' not in request_body:
            self.errors.append(f"{op_id}: requestBody missing content")
            return
        
        content = request_body['content']
        if not content:
            self.errors.append(f"{op_id}: requestBody content is empty")
        
        # Check for JSON
        if 'application/json' not in content:
            self.warnings.append(f"{op_id}: requestBody doesn't support application/json")
    
    def _validate_parameters(self, op_id: str, parameters: List):
        """Validate parameters."""
        for param in parameters:
            if 'name' not in param:
                self.errors.append(f"{op_id}: Parameter missing name")
            
            if 'in' not in param:
                self.errors.append(f"{op_id}: Parameter '{param.get('name', '?')}' missing 'in' field")
            
            if 'schema' not in param and '$ref' not in param:
                self.errors.append(f"{op_id}: Parameter '{param.get('name', '?')}' missing schema")
    
    def _validate_components(self):
        """Validate components section."""
        components = self.spec.get('components', {})
        
        if not components:
            self.warnings.append("No components defined (consider reusing schemas)")
            return
        
        # Validate schemas
        schemas = components.get('schemas', {})
        if schemas:
            self.info_messages.append(f"✓ Found {len(schemas)} component schemas")
            
            for schema_name, schema in schemas.items():
                if 'type' not in schema and '$ref' not in schema:
                    self.warnings.append(f"Schema '{schema_name}' missing type")
        
        # Security schemes
        security_schemes = components.get('securitySchemes', {})
        if security_schemes:
            self.info_messages.append(f"✓ Found {len(security_schemes)} security schemes")
    
    def _validate_security(self):
        """Validate security definitions."""
        components = self.spec.get('components', {})
        security_schemes = components.get('securitySchemes', {})
        
        if not security_schemes:
            self.warnings.append("No security schemes defined")
            return
        
        for scheme_name, scheme in security_schemes.items():
            scheme_type = scheme.get('type', '')
            
            if scheme_type == 'oauth2':
                if 'flows' not in scheme:
                    self.errors.append(f"OAuth2 scheme '{scheme_name}' missing flows")
            
            elif scheme_type == 'http':
                if 'scheme' not in scheme:
                    self.errors.append(f"HTTP scheme '{scheme_name}' missing scheme (bearer, basic, etc)")
            
            elif scheme_type == 'apiKey':
                if 'in' not in scheme:
                    self.errors.append(f"API Key scheme '{scheme_name}' missing 'in' field")
                if 'name' not in scheme:
                    self.errors.append(f"API Key scheme '{scheme_name}' missing 'name' field")
    
    def _check_versioning(self):
        """Check API versioning strategy."""
        paths = self.spec.get('paths', {})
        servers = self.spec.get('servers', [])
        
        # Check if versioning in path
        has_version_in_path = any('/v' in path for path in paths.keys())
        
        # Check if versioning in server URL
        has_version_in_server = any('/v' in s.get('url', '') for s in servers)
        
        if not has_version_in_path and not has_version_in_server:
            self.warnings.append("No API versioning detected (consider /v1, /v2 in paths or server URL)")
    
    def _check_error_responses(self):
        """Check for standardized error responses."""
        paths = self.spec.get('paths', {})
        
        error_codes = ['400', '401', '403', '404', '429', '500']
        operations_with_errors = 0
        total_operations = 0
        
        for path_item in paths.values():
            for method in ['get', 'post', 'put', 'patch', 'delete']:
                if method in path_item:
                    total_operations += 1
                    responses = path_item[method].get('responses', {})
                    
                    has_error_response = any(code in responses for code in error_codes)
                    if has_error_response:
                        operations_with_errors += 1
        
        if total_operations > 0:
            coverage = (operations_with_errors / total_operations) * 100
            if coverage < 50:
                self.warnings.append(f"Only {coverage:.0f}% of operations define error responses")
    
    def _check_pagination(self):
        """Check for pagination in list endpoints."""
        paths = self.spec.get('paths', {})
        
        list_endpoints = [path for path in paths.keys() if not re.search(r'\{.*\}', path)]
        
        for path in list_endpoints:
            path_item = paths[path]
            if 'get' in path_item:
                operation = path_item['get']
                parameters = operation.get('parameters', [])
                param_names = [p.get('name', '') for p in parameters]
                
                has_pagination = any(p in param_names for p in ['page', 'limit', 'offset', 'pageSize'])
                
                if not has_pagination:
                    self.info_messages.append(f"ℹ️  GET {path}: Consider adding pagination (page, limit, offset)")
    
    def _check_rate_limiting(self):
        """Check for rate limiting documentation."""
        paths = self.spec.get('paths', {})
        
        has_rate_limit_header = False
        for path_item in paths.values():
            for method in ['get', 'post', 'put', 'patch', 'delete']:
                if method in path_item:
                    responses = path_item[method].get('responses', {})
                    
                    for response in responses.values():
                        headers = response.get('headers', {})
                        if any('rate' in h.lower() for h in headers.keys()):
                            has_rate_limit_header = True
                            break
        
        if not has_rate_limit_header:
            self.info_messages.append("ℹ️  Consider documenting rate limiting (X-RateLimit-* headers)")
    
    def _check_examples(self):
        """Check for examples in schemas."""
        components = self.spec.get('components', {})
        schemas = components.get('schemas', {})
        
        schemas_with_examples = sum(1 for s in schemas.values() if 'example' in s or 'examples' in s)
        
        if schemas and schemas_with_examples == 0:
            self.warnings.append("No examples defined in component schemas (improves documentation)")
    
    def _print_results(self):
        """Print validation results."""
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60 + "\n")
        
        # Info messages
        if self.info_messages:
            for msg in self.info_messages:
                print(msg)
            print()
        
        # Errors
        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
            print()
        
        # Warnings
        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
            print()
        
        # Summary
        print("="*60)
        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("✅ VALIDATION PASSED - No issues found!")
        elif len(self.errors) == 0:
            print(f"✅ VALIDATION PASSED - {len(self.warnings)} warnings")
        else:
            print(f"❌ VALIDATION FAILED - {len(self.errors)} errors, {len(self.warnings)} warnings")
        print("="*60 + "\n")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate OpenAPI 3.0 specifications')
    parser.add_argument('spec_file', help='Path to OpenAPI spec (YAML or JSON)')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')
    
    args = parser.parse_args()
    
    validator = OpenAPIValidator(args.spec_file, strict=args.strict)
    success, error_count, warning_count = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
