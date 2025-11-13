# PM Tools Mastery Guide

Comprehensive guide for configuring, using, and mastering project management tools across Jira, Asana, Trello, Monday, ClickUp, Linear, and Notion.

## Tool Selection Matrix

### Quick Decision Guide

```
Choose based on:

JIRA:
✅ Software development teams
✅ Complex workflows (10+ statuses)
✅ Advanced reporting needs
✅ Enterprise scale (100+ users)
✅ DevOps integration (CI/CD)
❌ Non-technical teams
❌ Simple task tracking
❌ Budget constraints

ASANA:
✅ Marketing/creative teams
✅ Cross-functional collaboration
✅ Portfolio management
✅ Medium complexity (5-50 people)
✅ Visual timeline needs
❌ Agile ceremonies
❌ Developer-specific features
❌ Offline access

TRELLO:
✅ Simple kanban workflows
✅ Visual task management
✅ Small teams (2-15 people)
✅ Quick setup (<1 hour)
✅ Low budget
❌ Complex dependencies
❌ Gantt charts
❌ Advanced reporting

MONDAY.COM:
✅ All-in-one platform
✅ Heavy customization needs
✅ Multiple departments
✅ Visual dashboards
✅ CRM integration
❌ Budget-conscious
❌ Agile-specific features
❌ Simple needs

CLICKUP:
✅ Budget-friendly all-in-one
✅ Multiple view types needed
✅ Built-in docs/wikis
✅ Time tracking
✅ Flexible workflows
❌ Enterprise security
❌ Simplicity preference
❌ Minimal learning curve

LINEAR:
✅ Engineering teams
✅ Fast UI priority
✅ Git integration
✅ Keyboard-first users
✅ Cycle-based planning
❌ Non-technical teams
❌ Waterfall projects
❌ Visual preference

NOTION:
✅ Documentation-heavy
✅ Relational databases
✅ Wikis + PM combined
✅ Customization needs
✅ Small-medium teams
❌ Real-time collaboration
❌ Mobile-first users
❌ Structured workflows
```

### Cost Comparison (2025)

| Tool      | Free Tier          | Paid (per user/month) | Enterprise |
|-----------|--------------------|-----------------------|------------|
| Jira      | 10 users           | $7.75 Standard        | $16        |
| Asana     | 15 users           | $10.99 Premium        | Custom     |
| Trello    | Unlimited          | $5 Standard           | $17.50     |
| Monday    | 3 seats            | $9 Basic              | Custom     |
| ClickUp   | Unlimited tasks    | $7 Unlimited          | $19        |
| Linear    | Unlimited viewers  | $8 Standard           | Custom     |
| Notion    | Unlimited blocks   | $8 Plus               | $15        |

---

## Jira Advanced

### Project Setup

**Create Scrum Project:**
```
1. Projects → Create Project
2. Select "Scrum" template
3. Configure:
   ├─ Project Name
   ├─ Project Key (e.g., PROJ)
   ├─ Project Lead
   └─ Default Assignee
```

**Board Configuration:**
```
Board Settings:
├─ Columns:
│  ├─ To Do (Backlog, Selected for Development)
│  ├─ In Progress (In Progress)
│  ├─ In Review (In Review, In QA)
│  └─ Done (Done)
│
├─ Swimlanes:
│  ├─ By Priority (Critical → Low)
│  ├─ By Assignee
│  └─ By Epic
│
├─ Card Layout:
│  ├─ Show: Story Points, Assignee, Priority
│  └─ Card Colors: By Issue Type
│
├─ Estimation:
│  ├─ Story Points (Fibonacci)
│  └─ Time Tracking (optional)
│
└─ Quick Filters:
   ├─ My Issues
   ├─ Recently Updated
   └─ Only Bugs
```

### Issue Types & Workflows

**Standard Hierarchy:**
```
Epic (High-level feature)
├─ Story (User story)
│  └─ Subtask (Breakdown)
├─ Bug (Defect)
└─ Task (Non-story work)
```

**Custom Workflow Example:**
```
TO DO
  ↓
IN PROGRESS
  ↓
CODE REVIEW
  ↓ (Approved)
IN QA
  ↓ (Passed)
READY FOR RELEASE
  ↓ (Deployed)
DONE

Transitions:
- To Do → In Progress: "Start Work"
- In Progress → Code Review: "Submit PR"
- Code Review → In Progress: "Request Changes"
- Code Review → In QA: "Approve"
- In QA → In Progress: "Fail QA"
- In QA → Ready: "Pass QA"
- Ready → Done: "Deploy"
```

### JQL Mastery

**Essential Queries:**

```jql
# My open issues
assignee = currentUser() AND resolution = Unresolved ORDER BY priority DESC

# Sprint burndown
project = PROJ AND sprint = 5 AND resolution = Unresolved

# Overdue tasks
duedate < now() AND resolution = Unresolved

# Critical bugs
type = Bug AND priority = Critical ORDER BY created DESC

# Recently completed
project = PROJ AND status = Done AND resolved >= -7d

# Blocked issues
status = Blocked OR labels = blocked

# Epics without stories
type = Epic AND issueFunction in linkedIssuesOf("type = Story") = 0

# Velocity data (last 5 sprints)
project = PROJ AND sprint in closedSprints() AND sprint >= -5 AND resolution = Done

# Technical debt
labels = tech-debt AND resolution = Unresolved ORDER BY priority DESC

# Story points by assignee
project = PROJ AND sprint = 5 GROUP BY assignee
```

