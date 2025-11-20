---
name: senior-project-manager
description: |
  Manages projects using PMP standards, Agile/Scrum, and Waterfall methodologies. Creates project charters, BRDs, risk registers, and sprint plans. Configures PM tools (Jira, Asana, Trello, ClickUp, Linear) and generates Excel reports (Gantt charts, burndown) and PowerPoint presentations. Use when planning projects, running sprints, writing requirements, managing risks, or creating PM deliverables.
---

# Senior Project Manager Skill

Comprehensive project management expertise combining PMP standards, Agile/Scrum specialization, and traditional Waterfall methodology for enterprise project delivery.

## Core Competencies

### 1. PMP Framework (PMBOK)
- 10 Knowledge Areas
- 5 Process Groups (Initiating, Planning, Executing, Monitoring, Closing)
- Project Charter development
- WBS and Gantt chart creation
- Critical path analysis

### 2. Agile & Scrum (Specialization)
- Scrum ceremonies (Planning, Daily, Review, Retrospective)
- Product backlog management
- Sprint execution and tracking
- T-shirt sizing and story points
- Velocity tracking and forecasting

### 3. Waterfall Methodology
- Sequential phase execution
- Comprehensive upfront planning
- Gate reviews and approvals
- Change control processes
- Traditional risk management

### 4. Hybrid Approach
- Combining predictive and adaptive methods
- Phased delivery with iterative development
- Scaled Agile Framework (SAFe) basics
- Transitioning between methodologies

## Quick Start Workflows

### Initiate New Project

**Step 1: Create Project Charter**
```bash
# Use PMP standard charter
Read {baseDir}/templates/project-charter-template.md

# Or Agile lightweight version
Read {baseDir}/templates/project-charter-agile.md
```

**Step 2: Identify Stakeholders**
```bash
# Review stakeholder analysis
Read {baseDir}/references/risk-stakeholder.md section "Stakeholder Identification"

# Document in charter
- Power/Interest matrix
- Communication requirements
- Engagement strategies
```

**Step 3: Define Success Criteria**
- SMART objectives
- Acceptance criteria
- Key performance indicators
- Definition of Done (Agile)

### Plan Sprint (Agile)

**Step 1: Backlog Refinement**
```bash
# Review backlog preparation
Read {baseDir}/references/agile-scrum.md section "Backlog Refinement"

# Prepare stories with:
- Clear acceptance criteria
- T-shirt size estimates
- Dependencies identified
```

**Step 2: Sprint Planning Meeting**
```bash
# Use sprint planning template
Read {baseDir}/templates/sprint-planning-template.md

# Agenda:
1. Review sprint goal
2. Select backlog items
3. Estimate story points
4. Define sprint backlog
5. Commit to deliverables
```

**Step 3: Track Progress**
```bash
# Generate burndown chart
python {baseDir}/scripts/burndown_generator.py --sprint 5

# Monitor daily:
- Burndown trend
- Velocity
- Blockers
```

### Conduct Retrospective

**Step 1: Prepare Retrospective**
```bash
# Review retrospective guide
Read {baseDir}/references/agile-scrum.md section "Sprint Retrospective"

# Choose format:
- Mad/Sad/Glad
- Start/Stop/Continue
- 4Ls (Liked/Learned/Lacked/Longed for)
```

**Step 2: Facilitate Meeting**
```bash
# Use retrospective template
Read {baseDir}/templates/retrospective-template.md

# Timebox (90 min):
1. Set stage (5 min)
2. Gather data (15 min)
3. Generate insights (30 min)
4. Decide actions (30 min)
5. Close (10 min)
```

**Step 3: Track Action Items**
- Assign owners
- Set deadlines
- Review in next retro
- Measure improvements

### Manage Risks

**Step 1: Identify Risks**
```bash
# Review risk identification techniques
Read {baseDir}/references/risk-stakeholder.md section "Risk Identification"

# Methods:
- Brainstorming
- SWOT analysis
- Checklist review
- Expert interviews
```

