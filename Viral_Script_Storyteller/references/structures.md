# Story Structure Frameworks

**Purpose:** Format-specific frameworks for different video types and platforms

## Universal Story Arc

```
Every great video follows emotional journey:

SETUP → TENSION → RESOLUTION → ACTION

1. SETUP: Establish context (5-10%)
2. TENSION: Build interest/problem (40-60%)
3. RESOLUTION: Deliver payoff (30-40%)
4. ACTION: Drive next step (5-10%)
```

---

## Short-Form Structures (15-60 seconds)

### Structure 1: Problem-Solution Sprint

**Total Duration:** 30-60 seconds  
**Best For:** Bug fixes, quick tips, tool recommendations

```
[0-5s]   HOOK: "Getting this error?"
[5-10s]  PROBLEM: Show/describe the pain
[10-40s] SOLUTION: 2-3 step fix
[40-55s] PROOF: Show it working
[55-60s] CTA: "Follow for more fixes"
```

**Example Script:**
```
(0-3s) "Docker build failing? Here's why"
(3-8s) "You're missing this in your Dockerfile"
(8-25s) "Add COPY requirements.txt first,
         then RUN pip install,
         finally COPY everything else"
(25-50s) [Show successful build]
(50-60s) "Follow for daily Docker tips"
```

**Visual Flow:**
- Error screen → Problematic code → Fixed code → Success

---

### Structure 2: Transformation Story

**Total Duration:** 45-60 seconds  
**Best For:** Before/after, case studies, optimization

```
[0-5s]   HOOK: "How I went from X to Y"
[5-15s]  BEFORE: Starting state (bad metrics)
[15-30s] CHANGE: What I did differently
[30-50s] AFTER: New results (good metrics)
[50-60s] CTA: "Want the full breakdown?"
```

**Example Script:**
```
(0-5s)  "How I cut API response time by 90%"
(5-15s)  "We were at 800ms average, users complaining"
(15-35s) "Added Redis caching, optimized queries,
          implemented CDN for static assets"
(35-50s) "Now at 80ms. Users happy, bounce rate dropped 40%"
(50-60s) "Follow for more performance hacks"
```

**Visual Flow:**
- Slow loading spinner → Graph showing improvement → Happy user

---

### Structure 3: Listicle Rapid-Fire

**Total Duration:** 30-60 seconds  
**Best For:** Tool lists, quick tips, resource compilations

```
[0-3s]   HOOK: "X things every developer needs"
[3-8s]   CONTEXT: Why these matter
[8-45s]  LIST: Item 1 (7s) → Item 2 (7s) → Item 3 (7s) → ...
[45-60s] CTA: "Save this for later"
```

**Example Script:**
```
(0-3s)  "5 VS Code extensions that save hours"
(3-8s)  "I use these daily, they're game-changers"
(8-15s)  "#1: GitHub Copilot - AI pair programmer"
(15-22s) "#2: Thunder Client - API testing in VS Code"
(22-29s) "#3: Error Lens - Inline error display"
(29-36s) "#4: Live Server - Auto-refresh for web"
(36-43s) "#5: Prettier - Auto code formatting"
(43-60s) "Save this list. Links in bio"
```

**Visual Flow:**
- Fast cuts between each item, logo → demo → next

---

### Structure 4: Myth-Buster

**Total Duration:** 30-60 seconds  
**Best For:** Correcting misconceptions, hot takes

```
[0-5s]   HOOK: "Everyone says X, but..."
[5-15s]  MYTH: What people believe
[15-35s] TRUTH: Why it's wrong + correct approach
[35-50s] PROOF: Evidence or example
[50-60s] CTA: "Share if this surprised you"
```

**Example Script:**
```
(0-5s)  "Stop using microservices for everything"
(5-15s) "Everyone thinks they scale better"
(15-35s) "Truth: Monoliths can handle millions of users.
         Microservices add complexity you don't need early"
(35-50s) "Instagram was a monolith serving 30M users"
(50-60s) "Agree or disagree? Comment below"
```

**Visual Flow:**
- Common belief (crossed out) → Truth revealed → Proof

---

## Medium-Form Structures (60-180 seconds)

### Structure 5: Deep-Dive Tutorial

**Total Duration:** 90-180 seconds  
**Best For:** Technical walkthroughs, implementations