**Advanced Filters:**

```jql
# Complex query with multiple conditions
project = PROJ 
  AND sprint = 5 
  AND (
    (type = Story AND "Story Points" > 5)
    OR (type = Bug AND priority = High)
  )
  AND assignee in (user1, user2)
  AND labels not in (tech-debt, spike)
  ORDER BY priority DESC, created ASC
```

### Automation Rules

**Auto-assign when moved:**
```
Trigger: Issue transitioned to "In Review"
Condition: Issue type = Story OR Bug
Action: Assign to Reporter
```

**Auto-close parent when subtasks done:**
```
Trigger: Issue transitioned to Done
Condition: Is subtask
Action: If parent has all subtasks done → Transition parent to Done
```

**Slack notification for critical bugs:**
```
Trigger: Issue created
Condition: Type = Bug AND Priority = Critical
Action: Send Slack message to #engineering
        Message: "🚨 Critical bug: {{issue.key}} - {{issue.summary}}"
```

**Auto-transition on PR merge:**
```
Trigger: Development → PR merged
Condition: Status = "In Review"
Action: Transition to "In QA"
        Add comment: "PR merged, ready for QA"
```

**Sprint start reminder:**
```
Trigger: Scheduled (Every Monday 9 AM)
Action: Send email to team
        Subject: "Sprint Planning at 10 AM"
```

### Custom Fields

**Essential Fields:**

1. **Story Points** (Number)
   - Fibonacci scale: 1, 2, 3, 5, 8, 13, 21
   - For velocity tracking

2. **Sprint** (Sprint picker)
   - Auto-assigned to active sprint
   - Backlog if unassigned

3. **Effort (T-Shirt Size)** (Select)
   - Options: XS, S, M, L, XL, XXL
   - For rough estimation

4. **Risk Level** (Select)
   - Options: Low, Medium, High
   - For risk tracking

5. **Business Value** (Number)
   - Score: 1-100
   - For prioritization

6. **Blocked By** (Issue Link)
   - Custom link type
   - For dependency tracking

### Dashboard Gadgets

**Sprint Health Dashboard:**

```
Layout:
┌──────────────┬──────────────┐
│ Sprint       │ Velocity     │
│ Burndown     │ Chart        │
├──────────────┼──────────────┤
│ Issue        │ Assigned     │
│ Statistics   │ to Me        │
├──────────────┴──────────────┤
│ Created vs Resolved Chart   │
└─────────────────────────────┘
```

**Available Gadgets:**
- Sprint Burndown Chart
- Velocity Chart
- Epic Burndown
- Pie Chart (status, assignee, priority)
- Filter Results (saved JQL)
- Issue Statistics
- Activity Stream
- Road Map
- Two-Dimensional Filter Statistics

### Integration & APIs

**GitHub Integration:**
```
Setup:
1. Jira Settings → Apps → GitHub
2. Connect GitHub account
3. Authorize repositories

Usage:
# In commit message
git commit -m "Add login API [PROJ-123]"
# Updates PROJ-123 → "In Progress"

# Close issue
git commit -m "Fix auth bug, closes PROJ-124"
# Transitions PROJ-124 → "Done"
```

**Slack Integration:**
```
Setup:
1. Jira Settings → Apps → Slack
2. Connect workspace
3. Configure channels

Commands:
/jira create    → Create issue from Slack
/jira assign    → Assign issue
/jira comment   → Add comment
/jira transition → Change status
```

**Python API:**
```python
from jira import JIRA

jira = JIRA('https://company.atlassian.net', basic_auth=('user', 'token'))

# Create issue
issue = jira.create_issue(
    project='PROJ',
    summary='New feature',
    description='Details here',
    issuetype={'name': 'Story'},
    customfield_10016=5  # Story points
)

# Search issues
issues = jira.search_issues('project=PROJ AND sprint=5')

# Transition issue
jira.transition_issue(issue, 'In Progress')

# Add comment
jira.add_comment(issue, 'Work started')
```

---

## Asana Pro

### Project Structure

**Portfolio → Project → Section → Task → Subtask**

```
Portfolio: Product Development
├─ Project: Q1 2025 Features
│  ├─ Section: Sprint 1
│  │  ├─ Task: User authentication
│  │  │  ├─ Subtask: Design login UI
│  │  │  ├─ Subtask: Implement backend
│  │  │  └─ Subtask: Write tests
│  │  └─ Task: Profile management
│  └─ Section: Sprint 2
└─ Project: Bug Fixes
```

### Project Templates

**Scrum Sprint Template:**
```
Sections:
├─ Backlog (Prioritized stories)
├─ Sprint Planning (Selected for sprint)
├─ In Progress (WIP limit: 5)
├─ In Review (Code review + QA)
└─ Done (Completed this sprint)

Custom Fields:
├─ Story Points (Number: 1, 2, 3, 5, 8)
├─ Priority (Dropdown: P0-P3)
├─ Sprint (Text: Sprint 5)
└─ Effort (Dropdown: S/M/L/XL)

Task Template:
Title: [Type] Short description
Description:
  User Story: As a [user], I want [feature] so that [benefit]
  Acceptance Criteria:
  - [ ] Criterion 1
  - [ ] Criterion 2
  - [ ] Criterion 3
  Dependencies: [Link tasks]
  Subtasks:
  - Design
  - Implement
  - Test
```

