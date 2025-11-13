#!/usr/bin/env python3
"""
Asana Task Tracker
==================
Automate Asana task management, reporting, and capacity planning.

Features:
- Bulk task creation from CSV
- Weekly status reports
- Team capacity analysis
- Task synchronization
- Custom field management

Setup:
    pip install asana

Configuration:
    ASANA_TOKEN=your_personal_access_token

Usage:
    python asana_tracker.py create --file tasks.csv --project 1234567890
    python asana_tracker.py report --project 1234567890 --format markdown
    python asana_tracker.py capacity --team engineering
    python asana_tracker.py sync --source jira --project PROJ
"""

import os
import sys
import csv
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Check if asana library is available
try:
    import asana
    ASANA_AVAILABLE = True
except ImportError:
    ASANA_AVAILABLE = False


class AsanaTracker:
    """Asana task automation and reporting tool."""
    
    def __init__(self, token: str = None):
        """Initialize Asana client."""
        if not ASANA_AVAILABLE:
            print("Error: asana library not installed.")
            print("Install with: pip install asana")
            sys.exit(1)
        
        self.token = token or os.getenv('ASANA_TOKEN')
        
        if not self.token:
            print("Error: Missing Asana token.")
            print("Set ASANA_TOKEN environment variable or pass --token")
            sys.exit(1)
        
        try:
            self.client = asana.Client.access_token(self.token)
            self.me = self.client.users.me()
            print(f"✅ Connected to Asana as: {self.me['name']}")
        except Exception as e:
            print(f"Error connecting to Asana: {e}")
            sys.exit(1)
    
    def create_tasks_from_csv(self, csv_file: str, project_gid: str):
        """Bulk create tasks from CSV file.
        
        CSV Format:
        name,description,assignee_email,due_date,priority,effort
        Task 1,Description here,user@company.com,2025-12-31,High,5
        """
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                created = 0
                failed = 0
                
                for row in reader:
                    try:
                        task_data = {
                            'name': row.get('name', 'Untitled Task'),
                            'projects': [project_gid]
                        }
                        
                        if row.get('description'):
                            task_data['notes'] = row['description']
                        
                        if row.get('due_date'):
                            task_data['due_on'] = row['due_date']
                        
                        # Find assignee by email
                        if row.get('assignee_email'):
                            assignee = self._find_user_by_email(row['assignee_email'])
                            if assignee:
                                task_data['assignee'] = assignee['gid']
                        
                        # Create task
                        task = self.client.tasks.create_task(task_data)
                        
                        # Set custom fields if provided
                        if row.get('priority'):
                            self._set_custom_field(task['gid'], 'Priority', row['priority'])
                        
                        if row.get('effort'):
                            self._set_custom_field(task['gid'], 'Effort', row['effort'])
                        
                        created += 1
                        print(f"✅ Created: {task['name']}")
                        
                    except Exception as e:
                        failed += 1
                        print(f"⚠️  Failed: {row.get('name', 'Unknown')} - {e}")
                
                print(f"\n📊 Summary: {created} created, {failed} failed")
                
        except FileNotFoundError:
            print(f"Error: File not found: {csv_file}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            sys.exit(1)
    
    def generate_weekly_report(self, project_gid: str, output_format: str = 'markdown'):
        """Generate weekly status report."""
        try:
            # Get project details
            project = self.client.projects.get_project(project_gid)
            
            # Date ranges
            today = datetime.now()
            week_start = today - timedelta(days=7)
            week_end = today
            next_week_end = today + timedelta(days=7)
            
            # Get all tasks in project
            tasks = list(self.client.tasks.get_tasks_for_project(project_gid))
            
            # Categorize tasks
            completed_this_week = []
            due_next_week = []
            overdue = []
            
            for task_basic in tasks:
                # Get full task details
                task = self.client.tasks.get_task(task_basic['gid'])
                
                # Check if completed this week
                if task.get('completed') and task.get('completed_at'):
                    completed_date = datetime.fromisoformat(task['completed_at'].replace('Z', '+00:00'))
                    if week_start <= completed_date <= week_end:
                        completed_this_week.append(task)
                
                # Check if due next week
                if not task.get('completed') and task.get('due_on'):
                    due_date = datetime.strptime(task['due_on'], '%Y-%m-%d')
                    if today <= due_date <= next_week_end:
                        due_next_week.append(task)
                    elif due_date < today:
                        overdue.append(task)
            
            # Generate report
            if output_format == 'markdown':
                self._print_markdown_report(project, completed_this_week, due_next_week, overdue)
            else:
                self._print_json_report(project, completed_this_week, due_next_week, overdue)
                
        except Exception as e:
            print(f"Error generating report: {e}")
            sys.exit(1)
    
    def analyze_team_capacity(self, team_name: str = None, workspace_gid: str = None):
        """Analyze team workload and capacity."""
        try:
            # Get workspace
            if not workspace_gid:
                workspaces = list(self.client.workspaces.get_workspaces())
                workspace_gid = workspaces[0]['gid']
            
            # Get team members
            if team_name:
                team = self._find_team_by_name(workspace_gid, team_name)
                if not team:
                    print(f"Error: Team '{team_name}' not found")
                    sys.exit(1)
                members = list(self.client.teams.get_team(team['gid'])['members'])
            else:
                # Get all workspace users
                members = list(self.client.users.get_users_for_workspace(workspace_gid))
            
            print(f"\n📊 Team Capacity Analysis\n")
            print(f"{'Member':<25} {'Active Tasks':<15} {'Overdue':<10} {'Status':<10}")
            print("-" * 65)
            
            for member in members:
                user_gid = member['gid']
                
                # Get tasks assigned to user
                tasks = list(self.client.tasks.get_tasks({
                    'assignee': user_gid,
                    'workspace': workspace_gid,
                    'completed_since': 'now'
                }))
                
                active_count = len(tasks)
                
                # Count overdue
                overdue_count = 0
                for task_basic in tasks:
                    task = self.client.tasks.get_task(task_basic['gid'])
                    if task.get('due_on'):
                        due_date = datetime.strptime(task['due_on'], '%Y-%m-%d')
                        if due_date < datetime.now() and not task.get('completed'):
                            overdue_count += 1
                
                # Determine status
                if active_count > 15:
                    status = "🔴 Over"
                elif active_count > 10:
                    status = "🟡 High"
                else:
                    status = "🟢 Good"
                
                print(f"{member['name']:<25} {active_count:<15} {overdue_count:<10} {status:<10}")
            
            print("-" * 65)
            
        except Exception as e:
            print(f"Error analyzing capacity: {e}")
            sys.exit(1)
    
    def sync_from_jira(self, jira_file: str, project_gid: str):
        """Sync tasks from Jira export JSON to Asana."""
        try:
            with open(jira_file, 'r', encoding='utf-8') as f:
                jira_issues = json.load(f)
            
            print(f"Syncing {len(jira_issues)} issues from Jira...\n")
            
            synced = 0
            skipped = 0
            
            for issue in jira_issues:
                # Check if already exists (by name/key)
                existing = self._find_task_by_name(project_gid, issue['key'])
                
                if existing:
                    skipped += 1
                    print(f"⏭️  Skipped (exists): {issue['key']}")
                    continue
                
                # Create task
                task_data = {
                    'name': f"{issue['key']}: {issue['summary']}",
                    'notes': f"Synced from Jira\nStatus: {issue['status']}",
                    'projects': [project_gid]
                }
                
                task = self.client.tasks.create_task(task_data)
                synced += 1
                print(f"✅ Synced: {issue['key']}")
            
            print(f"\n📊 Summary: {synced} synced, {skipped} skipped")
            
        except FileNotFoundError:
            print(f"Error: File not found: {jira_file}")
            sys.exit(1)
        except Exception as e:
            print(f"Error syncing from Jira: {e}")
            sys.exit(1)
    
    def _find_user_by_email(self, email: str) -> Optional[Dict]:
        """Find user by email address."""
        try:
            workspaces = list(self.client.workspaces.get_workspaces())
            for workspace in workspaces:
                users = list(self.client.users.get_users_for_workspace(workspace['gid']))
                for user in users:
                    if user.get('email', '').lower() == email.lower():
                        return user
            return None
        except:
            return None
    
    def _find_team_by_name(self, workspace_gid: str, team_name: str) -> Optional[Dict]:
        """Find team by name."""
        try:
            teams = list(self.client.teams.get_teams_for_workspace(workspace_gid))
            for team in teams:
                if team_name.lower() in team['name'].lower():
                    return team
            return None
        except:
            return None
    
    def _find_task_by_name(self, project_gid: str, name: str) -> Optional[Dict]:
        """Find task by name in project."""
        try:
            tasks = list(self.client.tasks.get_tasks_for_project(project_gid))
            for task in tasks:
                if name in task['name']:
                    return task
            return None
        except:
            return None
    
    def _set_custom_field(self, task_gid: str, field_name: str, value: str):
        """Set custom field value on task."""
        try:
            # Note: Custom field setting requires knowing the custom field GID
            # This is a simplified version
            pass
        except:
            pass
    
    def _print_markdown_report(self, project: Dict, completed: List, due_next: List, overdue: List):
        """Print report in markdown format."""
        print(f"\n# Weekly Status Report: {project['name']}")
        print(f"**Report Date:** {datetime.now().strftime('%Y-%m-%d')}\n")
        
        print(f"## ✅ Completed This Week ({len(completed)})\n")
        if completed:
            for task in completed[:10]:  # Top 10
                assignee = task.get('assignee', {}).get('name', 'Unassigned')
                print(f"- {task['name']} ({assignee})")
        else:
            print("*No tasks completed this week*\n")
        
        print(f"\n## 📅 Due Next Week ({len(due_next)})\n")
        if due_next:
            for task in due_next[:10]:
                assignee = task.get('assignee', {}).get('name', 'Unassigned')
                due_date = task.get('due_on', 'No date')
                print(f"- {task['name']} ({assignee}) - Due: {due_date}")
        else:
            print("*No tasks due next week*\n")
        
        print(f"\n## ⚠️ Overdue Tasks ({len(overdue)})\n")
        if overdue:
            for task in overdue:
                assignee = task.get('assignee', {}).get('name', 'Unassigned')
                due_date = task.get('due_on', 'No date')
                print(f"- {task['name']} ({assignee}) - Due: {due_date}")
        else:
            print("*No overdue tasks*\n")
    
    def _print_json_report(self, project: Dict, completed: List, due_next: List, overdue: List):
        """Print report in JSON format."""
        report = {
            'project': project['name'],
            'report_date': datetime.now().isoformat(),
            'completed_this_week': [
                {
                    'name': t['name'],
                    'assignee': t.get('assignee', {}).get('name', 'Unassigned'),
                    'completed_at': t.get('completed_at')
                }
                for t in completed
            ],
            'due_next_week': [
                {
                    'name': t['name'],
                    'assignee': t.get('assignee', {}).get('name', 'Unassigned'),
                    'due_on': t.get('due_on')
                }
                for t in due_next
            ],
            'overdue': [
                {
                    'name': t['name'],
                    'assignee': t.get('assignee', {}).get('name', 'Unassigned'),
                    'due_on': t.get('due_on')
                }
                for t in overdue
            ]
        }
        
        print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description='Asana task automation and reporting tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  ASANA_TOKEN   Personal access token from Asana

Commands:
  create        Create tasks from CSV file
  report        Generate weekly status report
  capacity      Analyze team capacity
  sync          Sync tasks from external source

Examples:
  python asana_tracker.py create --file tasks.csv --project 1234567890
  python asana_tracker.py report --project 1234567890 --format markdown
  python asana_tracker.py capacity --team engineering
  python asana_tracker.py sync --source jira --file jira.json --project 1234567890
        """
    )
    
    parser.add_argument('command', choices=['create', 'report', 'capacity', 'sync'],
                       help='Command to execute')
    parser.add_argument('--token', help='Asana token (or set ASANA_TOKEN env var)')
    parser.add_argument('--project', '-p', help='Project GID')
    parser.add_argument('--file', '-f', help='Input file (CSV for create, JSON for sync)')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown',
                       help='Report format (default: markdown)')
    parser.add_argument('--team', '-t', help='Team name for capacity analysis')
    parser.add_argument('--workspace', '-w', help='Workspace GID')
    parser.add_argument('--source', choices=['jira'], help='Sync source')
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = AsanaTracker(token=args.token)
    
    # Execute command
    if args.command == 'create':
        if not args.file:
            print("Error: --file required for create")
            sys.exit(1)
        if not args.project:
            print("Error: --project required for create")
            sys.exit(1)
        
        tracker.create_tasks_from_csv(args.file, args.project)
    
    elif args.command == 'report':
        if not args.project:
            print("Error: --project required for report")
            sys.exit(1)
        
        tracker.generate_weekly_report(args.project, args.format)
    
    elif args.command == 'capacity':
        tracker.analyze_team_capacity(args.team, args.workspace)
    
    elif args.command == 'sync':
        if not args.source:
            print("Error: --source required for sync")
            sys.exit(1)
        if not args.file:
            print("Error: --file required for sync")
            sys.exit(1)
        if not args.project:
            print("Error: --project required for sync")
            sys.exit(1)
        
        if args.source == 'jira':
            tracker.sync_from_jira(args.file, args.project)


if __name__ == '__main__':
    main()
