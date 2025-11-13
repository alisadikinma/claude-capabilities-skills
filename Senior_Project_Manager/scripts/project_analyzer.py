#!/usr/bin/env python3
"""
Project Health Analyzer
=======================
Comprehensive project analysis tool for PM health assessment.

Features:
- Earned Value Management (EVM) calculations
- Schedule & budget variance analysis
- RAG status generation (Red/Amber/Green)
- Agile velocity tracking
- Risk exposure assessment
- Forecast completion & cost
- Actionable recommendations

Usage:
    python project_analyzer.py --input project.json --format text
    python project_analyzer.py --input project.csv --export report.json

Input Format (JSON):
{
  "project": "Project Name",
  "methodology": "Agile|Waterfall|Hybrid",
  "budget": {
    "total": 500000,
    "spent": 275000,
    "planned_spent": 250000
  },
  "schedule": {
    "planned_completion": 0.50,
    "actual_completion": 0.45,
    "total_days": 180,
    "elapsed_days": 90
  },
  "agile_metrics": {
    "sprints_completed": 9,
    "velocity": [28, 30, 32, 29, 31, 30, 28, 32, 30],
    "committed": 300,
    "completed": 270
  },
  "risks": [
    {"probability": 0.7, "impact": 8, "status": "Open"},
    {"probability": 0.5, "impact": 5, "status": "Mitigated"}
  ]
}
"""