**Waterfall Project Template:**
```
Sections:
├─ 1. Initiation
│  ├─ Project charter
│  └─ Stakeholder identification
├─ 2. Planning
│  ├─ Requirements
│  ├─ WBS
│  └─ Risk register
├─ 3. Execution
│  ├─ Development
│  └─ Testing
├─ 4. Monitoring
│  ├─ Status reports
│  └─ Change requests
└─ 5. Closure
   ├─ Final deliverables
   └─ Lessons learned

Custom Fields:
├─ Phase (Dropdown)
├─ Milestone (Checkbox)
├─ Budget ($)
└─ RAG Status (Dropdown: Green/Yellow/Red)
```

### Custom Fields

**Essential Fields:**

1. **Priority** (Dropdown)
   ```
   P0 - Critical (Fix immediately)
   P1 - High (This sprint)
   P2 - Medium (Next sprint)
   P3 - Low (Backlog)
   ```

2. **Effort** (Dropdown)
   ```
   S - Small (1-2 days)
   M - Medium (3-5 days)
   L - Large (1-2 weeks)
   XL - Extra Large (>2 weeks, split!)
   ```

3. **Status** (Dropdown)
   ```
   Not Started
   In Progress
   Blocked
   In Review
   Complete
   ```

4. **Sprint** (Text)
   ```
   Sprint 1, Sprint 2, etc.
   Or: 2025-Q1-S1, 2025-Q1-S2
   ```

5. **Story Points** (Number)
   ```
   Fibonacci: 1, 2, 3, 5, 8, 13
   ```

### Task Dependencies

**Types:**
- **Waiting on** (This task blocked by another)
- **Blocking** (This task blocks another)

**Setup:**
```
Task A: Implement API
  ↓ (Blocking)
Task B: Build UI (Waiting on Task A)
  ↓ (Blocking)
Task C: Integration Test (Waiting on Task B)
```

**Dependency Rules:**
1. Don't create circular dependencies
2. Keep chains manageable (<5 levels)
3. Review critical path weekly
4. Mark blocked tasks clearly

### Timeline (Gantt) View

**Setup:**
```
1. Click "Timeline" tab
2. Add tasks with dates
3. Show dependencies
4. Color-code by:
   - Assignee
   - Section
   - Custom field (Priority)
```

**Best Practices:**
- Add milestones (diamond markers)
- Set dependencies visually (drag lines)
- Group by project/section
- Use color for status (green/yellow/red)
- Export to PDF for stakeholders

### Automation Rules

**Rule 1: Auto-move to "In Review" when subtasks done**
```
Trigger: All subtasks completed
Action: Move to section "In Review"
        Add comment: "All subtasks complete, ready for review"
```

**Rule 2: Assign to PM when blocked**
```
Trigger: Custom field "Status" changed to "Blocked"
Action: Assign to [PM Name]
        Add follower: [Scrum Master]
```

**Rule 3: Create follow-up task**
```
Trigger: Task moved to "Done"
Condition: Has tag "Needs Follow-up"
Action: Create new task in "Backlog"
        Title: "Follow-up: [Original Task Name]"
        Assign to: Original Assignee
```

**Rule 4: Sprint closure reminder**
```
Trigger: Task due date approaches (2 days before)
Condition: Section = "In Progress"
Action: Send notification to assignee
        Add comment: "⏰ Sprint ends in 2 days"
```

### Forms for Intake

**Bug Report Form:**
```
Fields:
- Title (Short text)
- Description (Long text)
- Steps to Reproduce (Long text)
- Expected vs Actual (Long text)
- Severity (Dropdown: Critical/High/Medium/Low)
- Environment (Dropdown: Prod/Staging/Dev)
- Screenshots (File upload)

Submission Action:
→ Create task in "Bug Triage" project
→ Assign to QA Lead
→ Add tag "New Bug"
```

**Feature Request Form:**
```
Fields:
- Feature Name
- Business Justification
- User Story
- Acceptance Criteria
- Priority (Requestor's view)
- Impacted Users

Submission Action:
→ Create task in "Feature Backlog"
→ Assign to Product Owner
→ Send confirmation email
```

### Workload Management

**View Team Capacity:**
```
1. Go to project → Workload tab
2. Set capacity: Hours per week per person
3. View allocation:
   - Green: Under capacity
   - Yellow: At capacity
   - Red: Over-allocated
```

**Balance Workload:**
- Drag tasks between people
- Adjust task durations
- Defer low-priority work
- Add resources if needed

### Reporting

**Status Report:**
```
1. Create Portfolio
2. Add projects to portfolio
3. View Progress tab
4. Export to PDF/CSV
```

**Custom Chart:**
```
1. Chart → Add chart
2. Select:
   - X-axis: Due date
   - Y-axis: Count of tasks
   - Group by: Status
3. Filter: Custom field "Priority" = P0, P1
4. Add to Dashboard
```

