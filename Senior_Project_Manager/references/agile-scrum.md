# Agile & Scrum Reference Guide

Comprehensive guide for Agile methodologies with deep focus on Scrum framework, ceremonies, and practices.

## Table of Contents
1. [Agile Manifesto & Principles](#agile-manifesto--principles)
2. [Scrum Framework](#scrum-framework)
3. [Scrum Roles](#scrum-roles)
4. [Scrum Ceremonies](#scrum-ceremonies)
5. [Sprint Retrospective Deep Dive](#sprint-retrospective-deep-dive)
6. [Estimation Techniques](#estimation-techniques)
7. [T-Shirt Sizing](#t-shirt-sizing)
8. [Product Backlog Management](#product-backlog-management)
9. [Velocity & Metrics](#velocity--metrics)
10. [Common Anti-Patterns](#common-anti-patterns)

---

## Agile Manifesto & Principles

### The Four Values
1. **Individuals and interactions** over processes and tools
2. **Working software** over comprehensive documentation
3. **Customer collaboration** over contract negotiation
4. **Responding to change** over following a plan

*While there is value in the items on the right, we value the items on the left more.*

### 12 Agile Principles
1. Customer satisfaction through early and continuous delivery
2. Welcome changing requirements, even late in development
3. Deliver working software frequently (weeks not months)
4. Business people and developers work together daily
5. Build projects around motivated individuals
6. Face-to-face conversation is most effective
7. Working software is primary measure of progress
8. Sustainable development (maintain constant pace)
9. Continuous attention to technical excellence
10. Simplicity (maximize work not done)
11. Self-organizing teams produce best architectures
12. Regular reflection and adjustment

---

## Scrum Framework

### Overview
Scrum is a lightweight framework for developing, delivering, and sustaining complex products.

### Scrum Pillars
1. **Transparency**: Everyone knows what's happening
2. **Inspection**: Regular check-ins on progress
3. **Adaptation**: Adjust when things deviate

### Scrum Values
- **Commitment**: Team commits to achieving goals
- **Courage**: Team has courage to do the right thing
- **Focus**: Team focuses on sprint work
- **Openness**: Team is open about challenges
- **Respect**: Team members respect each other

### Scrum Flow
```
Product Backlog
     ↓
Sprint Planning → Sprint Backlog
     ↓
Daily Scrum (daily check-in)
     ↓
Sprint (1-4 weeks)
     ↓
Sprint Review (demo to stakeholders)
     ↓
Sprint Retrospective (team improvement)
     ↓
Increment (potentially shippable product)
     ↓
Repeat
```

---

## Scrum Roles

### 1. Product Owner (PO)

**Responsibilities:**
- Define product vision
- Manage product backlog
- Prioritize features
- Accept/reject work
- Maximize product value

**Daily Activities:**
- Refine backlog items
- Answer team questions
- Engage with stakeholders
- Make trade-off decisions
- Review completed work

**Success Criteria:**
- Clear product vision communicated
- Backlog is prioritized and refined
- Available to team daily
- Stakeholders satisfied
- ROI is positive

**Anti-patterns:**
- Absent or unavailable
- Changes priorities mid-sprint
- Micromanages team
- Doesn't accept completed work
- Unclear about requirements

### 2. Scrum Master (SM)

**Responsibilities:**
- Facilitate scrum events
- Remove impediments
- Coach team on Agile practices
- Shield team from distractions
- Promote self-organization

**Daily Activities:**
- Facilitate Daily Scrum
- Track and remove blockers
- Coach team members
- Improve team processes
- Communicate with stakeholders

**Success Criteria:**
- Team is productive and improving
- Impediments are removed quickly
- Ceremonies are effective
- Team is self-organizing
- Continuous improvement happening

**Anti-patterns:**
- Acts as project manager
- Solves problems for team
- Doesn't address impediments
- Dominates meetings
- Ignores team dysfunction

### 3. Development Team

**Characteristics:**
- 3-9 members (ideal: 5-7)
- Cross-functional
- Self-organizing
- No sub-teams
- Collectively responsible

**Responsibilities:**
- Deliver potentially shippable increment
- Estimate work
- Self-organize tasks
- Maintain technical excellence
- Collaborate daily

**Success Criteria:**
- Sprint goals met consistently
- Quality is high
- Team is improving
- Sustainable pace maintained
- Innovation happening

**Anti-patterns:**
- Waiting for assignments
- Siloed work (not collaborating)
- Poor technical practices
- Over-committing
- Not helping teammates

---

## Scrum Ceremonies

### 1. Sprint Planning

**Duration:** 2-4 hours for 2-week sprint (4-8 hours for 4-week)

**Attendees:** Product Owner, Scrum Master, Development Team

**Purpose:** Plan work for upcoming sprint

**Agenda:**
```
Part 1: What can be done? (50%)
- Product Owner presents top priority items
- Team asks clarifying questions
- Team forecasts what can be completed
- Team crafts sprint goal

Part 2: How will it be done? (50%)
- Team breaks down selected items
- Team creates task breakdown
- Team estimates tasks (hours)
- Team commits to sprint goal
```

**Outputs:**
- Sprint goal (one-sentence objective)
- Sprint backlog (selected stories + tasks)
- Team commitment

**Best Practices:**
- Have refined backlog ready (top 2 sprints)
- Use historical velocity for planning
- Leave buffer for unknowns (20%)
- Entire team participates
- Focus on sprint goal, not just stories

**Example Sprint Goal:**
```
Good: "Enable users to search and filter products by category and price"
Bad: "Complete 5 user stories"

Good: "Fix top 10 customer-reported bugs and improve app stability"
Bad: "Do bug fixes"
```

### 2. Daily Scrum (Daily Standup)

**Duration:** 15 minutes (strictly timeboxed)

**Attendees:** Development Team (required), Scrum Master (optional), PO (optional)

**Purpose:** Synchronize activities and plan next 24 hours

**Format:** Each team member answers:
1. What did I complete yesterday?
2. What will I work on today?
3. Are there any impediments?

**Alternative Formats:**
- Walk the board (discuss each story)
- Focus on sprint goal progress
- Discuss what's blocking sprint goal

**Best Practices:**
- Same time, same place
- Stand up (keeps it short)
- Focus on coordination, not status reporting
- Take detailed discussions offline
- Update task board during or after
- Scrum Master tracks impediments

**Anti-patterns:**
- Goes over 15 minutes
- Turns into problem-solving session
- Becomes status report to manager
- Team members don't listen to each other
- People arrive late
- Held in front of computer (distractions)

### 3. Sprint Review (Demo)

**Duration:** 1-2 hours for 2-week sprint

**Attendees:** Scrum Team + Stakeholders

**Purpose:** Inspect increment and adapt product backlog

**Agenda:**
```
1. Product Owner explains what was planned vs. done (5 min)
2. Development Team demonstrates working software (40 min)
   - Show completed stories only
   - Live demo (not PowerPoint)
   - Get feedback from stakeholders
3. Product Owner discusses backlog status (10 min)
4. Collaborative discussion on next steps (30 min)
5. Review timeline, budget, capabilities (5 min)
```

**Best Practices:**
- Demo in production-like environment
- Let team members demo their work
- Encourage stakeholder questions
- Capture feedback for backlog
- Celebrate achievements
- Be honest about what's not done

**Anti-patterns:**
- No stakeholders attend
- Demo doesn't work (not tested)
- Show incomplete work
- Team doesn't participate
- Too much preparation (over-polished)
- Defensive when receiving feedback

### 4. Sprint Retrospective

**Duration:** 1.5 hours for 2-week sprint

**Attendees:** Development Team + Scrum Master (PO optional)

**Purpose:** Inspect team and create improvement plan

**See dedicated section below for deep dive**

---

## Sprint Retrospective Deep Dive

### Purpose & Importance
Retrospective is the team's dedicated time to improve. It's the most important ceremony for long-term success.

**Retrospective Prime Directive:**
> "Regardless of what we discover, we understand and truly believe that everyone did the best job they could, given what they knew at the time, their skills and abilities, the resources available, and the situation at hand."

### Retrospective Formats

#### Format 1: Mad/Sad/Glad

**Setup:** Create three columns

**Process:**
1. **Silent Generation (10 min)**: Each person writes sticky notes
   - Mad: What frustrated you?
   - Sad: What disappointed you?
   - Glad: What made you happy?

2. **Grouping (10 min)**: Team groups similar items

3. **Voting (5 min)**: Each person gets 3-5 votes

4. **Discussion (45 min)**: Discuss top voted items

5. **Actions (20 min)**: Define 2-3 concrete actions

**Example:**
```
MAD:
- Too many production bugs
- Meetings interrupt deep work
- Unclear requirements

SAD:
- Didn't complete sprint goal
- Team member left
- Technical debt growing

GLAD:
- Good collaboration on Feature X
- New test framework working well
- Stakeholders loved the demo
```

#### Format 2: Start/Stop/Continue

**Process:**
1. What should we **START** doing?
2. What should we **STOP** doing?
3. What should we **CONTINUE** doing?

**Example:**
```
START:
- Pair programming on complex features
- Writing integration tests
- Refining backlog 1 sprint ahead

STOP:
- Working overtime
- Skipping code reviews
- Accepting vague user stories

CONTINUE:
- Daily standups at 9:30 AM
- Knowledge sharing sessions
- Using automated deployment
```

#### Format 3: 4Ls (Liked, Learned, Lacked, Longed For)

**Process:**
1. **Liked**: What did we enjoy?
2. **Learned**: What did we discover?
3. **Lacked**: What was missing?
4. **Longed For**: What did we wish for?

**Example:**
```
LIKED:
- New team member ramped up quickly
- Clear acceptance criteria this sprint
- Stable production environment

LEARNED:
- Redis caching improved performance by 10x
- Stakeholders prefer bi-weekly demos
- Automated tests catch 80% of bugs

LACKED:
- Design resources (caused delays)
- Clear API documentation
- Staging environment parity

LONGED FOR:
- More time for learning/R&D
- Better developer tools
- Co-located team space
```

#### Format 4: Timeline Retrospective

**Setup:** Draw timeline of sprint on whiteboard

**Process:**
1. Mark major events on timeline
2. Each person adds sticky notes with emotions
3. Discuss patterns and themes
4. Identify what to improve

**Good for:** Sprints with significant events or challenges

#### Format 5: Sailboat Retrospective

**Metaphor:**
- **Sailboat** = Team
- **Wind** = What helps us go faster
- **Anchor** = What slows us down
- **Rocks** = Risks ahead
- **Island** = Goal/Vision

**Process:**
1. Draw sailboat, wind, anchor, rocks, island
2. Team adds sticky notes to each area
3. Discuss and prioritize
4. Define actions

### Retrospective Structure (90 min)

**1. Set the Stage (5 min)**
- Welcome everyone
- Remind of prime directive
- Set working agreements
- Check-in activity (e.g., one word to describe sprint)

**2. Gather Data (15 min)**
- Timeline of events
- Metrics review (velocity, bugs, etc.)
- Silent writing of observations
- Everyone participates equally

**3. Generate Insights (30 min)**
- Group related items
- Vote on priorities
- Dig into root causes
- Use "5 Whys" technique
- Look for patterns

**Example 5 Whys:**
```
Problem: Too many production bugs

Why? → We didn't test thoroughly
Why? → We ran out of time
Why? → We over-committed in planning
Why? → We didn't account for bug fixes
Why? → We haven't established a bug budget

Root Cause: Need to allocate 20% of capacity for bug fixes
```

**4. Decide What to Do (30 min)**
- Brainstorm solutions
- Select 2-3 actionable improvements
- Make them SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- Assign owners
- Define success criteria

**Good Action Items:**
```
✓ "John will research pair programming tools and propose one by next sprint"
✓ "Team will allocate 20% of capacity for tech debt starting next sprint"
✓ "Sarah will create API documentation template this week"

✗ "We should communicate better" (too vague)
✗ "Try to improve quality" (no owner, not measurable)
✗ "Stop having bugs" (unrealistic)
```

**5. Close the Retrospective (10 min)**
- Summarize action items
- Appreciate team members
- Assign action owners
- Schedule follow-up
- Quick feedback on retro itself

### Tracking Improvements

**Action Item Template:**
```markdown
## Retrospective Action Items - Sprint X

**Action 1:** [What to do]
- Owner: [Name]
- Due: [Date]
- Success Criteria: [How we know it's done]
- Status: Not Started / In Progress / Done

**Action 2:** [What to do]
- Owner: [Name]
- Due: [Date]
- Success Criteria: [How we know it's done]
- Status: Not Started / In Progress / Done
```

**Review in Next Retro:**
- Were actions completed?
- Did they have desired effect?
- What did we learn?
- Carry forward incomplete actions?

### Facilitation Tips

**For Scrum Master:**
1. Rotate formats (keeps it fresh)
2. Be neutral facilitator (don't dominate)
3. Encourage quiet voices
4. Manage time strictly
5. Focus on team, not individuals
6. Make it safe to speak honestly
7. Follow up on action items
8. Celebrate improvements

**Red Flags:**
- Same people always talking
- Blaming individuals
- No action items defined
- Actions never completed
- Retro becoming routine/boring
- Avoiding difficult topics
- Manager dominates discussion

---

## Estimation Techniques

### Why Estimate?
- Forecast delivery dates
- Prioritize features
- Identify risks early
- Plan capacity
- Measure velocity

### Estimation Methods

#### 1. T-Shirt Sizing (High-Level)

**Purpose:** Quick, rough estimation for roadmap planning

**Sizes:** XS, S, M, L, XL, 2XL, 3XL

**When to Use:**
- Early roadmap planning
- Feature comparison
- Initial backlog
- When precision isn't needed

**Process:**
1. Present feature/epic
2. Team discusses complexity and risk
3. Quick vote using T-shirt sizes
4. Discuss if no consensus
5. Re-vote until agreement

**Advantages:**
- Fast and intuitive
- Non-technical stakeholders understand
- Good for long-term planning
- Reduces estimation pressure

**Disadvantages:**
- Not precise
- Harder to track velocity
- Needs conversion to hours/points later

#### 2. Story Points (Detailed)

**Purpose:** Relative estimation for sprint planning

**Scale:** Fibonacci sequence (1, 2, 3, 5, 8, 13, 21, 40, 100)

**What Story Points Represent:**
- Complexity
- Effort
- Uncertainty
- Risk

**Not:**
- Time (not hours)
- Individual capacity
- Calendar days

**Reference Stories:**
Create baseline examples:
```
1 point: Fix typo in UI text
2 points: Add validation to form field
3 points: Create new API endpoint (CRUD)
5 points: Integrate third-party payment gateway
8 points: Implement search functionality
13 points: Build user authentication system
21 points: Create reporting dashboard
```

**Best Practices:**
- Estimate as a team
- Use relative sizing
- Don't over-think
- Re-calibrate baselines
- Don't convert to hours

#### 3. Planning Poker

**Purpose:** Team-based consensus estimation

**Materials:**
- Planning poker cards (Fibonacci)
- User stories
- Product Owner

**Process:**
```
1. Product Owner reads story
2. Team asks clarifying questions
3. Each team member selects card (private)
4. All reveal simultaneously
5. Discuss outliers (highest and lowest explain)
6. Re-vote until consensus (2-3 rounds max)
7. Record estimate
```

**Advantages:**
- Prevents anchoring bias
- Everyone participates
- Uncovers assumptions
- Builds shared understanding
- Fun and engaging

**Tips:**
- Keep discussions time-boxed (5 min per story)
- High variance = story too unclear
- Split stories >13 points
- Don't average estimates (seek consensus)

#### 4. Ideal Days

**Purpose:** Estimate in "perfect working days"

**Process:**
- How many days if no interruptions?
- No meetings, no distractions
- All tools and info available

**Conversion:**
```
1 ideal day ≈ 2-3 calendar days
(Accounts for meetings, distractions, etc.)
```

---

## T-Shirt Sizing

### T-Shirt Sizing Matrix

**Risk vs Complexity Framework:**

```
         │  Low    │ Medium │  High  │Very High│
Risk     │Complexity│Complexity│Complexity│Complexity│
─────────┼─────────┼────────┼────────┼─────────┤
Very High│   L     │   XL   │  2XL   │  3XL    │
         │         │        │        │         │
High     │   M     │   L    │   XL   │  2XL    │
         │         │        │        │         │
Medium   │   S     │   M    │   L    │   XL    │
         │         │        │        │         │
Low      │   XS    │   S    │   M    │   L     │
─────────┴─────────┴────────┴────────┴─────────┘
```

### Sizing Guidelines

**XS (Extra Small)**
- Low risk, low complexity
- **Time:** 2-4 hours
- **Example:** Fix typo, update text, change color
- **Story Points:** 1

**S (Small)**
- Low-medium risk/complexity
- **Time:** 4-8 hours (half day to 1 day)
- **Example:** Add form validation, update single API endpoint
- **Story Points:** 2

**M (Medium)**
- Medium risk/complexity
- **Time:** 1-2 days
- **Example:** Create new page with basic CRUD, implement simple feature
- **Story Points:** 3-5

**L (Large)**
- Medium-high risk/complexity
- **Time:** 2-3 days
- **Example:** Integrate third-party API, build complex form
- **Story Points:** 5-8

**XL (Extra Large)**
- High risk/complexity
- **Time:** 3-5 days
- **Example:** Implement authentication system, create reporting module
- **Story Points:** 8-13

**2XL (2X Large)**
- Very high risk/complexity
- **Time:** 1-2 weeks
- **Example:** Build payment processing, create admin dashboard
- **Story Points:** 13-21
- **⚠️ Should be split into smaller stories**

**3XL (3X Large)**
- Extremely high risk/complexity
- **Time:** 2+ weeks
- **Example:** Complete system redesign, major architecture change
- **Story Points:** 21+
- **❌ Must be split - too large for sprint**

### When to Use T-Shirt Sizing

**Use T-Shirt Sizing When:**
- ✅ Roadmap planning (quarterly/annual)
- ✅ Epic sizing
- ✅ Quick feature comparison
- ✅ Communicating with executives
- ✅ Initial backlog estimation

**Use Story Points When:**
- ✅ Sprint planning
- ✅ Velocity tracking
- ✅ Detailed estimation
- ✅ Capacity planning
- ✅ Team forecasting

### Conversion Table

```
T-Shirt │ Story Points │ Ideal Days │ Real Days │ Real Hours
────────┼──────────────┼────────────┼───────────┼───────────
XS      │      1       │    0.25    │   0.5-1   │    2-4
S       │      2       │    0.5     │   1-2     │    4-8
M       │     3-5      │     1      │   2-3     │   8-16
L       │     5-8      │    1.5     │   3-5     │   16-32
XL      │    8-13      │     2      │   5-8     │   32-64
2XL     │   13-21      │    2-3     │  8-15     │  64-120
3XL     │     21+      │     4+     │   15+     │   120+
```

**Note:** These are guidelines, not strict rules. Teams should calibrate based on their context.

### T-Shirt Sizing Workshop

**Agenda (2 hours):**

**1. Align on Definitions (30 min)**
- Review T-shirt sizes
- Discuss complexity vs risk
- Create reference examples
- Agree on criteria

**2. Size Epics/Features (60 min)**
- Present each item (5 min)
- Silent sizing (1 min)
- Reveal sizes
- Discuss differences
- Converge on size
- Repeat

**3. Prioritize (20 min)**
- Group by T-shirt size
- Discuss dependencies
- Identify quick wins (small, high value)
- Sequence work

**4. Roadmap Planning (10 min)**
- Map to quarters/releases
- Account for capacity
- Identify risks
- Next steps

**Output:**
- Sized backlog
- Rough roadmap
- Shared understanding

---

## Product Backlog Management

### Backlog Refinement

**Purpose:** Prepare upcoming work for sprint planning

**Frequency:** Mid-sprint or continuous

**Duration:** 5-10% of sprint capacity

**Activities:**
- Break down large stories
- Add acceptance criteria
- Estimate stories
- Remove outdated items
- Clarify requirements

**Ready Definition:**
A story is ready when it has:
- [ ] Clear user story format
- [ ] Acceptance criteria defined
- [ ] Estimated (story points or T-shirt)
- [ ] Dependencies identified
- [ ] Design/mockups attached (if needed)
- [ ] Technical approach agreed

**Example Ready Story:**
```
As a customer
I want to reset my password via email
So that I can regain access to my account

Acceptance Criteria:
- Given I'm on login page, when I click "Forgot Password", then I see email input form
- Given I enter valid email, when I submit, then I receive reset link via email
- Given I click reset link, when I create new password, then I can login with new password
- Password must be 8+ characters with 1 number and 1 special character

Story Points: 5
Design: [Link to mockup]
Dependencies: Email service configured
```

### Backlog Prioritization

**Prioritization Frameworks:**

**1. MoSCoW Method**
- **Must Have**: Critical for release
- **Should Have**: Important but not critical
- **Could Have**: Nice to have
- **Won't Have**: Not this release

**2. RICE Score**
```
RICE = (Reach × Impact × Confidence) / Effort

Reach: How many users affected?
Impact: How much impact? (3=High, 2=Medium, 1=Low)
Confidence: How confident? (100%=High, 80%=Medium, 50%=Low)
Effort: Person-months of work

Example:
Feature A: (1000 × 3 × 80%) / 2 = 1200
Feature B: (500 × 2 × 100%) / 1 = 1000
Priority: Feature A > Feature B
```

**3. Value vs Effort**
```
       High Value
           │
 Do First  │  Do Next
───────────┼───────────
 Do Last   │  Avoid
           │
       Low Effort → High Effort
```

---

## Velocity & Metrics

### Velocity

**Definition:** Amount of work completed per sprint (in story points)

**Calculation:**
```
Velocity = Sum of story points for completed stories in sprint

Sprint 1: 23 points
Sprint 2: 21 points
Sprint 3: 25 points
Average Velocity: (23 + 21 + 25) / 3 = 23 points
```

**Using Velocity:**
- Forecast delivery dates
- Plan sprint capacity
- Identify trends
- Measure team productivity

**Important Notes:**
- Velocity is team-specific (don't compare teams)
- Takes 3-5 sprints to stabilize
- Focus on trend, not absolute number
- Can decrease (it's okay - quality matters)

### Burndown Chart

**Sprint Burndown:**
- X-axis: Days in sprint
- Y-axis: Remaining work (story points)
- Ideal line: Linear decrease
- Actual line: Real progress

**Healthy Patterns:**
```
Points
  ^
  │\
  │ \  Ideal
  │  \
  │   \___  Actual (slightly above/below is normal)
  │       \
  └─────────> Days
```

**Unhealthy Patterns:**
```
Flat Line (no progress):
  │────────
  │        \___
  └─────────────>

Late Rush (all at end):
  │────────────
  │            │
  │            └──
  └───────────────>
```

### Cumulative Flow Diagram

Shows work in different states over time:
- Backlog
- In Progress
- Done

**Healthy CFD:**
- Parallel bands (steady flow)
- Increasing "Done" line
- Small "In Progress" band

**Unhealthy CFD:**
- Widening "In Progress" (bottleneck)
- Flat "Done" (no completions)
- Growing "Backlog" (scope creep)

---

## Common Anti-Patterns

### Sprint Anti-Patterns

**1. Incomplete Sprints**
- **Problem:** Stories not done by sprint end
- **Root Cause:** Over-commitment, poor estimates, blockers
- **Solution:** Use velocity, add buffer, improve refinement

**2. Sprint Goal Ignored**
- **Problem:** Team works on random stories
- **Root Cause:** No clear goal, PO changing priorities
- **Solution:** Define clear sprint goal, commit to it

**3. Carrying Over Work**
- **Problem:** Incomplete stories roll to next sprint
- **Root Cause:** Stories too large, poor planning
- **Solution:** Split stories, finish before starting new

### Team Anti-Patterns

**1. Not Self-Organizing**
- **Problem:** Waiting for assignments
- **Root Cause:** Command-control culture, weak SM
- **Solution:** Empower team, coach self-organization

**2. Specialists, Not Generalizing**
- **Problem:** "That's not my job" mentality
- **Root Cause:** Siloed skills, lack of collaboration
- **Solution:** Pair programming, knowledge sharing, T-shaped skills

**3. No Technical Excellence**
- **Problem:** Growing technical debt, quality issues
- **Root Cause:** Pressure to deliver, no time for quality
- **Solution:** Definition of Done includes quality, allocate tech debt time

### Ceremony Anti-Patterns

**1. Status Report Daily Scrum**
- **Problem:** Team reports to manager, not each other
- **Root Cause:** Management attendance, lack of self-organization
- **Solution:** Focus on coordination, managers observe only

**2. Demo of Incomplete Work**
- **Problem:** Showing unfinished stories
- **Root Cause:** Over-commitment, poor planning
- **Solution:** Only demo "Done" work per Definition of Done

**3. Action-less Retrospective**
- **Problem:** Talk but no improvements
- **Root Cause:** No follow-up, too many actions
- **Solution:** 2-3 actions max, track completion

---

**Best Practices Summary:**
- Keep sprints time-boxed and consistent
- Maintain sustainable pace
- Focus on working software
- Collaborate continuously
- Reflect and improve regularly
- Respect Definition of Done
- Empower the team
- Protect sprint commitment

**Next Steps:**
- Read waterfall-predictive.md for traditional PM
- Read hybrid-approach.md for combining methodologies
- Read metrics-reporting.md for advanced metrics
