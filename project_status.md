# Senior Project Manager Skill - Project Status

**Last Updated:** 2025-11-13  
**Status:** ✅ 100% COMPLETE (26/26 files done)  
**Next Phase:** Ready for packaging

---

## ✅ COMPLETED (26/26 files) - ALL DONE

### 1. SKILL.md ✅
- **Status:** Fully updated
- **Size:** ~1,100 lines
- **Changes made:**
  - Updated description to include BRD, requirements elicitation, PM tools, Excel/PPT generation
  - Added "Create Business Requirements Document (BRD)" workflow section
  - Added "Generate Excel & PowerPoint Deliverables" workflow section
  - Added PM Tools Mastery section (Jira, Asana, Trello, Monday, ClickUp, Linear, Notion)
  - Updated Progressive Enhancement section to include pm-tools-guide.md
- **Quality:** Comprehensive, follows best practices

### 2. references/metrics-reporting.md ✅
- **Status:** Newly created
- **Size:** ~900 lines
- **Content:**
  - Agile Metrics (Velocity, Burndown, Cycle Time, Escaped Defects, Lead Time)
  - Waterfall Metrics (SPI, CPI, SV, CV, Milestone Hit Rate)
  - Universal KPIs (CSAT, NPS, ROI, Team Utilization, Quality)
  - Reporting Formats (Executive Dashboard, Weekly Status, Sprint Review)
  - PM Tools Integration (Jira reports, Asana reports, Excel analytics)
  - Best Practices & Common Pitfalls
- **Quality:** Production-ready, detailed formulas and examples

### 3. references/pm-tools-guide.md ✅
- **Status:** Newly created
- **Size:** ~1,400 lines
- **Content:**
  - Tool Selection Matrix (when to use which tool)
  - Cost Comparison table
  - Jira Advanced (setup, workflows, JQL, automation, integrations, API)
  - Asana Pro (structure, templates, custom fields, dependencies, automation, forms)
  - Trello Advanced (board structure, Power-Ups, Butler automation, labels, integrations)
  - Monday.com (board types, automations, dashboards, integrations)
  - ClickUp Mastery (hierarchy, multiple views, time tracking, docs, automations)
  - Linear Advanced (cycle planning, keyboard shortcuts, Git integration, triage)
  - Notion PM Setup (database structure, templates, views, linked databases)
  - Tool Migration Strategies (export/import, checklists, hybrid approach)
  - Best Practices across all tools
- **Quality:** Comprehensive, real-world examples, production-ready

### 4. references/pmp-framework.md ✅
- **Status:** Updated (added Requirements Management section)
- **Size:** Original ~600 lines + 519 new lines = ~1,119 lines
- **New Content:**
  - Requirements Management section (~519 lines)
  - Requirements Categories (Business, Stakeholder, Solution, Transition)
  - Requirements Elicitation Techniques (7 techniques with details)
  - Requirements Analysis (categorization, prioritization, conflict resolution, feasibility)
  - Full BRD structure template (13 sections)
  - Requirements Traceability Matrix (RTM) guide
  - Requirements Validation techniques
  - Requirements Change Management process
  - Common Pitfalls & Best Practices
- **Quality:** Enterprise-grade, follows PMBOK/BABOK standards

### 5. scripts/burndown_generator.py ✅
- **Status:** Newly created
- **Size:** ~380 lines
- **Features:**
  - Load data from CSV, JSON, or manual entry
  - Calculate ideal burndown (linear)
  - Calculate sprint metrics (velocity, forecast, variance)
  - Generate matplotlib chart (if installed)
  - Print comprehensive text report
  - Daily breakdown with comparison to ideal
  - Support for 1-20 day sprints
- **Quality:** Production-ready, proper error handling, documented

### 6. scripts/risk_calculator.py ✅
- **Status:** Newly created
- **Size:** ~500 lines
- **Features:**
  - Risk class with probability/impact normalization
  - Supports text input ("High", "Medium") or numeric
  - Calculate risk scores (Probability × Impact)
  - Risk level categorization (Critical/High/Medium/Low)
  - Load from CSV, JSON, or manual entry
  - Sort by score, probability, or impact
  - Filter by level or status
  - Calculate total risk exposure
  - Comprehensive statistics
  - Export to CSV or JSON
- **Quality:** Production-ready, enterprise-grade risk management

---

## ✅ ALL FILES COMPLETED

### Phase 1: Core Scripts (3/3) ✅

