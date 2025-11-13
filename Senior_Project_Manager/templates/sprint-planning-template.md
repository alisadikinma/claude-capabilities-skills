# Sprint Planning

**Sprint #:** [Number]  
**Sprint Goal:** [One clear, achievable objective for this sprint]  
**Sprint Dates:** [Start Date] to [End Date]  
**Team:** [Team Name]  
**Facilitated By:** [Scrum Master Name]  
**Date:** [YYYY-MM-DD]

---

## Sprint Information

| Detail | Value |
|--------|-------|
| **Sprint Number** | [e.g., Sprint 15] |
| **Sprint Duration** | [e.g., 2 weeks / 10 working days] |
| **Start Date** | [YYYY-MM-DD] |
| **End Date** | [YYYY-MM-DD] |
| **Sprint Review** | [Date & Time] |
| **Sprint Retrospective** | [Date & Time] |
| **Sprint Goal** | [Clear, concise goal that guides sprint work] |

---

## Team Capacity Calculation

### Team Composition
| Name | Role | Availability (%) | Days Available | Hours Available |
|------|------|------------------|----------------|-----------------|
| [Name] | Developer | 100% | 10 | 80 |
| [Name] | Developer | 80% | 8 | 64 |
| [Name] | QA Engineer | 100% | 10 | 80 |
| [Name] | Designer | 50% | 5 | 40 |
| **TOTAL** | | | | **264 hours** |

### Capacity Adjustments
- **PTO/Holidays:** [X hours] ([Name] on vacation Days 8-10)
- **Meetings/Ceremonies:** [X hours] (Standups, reviews, retro)
- **Support/Maintenance:** [X hours] (Production support rotation)
- **Other:** [X hours] ([Description])

**Adjusted Total Capacity:** [Total Hours] hours

### Capacity by Story Points
- Average velocity: [X] points/sprint
- Recent velocity (last 3 sprints): [A], [B], [C] points
- **Target Commitment:** [X] story points (based on avg velocity)

---

## Sprint Backlog

### Committed User Stories

| ID | User Story | Story Points | Assignee | Priority | Status |
|----|------------|--------------|----------|----------|--------|
| US-101 | As a [user], I want [feature] so that [value] | 8 | [Name] | High | Not Started |
| US-102 | As a [user], I want [feature] so that [value] | 5 | [Name] | High | Not Started |
| US-103 | As a [user], I want [feature] so that [value] | 3 | [Name] | Medium | Not Started |
| US-104 | As a [user], I want [feature] so that [value] | 5 | [Name] | Medium | Not Started |
| US-105 | As a [user], I want [feature] so that [value] | 8 | [Name] | Low | Not Started |

**Total Committed:** [X] story points

### Stretch Goals (if capacity allows)
| ID | User Story | Story Points | Assignee | Priority |
|----|------------|--------------|----------|----------|
| US-106 | As a [user], I want [feature] so that [value] | 3 | [Name] | Low |

---

## User Story Template

Use this format for each backlog item:

```
User Story ID: US-XXX
Title: [Brief title]

User Story:
As a [type of user]
I want [action/feature]
So that [benefit/value]

Acceptance Criteria:
- [ ] Given [context], when [action], then [expected result]
- [ ] Given [context], when [action], then [expected result]
- [ ] [Additional criteria]

Technical Notes:
- [Technical consideration 1]
- [Technical consideration 2]

Dependencies:
- [Dependency on US-YYY]
- [External dependency]

Estimated Effort: [X] story points
Priority: [High/Medium/Low]
Assigned To: [Name]
```

---

## Estimation Guidelines

### Planning Poker Scale (Fibonacci)
| Points | Complexity | Typical Duration | Examples |
|--------|------------|------------------|----------|
| 1 | Trivial | 1-2 hours | Config change, simple copy update |
| 2 | Simple | 2-4 hours | Small UI tweak, straightforward bug fix |
| 3 | Easy | 4-8 hours | Basic CRUD operation, simple form |
| 5 | Medium | 1-2 days | Feature with multiple components |
| 8 | Complex | 2-3 days | Integration with external API |
| 13 | Very Complex | 3-5 days | Major feature, significant refactoring |
| 21 | Epic-sized | >1 week | Too large, should be broken down |

