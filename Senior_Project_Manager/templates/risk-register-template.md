# Risk Register

**Project:** [Project Name]  
**Project Manager:** [PM Name]  
**Date Created:** [YYYY-MM-DD]  
**Last Updated:** [YYYY-MM-DD]  
**Version:** [X.X]

---

## Risk Register Overview

**Purpose:** Track, assess, and manage project risks throughout the project lifecycle.

**Risk Review Frequency:** [e.g., Weekly with core team, Monthly with steering committee]

**Escalation Threshold:** Risks with score ≥ [X] (e.g., 15) escalate to [Steering Committee/Sponsor]

---

## Risk Summary Dashboard

| Risk Level | Count | Total Exposure |
|------------|-------|----------------|
| 🔴 **Critical** (Score 20-25) | [X] | $[Amount] |
| 🟠 **High** (Score 15-19) | [X] | $[Amount] |
| 🟡 **Medium** (Score 8-14) | [X] | $[Amount] |
| 🟢 **Low** (Score 1-7) | [X] | $[Amount] |
| **TOTAL** | **[X]** | **$[Total]** |

**Active Risks:** [X]  
**Mitigated Risks:** [Y]  
**Closed Risks:** [Z]

---

## Risk Register Table

| ID | Risk Description | Category | Probability | Impact | Score | Risk Level | Response Strategy | Mitigation Plan | Owner | Status | Last Updated |
|----|------------------|----------|-------------|--------|-------|------------|-------------------|-----------------|-------|--------|--------------|
| R-001 | [Concise description of risk event] | [Category] | [1-5] | [1-5] | [P×I] | [Level] | [Strategy] | [Mitigation actions] | [Name] | [Status] | [Date] |
| R-002 | Key vendor delays delivery by 3+ months | Vendor | 3 | 5 | 15 | High | Mitigate | Early contract penalties, backup vendor identified | [Name] | Open | 2025-11-01 |
| R-003 | Data migration accuracy < 95% | Technical | 4 | 4 | 16 | High | Mitigate | Run pilot migration, automated validation scripts | [Name] | Open | 2025-11-05 |
| R-004 | User adoption < 80% after go-live | Change Mgmt | 3 | 4 | 12 | Medium | Mitigate | Exec sponsorship, training program, champions network | [Name] | Open | 2025-11-10 |
| R-005 | Budget overrun > 15% | Financial | 2 | 5 | 10 | Medium | Accept | 10% contingency reserve, monthly burn rate review | PM | Open | 2025-11-12 |
| R-006 | Integration with ERP fails | Technical | 2 | 4 | 8 | Medium | Mitigate | Early POC, dedicated integration specialist | [Name] | Mitigated | 2025-10-15 |

---

## Risk Categories

[Define categories relevant to your project]

| Category | Description | Examples |
|----------|-------------|----------|
| **Technical** | Technology, architecture, integration risks | System compatibility, performance, scalability |
| **Vendor/3rd Party** | External dependencies, supplier risks | Vendor delays, quality issues, contract disputes |
| **Resource** | Team availability, skills, capacity | Key person departure, insufficient expertise |
| **Financial** | Budget, funding, cost risks | Budget cuts, cost overruns, ROI not achieved |
| **Schedule** | Timeline, milestone, deadline risks | Dependencies, estimation errors, scope creep |
| **Scope** | Requirements, deliverables, change risks | Unclear requirements, gold-plating, scope creep |
| **Change Management** | Adoption, training, culture risks | Resistance to change, low adoption, training gaps |
| **Compliance/Legal** | Regulatory, legal, policy risks | Regulatory changes, contract issues, IP disputes |
| **External** | Market, competition, political risks | Market shifts, competitor moves, political changes |
| **Operational** | BAU operations, support, maintenance | Lack of support resources, operational readiness |

---

## Probability Definitions

| Level | Description | Likelihood | Numeric Score |
|-------|-------------|------------|---------------|
| **Very Low** | Highly unlikely to occur | <10% chance | 1 |
| **Low** | Unlikely but possible | 10-30% chance | 2 |
| **Medium** | Moderately likely | 30-50% chance | 3 |
| **High** | Likely to occur | 50-70% chance | 4 |
| **Very High** | Almost certain to occur | >70% chance | 5 |

---

## Impact Definitions

