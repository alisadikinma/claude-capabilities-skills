# PMP Framework Reference Guide

Comprehensive guide for Project Management Professional (PMP) standards based on PMBOK Guide.

## Table of Contents
1. [10 Knowledge Areas](#10-knowledge-areas)
2. [5 Process Groups](#5-process-groups)
3. [Project Charter](#project-charter)
4. [Integration Management](#integration-management)
5. [Scope Management](#scope-management)
6. [Schedule Management](#schedule-management)
7. [Cost Management](#cost-management)
8. [Quality Management](#quality-management)
9. [Resource Management](#resource-management)
10. [Communications Management](#communications-management)

---

## 10 Knowledge Areas

### 1. Project Integration Management
Coordinates all aspects of project management.

**Key Processes:**
- Develop Project Charter
- Develop Project Management Plan
- Direct and Manage Project Work
- Manage Project Knowledge
- Monitor and Control Project Work
- Perform Integrated Change Control
- Close Project or Phase

**Deliverables:**
- Project charter
- Project management plan
- Change requests
- Lessons learned register

### 2. Project Scope Management
Defines and controls what is and is not included.

**Key Processes:**
- Plan Scope Management
- Collect Requirements
- Define Scope
- Create WBS
- Validate Scope
- Control Scope

**Tools:**
- Requirements traceability matrix
- Work breakdown structure (WBS)
- Scope baseline

### 3. Project Schedule Management
Manages timely completion of project.

**Key Processes:**
- Plan Schedule Management
- Define Activities
- Sequence Activities
- Estimate Activity Durations
- Develop Schedule
- Control Schedule

**Tools:**
- Gantt charts
- Critical path method (CPM)
- Program Evaluation and Review Technique (PERT)

### 4. Project Cost Management
Plans, estimates, budgets, and controls costs.

**Key Processes:**
- Plan Cost Management
- Estimate Costs
- Determine Budget
- Control Costs

**Tools:**
- Earned Value Management (EVM)
- Cost baseline
- Funding requirements

### 5. Project Quality Management
Ensures project satisfies needs.

**Key Processes:**
- Plan Quality Management
- Manage Quality
- Control Quality

**Tools:**
- Quality metrics
- Quality audits
- Statistical sampling

### 6. Project Resource Management
Identifies, acquires, and manages resources.

**Key Processes:**
- Plan Resource Management
- Estimate Activity Resources
- Acquire Resources
- Develop Team
- Manage Team
- Control Resources

**Tools:**
- Resource histogram
- RACI matrix
- Team charter

### 7. Project Communications Management
Ensures timely and appropriate information flow.

**Key Processes:**
- Plan Communications Management
- Manage Communications
- Monitor Communications

**Tools:**
- Communication matrix
- Stakeholder register
- Performance reports

### 8. Project Risk Management
Identifies and manages project risks.

**Key Processes:**
- Plan Risk Management
- Identify Risks
- Perform Qualitative Risk Analysis
- Perform Quantitative Risk Analysis
- Plan Risk Responses
- Implement Risk Responses
- Monitor Risks

**Tools:**
- Risk register
- Probability and impact matrix
- Risk breakdown structure

### 9. Project Procurement Management
Purchases or acquires products/services.

**Key Processes:**
- Plan Procurement Management
- Conduct Procurements
- Control Procurements

**Tools:**
- Make-or-buy analysis
- Contract types (FFP, CPFF, T&M)
- Vendor evaluation criteria

### 10. Project Stakeholder Management
Identifies and manages stakeholders.

**Key Processes:**
- Identify Stakeholders
- Plan Stakeholder Engagement
- Manage Stakeholder Engagement
- Monitor Stakeholder Engagement

**Tools:**
- Stakeholder register
- Power/interest grid
- Engagement assessment matrix

---

## 5 Process Groups

### 1. Initiating Process Group

**Purpose:** Formally authorize project or phase.

**Key Activities:**
- Define project at high level
- Identify stakeholders
- Obtain authorization
- Assign project manager

**Major Deliverable: Project Charter**

**Charter Contents:**
1. Project title and description
2. Project manager assigned (with authority level)
3. Business case justification
4. Measurable project objectives
5. High-level requirements
6. High-level project description and boundaries
7. Overall project risk
8. Summary milestone schedule
9. Summary budget
10. Stakeholder list
11. Project approval requirements
12. Assigned project manager, responsibility, and authority
13. Sponsor authorization

**Example Charter Structure:**
```markdown
# PROJECT CHARTER

## Project Information
- Project Name: [Name]
- Project Manager: [Name]
- Sponsor: [Name]
- Date: [Date]

## Business Case
[Why this project? What problem does it solve?]

## Project Objectives
1. [SMART objective 1]
2. [SMART objective 2]
3. [SMART objective 3]

## High-Level Scope
In Scope:
- [Major deliverable 1]
- [Major deliverable 2]

Out of Scope:
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

## Milestones
| Milestone | Target Date |
|-----------|-------------|
| Kickoff | Month 1 |
| Design Complete | Month 3 |
| Go-Live | Month 6 |

## Budget
Total Budget: $XXX,XXX
- Phase 1: $XX,XXX
- Phase 2: $XX,XXX
- Contingency (15%): $XX,XXX

## Stakeholders
| Name | Role | Interest |
|------|------|----------|
| [Name] | Sponsor | High |
| [Name] | User Rep | High |

## Risks & Assumptions
**Key Risks:**
- [Risk 1]
- [Risk 2]

**Key Assumptions:**
- [Assumption 1]
- [Assumption 2]

## Approval
Sponsor Signature: _________________ Date: _______
PM Signature: _________________ Date: _______
```

### 2. Planning Process Group

**Purpose:** Establish scope, refine objectives, define actions.

**Key Activities:**
- Develop project management plan
- Define scope in detail
- Create WBS
- Develop schedule
- Estimate costs
- Plan quality, resources, communications
- Identify risks

**Major Deliverables:**
- Project management plan (integrated)
- Scope baseline (scope statement + WBS + WBS dictionary)
- Schedule baseline
- Cost baseline

**Planning Sequence:**
1. Define scope → Create WBS
2. Sequence activities → Estimate durations
3. Develop schedule → Estimate costs
4. Determine budget → Plan quality
5. Plan resources → Plan communications
6. Identify risks → Plan risk responses

### 3. Executing Process Group

**Purpose:** Complete work defined in project management plan.

**Key Activities:**
- Direct and manage project work
- Manage quality
- Acquire resources
- Develop team
- Manage communications
- Implement risk responses
- Conduct procurements
- Manage stakeholder engagement

**Focus Areas:**
- Deliverables production
- Team performance
- Vendor management
- Stakeholder engagement
- Information distribution

### 4. Monitoring and Controlling Process Group

**Purpose:** Track, review, and regulate progress and performance.

**Key Activities:**
- Monitor and control project work
- Perform integrated change control
- Validate scope
- Control scope, schedule, costs
- Control quality, resources, communications
- Monitor risks
- Monitor stakeholder engagement

**Key Metrics:**
- Schedule variance (SV)
- Cost variance (CV)
- Schedule performance index (SPI)
- Cost performance index (CPI)

**Earned Value Management:**
```
Planned Value (PV) = Budgeted cost of work scheduled
Earned Value (EV) = Budgeted cost of work performed
Actual Cost (AC) = Actual cost of work performed

Schedule Variance (SV) = EV - PV
Cost Variance (CV) = EV - AC

SPI = EV / PV (>1.0 is ahead, <1.0 is behind)
CPI = EV / AC (>1.0 is under budget, <1.0 is over budget)

Estimate at Completion (EAC) = BAC / CPI
Estimate to Complete (ETC) = EAC - AC
Variance at Completion (VAC) = BAC - EAC
```

### 5. Closing Process Group

**Purpose:** Finalize all activities to formally close project.

**Key Activities:**
- Close project or phase
- Close procurements
- Transfer deliverables
- Release resources
- Document lessons learned
- Archive project records

**Closing Checklist:**
- [ ] All deliverables accepted
- [ ] Customer sign-off obtained
- [ ] Final payments processed
- [ ] Contracts closed
- [ ] Resources released
- [ ] Lessons learned documented
- [ ] Project archives completed
- [ ] Celebrate success

---

## Work Breakdown Structure (WBS)

### Purpose
Decompose project into manageable components.

### Levels
```
Level 1: Project
├─ Level 2: Major Deliverables
│  ├─ Level 3: Sub-deliverables
│  │  ├─ Level 4: Work Packages
│  │  │  └─ Level 5: Activities
```

### Rules
1. 100% Rule: Sum of child elements = parent
2. Mutually exclusive: No overlap
3. Outcome-oriented: Focus on deliverables, not activities
4. Work package level: 8-80 hours rule

### Example: Website Development
```
1.0 Website Development Project
├─ 1.1 Project Management
│  ├─ 1.1.1 Initiation
│  ├─ 1.1.2 Planning
│  ├─ 1.1.3 Execution
│  └─ 1.1.4 Closure
├─ 1.2 Requirements
│  ├─ 1.2.1 Gather requirements
│  ├─ 1.2.2 Document requirements
│  └─ 1.2.3 Requirements approval
├─ 1.3 Design
│  ├─ 1.3.1 UI/UX design
│  ├─ 1.3.2 Technical architecture
│  └─ 1.3.3 Database design
├─ 1.4 Development
│  ├─ 1.4.1 Frontend development
│  ├─ 1.4.2 Backend development
│  └─ 1.4.3 Database implementation
├─ 1.5 Testing
│  ├─ 1.5.1 Unit testing
│  ├─ 1.5.2 Integration testing
│  └─ 1.5.3 UAT
└─ 1.6 Deployment
   ├─ 1.6.1 Production setup
   ├─ 1.6.2 Data migration
   └─ 1.6.3 Go-live
```

---

## Critical Path Method (CPM)

### Purpose
Identify longest sequence of activities (critical path).

### Process
1. List all activities
2. Determine dependencies
3. Create network diagram
4. Estimate durations
5. Calculate early start/finish
6. Calculate late start/finish
7. Calculate float/slack
8. Identify critical path

### Example Calculation
```
Activity | Duration | Predecessors | ES | EF | LS | LF | Float
---------|----------|--------------|----|----|----|----|------
A        | 3        | -            | 0  | 3  | 0  | 3  | 0 (Critical)
B        | 2        | A            | 3  | 5  | 3  | 5  | 0 (Critical)
C        | 4        | A            | 3  | 7  | 5  | 9  | 2
D        | 3        | B            | 5  | 8  | 5  | 8  | 0 (Critical)
E        | 2        | C,D          | 8  | 10 | 8  | 10 | 0 (Critical)

Critical Path: A → B → D → E (Total Duration: 10 days)
```

### Managing Critical Path
- Focus monitoring on critical activities
- Allocate best resources to critical path
- Crash activities if needed (add resources)
- Fast-track by overlapping activities

---

## Change Control Process

### Purpose
Manage approved changes systematically.

### Change Control Board (CCB)
**Members:**
- Project sponsor
- Project manager
- Key stakeholders
- Technical leads

**Responsibilities:**
- Review change requests
- Approve/reject/defer changes
- Assess impact on scope, schedule, cost
- Prioritize changes

### Process Flow
```
1. Change Request Submitted
   ↓
2. Log in Change Log
   ↓
3. Initial Assessment (PM)
   - Impact on scope?
   - Impact on schedule?
   - Impact on budget?
   - Impact on quality?
   ↓
4. Detailed Analysis
   - Technical feasibility
   - Resource requirements
   - Risk assessment
   ↓
5. CCB Review
   ↓
6. Decision: Approve / Reject / Defer
   ↓
7. If Approved:
   - Update project plan
   - Update baselines
   - Communicate to stakeholders
   - Implement change
   ↓
8. Verify Change Implementation
   ↓
9. Close Change Request
```

### Change Request Template
```markdown
# CHANGE REQUEST

CR Number: CR-001
Date Submitted: [Date]
Submitted By: [Name]

## Description
[Detailed description of change]

## Justification
[Why is this change needed?]

## Impact Analysis
- Scope: [Impact]
- Schedule: [+/- X days]
- Budget: [+/- $X]
- Quality: [Impact]
- Risk: [New risks introduced]

## Priority: High / Medium / Low

## Recommendation: Approve / Reject / Defer

## CCB Decision
Decision: [Approved/Rejected/Deferred]
Date: [Date]
Notes: [Rationale]

Approved By: _______________ Date: _______
```

---

## Lessons Learned Process

### Purpose
Capture knowledge for future projects.

### When to Capture
- End of each phase
- After major milestones
- Project closure
- When issues occur

### Categories
1. **What Went Well**
   - Successful practices
   - Effective tools/techniques
   - Strong team dynamics

2. **What Could Be Improved**
   - Challenges faced
   - Mistakes made
   - Process gaps

3. **Recommendations**
   - Specific actions for future
   - Process improvements
   - Tool/template updates

### Lessons Learned Template
```markdown
# LESSONS LEARNED

Project: [Name]
Date: [Date]
Phase: [Initiation/Planning/Execution/Closing]

## What Went Well
1. [Success 1]: [Description and why it worked]
2. [Success 2]: [Description and why it worked]

## What Could Be Improved
1. [Challenge 1]: [Description and impact]
   - Root Cause: [Why did this happen?]
   - Recommendation: [What to do differently]

2. [Challenge 2]: [Description and impact]
   - Root Cause: [Why did this happen?]
   - Recommendation: [What to do differently]

## Key Takeaways
1. [Key learning 1]
2. [Key learning 2]
3. [Key learning 3]

## Action Items for Future Projects
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]
```

---

## Requirements Management

### Purpose
Elicit, analyze, document, and manage stakeholder needs throughout project lifecycle.

### Requirements Categories

**1. Business Requirements**
- High-level needs of the organization
- Business objectives and goals
- Success criteria

**Example:**
- Increase customer retention by 20%
- Reduce operational costs by $500K annually
- Enter new market segment

**2. Stakeholder Requirements**
- Needs of specific stakeholder groups
- User expectations
- Operational constraints

**Example:**
- Sales team needs mobile access to CRM
- Finance needs automated reporting
- IT needs single sign-on integration

**3. Solution Requirements**

**a) Functional Requirements (what system must do)**
- User interactions
- Business processes
- Calculations and validations

**Example:**
- FR-001: System shall allow users to reset password via email
- FR-002: System shall validate credit card numbers using Luhn algorithm
- FR-003: System shall send confirmation email within 5 seconds of order

**b) Non-Functional Requirements (how system performs)**
- Performance (speed, capacity)
- Security (authentication, authorization)
- Usability (ease of use)
- Reliability (uptime, recovery)
- Scalability (growth capacity)

**Example:**
- NFR-001: System shall support 10,000 concurrent users
- NFR-002: System shall have 99.9% uptime
- NFR-003: Page load time shall be <2 seconds
- NFR-004: System shall encrypt all data at rest using AES-256

**4. Transition Requirements**
- Data migration needs
- Training requirements
- Deployment constraints

### Requirements Elicitation Techniques

**1. Interviews**
- One-on-one with stakeholders
- Structured or unstructured
- Document responses

**Prep:**
```
1. Research stakeholder role
2. Prepare open-ended questions
3. Schedule 30-60 minutes
4. Record (with permission)
5. Send thank-you + summary
```

**Sample Questions:**
- What problem are you trying to solve?
- What does success look like?
- What are your biggest concerns?
- What systems do you currently use?
- What would make your job easier?

**2. Focus Groups**
- Group of 6-12 stakeholders
- Facilitated discussion
- Brainstorming session

**Best Practices:**
- Homogeneous groups (similar roles)
- Neutral facilitator
- Ground rules (respect, no judgment)
- Time-boxed (90-120 minutes)

**3. Workshops**
- Collaborative session
- Requirements prioritization
- Consensus building

**Agenda:**
```
1. Introduction (10 min)
2. Context setting (15 min)
3. Brainstorming (30 min)
4. Grouping/categorizing (20 min)
5. Prioritization (30 min)
6. Next steps (15 min)
```

**4. Observation**
- Watch users perform tasks
- Identify pain points
- Understand workflow

**Process:**
- Get permission
- Minimal interference
- Take detailed notes
- Ask clarifying questions
- Document as-is process

**5. Surveys/Questionnaires**
- Reach large audience
- Quantitative data
- Statistical analysis

**Design Tips:**
- Keep short (<10 minutes)
- Mix question types
- Include open-ended questions
- Pilot test first

**6. Document Analysis**
- Review existing docs
- Business process diagrams
- Current system specs
- Regulatory requirements

**Sources:**
- Business plans
- Process manuals
- System documentation
- Compliance documents
- Competitor analysis

**7. Prototyping**
- Build mockup/wireframe
- Get feedback iteratively
- Refine requirements

**Types:**
- Throwaway (exploratory)
- Evolutionary (iterative refinement)
- Paper (low-fi sketches)
- Digital (interactive)

### Requirements Analysis

**1. Categorization**
```
Group by:
- Functional vs Non-Functional
- Must-Have vs Nice-to-Have (MoSCoW)
- User role
- Module/feature area
```

**2. Prioritization (MoSCoW Method)**
```
Must Have:  Essential for launch (60% of requirements)
Should Have: Important but not critical (20%)
Could Have:  Nice to have if time/budget (20%)
Won't Have:  Out of scope for this release (0%)
```

**3. Conflict Resolution**
```
When requirements conflict:
1. Identify stakeholders involved
2. Understand underlying needs
3. Facilitate discussion
4. Seek win-win solution
5. Escalate if needed
6. Document decision rationale
```

**4. Feasibility Analysis**
```
Assess:
- Technical feasibility (can we build it?)
- Economic feasibility (cost vs benefit?)
- Operational feasibility (can we support it?)
- Schedule feasibility (enough time?)
- Legal feasibility (compliant?)
```

### Business Requirements Document (BRD)

**Structure:**
```markdown
# BUSINESS REQUIREMENTS DOCUMENT

## 1. Executive Summary
[1-2 paragraphs: Project overview, objectives, expected benefits]

## 2. Business Objectives
**Primary Objective:**
[Main business goal]

**Secondary Objectives:**
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

**Success Criteria:**
- [Measurable criterion 1]
- [Measurable criterion 2]

## 3. Scope

**In Scope:**
- [Feature/capability 1]
- [Feature/capability 2]

**Out of Scope:**
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

**Future Considerations:**
- [Possible future enhancement]

## 4. Stakeholders

| Name | Role | Department | Interest | Influence |
|------|------|------------|----------|----------|
| [Name] | Sponsor | Executive | High | High |
| [Name] | End User | Sales | High | Medium |

## 5. Current State

**As-Is Process:**
[Describe current workflow/system]

**Pain Points:**
1. [Problem 1 - Impact]
2. [Problem 2 - Impact]

**Current Systems:**
- [System 1 - Purpose]
- [System 2 - Purpose]

## 6. Proposed Solution

**To-Be Process:**
[Describe future workflow/system]

**High-Level Features:**
1. [Feature 1 - Description]
2. [Feature 2 - Description]

**Benefits:**
- [Quantified benefit 1]
- [Quantified benefit 2]

## 7. Functional Requirements

**FR-001: User Authentication**
- Description: System shall allow users to login with email/password
- Priority: Must Have
- Acceptance Criteria:
  - [ ] User can login with valid credentials
  - [ ] Invalid credentials show error message
  - [ ] Account locks after 5 failed attempts

**FR-002: Password Reset**
- Description: System shall allow users to reset forgotten password
- Priority: Must Have
- Acceptance Criteria:
  - [ ] User receives reset email within 5 minutes
  - [ ] Reset link expires after 24 hours
  - [ ] New password meets complexity requirements

## 8. Non-Functional Requirements

**Performance:**
- NFR-001: System shall respond to 95% of requests within 2 seconds
- NFR-002: System shall support 5,000 concurrent users

**Security:**
- NFR-003: All passwords must be hashed using bcrypt
- NFR-004: All data transmission must use TLS 1.3

**Usability:**
- NFR-005: Interface shall be accessible (WCAG 2.1 Level AA)
- NFR-006: Users shall complete checkout in <3 clicks

**Reliability:**
- NFR-007: System uptime shall be 99.9%
- NFR-008: System shall recover from failure within 5 minutes

## 9. Assumptions & Constraints

**Assumptions:**
- Users have internet access
- Users have modern web browsers
- API endpoints will remain stable

**Constraints:**
- Budget: $500K
- Timeline: 6 months
- Team size: 5 developers
- Must integrate with legacy system

## 10. Dependencies

**Internal:**
- Requires completion of Project X
- Depends on IT infrastructure upgrade

**External:**
- Third-party API availability
- Vendor contract renewal

## 11. Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High | High | [Strategy] |
| [Risk 2] | Med | Low | [Strategy] |

## 12. Acceptance Criteria

**Project accepted when:**
- [ ] All Must Have requirements implemented
- [ ] UAT completed successfully
- [ ] Performance targets met
- [ ] Security audit passed
- [ ] User training completed
- [ ] Documentation delivered

## 13. Approval

Business Owner: ______________ Date: ______
Project Sponsor: _____________ Date: ______
Project Manager: _____________ Date: ______
```

### Requirements Traceability Matrix (RTM)

**Purpose:** Track requirements from elicitation through delivery.

**Template:**
```
| Req ID | Description | Source | Priority | Design Spec | Test Case | Status |
|--------|-------------|--------|----------|-------------|-----------|--------|
| FR-001 | User login | Stakeholder A | Must | DS-001 | TC-001 | Done |
| FR-002 | Password reset | Stakeholder B | Must | DS-002 | TC-002 | In Progress |
| NFR-001 | <2s response | SLA | Must | DS-003 | TC-003 | Not Started |
```

**Benefits:**
- Ensures all requirements are addressed
- Tracks requirement status
- Links requirements to design and testing
- Supports impact analysis for changes
- Provides audit trail

**Usage:**
```
1. Create at requirements phase
2. Update throughout project
3. Review weekly in status meetings
4. Use for change impact analysis
5. Verify 100% coverage before launch
```

### Requirements Validation

**Techniques:**

**1. Formal Reviews**
- Walkthrough with stakeholders
- Line-by-line review
- Sign-off required

**2. Prototyping**
- Build mockup
- Get user feedback
- Refine requirements

**3. Test Case Development**
- Write test cases from requirements
- If can't write test, requirement unclear
- Verify testability

**4. Acceptance Criteria**
- Each requirement has clear criteria
- Measurable and verifiable
- Given-When-Then format

**Example:**
```
Given: User is on login page
When: User enters valid credentials
Then: User is redirected to dashboard
```

### Requirements Change Management

**Process:**
```
1. Change Request Submitted
   ↓
2. Impact Analysis
   - Which requirements affected?
   - Impact on design/code/tests?
   - Schedule impact?
   - Cost impact?
   ↓
3. Stakeholder Review
   ↓
4. Approve/Reject
   ↓
5. Update BRD, RTM
   ↓
6. Communicate to team
   ↓
7. Update artifacts (design, code, tests)
```

**Version Control:**
- Document version numbers
- Track change history
- Maintain audit trail
- Archive old versions

**Example:**
```
BRD v1.0 - Initial (Jan 1)
BRD v1.1 - Added FR-015 (Jan 15)
BRD v2.0 - Scope change approved (Feb 1)
```

### Common Pitfalls

**1. Vague Requirements**
❌ "System should be fast"
✅ "System shall respond to 95% of requests within 2 seconds"

**2. Gold Plating**
❌ Adding features not requested
✅ Stick to documented requirements

**3. Scope Creep**
❌ "While you're at it, can you also..."
✅ Formal change control process

**4. Skipping Validation**
❌ Assuming requirements are correct
✅ Review with stakeholders regularly

**5. Poor Documentation**
❌ Verbal agreements only
✅ Written, approved BRD

**6. Ignoring Non-Functional Requirements**
❌ Focus only on features
✅ Document performance, security, usability

### Best Practices

**1. Start with "Why"**
- Understand business need
- Don't jump to solution
- Question assumptions

**2. Involve Right Stakeholders**
- End users (day-to-day users)
- Business owners (decision makers)
- Technical team (implementers)
- Compliance (regulatory)

**3. Use Visual Models**
- Process flows
- Wireframes
- Use case diagrams
- Data models

**4. Write Clear Requirements**
- Each requirement is unique
- Specific and measurable
- Testable and verifiable
- Traceable to source

**5. Prioritize Ruthlessly**
- Not everything is Must Have
- Use MoSCoW method
- Validate with stakeholders
- Re-prioritize regularly

**6. Maintain Traceability**
- Link requirements to source
- Link to design/code/tests
- Track status
- Update regularly

**7. Expect Change**
- Requirements will evolve
- Have change process
- Assess impact before accepting
- Communicate changes

---

## Best Practices Summary

### Project Charter
- Get executive sponsor approval
- Keep it high-level (1-2 pages)
- Include measurable objectives
- Clearly state authority levels
- Document assumptions and constraints

### Scope Management
- Involve stakeholders in requirements
- Use requirements traceability matrix
- Create detailed WBS
- Define acceptance criteria clearly
- Implement formal change control

### Schedule Management
- Identify all dependencies
- Use realistic estimates
- Build in buffers
- Monitor critical path
- Update schedule weekly

### Cost Management
- Use bottom-up estimating
- Include contingency reserve
- Track earned value metrics
- Forecast regularly
- Control scope creep

### Quality Management
- Define quality standards upfront
- Plan for quality reviews
- Conduct regular audits
- Implement lessons learned
- Focus on prevention over inspection

---

**Next Steps:**
- Read agile-scrum.md for Agile methodologies
- Read waterfall-predictive.md for traditional approach
- Read risk-stakeholder.md for stakeholder management