**Step 2: Assess and Prioritize**
```bash
# Calculate risk scores
python {baseDir}/scripts/risk_calculator.py --project myproject

# Use risk register
Read {baseDir}/templates/risk-register-template.md

# Score: Probability × Impact
```

**Step 3: Develop Response Plans**
- Avoid, Transfer, Mitigate, Accept
- Assign risk owners
- Define triggers
- Allocate contingency reserve

### Create Business Requirements Document (BRD)

**Step 1: Elicit Requirements**
```bash
# Use stakeholder interview guide
Read {baseDir}/templates/stakeholder-interview-guide.md

# Techniques:
- One-on-one interviews
- Focus groups
- Workshops
- Observation
- Document analysis
```

**Step 2: Document Requirements**
```bash
# Use BRD template
Read {baseDir}/templates/brd-template.md

# Structure:
1. Executive Summary
2. Business Objectives
3. Scope (In/Out)
4. Functional Requirements
5. Non-Functional Requirements
6. Assumptions & Constraints
7. Success Criteria
```

**Step 3: Validate & Trace**
```bash
# Create traceability matrix
Read {baseDir}/templates/requirements-traceability-matrix.md

# Track:
- Requirement ID → Design → Test Case
- Business need → Technical spec
- Stakeholder → Requirement ownership
```

**Step 4: Get Sign-off**
- Review with stakeholders
- Address feedback
- Formal approval process
- Baseline document

## Key Workflows

### 1. Methodology Selection

**Decision Tree:**
```
Project characteristics?
├─ Requirements clear & stable?
│  ├─ Yes → Regulatory/fixed scope?
│  │  ├─ Yes → WATERFALL
│  │  └─ No → Consider HYBRID
│  └─ No → Frequent changes expected?
│     ├─ Yes → AGILE (Scrum/Kanban)
│     └─ No → HYBRID (iterative phases)
│
├─ Team location?
│  ├─ Co-located → AGILE works well
│  └─ Distributed → AGILE with strong tools
│
└─ Stakeholder involvement?
   ├─ High availability → AGILE
   └─ Limited availability → WATERFALL
```

**For Agile, choose framework:**
```
Team size & complexity?
├─ Single team (5-9 people) → SCRUM
├─ Multiple teams → SAFe or LeSS
├─ Flow-based work → KANBAN
└─ Fixed timeline → SCRUMBAN
```

### 2. Estimation Workshop

**Scenario:** Team needs to estimate new features

**Process:**
1. Review estimation techniques
   - Read {baseDir}/references/agile-scrum.md section "Estimation Techniques"
   - Read {baseDir}/templates/estimation-workshop.md

2. **T-Shirt Sizing** (Initial rough estimate)
   ```
   Risk vs Complexity Matrix:
   
   RISK:
   Very High: L    XL   2XL  3XL
   High:      M    L    XL   2XL
   Medium:    S    M    L    XL
   Low:       XS   S    M    L
              Low  Med  High VHigh
                 COMPLEXITY
   ```

3. **Planning Poker** (Detailed estimate)
   - Use Fibonacci sequence (1, 2, 3, 5, 8, 13, 21)
   - Everyone reveals simultaneously
   - Discuss outliers
   - Re-vote until consensus

4. **Convert to Hours** (if needed)
   ```
   T-Shirt → Story Points → Hours
   XS  = 1 pt  = 2-4 hours
   S   = 2 pts = 4-8 hours
   M   = 3 pts = 1-2 days
   L   = 5 pts = 2-3 days
   XL  = 8 pts = 3-5 days
   2XL = 13 pts = 1-2 weeks
   ```

**Validation:**
- Check against team velocity
- Review with technical leads
- Adjust for unknowns

### 3. Waterfall Project Planning

**Scenario:** Large infrastructure project with fixed requirements

**Process:**
1. Define scope completely
   - Read {baseDir}/references/waterfall-predictive.md section "Scope Definition"
   - Create detailed requirements document
   - Get stakeholder sign-off

2. Create Work Breakdown Structure (WBS)
   - Read {baseDir}/templates/wbs-template.md
   - Decompose to work packages
   - Assign responsibility