| Level | Schedule Impact | Budget Impact | Quality Impact | Scope Impact | Numeric Score |
|-------|----------------|---------------|----------------|--------------|---------------|
| **Very Low** | <1 week delay | <$10K increase | Minor quality issue | <5% scope impact | 1 |
| **Low** | 1-2 weeks delay | $10-50K increase | Quality degradation | 5-10% scope impact | 2 |
| **Medium** | 2-4 weeks delay | $50-100K increase | Significant quality issues | 10-20% scope impact | 3 |
| **High** | 1-2 months delay | $100-250K increase | Major quality problems | 20-40% scope impact | 4 |
| **Very High** | >2 months delay | >$250K increase | Critical failure risk | >40% scope impact | 5 |

**Note:** Adjust thresholds based on project size and budget.

---

## Risk Scoring Matrix

| | **Very Low (1)** | **Low (2)** | **Medium (3)** | **High (4)** | **Very High (5)** |
|---|---|---|---|---|---|
| **Very High (5)** | 5 - Low | 10 - Med | 15 - High | 20 - Critical | 25 - Critical |
| **High (4)** | 4 - Low | 8 - Med | 12 - Med | 16 - High | 20 - Critical |
| **Medium (3)** | 3 - Low | 6 - Low | 9 - Med | 12 - Med | 15 - High |
| **Low (2)** | 2 - Low | 4 - Low | 6 - Low | 8 - Med | 10 - Med |
| **Very Low (1)** | 1 - Low | 2 - Low | 3 - Low | 4 - Low | 5 - Low |

**Risk Score = Probability × Impact**

**Risk Levels:**
- **Critical:** Score 20-25 (Red)
- **High:** Score 15-19 (Orange)
- **Medium:** Score 8-14 (Yellow)
- **Low:** Score 1-7 (Green)

---

## Response Strategies

### Strategy Selection Guide

| Strategy | When to Use | Ownership | Example Actions |
|----------|-------------|-----------|-----------------|
| **Avoid** | Risk unacceptable, eliminate cause | Project team | Change approach, remove feature, use proven technology |
| **Transfer** | Risk manageable by 3rd party | External party | Insurance, contracts, outsourcing, warranties |
| **Mitigate** | Reduce probability or impact | Project team | Prototyping, testing, redundancy, training |
| **Accept** | Low impact or cost of mitigation > risk | Project team/Sponsor | Contingency reserve, workarounds, monitoring |

### Detailed Strategy Descriptions

**1. AVOID**
- **Goal:** Eliminate the risk entirely
- **Actions:**
  - Change project scope to remove risky element
  - Use proven technology instead of cutting-edge
  - Redesign to avoid risky approach
- **Example:** Switch from custom-built to COTS solution

**2. TRANSFER**
- **Goal:** Shift risk impact to third party
- **Actions:**
  - Purchase insurance
  - Contractual penalties/SLAs with vendors
  - Outsource risky work to specialist
- **Example:** Fixed-price contract with vendor includes penalties for delays

**3. MITIGATE**
- **Goal:** Reduce probability or impact
- **Actions:**
  - Prototyping/POC to validate approach
  - Additional testing/quality gates
  - Training/skill development
  - Redundancy/backup systems
- **Example:** Run pilot data migration with 10% of records

**4. ACCEPT**
- **Goal:** Acknowledge risk, prepare contingency
- **Actions:**
  - Document risk and rationale
  - Set aside contingency budget
  - Monitor risk indicators
  - Prepare workaround plan
- **Example:** Accept 5% chance of minor delay, have 2-week buffer

---

## Detailed Risk Entries

### Risk ID: R-001
**Risk Title:** [Descriptive title]

**Description:**  
[Detailed description of the risk event, including what could happen and under what conditions]

**Category:** [Category from list]

**Probability:** [1-5] - [Description]  
**Impact:** [1-5] - [Description]  
**Risk Score:** [P × I]  
**Risk Level:** [Critical/High/Medium/Low]

**Triggers/Indicators:**
- [Early warning sign 1]
- [Early warning sign 2]
- [Early warning sign 3]

**Root Causes:**
- [Underlying cause 1]
- [Underlying cause 2]

**Response Strategy:** [Avoid/Transfer/Mitigate/Accept]

**Mitigation Plan:**
1. [Action 1 with timeline]
2. [Action 2 with timeline]
3. [Action 3 with timeline]

**Contingency Plan (if risk occurs):**
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Owner:** [Name]  
**Status:** [Open/Mitigated/Closed/Occurred]  
**Last Review Date:** [YYYY-MM-DD]  
**Target Closure Date:** [YYYY-MM-DD]

