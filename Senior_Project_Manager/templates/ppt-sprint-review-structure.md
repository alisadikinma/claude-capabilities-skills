# PowerPoint Sprint Review Structure

## Presentation Overview

**Purpose:** Demonstrate completed work and gather stakeholder feedback  
**Audience:** Product Owner, stakeholders, team  
**Frequency:** End of every sprint (every 2 weeks typical)  
**Duration:** 60-90 minutes (30 min demo, 30 min discussion, optional Q&A)  

## Slide Deck Structure (8 Slides)

### Slide 1: Sprint Overview & Goals
**Layout:** Title slide with sprint metadata

**Elements:**
1. **Title Section (Top 30%):**
   - Project Name
   - "Sprint [N] Review"
   - Sprint Dates (e.g., "Jan 15 - Jan 26, 2024")
   - Team Name

2. **Sprint Goal Box (Center 40%):**
   ```
   🎯 SPRINT GOAL:
   "Implement user authentication and 
    complete profile management features"
   ```
   - Large text, centered
   - Icon (target) before goal
   - Border around box for emphasis

3. **Quick Stats (Bottom 30%):**
   ```
   Sprint Duration:    2 weeks (10 working days)
   Team Capacity:      80 story points
   Stories Completed:  14 of 16 (87.5%)
   Points Completed:   68 of 80 (85%)
   ```

**Visual Notes:**
- Use sprint theme color (e.g., each sprint gets a color)
- Clean, minimal design
- Team logo in corner

---

### Slide 2: Sprint Velocity & Burndown
**Layout:** Dual chart layout

**Header:** "Sprint Metrics" (28pt)

**Left Half: Velocity Trend (60%)**
- **Chart Type:** Column chart with trend line
- **X-Axis:** Sprint numbers (Sprint N-5 to Sprint N)
- **Y-Axis:** Story points completed
- **Data Points:**
  ```
  Sprint N-5: 55 pts
  Sprint N-4: 62 pts
  Sprint N-3: 58 pts
  Sprint N-2: 70 pts
  Sprint N-1: 65 pts
  Sprint N:   68 pts (current)
  ```
- **Trend Line:** Moving average (dotted line)
- **Target Line:** Team capacity (80 pts) - horizontal dashed line

**Callout Box:**
```
Average Velocity: 63 pts
Sprint N Performance: 85% of capacity
Trend: Steady improvement
```

**Right Half: Sprint Burndown (40%)**
- **Chart Type:** Line chart
- **X-Axis:** Days in sprint (Day 1 to Day 10)
- **Y-Axis:** Story points remaining
- **Lines:**
  - Ideal burndown (gray dashed)
  - Actual burndown (blue solid)
- **Annotations:**
  - Mark weekends
  - Highlight significant events (demo day, holiday)

**Visual Notes:**
- Actual line below ideal = ahead of schedule (good)
- Actual line above ideal = behind schedule (needs attention)
- Flat portions = blockers or scope changes

---

### Slide 3: Completed Stories Overview
**Layout:** Table format

**Header:** "Completed User Stories (14 of 16)" (28pt)

**Table Columns:**
| ID | Story | Points | Status | Demo? |
|----|-------|--------|--------|-------|
| US-101 | User login with email/password | 5 | ✅ Done | Yes |
| US-102 | Social login (Google, Facebook) | 8 | ✅ Done | Yes |
| US-103 | Password reset flow | 3 | ✅ Done | Yes |
| US-104 | User profile creation | 5 | ✅ Done | Yes |
| US-105 | Profile photo upload | 3 | ✅ Done | Yes |
| US-106 | Email verification | 2 | ✅ Done | No |
| US-107 | Profile editing | 3 | ✅ Done | Yes |
| US-108 | Account deletion | 2 | ✅ Done | No |
| US-109 | Privacy settings page | 5 | ✅ Done | Yes |
| US-110 | Two-factor authentication | 8 | ✅ Done | Yes |
| US-111 | Login attempt logging | 3 | ✅ Done | No |
| US-112 | Session management | 5 | ✅ Done | No |
| US-113 | Remember me functionality | 2 | ✅ Done | Yes |
| US-114 | Logout functionality | 1 | ✅ Done | No |

**Total Points Completed:** 68 / 80 (85%)

**Visual Notes:**
- Highlight stories marked "Yes" for demo (bold or light blue background)
- Alternate row shading for readability
- Check mark icon (✅) in Status column