### Phase 1: Core Scripts (2 files)

#### 7. scripts/project_analyzer.py ✅
**Status:** COMPLETE
**Purpose:** Comprehensive project health analysis  
**Required Features:**
- Parse project data from JSON/CSV
- Calculate Earned Value metrics (EV, PV, AC, SPI, CPI, SV, CV, EAC, ETC, VAC)
- Analyze schedule performance
- Analyze budget variance
- Calculate team velocity (if Agile)
- Assess risk exposure (integrate with risk_calculator.py)
- Generate RAG status (Red/Amber/Green)
- Health indicators with thresholds
- Forecast completion date
- Recommend corrective actions
- Export report (text, JSON, CSV)

**Input Format Examples:**
```json
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
```

**Output Report Should Include:**
- Executive Summary (1-2 sentences)
- Overall RAG Status with emoji
- Earned Value Analysis (all metrics)
- Schedule Analysis (on time? forecast?)
- Budget Analysis (on budget? forecast?)
- Velocity Analysis (if Agile)
- Risk Exposure Score
- Top 3 Concerns
- Recommended Actions
- Detailed metrics table

**Quality Requirements:**
- Proper error handling
- Support both Agile and Waterfall projects
- Clear documentation
- ~400-500 lines
- Follow same structure as other scripts

---

### Phase 2: PM Tool Integration Scripts (2 files)

#### 8. scripts/jira_sync.py ✅
**Status:** COMPLETE
**Purpose:** Jira data export/import and automation  
**Required Features:**

**Commands:**
1. **Export:**
   - `python jira_sync.py export --project PROJ --sprint 5 --output sprint5.json`
   - Export issues from specific sprint
   - Export backlog items
   - Export epics with linked stories
   - Include: key, summary, status, assignee, story points, labels, sprint
   - JSON format for easy processing

2. **Import:**
   - `python jira_sync.py import --file backlog.json --project PROJ`
   - Bulk create issues from JSON/CSV
   - Update existing issues (by key)
   - Set custom fields (story points, sprint)

3. **Burndown:**
   - `python jira_sync.py burndown --sprint 5 --output chart.png`
   - Fetch sprint data via API
   - Generate burndown chart
   - Integrate with burndown_generator.py

4. **Velocity:**
   - `python jira_sync.py velocity --project PROJ --sprints 5`
   - Calculate velocity for last N sprints
   - Generate velocity chart
   - Print statistics

**Configuration:**
- Use environment variables or config file for credentials
- Support both Jira Cloud and Server
- JIRA_URL, JIRA_USER, JIRA_TOKEN

**Dependencies:**
- `jira` library (from PyPI)
- Handle case where library not installed gracefully

**Quality Requirements:**
- Proper authentication handling
- Rate limiting awareness
- Error handling (network issues, auth failures, invalid project)
- ~400-500 lines

#### 9. scripts/asana_tracker.py ✅
**Status:** COMPLETE
**Purpose:** Asana task automation and reporting  
**Required Features:**

**Commands:**
1. **Create Tasks:**
   - `python asana_tracker.py create --file tasks.csv --project 1234567890`
   - Bulk task creation from CSV
   - Set custom fields (Priority, Effort, Sprint)
   - Assign tasks
   - Set due dates

2. **Report:**
   - `python asana_tracker.py report --project 1234567890 --format markdown`
   - Weekly status report
   - Tasks completed this week
   - Tasks due next week
   - Overdue tasks
   - Export to markdown or JSON

3. **Capacity:**
   - `python asana_tracker.py capacity --team engineering`
   - Show team workload
   - Calculate capacity (hours available vs allocated)
   - Identify over-allocated members
   - Suggest rebalancing

4. **Sync:**
   - `python asana_tracker.py sync --source jira --project PROJ`
   - Sync tasks from Jira to Asana
   - Map fields appropriately
   - Avoid duplicates

**Configuration:**
- ASANA_TOKEN environment variable
- Config file for workspace/project mappings

**Dependencies:**
- `asana` library (from PyPI)
- Handle gracefully if not installed

**Quality Requirements:**
- API rate limiting handling
- Proper error messages
- CSV format documentation
- ~400-500 lines

---

### Phase 2: Document Templates (12/12) ✅

All templates should be **markdown format**, comprehensive, and follow PM best practices.

