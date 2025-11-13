# Risk & Stakeholder Management Reference

Comprehensive guide for identifying, assessing, and managing project risks and stakeholders.

## Table of Contents
1. [Risk Management](#risk-management)
2. [Risk Identification](#risk-identification)
3. [Risk Assessment](#risk-assessment)
4. [Risk Response](#risk-response)
5. [Stakeholder Management](#stakeholder-management)
6. [Stakeholder Engagement](#stakeholder-engagement)

---

## Risk Management

### Risk Management Process
```
1. Plan Risk Management
2. Identify Risks
3. Perform Qualitative Analysis (Probability × Impact)
4. Perform Quantitative Analysis ($$$ impact)
5. Plan Risk Responses
6. Implement Responses
7. Monitor Risks
```

### Risk Register Template
```markdown
| Risk ID | Description | Category | Probability | Impact | Score | Owner | Response | Status |
|---------|-------------|----------|-------------|--------|-------|-------|----------|--------|
| R001 | Key developer leaves | Resource | Medium (50%) | High (8) | 4.0 | PM | Mitigate | Open |
| R002 | API integration delay | Technical | High (70%) | Medium (5) | 3.5 | Tech Lead | Transfer | Open |
```

---

## Risk Identification

### Identification Techniques

**1. Brainstorming**
- Gather team and stakeholders
- Free-flowing idea generation
- No criticism during generation
- Categorize and prioritize after

**2. SWOT Analysis**
```
Strengths → Opportunities (leverage)
Weaknesses → Threats (mitigate)

SWOT for Project:
Strengths: Experienced team, proven technology
Weaknesses: Tight timeline, limited budget
Opportunities: Market demand, executive support
Threats: Competitor launch, resource turnover
```

**3. Checklist Analysis**
- Use historical risk data
- Industry-specific risks
- Organizational risk library

**4. Expert Interviews**
- SMEs in relevant domains
- Lessons learned from past projects
- External consultants

**5. Risk Breakdown Structure (RBS)**
```
Project Risks
├─ Technical
│  ├─ Technology maturity
│  ├─ Integration complexity
│  └─ Performance issues
├─ External
│  ├─ Vendor dependency
│  ├─ Regulatory changes
│  └─ Market conditions
├─ Organizational
│  ├─ Resource availability
│  ├─ Funding issues
│  └─ Priority changes
└─ Project Management
   ├─ Scope creep
   ├─ Schedule delays
   └─ Communication gaps
```

### Common Project Risks

**Technical Risks:**
- New/unproven technology
- Integration challenges
- Performance/scalability issues
- Technical debt
- Security vulnerabilities

**Schedule Risks:**
- Optimistic estimates
- Resource unavailability
- Dependency delays
- Scope creep
- Rework due to quality issues

**Cost Risks:**
- Inaccurate estimates
- Scope changes
- Resource rate increases
- Exchange rate fluctuations
- Unplanned expenses

**Resource Risks:**
- Key person dependency
- Skill gaps
- Turnover
- Competing priorities
- Unavailability

**External Risks:**
- Vendor delays/failure
- Regulatory changes
- Market shifts
- Natural disasters
- Geopolitical events

---

## Risk Assessment

### Qualitative Risk Analysis

**Probability Scale:**
```
Very High: 80-100% (0.9)
High:      60-80%  (0.7)
Medium:    40-60%  (0.5)
Low:       20-40%  (0.3)
Very Low:  0-20%   (0.1)
```

**Impact Scale (1-10):**
```
Catastrophic: 9-10 (Project failure)
High:         7-8  (Major objectives threatened)
Medium:       4-6  (Important objectives affected)
Low:          2-3  (Minor impact)
Negligible:   1    (Minimal impact)
```

**Risk Score Calculation:**
```
Risk Score = Probability × Impact

Example:
Risk: Key developer leaves
Probability: Medium (0.5 or 50%)
Impact: High (8/10)
Risk Score: 0.5 × 8 = 4.0

Risk Priority:
Critical: 6.0+ (Red)
High: 4.0-5.9 (Orange)
Medium: 2.0-3.9 (Yellow)
Low: <2.0 (Green)
```

### Probability-Impact Matrix
```
Impact →    Low  Med  High VHigh
          ┌────┬────┬────┬────┐
VHigh 0.9 │ 🟡 │ 🟠 │ 🔴 │ 🔴 │
          ├────┼────┼────┼────┤
High 0.7  │ 🟢 │ 🟡 │ 🟠 │ 🔴 │
          ├────┼────┼────┼────┤
Med 0.5   │ 🟢 │ 🟡 │ 🟡 │ 🟠 │
          ├────┼────┼────┼────┤
Low 0.3   │ 🟢 │ 🟢 │ 🟡 │ 🟡 │
          └────┴────┴────┴────┘
```

### Quantitative Risk Analysis

**Expected Monetary Value (EMV):**
```
EMV = Probability × Financial Impact

Example:
Risk: Server failure during peak
Probability: 20%
Financial Impact: $100,000 lost revenue
EMV: 0.2 × $100,000 = $20,000

Use EMV for:
- Cost-benefit analysis
- Contingency reserve calculation
- Risk prioritization
```

**Monte Carlo Simulation:**
- Simulate thousands of scenarios
- Calculate probability distribution
- Determine confidence levels
- Common for schedule and cost risks

---

## Risk Response

### Response Strategies

**For Threats (Negative Risks):**

**1. Avoid**
- Eliminate the risk entirely
- Change project plan
- Remove risky feature
- Use proven technology instead

**Example:** Risk of using new framework
**Response:** Use mature, proven framework instead

**2. Transfer**
- Shift risk to third party
- Insurance
- Outsourcing
- Fixed-price contracts

**Example:** Risk of infrastructure failure
**Response:** Use cloud provider with SLA

**3. Mitigate**
- Reduce probability or impact
- Preventive actions
- Most common response

**Example:** Risk of key person leaving
**Response:** 
- Cross-training
- Documentation
- Succession planning
- Retention bonus

**4. Accept**
- Acknowledge risk but take no action
- Active: Set aside contingency
- Passive: Deal with it if it occurs

**Example:** Risk of minor delay
**Response:** Accept - buffer in schedule covers it

**For Opportunities (Positive Risks):**

**1. Exploit**
- Ensure opportunity happens
- Assign best resources
- Fast-track schedule

**2. Share**
- Partner with others
- Joint venture
- Strategic alliance

**3. Enhance**
- Increase probability or impact
- Add resources
- Improve conditions

**4. Accept**
- Take advantage if it occurs
- No proactive action

### Risk Response Plan Template
```markdown
## Risk Response Plan

**Risk ID:** R001
**Description:** Key developer may leave during critical phase
**Category:** Resource Risk
**Probability:** Medium (50%)
**Impact:** High (8)
**Risk Score:** 4.0 (High Priority)

### Response Strategy: Mitigate

**Preventive Actions:**
1. Implement knowledge sharing sessions (weekly)
2. Document critical code and architecture
3. Cross-train 2 backup developers
4. Offer retention bonus for project duration

**Contingency Plan (if risk occurs):**
1. Activate backup developer immediately
2. Prioritize critical path items
3. Consider consultant for 2-3 weeks
4. Adjust timeline if needed

**Owner:** Project Manager
**Budget:** $10,000 (contingency)
**Trigger:** Developer gives notice
**Status:** Active monitoring

**Monitoring:**
- Weekly check-ins with developer
- Track satisfaction scores
- Watch for signs (resume updates, recruiter calls)
```

### Contingency Reserve

**Calculation Methods:**

**1. Percentage of Base Estimate**
```
Low risk project: 5-10%
Medium risk: 10-20%
High risk: 20-40%

Example:
Project Budget: $500,000
Risk Level: Medium (15%)
Contingency: $500,000 × 0.15 = $75,000
Total Budget: $575,000
```

**2. Expected Monetary Value**
```
Sum of all risk EMVs

Risk A: 0.3 × $50,000 = $15,000
Risk B: 0.5 × $30,000 = $15,000
Risk C: 0.2 × $40,000 = $8,000
Total EMV = $38,000
Contingency Reserve = $38,000
```

---

## Stakeholder Management

### Stakeholder Identification

**Stakeholder Categories:**
- **Primary:** Directly affected (users, team, sponsors)
- **Secondary:** Indirectly affected (operations, support)
- **Internal:** Within organization
- **External:** Outside organization (vendors, regulators, public)

### Power/Interest Grid
```
       High Power
           │
  Manage  │  Keep
 Closely  │ Satisfied
───────────┼───────────
           │
 Monitor   │  Keep
           │ Informed
           │
       Low Interest → High Interest
```

**Quadrant Strategies:**

**High Power, High Interest (Manage Closely)**
- Project sponsor
- Executive leadership
- Key business owners
- *Strategy:* Frequent communication, involve in decisions

**High Power, Low Interest (Keep Satisfied)**
- Senior management
- Department heads
- *Strategy:* Regular updates, meet their needs

**Low Power, High Interest (Keep Informed)**
- End users
- Project team
- *Strategy:* Adequate information, show consideration

**Low Power, Low Interest (Monitor)**
- Peripheral stakeholders
- *Strategy:* General communications, minimal effort

### Stakeholder Register
```markdown
| Stakeholder | Role | Power | Interest | Influence | Strategy | Communication |
|-------------|------|-------|----------|-----------|----------|---------------|
| John Smith | Sponsor | High | High | High | Manage Closely | Weekly 1:1 |
| Jane Doe | User Rep | Low | High | Medium | Keep Informed | Bi-weekly demo |
| Bob Jones | IT Ops | High | Low | Low | Keep Satisfied | Monthly email |
```

---

## Stakeholder Engagement

### Communication Planning

**Communication Matrix:**
```markdown
| Stakeholder | Information Needed | Frequency | Method | Owner |
|-------------|-------------------|-----------|---------|-------|
| Sponsor | Project status, risks, budget | Weekly | Meeting | PM |
| Steering Committee | Executive summary | Monthly | Report + Meeting | PM |
| Team | Task assignments, blockers | Daily | Standup | SM |
| Users | Progress, training | Bi-weekly | Demo | PO |
```

### Managing Difficult Stakeholders

**Resistant Stakeholder:**
```
Symptoms: Passive resistance, delays, non-cooperation

Actions:
1. Understand their concerns
2. Involve them in decisions
3. Show WIIFM (What's In It For Me)
4. Build relationship
5. Escalate if needed
```

**Conflicting Stakeholders:**
```
Symptoms: Contradictory requirements, competing priorities

Actions:
1. Facilitate joint meeting
2. Find common ground
3. Clarify priorities
4. Document trade-offs
5. Executive decision if no consensus
```

**Absent Stakeholder:**
```
Symptoms: Doesn't attend meetings, slow responses

Actions:
1. Understand why (too busy, not interested?)
2. Adjust communication approach
3. Delegate to representative
4. Escalate impact to their manager
5. Document attempts to engage
```

### Conflict Resolution

**5 Conflict Resolution Styles:**

**1. Competing (Win-Lose)**
- Assert your position
- Use when: Quick decision needed, you're right, emergency

**2. Collaborating (Win-Win)**
- Work together for mutual benefit
- Use when: Both parties' concerns are important, time available

**3. Compromising (Partial Win-Win)**
- Meet in the middle
- Use when: Quick solution needed, both parties equal power

**4. Avoiding (Lose-Lose)**
- Postpone or withdraw
- Use when: Issue trivial, cooling-off needed, no chance of winning

**5. Accommodating (Lose-Win)**
- Give in to other party
- Use when: Maintaining relationship more important, you're wrong

**Preferred Order:** Collaborating > Compromising > Competing > Accommodating > Avoiding

---

## Risk Monitoring

### Risk Review Cadence

**Weekly (PM + Team):**
- Review top 10 risks
- Check triggers
- Update probabilities
- New risks identified

**Monthly (Steering Committee):**
- Top 5 risks reported
- Major changes highlighted
- Resource needs for mitigation
- Contingency status

**At Milestones:**
- Comprehensive risk review
- Update risk register
- Reassess all risks
- Identify new phase risks

### Risk Metrics

**Key Metrics:**
```
1. Number of Open Risks: Track trend
2. Average Risk Score: Should decrease over time
3. Risks Realized: How many occurred?
4. Mitigation Effectiveness: Did responses work?
5. Contingency Usage: Tracking reserve burn
```

### Risk Report Template
```markdown
# Risk Report - [Month Year]

## Summary
- Total Risks: 25 (15 open, 10 closed)
- Critical Risks: 3
- High Risks: 7
- Risks Realized This Month: 2

## Top 5 Risks

### 1. Integration Delay (CRITICAL)
- **Score:** 7.2 (was 6.0)
- **Trend:** ↑ Increasing
- **Status:** Vendor 2 weeks behind
- **Action:** Weekly vendor calls, backup plan ready

### 2. Resource Turnover (HIGH)
- **Score:** 4.0 (was 4.0)
- **Trend:** → Stable
- **Status:** Monitoring, retention plan in place
- **Action:** Monthly satisfaction check-ins

## Risks Realized
- R015: Server capacity issue - Mitigated successfully
- R022: Requirements change - Managed via change control

## New Risks This Month
- R026: Security audit finding (Medium, 3.0)
- R027: Third-party API deprecation (Low, 1.5)

## Contingency Status
- Allocated: $100,000
- Used: $25,000
- Remaining: $75,000
```

---

**Best Practices:**
- Update risk register weekly
- Involve team in risk identification
- Don't ignore low-probability high-impact risks
- Communicate risks transparently
- Review risk responses regularly
- Learn from risks that materialized
- Engage stakeholders appropriately
- Document everything

**Next Steps:**
- Read pmp-framework.md for overall PM processes
- Read metrics-reporting.md for tracking KPIs
- Use templates/ for risk register and stakeholder analysis