**Bottom Section:**
```
📊 Sprint Commitment Achievement: 87.5%
🎯 Story Points Achievement: 85%
```

---

### Slide 4: Incomplete Stories (Carry-Over)
**Layout:** Table with explanation

**Header:** "Incomplete Stories (2 of 16)" (28pt)

**Table:**
| ID | Story | Points | Reason | Status | Next Sprint |
|----|-------|--------|--------|--------|-------------|
| US-115 | OAuth integration testing | 8 | API keys delayed from vendor | 60% | Priority 1 |
| US-116 | Admin dashboard prototype | 13 | Scope expanded during sprint | 30% | Split into 2 stories |

**Analysis Box:**
```
🔍 WHY INCOMPLETE:
• US-115: External dependency (vendor delay by 3 days)
• US-116: Scope creep (added 2 additional reports not in AC)

✅ ACTIONS TAKEN:
• Escalated vendor issue to procurement
• Re-estimated US-116 → split into US-116a (8 pts) and US-116b (5 pts)
• Both stories moved to Sprint N+1 backlog
```

**Visual Notes:**
- Orange/amber color for incomplete stories
- Reason column should be concise but clear
- Action box should show problem-solving

---

### Slide 5: Demo Highlights (Visual Showcase)
**Layout:** Screenshot carousel or grid

**Header:** "Demo Walkthrough" (28pt)

**Content Structure:**
- 3-6 key screenshots with annotations
- Each screenshot: 40% of slide width
- Caption below each: 1-2 lines

**Example Layout:**
```
┌─────────────────┐  ┌─────────────────┐
│  Screenshot 1   │  │  Screenshot 2   │
│  Login Page     │  │  Social Login   │
└─────────────────┘  └─────────────────┘
 "New UI with           "One-click Google
  brand colors"          & Facebook login"

┌─────────────────┐  ┌─────────────────┐
│  Screenshot 3   │  │  Screenshot 4   │
│  Profile Page   │  │  2FA Setup      │
└─────────────────┘  └─────────────────┘
 "Editable fields       "Enhanced security
  with validation"       with SMS/app codes"
```

**Alternative:** Video Recording Link
```
🎥 Full Demo Video: [Link to Loom/YouTube]
Duration: 8 minutes
Key Timestamps:
  0:00 - Login flows
  2:30 - Profile management
  5:15 - Security features
  7:00 - Admin capabilities
```

**Visual Notes:**
- Use actual product screenshots (not mockups)
- Blur sensitive data if needed
- Arrows/circles to highlight new features
- Keep captions benefit-focused ("User can now...")

---

### Slide 6: Technical Achievements & Quality
**Layout:** Split metrics

**Header:** "Engineering Excellence" (28pt)

**Left Half: Technical Metrics (50%)**
```
📈 CODE QUALITY:
• Code Coverage:          87% (target: 80%)
• Code Review Pass Rate:  95%
• Technical Debt Hours:   -12 hours (reduced)
• Build Success Rate:     98%

🐛 DEFECTS:
• Bugs Fixed:             18
• New Bugs Found:         3
• Critical Issues:        0
• Escaped Defects:        1 (minor, UI only)

⚡ PERFORMANCE:
• API Response Time:      < 200ms (target: 300ms)
• Page Load Time:         1.2s (target: 2s)
• Database Queries:       Optimized 15 slow queries
```

**Right Half: DevOps & Infrastructure (50%)**
```
🚀 DEPLOYMENTS:
• Staging Deploys:        12 times this sprint
• Production Deploys:     2 times (smooth)
• Rollback Required:      0

🔐 SECURITY:
• Security Scan:          Passed (0 high/critical)
• Dependencies Updated:   5 packages
• Vulnerability Fixes:    2 medium-severity

📚 DOCUMENTATION:
• API Docs Updated:       ✅
• README Updated:         ✅
• Runbook Created:        ✅ (new)
```

**Visual Notes:**
- Use icons for each category
- Color-code metrics: Green (good), Amber (acceptable), Red (needs attention)
- Compare to previous sprint if possible

---

### Slide 7: Team Retrospective Highlights
**Layout:** Summary format (not full retro)

**Header:** "Team Reflections" (28pt)

**Section 1: What Went Well (Top 30%)**
```
🎉 WINS:
• Pair programming improved code quality
• Daily standups kept team aligned
• Early API testing caught integration issues
• Strong collaboration with design team
```

