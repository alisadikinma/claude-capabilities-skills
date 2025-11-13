# Metrics & Reporting Reference

Comprehensive guide for project metrics, KPIs, and reporting across methodologies and tools.

## Agile Metrics

### Velocity

**Definition:** Story points completed per sprint

**Formula:**
```
Velocity = Σ Story Points (Completed) / Sprint
```

**Tracking:**
- Calculate per sprint
- Track 6-sprint rolling average
- Use for forecasting

**Healthy Trends:**
- Stable or gradually increasing
- Low variance sprint-to-sprint
- Predictable within ±20%

**Red Flags:**
- Declining trend over 3+ sprints
- High variance (>30% sprint-to-sprint)
- Inflation without productivity increase

**Tools:**
- Jira: Velocity Chart (Reports → Velocity Chart)
- Asana: Custom field aggregation
- Excel: `=SUMIF(Sprint, "Sprint 5", Points)`

### Sprint Burndown

**Definition:** Remaining work vs time in sprint

**Components:**
- Ideal burndown line (linear)
- Actual burndown (updated daily)
- Scope change indicator

**Patterns:**

```
Good Pattern:
│
│\
│ \___  (Steady decline)
│     \___
└─────────── Days

Bad Pattern:
│
│────────\  (Late completion)
│         \___
│            \___
└─────────────── Days
```

**Analysis:**
- Flat line = No progress
- Rising line = Scope increase
- Steep drop at end = Poor estimation or hiding progress

**Tools:**
- Jira: Built-in burndown chart
- Linear: Auto-generated per cycle
- Excel: Line chart with dual series

### Cycle Time

**Definition:** Time from "Started" to "Done"

**Formula:**
```
Cycle Time = Done Date - Start Date
```

**Targets:**
- Small stories: 1-3 days
- Medium stories: 3-5 days
- Large stories: 5-10 days

**Analysis:**
- High cycle time = Bottlenecks or oversized work
- Increasing trend = Process degradation
- High variance = Inconsistent story sizing

**Tools:**
- Jira: Control Chart (Reports)
- Linear: Insights → Cycle time
- ClickUp: Time tracking reports

### Escaped Defects

**Definition:** Bugs found after sprint closure

**Formula:**
```
Escaped Defects Rate = Bugs (Post-Sprint) / Total Stories × 100%
```

**Targets:**
- Excellent: <5%
- Good: 5-10%
- At Risk: 10-20%
- Poor: >20%

**Root Causes:**
- Inadequate testing
- Unclear Definition of Done
- Technical debt accumulation
- Insufficient code review

**Tools:**
- Jira: Filter → `type = Bug AND created >= sprint.end`
- Asana: Custom field "Defect Escaped"
- Notion: Formula in Bugs database

### Lead Time

**Definition:** Time from backlog entry to done

**Formula:**
```
Lead Time = Done Date - Created Date
```

**Analysis:**
- Lead Time = Cycle Time + Wait Time
- Long wait time = Backlog prioritization issue
- Growing lead time = Capacity problem

**Benchmarks:**
- Urgent: <1 week
- Normal: 2-4 weeks
- Low priority: 1-2 months

## Waterfall Metrics

### Schedule Performance Index (SPI)

**Definition:** Ratio of work performed to work planned

**Formula:**
```
SPI = EV / PV

Where:
EV = Earned Value (% Complete × Budget)
PV = Planned Value (Scheduled work value)
```

**Interpretation:**
- SPI = 1.0 → On schedule
- SPI > 1.0 → Ahead of schedule
- SPI < 1.0 → Behind schedule

**Example:**
```
Project: $100K budget, 50% complete
Planned: 60% complete by now
EV = 0.50 × $100K = $50K
PV = 0.60 × $100K = $60K
SPI = $50K / $60K = 0.83 (17% behind)
```

**Tools:**
- MS Project: EV analysis built-in
- Excel: Manual calculation with formulas
- Primavera: EV reports

### Cost Performance Index (CPI)

**Definition:** Ratio of work performed to actual cost

**Formula:**
```
CPI = EV / AC

Where:
AC = Actual Cost (Money spent)
```

**Interpretation:**
- CPI = 1.0 → On budget
- CPI > 1.0 → Under budget
- CPI < 1.0 → Over budget

**Example:**
```
EV = $50K (50% of $100K)
AC = $60K (actually spent)
CPI = $50K / $60K = 0.83 (17% over budget)
```

**Critical Threshold:**
- CPI < 0.90 → Executive escalation needed

### Schedule Variance (SV)

**Definition:** Difference between earned and planned value