3. Develop schedule
   - Identify dependencies
   - Calculate critical path
   - Create Gantt chart
   - Add buffers

4. Estimate costs
   - Bottom-up estimation
   - Add contingency (10-20%)
   - Get budget approval

5. Execute with change control
   - Strict change management
   - Gate reviews
   - Variance analysis

### 4. Hybrid Approach

**Scenario:** Complex project with stable architecture but evolving features

**Process:**
1. Use Waterfall for infrastructure phases
   - Architecture design (predictive)
   - Infrastructure setup (sequential)
   - Security implementation (controlled)

2. Use Agile for feature development
   - Sprint-based delivery
   - Continuous feedback
   - Iterative improvements

3. Integration points
   - Architecture reviews every 2 sprints
   - Infrastructure as enabler for features
   - Coordinated releases

**Example: E-commerce Platform**
```
Phase 1: Infrastructure (Waterfall - 3 months)
├─ Network setup
├─ Server provisioning
├─ Database design
└─ Security framework

Phase 2: Feature Development (Agile - 6 months)
├─ Sprint 1-2: User registration & authentication
├─ Sprint 3-4: Product catalog
├─ Sprint 5-6: Shopping cart
├─ Sprint 7-8: Payment gateway
├─ Sprint 9-10: Order management
└─ Sprint 11-12: Analytics & reporting
```

### 5. Status Reporting

**Weekly Status Report:**
```bash
# Use universal template
Read {baseDir}/templates/status-report-template.md

# Include:
1. Executive summary (RAG status)
2. Accomplishments this week
3. Planned for next week
4. Issues and risks
5. Budget status
6. Schedule status
7. Key metrics
```

**For Agile Projects:**
- Sprint burndown chart
- Velocity trend
- Release burndown
- Impediment log

**For Waterfall Projects:**
- Milestone status
- Earned value (EV, PV, AC)
- Schedule variance (SV)
- Cost variance (CV)

### 6. Generate Excel & PowerPoint Deliverables

**Excel Reports:**

**Risk Register:**
```bash
# CRITICAL: Read xlsx skill first
Read /mnt/skills/public/xlsx/SKILL.md

# Then read PM-specific structure
Read {baseDir}/templates/excel-risk-register-structure.md

# Create Excel file with:
- Risk ID, Description, Category
- Probability, Impact, Risk Score
- Mitigation Plan, Owner, Status
- Conditional formatting (red/yellow/green)
```

**Gantt Chart:**
```bash
# Read xlsx skill first
Read /mnt/skills/public/xlsx/SKILL.md

# Then read Gantt structure
Read {baseDir}/templates/excel-gantt-structure.md

# Create Excel with:
- Task list with start/end dates
- Timeline visualization
- Dependencies arrows
- Critical path highlighting
- Progress tracking (%)
```

**PowerPoint Reports:**

**Status Report Presentation:**
```bash
# CRITICAL: Read pptx skill first
Read /mnt/skills/public/pptx/SKILL.md

# Then read status report structure
Read {baseDir}/templates/ppt-status-report-structure.md

# Create PPT with:
Slide 1: Title + RAG status
Slide 2: Executive summary
Slide 3: Accomplishments (bullet points)
Slide 4: Issues & Risks (table)
Slide 5: Budget/Schedule status (charts)
Slide 6: Next steps
```

**Sprint Review Presentation:**
```bash
# Read pptx skill first
Read /mnt/skills/public/pptx/SKILL.md

# Then read sprint review structure
Read {baseDir}/templates/ppt-sprint-review-structure.md

# Create PPT with:
Slide 1: Sprint goal & dates
Slide 2: Velocity chart
Slide 3: Completed stories (with screenshots)
Slide 4: Burndown chart
Slide 5: Demo highlights
Slide 6: Retrospective actions
```

**Key Principle:**
Always leverage built-in xlsx/pptx skills instead of writing custom Python. PM templates provide structure, built-in skills handle generation.

### 7. Project Health Check

**Scenario:** Mid-project health assessment

