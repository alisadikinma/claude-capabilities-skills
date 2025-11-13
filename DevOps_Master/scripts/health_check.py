#!/usr/bin/env python3
"""
Kubernetes Application Health Check

Performs comprehensive health check for deployed applications including
pods, services, ingress, and dependencies.

Usage:
    python health_check.py <namespace>
    python health_check.py production
    
    # Check all namespaces
    python health_check.py --all
"""

import sys
import subprocess
import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HealthCheckResult:
    component: str
    status: str  # healthy, warning, unhealthy
    message: str
    details: str = ""

class HealthChecker:
    def __init__(self, namespace: str = None, check_all: bool = False):
        self.namespace = namespace
        self.check_all = check_all
        self.results = []
        
    def check(self) -> List[HealthCheckResult]:
        """Run health checks"""
        print("🏥 Kubernetes Application Health Check")
        print("=" * 60)
        
        if self.check_all:
            print("Checking all namespaces\n")
            namespaces = self.get_namespaces()
            for ns in namespaces:
                if not ns.startswith('kube-'):  # Skip system namespaces
                    print(f"\n📦 Namespace: {ns}")
                    print("-" * 60)
                    self.namespace = ns
                    self.run_checks()
        else:
            print(f"Namespace: {self.namespace}\n")
            self.run_checks()
        
        self.print_report()
        
        return self.results
    
    def run_checks(self):
        """Run all health checks for namespace"""
        self.check_pods()
        self.check_deployments()
        self.check_services()
        self.check_ingress()
        self.check_pvcs()
        self.check_configmaps_secrets()
    
    def kubectl(self, args: List[str]) -> Dict[str, Any]:
        """Run kubectl command and return JSON output"""
        try:
            cmd = ['kubectl'] + args
            if self.namespace and '--all-namespaces' not in args:
                cmd += ['-n', self.namespace]
            cmd += ['-o', 'json']
            
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def get_namespaces(self) -> List[str]:
        """Get all namespaces"""
        result = self.kubectl(['get', 'namespaces'])
        if result and 'items' in result:
            return [ns['metadata']['name'] for ns in result['items']]
        return []
    
    def check_pods(self):
        """Check pod health"""
        pods = self.kubectl(['get', 'pods'])
        
        if not pods or 'items' not in pods:
            self.add_result(
                'Pods',
                'warning',
                'No pods found in namespace'
            )
            return
        
        total_pods = len(pods['items'])
        running_pods = 0
        pending_pods = 0
        failed_pods = 0
        crashloop_pods = []
        
        for pod in pods['items']:
            name = pod['metadata']['name']
            phase = pod['status'].get('phase', 'Unknown')
            
            if phase == 'Running':
                running_pods += 1
                
                # Check container statuses
                container_statuses = pod['status'].get('containerStatuses', [])
                for container in container_statuses:
                    if not container.get('ready', False):
                        state = container.get('state', {})
                        if 'waiting' in state:
                            reason = state['waiting'].get('reason', '')
                            if reason == 'CrashLoopBackOff':
                                crashloop_pods.append(name)
            elif phase == 'Pending':
                pending_pods += 1
            elif phase == 'Failed':
                failed_pods += 1
        
        # Evaluate overall pod health
        if failed_pods > 0 or crashloop_pods:
            self.add_result(
                'Pods',
                'unhealthy',
                f"{running_pods}/{total_pods} running, {failed_pods} failed",
                f"Failed pods: {failed_pods}, CrashLoopBackOff: {crashloop_pods}"
            )
        elif pending_pods > 0:
            self.add_result(
                'Pods',
                'warning',
                f"{running_pods}/{total_pods} running, {pending_pods} pending"
            )
        else:
            self.add_result(
                'Pods',
                'healthy',
                f"{running_pods}/{total_pods} running"
            )
    
    def check_deployments(self):
        """Check deployment health"""
        deployments = self.kubectl(['get', 'deployments'])
        
        if not deployments or 'items' not in deployments:
            return
        
        for deployment in deployments['items']:
            name = deployment['metadata']['name']
            spec = deployment.get('spec', {})
            status = deployment.get('status', {})
            
            desired = spec.get('replicas', 0)
            ready = status.get('readyReplicas', 0)
            available = status.get('availableReplicas', 0)
            
            if ready == desired and available == desired:
                self.add_result(
                    f"Deployment/{name}",
                    'healthy',
                    f"{ready}/{desired} replicas ready"
                )
            elif ready == 0:
                self.add_result(
                    f"Deployment/{name}",
                    'unhealthy',
                    f"No replicas ready ({ready}/{desired})"
                )
            else:
                self.add_result(
                    f"Deployment/{name}",
                    'warning',
                    f"Partial deployment ({ready}/{desired} ready)"
                )
    
    def check_services(self):
        """Check service health"""
        services = self.kubectl(['get', 'services'])
        
        if not services or 'items' not in services:
            return
        
        for service in services['items']:
            name = service['metadata']['name']
            spec = service.get('spec', {})
            
            # Check if service has endpoints
            endpoints = self.kubectl(['get', 'endpoints', name])
            
            if endpoints and 'subsets' in endpoints:
                subsets = endpoints.get('subsets', [])
                if subsets and any(s.get('addresses') for s in subsets):
                    endpoint_count = sum(
                        len(s.get('addresses', [])) 
                        for s in subsets
                    )
                    self.add_result(
                        f"Service/{name}",
                        'healthy',
                        f"{endpoint_count} endpoint(s) available"
                    )
                else:
                    self.add_result(
                        f"Service/{name}",
                        'warning',
                        "No endpoints available"
                    )
            else:
                # External service (no endpoints)
                if spec.get('type') == 'ExternalName':
                    self.add_result(
                        f"Service/{name}",
                        'healthy',
                        "ExternalName service"
                    )
    
    def check_ingress(self):
        """Check ingress health"""
        ingresses = self.kubectl(['get', 'ingress'])
        
        if not ingresses or 'items' not in ingresses:
            return
        
        for ingress in ingresses['items']:
            name = ingress['metadata']['name']
            status = ingress.get('status', {})
            
            # Check if ingress has load balancer
            lb = status.get('loadBalancer', {})
            ingress_ips = lb.get('ingress', [])
            
            if ingress_ips:
                ip_or_host = ingress_ips[0].get('ip') or ingress_ips[0].get('hostname')
                self.add_result(
                    f"Ingress/{name}",
                    'healthy',
                    f"Load balancer: {ip_or_host}"
                )
            else:
                self.add_result(
                    f"Ingress/{name}",
                    'warning',
                    "No load balancer assigned"
                )
    
    def check_pvcs(self):
        """Check PersistentVolumeClaim health"""
        pvcs = self.kubectl(['get', 'persistentvolumeclaims'])
        
        if not pvcs or 'items' not in pvcs:
            return
        
        for pvc in pvcs['items']:
            name = pvc['metadata']['name']
            status = pvc.get('status', {})
            phase = status.get('phase', 'Unknown')
            
            if phase == 'Bound':
                capacity = status.get('capacity', {}).get('storage', 'Unknown')
                self.add_result(
                    f"PVC/{name}",
                    'healthy',
                    f"Bound ({capacity})"
                )
            elif phase == 'Pending':
                self.add_result(
                    f"PVC/{name}",
                    'warning',
                    "Pending binding"
                )
            else:
                self.add_result(
                    f"PVC/{name}",
                    'unhealthy',
                    f"Status: {phase}"
                )
    
    def check_configmaps_secrets(self):
        """Check ConfigMaps and Secrets"""
        # ConfigMaps
        configmaps = self.kubectl(['get', 'configmaps'])
        if configmaps and 'items' in configmaps:
            count = len(configmaps['items'])
            self.add_result(
                'ConfigMaps',
                'healthy',
                f"{count} ConfigMap(s)"
            )
        
        # Secrets
        secrets = self.kubectl(['get', 'secrets'])
        if secrets and 'items' in secrets:
            # Filter out service account tokens
            app_secrets = [
                s for s in secrets['items']
                if s.get('type') != 'kubernetes.io/service-account-token'
            ]
            count = len(app_secrets)
            self.add_result(
                'Secrets',
                'healthy',
                f"{count} Secret(s)"
            )
    
    def add_result(self, component: str, status: str, message: str, details: str = ""):
        """Add health check result"""
        self.results.append(HealthCheckResult(
            component=component,
            status=status,
            message=message,
            details=details
        ))
    
    def print_report(self):
        """Print health check report"""
        print("\n" + "=" * 60)
        print("📊 HEALTH CHECK REPORT")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.results:
            print("\n⚠️  No components found")
            print("=" * 60)
            return
        
        # Group by status
        by_status = {
            'healthy': [],
            'warning': [],
            'unhealthy': []
        }
        
        for result in self.results:
            by_status[result.status].append(result)
        
        # Print results
        status_symbols = {
            'healthy': '✅',
            'warning': '⚠️',
            'unhealthy': '❌'
        }
        
        for status in ['healthy', 'warning', 'unhealthy']:
            results = by_status[status]
            if not results:
                continue
            
            print(f"\n{status_symbols[status]} {status.upper()} ({len(results)}):")
            print("-" * 60)
            
            for result in results:
                print(f"\n{result.component}: {result.message}")
                if result.details:
                    print(f"  Details: {result.details}")
        
        # Summary
        print("\n" + "=" * 60)
        print("📈 SUMMARY")
        print("=" * 60)
        total = len(self.results)
        print(f"Total Components: {total}")
        for status in ['healthy', 'warning', 'unhealthy']:
            count = len(by_status[status])
            if count > 0:
                percentage = (count / total) * 100
                print(f"  {status_symbols[status]} {status.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Overall health score
        healthy_count = len(by_status['healthy'])
        health_score = (healthy_count / total) * 100 if total > 0 else 0
        
        print(f"\n🎯 Overall Health Score: {health_score:.1f}%")
        
        if health_score == 100:
            print("Status: 🟢 Excellent")
        elif health_score >= 80:
            print("Status: 🟡 Good")
        elif health_score >= 60:
            print("Status: 🟠 Fair")
        else:
            print("Status: 🔴 Poor")
        
        print("=" * 60)
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python health_check.py <namespace>")
        print("       python health_check.py --all")
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        checker = HealthChecker(check_all=True)
    else:
        namespace = sys.argv[1]
        checker = HealthChecker(namespace=namespace)
    
    results = checker.check()
    
    # Exit with error if any unhealthy components
    unhealthy = sum(1 for r in results if r.status == 'unhealthy')
    
    sys.exit(1 if unhealthy > 0 else 0)


if __name__ == '__main__':
    main()
