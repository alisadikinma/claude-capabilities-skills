#!/usr/bin/env python3
"""
Tech Stack Recommender - Technology recommendation engine
Analyzes project requirements and recommends appropriate technology stack.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ProjectType(Enum):
    """Project types"""
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    API_SERVICE = "api_service"
    ML_SYSTEM = "ml_system"
    FULL_STACK = "full_stack"


@dataclass
class TechRecommendation:
    """Technology recommendation"""
    category: str
    recommended: str
    alternatives: List[str]
    rationale: str
    learning_curve: str  # easy, medium, hard
    maturity: str  # experimental, stable, mature


@dataclass
class TechStack:
    """Complete technology stack recommendation"""
    project_type: str
    recommendations: Dict[str, TechRecommendation]
    estimated_cost: Dict[str, str]
    team_size_fit: str
    warnings: List[str]


class TechStackRecommender:
    """Recommends technology stack based on project requirements"""
    
    def __init__(self):
        self.tech_database = self._initialize_tech_database()
    
    def _initialize_tech_database(self) -> Dict:
        """Initialize technology database with scoring criteria"""
        return {
            'backend': {
                'fastapi': {
                    'score_factors': {
                        'performance': 95,
                        'async_needed': 100,
                        'ml_integration': 90,
                        'api_focus': 100,
                        'modern_stack': 95,
                        'python_team': 100
                    },
                    'learning_curve': 'medium',
                    'maturity': 'stable',
                    'best_for': 'High-performance APIs, ML inference, async operations'
                },
                'django': {
                    'score_factors': {
                        'admin_panel': 100,
                        'orm_needed': 95,
                        'full_featured': 100,
                        'python_team': 100,
                        'rapid_dev': 90
                    },
                    'learning_curve': 'easy',
                    'maturity': 'mature',
                    'best_for': 'Full-featured web apps, admin panels, batteries-included'
                },
                'laravel': {
                    'score_factors': {
                        'php_team': 100,
                        'rapid_dev': 95,
                        'full_featured': 95,
                        'orm_needed': 90,
                        'admin_panel': 85
                    },
                    'learning_curve': 'easy',
                    'maturity': 'mature',
                    'best_for': 'PHP shops, rapid development, full-stack framework'
                },
                'express': {
                    'score_factors': {
                        'javascript_team': 100,
                        'flexible': 90,
                        'real_time': 85,
                        'minimal': 80
                    },
                    'learning_curve': 'easy',
                    'maturity': 'mature',
                    'best_for': 'JavaScript full-stack, real-time apps, flexibility'
                },
                'go': {
                    'score_factors': {
                        'performance': 100,
                        'microservices': 95,
                        'concurrent': 100,
                        'simple_deploy': 90
                    },
                    'learning_curve': 'hard',
                    'maturity': 'mature',
                    'best_for': 'High-performance microservices, concurrency'
                }
            },
            'frontend': {
                'nextjs': {
                    'score_factors': {
                        'seo_critical': 100,
                        'react_team': 100,
                        'ssr_needed': 100,
                        'modern_stack': 95,
                        'vercel_deploy': 90
                    },
                    'learning_curve': 'medium',
                    'maturity': 'stable',
                    'best_for': 'SEO-critical apps, SSR/SSG, React ecosystem'
                },
                'vue': {
                    'score_factors': {
                        'easy_learn': 100,
                        'laravel_team': 95,
                        'progressive': 90,
                        'lightweight': 85
                    },
                    'learning_curve': 'easy',
                    'maturity': 'mature',
                    'best_for': 'Easy learning curve, Laravel integration, progressive enhancement'
                },
                'react': {
                    'score_factors': {
                        'complex_ui': 95,
                        'large_team': 90,
                        'ecosystem': 100,
                        'job_market': 95
                    },
                    'learning_curve': 'medium',
                    'maturity': 'mature',
                    'best_for': 'Complex UIs, large teams, extensive ecosystem'
                },
                'svelte': {
                    'score_factors': {
                        'performance': 100,
                        'small_bundle': 100,
                        'simple_syntax': 95
                    },
                    'learning_curve': 'easy',
                    'maturity': 'stable',
                    'best_for': 'Performance-critical, small bundle size, simple syntax'
                }
            },
            'mobile': {
                'flutter': {
                    'score_factors': {
                        'cross_platform': 100,
                        'single_codebase': 100,
                        'fast_dev': 95,
                        'hot_reload': 100,
                        'ui_consistency': 100
                    },
                    'learning_curve': 'medium',
                    'maturity': 'stable',
                    'best_for': 'Cross-platform, single codebase, fast development'
                },
                'react_native': {
                    'score_factors': {
                        'cross_platform': 100,
                        'javascript_team': 100,
                        'web_sharing': 90,
                        'ecosystem': 95
                    },
                    'learning_curve': 'medium',
                    'maturity': 'mature',
                    'best_for': 'JavaScript teams, code sharing with web'
                },
                'kotlin': {
                    'score_factors': {
                        'android_only': 100,
                        'native_performance': 100,
                        'jetpack_compose': 95
                    },
                    'learning_curve': 'medium',
                    'maturity': 'mature',
                    'best_for': 'Android-only, native performance, Jetpack Compose'
                },
                'swift': {
                    'score_factors': {
                        'ios_only': 100,
                        'native_performance': 100,
                        'swiftui': 95
                    },
                    'learning_curve': 'medium',
                    'maturity': 'mature',
                    'best_for': 'iOS-only, native performance, SwiftUI'
                }
            },
            'database': {
                'postgresql': {
                    'score_factors': {
                        'relational': 100,
                        'acid': 100,
                        'json_support': 95,
                        'extensions': 100,
                        'complex_queries': 100
                    },
                    'learning_curve': 'medium',
                    'maturity': 'mature',
                    'best_for': 'Complex queries, ACID, JSON, extensions (PostGIS, pgvector)'
                },
                'mysql': {
                    'score_factors': {
                        'relational': 100,
                        'simple': 90,
                        'wordpress': 100,
                        'laravel': 95
                    },
                    'learning_curve': 'easy',
                    'maturity': 'mature',
                    'best_for': 'Simple relational needs, WordPress/Laravel ecosystem'
                },
                'mongodb': {
                    'score_factors': {
                        'flexible_schema': 100,
                        'rapid_iteration': 95,
                        'document': 100,
                        'horizontal_scale': 90
                    },
                    'learning_curve': 'easy',
                    'maturity': 'mature',
                    'best_for': 'Flexible schema, rapid iteration, document storage'
                },
                'redis': {
                    'score_factors': {
                        'caching': 100,
                        'session_store': 100,
                        'pub_sub': 95,
                        'fast': 100
                    },
                    'learning_curve': 'easy',
                    'maturity': 'mature',
                    'best_for': 'Caching, session storage, pub/sub, queues'
                }
            },
            'ml_framework': {
                'pytorch': {
                    'score_factors': {
                        'research': 100,
                        'flexibility': 100,
                        'pythonic': 100,
                        'community': 95
                    },
                    'learning_curve': 'medium',
                    'maturity': 'mature',
                    'best_for': 'Research, flexibility, dynamic graphs, computer vision'
                },
                'tensorflow': {
                    'score_factors': {
                        'production': 100,
                        'deployment': 100,
                        'mobile': 95,
                        'enterprise': 90
                    },
                    'learning_curve': 'hard',
                    'maturity': 'mature',
                    'best_for': 'Production deployment, mobile (TFLite), TFServing'
                },
                'huggingface': {
                    'score_factors': {
                        'nlp': 100,
                        'transformers': 100,
                        'pretrained': 100,
                        'easy_use': 95
                    },
                    'learning_curve': 'easy',
                    'maturity': 'stable',
                    'best_for': 'NLP, transformers, pre-trained models, fine-tuning'
                }
            },
            'deployment': {
                'docker': {
                    'score_factors': {
                        'consistency': 100,
                        'portability': 100,
                        'simple': 90
                    },
                    'learning_curve': 'medium',
                    'maturity': 'mature',
                    'best_for': 'Consistent environments, portability, dev/prod parity'
                },
                'kubernetes': {
                    'score_factors': {
                        'microservices': 100,
                        'auto_scale': 100,
                        'enterprise': 95,
                        'orchestration': 100
                    },
                    'learning_curve': 'hard',
                    'maturity': 'mature',
                    'best_for': 'Microservices, auto-scaling, enterprise, orchestration'
                },
                'vercel': {
                    'score_factors': {
                        'nextjs': 100,
                        'zero_config': 100,
                        'frontend': 95,
                        'fast_deploy': 100
                    },
                    'learning_curve': 'easy',
                    'maturity': 'stable',
                    'best_for': 'Next.js apps, zero-config, frontend-focused'
                },
                'aws': {
                    'score_factors': {
                        'enterprise': 100,
                        'scalability': 100,
                        'services': 100,
                        'mature': 100
                    },
                    'learning_curve': 'hard',
                    'maturity': 'mature',
                    'best_for': 'Enterprise, wide service range, market leader'
                }
            }
        }
    
    def recommend(
        self,
        requirements: str,
        team_size: int = 5,
        team_skills: Optional[List[str]] = None,
        budget: str = 'medium'  # low, medium, high
    ) -> TechStack:
        """
        Recommend technology stack based on requirements.
        
        Args:
            requirements: Project requirements text
            team_size: Number of team members
            team_skills: List of team's existing skills
            budget: Budget level (low, medium, high)
            
        Returns:
            TechStack with recommendations
        """
        req_lower = requirements.lower()
        team_skills = team_skills or []
        
        # Detect project type
        project_type = self._detect_project_type(req_lower)
        
        # Get recommendations for each category
        recommendations = {}
        
        if 'web' in project_type or 'full_stack' in project_type:
            recommendations['backend'] = self._recommend_backend(
                req_lower, team_skills
            )
            recommendations['frontend'] = self._recommend_frontend(
                req_lower, team_skills
            )
        
        if 'mobile' in project_type or 'full_stack' in project_type:
            recommendations['mobile'] = self._recommend_mobile(
                req_lower, team_skills
            )
        
        if 'ml' in project_type or 'ai' in req_lower:
            recommendations['ml_framework'] = self._recommend_ml(
                req_lower, team_skills
            )
        
        # Always recommend database and deployment
        recommendations['database'] = self._recommend_database(req_lower)
        recommendations['cache'] = self._recommend_cache(req_lower)
        recommendations['deployment'] = self._recommend_deployment(
            req_lower, team_size, budget
        )
        
        # Estimate costs
        estimated_cost = self._estimate_costs(recommendations, budget)
        
        # Check team fit
        team_size_fit = self._assess_team_fit(team_size, recommendations)
        
        # Generate warnings
        warnings = self._generate_warnings(
            recommendations, team_skills, team_size, budget
        )
        
        return TechStack(
            project_type=project_type,
            recommendations=recommendations,
            estimated_cost=estimated_cost,
            team_size_fit=team_size_fit,
            warnings=warnings
        )
    
    def _detect_project_type(self, requirements: str) -> str:
        """Detect primary project type"""
        if 'mobile' in requirements and 'web' in requirements:
            return 'full_stack'
        elif 'mobile' in requirements or 'ios' in requirements or 'android' in requirements:
            return 'mobile_app'
        elif 'api' in requirements and 'frontend' not in requirements:
            return 'api_service'
        elif 'ml' in requirements or 'ai' in requirements or 'model' in requirements:
            return 'ml_system'
        else:
            return 'web_app'
    
    def _recommend_backend(
        self, requirements: str, team_skills: List[str]
    ) -> TechRecommendation:
        """Recommend backend framework"""
        scores = {}
        
        for tech, data in self.tech_database['backend'].items():
            score = 0
            factors = data['score_factors']
            
            # Performance requirements
            if 'performance' in factors and ('performance' in requirements or 'fast' in requirements):
                score += factors['performance']
            
            # Async requirements
            if 'async_needed' in factors and 'async' in requirements:
                score += factors['async_needed']
            
            # ML integration
            if 'ml_integration' in factors and ('ml' in requirements or 'ai' in requirements):
                score += factors['ml_integration']
            
            # Team skills boost
            if 'python' in tech.lower() and 'python' in [s.lower() for s in team_skills]:
                score += 50
            if 'php' in tech.lower() and 'php' in [s.lower() for s in team_skills]:
                score += 50
            if tech == 'express' and 'javascript' in [s.lower() for s in team_skills]:
                score += 50
            
            # API focus
            if 'api_focus' in factors and 'api' in requirements:
                score += factors['api_focus']
            
            scores[tech] = score
        
        recommended = max(scores, key=scores.get)
        alternatives = sorted(scores.items(), key=lambda x: x[1], reverse=True)[1:3]
        
        data = self.tech_database['backend'][recommended]
        
        return TechRecommendation(
            category='backend',
            recommended=recommended,
            alternatives=[alt[0] for alt in alternatives],
            rationale=data['best_for'],
            learning_curve=data['learning_curve'],
            maturity=data['maturity']
        )
    
    def _recommend_frontend(
        self, requirements: str, team_skills: List[str]
    ) -> TechRecommendation:
        """Recommend frontend framework"""
        scores = {}
        
        for tech, data in self.tech_database['frontend'].items():
            score = 0
            factors = data['score_factors']
            
            # SEO requirements
            if 'seo_critical' in factors and 'seo' in requirements:
                score += factors['seo_critical']
            
            # Team skills
            if 'react' in tech.lower() and 'react' in [s.lower() for s in team_skills]:
                score += 60
            if tech == 'vue' and ('vue' in [s.lower() for s in team_skills] or 'laravel' in [s.lower() for s in team_skills]):
                score += 60
            
            # Performance
            if 'performance' in factors and 'performance' in requirements:
                score += factors['performance']
            
            # Easy learning
            if 'easy_learn' in factors and len(team_skills) < 2:
                score += factors['easy_learn']
            
            scores[tech] = score
        
        recommended = max(scores, key=scores.get)
        alternatives = sorted(scores.items(), key=lambda x: x[1], reverse=True)[1:3]
        
        data = self.tech_database['frontend'][recommended]
        
        return TechRecommendation(
            category='frontend',
            recommended=recommended,
            alternatives=[alt[0] for alt in alternatives],
            rationale=data['best_for'],
            learning_curve=data['learning_curve'],
            maturity=data['maturity']
        )
    
    def _recommend_mobile(
        self, requirements: str, team_skills: List[str]
    ) -> TechRecommendation:
        """Recommend mobile framework"""
        if 'ios' in requirements and 'android' not in requirements:
            recommended = 'swift'
        elif 'android' in requirements and 'ios' not in requirements:
            recommended = 'kotlin'
        elif 'javascript' in [s.lower() for s in team_skills] or 'react' in [s.lower() for s in team_skills]:
            recommended = 'react_native'
        else:
            recommended = 'flutter'  # Best default for cross-platform
        
        data = self.tech_database['mobile'][recommended]
        all_mobile = list(self.tech_database['mobile'].keys())
        alternatives = [m for m in all_mobile if m != recommended][:2]
        
        return TechRecommendation(
            category='mobile',
            recommended=recommended,
            alternatives=alternatives,
            rationale=data['best_for'],
            learning_curve=data['learning_curve'],
            maturity=data['maturity']
        )
    
    def _recommend_ml(
        self, requirements: str, team_skills: List[str]
    ) -> TechRecommendation:
        """Recommend ML framework"""
        if 'nlp' in requirements or 'transformers' in requirements or 'bert' in requirements:
            recommended = 'huggingface'
        elif 'production' in requirements or 'deploy' in requirements:
            recommended = 'tensorflow'
        else:
            recommended = 'pytorch'  # Best default
        
        data = self.tech_database['ml_framework'][recommended]
        all_ml = list(self.tech_database['ml_framework'].keys())
        alternatives = [m for m in all_ml if m != recommended][:2]
        
        return TechRecommendation(
            category='ml_framework',
            recommended=recommended,
            alternatives=alternatives,
            rationale=data['best_for'],
            learning_curve=data['learning_curve'],
            maturity=data['maturity']
        )
    
    def _recommend_database(self, requirements: str) -> TechRecommendation:
        """Recommend primary database"""
        if 'flexible schema' in requirements or 'mongodb' in requirements:
            recommended = 'mongodb'
        elif 'mysql' in requirements or 'wordpress' in requirements:
            recommended = 'mysql'
        else:
            recommended = 'postgresql'  # Best default
        
        data = self.tech_database['database'][recommended]
        
        return TechRecommendation(
            category='database',
            recommended=recommended,
            alternatives=['mysql', 'mongodb'] if recommended == 'postgresql' else ['postgresql'],
            rationale=data['best_for'],
            learning_curve=data['learning_curve'],
            maturity=data['maturity']
        )
    
    def _recommend_cache(self, requirements: str) -> TechRecommendation:
        """Recommend caching solution"""
        data = self.tech_database['database']['redis']
        
        return TechRecommendation(
            category='cache',
            recommended='redis',
            alternatives=['memcached'],
            rationale=data['best_for'],
            learning_curve=data['learning_curve'],
            maturity=data['maturity']
        )
    
    def _recommend_deployment(
        self, requirements: str, team_size: int, budget: str
    ) -> TechRecommendation:
        """Recommend deployment platform"""
        if 'nextjs' in requirements and budget != 'low':
            recommended = 'vercel'
        elif 'kubernetes' in requirements or team_size > 10:
            recommended = 'kubernetes'
        elif team_size < 5 and budget == 'low':
            recommended = 'docker'
        else:
            recommended = 'aws'
        
        data = self.tech_database['deployment'][recommended]
        
        return TechRecommendation(
            category='deployment',
            recommended=recommended,
            alternatives=['aws', 'docker'] if recommended != 'aws' else ['vercel', 'docker'],
            rationale=data['best_for'],
            learning_curve=data['learning_curve'],
            maturity=data['maturity']
        )
    
    def _estimate_costs(
        self, recommendations: Dict, budget: str
    ) -> Dict[str, str]:
        """Estimate monthly costs"""
        costs = {
            'development': '$0 (open source)',
            'hosting': '$50-200 (startup) → $500-2K (production)',
            'third_party': '$0-100 (free tiers available)'
        }
        
        if recommendations.get('deployment', {}).recommended == 'kubernetes':
            costs['hosting'] = '$200-500 (startup) → $2K-10K (production)'
        
        return costs
    
    def _assess_team_fit(
        self, team_size: int, recommendations: Dict
    ) -> str:
        """Assess if stack fits team size"""
        complexity_score = 0
        
        for rec in recommendations.values():
            if rec.learning_curve == 'hard':
                complexity_score += 2
            elif rec.learning_curve == 'medium':
                complexity_score += 1
        
        if team_size < 5 and complexity_score > 5:
            return 'challenging'
        elif team_size >= 5 and complexity_score > 8:
            return 'manageable'
        else:
            return 'good_fit'
    
    def _generate_warnings(
        self,
        recommendations: Dict,
        team_skills: List[str],
        team_size: int,
        budget: str
    ) -> List[str]:
        """Generate warnings about tech choices"""
        warnings = []
        
        # Check for skill gaps
        hard_learning = [r.recommended for r in recommendations.values() 
                        if r.learning_curve == 'hard']
        if hard_learning and len(team_skills) < 2:
            warnings.append(f"Steep learning curve: {', '.join(hard_learning)}")
        
        # Check team size vs complexity
        if team_size < 5 and len(recommendations) > 6:
            warnings.append("Tech stack may be too complex for small team")
        
        # Check experimental tech
        experimental = [r.recommended for r in recommendations.values() 
                       if r.maturity == 'experimental']
        if experimental:
            warnings.append(f"Experimental tech (risk): {', '.join(experimental)}")
        
        # Budget warnings
        if budget == 'low' and recommendations.get('deployment', {}).recommended in ['aws', 'kubernetes']:
            warnings.append("High infrastructure costs with chosen deployment")
        
        return warnings


def main():
    """Example usage"""
    recommender = TechStackRecommender()
    
    # Example 1: Simple web app
    print("=" * 70)
    print("Example 1: Blog Platform")
    print("=" * 70)
    
    req1 = """
    Build a blog platform with user authentication, 
    post creation, and commenting. SEO is important.
    """
    
    stack1 = recommender.recommend(
        req1,
        team_size=3,
        team_skills=['JavaScript', 'React'],
        budget='low'
    )
    
    print(f"Project Type: {stack1.project_type}")
    print(f"Team Fit: {stack1.team_size_fit}")
    print("\nRecommended Stack:")
    for category, rec in stack1.recommendations.items():
        print(f"\n  {category.upper()}: {rec.recommended}")
        print(f"    Alternatives: {', '.join(rec.alternatives)}")
        print(f"    Rationale: {rec.rationale}")
        print(f"    Learning: {rec.learning_curve}, Maturity: {rec.maturity}")
    
    print("\nEstimated Costs:")
    for cost_type, amount in stack1.estimated_cost.items():
        print(f"  {cost_type}: {amount}")
    
    if stack1.warnings:
        print("\n⚠️  Warnings:")
        for warning in stack1.warnings:
            print(f"  - {warning}")
    
    # Example 2: ML-powered mobile app
    print("\n" + "=" * 70)
    print("Example 2: AI-Powered Mobile App")
    print("=" * 70)
    
    req2 = """
    Build a mobile app (iOS and Android) with image recognition 
    using machine learning. Need real-time inference and offline capability.
    Backend API for user management and data sync.
    """
    
    stack2 = recommender.recommend(
        req2,
        team_size=6,
        team_skills=['Python', 'PyTorch'],
        budget='medium'
    )
    
    print(f"Project Type: {stack2.project_type}")
    print(f"Team Fit: {stack2.team_size_fit}")
    print("\nRecommended Stack:")
    for category, rec in stack2.recommendations.items():
        print(f"\n  {category.upper()}: {rec.recommended}")
        print(f"    Alternatives: {', '.join(rec.alternatives)}")
        print(f"    Rationale: {rec.rationale}")
    
    if stack2.warnings:
        print("\n⚠️  Warnings:")
        for warning in stack2.warnings:
            print(f"  - {warning}")


if __name__ == "__main__":
    main()
