# Requirements Engineering - Complete Guide

## Overview

Requirements engineering is the systematic process of eliciting, documenting, analyzing, and validating stakeholder needs to define what a system should do. Poor requirements are the #1 cause of project failures—unclear scope leads to rework, budget overruns, and stakeholder dissatisfaction.

---

## 1. Requirements Elicitation Techniques

### 1.1 Stakeholder Interviews

**When to Use:** Early discovery phase, understanding business context

**Structure:**
```
Preparation (1 hour):
- Research stakeholder background
- Prepare open-ended questions
- Define interview goals

Interview (60-90 minutes):
- Warm-up (5 min): Build rapport
- Context questions (15 min): Understand current state
- Problem exploration (30 min): Dig into pain points
- Solution ideas (20 min): Explore desired outcomes
- Wrap-up (10 min): Clarify next steps

Follow-up (30 minutes):
- Document findings
- Identify gaps for next interview
```

**Good Questions:**
- "Walk me through a typical day in your role"
- "What's the biggest pain point in your current workflow?"
- "If you had a magic wand, what would you change?"
- "What does success look like for this project?"

**Bad Questions:**
- "Do you want feature X?" (leading)
- "Would you use this if we built it?" (hypothetical)

### 1.2 Workshops & Brainstorming

**When to Use:** Aligning multiple stakeholders, generating ideas

**Effective Workshop Structure:**
```
1. Set the Stage (15 min)
   - Introduce objectives
   - Establish ground rules
   - Warm-up activity

2. Divergent Thinking (45 min)
   - Brainstorm ideas (no judgment)
   - Use sticky notes / virtual boards
   - Encourage wild ideas

3. Convergent Thinking (30 min)
   - Group similar ideas
   - Vote on priorities
   - Identify conflicts

4. Action Items (15 min)
   - Assign owners
   - Set deadlines
   - Document decisions
```

**Facilitation Tips:**
- Time-box activities (use timers)
- "Yes, and..." not "Yes, but..."
- Capture visual diagrams (workflows, journey maps)

### 1.3 User Observation (Contextual Inquiry)

**When to Use:** Understanding actual (vs stated) user behavior

**Process:**
1. Observe user in natural environment
2. Take notes without interrupting
3. Ask "why" questions after observation
4. Identify workarounds (signals of unmet needs)

**Example:**
```
Observed: User copies data from System A to Excel, 
          then uploads to System B
          
Question: "Why do you use Excel as intermediate step?"

Answer: "System A export isn't compatible with System B format,
         and I need to add calculated fields"

Insight: Integration opportunity + custom field requirements
```

### 1.4 Surveys & Questionnaires

**When to Use:** Gathering data from large user base, validating assumptions

**Survey Design Best Practices:**
- Keep it short (<10 minutes to complete)
- Mix question types: multiple choice, rating scales, open-ended
- Avoid double-barreled questions ("Is the app fast and easy?")
- Use logic branching (skip irrelevant questions)

**Example:**
```
Poor: "Do you like the app?"
Better: "On a scale of 1-5, how satisfied are you with [specific feature]?"

Poor: "What features do you want?"
Better: "Rank these features by importance: [List of 5 options]"
```

---

## 2. Writing Effective Requirements

### 2.1 Functional Requirements

**Template:**
```
FR-XXX: [Requirement Name]

The system shall [action] [object] [condition].

Example:
FR-001: User Authentication
The system shall authenticate users via email and password,
and lock accounts after 5 failed login attempts within 15 minutes.
```

**SMART Criteria:**
- **Specific:** No ambiguity
- **Measurable:** Testable acceptance criteria
- **Achievable:** Technically feasible
- **Relevant:** Ties to business goal
- **Testable:** Can verify if implemented correctly

**Good vs Bad Examples:**
```
❌ Bad: "System should be fast"
✅ Good: "System shall return search results within 2 seconds 
         for 95% of queries under normal load (1000 concurrent users)"

❌ Bad: "System should have good security"
✅ Good: "System shall encrypt all data at rest using AES-256 
         and in transit using TLS 1.3"
```