**CSV Export:**
```
1. List view → Export CSV
2. Columns include:
   - Task name
   - Assignee
   - Due date
   - Custom fields
   - Status
3. Open in Excel for analysis
```

---

## Trello Advanced

### Board Structure

**Sprint Board:**
```
Lists:
├─ Backlog (Prioritized top-to-bottom)
├─ Sprint Backlog (Selected for sprint)
├─ In Progress (WIP limit: 5 cards)
├─ Review (Code review + QA)
├─ Done (This sprint)
└─ Archived (Previous sprints)
```

**Kanban Board:**
```
Lists:
├─ Icebox (Ideas, low priority)
├─ Backlog (Ready to start)
├─ To Do (Next up)
├─ Doing (WIP: 3 cards max)
├─ Review
└─ Done
```

### Power-Ups (Essential)

**1. Calendar**
- Visualize due dates
- Drag-and-drop to reschedule
- Sync with Google Calendar

**2. Butler (Automation)**
```
Free tier: 250 actions/month
Paid: Unlimited

Examples:
- "When a card is moved to Done, archive it after 7 days"
- "Every Monday at 9 AM, create a card in 'To Do' named 'Weekly planning'"
- "When due date is in 1 day, add red label"
```

**3. Custom Fields**
```
Add metadata to cards:
- Story Points (Number)
- Priority (Dropdown: P0-P3)
- Effort (Text: S/M/L/XL)
- Sprint (Text: Sprint 5)
```

**4. Card Repeater**
```
Create recurring tasks:
- Daily standup (Every weekday)
- Sprint planning (Every 2 weeks)
- Monthly retrospective
```

**5. Voting**
```
Team prioritization:
- Enable voting on cards
- Sort by votes
- Discuss top-voted items
```

### Butler Automation

**Examples:**

```
# Archive done cards weekly
Schedule: Every Sunday at midnight
Command: archive all cards in list "Done" older than 7 days

# Auto-label by due date
Card Rule: when the due date is in less than 1 day, add the red label

# Move to review when checklist complete
Card Button: 
  Name: "✅ Ready for Review"
  Actions:
  - Check all items in checklist "Tasks"
  - Move card to list "Review"
  - Add comment "Moved to review by {username}"

# Daily standup reminder
Schedule: Every weekday at 9:00 AM
Command: post comment "🗣️ Daily standup in 30 minutes! https://zoom.us/j/123456" to all cards in list "In Progress"

# Sprint closure
Due Date: when the due date is today
Command:
- Move card to list "Done"
- Add green label
- Archive after 1 day
```

### Card Templates

**User Story Template:**
```
Title: [US] Short description

Description:
🎯 User Story:
As a [user type]
I want [feature]
So that [benefit]

📋 Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

🔗 Dependencies:
- Link to related cards

📊 Story Points: [TBD]

Labels: story, sprint-5
```

**Bug Template:**
```
Title: [BUG] Short description

Description:
🐛 Summary:
[Brief description]

📝 Steps to Reproduce:
1. Step 1
2. Step 2
3. Step 3

✅ Expected:
[What should happen]

❌ Actual:
[What actually happens]

🔧 Environment:
- OS: 
- Browser:
- Version:

📸 Screenshots:
[Attach here]

Labels: bug, severity-high
```

### Labels System

**Standard Labels:**
```
Priority:
🔴 P0 - Critical
🟠 P1 - High
🟡 P2 - Medium
🟢 P3 - Low

Type:
🎯 Story
🐛 Bug
⚙️ Task
💡 Spike

Sprint:
📅 Sprint-1
📅 Sprint-2

Status:
🚧 Blocked
⏳ Waiting
✅ Ready
```

### Integrations

**Slack:**
```
Setup: Power-Ups → Slack
Actions:
- Send card to Slack channel
- Create card from Slack message
- Notifications on card updates
```

**GitHub:**
```
Setup: Power-Ups → GitHub
Features:
- Attach PR to card
- Show PR status
- Link commits
```

**Google Drive:**
```
Setup: Power-Ups → Google Drive
Features:
- Attach Drive files
- Create new docs from card
- View files inline
```

### Export & Reporting

**Export Options:**
```
1. JSON (Full backup)
   Board Menu → More → Print and Export → Export JSON

2. CSV (For analysis)
   Board Menu → More → Print and Export → Export CSV

3. PDF (For stakeholders)
   Board Menu → More → Print and Export → Print
```

**Analytics:**
- Use exported CSV in Excel
- Track cycle time (date moved to "Doing" → "Done")
- Burndown: Count cards in "Done" daily
- Velocity: Story points completed per sprint

---

## Monday.com

### Board Types

**1. Scrum Board**
```
Groups:
├─ Backlog
├─ Sprint Planning
├─ Sprint 5 (Current)
├─ In Progress
└─ Done

Columns:
├─ Task (Text)
├─ Assignee (Person)
├─ Status (Status: To Do/Doing/Done)
├─ Story Points (Number)
├─ Priority (Priority: Critical/High/Medium/Low)
├─ Sprint (Dropdown)
└─ Effort (Dropdown: S/M/L/XL)
```