import json
import csv
import sys
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class ProjectAnalyzer:
    """Analyzes project health and generates comprehensive reports."""
    
    # RAG thresholds
    THRESHOLDS = {
        'CPI_RED': 0.90,
        'CPI_AMBER': 0.95,
        'SPI_RED': 0.90,
        'SPI_AMBER': 0.95,
        'VELOCITY_VARIANCE': 0.15,  # 15% variance threshold
        'RISK_HIGH': 30,
        'RISK_CRITICAL': 50
    }
    
    def __init__(self, data: Dict):
        """Initialize analyzer with project data."""
        self.data = data
        self.project_name = data.get('project', 'Unnamed Project')
        self.methodology = data.get('methodology', 'Unknown')
        self.budget = data.get('budget', {})
        self.schedule = data.get('schedule', {})
        self.agile_metrics = data.get('agile_metrics', {})
        self.risks = data.get('risks', [])
        
        # Calculated metrics
        self.evm_metrics = {}
        self.rag_status = {}
        self.concerns = []
        self.recommendations = []
        
    def analyze(self) -> Dict:
        """Run full project analysis."""
        self._calculate_earned_value()
        self._analyze_schedule()
        self._analyze_budget()
        self._analyze_velocity()
        self._calculate_risk_exposure()
        self._generate_rag_status()
        self._identify_concerns()
        self._generate_recommendations()
        
        return self._build_report()
    
    def _calculate_earned_value(self):
        """Calculate all EVM metrics."""
        # Extract budget data
        total_budget = self.budget.get('total', 0)
        actual_cost = self.budget.get('spent', 0)
        planned_spent = self.budget.get('planned_spent', 0)
        
        # Extract schedule data
        planned_pct = self.schedule.get('planned_completion', 0)
        actual_pct = self.schedule.get('actual_completion', 0)
        
        # Core EVM values
        pv = total_budget * planned_pct  # Planned Value
        ev = total_budget * actual_pct   # Earned Value
        ac = actual_cost                  # Actual Cost
        
        # Performance indices
        cpi = ev / ac if ac > 0 else 0  # Cost Performance Index
        spi = ev / pv if pv > 0 else 0  # Schedule Performance Index
        
        # Variances
        cv = ev - ac  # Cost Variance
        sv = ev - pv  # Schedule Variance
        
        # Forecasts
        bac = total_budget  # Budget at Completion
        eac = bac / cpi if cpi > 0 else 0  # Estimate at Completion
        etc = eac - ac  # Estimate to Complete
        vac = bac - eac  # Variance at Completion
        
        # To Complete Performance Index
        tcpi = (bac - ev) / (bac - ac) if (bac - ac) > 0 else 0
        
        self.evm_metrics = {
            'PV': pv,
            'EV': ev,
            'AC': ac,
            'BAC': bac,
            'CPI': cpi,
            'SPI': spi,
            'CV': cv,
            'SV': sv,
            'EAC': eac,
            'ETC': etc,
            'VAC': vac,
            'TCPI': tcpi
        }
    
    def _analyze_schedule(self):
        """Analyze schedule performance."""
        spi = self.evm_metrics.get('SPI', 0)
        total_days = self.schedule.get('total_days', 0)
        elapsed_days = self.schedule.get('elapsed_days', 0)
        actual_pct = self.schedule.get('actual_completion', 0)
        
        # Forecast completion
        if spi > 0 and actual_pct > 0:
            estimated_total_days = elapsed_days / actual_pct
            forecast_days = int(estimated_total_days)
            delay_days = forecast_days - total_days
        else:
            forecast_days = total_days
            delay_days = 0
        
        self.schedule_analysis = {
            'total_days': total_days,
            'elapsed_days': elapsed_days,
            'forecast_days': forecast_days,
            'delay_days': delay_days,
            'on_time': delay_days <= 0,
            'spi': spi
        }
    
    def _analyze_budget(self):
        """Analyze budget performance."""
        cpi = self.evm_metrics.get('CPI', 0)
        eac = self.evm_metrics.get('EAC', 0)
        bac = self.evm_metrics.get('BAC', 0)
        vac = self.evm_metrics.get('VAC', 0)
        
        overrun = eac - bac
        overrun_pct = (overrun / bac * 100) if bac > 0 else 0
        
        self.budget_analysis = {
            'total_budget': bac,
            'forecast_cost': eac,
            'overrun': overrun,
            'overrun_pct': overrun_pct,
            'on_budget': overrun <= 0,
            'cpi': cpi,
            'vac': vac
        }
    
    def _analyze_velocity(self):
        """Analyze Agile velocity trends."""
        if not self.agile_metrics or 'velocity' not in self.agile_metrics:
            self.velocity_analysis = None
            return
        
        velocity_data = self.agile_metrics.get('velocity', [])
        if not velocity_data:
            self.velocity_analysis = None
            return
        
        avg_velocity = sum(velocity_data) / len(velocity_data)
        recent_velocity = sum(velocity_data[-3:]) / min(3, len(velocity_data))
        
        # Calculate variance
        variance = abs(recent_velocity - avg_velocity) / avg_velocity if avg_velocity > 0 else 0
        stable = variance <= self.THRESHOLDS['VELOCITY_VARIANCE']
        
        # Commitment vs completion
        committed = self.agile_metrics.get('committed', 0)
        completed = self.agile_metrics.get('completed', 0)
        commitment_rate = (completed / committed * 100) if committed > 0 else 0
        
        self.velocity_analysis = {
            'avg_velocity': round(avg_velocity, 1),
            'recent_velocity': round(recent_velocity, 1),
            'variance': round(variance, 2),
            'stable': stable,
            'commitment_rate': round(commitment_rate, 1),
            'sprints_completed': self.agile_metrics.get('sprints_completed', 0)
        }
    
    def _calculate_risk_exposure(self):
        """Calculate total risk exposure score."""
        if not self.risks:
            self.risk_exposure = {
                'total_score': 0,
                'open_risks': 0,
                'level': 'LOW'
            }
            return
        
        total_score = 0
        open_risks = 0
        
        for risk in self.risks:
            prob = risk.get('probability', 0)
            impact = risk.get('impact', 0)
            status = risk.get('status', 'Open')
            
            if status.lower() in ['open', 'active']:
                score = prob * impact * 10  # Normalize to 0-100
                total_score += score
                open_risks += 1
        
        # Determine risk level
        if total_score >= self.THRESHOLDS['RISK_CRITICAL']:
            level = 'CRITICAL'
        elif total_score >= self.THRESHOLDS['RISK_HIGH']:
            level = 'HIGH'
        else:
            level = 'LOW'
        
        self.risk_exposure = {
            'total_score': round(total_score, 1),
            'open_risks': open_risks,
            'level': level
        }
    
    def _generate_rag_status(self):
        """Generate RAG status for each dimension."""
        cpi = self.evm_metrics.get('CPI', 0)
        spi = self.evm_metrics.get('SPI', 0)
        
        # Budget RAG
        if cpi < self.THRESHOLDS['CPI_RED']:
            budget_rag = 'RED'
        elif cpi < self.THRESHOLDS['CPI_AMBER']:
            budget_rag = 'AMBER'
        else:
            budget_rag = 'GREEN'
        
        # Schedule RAG
        if spi < self.THRESHOLDS['SPI_RED']:
            schedule_rag = 'RED'
        elif spi < self.THRESHOLDS['SPI_AMBER']:
            schedule_rag = 'AMBER'
        else:
            schedule_rag = 'GREEN'
        
        # Risk RAG
        risk_level = self.risk_exposure.get('level', 'LOW')
        if risk_level == 'CRITICAL':
            risk_rag = 'RED'
        elif risk_level == 'HIGH':
            risk_rag = 'AMBER'
        else:
            risk_rag = 'GREEN'
        
        # Velocity RAG (if Agile)
        if self.velocity_analysis:
            stable = self.velocity_analysis.get('stable', True)
            commitment_rate = self.velocity_analysis.get('commitment_rate', 100)
            
            if not stable or commitment_rate < 70:
                velocity_rag = 'RED'
            elif commitment_rate < 85:
                velocity_rag = 'AMBER'
            else:
                velocity_rag = 'GREEN'
        else:
            velocity_rag = None
        
        # Overall RAG (worst of all dimensions)
        rag_values = [budget_rag, schedule_rag, risk_rag]
        if velocity_rag:
            rag_values.append(velocity_rag)
        
        if 'RED' in rag_values:
            overall_rag = 'RED'
        elif 'AMBER' in rag_values:
            overall_rag = 'AMBER'
        else:
            overall_rag = 'GREEN'
        
        self.rag_status = {
            'overall': overall_rag,
            'budget': budget_rag,
            'schedule': schedule_rag,
            'risk': risk_rag,
            'velocity': velocity_rag
        }
    
    def _identify_concerns(self):
        """Identify top 3 concerns."""
        concerns = []
        
        # Budget concerns
        cpi = self.evm_metrics.get('CPI', 0)
        if cpi < self.THRESHOLDS['CPI_RED']:
            overrun_pct = self.budget_analysis.get('overrun_pct', 0)
            concerns.append({
                'area': 'Budget',
                'severity': 'HIGH',
                'description': f'Cost overrun: {overrun_pct:.1f}% over budget (CPI: {cpi:.2f})'
            })
        
        # Schedule concerns
        spi = self.evm_metrics.get('SPI', 0)
        if spi < self.THRESHOLDS['SPI_RED']:
            delay_days = self.schedule_analysis.get('delay_days', 0)
            concerns.append({
                'area': 'Schedule',
                'severity': 'HIGH',
                'description': f'Project delayed: {delay_days} days behind (SPI: {spi:.2f})'
            })
        
        # Risk concerns
        if self.risk_exposure.get('level') == 'CRITICAL':
            total_score = self.risk_exposure.get('total_score', 0)
            open_risks = self.risk_exposure.get('open_risks', 0)
            concerns.append({
                'area': 'Risk',
                'severity': 'HIGH',
                'description': f'Critical risk exposure: {total_score:.0f} ({open_risks} open risks)'
            })
        
        # Velocity concerns (if Agile)
        if self.velocity_analysis:
            if not self.velocity_analysis.get('stable'):
                concerns.append({
                    'area': 'Velocity',
                    'severity': 'MEDIUM',
                    'description': 'Unstable velocity trend detected'
                })
            
            commitment_rate = self.velocity_analysis.get('commitment_rate', 100)
            if commitment_rate < 70:
                concerns.append({
                    'area': 'Velocity',
                    'severity': 'HIGH',
                    'description': f'Low commitment rate: {commitment_rate:.1f}%'
                })
        
        # Sort by severity and take top 3
        severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        concerns.sort(key=lambda x: severity_order.get(x['severity'], 3))
        
        self.concerns = concerns[:3]
    
    def _generate_recommendations(self):
        """Generate actionable recommendations."""
        recommendations = []
        
        cpi = self.evm_metrics.get('CPI', 0)
        spi = self.evm_metrics.get('SPI', 0)
        
        # Budget recommendations
        if cpi < self.THRESHOLDS['CPI_AMBER']:
            recommendations.append({
                'area': 'Budget',
                'action': 'Review and reduce non-critical scope',
                'priority': 'HIGH' if cpi < self.THRESHOLDS['CPI_RED'] else 'MEDIUM'
            })
            recommendations.append({
                'area': 'Budget',
                'action': 'Implement stricter cost controls and approval processes',
                'priority': 'HIGH'
            })
        
        # Schedule recommendations
        if spi < self.THRESHOLDS['SPI_AMBER']:
            recommendations.append({
                'area': 'Schedule',
                'action': 'Fast-track critical path activities',
                'priority': 'HIGH' if spi < self.THRESHOLDS['SPI_RED'] else 'MEDIUM'
            })
            recommendations.append({
                'area': 'Schedule',
                'action': 'Add resources to bottleneck tasks',
                'priority': 'MEDIUM'
            })
        
        # Risk recommendations
        risk_level = self.risk_exposure.get('level')
        if risk_level in ['HIGH', 'CRITICAL']:
            recommendations.append({
                'area': 'Risk',
                'action': 'Escalate top risks to steering committee',
                'priority': 'HIGH'
            })
            recommendations.append({
                'area': 'Risk',
                'action': 'Implement mitigation plans for open risks',
                'priority': 'HIGH'
            })
        
        # Velocity recommendations
        if self.velocity_analysis:
            commitment_rate = self.velocity_analysis.get('commitment_rate', 100)
            if commitment_rate < 85:
                recommendations.append({
                    'area': 'Velocity',
                    'action': 'Review sprint planning process and estimation accuracy',
                    'priority': 'MEDIUM'
                })
        
        self.recommendations = recommendations[:5]  # Top 5
    
    def _build_report(self) -> Dict:
        """Build comprehensive report."""
        overall_rag = self.rag_status.get('overall')
        rag_emoji = {'RED': '🔴', 'AMBER': '🟡', 'GREEN': '🟢'}.get(overall_rag, '⚪')
        
        # Executive summary
        cpi = self.evm_metrics.get('CPI', 0)
        spi = self.evm_metrics.get('SPI', 0)
        
        if overall_rag == 'GREEN':
            summary = f"Project is on track with healthy metrics."
        elif overall_rag == 'AMBER':
            summary = f"Project at risk - monitoring required."
        else:
            summary = f"Project in critical state - immediate action needed."
        
        return {
            'project': self.project_name,
            'methodology': self.methodology,
            'timestamp': datetime.now().isoformat(),
            'executive_summary': summary,
            'overall_rag': f"{rag_emoji} {overall_rag}",
            'rag_breakdown': self.rag_status,
            'evm_metrics': self.evm_metrics,
            'schedule_analysis': self.schedule_analysis,
            'budget_analysis': self.budget_analysis,
            'velocity_analysis': self.velocity_analysis,
            'risk_exposure': self.risk_exposure,
            'top_concerns': self.concerns,
            'recommendations': self.recommendations
        }