### 2.2 Non-Functional Requirements (NFRs)

**Categories:**

**Performance:**
```
- Response time: P50 < 100ms, P95 < 500ms, P99 < 1000ms
- Throughput: 10,000 requests per second
- Resource usage: Max 70% CPU under normal load
```

**Scalability:**
```
- Horizontal scaling: Support 100,000 concurrent users
- Database: Handle 1 billion records
- Storage: 10 TB data, growing at 100 GB/month
```

**Availability:**
```
- Uptime: 99.95% (21.6 min downtime/month)
- Disaster recovery: RPO < 1 hour, RTO < 4 hours
```

**Security:**
```
- Authentication: OAuth 2.0 with MFA
- Authorization: Role-Based Access Control (RBAC)
- Data: Encryption at rest (AES-256), in transit (TLS 1.3)
- Compliance: GDPR, SOC 2 Type II
```

**Usability:**
```
- Accessibility: WCAG 2.1 Level AA
- Learning curve: New users complete core tasks within 5 minutes
- Mobile responsive: Support iOS 14+, Android 10+
```

### 2.3 User Stories

**Format:**
```
As a [user role]
I want [action/feature]
So that [benefit/value]
```

**Example:**
```
As a warehouse manager
I want to scan barcodes to update inventory
So that I can reduce data entry errors and save time

Acceptance Criteria:
- [ ] Barcode scan updates inventory in real-time
- [ ] System displays confirmation within 1 second
- [ ] Invalid barcodes show error message
- [ ] Supports EAN-13 and Code 128 formats
- [ ] Works offline (syncs when reconnected)
```

**Story Splitting (When Too Large):**
```
Epic: "User can manage orders"

Split into:
- User can create order
- User can edit order
- User can cancel order
- User can view order history
```

**Estimation (Story Points):**
- 1 point: Few hours, trivial
- 3 points: 1-2 days, straightforward
- 5 points: 3-5 days, some complexity
- 8 points: 1 week, significant complexity
- 13+ points: Too large, split story

### 2.4 Use Cases

**Template:**
```
UC-XXX: [Use Case Name]

Actor: [Primary actor]
Preconditions: [What must be true before use case starts]
Trigger: [Event that initiates use case]

Main Flow:
1. Actor [action]
2. System [response]
3. Actor [action]
4. System [response]

Alternative Flows:
2a. If [condition], then [alternative path]

Exception Flows:
E1. If [error], system [recovery action]

Postconditions: [System state after completion]
```

**Example:**
```
UC-001: Process Payment

Actor: Customer
Preconditions: Cart has items, customer logged in
Trigger: Customer clicks "Checkout"

Main Flow:
1. Customer enters payment information
2. System validates card details
3. System processes payment via Stripe
4. System displays order confirmation
5. System sends confirmation email

Alternative Flows:
3a. If insufficient funds, system displays error and 
    prompts for different payment method

Exception Flows:
E1. If payment gateway down, system queues order and
    notifies customer of processing delay

Postconditions: Order status = "Paid", inventory updated
```

---

## 3. Requirements Analysis & Prioritization

### 3.1 MoSCoW Method

**Must Have:** Non-negotiable, system fails without it
- Example: User authentication, payment processing

**Should Have:** Important but not critical
- Example: Email notifications, search filters

**Could Have:** Nice to have, low impact if missing
- Example: Dark mode, export to PDF

**Won't Have (This Time):** Explicitly out of scope
- Example: Mobile app (focus on web first)

### 3.2 Kano Model

**Basic Needs:** Expected features (dissatisfaction if missing)
- Example: Website loads correctly, forms work

**Performance Needs:** More is better (linear satisfaction)
- Example: Page load speed, search relevance

**Excitement Needs:** Unexpected delights
- Example: AI-powered suggestions, beautiful animations

### 3.3 RICE Score (Prioritization Framework)