**Process:**
```bash
# Run project analyzer
python {baseDir}/scripts/project_analyzer.py --project myproject

# Analyzes:
- Schedule performance (CPI, SPI)
- Budget variance
- Risk exposure
- Team velocity (Agile)
- Stakeholder satisfaction
- Quality metrics
```

**Health Indicators:**
```
🟢 GREEN (Healthy):
- On schedule (±5%)
- On budget (±5%)
- All milestones met
- No critical risks
- Team morale high

🟡 YELLOW (At Risk):
- Schedule slip 5-10%
- Budget variance 5-10%
- Some milestones delayed
- Moderate risks
- Team concerns

🔴 RED (Critical):
- Schedule slip >10%
- Budget overrun >10%
- Major milestones missed
- Critical risks unmitigated
- Team issues
```

**Remediation Actions:**
- Green: Continue monitoring
- Yellow: Develop recovery plan
- Red: Executive escalation + corrective action

## PM Tools Mastery

### Quick Tool Selection

**Decision Matrix:**
```
Team Size & Needs:
├─ Small team (5-10), simple workflows → TRELLO
├─ Agile/Scrum focused → JIRA or LINEAR
├─ Marketing/creative projects → ASANA or MONDAY
├─ Enterprise/complex → JIRA (Advanced)
├─ Budget-conscious → CLICKUP (all-in-one)
└─ Documentation-heavy → NOTION + integrations
```

### Jira Workflows

**Sprint Setup:**
```bash
# Import sprint template
Read {baseDir}/templates/jira-sprint-template.json

# Configure board:
1. Create Scrum/Kanban board
2. Set sprint duration (2 weeks)
3. Configure columns (To Do, In Progress, Review, Done)
4. Add swimlanes (by assignee/priority)
5. Enable estimation (story points)
```

**Automation Rules:**
- Auto-assign to reporter when status = "In Review"
- Auto-close when all subtasks done
- Notify Slack when critical bug created
- Auto-transition when PR merged

**JQL Queries:**
```jql
# Sprint burndown issues
project = PROJ AND sprint = 5 AND status != Done

# Overdue critical bugs
project = PROJ AND type = Bug AND priority = Critical AND due < now()

# My incomplete work
assignee = currentUser() AND resolution = Unresolved ORDER BY priority DESC

# Velocity report data
project = PROJ AND sprint in closedSprints() AND sprint >= -5
```

**For complete Jira guide:**
- Read {baseDir}/references/pm-tools-guide.md section "Jira Advanced"

### Asana Workflows

**Project Template Setup:**
```bash
# Import project structure
Read {baseDir}/templates/asana-project-template.csv

# Best practices:
1. Use Sections for phases/sprints
2. Custom fields for priority/effort
3. Dependencies for task relationships
4. Timeline view for Gantt-style planning
5. Dashboard for portfolio reporting
```

**Task Automation:**
- Add task to sprint when tagged "Sprint 5"
- Move to "In Review" when subtasks complete
- Assign to PM when moved to "Blocked"
- Create follow-up task on completion

**Portfolio Management:**
```
Portfolio Dashboard:
├─ Project Status (RAG)
├─ Milestones Timeline
├─ Resource Allocation
├─ Budget Tracking
└─ Risk Heat Map
```

**For complete Asana guide:**
- Read {baseDir}/references/pm-tools-guide.md section "Asana Pro"

### Trello Power-Ups

**Essential Power-Ups:**
1. **Calendar** - Deadline visualization
2. **Butler** - Automation (free tier: 250 actions/month)
3. **Custom Fields** - Add metadata (effort, priority)
4. **Card Repeater** - Recurring tasks
5. **Voting** - Team prioritization

**Butler Automation Examples:**
```
# Daily standup reminder
Every weekday at 9:00 AM, post comment "Daily standup in 30 min"

# Auto-archive done cards
Every day, archive all cards in list "Done" older than 1 week

# Sprint closure
When a card is moved to "Done", add label "Sprint 5 Complete"
```

**For complete Trello guide:**
- Read {baseDir}/references/pm-tools-guide.md section "Trello Advanced"

### Monday.com Workflows

