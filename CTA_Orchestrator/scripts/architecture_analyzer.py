#!/usr/bin/env python3
"""
Architecture Analyzer - Project complexity and architecture analysis
Analyzes project requirements to recommend appropriate architecture patterns.
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ArchitectureRecommendation:
    """Architecture recommendation result"""
    pattern: str
    confidence: float
    rationale: List[str]
    alternatives: List[str]
    warnings: List[str]


class ArchitectureAnalyzer:
    """Analyzes project requirements and recommends architecture patterns"""
    
    def __init__(self):
        self.pattern_rules = self._initialize_pattern_rules()
    
    def _initialize_pattern_rules(self) -> Dict:
        """Initialize architecture pattern decision rules"""
        return {
            'monolith': {
                'score_factors': {
                    'team_small': 30,        # Team < 5 people
                    'simple_domain': 25,     # Simple business logic
                    'mvp': 20,               # MVP or prototype
                    'tight_deadline': 15,    # < 3 months
                    'crud_heavy': 10         # Mostly CRUD operations
                },
                'max_score': 100,
                'threshold': 60
            },
            'modular_monolith': {
                'score_factors': {
                    'team_medium': 25,       # Team 5-10 people
                    'multiple_domains': 20,  # Multiple business domains
                    'growth_planned': 20,    # Planning to scale
                    'moderate_complexity': 15, # Medium complexity
                    'need_flexibility': 20   # Want flexibility without microservices
                },
                'max_score': 100,
                'threshold': 55
            },
            'microservices': {
                'score_factors': {
                    'team_large': 30,        # Team 10+ people
                    'complex_domain': 25,    # Complex business logic
                    'scale_required': 20,    # Need independent scaling
                    'multiple_tech': 10,     # Different tech stacks needed
                    'frequent_deploy': 15    # Multiple deploys per day
                },
                'max_score': 100,
                'threshold': 60
            },
            'serverless': {
                'score_factors': {
                    'variable_load': 30,     # Unpredictable traffic
                    'event_driven': 25,      # Event-driven workflows
                    'stateless': 20,         # Stateless operations
                    'quick_prototype': 15,   # Need fast time-to-market
                    'cost_sensitive': 10     # Want pay-per-use
                },
                'max_score': 100,
                'threshold': 50
            }
        }
    
    def analyze(self, requirements: str, team_size: int = 5, 
                timeline_weeks: int = 12) -> ArchitectureRecommendation:
        """
        Analyze requirements and recommend architecture.
        
        Args:
            requirements: Project requirements text
            team_size: Number of developers (default: 5)
            timeline_weeks: Project timeline in weeks (default: 12)
            
        Returns:
            ArchitectureRecommendation with pattern and rationale
        """
        req_lower = requirements.lower()
        
        # Calculate scores for each pattern
        scores = {}
        for pattern in self.pattern_rules.keys():
            scores[pattern] = self._calculate_pattern_score(
                pattern, req_lower, team_size, timeline_weeks
            )
        
        # Get recommended pattern
        recommended = max(scores, key=scores.get)
        confidence = scores[recommended] / self.pattern_rules[recommended]['max_score']
        
        # Build rationale
        rationale = self._build_rationale(recommended, req_lower, team_size, timeline_weeks)
        
        # Get alternatives
        alternatives = self._get_alternatives(scores, recommended)
        
        # Generate warnings
        warnings = self._generate_warnings(recommended, req_lower, team_size, timeline_weeks)
        
        return ArchitectureRecommendation(
            pattern=recommended,
            confidence=confidence,
            rationale=rationale,
            alternatives=alternatives,
            warnings=warnings
        )
    
    def _calculate_pattern_score(
        self, 
        pattern: str, 
        requirements: str,
        team_size: int,
        timeline_weeks: int
    ) -> float:
        """Calculate score for a specific pattern"""
        score = 0
        factors = self.pattern_rules[pattern]['score_factors']
        
        # Team size factors
        if 'team_small' in factors and team_size <= 5:
            score += factors['team_small']
        if 'team_medium' in factors and 5 < team_size <= 10:
            score += factors['team_medium']
        if 'team_large' in factors and team_size > 10:
            score += factors['team_large']
        
        # Timeline factors
        if 'tight_deadline' in factors and timeline_weeks < 12:
            score += factors['tight_deadline']
        if 'mvp' in factors and ('mvp' in requirements or 'prototype' in requirements):
            score += factors['mvp']
        if 'quick_prototype' in factors and timeline_weeks < 8:
            score += factors['quick_prototype']
        
        # Complexity factors
        complexity_keywords = ['complex', 'sophisticated', 'advanced', 'enterprise']
        is_complex = any(kw in requirements for kw in complexity_keywords)
        
        if 'simple_domain' in factors and not is_complex:
            score += factors['simple_domain']
        if 'moderate_complexity' in factors and is_complex:
            score += factors['moderate_complexity'] * 0.5
        if 'complex_domain' in factors and is_complex:
            score += factors['complex_domain']
        
        # CRUD detection
        crud_keywords = ['crud', 'create', 'read', 'update', 'delete', 'form']
        crud_count = sum(1 for kw in crud_keywords if kw in requirements)
        if 'crud_heavy' in factors and crud_count >= 3:
            score += factors['crud_heavy']
        
        # Scalability factors
        scale_keywords = ['scale', 'scalability', 'high traffic', 'load', 'millions']
        needs_scale = any(kw in requirements for kw in scale_keywords)
        
        if 'scale_required' in factors and needs_scale:
            score += factors['scale_required']
        
        # Event-driven detection
        event_keywords = ['event', 'queue', 'async', 'message', 'pub/sub']
        is_event_driven = any(kw in requirements for kw in event_keywords)
        
        if 'event_driven' in factors and is_event_driven:
            score += factors['event_driven']
        
        # Variable load detection
        variable_keywords = ['variable', 'unpredictable', 'spike', 'burst']
        has_variable_load = any(kw in requirements for kw in variable_keywords)
        
        if 'variable_load' in factors and has_variable_load:
            score += factors['variable_load']
        
        # Stateless detection
        if 'stateless' in factors and 'stateless' in requirements:
            score += factors['stateless']
        
        # Multiple domains detection
        domain_keywords = ['module', 'service', 'component', 'domain']
        domain_count = sum(1 for kw in domain_keywords if kw in requirements)
        
        if 'multiple_domains' in factors and domain_count >= 3:
            score += factors['multiple_domains']
        
        # Growth planning
        growth_keywords = ['growth', 'expand', 'future', 'scalable']
        plans_growth = any(kw in requirements for kw in growth_keywords)
        
        if 'growth_planned' in factors and plans_growth:
            score += factors['growth_planned']
        
        # Multiple tech stacks
        tech_keywords = ['python', 'node', 'java', 'go', 'rust']
        tech_count = sum(1 for kw in tech_keywords if kw in requirements)
        
        if 'multiple_tech' in factors and tech_count >= 2:
            score += factors['multiple_tech']
        
        # Frequent deployment
        deploy_keywords = ['continuous', 'ci/cd', 'frequent deploy', 'multiple per day']
        frequent_deploy = any(kw in requirements for kw in deploy_keywords)
        
        if 'frequent_deploy' in factors and frequent_deploy:
            score += factors['frequent_deploy']
        
        return score
    
    def _build_rationale(
        self,
        pattern: str,
        requirements: str,
        team_size: int,
        timeline_weeks: int
    ) -> List[str]:
        """Build human-readable rationale for recommendation"""
        rationale = []
        
        if pattern == 'monolith':
            rationale.append(f"Team size ({team_size}) is well-suited for monolithic architecture")
            if timeline_weeks < 12:
                rationale.append(f"Timeline ({timeline_weeks} weeks) favors simple architecture")
            if 'crud' in requirements.lower():
                rationale.append("CRUD-heavy application works well as monolith")
            rationale.append("Lower operational complexity compared to distributed systems")
            
        elif pattern == 'modular_monolith':
            rationale.append("Provides good balance between simplicity and flexibility")
            rationale.append(f"Team size ({team_size}) can manage modular structure")
            rationale.append("Easier to extract microservices later if needed")
            if 'growth' in requirements.lower():
                rationale.append("Good foundation for future growth")
                
        elif pattern == 'microservices':
            rationale.append(f"Large team ({team_size}) can work independently on services")
            if 'scale' in requirements.lower():
                rationale.append("Enables independent scaling of components")
            if 'complex' in requirements.lower():
                rationale.append("Complex domain benefits from service boundaries")
            rationale.append("Allows technology diversity per service")
            
        elif pattern == 'serverless':
            if 'variable' in requirements.lower() or 'spike' in requirements.lower():
                rationale.append("Variable load pattern fits serverless model")
            if 'event' in requirements.lower():
                rationale.append("Event-driven architecture aligns with serverless")
            rationale.append("Pay-per-use pricing can reduce costs")
            rationale.append("Zero infrastructure management")
        
        return rationale
    
    def _get_alternatives(self, scores: Dict[str, float], recommended: str) -> List[str]:
        """Get alternative architecture patterns"""
        sorted_patterns = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        alternatives = []
        
        for pattern, score in sorted_patterns[1:]:
            threshold = self.pattern_rules[pattern]['threshold']
            if score >= threshold * 0.7:  # At least 70% of threshold
                alternatives.append(pattern)
        
        return alternatives[:2]  # Return top 2 alternatives
    
    def _generate_warnings(
        self,
        pattern: str,
        requirements: str,
        team_size: int,
        timeline_weeks: int
    ) -> List[str]:
        """Generate warnings about potential issues"""
        warnings = []
        
        if pattern == 'monolith':
            if team_size > 8:
                warnings.append("Large team may face coordination issues with monolith")
            if 'scale' in requirements:
                warnings.append("Monolith may struggle with scaling requirements")
                
        elif pattern == 'modular_monolith':
            warnings.append("Requires discipline to maintain module boundaries")
            if team_size < 5:
                warnings.append("May be over-engineering for small team")
                
        elif pattern == 'microservices':
            if team_size < 10:
                warnings.append("Small team may struggle with microservices complexity")
            if timeline_weeks < 16:
                warnings.append("Tight timeline makes microservices risky")
            warnings.append("High operational overhead (monitoring, deployment)")
            warnings.append("Eventual consistency and distributed transaction challenges")
            
        elif pattern == 'serverless':
            warnings.append("Cold start latency may affect user experience")
            warnings.append("Vendor lock-in risk")
            if 'stateful' in requirements:
                warnings.append("Stateful applications challenging in serverless")
        
        return warnings
    
    def estimate_complexity_metrics(self, requirements: str) -> Dict:
        """
        Estimate various complexity metrics.
        
        Returns:
            Dict with complexity scores (0-100)
        """
        req_lower = requirements.lower()
        
        # Domain complexity
        domain_keywords = ['complex', 'sophisticated', 'enterprise', 'advanced']
        domain_score = min(100, sum(20 for kw in domain_keywords if kw in req_lower))
        
        # Technical complexity
        tech_keywords = ['microservices', 'distributed', 'real-time', 'high-availability']
        tech_score = min(100, sum(25 for kw in tech_keywords if kw in req_lower))
        
        # Integration complexity
        integration_keywords = ['integration', 'third-party', 'api', 'webhook']
        integration_score = min(100, sum(15 for kw in integration_keywords if kw in req_lower))
        
        # Data complexity
        data_keywords = ['big data', 'analytics', 'etl', 'warehouse', 'petabyte']
        data_score = min(100, sum(20 for kw in data_keywords if kw in req_lower))
        
        # Overall complexity (weighted average)
        overall = (
            domain_score * 0.3 +
            tech_score * 0.3 +
            integration_score * 0.2 +
            data_score * 0.2
        )
        
        return {
            'domain_complexity': domain_score,
            'technical_complexity': tech_score,
            'integration_complexity': integration_score,
            'data_complexity': data_score,
            'overall_complexity': overall
        }


def main():
    """Example usage"""
    analyzer = ArchitectureAnalyzer()
    
    # Example 1: Simple CRUD app
    print("=" * 70)
    print("Example 1: Simple CRUD Blog App")
    print("=" * 70)
    
    req1 = """
    Build a simple blog platform where users can create, read, update, 
    and delete blog posts. Basic authentication required.
    """
    
    result1 = analyzer.analyze(req1, team_size=3, timeline_weeks=8)
    print(f"Recommended: {result1.pattern}")
    print(f"Confidence: {result1.confidence:.1%}")
    print("\nRationale:")
    for r in result1.rationale:
        print(f"  - {r}")
    print(f"\nAlternatives: {', '.join(result1.alternatives)}")
    if result1.warnings:
        print("\nWarnings:")
        for w in result1.warnings:
            print(f"  ⚠️  {w}")
    
    # Example 2: Complex enterprise system
    print("\n" + "=" * 70)
    print("Example 2: Complex E-commerce Platform")
    print("=" * 70)
    
    req2 = """
    Build a sophisticated e-commerce platform with:
    - Product catalog with millions of SKUs
    - Real-time inventory management across multiple warehouses
    - Recommendation engine using ML
    - High-availability requirements (99.99%)
    - Multiple payment gateways integration
    - Microservices architecture preferred
    - Team of 15 developers
    - Need to scale to handle Black Friday traffic spikes
    """
    
    result2 = analyzer.analyze(req2, team_size=15, timeline_weeks=24)
    print(f"Recommended: {result2.pattern}")
    print(f"Confidence: {result2.confidence:.1%}")
    print("\nRationale:")
    for r in result2.rationale:
        print(f"  - {r}")
    print(f"\nAlternatives: {', '.join(result2.alternatives)}")
    if result2.warnings:
        print("\nWarnings:")
        for w in result2.warnings:
            print(f"  ⚠️  {w}")
    
    # Complexity metrics
    print("\nComplexity Metrics:")
    metrics = analyzer.estimate_complexity_metrics(req2)
    for metric, score in metrics.items():
        print(f"  {metric}: {score:.0f}/100")
    
    # Example 3: Event-driven serverless
    print("\n" + "=" * 70)
    print("Example 3: Image Processing Service")
    print("=" * 70)
    
    req3 = """
    Build an image processing service that:
    - Receives images via webhook from various sources
    - Processes images (resize, compress, watermark)
    - Stores in S3
    - Unpredictable traffic with occasional spikes
    - Event-driven architecture
    - Stateless operations
    - Cost-sensitive startup project
    """
    
    result3 = analyzer.analyze(req3, team_size=2, timeline_weeks=6)
    print(f"Recommended: {result3.pattern}")
    print(f"Confidence: {result3.confidence:.1%}")
    print("\nRationale:")
    for r in result3.rationale:
        print(f"  - {r}")
    print(f"\nAlternatives: {', '.join(result3.alternatives)}")
    if result3.warnings:
        print("\nWarnings:")
        for w in result3.warnings:
            print(f"  ⚠️  {w}")


if __name__ == "__main__":
    main()
