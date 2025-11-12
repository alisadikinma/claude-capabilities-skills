#!/usr/bin/env python3
"""
System Requirements Document (SRD) Generator
Generates SRD skeleton from interview notes and requirements gathering sessions.

Usage:
    python generate_srd.py --input notes.yaml
    python generate_srd.py --input notes.yaml --output srd.md
"""

import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class SRDGenerator:
    """Generate System Requirements Document from structured notes."""
    
    def __init__(self, input_path: str, output_path: str = 'srd.md'):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.notes = self._load_notes()
    
    def _load_notes(self) -> Dict:
        """Load interview notes from YAML."""
        with open(self.input_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def generate(self):
        """Generate complete SRD document."""
        print(f"📝 Generating SRD from {self.input_path}\n")
        
        document = self._generate_header()
        document += self._generate_executive_summary()
        document += self._generate_functional_requirements()
        document += self._generate_non_functional_requirements()
        document += self._generate_constraints()
        document += self._generate_user_stories()
        document += self._generate_use_cases()
        document += self._generate_assumptions()
        document += self._generate_risks()
        document += self._generate_glossary()
        document += self._generate_appendix()
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(document)
        
        print(f"✅ SRD generated: {self.output_path}")
        print(f"📄 Word count: {len(document.split())}")
    
    def _generate_header(self) -> str:
        """Generate document header."""
        project = self.notes.get('project', {})
        
        return f"""# System Requirements Document (SRD)

## {project.get('name', 'Project Name')}

**Version:** {project.get('version', '1.0.0')}  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Status:** {project.get('status', 'Draft')}

**Prepared by:** {project.get('analyst', 'System Analyst')}  
**Reviewed by:** {project.get('reviewer', 'TBD')}  
**Approved by:** {project.get('approver', 'TBD')}

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | {datetime.now().strftime('%Y-%m-%d')} | {project.get('analyst', 'Analyst')} | Initial draft |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Functional Requirements](#functional-requirements)
3. [Non-Functional Requirements](#non-functional-requirements)
4. [Constraints](#constraints)
5. [User Stories](#user-stories)
6. [Use Cases](#use-cases)
7. [Assumptions](#assumptions)
8. [Risks](#risks)
9. [Glossary](#glossary)
10. [Appendix](#appendix)

---

"""
    
    def _generate_executive_summary(self) -> str:
        """Generate executive summary."""
        summary = self.notes.get('executive_summary', {})
        
        content = """## 1. Executive Summary

"""
        
        # Business objectives
        if 'business_objectives' in summary:
            content += "### 1.1 Business Objectives\n\n"
            for obj in summary['business_objectives']:
                content += f"- {obj}\n"
            content += "\n"
        
        # Success criteria
        if 'success_criteria' in summary:
            content += "### 1.2 Success Criteria (KPIs)\n\n"
            content += "| Metric | Target | Measurement |\n"
            content += "|--------|--------|-------------|\n"
            for kpi in summary['success_criteria']:
                content += f"| {kpi['metric']} | {kpi['target']} | {kpi['measurement']} |\n"
            content += "\n"
        
        # Scope
        if 'scope' in summary:
            content += "### 1.3 Project Scope\n\n"
            scope = summary['scope']
            
            if 'in_scope' in scope:
                content += "**In Scope:**\n"
                for item in scope['in_scope']:
                    content += f"- {item}\n"
                content += "\n"
            
            if 'out_of_scope' in scope:
                content += "**Out of Scope:**\n"
                for item in scope['out_of_scope']:
                    content += f"- {item}\n"
                content += "\n"
        
        # Budget & timeline
        if 'budget' in summary or 'timeline' in summary:
            content += "### 1.4 Budget & Timeline\n\n"
            
            if 'budget' in summary:
                content += f"**Budget:** {summary['budget']}\n\n"
            
            if 'timeline' in summary:
                content += f"**Timeline:** {summary['timeline']}\n\n"
        
        content += "---\n\n"
        return content
    
    def _generate_functional_requirements(self) -> str:
        """Generate functional requirements."""
        functional = self.notes.get('functional_requirements', {})
        
        content = """## 2. Functional Requirements

"""
        
        if 'features' in functional:
            for idx, feature in enumerate(functional['features'], 1):
                content += f"### FR-{idx:03d}: {feature['name']}\n\n"
                
                content += f"**Description:** {feature['description']}\n\n"
                
                if 'priority' in feature:
                    content += f"**Priority:** {feature['priority']}\n\n"
                
                if 'acceptance_criteria' in feature:
                    content += "**Acceptance Criteria:**\n"
                    for criterion in feature['acceptance_criteria']:
                        content += f"- {criterion}\n"
                    content += "\n"
                
                if 'dependencies' in feature:
                    content += f"**Dependencies:** {', '.join(feature['dependencies'])}\n\n"
                
                content += "---\n\n"
        
        return content
    
    def _generate_non_functional_requirements(self) -> str:
        """Generate non-functional requirements."""
        nfr = self.notes.get('non_functional_requirements', {})
        
        content = """## 3. Non-Functional Requirements

"""
        
        # Performance
        if 'performance' in nfr:
            content += "### 3.1 Performance Requirements\n\n"
            content += "| Metric | Requirement | Measurement Method |\n"
            content += "|--------|-------------|--------------------|\n"
            for perf in nfr['performance']:
                content += f"| {perf['metric']} | {perf['requirement']} | {perf['measurement']} |\n"
            content += "\n"
        
        # Scalability
        if 'scalability' in nfr:
            content += "### 3.2 Scalability Requirements\n\n"
            for req in nfr['scalability']:
                content += f"- {req}\n"
            content += "\n"
        
        # Availability & Reliability
        if 'availability' in nfr:
            content += "### 3.3 Availability & Reliability\n\n"
            content += f"**Target SLA:** {nfr['availability'].get('sla', 'TBD')}\n\n"
            
            if 'uptime' in nfr['availability']:
                content += f"**Uptime:** {nfr['availability']['uptime']}\n\n"
            
            if 'rpo' in nfr['availability']:
                content += f"**RPO (Recovery Point Objective):** {nfr['availability']['rpo']}\n\n"
            
            if 'rto' in nfr['availability']:
                content += f"**RTO (Recovery Time Objective):** {nfr['availability']['rto']}\n\n"
        
        # Security
        if 'security' in nfr:
            content += "### 3.4 Security Requirements\n\n"
            for req in nfr['security']:
                content += f"- {req}\n"
            content += "\n"
        
        # Compliance
        if 'compliance' in nfr:
            content += "### 3.5 Compliance Requirements\n\n"
            for req in nfr['compliance']:
                content += f"- {req}\n"
            content += "\n"
        
        # Usability
        if 'usability' in nfr:
            content += "### 3.6 Usability Requirements\n\n"
            for req in nfr['usability']:
                content += f"- {req}\n"
            content += "\n"
        
        content += "---\n\n"
        return content
    
    def _generate_constraints(self) -> str:
        """Generate constraints."""
        constraints = self.notes.get('constraints', {})
        
        content = """## 4. Constraints

"""
        
        if 'technical' in constraints:
            content += "### 4.1 Technical Constraints\n\n"
            for constraint in constraints['technical']:
                content += f"- {constraint}\n"
            content += "\n"
        
        if 'business' in constraints:
            content += "### 4.2 Business Constraints\n\n"
            for constraint in constraints['business']:
                content += f"- {constraint}\n"
            content += "\n"
        
        if 'regulatory' in constraints:
            content += "### 4.3 Regulatory Constraints\n\n"
            for constraint in constraints['regulatory']:
                content += f"- {constraint}\n"
            content += "\n"
        
        if 'resource' in constraints:
            content += "### 4.4 Resource Constraints\n\n"
            for constraint in constraints['resource']:
                content += f"- {constraint}\n"
            content += "\n"
        
        content += "---\n\n"
        return content
    
    def _generate_user_stories(self) -> str:
        """Generate user stories."""
        stories = self.notes.get('user_stories', [])
        
        if not stories:
            return ""
        
        content = """## 5. User Stories

"""
        
        for idx, story in enumerate(stories, 1):
            content += f"### US-{idx:03d}: {story['title']}\n\n"
            
            content += f"**As a** {story['role']}  \n"
            content += f"**I want** {story['action']}  \n"
            content += f"**So that** {story['benefit']}\n\n"
            
            if 'priority' in story:
                content += f"**Priority:** {story['priority']}\n\n"
            
            if 'acceptance_criteria' in story:
                content += "**Acceptance Criteria:**\n"
                for criterion in story['acceptance_criteria']:
                    content += f"- {criterion}\n"
                content += "\n"
            
            content += "---\n\n"
        
        return content
    
    def _generate_use_cases(self) -> str:
        """Generate use cases."""
        use_cases = self.notes.get('use_cases', [])
        
        if not use_cases:
            return ""
        
        content = """## 6. Use Cases

"""
        
        for idx, uc in enumerate(use_cases, 1):
            content += f"### UC-{idx:03d}: {uc['name']}\n\n"
            
            content += f"**Actor:** {uc['actor']}\n\n"
            content += f"**Description:** {uc['description']}\n\n"
            
            if 'preconditions' in uc:
                content += "**Preconditions:**\n"
                for precond in uc['preconditions']:
                    content += f"- {precond}\n"
                content += "\n"
            
            if 'main_flow' in uc:
                content += "**Main Flow:**\n"
                for step_idx, step in enumerate(uc['main_flow'], 1):
                    content += f"{step_idx}. {step}\n"
                content += "\n"
            
            if 'alternative_flows' in uc:
                content += "**Alternative Flows:**\n"
                for alt in uc['alternative_flows']:
                    content += f"- {alt}\n"
                content += "\n"
            
            if 'postconditions' in uc:
                content += "**Postconditions:**\n"
                for postcond in uc['postconditions']:
                    content += f"- {postcond}\n"
                content += "\n"
            
            content += "---\n\n"
        
        return content
    
    def _generate_assumptions(self) -> str:
        """Generate assumptions."""
        assumptions = self.notes.get('assumptions', [])
        
        if not assumptions:
            return ""
        
        content = """## 7. Assumptions

"""
        
        for assumption in assumptions:
            content += f"- {assumption}\n"
        
        content += "\n---\n\n"
        return content
    
    def _generate_risks(self) -> str:
        """Generate risk assessment."""
        risks = self.notes.get('risks', [])
        
        if not risks:
            return ""
        
        content = """## 8. Risks

"""
        
        content += "| Risk | Probability | Impact | Mitigation Strategy |\n"
        content += "|------|-------------|--------|---------------------|\n"
        
        for risk in risks:
            content += f"| {risk['description']} | {risk['probability']} | {risk['impact']} | {risk['mitigation']} |\n"
        
        content += "\n---\n\n"
        return content
    
    def _generate_glossary(self) -> str:
        """Generate glossary."""
        glossary = self.notes.get('glossary', {})
        
        if not glossary:
            return ""
        
        content = """## 9. Glossary

"""
        
        for term, definition in sorted(glossary.items()):
            content += f"**{term}:** {definition}\n\n"
        
        content += "---\n\n"
        return content
    
    def _generate_appendix(self) -> str:
        """Generate appendix."""
        content = """## 10. Appendix

### A. Stakeholder List

| Name | Role | Responsibility | Contact |
|------|------|----------------|---------|
| TBD | TBD | TBD | TBD |

### B. References

- [Document 1] - Description
- [Document 2] - Description

### C. Change Log

All changes to this document will be tracked in the Document Control section.

---

**End of Document**
"""
        
        return content


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate System Requirements Document')
    parser.add_argument('--input', required=True, help='Path to interview notes (YAML)')
    parser.add_argument('--output', default='srd.md', help='Output SRD file')
    
    args = parser.parse_args()
    
    generator = SRDGenerator(args.input, args.output)
    generator.generate()


if __name__ == '__main__':
    main()