**Estimation Process:**
1. Product Owner presents user story
2. Team asks clarifying questions
3. Each team member selects estimate privately
4. All reveal simultaneously (Planning Poker)
5. Discuss outliers (highest and lowest explain)
6. Re-vote if needed until consensus

**Velocity Reference:**
- Last sprint: [X] points completed
- Average (last 3): [Y] points
- Trend: [Increasing/Stable/Decreasing]

---

## Definition of Done (DoD)

A user story is "Done" when ALL criteria are met:

### Code Quality
- [ ] Code written and follows team standards
- [ ] Code reviewed and approved by peer
- [ ] Unit tests written (>80% coverage)
- [ ] All tests passing (unit, integration, e2e)
- [ ] No critical or high-severity bugs
- [ ] Code merged to main branch

### Documentation
- [ ] Technical documentation updated
- [ ] User-facing documentation created/updated
- [ ] Inline code comments for complex logic
- [ ] README updated if applicable

### Testing
- [ ] Functionality tested in dev environment
- [ ] QA testing completed and passed
- [ ] Edge cases and error handling validated
- [ ] Cross-browser/device testing (if applicable)
- [ ] Performance acceptable (no regressions)

### Acceptance
- [ ] Meets all acceptance criteria
- [ ] Product Owner reviewed and approved
- [ ] Deployed to staging environment
- [ ] Ready for production deployment

### Cleanup
- [ ] Feature flags configured (if applicable)
- [ ] Logging/monitoring set up
- [ ] No TODO/FIXME comments remain
- [ ] Unused code removed

---

## Dependencies & Blockers

### External Dependencies
| Dependency | Owner | Expected Date | Impact | Status |
|------------|-------|---------------|--------|--------|
| [e.g., API endpoint from Team B] | [Name/Team] | [YYYY-MM-DD] | US-101 blocked | In Progress |
| [e.g., Design mockups] | [Designer] | [YYYY-MM-DD] | US-103 delayed | Not Started |

### Internal Dependencies
| Story | Depends On | Reason |
|-------|------------|--------|
| US-102 | US-101 | Requires auth module from US-101 |
| US-104 | US-103 | UI components needed first |

### Known Risks/Blockers
1. **[Risk/Blocker]:** [Description]
   - **Impact:** [High/Medium/Low]
   - **Mitigation:** [Plan to address]
   - **Owner:** [Name]

2. **[Risk/Blocker]:** [Description]
   - **Impact:** [High/Medium/Low]
   - **Mitigation:** [Plan to address]
   - **Owner:** [Name]

---

## Sprint Risks

| Risk | Probability | Impact | Mitigation Strategy | Owner |
|------|-------------|--------|---------------------|-------|
| [e.g., Key developer PTO last 2 days] | High | Medium | Front-load critical work, pair programming | [Name] |
| [e.g., Third-party API unstable] | Medium | High | Build fallback mechanism, mock responses | [Name] |
| [e.g., Scope creep from stakeholders] | Low | High | Strict adherence to sprint goal, defer to backlog | SM |

---

## Capacity vs Commitment Analysis

### Capacity Check
- **Team Capacity:** [X] hours / [Y] story points
- **Total Committed:** [A] hours / [B] story points
- **Utilization:** [B/Y × 100]%

### Assessment
- ✅ **Healthy:** 80-90% utilization (buffer for unknowns)
- ⚠️ **At Risk:** >90% utilization (tight, no buffer)
- 🔴 **Overcommitted:** >100% utilization (reduce scope)

**Recommendation:** [Based on assessment, adjust commitment if needed]

---

## Sprint Goal Details

### Primary Objective
[Describe the sprint goal in 1-2 sentences. This should be the "why" behind the selected stories.]

Example:
*"Enable users to create and manage custom dashboards, providing personalized views of their key metrics and KPIs."*