```
RICE Score = (Reach × Impact × Confidence) / Effort

Reach: How many users affected per time period?
Impact: How much does it move key metrics? (3=massive, 2=high, 1=medium, 0.5=low)
Confidence: How certain are we? (100%=high, 80%=medium, 50%=low)
Effort: Person-months of work

Example:
Feature: In-app chat support
Reach: 1000 users/month
Impact: 2 (high - reduces support tickets 30%)
Confidence: 80%
Effort: 2 person-months

RICE = (1000 × 2 × 0.8) / 2 = 800
```

---

## 4. Requirements Validation

### 4.1 Review Checklist

**Completeness:**
- [ ] All stakeholders interviewed
- [ ] Edge cases documented
- [ ] Error scenarios covered
- [ ] Dependencies identified

**Consistency:**
- [ ] No conflicting requirements
- [ ] Terminology used consistently
- [ ] Priorities aligned across stakeholders

**Feasibility:**
- [ ] Technical feasibility validated with engineering
- [ ] Budget constraints considered
- [ ] Timeline realistic

**Testability:**
- [ ] Each requirement has acceptance criteria
- [ ] Success metrics defined
- [ ] Test scenarios documented

### 4.2 Prototype & Validation

**Low-Fidelity:**
- Paper sketches, wireframes
- Use for early feedback (cheap to change)

**High-Fidelity:**
- Interactive Figma/Sketch prototypes
- Use for usability testing before development

**Validation Questions:**
- "Does this solve your problem?"
- "Would you use this daily?"
- "What's confusing or unclear?"
- "What's missing?"

---

## 5. Requirements Traceability

### 5.1 Traceability Matrix

Links requirements to business objectives, design, implementation, and tests.

| Req ID | Requirement | Business Goal | Design | Code | Tests |
|--------|-------------|---------------|--------|------|-------|
| FR-001 | User login | Secure access | LoginScreen.tsx | auth.service.js | login.test.js |
| FR-002 | Password reset | User retention | ResetPassword.tsx | reset.service.js | reset.test.js |

**Benefits:**
- Impact analysis (what breaks if we change X?)
- Coverage gaps (untested requirements)
- Audit trail (why did we build this?)

---

## 6. Common Pitfalls & How to Avoid

### 6.1 Gold Plating

**Problem:** Adding features not requested by stakeholders

**Solution:**
- Always tie features to business goals
- Ask "What problem does this solve?"
- Use MVP approach (ship minimum viable, iterate)

### 6.2 Scope Creep

**Problem:** Requirements keep expanding during development

**Solution:**
- Formal change request process
- Impact analysis (cost, timeline) for each change
- Say "yes, we'll add to backlog for v2"

### 6.3 Vague Requirements

**Problem:** "System should be user-friendly"

**Solution:**
- Convert to measurable criteria
- "New users complete signup in < 3 minutes (90% success rate)"

### 6.4 Ignoring Non-Functional Requirements

**Problem:** Focus only on features, ignore performance/security

**Solution:**
- Ask explicitly about NFRs in every interview
- "How many users? How fast? How secure?"

---

## 7. Tools & Templates

**Requirements Management:**
- Jira (user stories, epics, roadmap)
- Azure DevOps (requirements, traceability)
- Confluence (documentation)

**Diagramming:**
- Miro (collaborative whiteboarding)
- Lucidchart (flowcharts, use case diagrams)
- Figma (wireframes, prototypes)

**Templates:**
- User Story Template: [As a X, I want Y, so that Z]
- Use Case Template: [Actor, preconditions, main flow, postconditions]
- Requirements Document: [SRD template in assets/]

---

## 8. Best Practices Summary

1. **Start with Why:** Understand business goals before diving into features
2. **Involve Users Early:** Don't rely on secondhand requirements
3. **Iterate:** Requirements evolve—embrace change, but manage it
4. **Be Specific:** Vague requirements = miscommunication
5. **Prioritize Ruthlessly:** Not everything is "high priority"
6. **Document Decisions:** Use ADRs to explain why choices were made
7. **Validate Continuously:** Prototypes, demos, user testing
8. **Think End-to-End:** Don't forget error cases, edge cases, integrations

---

**Key Takeaway:** Good requirements are the foundation of successful projects. Invest time upfront to understand needs deeply—it saves 10x the cost in rework later.