**Board Templates:**
- Sprint Planning Board
- Bug Tracking Board
- Project Roadmap Board
- Resource Management Board

**Automation Recipes:**
```
# Status-based notifications
When status changes to "Stuck", notify PM

# Timeline tracking
When deadline approaches in 2 days, notify assignee

# Dependency management
When dependency task completes, notify dependent task owner
```

**Integration Power:**
- Slack: Real-time updates
- Jira: Bi-directional sync
- GitHub: PR status tracking
- Zoom: Meeting scheduling

**For complete Monday guide:**
- Read {baseDir}/references/pm-tools-guide.md section "Monday.com"

### ClickUp (All-in-One)

**Why ClickUp:**
- Free tier supports unlimited tasks
- Native time tracking
- Built-in docs (replaces Confluence)
- Multiple views (List, Board, Gantt, Calendar)
- Advanced automations

**Setup Hierarchy:**
```
Workspace
└─ Space (Department/Team)
   └─ Folder (Project)
      └─ List (Sprint/Phase)
         └─ Task
            └─ Subtask
```

**Custom Fields for PM:**
- Effort (dropdown: S/M/L/XL)
- Priority (1-4)
- Sprint (number)
- Risk Level (Low/Med/High)
- Budget Impact ($)

**For complete ClickUp guide:**
- Read {baseDir}/references/pm-tools-guide.md section "ClickUp Mastery"

### Linear (Developer-Focused)

**Why Linear:**
- Blazing fast UI
- Git integration (auto-updates from commits)
- Keyboard-first navigation
- Cycle-based planning (similar to sprints)
- Triage workflow for issues

**Cycle Planning:**
```bash
# Create cycle
1. Set duration (1-2 weeks)
2. Set team capacity
3. Assign issues from backlog
4. Track progress (auto burndown)
5. Review cycle stats
```

**Git Integration:**
```
git commit -m "Implement login API [LIN-123]"
# Auto-updates Linear issue LIN-123 → "In Progress"

git commit -m "Fix auth bug, closes LIN-124"
# Auto-closes Linear issue LIN-124
```

**For complete Linear guide:**
- Read {baseDir}/references/pm-tools-guide.md section "Linear Advanced"

### Notion (Documentation + PM)

**PM Database Templates:**
1. **Projects Database** (portfolio view)
2. **Sprint Tasks** (linked to Projects)
3. **Meeting Notes** (tagged by project)
4. **Retrospectives** (timeline view)
5. **Risk Register** (filtered by project)

**Relational Database Setup:**
```
Projects (Master)
├─ Properties: Status, PM, Budget, Deadline
├─ Relations: → Tasks, → Risks, → Meetings
└─ Rollups: Total tasks, Open risks, Budget used

Tasks (Detail)
├─ Properties: Assignee, Status, Effort, Sprint
├─ Relations: ← Projects
└─ Formula: Overdue = if(Deadline < now(), "⚠️", "✅")
```

**For complete Notion guide:**
- Read {baseDir}/references/pm-tools-guide.md section "Notion PM Setup"

### Cross-Tool Migration

**Scenario:** Migrate from Jira → Asana

**Process:**
```bash
# Export from Jira
python {baseDir}/scripts/jira_sync.py export --project PROJ --output jira_export.json

# Transform format
python {baseDir}/scripts/tool_migrator.py --from jira --to asana --input jira_export.json --output asana_import.csv

# Import to Asana
# Use Asana CSV importer in web UI
```

**Data Mapping:**
```
Jira              → Asana
─────────────────────────────
Epic              → Project
Story             → Task
Subtask           → Subtask
Sprint            → Section
Story Points      → Custom Field
Priority          → Priority
Assignee          → Assignee
Labels            → Tags
Comments          → Comments
Attachments       → Files
```

**For tool migration guide:**
- Read {baseDir}/references/pm-tools-guide.md section "Migration Strategies"

### Tool-Specific Scripts

**Jira Sync:**
```bash
# Export sprint data
python {baseDir}/scripts/jira_sync.py export --sprint 5

# Import backlog
python {baseDir}/scripts/jira_sync.py import --file backlog.json

# Generate burndown
python {baseDir}/scripts/jira_sync.py burndown --sprint 5 --output chart.png
```