### Success Criteria
The sprint will be successful if:
1. [Criterion 1: e.g., All 3 dashboard user stories completed and deployed]
2. [Criterion 2: e.g., Zero critical bugs in production]
3. [Criterion 3: e.g., Performance benchmarks met (<2s load time)]

### Alignment to Product Goals
- **Product Objective:** [e.g., Increase user engagement by 25%]
- **How This Sprint Contributes:** [e.g., Custom dashboards address #1 user request, expected to boost daily active users]

---

## Action Items from Planning

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [e.g., Request design review for US-103] | [Name] | [Day 1] | Pending |
| [e.g., Set up CI/CD pipeline for new service] | [Name] | [Day 2] | Pending |
| [e.g., Schedule knowledge transfer session] | [Name] | [Day 3] | Pending |
| [e.g., Clarify acceptance criteria with PO] | [Name] | [Today] | Complete |

---

## Daily Standup Schedule

**Time:** [e.g., 9:00 AM daily]  
**Duration:** 15 minutes  
**Location:** [Physical location or video link]

**Standup Format:**
- What did I complete yesterday?
- What will I work on today?
- Any blockers or impediments?

**Parking Lot:** Topics requiring longer discussion will be noted and addressed after standup with relevant parties only.

---

## Sprint Ceremonies Schedule

| Ceremony | Date | Time | Duration | Participants | Location |
|----------|------|------|----------|--------------|----------|
| **Sprint Planning** | [YYYY-MM-DD] | [HH:MM] | 2 hours | Full team + PO | [Room/Link] |
| **Daily Standups** | Daily | [HH:MM] | 15 min | Full team | [Room/Link] |
| **Backlog Refinement** | [YYYY-MM-DD] | [HH:MM] | 1 hour | Team + PO | [Room/Link] |
| **Sprint Review** | [YYYY-MM-DD] | [HH:MM] | 1 hour | Team + Stakeholders | [Room/Link] |
| **Sprint Retrospective** | [YYYY-MM-DD] | [HH:MM] | 45 min | Full team | [Room/Link] |

---

## Notes & Decisions

### Key Decisions Made
1. **[Decision]:** [Description]
   - **Rationale:** [Why this decision was made]
   - **Impact:** [Consequences of this decision]

2. **[Decision]:** [Description]
   - **Rationale:** [Why this decision was made]
   - **Impact:** [Consequences of this decision]

### Open Questions
1. [Question about US-XXX]
   - **Owner:** [Name to investigate]
   - **Due:** [Date]

2. [Question about integration approach]
   - **Owner:** [Name to investigate]
   - **Due:** [Date]

### Parking Lot
[Topics raised during planning that need follow-up but don't block sprint start]
- [Topic 1]
- [Topic 2]

---

## Follow-up from Previous Sprint

### Carry-Over Items
| ID | Story | Reason Not Completed | Status This Sprint |
|----|-------|----------------------|-------------------|
| US-095 | [Summary] | [e.g., Blocked by external dep] | Committed |
| US-097 | [Summary] | [e.g., Underestimated complexity] | Moved to backlog |

### Action Items from Last Retro
| Action | Owner | Status |
|--------|-------|--------|
| [e.g., Set up automated testing] | [Name] | ✅ Complete |
| [e.g., Document API usage] | [Name] | 🔄 In Progress |
| [e.g., Improve code review turnaround] | Team | 📋 Ongoing |

---

## Team Agreements

### Working Agreements (Reminder)
- Code review within 24 hours
- No meetings between 10-12 PM (focus time)
- All blockers raised in standup immediately
- Definition of Done must be met before moving to "Done"
- Pair programming on complex stories encouraged

### Communication Channels
- **Urgent blockers:** Slack #team-alerts
- **General questions:** Slack #team-dev
- **Technical discussions:** Slack #tech-architecture
- **Off-hours support:** On-call rotation (check schedule)

---

**Planning Complete:** [Date & Time]  
**Facilitated By:** [Scrum Master]  
**Participants:** [List attendees]

---

**Document Version:** 1.0  
**Last Updated:** [YYYY-MM-DD]  
**Next Review:** Sprint Review ([Date])
