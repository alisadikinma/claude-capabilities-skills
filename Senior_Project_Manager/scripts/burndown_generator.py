#!/usr/bin/env python3
"""
Burndown Chart Generator for Agile/Scrum Projects

Generates sprint burndown charts from task data.
Supports manual input, CSV import, and Jira integration.

Usage:
    python burndown_generator.py --sprint 5
    python burndown_generator.py --csv tasks.csv --sprint 5
    python burndown_generator.py --sprint 5 --output burndown.png
"""

import argparse
import csv
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not installed. Install with: pip install matplotlib")


class BurndownGenerator:
    def __init__(self, sprint_number, sprint_days=10, total_points=None):
        self.sprint_number = sprint_number
        self.sprint_days = sprint_days
        self.total_points = total_points
        self.daily_remaining = []
        self.dates = []
        
    def load_from_csv(self, csv_path):
        """Load sprint data from CSV file.
        
        CSV Format:
        date,remaining_points
        2025-01-01,30
        2025-01-02,28
        ...
        """
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = datetime.strptime(row['date'], '%Y-%m-%d')
                points = float(row['remaining_points'])
                self.dates.append(date)
                self.daily_remaining.append(points)
        
        if not self.total_points:
            self.total_points = self.daily_remaining[0] if self.daily_remaining else 0
            
    def load_from_json(self, json_path):
        """Load sprint data from JSON file.
        
        JSON Format:
        {
            "sprint": 5,
            "start_date": "2025-01-01",
            "sprint_days": 10,
            "total_points": 30,
            "daily_data": [
                {"day": 1, "remaining": 30},
                {"day": 2, "remaining": 28},
                ...
            ]
        }
        """
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        self.sprint_number = data.get('sprint', self.sprint_number)
        self.sprint_days = data.get('sprint_days', self.sprint_days)
        self.total_points = data.get('total_points', self.total_points)
        
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        
        for day_data in data['daily_data']:
            day = day_data['day']
            remaining = day_data['remaining']
            date = start_date + timedelta(days=day-1)
            self.dates.append(date)
            self.daily_remaining.append(remaining)
            
    def load_manual(self):
        """Manually input daily remaining points."""
        print(f"\\nEnter daily remaining points for Sprint {self.sprint_number}")
        print(f"Sprint duration: {self.sprint_days} days")
        
        if not self.total_points:
            self.total_points = float(input("Total story points committed: "))
        
        start_date_str = input("Sprint start date (YYYY-MM-DD): ")
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
        print(f"\\nEnter remaining points for each day (or press Enter to stop):")
        
        for day in range(1, self.sprint_days + 1):
            date = start_date + timedelta(days=day-1)
            try:
                points_str = input(f"Day {day} ({date.strftime('%Y-%m-%d')}): ")
                if not points_str:
                    break
                points = float(points_str)
                self.dates.append(date)
                self.daily_remaining.append(points)
            except ValueError:
                print(f"Invalid input. Skipping day {day}")
                continue
                
    def calculate_ideal_burndown(self):
        """Calculate ideal burndown line (linear)."""
        if not self.total_points or not self.dates:
            return [], []
        
        start_date = self.dates[0]
        end_date = start_date + timedelta(days=self.sprint_days - 1)
        
        ideal_dates = [start_date + timedelta(days=i) for i in range(self.sprint_days)]
        daily_burn = self.total_points / (self.sprint_days - 1)
        ideal_points = [self.total_points - (daily_burn * i) for i in range(self.sprint_days)]
        
        return ideal_dates, ideal_points
        
    def calculate_metrics(self):
        """Calculate sprint metrics."""
        if not self.daily_remaining or not self.dates:
            return {}
        
        current_remaining = self.daily_remaining[-1]
        days_elapsed = len(self.daily_remaining)
        days_left = self.sprint_days - days_elapsed
        
        # Velocity (points completed so far)
        completed = self.total_points - current_remaining
        velocity = completed / days_elapsed if days_elapsed > 0 else 0
        
        # Forecast (at current velocity, when will we finish?)
        if velocity > 0:
            forecast_days = current_remaining / velocity
            forecast_completion = days_elapsed + forecast_days
        else:
            forecast_completion = float('inf')
        
        # On track? (compare to ideal)
        ideal_dates, ideal_points = self.calculate_ideal_burndown()
        if days_elapsed <= len(ideal_points):
            ideal_remaining = ideal_points[days_elapsed - 1]
            variance = current_remaining - ideal_remaining
            on_track = variance <= 0  # On track if at or below ideal
        else:
            variance = None
            on_track = None
        
        return {
            'sprint': self.sprint_number,
            'total_points': self.total_points,
            'completed_points': completed,
            'remaining_points': current_remaining,
            'days_elapsed': days_elapsed,
            'days_left': days_left,
            'velocity': velocity,
            'forecast_completion': forecast_completion,
            'on_track': on_track,
            'variance': variance
        }
        
    def generate_chart(self, output_path='burndown.png'):
        """Generate burndown chart visualization."""
        if not HAS_MATPLOTLIB:
            print("Error: matplotlib not installed. Cannot generate chart.")
            return False
        
        if not self.daily_remaining or not self.dates:
            print("Error: No data to plot")
            return False
        
        # Calculate ideal burndown
        ideal_dates, ideal_points = self.calculate_ideal_burndown()
        
        # Create figure
        plt.figure(figsize=(12, 7))
        
        # Plot ideal burndown
        plt.plot(ideal_dates, ideal_points, 'g--', linewidth=2, label='Ideal Burndown', alpha=0.7)
        
        # Plot actual burndown
        plt.plot(self.dates, self.daily_remaining, 'b-o', linewidth=2, label='Actual Burndown', markersize=8)
        
        # Add zero line
        plt.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
        
        # Formatting
        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Story Points Remaining', fontsize=12, fontweight='bold')
        plt.title(f'Sprint {self.sprint_number} Burndown Chart', fontsize=14, fontweight='bold')
        plt.legend(loc='upper right', fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Format x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.xticks(rotation=45)
        
        # Set y-axis to start at 0
        plt.ylim(bottom=0)
        
        # Add metrics text box
        metrics = self.calculate_metrics()
        metrics_text = f"""Sprint {metrics['sprint']} Metrics:
Total Points: {metrics['total_points']:.0f}
Completed: {metrics['completed_points']:.0f}
Remaining: {metrics['remaining_points']:.0f}
Velocity: {metrics['velocity']:.1f} pts/day
Days Elapsed: {metrics['days_elapsed']}
Days Left: {metrics['days_left']}
"""
        
        if metrics['on_track'] is not None:
            status = "✓ On Track" if metrics['on_track'] else "⚠ Behind Schedule"
            metrics_text += f"Status: {status}\\n"
            if metrics['variance']:
                metrics_text += f"Variance: {metrics['variance']:+.1f} pts\\n"
        
        plt.text(0.02, 0.98, metrics_text, transform=plt.gca().transAxes,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                fontsize=9, family='monospace')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Chart saved to: {output_path}")
        
        return True
        
    def print_report(self):
        """Print text report of burndown data."""
        metrics = self.calculate_metrics()
        
        print(f"\\n{'='*60}")
        print(f"SPRINT {metrics['sprint']} BURNDOWN REPORT")
        print(f"{'='*60}\\n")
        
        print(f"Total Story Points: {metrics['total_points']:.0f}")
        print(f"Completed Points:   {metrics['completed_points']:.0f}")
        print(f"Remaining Points:   {metrics['remaining_points']:.0f}")
        print(f"\\nDays Elapsed:       {metrics['days_elapsed']}")
        print(f"Days Remaining:     {metrics['days_left']}")
        print(f"\\nVelocity:           {metrics['velocity']:.2f} points/day")
        
        if metrics['forecast_completion'] != float('inf'):
            print(f"Forecast:           Complete in {metrics['forecast_completion']:.1f} total days")
            if metrics['forecast_completion'] > self.sprint_days:
                overage = metrics['forecast_completion'] - self.sprint_days
                print(f"                    ⚠ {overage:.1f} days beyond sprint end")
        else:
            print(f"Forecast:           ⚠ No progress, cannot forecast")
        
        if metrics['on_track'] is not None:
            print(f"\\nStatus:             ", end='')
            if metrics['on_track']:
                print("✓ On Track")
            else:
                print("⚠ Behind Schedule")
            
            if metrics['variance']:
                print(f"Variance:           {metrics['variance']:+.1f} points ", end='')
                if metrics['variance'] > 0:
                    print("(behind ideal)")
                else:
                    print("(ahead of ideal)")
        
        print(f"\\n{'='*60}")
        
        # Daily breakdown
        print(f"\\nDAILY BREAKDOWN:")
        print(f"{'Date':<12} {'Day':<5} {'Remaining':>10}")
        print(f"{'-'*30}")
        
        ideal_dates, ideal_points = self.calculate_ideal_burndown()
        
        for i, (date, remaining) in enumerate(zip(self.dates, self.daily_remaining)):
            day_num = i + 1
            date_str = date.strftime('%Y-%m-%d')
            ideal_str = ""
            if i < len(ideal_points):
                ideal = ideal_points[i]
                ideal_str = f" (ideal: {ideal:.1f})"
            print(f"{date_str:<12} {day_num:<5} {remaining:>10.1f}{ideal_str}")
        
        print(f"{'='*60}\\n")


def main():
    parser = argparse.ArgumentParser(description='Generate sprint burndown chart')
    parser.add_argument('--sprint', type=int, required=True, help='Sprint number')
    parser.add_argument('--days', type=int, default=10, help='Sprint duration in days (default: 10)')
    parser.add_argument('--points', type=float, help='Total story points committed')
    parser.add_argument('--csv', type=str, help='CSV file with daily data')
    parser.add_argument('--json', type=str, help='JSON file with sprint data')
    parser.add_argument('--output', type=str, default='burndown.png', help='Output chart file (default: burndown.png)')
    parser.add_argument('--no-chart', action='store_true', help='Skip chart generation, only print report')
    
    args = parser.parse_args()
    
    generator = BurndownGenerator(
        sprint_number=args.sprint,
        sprint_days=args.days,
        total_points=args.points
    )
    
    # Load data
    if args.csv:
        print(f"Loading data from CSV: {args.csv}")
        generator.load_from_csv(args.csv)
    elif args.json:
        print(f"Loading data from JSON: {args.json}")
        generator.load_from_json(args.json)
    else:
        generator.load_manual()
    
    # Generate outputs
    generator.print_report()
    
    if not args.no_chart:
        if HAS_MATPLOTLIB:
            generator.generate_chart(args.output)
        else:
            print("\\nSkipping chart generation (matplotlib not installed)")
            print("Install with: pip install matplotlib")


if __name__ == '__main__':
    main()