**Section 2: What Needs Improvement (Middle 30%)**
```
🔧 IMPROVEMENTS:
• Better story splitting (US-116 was too large)
• Earlier dependency identification
• More frequent stakeholder check-ins
• Test environment stability issues
```

**Section 3: Action Items (Bottom 40%)**
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Implement story point limit (max 8 pts) | PM | Sprint N+1 start | Open |
| Schedule bi-weekly vendor sync calls | Tech Lead | Jan 30 | Open |
| Add stakeholder demo on Day 5 | PM | Sprint N+1 | Open |
| Upgrade test environment infrastructure | DevOps | Feb 15 | In Progress |

**Visual Notes:**
- Keep positive tone even for improvements
- Action items should be SMART (specific, measurable)
- Assign owners to ensure accountability
- This is a teaser; full retro is separate meeting

---

### Slide 8: Next Sprint Preview & Questions
**Layout:** Forward-looking summary

**Header:** "Looking Ahead: Sprint N+1" (28pt)

**Section 1: Sprint N+1 Goals (Top 50%)**
```
🎯 NEXT SPRINT GOAL:
"Complete admin dashboard and implement 
 notification system"

📋 PLANNED STORIES (Top Priority):
1. US-116a: Admin user management (8 pts)
2. US-117: Real-time notifications (8 pts)
3. US-118: Email notification templates (5 pts)
4. US-119: Push notification service (8 pts)
5. US-120: Notification preferences (3 pts)
6. US-121: Notification history log (5 pts)

Total Planned: 75 story points
Sprint Capacity: 80 story points
Buffer: 5 points (6%)
```

**Section 2: Key Dates (Bottom 25%)**
```
📅 IMPORTANT DATES:
• Sprint Planning:     Jan 29, 10:00 AM
• Mid-Sprint Review:   Feb 2, 2:00 PM
• Sprint Demo:         Feb 9, 3:00 PM
• Retrospective:       Feb 9, 4:00 PM
```

**Section 3: Questions & Feedback (Bottom 25%)**
```
💬 OPEN DISCUSSION:

Questions for Stakeholders:
• Are you satisfied with the authentication flows?
• Any concerns about the current approach?
• Priority changes for upcoming features?

Feedback Channels:
• Slack: #project-feedback
• Email: pm@company.com
• Jira: Create ticket with label "feedback"
```

**Call to Action Box:**
```
📝 Next Steps:
✓ Review demo recording if you missed any details
✓ Submit feedback by Jan 28
✓ Attend Sprint Planning (Jan 29) if interested
```

---

## Alternative Slide Options

### Optional Slide: Customer Impact
**When to include:** Customer-facing features or significant UX changes

**Elements:**
- User satisfaction scores (if available)
- Support ticket reduction
- Feature adoption rates
- Customer testimonials/feedback quotes
- Usage analytics

**Example:**
```
📊 IMPACT METRICS:
• Login success rate:     98% (up from 92%)
• Support tickets (auth): 15 (down from 45)
• User satisfaction:      4.7/5 stars
• Daily active users:     +12% since release
```

### Optional Slide: Dependencies & Blockers
**When to include:** Complex projects with many integrations

**Elements:**
- Resolved dependencies this sprint
- Remaining dependencies for next sprint
- External blockers identified
- Mitigation plans

### Optional Slide: Technical Debt Report
**When to include:** If debt reduction is a sprint goal

**Elements:**
- Technical debt hours reduced
- Refactoring completed
- Legacy code removed
- Performance improvements
- Architecture improvements

---

## Demo Best Practices

### Live Demo Guidelines
1. **Prepare Demo Script:**
   - 5-7 key user stories to showcase
   - Script happy path AND edge cases
   - Note time allocation per story (3-5 min each)

2. **Demo Environment:**
   - Use staging with stable demo data
   - Have backup screenshots if demo fails
   - Pre-load pages to reduce wait time
   - Clear cache/cookies before demo

3. **Demo Flow:**
   - Start with end-user perspective
   - Show "before" state if applicable
   - Walk through new features step-by-step
   - Highlight acceptance criteria met
   - Mention technical innovations

4. **Engagement:**
   - Pause for questions after each story
   - Invite stakeholders to try features
   - Capture feedback in real-time
   - Note feature requests for backlog

### Demo Backup Plan
If live demo fails:
1. Switch to video recording
2. Show screenshots with walkthrough
3. Reschedule demo for next day
4. Continue with rest of review slides

---

## Presentation Tips

