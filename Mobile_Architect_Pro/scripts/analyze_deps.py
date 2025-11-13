#!/usr/bin/env python3
"""
Dependency Analyzer for Mobile Projects
Analyzes package compatibility across Flutter, React Native, Xamarin, Ionic, and Kotlin
"""

import argparse
import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PackageInfo:
    name: str
    version: str
    framework: str
    compatible: bool
    alternatives: List[str]
    notes: str


class DependencyAnalyzer:
    """Analyze dependencies for cross-platform mobile projects"""
    
    def __init__(self):
        self.framework_packages = self._load_framework_packages()
    
    def _load_framework_packages(self) -> Dict:
        """Load known package mappings"""
        return {
            'flutter': {
                'http': {'versions': ['>=0.13.0', '<2.0.0'], 'stable': True},
                'provider': {'versions': ['>=6.0.0'], 'stable': True},
                'bloc': {'versions': ['>=8.0.0'], 'stable': True},
                'dio': {'versions': ['>=5.0.0'], 'stable': True},
                'hive': {'versions': ['>=2.0.0'], 'stable': True},
                'sqflite': {'versions': ['>=2.0.0'], 'stable': True},
            },
            'react-native': {
                'axios': {'versions': ['>=1.0.0'], 'stable': True},
                '@reduxjs/toolkit': {'versions': ['>=1.9.0', '>=2.0.0'], 'stable': True},
                'react-query': {'versions': ['>=4.0.0', '>=5.0.0'], 'stable': True},
                'zustand': {'versions': ['>=4.0.0'], 'stable': True},
                '@react-navigation/native': {'versions': ['>=6.0.0'], 'stable': True},
            },
            'xamarin': {
                'Xamarin.Forms': {'versions': ['>=5.0.0'], 'stable': False, 'migrate_to': '.NET MAUI'},
                'Microsoft.Maui': {'versions': ['>=7.0.0', '>=8.0.0'], 'stable': True},
                'Prism': {'versions': ['>=8.0.0', '>=9.0.0'], 'stable': True},
                'Refit': {'versions': ['>=6.0.0', '>=7.0.0'], 'stable': True},
            },
            'ionic': {
                '@ionic/angular': {'versions': ['>=7.0.0'], 'stable': True},
                '@ionic/react': {'versions': ['>=7.0.0'], 'stable': True},
                '@ionic/vue': {'versions': ['>=7.0.0'], 'stable': True},
                '@capacitor/core': {'versions': ['>=5.0.0'], 'stable': True},
                '@capacitor/camera': {'versions': ['>=5.0.0'], 'stable': True},
            },
            'kotlin': {
                'androidx.compose.ui:ui': {'versions': ['>=1.5.0'], 'stable': True},
                'com.google.dagger:hilt-android': {'versions': ['>=2.48', '>=2.50'], 'stable': True},
                'androidx.room:room-runtime': {'versions': ['>=2.6.0'], 'stable': True},
                'com.squareup.retrofit2:retrofit': {'versions': ['>=2.9.0'], 'stable': True},
            }
        }
    
    def analyze_package(self, package_name: str, framework: str) -> PackageInfo:
        """Analyze a single package for compatibility"""
        framework_lower = framework.lower()
        
        if framework_lower not in self.framework_packages:
            return PackageInfo(
                name=package_name,
                version='unknown',
                framework=framework,
                compatible=False,
                alternatives=[],
                notes=f"Unknown framework: {framework}"
            )
        
        packages = self.framework_packages[framework_lower]
        
        if package_name in packages:
            pkg_info = packages[package_name]
            alternatives = []
            notes = ""
            
            if not pkg_info.get('stable', True):
                migrate_to = pkg_info.get('migrate_to', 'newer version')
                notes = f"⚠️  Consider migrating to {migrate_to}"
                alternatives = [migrate_to]
            
            return PackageInfo(
                name=package_name,
                version=pkg_info['versions'][-1],  # Latest version
                framework=framework,
                compatible=True,
                alternatives=alternatives,
                notes=notes
            )
        else:
            # Check for common alternatives
            alternatives = self._find_alternatives(package_name, framework_lower)
            return PackageInfo(
                name=package_name,
                version='unknown',
                framework=framework,
                compatible=False,
                alternatives=alternatives,
                notes=f"❌ Package not found for {framework}"
            )
    
    def _find_alternatives(self, package_name: str, framework: str) -> List[str]:
        """Find alternative packages"""
        alternatives_map = {
            'flutter': {
                'axios': ['dio', 'http'],
                'redux': ['bloc', 'provider', 'riverpod'],
                'express': ['shelf'],
            },
            'react-native': {
                'bloc': ['redux', 'zustand', 'mobx'],
                'provider': ['context', 'redux'],
            },
            'xamarin': {
                'flutter_bloc': ['Prism', 'MVVMCross'],
            },
            'ionic': {
                'redux': ['@ngrx/store', 'pinia', 'vuex'],
            },
            'kotlin': {
                'redux': ['ViewModel + LiveData', 'MVI'],
            }
        }
        
        return alternatives_map.get(framework, {}).get(package_name, [])
    
    def analyze_file(self, filepath: str, framework: str) -> List[PackageInfo]:
        """Analyze dependencies from file"""
        results = []
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Parse based on file type
            if filepath.endswith('pubspec.yaml'):
                packages = self._parse_pubspec(content)
            elif filepath.endswith('package.json'):
                packages = self._parse_package_json(content)
            elif filepath.endswith('.csproj'):
                packages = self._parse_csproj(content)
            elif filepath.endswith('build.gradle') or filepath.endswith('build.gradle.kts'):
                packages = self._parse_gradle(content)
            else:
                print(f"❌ Unsupported file type: {filepath}")
                return []
            
            for pkg in packages:
                result = self.analyze_package(pkg, framework)
                results.append(result)
        
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
        except Exception as e:
            print(f"❌ Error analyzing file: {e}")
        
        return results
    
    def _parse_pubspec(self, content: str) -> List[str]:
        """Parse Flutter pubspec.yaml"""
        packages = []
        in_deps = False
        
        for line in content.split('\n'):
            if line.strip().startswith('dependencies:'):
                in_deps = True
                continue
            if in_deps and line.strip() and not line.startswith('  '):
                break
            if in_deps and ':' in line:
                pkg = line.split(':')[0].strip()
                if pkg and not pkg.startswith('#'):
                    packages.append(pkg)
        
        return packages
    
    def _parse_package_json(self, content: str) -> List[str]:
        """Parse package.json"""
        try:
            data = json.loads(content)
            deps = data.get('dependencies', {})
            return list(deps.keys())
        except:
            return []
    
    def _parse_csproj(self, content: str) -> List[str]:
        """Parse .csproj file"""
        packages = []
        for line in content.split('\n'):
            if 'PackageReference Include=' in line:
                start = line.find('Include="') + 9
                end = line.find('"', start)
                if start > 8 and end > start:
                    packages.append(line[start:end])
        return packages
    
    def _parse_gradle(self, content: str) -> List[str]:
        """Parse build.gradle"""
        packages = []
        for line in content.split('\n'):
            if 'implementation(' in line or 'implementation ' in line:
                # Extract package name from implementation("group:artifact:version")
                if '"' in line:
                    start = line.find('"') + 1
                    end = line.find('"', start)
                    if start > 0 and end > start:
                        full = line[start:end]
                        # Get group:artifact part
                        parts = full.split(':')
                        if len(parts) >= 2:
                            packages.append(':'.join(parts[:2]))
        return packages
    
    def print_results(self, results: List[PackageInfo]):
        """Print analysis results"""
        print("\n" + "="*70)
        print("📦 DEPENDENCY ANALYSIS RESULTS")
        print("="*70 + "\n")
        
        compatible_count = sum(1 for r in results if r.compatible)
        total_count = len(results)
        
        print(f"Framework: {results[0].framework if results else 'Unknown'}")
        print(f"Total Packages: {total_count}")
        print(f"Compatible: {compatible_count} ✅")
        print(f"Issues: {total_count - compatible_count} ⚠️\n")
        
        print("-" * 70)
        
        for result in results:
            status = "✅" if result.compatible else "❌"
            print(f"{status} {result.name}")
            
            if result.compatible:
                print(f"   Version: {result.version}")
            else:
                print(f"   Status: Not compatible")
            
            if result.alternatives:
                print(f"   Alternatives: {', '.join(result.alternatives)}")
            
            if result.notes:
                print(f"   {result.notes}")
            
            print()
        
        print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze mobile project dependencies for compatibility'
    )
    parser.add_argument(
        'filepath',
        help='Path to dependency file (pubspec.yaml, package.json, .csproj, build.gradle)'
    )
    parser.add_argument(
        '--framework',
        choices=['flutter', 'react-native', 'xamarin', 'ionic', 'kotlin'],
        required=True,
        help='Target framework'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    analyzer = DependencyAnalyzer()
    results = analyzer.analyze_file(args.filepath, args.framework)
    
    if not results:
        print("❌ No dependencies found or file could not be parsed")
        sys.exit(1)
    
    if args.json:
        output = [
            {
                'name': r.name,
                'version': r.version,
                'framework': r.framework,
                'compatible': r.compatible,
                'alternatives': r.alternatives,
                'notes': r.notes
            }
            for r in results
        ]
        print(json.dumps(output, indent=2))
    else:
        analyzer.print_results(results)


if __name__ == '__main__':
    main()