**2. Roadmap Board**
```
Groups:
├─ Q1 2025
├─ Q2 2025
├─ Q3 2025
└─ Q4 2025

Columns:
├─ Feature (Text)
├─ Owner (Person)
├─ Status (Timeline: Planning/In Progress/Done)
├─ Timeline (Date range)
├─ Progress (Progress bar 0-100%)
└─ Confidence (Dropdown: High/Medium/Low)
```

**3. Bug Tracking**
```
Columns:
├─ Bug ID (Auto-number)
├─ Title (Text)
├─ Severity (Status: Critical/High/Medium/Low)
├─ Status (Status: New/Investigating/Fixed/Closed)
├─ Assignee (Person)
├─ Reported By (Person)
├─ Created Date (Date)
└─ Resolution (Long text)
```

### Automations

**Recipe 1: Status-based notifications**
```
When status changes to Stuck
→ Notify PM
→ Move to group "Blocked"
```

**Recipe 2: Deadline reminder**
```
When deadline approaches (2 days before)
→ Notify assignee
→ Add label "Due Soon"
```

**Recipe 3: Dependency management**
```
When status of item "Task A" changes to Done
→ Notify assignee of item "Task B"
→ Move "Task B" to group "Ready to Start"
```

**Recipe 4: Sprint closure**
```
When sprint end date arrives
→ Move all items with status "Done" to group "Archive"
→ Send summary to stakeholders
```

**Recipe 5: Auto-assign**
```
When item is created in group "Backlog"
→ Assign to Product Owner
→ Set status to "Needs Triage"
```

### Dashboards

**Sprint Dashboard:**
```
Widgets:
├─ Chart: Burndown (Story points by date)
├─ Battery: Sprint progress (% complete)
├─ Numbers: Total stories, Completed, Remaining
├─ Chart: Velocity (Last 5 sprints)
└─ Table: Current sprint tasks
```

**Portfolio Dashboard:**
```
Widgets:
├─ Timeline: Roadmap view (all projects)
├─ Chart: Budget vs Actual (per project)
├─ Chart: Projects by status (pie chart)
├─ Numbers: Total projects, On track, At risk
└─ Workload: Resource allocation
```

### Integrations

**Jira Sync:**
```
Setup: Integrations → Jira
Sync:
- Jira issues → Monday items
- Bi-directional status updates
- Comment sync
```

**Slack:**
```
Commands:
/monday create → Create item
/monday update → Update status
/monday search → Find items
```

**GitHub:**
```
Features:
- PR status in Monday
- Link commits to items
- Auto-update status on PR merge
```

**Zoom:**
```
Features:
- Schedule meetings from board
- Add Zoom links to items
- Track meeting attendance
```

### Views

**Kanban:**
- Group by: Status column
- Drag-and-drop between columns
- WIP limits (visual only)

**Timeline (Gantt):**
- Show dependencies
- Critical path (manual)
- Export to PDF

**Calendar:**
- View items by due date
- Drag to reschedule
- Color-code by group

**Workload:**
- Capacity per person (hours/week)
- Allocate tasks
- Balance workload

**Chart:**
- Burndown, velocity, status distribution
- Custom X/Y axes
- Filter by group, status, assignee

---

## ClickUp Mastery

### Hierarchy

```
Workspace (Company)
└─ Space (Department)
   └─ Folder (Project)
      └─ List (Sprint/Phase)
         └─ Task
            └─ Subtask
               └─ Checklist Item
```

**Example:**
```
Tech Company
└─ Engineering
   └─ Product Launch
      └─ Sprint 5
         └─ User Authentication
            └─ Implement OAuth
               ├─ Set up Auth0
               ├─ Create login endpoint
               └─ Write tests
```

### Multiple Views

**List View** (Default)
- Rows of tasks
- Quick edit inline
- Best for: Detailed work

**Board View** (Kanban)
- Columns by status
- Drag-and-drop
- Best for: Visual workflow

**Gantt View**
- Timeline bars
- Dependencies
- Best for: Project planning

**Calendar View**
- Tasks by due date
- Drag to reschedule
- Best for: Deadline tracking

**Timeline View**
- Week/month view
- Resource planning
- Best for: Capacity planning

**Table View** (Database)
- Spreadsheet interface
- Sort, filter, group
- Best for: Data analysis

**Mind Map**
- Brainstorming
- Task relationships
- Best for: Planning

**Workload View**
- Capacity per person
- Time estimates
- Best for: Resource management

### Custom Fields

**Essential Fields:**

1. **Story Points** (Number)
   - Default: 0
   - Use for: Velocity tracking

2. **Sprint** (Dropdown)
   - Options: Sprint 1, Sprint 2, ...
   - Use for: Filtering

3. **Effort** (Dropdown)
   - Options: XS, S, M, L, XL
   - Use for: Rough estimation

4. **Priority** (Dropdown)
   - Options: Critical, High, Medium, Low
   - Use for: Prioritization

5. **Risk** (Dropdown)
   - Options: High, Medium, Low
   - Use for: Risk tracking

6. **Progress** (Progress bar)
   - Auto-calculate from subtasks
   - Use for: Visual tracking

### Time Tracking

**Built-in Timer:**
```
1. Click timer icon on task
2. Start/stop timer
3. View time tracked
4. Generate timesheets
```

