#!/usr/bin/env python3
"""
Kubernetes Security Audit

Audits Kubernetes cluster for security misconfigurations and generates
a report with remediation steps.

Usage:
    python security_audit.py <cluster_context>
    python security_audit.py production-cluster
    
    # Use current context
    python security_audit.py
"""

import sys
import subprocess
import json
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class SecurityIssue:
    severity: str  # critical, high, medium, low
    category: str
    resource: str
    issue: str
    remediation: str

class SecurityAuditor:
    def __init__(self, context: str = None):
        self.context = context
        self.issues = []
        
    def audit(self) -> List[SecurityIssue]:
        """Run security audit"""
        print("🔒 Running Kubernetes Security Audit")
        print("=" * 60)
        
        if self.context:
            print(f"Context: {self.context}\n")
            self.set_context()
        else:
            print("Using current kubectl context\n")
        
        self.check_rbac()
        self.check_network_policies()
        self.check_pod_security()
        self.check_secrets()
        self.check_image_policies()
        self.check_resource_limits()
        self.check_ingress_security()
        
        self.print_report()
        
        return self.issues
    
    def set_context(self):
        """Set kubectl context"""
        try:
            subprocess.run(
                ['kubectl', 'config', 'use-context', self.context],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            print(f"❌ Failed to set context: {self.context}")
            sys.exit(1)
    
    def kubectl(self, args: List[str]) -> Dict[str, Any]:
        """Run kubectl command and return JSON output"""
        try:
            result = subprocess.run(
                ['kubectl'] + args + ['-o', 'json'],
                check=True,
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Warning: kubectl command failed: {' '.join(args)}")
            return {}
        except json.JSONDecodeError:
            return {}
    
    def check_rbac(self):
        """Check RBAC configuration"""
        print("Checking RBAC...")
        
        # Check for overly permissive ClusterRoleBindings
        crb = self.kubectl(['get', 'clusterrolebindings'])
        
        if crb and 'items' in crb:
            for binding in crb['items']:
                name = binding['metadata']['name']
                role_ref = binding.get('roleRef', {})
                subjects = binding.get('subjects', [])
                
                # Check for cluster-admin bindings
                if role_ref.get('name') == 'cluster-admin':
                    for subject in subjects:
                        if subject.get('kind') == 'ServiceAccount':
                            self.add_issue(
                                'high',
                                'RBAC',
                                f"ClusterRoleBinding/{name}",
                                f"ServiceAccount has cluster-admin privileges",
                                "Review and scope down permissions to least privilege"
                            )
                        elif subject.get('name') == 'system:unauthenticated':
                            self.add_issue(
                                'critical',
                                'RBAC',
                                f"ClusterRoleBinding/{name}",
                                "Unauthenticated users have cluster-admin",
                                "Remove unauthenticated subjects immediately"
                            )
    
    def check_network_policies(self):
        """Check NetworkPolicy configuration"""
        print("Checking Network Policies...")
        
        namespaces = self.kubectl(['get', 'namespaces'])
        
        if namespaces and 'items' in namespaces:
            for ns in namespaces['items']:
                ns_name = ns['metadata']['name']
                
                # Skip system namespaces
                if ns_name.startswith('kube-'):
                    continue
                
                # Check if namespace has NetworkPolicies
                netpol = self.kubectl(['get', 'networkpolicies', '-n', ns_name])
                
                if not netpol.get('items'):
                    self.add_issue(
                        'medium',
                        'Network',
                        f"Namespace/{ns_name}",
                        "No NetworkPolicies defined",
                        "Implement default-deny NetworkPolicy and allow specific traffic"
                    )
    
    def check_pod_security(self):
        """Check Pod Security Standards"""
        print("Checking Pod Security...")
        
        pods = self.kubectl(['get', 'pods', '--all-namespaces'])
        
        if pods and 'items' in pods:
            for pod in pods['items']:
                name = pod['metadata']['name']
                namespace = pod['metadata']['namespace']
                spec = pod.get('spec', {})
                
                # Check securityContext
                pod_security = spec.get('securityContext', {})
                
                # Check if running as root
                if not pod_security.get('runAsNonRoot'):
                    containers = spec.get('containers', [])
                    for container in containers:
                        container_security = container.get('securityContext', {})
                        if not container_security.get('runAsNonRoot'):
                            self.add_issue(
                                'high',
                                'Pod Security',
                                f"Pod/{namespace}/{name}",
                                "Container may run as root",
                                "Set securityContext.runAsNonRoot: true"
                            )
                            break
                
                # Check privileged containers
                for container in spec.get('containers', []):
                    container_security = container.get('securityContext', {})
                    if container_security.get('privileged'):
                        self.add_issue(
                            'critical',
                            'Pod Security',
                            f"Pod/{namespace}/{name}",
                            f"Container '{container['name']}' runs in privileged mode",
                            "Remove privileged: true unless absolutely necessary"
                        )
                    
                    # Check capabilities
                    capabilities = container_security.get('capabilities', {})
                    if capabilities.get('add'):
                        self.add_issue(
                            'medium',
                            'Pod Security',
                            f"Pod/{namespace}/{name}",
                            f"Container adds capabilities: {capabilities['add']}",
                            "Review if capabilities are necessary"
                        )
    
    def check_secrets(self):
        """Check Secrets configuration"""
        print("Checking Secrets...")
        
        secrets = self.kubectl(['get', 'secrets', '--all-namespaces'])
        
        if secrets and 'items' in secrets:
            for secret in secrets['items']:
                name = secret['metadata']['name']
                namespace = secret['metadata']['namespace']
                secret_type = secret.get('type', '')
                
                # Check for unencrypted secrets in etcd
                # Note: This check is limited - proper check requires etcd access
                self.add_issue(
                    'low',
                    'Secrets',
                    f"Cluster-wide",
                    "Verify secrets are encrypted at rest in etcd",
                    "Enable encryption at rest: https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/"
                )
                break  # Only add once
    
    def check_image_policies(self):
        """Check container image policies"""
        print("Checking Image Policies...")
        
        pods = self.kubectl(['get', 'pods', '--all-namespaces'])
        
        if pods and 'items' in pods:
            for pod in pods['items']:
                name = pod['metadata']['name']
                namespace = pod['metadata']['namespace']
                
                for container in pod['spec'].get('containers', []):
                    image = container.get('image', '')
                    
                    # Check for latest tag
                    if image.endswith(':latest') or ':' not in image:
                        self.add_issue(
                            'medium',
                            'Image Policy',
                            f"Pod/{namespace}/{name}",
                            f"Container uses 'latest' or no tag: {image}",
                            "Use specific version tags for reproducibility"
                        )
                    
                    # Check for private registry
                    if not any(registry in image for registry in ['gcr.io', 'docker.io', 'quay.io', 'ghcr.io']):
                        # Might be using imagePullSecrets
                        if not pod['spec'].get('imagePullSecrets'):
                            self.add_issue(
                                'low',
                                'Image Policy',
                                f"Pod/{namespace}/{name}",
                                "Private registry without imagePullSecrets",
                                "Add imagePullSecrets if using private registry"
                            )
    
    def check_resource_limits(self):
        """Check resource limits and requests"""
        print("Checking Resource Limits...")
        
        pods = self.kubectl(['get', 'pods', '--all-namespaces'])
        
        if pods and 'items' in pods:
            for pod in pods['items']:
                name = pod['metadata']['name']
                namespace = pod['metadata']['namespace']
                
                for container in pod['spec'].get('containers', []):
                    resources = container.get('resources', {})
                    
                    if not resources.get('limits'):
                        self.add_issue(
                            'medium',
                            'Resource Management',
                            f"Pod/{namespace}/{name}",
                            f"Container '{container['name']}' has no resource limits",
                            "Set resources.limits to prevent resource exhaustion"
                        )
                    
                    if not resources.get('requests'):
                        self.add_issue(
                            'low',
                            'Resource Management',
                            f"Pod/{namespace}/{name}",
                            f"Container '{container['name']}' has no resource requests",
                            "Set resources.requests for proper scheduling"
                        )
    
    def check_ingress_security(self):
        """Check Ingress security configuration"""
        print("Checking Ingress Security...")
        
        ingresses = self.kubectl(['get', 'ingress', '--all-namespaces'])
        
        if ingresses and 'items' in ingresses:
            for ingress in ingresses['items']:
                name = ingress['metadata']['name']
                namespace = ingress['metadata']['namespace']
                spec = ingress.get('spec', {})
                
                # Check for TLS
                if not spec.get('tls'):
                    self.add_issue(
                        'high',
                        'Ingress Security',
                        f"Ingress/{namespace}/{name}",
                        "Ingress does not use TLS",
                        "Add TLS configuration with valid certificates"
                    )
    
    def add_issue(self, severity: str, category: str, resource: str, 
                  issue: str, remediation: str):
        """Add security issue"""
        self.issues.append(SecurityIssue(
            severity=severity,
            category=category,
            resource=resource,
            issue=issue,
            remediation=remediation
        ))
    
    def print_report(self):
        """Print security audit report"""
        print("\n" + "=" * 60)
        print("📋 SECURITY AUDIT REPORT")
        print("=" * 60)
        
        if not self.issues:
            print("\n✅ No security issues found!")
            print("=" * 60)
            return
        
        # Group by severity
        by_severity = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        for issue in self.issues:
            by_severity[issue.severity].append(issue)
        
        # Print issues by severity
        severity_symbols = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🔵'
        }
        
        for severity in ['critical', 'high', 'medium', 'low']:
            issues = by_severity[severity]
            if not issues:
                continue
            
            print(f"\n{severity_symbols[severity]} {severity.upper()} ({len(issues)}):")
            print("-" * 60)
            
            for issue in issues:
                print(f"\nCategory: {issue.category}")
                print(f"Resource: {issue.resource}")
                print(f"Issue: {issue.issue}")
                print(f"Remediation: {issue.remediation}")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        total = len(self.issues)
        print(f"Total Issues: {total}")
        for severity in ['critical', 'high', 'medium', 'low']:
            count = len(by_severity[severity])
            if count > 0:
                print(f"  {severity_symbols[severity]} {severity.capitalize()}: {count}")
        
        print("\n" + "=" * 60)
        print()


def main():
    context = sys.argv[1] if len(sys.argv) > 1 else None
    
    auditor = SecurityAuditor(context)
    issues = auditor.audit()
    
    # Exit with error if critical or high severity issues found
    critical_or_high = sum(
        1 for issue in issues 
        if issue.severity in ['critical', 'high']
    )
    
    sys.exit(1 if critical_or_high > 0 else 0)


if __name__ == '__main__':
    main()
