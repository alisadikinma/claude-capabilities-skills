#!/usr/bin/env python3
"""
Skill Router - Automated skill selection and delegation
Analyzes project requirements and routes to appropriate technical skills.
"""

import re
from typing import List, Dict, Set
from enum import Enum


class Skill(Enum):
    """Available technical skills"""
    CTA_ORCHESTRATOR = "CTA_Orchestrator"
    WEB_ARCHITECT = "Web_Architect_Pro"
    MOBILE_ARCHITECT = "Mobile_Architect_Pro"
    AI_ENGINEER = "AI_Engineer_Pro"
    DEVOPS_MASTER = "DevOps_Master"
    SYSTEM_ANALYST = "System_Analyst_Expert"


class SkillRouter:
    """Routes project requirements to appropriate skills"""
    
    def __init__(self):
        self.skill_keywords = {
            Skill.WEB_ARCHITECT: {
                'web', 'frontend', 'backend', 'api', 'rest', 'graphql',
                'next.js', 'react', 'vue', 'laravel', 'django', 'fastapi',
                'express', 'node', 'spa', 'ssr', 'website', 'webapp'
            },
            Skill.MOBILE_ARCHITECT: {
                'mobile', 'app', 'ios', 'android', 'flutter', 'react native',
                'kotlin', 'swift', 'crossplatform', 'native'
            },
            Skill.AI_ENGINEER: {
                'ai', 'ml', 'machine learning', 'deep learning', 'neural',
                'pytorch', 'tensorflow', 'model', 'inference', 'training',
                'computer vision', 'nlp', 'cv', 'llm', 'embedding', 'prediction'
            },
            Skill.DEVOPS_MASTER: {
                'devops', 'deploy', 'deployment', 'ci/cd', 'docker', 'kubernetes',
                'k8s', 'infrastructure', 'cloud', 'aws', 'gcp', 'azure',
                'terraform', 'ansible', 'monitoring', 'prometheus', 'grafana'
            },
            Skill.SYSTEM_ANALYST: {
                'requirements', 'specification', 'fsd', 'functional', 'use case',
                'documentation', 'analysis', 'business logic', 'workflow'
            }
        }
    
    def analyze_requirements(self, requirements: str) -> Dict:
        """
        Analyze project requirements and determine which skills are needed.
        
        Args:
            requirements: Project requirements text
            
        Returns:
            Dict with analysis results
        """
        requirements_lower = requirements.lower()
        
        # Detect skills needed
        skills_needed = self._detect_skills(requirements_lower)
        
        # Determine complexity
        complexity = self._assess_complexity(requirements, skills_needed)
        
        # Check if CTA_Orchestrator is needed
        needs_orchestrator = len(skills_needed) >= 2
        
        # Build execution plan
        execution_plan = self._build_execution_plan(
            skills_needed, 
            needs_orchestrator,
            requirements_lower
        )
        
        return {
            'skills_needed': [skill.value for skill in skills_needed],
            'complexity': complexity,
            'needs_orchestrator': needs_orchestrator,
            'execution_plan': execution_plan,
            'estimated_duration': self._estimate_duration(complexity, len(skills_needed))
        }
    
    def _detect_skills(self, requirements: str) -> Set[Skill]:
        """Detect which skills are needed based on keywords"""
        skills_needed = set()
        
        for skill, keywords in self.skill_keywords.items():
            if any(keyword in requirements for keyword in keywords):
                skills_needed.add(skill)
        
        return skills_needed
    
    def _assess_complexity(self, requirements: str, skills_needed: Set[Skill]) -> str:
        """
        Assess project complexity based on multiple factors.
        
        Returns: 'simple', 'medium', 'complex', or 'very_complex'
        """
        score = 0
        
        # Factor 1: Number of skills needed
        score += len(skills_needed) * 10
        
        # Factor 2: Keywords indicating complexity
        complexity_keywords = {
            'microservices': 20,
            'distributed': 15,
            'real-time': 10,
            'scalability': 10,
            'high availability': 15,
            'multi-tenant': 10,
            'integration': 5,
            'migration': 10,
            'enterprise': 15,
            'complex': 10
        }
        
        for keyword, points in complexity_keywords.items():
            if keyword in requirements.lower():
                score += points
        
        # Factor 3: Feature count (rough estimate)
        feature_indicators = len(re.findall(r'\b(feature|functionality|module|component)\b', 
                                           requirements.lower()))
        score += feature_indicators * 3
        
        # Determine complexity level
        if score < 20:
            return 'simple'
        elif score < 50:
            return 'medium'
        elif score < 80:
            return 'complex'
        else:
            return 'very_complex'
    
    def _build_execution_plan(
        self, 
        skills_needed: Set[Skill],
        needs_orchestrator: bool,
        requirements: str
    ) -> List[Dict]:
        """Build step-by-step execution plan"""
        plan = []
        
        # Step 1: Always start with System Analyst if complex enough
        if len(skills_needed) >= 2 or 'requirement' in requirements:
            plan.append({
                'step': 1,
                'skill': Skill.SYSTEM_ANALYST.value,
                'action': 'Define functional requirements and use cases',
                'output': 'Functional Specification Document (FSD)'
            })
        
        # Step 2: CTA Orchestrator if multiple skills
        if needs_orchestrator:
            plan.append({
                'step': len(plan) + 1,
                'skill': Skill.CTA_ORCHESTRATOR.value,
                'action': 'Define system architecture and tech stack',
                'output': 'Architecture diagram, technology recommendations'
            })
        
        # Step 3: Individual skills in logical order
        skill_order = [
            Skill.WEB_ARCHITECT,
            Skill.MOBILE_ARCHITECT,
            Skill.AI_ENGINEER,
            Skill.DEVOPS_MASTER
        ]
        
        for skill in skill_order:
            if skill in skills_needed:
                action, output = self._get_skill_action_output(skill, requirements)
                plan.append({
                    'step': len(plan) + 1,
                    'skill': skill.value,
                    'action': action,
                    'output': output
                })
        
        return plan
    
    def _get_skill_action_output(self, skill: Skill, requirements: str) -> tuple:
        """Get appropriate action and output for each skill"""
        actions = {
            Skill.WEB_ARCHITECT: (
                'Design web application architecture (frontend + backend)',
                'API schema, database design, component structure'
            ),
            Skill.MOBILE_ARCHITECT: (
                'Design mobile application architecture',
                'App structure, state management, data flow'
            ),
            Skill.AI_ENGINEER: (
                'Design ML pipeline and model architecture',
                'Model specs, inference pipeline, training strategy'
            ),
            Skill.DEVOPS_MASTER: (
                'Setup deployment infrastructure and CI/CD',
                'Deployment blueprint, monitoring setup'
            )
        }
        return actions.get(skill, ('Execute task', 'Output'))
    
    def _estimate_duration(self, complexity: str, num_skills: int) -> str:
        """Estimate project duration"""
        base_weeks = {
            'simple': 2,
            'medium': 6,
            'complex': 12,
            'very_complex': 24
        }
        
        weeks = base_weeks[complexity] * (1 + (num_skills - 1) * 0.3)
        
        if weeks < 4:
            return f"{int(weeks)} weeks"
        else:
            months = weeks / 4
            return f"{int(months)} months"
    
    def route_query(self, query: str) -> Dict:
        """
        Simple routing for single queries (not full project analysis).
        
        Args:
            query: User query/question
            
        Returns:
            Dict with routing decision
        """
        query_lower = query.lower()
        
        # Single skill routing
        for skill, keywords in self.skill_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return {
                    'route_to': skill.value,
                    'confidence': 'high',
                    'reason': f'Query contains {skill.value} keywords'
                }
        
        # Default to CTA if unclear
        return {
            'route_to': Skill.CTA_ORCHESTRATOR.value,
            'confidence': 'low',
            'reason': 'Query unclear, routing to CTA for coordination'
        }