**Formula:**
```
SV = EV - PV
SV% = (EV - PV) / PV × 100%
```

**Interpretation:**
- SV = 0 → On schedule
- SV > 0 → Ahead
- SV < 0 → Behind

**Example:**
```
EV = $50K, PV = $60K
SV = $50K - $60K = -$10K
SV% = -$10K / $60K = -16.7%
```

### Cost Variance (CV)

**Definition:** Difference between earned value and actual cost

**Formula:**
```
CV = EV - AC
CV% = (EV - AC) / EV × 100%
```

**Interpretation:**
- CV = 0 → On budget
- CV > 0 → Under budget
- CV < 0 → Over budget

**Recovery Actions (CV < 0):**
- Reduce scope
- Optimize resources
- Negotiate vendor rates
- Use contingency reserve

### Milestone Hit Rate

**Definition:** Percentage of milestones achieved on time

**Formula:**
```
Hit Rate = On-Time Milestones / Total Milestones × 100%
```

**Targets:**
- World-class: >95%
- Good: 85-95%
- At Risk: 70-85%
- Poor: <70%

**Tracking:**
```
Phase 1:
├─ Milestone 1: ✅ On time
├─ Milestone 2: ⚠️ 2 days late
└─ Milestone 3: ✅ On time
Hit Rate = 2/3 = 67% (At Risk)
```

## Universal KPIs

### Customer Satisfaction (CSAT)

**Measurement:**
- Survey after deliverable/sprint
- 1-5 or 1-10 scale
- Question: "How satisfied are you with [deliverable]?"

**Formula:**
```
CSAT = (Satisfied Responses / Total Responses) × 100%

Where Satisfied = 4-5 on 5-point scale
```

**Benchmarks:**
- Excellent: >90%
- Good: 75-90%
- Poor: <75%

**Improvement Actions:**
- Gather qualitative feedback
- Address common complaints
- Increase stakeholder engagement

### Net Promoter Score (NPS)

**Question:** "How likely are you to recommend this project/team to others?"

**Scale:** 0-10

**Categories:**
- Promoters: 9-10
- Passives: 7-8
- Detractors: 0-6

**Formula:**
```
NPS = % Promoters - % Detractors
```

**Example:**
```
Survey: 100 responses
Promoters: 60 (60%)
Passives: 25 (25%)
Detractors: 15 (15%)
NPS = 60% - 15% = +45
```

**Benchmarks:**
- Excellent: >50
- Good: 30-50
- Acceptable: 0-30
- Poor: <0

### Return on Investment (ROI)

**Formula:**
```
ROI = (Benefit - Cost) / Cost × 100%
```

**Example:**
```
Project Cost: $500K
Annual Benefit: $800K
ROI = ($800K - $500K) / $500K = 60%
```

**Considerations:**
- Include ongoing operational costs
- Factor in time to value
- Account for opportunity cost
- Risk-adjust benefits

### Team Utilization

**Definition:** Productive time as % of available time

**Formula:**
```
Utilization = Productive Hours / Available Hours × 100%
```

**Targets:**
- Healthy: 70-85%
- Maximum sustainable: 85%
- Burnout risk: >90%

**Non-Productive Time:**
- Meetings (excessive)
- Context switching
- Waiting on dependencies
- Administrative overhead

**Optimization:**
- Reduce meeting load
- Batch similar work
- Remove blockers quickly
- Automate admin tasks

### Quality Metrics

**Defect Density:**
```
Defects per KLOC = Total Defects / (Lines of Code / 1000)
```

**Benchmarks:**
- Excellent: <1 defect/KLOC
- Good: 1-5 defects/KLOC
- Poor: >10 defects/KLOC

**Test Coverage:**
```
Coverage = Tested Code / Total Code × 100%
```

**Targets:**
- Critical paths: >90%
- Core features: >80%
- Overall: >70%

## Reporting Formats

### Executive Dashboard

**One-Page Format:**

```
PROJECT STATUS: [🟢 GREEN / 🟡 YELLOW / 🔴 RED]

SUMMARY:
- 65% complete (on schedule)
- $450K spent of $500K budget
- No critical risks

KEY METRICS:
├─ Schedule: SPI = 1.02 (2% ahead)
├─ Budget: CPI = 1.11 (11% under)
├─ Quality: 3 defects (low)
└─ Team: 82% utilization

TOP 3 RISKS:
1. [MEDIUM] Vendor delay - Mitigated
2. [LOW] Resource vacation - Planned
3. [LOW] API changes - Monitoring

NEXT WEEK:
- Complete Phase 2 milestone
- UAT with stakeholders
- Sprint 6 planning
```

