# Excel Gantt Chart Structure

## File Organization

### Sheet 1: Task List
**Purpose:** Master task data with timeline metadata

**Required Columns:**
| Column | Description | Data Type | Example |
|--------|-------------|-----------|---------|
| A | Task ID | Text | TASK-001 |
| B | Task Name | Text | Design database schema |
| C | Phase | Text | Planning, Design, Build, Test, Deploy |
| D | Owner | Text | John Doe |
| E | Start Date | Date | 2024-01-15 |
| F | End Date | Date | 2024-01-22 |
| G | Duration (Days) | Number | `=F2-E2` |
| H | Predecessor | Text | TASK-002 (comma-separated IDs) |
| I | % Complete | Percentage | 75% |
| J | Status | Text | Not Started, In Progress, Complete, On Hold |

**Conditional Formatting:**
```
Status Column:
- Not Started: Gray background
- In Progress: Blue background
- Complete: Green background
- On Hold: Red background

% Complete Column:
- 0-25%: Red progress bar
- 26-75%: Yellow progress bar
- 76-100%: Green progress bar
```

### Sheet 2: Timeline (Gantt Visualization)
**Purpose:** Visual timeline chart

**Structure:**
- Row 1: Month headers (merged cells)
- Row 2: Week numbers or dates
- Rows 3+: Tasks with bar chart

**Timeline Columns Setup:**
```
Columns K onwards represent timeline:
- Each column = 1 day or 1 week (depending on scale)
- Column headers: Dates (e.g., Jan 1, Jan 8, Jan 15...)
- Cell formulas check if date falls within task range
```

**Bar Chart Formula (Cell K3 onwards):**
```excel
=IF(AND(K$2>=$E3, K$2<=$F3), "█", "")
```

**Logic:**
- If timeline date (K$2) >= Start Date (E3) AND <= End Date (F3)
- Display block character "█" (creates bar)
- Apply conditional formatting based on status

**Conditional Formatting for Bars:**
```
Apply to Range: K3:ZZ999
Formulas:
1. Critical Path (Red): =$J3="Critical"
2. In Progress (Blue): =$J3="In Progress"
3. Complete (Green): =$J3="Complete"
4. Not Started (Gray): =$J3="Not Started"
```

### Sheet 3: Milestones
**Purpose:** Key project checkpoints

**Columns:**
| Column | Description | Example |
|--------|-------------|---------|
| A | Milestone ID | MS-001 |
| B | Milestone Name | Project Kickoff |
| C | Target Date | 2024-01-15 |
| D | Status | Complete, At Risk, On Track |
| E | Dependencies | TASK-001, TASK-005 |
| F | Notes | Stakeholder approval received |

**Milestone Markers in Gantt:**
- Add diamond symbol (◆) in timeline on milestone date
- Use different color than task bars

### Sheet 4: Resources
**Purpose:** Team capacity and allocation

**Columns:**
| Column | Description | Example |
|--------|-------------|---------|
| A | Resource Name | Sarah Johnson |
| B | Role | Developer |
| C | Allocated Hours/Week | 40 |
| D | Current Tasks | TASK-003, TASK-007 |
| E | Utilization % | 95% |
| F | Availability Start | 2024-01-01 |
| G | Availability End | 2024-12-31 |

### Sheet 5: Dashboard (Optional)
**Purpose:** Executive summary

**Components:**
1. **Project Overview Box:**
   - Project Name
   - PM Name
   - Start Date
   - End Date
   - Overall % Complete

2. **Status Summary:**
   - Total Tasks
   - Complete
   - In Progress
   - Not Started
   - Overdue

3. **Phase Progress Chart:**
   - Pie or bar chart showing % complete by phase

4. **Critical Path Highlight:**
   - List of critical path tasks
   - Days ahead/behind schedule

## Critical Path Calculation

**Step 1: Add Critical Path Column (Column K)**
```excel
=IF(SUMIF($H:$H, $A3, $G:$G)>0, "Yes", "No")
```
Logic: If any other task lists this task as predecessor, it's on critical path

**Step 2: Calculate Slack Time (Column L)**
```excel
=NETWORKDAYS($F3, MAX($F:$F)) - $G3
```
Zero slack = critical path

## Formulas Reference

### Duration Auto-Calculate
```excel
=NETWORKDAYS(E3, F3)
```
Excludes weekends

### % Complete Visual
```excel
=REPT("█", INT(I3*10))
```
Creates progress bar (10 blocks = 100%)

### Status Auto-Update
```excel
=IF(I3=1, "Complete", IF(I3>0, "In Progress", "Not Started"))
```