**Asana Automation:**
```bash
# Bulk task creation
python {baseDir}/scripts/asana_tracker.py create --file tasks.csv --project 123456

# Weekly status report
python {baseDir}/scripts/asana_tracker.py report --project 123456 --format markdown

# Resource allocation
python {baseDir}/scripts/asana_tracker.py capacity --team engineering
```

### Best Practices by Tool

**Jira:**
- Keep issue types simple (Epic/Story/Bug/Task)
- Use components for team ownership
- Automate transitions with workflow rules
- Regular backlog grooming
- Archive old sprints quarterly

**Asana:**
- Use My Tasks for personal kanban
- Template projects for repeatability
- Portfolio for executive visibility
- Forms for standardized intake
- Dependencies to block concurrent work

**Trello:**
- One board per project/team
- WIP limits on "In Progress" column
- Checklists for subtasks
- Labels for categorization
- Power-Ups sparingly (max 3-5)

**Monday:**
- Color-code statuses clearly
- Use timeline for Gantt view
- Dashboard for stakeholders
- Automations for notifications
- Workload view for capacity

**ClickUp:**
- Leverage multiple views per need
- Use time tracking for metrics
- Docs for requirements
- Goals for OKRs
- Mind maps for planning

**Linear:**
- Keyboard shortcuts (essential)
- Git branch auto-creation
- Cycles for predictable delivery
- Triage for incoming issues
- Views for different contexts

**Notion:**
- Templates for consistency
- Relations between databases
- Rollups for aggregation
- Synced blocks for updates
- Toggle lists for cleanliness

## Tool Integration

### Collaboration Tools
- **Confluence**: Documentation, knowledge base
- **SharePoint**: Document management
- **Teams/Zoom**: Meetings, ceremonies
- **Slack**: Real-time communication
- **Miro**: Virtual retrospectives, estimation

### Traditional PM Tools
- **MS Project**: Gantt charts, resource management
- **Primavera**: Large-scale scheduling
- **Excel**: Budget tracking, risk registers

**For comprehensive tool guidance:**
- Read {baseDir}/references/pm-tools-guide.md

## Decision Trees

### Sprint Goal Not Met
```
Sprint incomplete?
├─ Velocity too optimistic?
│  ├─ Yes → Adjust capacity for next sprint
│  │        Reduce story points by 20%
│  └─ No → Continue to next check
│
├─ External blockers?
│  ├─ Yes → Escalate impediments
│  │        Involve Scrum Master
│  └─ No → Continue to next check
│
├─ Stories too large?
│  ├─ Yes → Improve story splitting
│  │        No story >5 points
│  └─ No → Continue to next check
│
└─ Technical debt?
   ├─ Yes → Allocate 20% capacity to tech debt
   │        Discuss in retrospective
   └─ No → Review team composition
```

### Budget Overrun
```
Over budget?
├─ Scope creep?
│  ├─ Yes → Implement change control
│  │        Review all new requests
│  └─ No → Continue analysis
│
├─ Inefficient resources?
│  ├─ Yes → Optimize team structure
│  │        Training or replacement
│  └─ No → Continue analysis
│
├─ Incorrect estimates?
│  ├─ Yes → Re-estimate remaining work
│  │        Update budget forecast
│  └─ No → Continue analysis
│
└─ External factors?
   ├─ Yes → Document for lessons learned
   │        Request contingency funds
   └─ No → Deep-dive root cause analysis
```

## Best Practices

### PMP Standards
1. Always create formal project charter
2. Document assumptions and constraints
3. Identify stakeholders early
4. Maintain risk register
5. Track lessons learned
6. Close projects formally

### Agile/Scrum
1. Keep sprints time-boxed (2 weeks ideal)
2. Daily standups max 15 minutes
3. Product Owner must be available
4. Definition of Done is clear
5. Retrospectives drive improvement
6. Sustainable pace (no overtime)

### Waterfall
1. Complete requirements before design
2. Formal phase gate approvals
3. Comprehensive change control
4. Regular variance analysis
5. Document everything
6. Quality reviews at each phase