def main():
    """Example usage"""
    router = SkillRouter()
    
    # Example 1: Simple web app
    print("=" * 70)
    print("Example 1: Simple Web App")
    print("=" * 70)
    
    requirements1 = """
    Build a blog platform with Next.js frontend and FastAPI backend.
    Users can create, read, update, and delete posts.
    PostgreSQL database for storage.
    """
    
    result1 = router.analyze_requirements(requirements1)
    print(f"Skills Needed: {', '.join(result1['skills_needed'])}")
    print(f"Complexity: {result1['complexity']}")
    print(f"Needs Orchestrator: {result1['needs_orchestrator']}")
    print(f"Estimated Duration: {result1['estimated_duration']}")
    print("\nExecution Plan:")
    for step in result1['execution_plan']:
        print(f"  Step {step['step']}: {step['skill']}")
        print(f"    Action: {step['action']}")
        print(f"    Output: {step['output']}")
    
    # Example 2: Complex multi-platform project
    print("\n" + "=" * 70)
    print("Example 2: Complex AI-Powered Mobile + Web App")
    print("=" * 70)
    
    requirements2 = """
    Build an AI-powered e-commerce platform with:
    - Next.js web app for customers
    - Flutter mobile app for iOS and Android
    - Product recommendation ML model
    - Real-time inventory management
    - Microservices architecture
    - Deploy on AWS with Kubernetes
    - High availability and scalability requirements
    """
    
    result2 = router.analyze_requirements(requirements2)
    print(f"Skills Needed: {', '.join(result2['skills_needed'])}")
    print(f"Complexity: {result2['complexity']}")
    print(f"Needs Orchestrator: {result2['needs_orchestrator']}")
    print(f"Estimated Duration: {result2['estimated_duration']}")
    print("\nExecution Plan:")
    for step in result2['execution_plan']:
        print(f"  Step {step['step']}: {step['skill']}")
        print(f"    Action: {step['action']}")
        print(f"    Output: {step['output']}")
    
    # Example 3: Simple query routing
    print("\n" + "=" * 70)
    print("Example 3: Query Routing")
    print("=" * 70)
    
    queries = [
        "How do I optimize my PostgreSQL database?",
        "Best practices for Flutter state management?",
        "Setup CI/CD pipeline for Django app",
        "What is the best architecture pattern?"
    ]
    
    for query in queries:
        result = router.route_query(query)
        print(f"\nQuery: {query}")
        print(f"  Route to: {result['route_to']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Reason: {result['reason']}")


if __name__ == "__main__":
    main()