**Cost Impact (if realized):** $[Amount]  
**Schedule Impact (if realized):** [X weeks/months]

**Notes/History:**
- [Date]: [Update note]
- [Date]: [Update note]

---

### Risk ID: R-002
**Risk Title:** [Descriptive title]

[Repeat structure above for each risk]

---

## Risk Review Schedule

### Weekly Risk Reviews
**Participants:** Project Manager, Core Team  
**Focus:** Active risks, new risks, status updates  
**Duration:** 30 minutes

### Monthly Risk Reviews
**Participants:** PM, Sponsor, Steering Committee  
**Focus:** High/critical risks, trend analysis, escalations  
**Duration:** 60 minutes

### Risk Review Agenda
1. Review risk summary dashboard
2. Discuss each High/Critical risk status
3. Identify new risks
4. Update mitigation actions
5. Decide on risk responses
6. Update risk scores based on new information
7. Escalate risks exceeding threshold

---

## Escalation Criteria

**Immediate Escalation (to Sponsor):**
- Risk score ≥ 20 (Critical)
- Risk impact > 20% of project budget
- Risk threatens project viability
- Risk requires executive decision

**Steering Committee Escalation:**
- Multiple high risks (3+ with score ≥15)
- Total risk exposure > 30% of budget
- Inability to mitigate within project authority
- Strategic risks affecting other projects

**Escalation Process:**
1. Document risk with full assessment
2. Prepare recommendation with options
3. Schedule meeting with decision-maker
4. Present risk, impact, and recommended response
5. Obtain decision and document
6. Execute approved response strategy

---

## Risk Mitigation Tracking

| Risk ID | Mitigation Action | Owner | Due Date | Status | % Complete | Notes |
|---------|-------------------|-------|----------|--------|------------|-------|
| R-002 | Contract penalty clause | PM | 2025-11-15 | Complete | 100% | Signed |
| R-002 | Identify backup vendor | PM | 2025-11-20 | In Progress | 60% | 2 candidates shortlisted |
| R-003 | Run pilot migration | Tech Lead | 2025-11-25 | Not Started | 0% | Waiting for test environment |
| R-004 | Launch champions program | Change Mgr | 2025-12-01 | In Progress | 30% | 5/15 champions recruited |

---

## Closed/Resolved Risks

[Archive of risks that have been resolved or are no longer relevant]

| ID | Risk Description | Closure Date | Resolution | Lessons Learned |
|----|------------------|--------------|------------|-----------------|
| R-010 | [Description] | [Date] | [How it was resolved] | [Key takeaways] |
| R-015 | [Description] | [Date] | [How it was resolved] | [Key takeaways] |

---

## Lessons Learned & Best Practices

**From This Project:**
- [Lesson 1: What worked well in risk management]
- [Lesson 2: What could be improved]
- [Lesson 3: Unexpected risks encountered]

**Best Practices Applied:**
- [Practice 1: e.g., Early risk workshops with stakeholders]
- [Practice 2: e.g., Weekly risk pulse checks in standups]
- [Practice 3: e.g., Risk-adjusted contingency allocation]

---

## Risk Reporting

### Weekly Status Report (Risk Section)
- Top 3 risks by score
- New risks identified this week
- Risks closed this week
- Overall risk trend (increasing/decreasing)

### Monthly Executive Report
- Risk summary dashboard
- Critical/high risks with mitigation status
- Risk trend analysis
- Escalations and decisions needed

---

## Appendix: Risk Assessment Worksheet

Use this template when assessing new risks:

**Risk Title:** ___________________________

**What could go wrong?**  
[Description]

**What would cause this?**  
[Root causes]

**How would we know it's about to happen?**  
[Triggers/indicators]

**What would be the consequences?**  
[Impact on schedule, budget, quality, scope]

**Probability Assessment (1-5):** ___  
**Impact Assessment (1-5):** ___  
**Risk Score:** ___  
**Risk Level:** ___

**Response Strategy:** [Avoid / Transfer / Mitigate / Accept]

**What actions will we take?**  
1. [Action]
2. [Action]
3. [Action]

**Who will own this risk?** ___________________________

**When do we need to act?** ___________________________

---

**Document Control:**
- **Version:** [X.X]
- **Last Updated:** [YYYY-MM-DD]
- **Next Review:** [YYYY-MM-DD]
- **Owner:** [Project Manager Name]
- **Storage:** [Location/URL]