#### 10. templates/project-charter-template.md ✅
**Status:** COMPLETE
**Structure:**
- Header (Project name, PM, Sponsor, Date)
- Executive Summary (2-3 paragraphs)
- Business Case & Justification
- Project Objectives (SMART goals)
- High-Level Scope (In/Out)
- Stakeholders table
- Milestones & Timeline
- Budget Summary
- Key Assumptions
- High-Level Risks
- Success Criteria
- Approval Signatures section

**Length:** ~200-300 lines  
**Quality:** Enterprise-grade, PMP-aligned

#### 11. templates/sprint-planning-template.md ✅
**Status:** COMPLETE
**Structure:**
- Sprint Info (number, dates, goal)
- Team Capacity calculation
- Sprint Backlog (table format)
- Backlog Item structure (User Story format)
- Estimation guidelines (Planning Poker)
- Definition of Done checklist
- Dependencies section
- Sprint Risks
- Capacity vs Commitment comparison
- Action Items from planning

**Length:** ~150-200 lines  
**Quality:** Scrum-certified structure

#### 12. templates/retrospective-template.md ✅
**Status:** COMPLETE
**Structure:**
- Sprint Info
- Attendees
- Retrospective Format (multiple options: Mad/Sad/Glad, Start/Stop/Continue, 4Ls)
- What Went Well section
- What Didn't Go Well section
- Action Items (with owners and due dates)
- Follow-up from Previous Retro
- Team Happiness Score
- Key Takeaways

**Length:** ~150-200 lines  
**Quality:** Facilitator-friendly, actionable

#### 13. templates/risk-register-template.md ✅
**Status:** COMPLETE
**Structure:**
- Project Info header
- Risk Register table (ID, Description, Category, Probability, Impact, Score, Mitigation, Owner, Status)
- Risk Categories taxonomy
- Probability definitions (Very Low to Very High)
- Impact definitions (1-10 scale)
- Response Strategies (Avoid, Transfer, Mitigate, Accept)
- Risk Review Schedule
- Escalation criteria

**Length:** ~200-250 lines  
**Quality:** Enterprise risk management standard

#### 14. templates/status-report-template.md ✅
**Status:** COMPLETE
**Structure:**
- Report Header (week ending, project name, PM)
- Executive Summary (RAG status)
- Key Accomplishments This Week (bullets)
- Planned for Next Week (bullets)
- Issues & Risks table
- Budget Status (spent vs planned)
- Schedule Status (milestones)
- Key Metrics section
- Decisions Needed
- Next Steps

**Length:** ~150-200 lines  
**Quality:** Executive-friendly, scannable

#### 15. templates/brd-template.md ✅
**Status:** COMPLETE
**Structure:** (13 sections as documented in pmp-framework.md)
- Executive Summary
- Business Objectives
- Scope (In/Out/Future)
- Stakeholders table
- Current State (As-Is)
- Proposed Solution (To-Be)
- Functional Requirements (numbered FR-001, FR-002...)
- Non-Functional Requirements (NFR-001...)
- Assumptions & Constraints
- Dependencies
- Risks table
- Acceptance Criteria checklist
- Approval Signatures

**Length:** ~300-400 lines (comprehensive template)  
**Quality:** Enterprise BA standard, BABOK-aligned

#### 16. templates/requirements-traceability-matrix.md ✅
**Status:** COMPLETE
**Structure:**
- RTM Header (project, version, date)
- RTM Table (Req ID, Description, Source, Priority, Category, Design Spec, Test Case, Implementation Status, Verification Date, Owner)
- How to Use section
- Update Process
- Change Log table
- Coverage Metrics (% requirements traced)
- Orphan Requirements report

**Length:** ~100-150 lines  
**Quality:** Audit-ready, traceable

#### 17. templates/stakeholder-interview-guide.md ✅
**Status:** COMPLETE
**Structure:**
- Interview Preparation checklist
- Interview Structure (Introduction, Core Questions, Wrap-up)
- Question Bank organized by category:
  - Current State questions
  - Pain Points questions
  - Desired State questions
  - Process questions
  - Technical questions
  - Priority questions
- Active Listening tips
- Note-taking guidelines
- Follow-up Process
- Sample Interview Summary template

**Length:** ~200-250 lines  
**Quality:** Professional BA toolkit

#### 18. templates/excel-risk-register-structure.md ✅
**Status:** COMPLETE
**Purpose:** Guide for creating Excel Risk Register (NOT executable, just structure guide)