**Time Estimates:**
```
- Set estimate: e.g., 4h
- Track actual: Timer auto-tracks
- View variance: Estimate vs Actual
- Report: Time tracking report
```

**Billable Time:**
- Mark time as billable
- Set hourly rates per person
- Generate invoices

### Docs & Wikis

**Use Cases:**
- Meeting notes
- Requirements docs
- Retrospective notes
- Knowledge base

**Features:**
- Markdown support
- Link to tasks
- Embed views (tasks, charts)
- Templates

**Example: Sprint Retrospective Doc**
```markdown
# Sprint 5 Retrospective

**Date:** Mar 14, 2025
**Attendees:** [Linked users]

## What Went Well 😊
- Story A completed early
- Good team collaboration

## What Didn't Go Well 😞
- Story B blocked by API issues
- Underestimated complexity

## Action Items
[Embed task view: List "Retro Actions"]

## Metrics
[Embed chart: Velocity trend]
```

### Automations

**Trigger Types:**
- Status changed
- Assignee changed
- Due date changed
- Priority changed
- Custom field changed
- Time tracked
- Task created/moved

**Action Types:**
- Change status
- Assign task
- Move to list
- Create task
- Add comment
- Send email
- Webhook

**Examples:**

```
# Auto-assign on status change
When status changes to In Review
→ Assign to QA Lead
→ Add comment "Ready for testing"

# Create follow-up task
When task moved to Done
And has tag "Needs Follow-up"
→ Create task in Backlog
→ Assign to same assignee

# Sprint closure
When list "Sprint 5" due date arrives
→ Move all Done tasks to Archive
→ Send email to team with summary
```

### Integrations

**GitHub:**
- Link PRs to tasks
- Auto-update status on merge
- Show commit history

**Slack:**
- Task notifications in channels
- Create tasks from Slack
- Daily summaries

**Time Tracking:**
- Toggl, Harvest, Everhour
- Sync time entries
- Unified reporting

**Zapier:**
- Connect to 3000+ apps
- Custom workflows
- Advanced automations

### Goals (OKRs)

**Structure:**
```
Goal: Increase User Engagement
├─ Key Result 1: 50% MAU growth
│  └─ Tasks: [Linked tasks]
├─ Key Result 2: 4.5* app rating
│  └─ Tasks: [Linked tasks]
└─ Key Result 3: 20% feature adoption
   └─ Tasks: [Linked tasks]
```

**Tracking:**
- Set targets (number, boolean, currency, task)
- Auto-update from tasks
- Progress bars
- Due dates

---

## Linear Advanced

### Cycle-Based Planning

**Concept:** Similar to sprints, but more flexible

**Setup:**
```
1. Settings → Cycles
2. Duration: 1-2 weeks (typically 2)
3. Start day: Monday
4. Auto-archive: After 1 cycle
```

**Workflow:**
```
Create Cycle:
1. Start new cycle
2. Set team capacity (optional)
3. Move issues from Backlog
4. Assign to team members
5. Track progress (auto burndown)
6. Complete cycle
7. Review stats
```

### Keyboard-First Navigation

**Essential Shortcuts:**
```
C         → Create issue
/         → Quick search
K         → Command palette
Cmd+K     → Quick switcher
E         → Set status
A         → Assign
L         → Set label
P         → Set priority
Shift+P   → Set project
D         → Set due date
R         → Add relation
Z         → Add to cycle

Views:
1-9       → Switch to saved view
V         → View picker
G I       → Go to Inbox
G M       → Go to My Issues
G A       → Go to All Issues
```

**Power User Tips:**
- Use Cmd+K → Type issue ID → Enter (instant navigation)
- Press E → Type status → Enter (instant update)
- Use Quick Actions (/) in issue description

### Git Integration

**Branch Auto-Creation:**
```
Linear: Click "Create branch" on issue
→ Generates: feature/LIN-123-implement-login
→ Opens in GitHub/GitLab
```

**Commit Integration:**
```
# In commit message
git commit -m "Implement login API [LIN-123]"

→ Linear auto-updates LIN-123:
   - Status → "In Progress"
   - Adds commit link
   - Shows in activity

# Close issue
git commit -m "Fix auth bug, closes LIN-124"

→ Linear auto-closes LIN-124
```

**PR Status:**
- Shows PR status in Linear
- Draft, Open, Merged
- Link to PR
- Auto-transitions on merge

### Triage Workflow

**Concept:** Process incoming issues efficiently

**Setup:**
```
1. Create "Triage" view
2. Filter: Status = Triage
3. Sort by: Created date (oldest first)
```

**Process:**
```
For each issue:
1. Read description
2. Set priority (P0-P3)
3. Set project
4. Assign if clear owner
5. Add labels
6. Move to Backlog or Cycle
7. Next issue (Cmd+Down)
```

**Batch Operations:**
- Select multiple (Shift+Click)
- Bulk assign (A)
- Bulk label (L)
- Bulk project (Shift+P)

### Views

