#!/usr/bin/env python3
"""
Risk Calculator and Risk Register Generator

Calculates risk scores (Probability × Impact) and generates risk reports.
Supports CSV import, manual entry, and generates prioritized risk registers.

Usage:
    python risk_calculator.py --project myproject
    python risk_calculator.py --csv risks.csv
    python risk_calculator.py --project myproject --output risk_report.txt
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path


class Risk:
    """Represents a single project risk."""
    
    # Probability levels
    PROB_VERY_LOW = 0.1
    PROB_LOW = 0.3
    PROB_MEDIUM = 0.5
    PROB_HIGH = 0.7
    PROB_VERY_HIGH = 0.9
    
    # Impact levels (on scale of 1-10)
    IMPACT_VERY_LOW = 1
    IMPACT_LOW = 3
    IMPACT_MEDIUM = 5
    IMPACT_HIGH = 7
    IMPACT_VERY_HIGH = 10
    
    def __init__(self, risk_id, description, category, probability, impact, 
                 mitigation='', owner='', status='Open'):
        self.risk_id = risk_id
        self.description = description
        self.category = category
        self.probability = self._normalize_probability(probability)
        self.impact = self._normalize_impact(impact)
        self.mitigation = mitigation
        self.owner = owner
        self.status = status
        
    def _normalize_probability(self, value):
        """Convert text probability to numeric (0-1 scale)."""
        if isinstance(value, (int, float)):
            return min(1.0, max(0.0, value))
        
        value_lower = str(value).lower().strip()
        prob_map = {
            'very low': self.PROB_VERY_LOW,
            'verylow': self.PROB_VERY_LOW,
            'vl': self.PROB_VERY_LOW,
            'low': self.PROB_LOW,
            'l': self.PROB_LOW,
            'medium': self.PROB_MEDIUM,
            'med': self.PROB_MEDIUM,
            'm': self.PROB_MEDIUM,
            'high': self.PROB_HIGH,
            'h': self.PROB_HIGH,
            'very high': self.PROB_VERY_HIGH,
            'veryhigh': self.PROB_VERY_HIGH,
            'vh': self.PROB_VERY_HIGH,
        }
        
        return prob_map.get(value_lower, self.PROB_MEDIUM)
    
    def _normalize_impact(self, value):
        """Convert text impact to numeric (1-10 scale)."""
        if isinstance(value, (int, float)):
            return min(10, max(1, int(value)))
        
        value_lower = str(value).lower().strip()
        impact_map = {
            'very low': self.IMPACT_VERY_LOW,
            'verylow': self.IMPACT_VERY_LOW,
            'vl': self.IMPACT_VERY_LOW,
            'low': self.IMPACT_LOW,
            'l': self.IMPACT_LOW,
            'medium': self.IMPACT_MEDIUM,
            'med': self.IMPACT_MEDIUM,
            'm': self.IMPACT_MEDIUM,
            'high': self.IMPACT_HIGH,
            'h': self.IMPACT_HIGH,
            'very high': self.IMPACT_VERY_HIGH,
            'veryhigh': self.IMPACT_VERY_HIGH,
            'vh': self.IMPACT_VERY_HIGH,
        }
        
        return impact_map.get(value_lower, self.IMPACT_MEDIUM)
    
    @property
    def risk_score(self):
        """Calculate risk score: Probability × Impact."""
        return self.probability * self.impact
    
    @property
    def risk_level(self):
        """Categorize risk level based on score."""
        score = self.risk_score
        if score >= 7:
            return 'CRITICAL'
        elif score >= 4:
            return 'HIGH'
        elif score >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @property
    def color(self):
        """Get color code for risk level."""
        level = self.risk_level
        colors = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }
        return colors.get(level, '⚪')
    
    def to_dict(self):
        """Convert risk to dictionary."""
        return {
            'risk_id': self.risk_id,
            'description': self.description,
            'category': self.category,
            'probability': self.probability,
            'impact': self.impact,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'mitigation': self.mitigation,
            'owner': self.owner,
            'status': self.status
        }


class RiskRegister:
    """Manages a collection of project risks."""
    
    def __init__(self, project_name=''):
        self.project_name = project_name
        self.risks = []
        
    def add_risk(self, risk):
        """Add a risk to the register."""
        self.risks.append(risk)
        
    def load_from_csv(self, csv_path):
        """Load risks from CSV file.
        
        CSV Format:
        risk_id,description,category,probability,impact,mitigation,owner,status
        R001,API timeout,Technical,High,High,Implement retry logic,Dev Lead,Open
        ...
        """
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                risk = Risk(
                    risk_id=row['risk_id'],
                    description=row['description'],
                    category=row.get('category', 'General'),
                    probability=row['probability'],
                    impact=row['impact'],
                    mitigation=row.get('mitigation', ''),
                    owner=row.get('owner', ''),
                    status=row.get('status', 'Open')
                )
                self.add_risk(risk)
                
    def load_from_json(self, json_path):
        """Load risks from JSON file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.project_name = data.get('project', self.project_name)
        
        for risk_data in data.get('risks', []):
            risk = Risk(
                risk_id=risk_data['risk_id'],
                description=risk_data['description'],
                category=risk_data.get('category', 'General'),
                probability=risk_data['probability'],
                impact=risk_data['impact'],
                mitigation=risk_data.get('mitigation', ''),
                owner=risk_data.get('owner', ''),
                status=risk_data.get('status', 'Open')
            )
            self.add_risk(risk)
            
    def add_manual_risk(self):
        """Manually add a risk via interactive prompts."""
        print("\\n--- Add New Risk ---")
        
        risk_id = input("Risk ID (e.g., R001): ").strip()
        description = input("Description: ").strip()
        category = input("Category (Technical/Schedule/Budget/Resource/External): ").strip() or 'General'
        
        print("\\nProbability (Very Low, Low, Medium, High, Very High or 0-1): ")
        probability = input("> ").strip()
        
        print("\\nImpact (Very Low, Low, Medium, High, Very High or 1-10): ")
        impact = input("> ").strip()
        
        mitigation = input("\\nMitigation strategy: ").strip()
        owner = input("Risk owner: ").strip()
        status = input("Status (Open/Mitigated/Closed) [Open]: ").strip() or 'Open'
        
        risk = Risk(risk_id, description, category, probability, impact, 
                   mitigation, owner, status)
        
        self.add_risk(risk)
        print(f"\\n✓ Added risk {risk_id} (Score: {risk.risk_score:.2f}, Level: {risk.risk_level})")
        
    def get_sorted_risks(self, by='score', reverse=True):
        """Get risks sorted by score, probability, or impact."""
        if by == 'score':
            return sorted(self.risks, key=lambda r: r.risk_score, reverse=reverse)
        elif by == 'probability':
            return sorted(self.risks, key=lambda r: r.probability, reverse=reverse)
        elif by == 'impact':
            return sorted(self.risks, key=lambda r: r.impact, reverse=reverse)
        else:
            return self.risks
            
    def get_risks_by_level(self, level):
        """Get all risks of a specific level."""
        return [r for r in self.risks if r.risk_level == level]
        
    def get_risks_by_status(self, status):
        """Get all risks with a specific status."""
        return [r for r in self.risks if r.status.lower() == status.lower()]
        
    def calculate_total_exposure(self):
        """Calculate total risk exposure (sum of all risk scores)."""
        return sum(r.risk_score for r in self.risks if r.status.lower() != 'closed')
        
    def get_statistics(self):
        """Get risk register statistics."""
        open_risks = self.get_risks_by_status('Open')
        mitigated_risks = self.get_risks_by_status('Mitigated')
        closed_risks = self.get_risks_by_status('Closed')
        
        critical = self.get_risks_by_level('CRITICAL')
        high = self.get_risks_by_level('HIGH')
        medium = self.get_risks_by_level('MEDIUM')
        low = self.get_risks_by_level('LOW')
        
        return {
            'total_risks': len(self.risks),
            'open': len(open_risks),
            'mitigated': len(mitigated_risks),
            'closed': len(closed_risks),
            'critical': len(critical),
            'high': len(high),
            'medium': len(medium),
            'low': len(low),
            'total_exposure': self.calculate_total_exposure()
        }
        
    def print_report(self):
        """Print comprehensive risk report."""
        stats = self.get_statistics()
        
        print(f"\\n{'='*80}")
        print(f"RISK REGISTER: {self.project_name or 'Unnamed Project'}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\\n")
        
        # Summary statistics
        print("SUMMARY STATISTICS:")
        print(f"  Total Risks:        {stats['total_risks']}")
        print(f"  ├─ Open:            {stats['open']}")
        print(f"  ├─ Mitigated:       {stats['mitigated']}")
        print(f"  └─ Closed:          {stats['closed']}")
        print(f"\\n  Risk Levels:")
        print(f"  ├─ 🔴 Critical:      {stats['critical']}")
        print(f"  ├─ 🟠 High:          {stats['high']}")
        print(f"  ├─ 🟡 Medium:        {stats['medium']}")
        print(f"  └─ 🟢 Low:           {stats['low']}")
        print(f"\\n  Total Exposure:     {stats['total_exposure']:.2f}")
        
        # Risk breakdown by level
        for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            level_risks = self.get_risks_by_level(level)
            if level_risks:
                print(f"\\n{'='*80}")
                print(f"{level} RISKS ({len(level_risks)})")
                print(f"{'='*80}")
                
                for risk in sorted(level_risks, key=lambda r: r.risk_score, reverse=True):
                    self._print_risk_detail(risk)
                    
    def _print_risk_detail(self, risk):
        """Print detailed information for a single risk."""
        print(f"\\n{risk.color} {risk.risk_id}: {risk.description}")
        print(f"  Category:     {risk.category}")
        print(f"  Probability:  {risk.probability:.2f} ({self._format_probability(risk.probability)})")
        print(f"  Impact:       {risk.impact:.0f} ({self._format_impact(risk.impact)})")
        print(f"  Risk Score:   {risk.risk_score:.2f}")
        print(f"  Status:       {risk.status}")
        if risk.owner:
            print(f"  Owner:        {risk.owner}")
        if risk.mitigation:
            print(f"  Mitigation:   {risk.mitigation}")
            
    def _format_probability(self, prob):
        """Convert numeric probability to text."""
        if prob >= 0.85:
            return "Very High"
        elif prob >= 0.6:
            return "High"
        elif prob >= 0.4:
            return "Medium"
        elif prob >= 0.2:
            return "Low"
        else:
            return "Very Low"
            
    def _format_impact(self, impact):
        """Convert numeric impact to text."""
        if impact >= 9:
            return "Very High"
        elif impact >= 6:
            return "High"
        elif impact >= 4:
            return "Medium"
        elif impact >= 2:
            return "Low"
        else:
            return "Very Low"
            
    def export_to_csv(self, output_path):
        """Export risk register to CSV."""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['risk_id', 'description', 'category', 'probability', 
                         'impact', 'risk_score', 'risk_level', 'mitigation', 'owner', 'status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for risk in self.get_sorted_risks():
                writer.writerow(risk.to_dict())
                
        print(f"✓ Exported to CSV: {output_path}")
        
    def export_to_json(self, output_path):
        """Export risk register to JSON."""
        data = {
            'project': self.project_name,
            'generated': datetime.now().isoformat(),
            'statistics': self.get_statistics(),
            'risks': [risk.to_dict() for risk in self.get_sorted_risks()]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"✓ Exported to JSON: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Calculate and analyze project risks')
    parser.add_argument('--project', type=str, help='Project name')
    parser.add_argument('--csv', type=str, help='CSV file with risk data')
    parser.add_argument('--json', type=str, help='JSON file with risk data')
    parser.add_argument('--output', type=str, help='Output report file')
    parser.add_argument('--export-csv', type=str, help='Export to CSV file')
    parser.add_argument('--export-json', type=str, help='Export to JSON file')
    parser.add_argument('--add', action='store_true', help='Add risks manually')
    
    args = parser.parse_args()
    
    register = RiskRegister(project_name=args.project or 'Project')
    
    # Load data
    if args.csv:
        print(f"Loading risks from CSV: {args.csv}")
        register.load_from_csv(args.csv)
    elif args.json:
        print(f"Loading risks from JSON: {args.json}")
        register.load_from_json(args.json)
    
    # Add manual risks
    if args.add or (not args.csv and not args.json):
        while True:
            register.add_manual_risk()
            another = input("\\nAdd another risk? (y/n): ").strip().lower()
            if another != 'y':
                break
    
    # Generate report
    if args.output:
        import io
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        register.print_report()
        
        output = sys.stdout.getvalue()
        sys.stdout = original_stdout
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"✓ Report saved to: {args.output}")
        print(output)
    else:
        register.print_report()
    
    # Export
    if args.export_csv:
        register.export_to_csv(args.export_csv)
    
    if args.export_json:
        register.export_to_json(args.export_json)


if __name__ == '__main__':
    main()