**Content:**
- Sheet structure (columns to create)
- Column definitions:
  - Risk ID (text)
  - Description (text, wrap enabled)
  - Category (dropdown list)
  - Probability (dropdown: Very Low, Low, Medium, High, Very High)
  - Probability Score (formula: VLOOKUP)
  - Impact (dropdown: 1-10)
  - Risk Score (formula: =Probability_Score * Impact)
  - Risk Level (formula: IF nested for Critical/High/Medium/Low)
  - Mitigation Plan (text, wrap enabled)
  - Owner (dropdown or text)
  - Status (dropdown: Open, Mitigated, Closed)
  - Last Reviewed (date)
- Conditional Formatting rules:
  - Risk Level = Critical → Red fill
  - Risk Level = High → Orange fill
  - Risk Level = Medium → Yellow fill
  - Risk Level = Low → Green fill
- Data Validation setup
- Named Ranges to create
- Example formulas with cell references
- Chart recommendations (Risk Heat Map, Risk Distribution Pie)

**Length:** ~150-200 lines  
**Quality:** Step-by-step guide for PM to follow when using xlsx skill

#### 19. templates/excel-gantt-structure.md ✅
**Status:** COMPLETE (Nov 13, 2025)
**Purpose:** Guide for creating Excel Gantt Chart

**Content:**
- Sheet structure
- Column definitions:
  - Task ID (auto-number)
  - Task Name (text)
  - Start Date (date)
  - End Date (date)
  - Duration (formula: =End-Start)
  - % Complete (number, 0-100)
  - Predecessor (text, references Task ID)
  - Owner (text)
  - Status (dropdown)
- Timeline section:
  - Date headers (weekly or daily)
  - Conditional formatting for task bars
  - Today indicator (vertical line)
- Formulas for Gantt bars:
  - IF(AND(Date >= Start, Date <= End), "█", "")
  - Color based on status
- Critical Path highlighting
- Milestone markers (diamond shape)
- Dependencies arrows (manual or via connectors)
- Summary task formatting (bold, collapsed)
- Example with 20-task project

**Length:** ~150-200 lines  
**Quality:** Professional PM deliverable guide

---

#### 20. templates/ppt-status-report-structure.md ✅
**Status:** COMPLETE (Nov 13, 2025)
**Purpose:** Guide for creating PowerPoint Status Report (NOT executable, just structure)

**Content:**
- Recommended slide count: 6-8 slides
- Slide-by-slide structure:

**Slide 1: Title Slide**
- Project name
- Reporting period
- PM name
- Overall RAG status (large, centered)

**Slide 2: Executive Summary**
- RAG status breakdown (Schedule, Budget, Scope, Risk)
- 3-4 bullet summary
- Key highlight or concern (call-out box)

**Slide 3: Accomplishments**
- "What We Completed This Period"
- 5-7 bullets (concise)
- Icons for visual interest
- Deliverable highlights

**Slide 4: Issues & Risks**
- Two-column layout (Issues | Risks)
- Table format (Issue/Risk, Impact, Status, Owner)
- Top 3-5 each
- Color-coded by severity

**Slide 5: Budget & Schedule Status**
- Two charts:
  - Budget: Actual vs Planned (bar chart)
  - Schedule: Milestone timeline (Gantt-style)
- Key metrics as callout boxes
- Variance indicators

**Slide 6: Next Steps**
- "Planned for Next Period"
- 5-7 bullets
- Decisions needed (if any)
- Upcoming milestones

**Design Guidelines:**
- Color scheme: Professional blues/grays
- Font: Sans-serif (Calibri, Arial)
- Minimal text (rule of 6: max 6 bullets, 6 words per bullet)
- High contrast for readability
- Consistent layout

**Length:** ~200-250 lines  
**Quality:** Executive-presentation ready

#### 21. templates/ppt-sprint-review-structure.md ✅
**Status:** COMPLETE (Nov 13, 2025)
**Purpose:** Guide for creating PowerPoint Sprint Review Presentation

**Content:**
- Recommended slide count: 8-10 slides

**Slide 1: Title**
- Sprint number
- Dates
- Sprint goal

**Slide 2: Sprint Goal & Metrics**
- Sprint goal statement
- Key metrics (velocity, commitment, completed)
- Team composition

**Slide 3: Velocity Chart**
- Last 5-6 sprints
- Bar chart with trend line
- Observations

**Slide 4: Sprint Burndown**
- Ideal vs Actual burndown
- Scope changes noted
- Analysis