**Custom Views:**
```
Examples:
- My Active Issues
  Filter: Assignee = Me, Status != Done, Canceled
  
- This Cycle
  Filter: Cycle = Current
  
- Bugs by Priority
  Filter: Label = Bug
  Sort: Priority descending
  
- Blocked Issues
  Filter: Label = Blocked
  
- Needs Estimation
  Filter: Estimate = None, Status = Backlog
```

**Sharing Views:**
- Save view
- Share link with team
- Pin to sidebar
- Team-wide views

### Roadmap

**Structure:**
```
Projects (High-level features)
├─ Milestones (Key dates)
└─ Issues (Linked)

Example:
Project: User Management
├─ Milestone: Q1 Launch (Mar 31)
└─ Issues:
   ├─ LIN-123: Authentication
   ├─ LIN-124: Profile management
   └─ LIN-125: Permissions
```

**Timeline View:**
- Visual roadmap
- Drag milestones
- Show dependencies
- Export to PDF

### Labels & Priorities

**Label System:**
```
Type:
- bug
- feature
- improvement
- task

Area:
- backend
- frontend
- design
- infrastructure

Status:
- blocked
- needs-review
- ready

Custom:
- tech-debt
- security
- performance
```

**Priority Levels:**
```
No Priority (default)
Low          → Nice to have
Medium       → Important
High         → Should do this cycle
Urgent       → Drop everything
```

---

## Notion PM Setup

### Database Structure

**Projects Database (Master):**
```
Properties:
├─ Name (Title)
├─ Status (Select: Planning/Active/On Hold/Complete)
├─ PM (Person)
├─ Start Date (Date)
├─ End Date (Date)
├─ Budget (Number: $)
├─ Budget Used (Formula)
├─ Progress (Progress: 0-100%)
├─ Priority (Select: P0/P1/P2/P3)
├─ Tasks (Relation → Tasks DB)
├─ Risks (Relation → Risks DB)
├─ Meetings (Relation → Meetings DB)
└─ Docs (Relation → Docs DB)

Rollups:
├─ Total Tasks (Rollup: Count of Tasks)
├─ Done Tasks (Rollup: Count where Status = Done)
├─ Open Risks (Rollup: Count where Status = Open)
└─ Budget Spent (Rollup: Sum of Task Costs)
```

**Tasks Database (Detail):**
```
Properties:
├─ Task (Title)
├─ Project (Relation ← Projects)
├─ Status (Select: To Do/In Progress/Review/Done)
├─ Assignee (Person)
├─ Due Date (Date)
├─ Story Points (Number)
├─ Sprint (Select: Sprint 1, Sprint 2...)
├─ Priority (Select)
├─ Dependencies (Relation → Tasks)
├─ Subtasks (Relation → Tasks, self-reference)
└─ Cost (Number: $)

Formulas:
├─ Overdue (if(prop("Due Date") < now() and prop("Status") != "Done", "⚠️", ""))
├─ Days Left (dateBetween(prop("Due Date"), now(), "days"))
└─ Status Color (if(prop("Status") == "Done", "🟢", "🟡"))
```

**Risks Database:**
```
Properties:
├─ Risk (Title)
├─ Project (Relation ← Projects)
├─ Probability (Select: High/Med/Low)
├─ Impact (Select: High/Med/Low)
├─ Risk Score (Formula: Probability × Impact)
├─ Status (Select: Open/Mitigated/Closed)
├─ Owner (Person)
├─ Mitigation Plan (Long text)
└─ Last Reviewed (Date)

Formula (Risk Score):
if(prop("Probability") == "High", 3,
   if(prop("Probability") == "Med", 2, 1))
×
if(prop("Impact") == "High", 3,
   if(prop("Impact") == "Med", 2, 1))
```

### Templates

**Sprint Planning Template:**
```
# Sprint 5 Planning

## Sprint Goal
[One-sentence goal]

## Capacity
- Team size: 5 developers
- Sprint duration: 2 weeks
- Capacity: 150 points (30 per dev × 5)

## Sprint Backlog
[Linked database view: Tasks where Sprint = Sprint 5]

## Dependencies
[List external dependencies]

## Risks
[Linked database view: Risks relevant to Sprint 5]

## Definition of Done
- [ ] Code reviewed
- [ ] Tests written
- [ ] Deployed to staging
- [ ] QA approved
- [ ] Documentation updated
```

**Project Charter Template:**
```
# [Project Name]

## Executive Summary
[2-3 paragraphs]

## Business Objectives
- Objective 1
- Objective 2
- Objective 3

## Scope
**In Scope:**
- Feature A
- Feature B

**Out of Scope:**
- Feature C
- Feature D

## Stakeholders
[Table with Name, Role, Interest, Power]

## Timeline
- Start: [Date]
- End: [Date]
- Key Milestones: [List]

## Budget
- Approved: $X
- Contingency: $Y (10%)
- Total: $X+Y

## Success Criteria
- Criterion 1
- Criterion 2

## Risks
[Linked database view: Top 5 risks]
```

### Views & Filters

**Task Views:**

1. **Kanban (By Status)**
   ```
   Grouped by: Status
   Filter: Project = Current
   Sort: Priority descending
   ```

2. **Sprint Board**
   ```
   Grouped by: Sprint
   Filter: Sprint in (Sprint 5, Sprint 6)
   Sort: Priority descending
   ```