### Overdue Alert
```excel
=IF(AND(F3<TODAY(), J3<>"Complete"), "OVERDUE", "")
```

### Days Remaining
```excel
=IF(J3="Complete", 0, F3-TODAY())
```

## Dependencies Visualization

**Arrow Connection (Manual Steps):**
1. Insert Shapes > Arrow
2. Connect predecessor end to successor start
3. Format arrow: 1pt, Gray, Straight Connector

**Dependency Formula Check:**
```excel
=IF(COUNTIF($A:$A, H3)=0, "⚠️ Invalid Dependency", "✓")
```
Validates predecessor IDs exist

## Timeline Scaling Options

### Daily Scale (Detailed Projects)
- Each column = 1 day
- Suitable for: 1-3 month projects
- Column width: 3-5 characters

### Weekly Scale (Standard)
- Each column = 1 week
- Suitable for: 3-12 month projects
- Column width: 5-8 characters

### Monthly Scale (Strategic View)
- Each column = 1 month
- Suitable for: 1-3 year projects
- Column width: 10-15 characters

## Color Scheme

**Task Bars:**
- Critical Path: Red (#FF0000)
- In Progress: Blue (#4472C4)
- Complete: Green (#70AD47)
- Not Started: Gray (#A6A6A6)
- On Hold: Orange (#FFC000)

**Backgrounds:**
- Header Row: Dark Blue (#203864)
- Milestone Row: Light Yellow (#FFF2CC)
- Weekend Columns: Light Gray (#F2F2F2)

## Print Settings

**Page Setup:**
- Orientation: Landscape
- Scaling: Fit to 1 page wide
- Print Titles: Repeat Rows 1-2 on each page
- Margins: Narrow (0.25 inch)

**Print Area:**
- Include: Task List (A:J) + Timeline (up to last task end date)
- Exclude: Empty rows and columns beyond project scope

## Sample Data

**Example Task Entry:**
```
Task ID: TASK-001
Task Name: Requirement Gathering
Phase: Planning
Owner: Jane Smith
Start Date: 2024-01-15
End Date: 2024-01-22
Duration: 5 days (formula)
Predecessor: None
% Complete: 100%
Status: Complete
```

**Example with Dependency:**
```
Task ID: TASK-002
Task Name: Design Mockups
Phase: Design
Owner: John Doe
Start Date: 2024-01-23
End Date: 2024-02-05
Duration: 10 days
Predecessor: TASK-001
% Complete: 60%
Status: In Progress
```

## Advanced Features

### Baseline Comparison
Add columns:
- Baseline Start Date
- Baseline End Date
- Variance (days)

Formula for variance:
```excel
=F3-[Baseline_End_Date]
```

### Resource Loading Chart
Create pivot table:
- Rows: Resource Name
- Columns: Week
- Values: Sum of allocated hours

### Automatic Email Alerts (with VBA)
Trigger when:
- Task becomes overdue
- Task reaches 90% complete
- Milestone approaching (5 days before)

## Best Practices

1. **Keep task granularity consistent:** 2-10 day tasks ideal
2. **Update weekly:** Set recurring calendar reminder
3. **Lock headers:** Freeze panes at Row 3, Column K
4. **Version control:** Save as "Gantt_YYYYMMDD.xlsx"
5. **Backup formulas:** Keep formula sheet hidden
6. **Print regularly:** Weekly printout for standups
7. **Color-code phases:** Use fill color for phase column
8. **Add legends:** Create small legend box explaining colors

## Common Errors & Fixes

**Error: #VALUE! in Duration**
- Cause: Non-date value in Start/End
- Fix: Use Data Validation (Date format only)

**Error: Bars not showing**
- Cause: Column width too narrow or wrong date format
- Fix: Widen columns, check date headers match task dates

**Error: Circular dependency**
- Cause: Task lists itself as predecessor
- Fix: Audit predecessor column, remove self-references

**Error: Timeline not scrolling**
- Cause: Freeze panes incorrect
- Fix: View > Freeze Panes > Freeze Top Row + Freeze First Column

## Export Options

**To PDF:**
1. File > Save As > PDF
2. Options: Fit to 1 page wide
3. Include: Task list + visible timeline only

**To MS Project:**
1. Save as XML
2. Import into MS Project
3. Map columns to Project fields

**To PowerPoint:**
1. Copy Gantt range
2. Paste Special > Picture (Enhanced Metafile)
3. Resize in slide

---

**Integration Note:** This Excel structure works best when combined with:
- Risk Register (separate Excel sheet)
- Status Report (PowerPoint using data from this Gantt)
- Resource Plan (separate sheet or project plan)
