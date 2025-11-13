#!/usr/bin/env python3
"""
Jira Sync Tool
==============
Automate Jira data export/import, burndown generation, and velocity tracking.

Features:
- Export issues from sprints/backlog
- Bulk import/update issues
- Generate burndown charts
- Calculate team velocity
- Support both Jira Cloud and Server

Setup:
    pip install jira matplotlib

Configuration (via environment variables):
    JIRA_URL=https://yourcompany.atlassian.net
    JIRA_USER=your.email@company.com
    JIRA_TOKEN=your_api_token

Usage:
    python jira_sync.py export --project PROJ --sprint 5 --output sprint5.json
    python jira_sync.py import --file backlog.json --project PROJ
    python jira_sync.py burndown --sprint 5 --output chart.png
    python jira_sync.py velocity --project PROJ --sprints 5
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Check if jira library is available
try:
    from jira import JIRA, JIRAError
    JIRA_AVAILABLE = True
except ImportError:
    JIRA_AVAILABLE = False

# Check if matplotlib is available for charts
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class JiraSync:
    """Jira data synchronization and automation tool."""
    
    def __init__(self, url: str = None, user: str = None, token: str = None):
        """Initialize Jira connection."""
        if not JIRA_AVAILABLE:
            print("Error: jira library not installed.")
            print("Install with: pip install jira")
            sys.exit(1)
        
        # Get credentials from params or environment
        self.url = url or os.getenv('JIRA_URL')
        self.user = user or os.getenv('JIRA_USER')
        self.token = token or os.getenv('JIRA_TOKEN')
        
        if not all([self.url, self.user, self.token]):
            print("Error: Missing Jira credentials.")
            print("Set environment variables: JIRA_URL, JIRA_USER, JIRA_TOKEN")
            print("Or pass as arguments: --url, --user, --token")
            sys.exit(1)
        
        try:
            self.jira = JIRA(
                server=self.url,
                basic_auth=(self.user, self.token)
            )
            print(f"✅ Connected to Jira: {self.url}")
        except JIRAError as e:
            print(f"Error connecting to Jira: {e}")
            sys.exit(1)
    
    def export_sprint(self, project: str, sprint_id: int, output_file: str):
        """Export issues from a specific sprint."""
        try:
            # JQL query for sprint issues
            jql = f'project = {project} AND sprint = {sprint_id}'
            issues = self.jira.search_issues(jql, maxResults=500)
            
            data = []
            for issue in issues:
                item = {
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'status': issue.fields.status.name,
                    'issue_type': issue.fields.issuetype.name,
                    'assignee': issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned',
                    'priority': issue.fields.priority.name if issue.fields.priority else 'None',
                    'labels': issue.fields.labels,
                    'created': issue.fields.created,
                    'updated': issue.fields.updated
                }
                
                # Story points (custom field, may vary)
                if hasattr(issue.fields, 'customfield_10016'):
                    item['story_points'] = issue.fields.customfield_10016
                
                data.append(item)
            
            # Save to JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Exported {len(data)} issues to {output_file}")
            
        except JIRAError as e:
            print(f"Error exporting sprint: {e}")
            sys.exit(1)
    
    def export_backlog(self, project: str, output_file: str):
        """Export backlog items (issues without sprint)."""
        try:
            jql = f'project = {project} AND sprint is EMPTY AND status != Done ORDER BY priority DESC'
            issues = self.jira.search_issues(jql, maxResults=500)
            
            data = []
            for issue in issues:
                item = {
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'status': issue.fields.status.name,
                    'issue_type': issue.fields.issuetype.name,
                    'priority': issue.fields.priority.name if issue.fields.priority else 'None',
                    'labels': issue.fields.labels
                }
                
                if hasattr(issue.fields, 'customfield_10016'):
                    item['story_points'] = issue.fields.customfield_10016
                
                data.append(item)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Exported {len(data)} backlog items to {output_file}")
            
        except JIRAError as e:
            print(f"Error exporting backlog: {e}")
            sys.exit(1)
    
    def import_issues(self, project: str, input_file: str, update_existing: bool = False):
        """Bulk create or update issues from JSON file."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                issues_data = json.load(f)
            
            created = 0
            updated = 0
            
            for item in issues_data:
                # Check if issue exists (by key)
                issue_key = item.get('key')
                
                if issue_key and update_existing:
                    try:
                        # Update existing issue
                        issue = self.jira.issue(issue_key)
                        
                        update_fields = {}
                        if 'summary' in item:
                            update_fields['summary'] = item['summary']
                        if 'status' in item:
                            # Transition to status (requires transition ID)
                            transitions = self.jira.transitions(issue)
                            for t in transitions:
                                if t['name'] == item['status']:
                                    self.jira.transition_issue(issue, t['id'])
                                    break
                        
                        if update_fields:
                            issue.update(fields=update_fields)
                        
                        updated += 1
                        print(f"✅ Updated: {issue_key}")
                        
                    except JIRAError:
                        print(f"⚠️  Could not update {issue_key}")
                else:
                    # Create new issue
                    fields = {
                        'project': {'key': project},
                        'summary': item.get('summary', 'Untitled'),
                        'issuetype': {'name': item.get('issue_type', 'Task')}
                    }
                    
                    if 'description' in item:
                        fields['description'] = item['description']
                    if 'priority' in item:
                        fields['priority'] = {'name': item['priority']}
                    if 'labels' in item:
                        fields['labels'] = item['labels']
                    
                    new_issue = self.jira.create_issue(fields=fields)
                    created += 1
                    print(f"✅ Created: {new_issue.key} - {item.get('summary', '')[:50]}")
            
            print(f"\n📊 Summary: {created} created, {updated} updated")
            
        except FileNotFoundError:
            print(f"Error: File not found: {input_file}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {input_file}")
            sys.exit(1)
        except JIRAError as e:
            print(f"Error importing issues: {e}")
            sys.exit(1)
    
    def generate_burndown(self, sprint_id: int, output_file: str = None):
        """Generate burndown chart for sprint."""
        if not MATPLOTLIB_AVAILABLE:
            print("Error: matplotlib not installed.")
            print("Install with: pip install matplotlib")
            sys.exit(1)
        
        try:
            # Get sprint details
            sprint = self.jira.sprint(sprint_id)
            
            # Get issues in sprint
            jql = f'sprint = {sprint_id}'
            issues = self.jira.search_issues(jql, maxResults=500)
            
            # Calculate total story points
            total_points = 0
            for issue in issues:
                if hasattr(issue.fields, 'customfield_10016') and issue.fields.customfield_10016:
                    total_points += issue.fields.customfield_10016
            
            # Get sprint dates
            start_date = datetime.fromisoformat(sprint.startDate.replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(sprint.endDate.replace('Z', '+00:00'))
            
            # Calculate ideal burndown (linear)
            sprint_days = (end_date - start_date).days
            ideal_burndown = [total_points - (total_points / sprint_days * i) for i in range(sprint_days + 1)]
            
            # Note: Actual burndown requires changelog data (complex)
            # For now, show ideal line
            
            # Create chart
            fig, ax = plt.subplots(figsize=(10, 6))
            
            days = list(range(sprint_days + 1))
            ax.plot(days, ideal_burndown, 'b--', label='Ideal Burndown', linewidth=2)
            
            ax.set_xlabel('Sprint Day')
            ax.set_ylabel('Story Points Remaining')
            ax.set_title(f'Sprint {sprint_id} Burndown Chart')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Save or show
            if output_file:
                plt.savefig(output_file, dpi=300, bbox_inches='tight')
                print(f"✅ Burndown chart saved to {output_file}")
            else:
                plt.show()
            
        except JIRAError as e:
            print(f"Error generating burndown: {e}")
            sys.exit(1)
    
    def calculate_velocity(self, project: str, num_sprints: int = 5):
        """Calculate team velocity for last N sprints."""
        try:
            # Get recent sprints
            board_id = self._get_board_id(project)
            sprints = self.jira.sprints(board_id, state='closed', maxResults=num_sprints)
            
            velocities = []
            
            print(f"\n📊 Velocity Analysis (Last {num_sprints} Sprints)\n")
            print(f"{'Sprint':<15} {'Committed':<12} {'Completed':<12} {'Velocity':<10}")
            print("-" * 50)
            
            for sprint in reversed(list(sprints)):
                jql = f'sprint = {sprint.id} AND status = Done'
                done_issues = self.jira.search_issues(jql, maxResults=500)
                
                velocity = 0
                for issue in done_issues:
                    if hasattr(issue.fields, 'customfield_10016') and issue.fields.customfield_10016:
                        velocity += issue.fields.customfield_10016
                
                velocities.append(velocity)
                
                # Count committed (all issues in sprint)
                jql_all = f'sprint = {sprint.id}'
                all_issues = self.jira.search_issues(jql_all, maxResults=500)
                committed = sum(
                    getattr(issue.fields, 'customfield_10016', 0) or 0
                    for issue in all_issues
                )
                
                print(f"{sprint.name:<15} {committed:<12.0f} {velocity:<12.0f} {velocity:<10.0f}")
            
            if velocities:
                avg_velocity = sum(velocities) / len(velocities)
                print("-" * 50)
                print(f"Average Velocity: {avg_velocity:.1f} points/sprint")
                
                # Calculate trend
                if len(velocities) >= 3:
                    recent_avg = sum(velocities[:3]) / 3
                    trend = "📈 Increasing" if recent_avg > avg_velocity else "📉 Decreasing"
                    print(f"Trend: {trend}")
                
                # Generate chart if matplotlib available
                if MATPLOTLIB_AVAILABLE:
                    self._plot_velocity_chart(velocities, avg_velocity)
            
        except JIRAError as e:
            print(f"Error calculating velocity: {e}")
            sys.exit(1)
    
    def _get_board_id(self, project: str) -> int:
        """Get board ID for project."""
        boards = self.jira.boards()
        for board in boards:
            if project.upper() in board.name.upper():
                return board.id
        
        # Default to first board
        if boards:
            return boards[0].id
        
        raise ValueError(f"No board found for project {project}")
    
    def _plot_velocity_chart(self, velocities: List[float], avg: float):
        """Plot velocity chart."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sprints = list(range(1, len(velocities) + 1))
        ax.bar(sprints, velocities, color='steelblue', alpha=0.7, label='Velocity')
        ax.axhline(y=avg, color='red', linestyle='--', linewidth=2, label=f'Average ({avg:.1f})')
        
        ax.set_xlabel('Sprint')
        ax.set_ylabel('Story Points Completed')
        ax.set_title('Team Velocity Trend')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Jira synchronization and automation tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  JIRA_URL      Jira instance URL (e.g., https://company.atlassian.net)
  JIRA_USER     Jira username/email
  JIRA_TOKEN    Jira API token

Commands:
  export        Export sprint or backlog issues
  import        Import/update issues from JSON
  burndown      Generate sprint burndown chart
  velocity      Calculate team velocity

Examples:
  python jira_sync.py export --project PROJ --sprint 5 --output sprint5.json
  python jira_sync.py export --project PROJ --backlog --output backlog.json
  python jira_sync.py import --file issues.json --project PROJ
  python jira_sync.py burndown --sprint 5 --output burndown.png
  python jira_sync.py velocity --project PROJ --sprints 6
        """
    )
    
    parser.add_argument('command', choices=['export', 'import', 'burndown', 'velocity'],
                       help='Command to execute')
    parser.add_argument('--url', help='Jira URL (or set JIRA_URL env var)')
    parser.add_argument('--user', help='Jira user (or set JIRA_USER env var)')
    parser.add_argument('--token', help='Jira token (or set JIRA_TOKEN env var)')
    parser.add_argument('--project', '-p', help='Project key (e.g., PROJ)')
    parser.add_argument('--sprint', '-s', type=int, help='Sprint ID')
    parser.add_argument('--backlog', action='store_true', help='Export backlog instead of sprint')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--file', '-f', help='Input file for import')
    parser.add_argument('--sprints', type=int, default=5, help='Number of sprints for velocity (default: 5)')
    parser.add_argument('--update', action='store_true', help='Update existing issues on import')
    
    args = parser.parse_args()
    
    # Initialize Jira connection
    sync = JiraSync(url=args.url, user=args.user, token=args.token)
    
    # Execute command
    if args.command == 'export':
        if not args.project:
            print("Error: --project required for export")
            sys.exit(1)
        if not args.output:
            print("Error: --output required for export")
            sys.exit(1)
        
        if args.backlog:
            sync.export_backlog(args.project, args.output)
        else:
            if not args.sprint:
                print("Error: --sprint required (or use --backlog)")
                sys.exit(1)
            sync.export_sprint(args.project, args.sprint, args.output)
    
    elif args.command == 'import':
        if not args.file:
            print("Error: --file required for import")
            sys.exit(1)
        if not args.project:
            print("Error: --project required for import")
            sys.exit(1)
        
        sync.import_issues(args.project, args.file, args.update)
    
    elif args.command == 'burndown':
        if not args.sprint:
            print("Error: --sprint required for burndown")
            sys.exit(1)
        
        sync.generate_burndown(args.sprint, args.output)
    
    elif args.command == 'velocity':
        if not args.project:
            print("Error: --project required for velocity")
            sys.exit(1)
        
        sync.calculate_velocity(args.project, args.sprints)


if __name__ == '__main__':
    main()