3. **My Tasks**
   ```
   Filter: Assignee = Me AND Status != Done
   Sort: Due Date ascending
   ```

4. **Overdue**
   ```
   Filter: Overdue = "⚠️"
   Sort: Due Date ascending
   ```

**Project Views:**

1. **Active Projects**
   ```
   Filter: Status = Active
   Sort: Priority descending
   ```

2. **Portfolio Dashboard**
   ```
   View: Gallery
   Show: Status, PM, Progress, Budget
   Filter: Status != Complete
   ```

3. **Timeline (Gantt)**
   ```
   View: Timeline
   Start date: Start Date
   End date: End Date
   Color: By Status
   ```

### Linked Databases

**Concept:** Show same database with different views

**Example:**
```
Main Page: Projects Master Database

Sprint 5 Page:
├─ Linked DB: Tasks (filtered to Sprint 5)
├─ Linked DB: Risks (filtered to Sprint 5)
└─ Linked DB: Meetings (filtered to Sprint 5)

Each linked DB can have unique:
- Filters
- Sorts
- Views (Table, Board, Calendar)
- Properties shown
```

### Automation (Limited)

**Using Formulas:**
```
# Auto-calculate days left
dateBetween(prop("Due Date"), now(), "days")

# Auto-set RAG status
if(prop("Overdue"), "🔴",
   if(prop("Days Left") < 3, "🟡", "🟢"))

# Calculate budget remaining
prop("Budget") - prop("Budget Used")
```

**Recurring Tasks:**
```
# Use template button
Create button: "New Weekly Retrospective"
→ Creates task with:
   - Title: "Retrospective - [Week of ...]"
   - Template: Retro format
   - Due: Next Friday
```

### Integrations

**Slack:**
- Share pages to Slack
- Update notifications
- Database updates from Slack (via Zapier)

**Google Calendar:**
- Embed calendar in Notion
- Two-way sync (via third-party)

**Zapier:**
- Create task from email
- Sync with Jira/Asana
- Auto-create from form submissions

---

## Tool Migration Strategies

### Data Export/Import

**From Jira:**
```
Export:
1. Jira → Issues → Export issues
2. Format: CSV
3. Include: All fields

Import to Asana:
1. Asana → Import → CSV
2. Map fields:
   - Summary → Name
   - Description → Description
   - Story Points → Custom field
   - Status → Section
3. Validate & import
```

**From Asana:**
```
Export:
1. Project → Export → CSV
2. All tasks exported

Import to Jira:
1. Jira → Import
2. CSV Importer
3. Map fields
4. Create issues
```

**From Trello:**
```
Export:
1. Board → Menu → More → Export JSON
2. Save file

Import to ClickUp:
1. ClickUp → Import
2. Trello option
3. Connect Trello account
4. Select boards
5. Map to Spaces
```

### Migration Checklist

**Pre-Migration:**
- [ ] Export data from old tool
- [ ] Audit data quality
- [ ] Map workflows (old → new)
- [ ] Map custom fields
- [ ] Identify integrations to migrate
- [ ] Train team on new tool
- [ ] Set up test instance
- [ ] Pilot with small team

**During Migration:**
- [ ] Import data
- [ ] Validate data integrity
- [ ] Configure workflows
- [ ] Set up automations
- [ ] Configure integrations
- [ ] Test with real scenarios
- [ ] Parallel run (optional)

**Post-Migration:**
- [ ] Full team training
- [ ] Monitor adoption
- [ ] Gather feedback
- [ ] Optimize workflows
- [ ] Archive old tool data
- [ ] Document new processes

### Hybrid Approach

**Scenario:** Large org, can't migrate everyone at once

**Strategy:**
```
Phase 1: Pilot Team (Month 1)
├─ Select 1-2 teams
├─ Migrate their projects
├─ Gather feedback
└─ Refine processes

Phase 2: Early Adopters (Month 2-3)
├─ Migrate willing teams
├─ Document best practices
└─ Create training materials

Phase 3: Full Rollout (Month 4-6)
├─ Migrate all remaining teams
├─ Decommission old tool
└─ Celebrate success
```

**Integration Bridge:**
- Use Zapier/Integromat for bi-directional sync
- Gradual cutover per team
- Maintain data consistency

---

## Best Practices Across Tools

### Universal PM Principles

1. **Keep workflows simple**
   - Minimize status columns (<7)
   - Clear status meanings
   - Easy transitions

2. **Use templates**
   - User story format
   - Bug report structure
   - Meeting notes

3. **Automate repetitive tasks**
   - Status updates
   - Notifications
   - Recurring tasks

4. **Regular cleanup**
   - Archive old projects
   - Delete unused labels
   - Review automations

5. **Team training**
   - Tool-specific sessions
   - Best practices docs
   - Office hours for questions

### Data Hygiene

**Task Hygiene:**
- Close done tasks promptly
- Update status regularly
- Keep descriptions current
- Remove outdated info

**Project Hygiene:**
- Archive completed projects
- Update roadmaps quarterly
- Review risk registers weekly
- Clean up duplicates

**Integration Hygiene:**
- Remove unused integrations
- Update API tokens
- Test automations monthly
- Monitor sync errors

---

**Remember:** The best PM tool is the one your team actually uses. Choose for adoption, not features.