**Tools:**
- PowerPoint: One-slide summary
- Jira: Dashboard with gadgets
- Notion: Status database with rollups

### Weekly Status Report

**Structure:**

```markdown
# Week Ending: [Date]

## Executive Summary
- Overall status: GREEN
- Key accomplishment: Feature X shipped
- Critical issue: None

## Accomplishments This Week
1. Completed user authentication module
2. Deployed to staging environment
3. Completed security audit
4. Sprint 5 retrospective conducted

## Planned for Next Week
1. Begin integration testing
2. Stakeholder demo on Thursday
3. Sprint 6 planning
4. Address audit findings

## Metrics
- Velocity: 32 points (target: 30)
- Burndown: On track
- Defects: 2 (low severity)

## Issues & Risks
| Issue | Impact | Status | Owner |
|-------|--------|--------|-------|
| API latency | MED | Investigating | Dev Lead |
| Vendor delay | LOW | Monitoring | PM |

## Budget Status
- Spent: $450K / $500K (90%)
- Forecast: On budget
- Variance: +$10K (2% under)

## Schedule Status
- Current phase: 65% complete
- Milestone: On track for 3/15
- Critical path: No delays
```

### Sprint Review Metrics

**Agile-Specific Report:**

```
SPRINT 5 REVIEW

Duration: 2 weeks (Mar 1-14)
Goal: Complete user management module

VELOCITY:
- Committed: 30 points
- Completed: 28 points
- Carry over: 2 points (7%)

BURNDOWN:
- Day 1: 30 points remaining
- Day 10: 5 points remaining (on track)
- Day 14: 2 points remaining
- Pattern: Steady decline ✅

COMPLETED STORIES:
1. User registration (5 pts) ✅
2. Login/logout (3 pts) ✅
3. Password reset (5 pts) ✅
4. Profile management (8 pts) ✅
5. Role assignment (7 pts) ✅

INCOMPLETE:
6. Bulk user import (2 pts) → Carry to Sprint 6

RETROSPECTIVE ACTIONS:
1. Improve story splitting
2. Daily standup at 9:30 AM
3. Pair programming for complex tasks

TEAM HAPPINESS: 8/10 👍
```

## PM Tools Integration

### Jira Reports

**Built-in Reports:**
1. **Velocity Chart**
   - Path: Reports → Agile → Velocity Chart
   - Shows points per sprint (bar chart)
   - Trend line for forecasting

2. **Burndown Chart**
   - Path: Reports → Agile → Sprint Burndown
   - Daily remaining work
   - Scope change indicator

3. **Cumulative Flow**
   - Path: Reports → Agile → Cumulative Flow
   - Work distribution by status
   - Identifies bottlenecks

4. **Control Chart**
   - Path: Reports → Agile → Control Chart
   - Cycle time visualization
   - Outlier detection

5. **Epic Report**
   - Path: Reports → Agile → Epic Report
   - Epic progress tracking
   - Story completion breakdown

**Custom Dashboards:**
```
Sprint Health Dashboard:
├─ Gadget: Sprint Burndown
├─ Gadget: Velocity Chart
├─ Gadget: Issue Statistics (pie chart)
├─ Gadget: Assigned to Me (filter)
└─ Gadget: Created vs Resolved (chart)
```

**JQL for Metrics:**
```jql
# Velocity calculation
project = PROJ AND sprint in (5, 6, 7, 8, 9) AND resolution = Done

# Defect rate
project = PROJ AND type = Bug AND created >= -14d

# Cycle time
project = PROJ AND status = Done AND resolved >= -30d
```

### Asana Reports

**Portfolio Dashboard:**
- Path: Portfolios → Dashboard
- Shows: Status, workload, timeline
- Custom fields for KPIs

**Workload View:**
- Path: Project → Workload
- Capacity per person
- Over/under allocation
- Time period selection

**Timeline (Gantt):**
- Path: Project → Timeline
- Task dependencies
- Critical path (inferred)
- Date range filtering

**Custom Reports:**
```
Status Report:
├─ Tasks by status (pie chart)
├─ Tasks by assignee (bar chart)
├─ Upcoming due dates (list)
└─ Overdue tasks (list)
```

### Excel Analytics

**Velocity Tracker:**
```excel
| Sprint | Committed | Completed | Variance |
|--------|-----------|-----------|----------|
| 1      | 25        | 20        | -5       |
| 2      | 25        | 24        | -1       |
| 3      | 26        | 28        | +2       |
| Avg    | 25.3      | 24.0      | -1.3     |

Formula (Variance): =C2-B2
Chart: Line chart with Committed & Completed
```