### Time Allocation (90-minute meeting)
- **Slide 1-2:** 10 min (context + metrics)
- **Slide 3-4:** 10 min (story summary)
- **Slide 5:** 30 min (LIVE DEMO - main event)
- **Slide 6:** 10 min (technical details)
- **Slide 7:** 10 min (team insights)
- **Slide 8:** 5 min (next sprint preview)
- **Q&A:** 15 min (open discussion)

### For Product Owner
- Focus on business value delivered
- Highlight customer impact
- Address scope changes proactively
- Celebrate team achievements
- Be honest about challenges

### For Stakeholders
- Start with high-level summary
- Demo is the star - keep slides minimal
- Relate features to business goals
- Quantify impact when possible
- Invite hands-on exploration

### For Distributed Teams
- Record demo ahead of time
- Use screen sharing + video
- Interactive tools (Miro, Mural) for feedback
- Slack thread for async questions
- Follow-up email with recording link

---

## Design Guidelines

### Typography
- **Headers:** Calibri Bold, 28pt
- **Body Text:** Calibri, 16-18pt
- **Captions:** Calibri, 12-14pt
- **Data Labels:** Arial, 14pt

### Color Scheme
**Sprint Status:**
- Completed: #70AD47 (green)
- In Progress: #4472C4 (blue)
- Incomplete: #FFC000 (amber)
- Blocked: #FF0000 (red)

**Charts:**
- Velocity bars: #4472C4
- Trend line: #203864 (dark blue)
- Target line: #7F7F7F (gray, dashed)

**Backgrounds:**
- Slide background: White or #F5F5F5
- Section highlights: Light blue (#E7F0FF)

### Visual Consistency
- Use same layout for all sprint reviews
- Consistent font sizing across slides
- Team logo on every slide (top right)
- Sprint number in footer

---

## Automation Opportunities

### Data Integration
Pull from:
- **Jira/Linear:** Story completion, velocity
- **GitHub/GitLab:** Code metrics, PR stats
- **TestRail:** Test coverage, defect data
- **New Relic/DataDog:** Performance metrics

### PowerPoint Automation (Python)
```python
from pptx import Presentation
import pandas as pd

# Load template
prs = Presentation('sprint-review-template.pptx')

# Update Sprint N on all slides
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            text = shape.text
            text = text.replace("{{SPRINT_NUMBER}}", str(sprint_num))
            text = text.replace("{{SPRINT_DATES}}", sprint_dates)

# Update velocity chart (Slide 2)
chart_slide = prs.slides[1]
chart = chart_slide.shapes[3].chart
chart_data = pd.read_csv('velocity_data.csv')
update_chart(chart, chart_data)

# Generate screenshot grid (Slide 5)
demo_slide = prs.slides[4]
add_screenshots(demo_slide, screenshot_folder='demo_screenshots/')

prs.save(f'Sprint_{sprint_num}_Review.pptx')
```

---

## Quality Checklist

Before the meeting:
- [ ] All velocity/burndown data accurate
- [ ] Screenshots updated with latest build
- [ ] Demo environment tested (dry run)
- [ ] All stakeholders invited
- [ ] Recording setup tested (if remote)
- [ ] Backup plan prepared
- [ ] Feedback mechanism ready
- [ ] Next sprint backlog reviewed
- [ ] File named: "ProjectName_Sprint[N]_Review_YYYYMMDD.pptx"

After the meeting:
- [ ] Recording shared (if recorded)
- [ ] Feedback captured in backlog
- [ ] Action items assigned
- [ ] Presentation archived
- [ ] Thank-you message sent to team

---

## Common Pitfalls to Avoid

❌ **Don't:**
- Turn it into a status meeting (it's about the product)
- Spend too much time on slides (demo is key)
- Skip incomplete stories (be transparent)
- Over-explain technical details to non-technical audience
- Go over time (respect 90-minute limit)
- Forget to celebrate wins

✅ **Do:**
- Let the product speak (demo first)
- Invite hands-on exploration
- Acknowledge team contributions
- Be honest about challenges
- Capture feedback in real-time
- End on a positive, forward-looking note

---

**Integration Note:** This Sprint Review presentation pulls data from:
- Jira/Linear (story status, velocity, burndown)
- GitHub/GitLab (code metrics)
- Test management tools (quality metrics)
- Retrospective notes (team insights)

**Agile Principle:** The Sprint Review is an informal meeting focused on the increment and gathering feedback, NOT a status report for management. Keep it collaborative and product-focused.