### Universal PM
1. Communicate proactively
2. Manage stakeholder expectations
3. Address risks early
4. Celebrate wins
5. Learn from failures
6. Maintain work-life balance

## Common Challenges & Solutions

### Challenge: Low Velocity
**Symptoms:**
- Sprint goals not met consistently
- Burndown not tracking well
- Team frustrated

**Solutions:**
1. Review story point calibration
2. Identify and remove impediments
3. Reduce WIP (work in progress)
4. Check for technical debt
5. Improve story splitting
6. Team capacity issues?

**Action:** Run retrospective focused on velocity

### Challenge: Scope Creep
**Symptoms:**
- Constant new requirements
- Timeline extending
- Budget pressure

**Solutions:**
1. Strengthen change control process
2. Product Owner prioritization
3. Say "No" or "Later"
4. Document all changes
5. Re-baseline if needed

**For Agile:** Add to backlog, prioritize
**For Waterfall:** Formal change request

### Challenge: Stakeholder Conflict
**Symptoms:**
- Contradictory requirements
- Competing priorities
- Meeting gridlock

**Solutions:**
1. Power/Interest mapping
2. Individual stakeholder meetings
3. Facilitate consensus workshop
4. Executive sponsor involvement
5. Document decisions clearly

**Read:** {baseDir}/references/risk-stakeholder.md section "Conflict Resolution"

## Success Metrics

### Agile KPIs
- **Velocity**: Story points per sprint (track trend)
- **Sprint Commitment**: % of stories completed
- **Escaped Defects**: Bugs found post-sprint
- **Team Happiness**: Measured in retros
- **Cycle Time**: Time from start to done

### Waterfall KPIs
- **Schedule Variance (SV)**: EV - PV
- **Cost Variance (CV)**: EV - AC
- **SPI (Schedule Performance Index)**: EV / PV
- **CPI (Cost Performance Index)**: EV / AC
- **Milestone Hit Rate**: % on-time milestones

### Universal KPIs
- **Customer Satisfaction**: NPS or CSAT score
- **ROI**: Return on investment
- **Team Utilization**: % productive time
- **Risk Mitigation**: % risks addressed
- **Quality**: Defect density

**Target Benchmarks:**
- Velocity: Steady or increasing
- SPI/CPI: > 0.95 (healthy)
- Sprint commitment: > 80%
- Customer satisfaction: > 8/10
- Team happiness: > 7/10

## Progressive Enhancement

This skill uses progressive disclosure:
- **SKILL.md** (this file): Quick workflows and decision trees
- **references/**: Deep-dive methodology guides
- **templates/**: Ready-to-use project documents
- **scripts/**: Automation for analysis and tracking

Load additional resources based on your needs:
- PMP framework → pmp-framework.md
- Agile/Scrum mastery → agile-scrum.md
- Waterfall planning → waterfall-predictive.md
- Hybrid approaches → hybrid-approach.md
- Risk & stakeholders → risk-stakeholder.md
- Metrics & reporting → metrics-reporting.md
- PM tools mastery → pm-tools-guide.md

## Getting Started Checklist

Before starting any project:
- [ ] Project charter created and approved
- [ ] Stakeholders identified and mapped
- [ ] Methodology selected (Agile/Waterfall/Hybrid)
- [ ] Team roles assigned
- [ ] Communication plan established
- [ ] Risk register initialized
- [ ] Success criteria defined
- [ ] Budget allocated
- [ ] Tools configured
- [ ] Kickoff meeting scheduled

For Agile projects, add:
- [ ] Product backlog created
- [ ] Sprint duration decided
- [ ] Definition of Done agreed
- [ ] Ceremony schedule set
- [ ] Burndown charts configured

For Waterfall projects, add:
- [ ] WBS completed
- [ ] Gantt chart created
- [ ] Critical path identified
- [ ] Gate review schedule set
- [ ] Change control process defined

---

**Remember:** Great PMs adapt their methodology to the project, not the project to their methodology. Know all approaches and choose wisely.