def load_json(filepath: str) -> Dict:
    """Load project data from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        sys.exit(1)


def load_csv(filepath: str) -> Dict:
    """Load project data from CSV file (simplified format)."""
    try:
        data = {
            'budget': {},
            'schedule': {},
            'agile_metrics': {},
            'risks': []
        }
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse budget
                if 'total_budget' in row:
                    data['budget']['total'] = float(row.get('total_budget', 0))
                if 'spent' in row:
                    data['budget']['spent'] = float(row.get('spent', 0))
                if 'planned_spent' in row:
                    data['budget']['planned_spent'] = float(row.get('planned_spent', 0))
                
                # Parse schedule
                if 'planned_completion' in row:
                    data['schedule']['planned_completion'] = float(row.get('planned_completion', 0))
                if 'actual_completion' in row:
                    data['schedule']['actual_completion'] = float(row.get('actual_completion', 0))
        
        return data
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)


def print_text_report(report: Dict):
    """Print report in human-readable text format."""
    print("\n" + "="*60)
    print(f"PROJECT HEALTH ANALYSIS REPORT")
    print("="*60)
    print(f"\nProject: {report['project']}")
    print(f"Methodology: {report['methodology']}")
    print(f"Report Date: {report['timestamp'][:10]}")
    print("\n" + "-"*60)
    
    print(f"\n📊 EXECUTIVE SUMMARY")
    print(f"Status: {report['overall_rag']}")
    print(f"{report['executive_summary']}")
    
    print(f"\n🚦 RAG STATUS BREAKDOWN")
    rag = report['rag_breakdown']
    print(f"  Budget:   {rag['budget']}")
    print(f"  Schedule: {rag['schedule']}")
    print(f"  Risk:     {rag['risk']}")
    if rag.get('velocity'):
        print(f"  Velocity: {rag['velocity']}")
    
    print(f"\n💰 EARNED VALUE METRICS")
    evm = report['evm_metrics']
    print(f"  CPI: {evm['CPI']:.2f}  |  SPI: {evm['SPI']:.2f}")
    print(f"  BAC: ${evm['BAC']:,.0f}  |  EAC: ${evm['EAC']:,.0f}")
    print(f"  CV:  ${evm['CV']:,.0f}  |  SV:  ${evm['SV']:,.0f}")
    print(f"  VAC: ${evm['VAC']:,.0f} (Forecast variance)")
    
    print(f"\n📅 SCHEDULE ANALYSIS")
    sched = report['schedule_analysis']
    print(f"  Planned Duration: {sched['total_days']} days")
    print(f"  Forecast: {sched['forecast_days']} days")
    if sched['delay_days'] > 0:
        print(f"  ⚠️  Delay: {sched['delay_days']} days behind")
    else:
        print(f"  ✅ On time")
    
    print(f"\n💵 BUDGET ANALYSIS")
    budget = report['budget_analysis']
    print(f"  Total Budget: ${budget['total_budget']:,.0f}")
    print(f"  Forecast Cost: ${budget['forecast_cost']:,.0f}")
    if budget['overrun'] > 0:
        print(f"  ⚠️  Overrun: ${budget['overrun']:,.0f} ({budget['overrun_pct']:.1f}%)")
    else:
        print(f"  ✅ On budget")
    
    if report.get('velocity_analysis'):
        print(f"\n⚡ VELOCITY ANALYSIS (Agile)")
        vel = report['velocity_analysis']
        print(f"  Avg Velocity: {vel['avg_velocity']} pts/sprint")
        print(f"  Recent: {vel['recent_velocity']} pts/sprint")
        print(f"  Commitment Rate: {vel['commitment_rate']:.1f}%")
        print(f"  Stable: {'✅ Yes' if vel['stable'] else '⚠️ No'}")
    
    print(f"\n⚠️  RISK EXPOSURE")
    risk = report['risk_exposure']
    print(f"  Total Score: {risk['total_score']:.0f}")
    print(f"  Open Risks: {risk['open_risks']}")
    print(f"  Level: {risk['level']}")
    
    if report['top_concerns']:
        print(f"\n🚨 TOP CONCERNS")
        for i, concern in enumerate(report['top_concerns'], 1):
            print(f"  {i}. [{concern['severity']}] {concern['area']}: {concern['description']}")
    
    if report['recommendations']:
        print(f"\n💡 RECOMMENDED ACTIONS")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. [{rec['priority']}] {rec['area']}: {rec['action']}")
    
    print("\n" + "="*60 + "\n")


def export_json(report: Dict, filepath: str):
    """Export report to JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"✅ Report exported to: {filepath}")
    except Exception as e:
        print(f"Error exporting JSON: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze project health and generate comprehensive reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python project_analyzer.py --input project.json
  python project_analyzer.py --input data.csv --export report.json
  python project_analyzer.py --input project.json --format json
        """
    )
    
    parser.add_argument('--input', '-i', required=True,
                       help='Input file (JSON or CSV)')
    parser.add_argument('--format', '-f', choices=['text', 'json'],
                       default='text', help='Output format (default: text)')
    parser.add_argument('--export', '-e',
                       help='Export report to JSON file')
    
    args = parser.parse_args()
    
    # Load data
    if args.input.endswith('.json'):
        data = load_json(args.input)
    elif args.input.endswith('.csv'):
        data = load_csv(args.input)
    else:
        print("Error: Input file must be .json or .csv")
        sys.exit(1)
    
    # Analyze
    analyzer = ProjectAnalyzer(data)
    report = analyzer.analyze()
    
    # Output
    if args.format == 'json':
        print(json.dumps(report, indent=2))
    else:
        print_text_report(report)
    
    # Export
    if args.export:
        export_json(report, args.export)


if __name__ == '__main__':
    main()