```
[0-5s]    HOOK: "Build X in under 3 minutes"
[5-20s]   WHY: Problem this solves
[20-40s]  SETUP: Prerequisites, installation
[40-120s] STEPS: Detailed walkthrough (3-5 steps)
[120-160s] DEMO: Show it working end-to-end
[160-180s] CTA: "Code in description"
```

**Step Structure (within 40-120s section):**
```
Each step:
- State step: "Step 1: Initialize project"
- Show command: "npm create vite@latest"
- Explain briefly: "This scaffolds a Vite app"
- Show result: "Project folder created"
```

**Example Script:**
```
(0-5s)   "Deploy Next.js to Vercel in 2 minutes"
(5-20s)  "Vercel is made for Next.js, zero config needed"
(20-40s) "You need: Node.js, Git, and a GitHub account"
(40-60s) "Step 1: Push code to GitHub repository"
(60-80s) "Step 2: Import repo in Vercel dashboard"
(80-100s) "Step 3: Click deploy, wait 30 seconds"
(100-120s) "Step 4: Your site is live at custom-domain.vercel.app"
(120-160s) [Show deployed site, click around, show speed]
(160-180s) "Full guide in description. Follow for more"
```

**Visual Flow:**
- Problem → Tools needed → Step-by-step screen recording → Final product

---

### Structure 6: Concept Explainer

**Total Duration:** 60-120 seconds  
**Best For:** Technical concepts, system design, architecture

```
[0-5s]   HOOK: "How does X actually work?"
[5-20s]  ANALOGY: Everyday comparison
[20-50s] TECHNICAL: Actual implementation
[50-90s] EXAMPLE: Real-world use case
[90-120s] CTA: "Questions? Comment below"
```

**Example Script:**
```
(0-5s)  "How do WebSockets work?"
(5-20s) "Think of it like a phone call vs texting.
         HTTP is texting - you send, wait for reply.
         WebSockets are a call - both talk anytime"
(20-50s) "WebSockets create a persistent connection.
         Server and client can push data anytime,
         no need to request first"
(50-90s) "Perfect for chat apps, live dashboards,
         multiplayer games - anything real-time"
(90-120s) "Want to build one? Comment 'WEBSOCKET'"
```

**Visual Flow:**
- Analogy illustration → Technical diagram → Real app example

---

## Long-Form Structures (3-10 minutes)

### Structure 7: Complete Tutorial Series

**Total Duration:** 300-600 seconds  
**Best For:** Project builds, comprehensive guides

```
[0-10s]    HOOK: What we're building
[10-60s]   CONTEXT: Why it matters, what you'll learn
[60-120s]  ARCHITECTURE: Overview of system design
[120-480s] IMPLEMENTATION: Step-by-step coding
           ├─ Module 1 (60s)
           ├─ Module 2 (60s)
           ├─ Module 3 (60s)
           ├─ Module 4 (60s)
           └─ Integration (60s)
[480-540s] TESTING: Verify everything works
[540-600s] NEXT STEPS: What to explore, CTA
```

**Example Script:**
```
(0-10s)   "Building a full-stack todo app with Next.js"
(10-60s)  "You'll learn: React, API routes, Prisma, PostgreSQL"
(60-120s) "Architecture: Next.js handles front and back,
           Prisma talks to database, Vercel hosts it"
(120-240s) [Build frontend: components, state, UI]
(240-360s) [Build API: routes, database, CRUD ops]
(360-420s) [Connect: API calls, error handling]
(420-480s) [Style: Tailwind, responsive design]
(480-540s) [Test: Create todo, edit, delete, verify DB]
(540-600s) "Deploy to Vercel next. Link in description"
```

**Visual Flow:**
- Final product demo → Architecture diagram → Code (lots of code) → Testing → Outro

---

### Structure 8: Case Study Deep Dive

**Total Duration:** 180-300 seconds  
**Best For:** Post-mortems, architecture breakdowns, lessons learned

```
[0-10s]    HOOK: The impressive result
[10-40s]   PROBLEM: Original challenge
[40-80s]   ATTEMPTS: What didn't work (briefly)
[80-220s]  SOLUTION: What worked (detailed)
           ├─ Approach 1 (40s)
           ├─ Approach 2 (40s)
           └─ Integration (40s)
[220-260s] RESULTS: Metrics, before/after
[260-300s] LESSONS: Key takeaways, CTA
```