**Slide 5-7: Completed Stories (Demo)**
- One story per slide
- Story title + acceptance criteria
- Screenshot or demo recording
- User value statement

**Slide 8: Incomplete Work**
- Carry-over stories
- Reasons
- Plan forward

**Slide 9: Retrospective Highlights**
- What went well (2-3 items)
- What to improve (2-3 items)
- Action items

**Slide 10: Next Sprint Preview**
- Sprint N+1 goal
- Top priorities
- Dependencies/risks

**Design Guidelines:**
- Agile-friendly colors (greens, blues)
- Screenshots prominent
- Data visualizations clear
- Demo-focused (not text-heavy)

**Length:** ~200-250 lines  
**Quality:** Product Owner / stakeholder demo ready

---

## ✅ COMPLETION SUMMARY

### Final Delivery Status
**All 26 files completed on November 13, 2025**

### Quality Verification
- ✅ All files follow defined structure
- ✅ Consistent style across skill
- ✅ Comprehensive production-ready content
- ✅ Real-world examples included
- ✅ Proper markdown formatting
- ✅ All SKILL.md references verified
- ✅ Enterprise/PMP standard achieved

### Files Completed Today (Nov 13)
1. ✅ excel-gantt-structure.md
2. ✅ ppt-status-report-structure.md
3. ✅ ppt-sprint-review-structure.md

### Ready for Distribution
**Package using:**
```bash
python scripts/package_skill.py D:\Projects\claude-capabilities-skills\Senior_Project_Manager
```

---

## ✅ FINAL FOLDER STRUCTURE

```
Senior_Project_Manager/
├── SKILL.md ✅
├── references/ (7 files)
│   ├── agile-scrum.md ✅
│   ├── hybrid-approach.md ✅
│   ├── metrics-reporting.md ✅
│   ├── pm-tools-guide.md ✅
│   ├── pmp-framework.md ✅
│   ├── risk-stakeholder.md ✅
│   └── waterfall-predictive.md ✅
├── scripts/ (5 files)
│   ├── asana_tracker.py ✅
│   ├── burndown_generator.py ✅
│   ├── jira_sync.py ✅
│   ├── project_analyzer.py ✅
│   └── risk_calculator.py ✅
└── templates/ (12 files)
    ├── brd-template.md ✅
    ├── excel-gantt-structure.md ✅ ⭐
    ├── excel-risk-register-structure.md ✅
    ├── ppt-sprint-review-structure.md ✅ ⭐
    ├── ppt-status-report-structure.md ✅ ⭐
    ├── project-charter-template.md ✅
    ├── requirements-traceability-matrix.md ✅
    ├── retrospective-template.md ✅
    ├── risk-register-template.md ✅
    ├── sprint-planning-template.md ✅
    ├── stakeholder-interview-guide.md ✅
    └── status-report-template.md ✅

Total: 26 files ✅
⭐ = Completed Nov 13, 2025
```

---

## ✅ EFFORT COMPLETED

**Total Development Time:** ~11 hours
- Scripts (5): ~4 hours ✅
- Core Templates (5): ~2.5 hours ✅
- BRD Templates (3): ~2 hours ✅
- Excel Guides (2): ~1 hour ✅
- PPT Guides (2): ~1.5 hours ✅

**Quality:** Enterprise/production-ready

---

## DEPENDENCIES & NOTES

### Python Scripts Dependencies
```
# Required for burndown_generator.py
pip install matplotlib

# Required for jira_sync.py
pip install jira

# Required for asana_tracker.py
pip install asana
```

All scripts should gracefully handle missing dependencies with helpful error messages.

### Integration Points
- burndown_generator.py should be callable from jira_sync.py
- project_analyzer.py should be able to import from risk_calculator.py
- Templates should reference each other appropriately (e.g., BRD template references RTM template)

### File Naming Conventions
- Python scripts: snake_case.py
- Markdown templates: kebab-case.md
- All lowercase
- Descriptive names

---

## ✅ FINAL DELIVERABLE - COMPLETE

**All 26 files done!**

**Package Command:**
```bash
python scripts/package_skill.py D:\Projects\claude-capabilities-skills\Senior_Project_Manager
```

**Target Users:**
- ✅ PMP-certified PMs
- ✅ Agile/Scrum practitioners
- ✅ Enterprise PM teams
- ✅ PM tool power users
- ✅ BA/PM hybrid roles

---

**STATUS: PRODUCTION READY ✅**  
**Date: November 13, 2025**  
**Version: 1.0.0**