**Risk Heat Map:**
```excel
| Risk ID | Probability | Impact | Score | Color |
|---------|-------------|--------|-------|-------|
| R01     | High (3)    | High   | 9     | RED   |
| R02     | Med (2)     | Low    | 2     | GREEN |

Formula (Score): =B2*C2
Conditional Formatting:
- RED: >=6
- YELLOW: 3-5
- GREEN: <=2
```

**Earned Value:**
```excel
| Metric | Formula               | Value   |
|--------|-----------------------|---------|
| PV     | Planned % × Budget    | $60K    |
| EV     | Actual % × Budget     | $50K    |
| AC     | Actual Cost           | $55K    |
| SPI    | =B3/B2                | 0.83    |
| CPI    | =B3/B4                | 0.91    |
| SV     | =B3-B2                | -$10K   |
| CV     | =B3-B4                | -$5K    |

Status: 🔴 RED (SPI < 0.90)
```

## Best Practices

### Metric Selection

**Choose metrics that:**
1. **Drive behavior** you want to encourage
2. **Are actionable** (can respond to changes)
3. **Are measurable** (objective data)
4. **Align with goals** (support strategy)

**Avoid:**
- Vanity metrics (look good but meaningless)
- Lagging-only indicators (no time to react)
- Too many metrics (analysis paralysis)
- Metrics that encourage gaming

### Reporting Cadence

**Daily:**
- Standup updates
- Burndown chart update
- Blocker identification

**Weekly:**
- Status report to stakeholders
- Risk register review
- Velocity tracking

**Sprint/Monthly:**
- Sprint review metrics
- Retrospective outcomes
- Portfolio dashboard
- Executive summary

**Quarterly:**
- Strategic KPIs
- ROI analysis
- Team satisfaction survey
- Lessons learned

### Data Quality

**Ensure:**
1. **Timely updates** (daily for burndown, weekly for status)
2. **Consistent definitions** (everyone calculates same way)
3. **Accurate inputs** (validate data sources)
4. **Complete data** (no missing sprints/tasks)

**Common Issues:**
- Stories closed late (skews velocity)
- Points changed after sprint (invalidates burndown)
- Tasks in wrong status (incorrect cycle time)
- Manual calculations (human error)

### Automation

**Automate when possible:**
- Jira → Slack daily summary
- Excel → Email weekly report
- API → Custom dashboard
- Scripts → Metric calculations

**Example Python:**
```python
# Auto-generate weekly status from Jira
import jira

jira = JIRA('https://mycompany.atlassian.net', auth=('user', 'token'))

issues_done = jira.search_issues('project=PROJ AND status=Done AND resolved >= -7d')
issues_planned = jira.search_issues('project=PROJ AND status="To Do" AND sprint=6')

print(f"Completed this week: {len(issues_done)}")
print(f"Planned for next week: {len(issues_planned)}")
```

## Common Pitfalls

### Metric Gaming

**Problem:** Team optimizes for metrics instead of outcomes

**Examples:**
- Inflating story points to boost velocity
- Closing stories prematurely to hit targets
- Cherry-picking easy tasks
- Hiding defects to improve quality metrics

**Solutions:**
- Measure multiple dimensions (can't game all)
- Focus on outcomes, not outputs
- Review work quality, not just metrics
- Celebrate learning, not just performance

### Analysis Paralysis

**Problem:** Too many metrics, no action

**Symptoms:**
- Dashboards with 20+ metrics
- Weekly reports exceed 5 pages
- Metrics not discussed in meetings
- No decisions based on data

**Solutions:**
- Limit to 5-7 key metrics
- Tie each metric to action threshold
- Review and act on data in rituals
- Archive unused metrics

### Lagging Indicators Only

**Problem:** All metrics show past, no predictive power

**Example:**
- Velocity (lagging)
- Defect count (lagging)
- Budget spent (lagging)

**Solution:** Balance with leading indicators
- Team happiness → Predicts velocity
- Code review thoroughness → Predicts defects
- Burn rate trend → Predicts budget

### Inconsistent Measurement

**Problem:** Definitions change, making trends meaningless

**Example:**
- Sprint 1-3: Velocity = completed points
- Sprint 4+: Velocity = committed points
- Result: Can't compare trends

**Solution:**
- Document calculation methods
- Standardize across teams
- Version metric definitions
- Baseline when changing methods

---

**Remember:** Metrics should inform decisions, not replace judgment. A PM who only looks at dashboards misses the human signals that numbers can't capture.