**Example Script:**
```
(0-10s)   "How we scaled to 1M concurrent users"
(10-40s)  "Started with monolith, hitting 10K user limit"
(40-80s)  "Tried vertical scaling - worked until $5K/month"
(80-140s) "Moved to microservices: Auth, API, Workers
          Used Kubernetes for orchestration
          Added Redis for caching"
(140-200s) "Implemented CDN for static assets
           Load balancers across 3 regions
           Database read replicas"
(200-220s) "Result: Handle 1M users, costs $2K/month"
(220-260s) "Lessons: Start simple, scale when needed
           Monitor before optimizing
           Cache aggressively"
(260-300s) "Full architecture breakdown in next video"
```

**Visual Flow:**
- Growth chart → Problem visualization → Solution diagrams → Results → Lessons

---

## Story Rhythm & Pacing

### Fast Pace (TikTok, Shorts)
- **Cut rate:** Every 2-3 seconds
- **Speech rate:** 150-180 words/minute
- **Visual changes:** Constant (text, zoom, B-roll)
- **Music:** Upbeat, trending

### Medium Pace (YouTube, LinkedIn)
- **Cut rate:** Every 5-7 seconds
- **Speech rate:** 130-150 words/minute
- **Visual changes:** Regular (transitions, highlights)
- **Music:** Background, subtle

### Slow Pace (Educational, Deep Dives)
- **Cut rate:** Every 10-15 seconds
- **Speech rate:** 110-130 words/minute
- **Visual changes:** Purposeful (diagram reveals)
- **Music:** Minimal or none

---

## Emotional Journey Mapping

```
Every video should follow emotional curve:

Curiosity → Interest → Aha! Moment → Satisfaction → Desire

Example: Docker Tutorial
├─ Curiosity: "Docker failing?" (hook)
├─ Interest: "Here's the actual problem" (setup)
├─ Aha!: "Add this one line" (solution reveal)
├─ Satisfaction: [Shows it working] (proof)
└─ Desire: "Follow for more" (CTA)
```

---

## Structure Selection Guide

```
Choose structure based on:

┌─ Content Type ───────────┬─ Recommended Structure ─────┐
│ Bug fix                  │ Problem-Solution Sprint     │
│ Tool review              │ Listicle Rapid-Fire        │
│ Performance improvement  │ Transformation Story       │
│ Controversial opinion    │ Myth-Buster                │
│ Technical concept        │ Concept Explainer          │
│ Step-by-step guide       │ Deep-Dive Tutorial         │
│ Build from scratch       │ Complete Tutorial Series   │
│ Production experience    │ Case Study Deep Dive       │
└──────────────────────────┴────────────────────────────┘
```

---

## Script Timing Calculator

**Words per minute by platform:**
- TikTok/Reels: 150-180 WPM (fast, energetic)
- YouTube Shorts: 130-150 WPM (moderate)
- YouTube Long-form: 110-130 WPM (conversational)
- LinkedIn: 100-120 WPM (professional)

**Formula:**
```
Video Length (seconds) ÷ 60 × WPM = Max Word Count

Example:
60-second TikTok:
60 ÷ 60 × 150 = 150 words maximum
```

**Buffer:** Subtract 20% for pauses, visual demos
```
150 words - 20% = 120 words (safe target)
```

---

## Common Structure Mistakes

❌ **Hook too late** (after 5 seconds)  
✓ Hook in first 3 seconds maximum

❌ **Too many concepts** (trying to teach everything)  
✓ One clear concept per video

❌ **No visual variation** (static screen)  
✓ Change visuals every 5-10 seconds

❌ **Rushed ending** (forgetting CTA)  
✓ Reserve last 5 seconds for clear CTA

❌ **Uneven pacing** (slow start, rushed end)  
✓ Consistent energy throughout

---

## Structure Templates Quick Reference

**30-second video:**
```
0-3s:   Hook (curiosity)
3-10s:  Setup (context)
10-25s: Value delivery (main content)
25-30s: CTA
```

**60-second video:**
```
0-5s:   Hook
5-15s:  Problem/Context
15-50s: Solution/Content (2-3 points)
50-60s: CTA
```

**3-minute video:**
```
0-10s:   Hook
10-30s:  Why it matters
30-150s: Step-by-step content
150-170s: Demo/Results
170-180s: Next steps + CTA
```

---

**Remember:** Structure is your video's skeleton. Fill it with personality, energy, and value. The best structures become invisible—viewers just feel engaged.
