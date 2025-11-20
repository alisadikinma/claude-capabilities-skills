---
name: genz-book-designer
description: |
  Creates engaging business and educational books optimized for Gen Z audiences (15-30 years). Generates viral-worthy titles, curiosity-driven chapter names, and interactive pit stops (games, challenges, visual breaks) per sub-chapter. Includes comprehensive storytelling frameworks, visual psychology principles, and 20+ real-world use cases. Use when designing books for Gen Z, creating business/educational content, brainstorming book titles, structuring engaging chapters, or implementing retention strategies for short attention spans.
---

# GenZ Book Designer

**Transform educational and business books into Gen Z engagement machines with viral titles, interactive pit stops, and visual storytelling.**

This skill helps you design books that Gen Z (15-30 years) actually finish reading by combining:
- **Viral title formulas** that stop scrolling
- **Curiosity-driven chapter naming** (no boring "Chapter 1, Chapter 2")
- **Interactive pit stops** per sub-chapter (games, challenges, visual breaks)
- **Visual psychology** for color, layout, and illustration placement
- **Retention pacing** optimized for short attention spans

## Quick Start

### 1. Generate Viral Book Title

**Input your book concept:**
```
Topic: Starting a side hustle
Target: Gen Z entrepreneurs (18-25)
Tone: Motivational but practical
```

**Claude will generate:**
- 10 title options using proven formulas
- Subtitle variations
- Hook analysis (why each title works)
- A/B testing recommendations

**Example output:**
- "Side Hustle Speedrun: Level Up From Broke to Boss in 90 Days"
- "The $10K Glitch: How Gen Z Hacked the Side Income Code"
- "Your 9-5 is Your Side Hustle Now (Here's the New Playbook)"

### 2. Create Chapter Names

**Standard vs. GenZ Naming:**
```
❌ Chapter 1: Introduction to Marketing
✅ "The Instagram Algorithm is Lying to You (Here's Why)"

❌ Chapter 5: Financial Planning Basics  
✅ "Why Your Parents' Money Advice is Broke (Literally)"
```

**Request format:**
```
Claude, create chapter names for:
- 8 chapters
- Topic: Digital marketing for beginners
- Style: Provocative but educational
```

### 3. Design Pit Stops

**Pit stops = engagement breaks every sub-chapter** to prevent reader fatigue.

**Types available:**
1. **Quick Challenges** (2-3 minutes)
   - "Screenshot your worst ad and caption why it failed"
   - "DM 3 brands with better tagline ideas"
   
2. **Visual Games**
   - Spot the difference (good vs. bad design)
   - Swipe left/right on strategy examples
   
3. **Reflection Prompts**
   - "Before moving on: Which of these 3 mistakes have you made?"
   - Fill-in-the-blank frameworks
   
4. **Progress Checkpoints**
   - "You've unlocked: Storytelling frameworks"
   - Level bars, achievement badges

**Request format:**
```
Claude, design 3 pit stops for sub-chapter:
"How to Write Hooks That Stop Scrolling"
```

## Core Workflows

### Workflow 1: Complete Book Design (End-to-End)

**Step 1: Define Your Book**
```
1. Topic & core message
2. Target audience segment (18-22 college? 25-30 professionals?)
3. Desired outcome (skill, mindset, action)
4. Book length (20K words? 40K words?)
```

**Step 2: Generate Title Options**
Claude provides 10 titles using formulas from `references/title-formulas.md`

**Step 3: Structure Chapters**
- Create 6-10 chapter arc
- Name each chapter using curiosity hooks
- Define 3-5 sub-chapters per chapter
- See `references/chapter-naming.md` for patterns

**Step 4: Design Pit Stops**
- Place 1 pit stop per sub-chapter
- Mix types: challenges, games, reflections
- Reference `assets/pit-stop-library.md` for 100+ ready-made options

**Step 5: Visual Guidance**
- Color palette recommendations (Gen Z psychology)
- Illustration placement per pit stop
- Layout templates for high engagement
- See `references/visual-psychology.md`

**Step 6: Review Use Cases**
Check `references/use-cases.md` for similar book examples

### Workflow 2: Title Brainstorming Only

```
You: "I need a viral title for a book about productivity hacks for remote workers"

Claude:
1. Loads title-formulas.md
2. Generates 10 options with rationale
3. Provides subtitle variations
4. Suggests A/B test approach
```

**Formulas used:**
- The [Number] [Adjective] [Noun] Pattern
- The [Opposite] [Expectation] Hook
- The "Your [Authority Figure] is Wrong" Pattern
- The [Timeframe] Challenge Format
- The [Hidden Truth] Reveal

### Workflow 3: Chapter Naming Sprint

```
You: "I have 8 chapter topics, need Gen Z-style names"

Claude:
1. Reviews your chapter topics
2. Applies naming patterns from chapter-naming.md
3. Provides 2-3 options per chapter
4. Explains hook psychology
```

**Naming patterns:**
- Question hooks ("Why Does [X] Keep Happening?")
- Challenge frames ("[Do This] Before [Consequence]")
- Revelation formats ("The [Thing] No One Tells You About [Topic]")
- Myth-busting ("[Common Belief] is a Scam (Here's Proof)")

### Workflow 4: Pit Stop Design System

```
You: "Design pit stops for chapter: 'How to Validate Your Business Idea in 48 Hours'"

Claude:
1. Identifies 4 sub-chapters in the chapter
2. Designs 1 pit stop per sub-chapter
3. Mixes types (challenge, game, reflection, checkpoint)
4. Provides visual mockup descriptions
```

**Example pit stop:**
```
SUB-CHAPTER: "Finding Your First 10 Beta Customers"

PIT STOP: "The 10-DM Challenge"
Type: Quick Challenge (5 minutes)
Visual: Illustrated checklist with progress bubbles

Instructions:
"Before you flip this page, open Instagram and:
1. Find 3 accounts in your target niche
2. DM them this exact script: [provided]
3. Screenshot their responses
4. Return here to unlock the next section"

Unlock reward: "Beta Customer Script Templates"
```

## Advanced Features

### A. Multi-Format Output

**Request different formats:**
- Standard book manuscript
- Notion-style interactive doc
- Slide deck preview (pitch to publishers)
- Social media teaser series (pre-launch)

**Example:**
```
You: "Convert chapter 3 into a Notion template with embedded pit stops"

Claude generates:
- Toggle sections for each sub-chapter
- Embedded Notion buttons for pit stops
- Progress checkboxes
- Linked databases for challenges
```

### B. Audience Customization

**Segment-specific variations:**

| Age Range | Business Focus | Pit Stop Style |
|-----------|----------------|----------------|
| 15-18 | First jobs, gig economy | Gamified, meme-heavy |
| 19-24 | Side hustles, startups | Challenge-driven, competitive |
| 25-30 | Career growth, leadership | Reflection-focused, professional |

**Request:**
```
"Adjust pit stops for 25-30 age segment"
→ Claude reduces gaming elements, adds strategic reflection prompts
```

### C. Visual Direction

**For each pit stop, Claude provides:**
- Illustration description (brief for designer)
- Color palette (based on visual-psychology.md)
- Layout recommendation (full-page? sidebar? inline?)
- Reference inspiration (similar successful books)

**Example:**
```
Pit Stop: "The Value Ladder"
Visual: Full-page infographic
Colors: Gradient from #FF6B6B (bottom) to #4ECDC4 (top)
Style: Duotone illustration with hand-drawn accents
Inspiration: Similar to "Atomic Habits" visual breakdowns
```

## File References

**When you need deeper guidance, Claude reads these files:**

### Core References
- `references/title-formulas.md` - 50+ viral title patterns with examples
- `references/chapter-naming.md` - Curiosity hook patterns and myth-busting frameworks
- `references/pit-stop-mechanics.md` - Game design, challenge types, engagement theory
- `references/visual-psychology.md` - Color psychology, layout patterns for Gen Z
- `references/use-cases.md` - 20+ real book examples (business, educational, self-help)

### Ready-to-Use Assets
- `assets/pit-stop-library.md` - 100+ pre-designed pit stops (copy-paste ready)
- `assets/title-worksheet.md` - Brainstorming template for title generation
- `assets/chapter-blueprint.md` - Chapter structure template with pit stop placement

**How to use references:**
```
You: "Show me viral title patterns for business books"
→ Claude reads references/title-formulas.md
→ Extracts business-specific patterns
→ Generates custom examples
```

## Key Principles

### 1. Attention Span Economics
**Gen Z reality:**
- Average attention span: 8 seconds (goldfish = 9 seconds)
- Context switching: Every 3-5 minutes on average
- Visual processing: 60,000x faster than text

**Design implications:**
- Sub-chapters: Max 1,200 words (5-6 min read)
- Pit stops: Every 1,200-1,500 words
- Visual breaks: Every 2 pages minimum

### 2. Storytelling Over Lecturing

**Traditional educational book:**
```
"Marketing is important because... [500 words of theory]
Here are the principles... [bullet list]
Now apply this framework... [generic example]"
```

**Gen Z approach:**
```
"Last Tuesday, I lost $2,000 because I ignored this one rule.
Here's exactly what happened... [story]
The mistake? [reveal]
The fix? [actionable framework]
Your turn → [pit stop challenge]"
```

### 3. Visual Hierarchy

**Every page needs:**
- **Primary focus** (main text/story)
- **Secondary element** (callout, quote, or visual)
- **Breathing room** (white space, margins)

**Color coding:**
- Primary content: Black/dark gray text
- Important callouts: Accent color boxes
- Pit stops: Distinct background color (consistent throughout)
- Progress indicators: Gamification colors (green for completion)

### 4. Pit Stop Placement Strategy

**Per sub-chapter structure:**
```
[Hook/Story - 200 words]
↓
[Concept Explanation - 400 words]
↓
[Example/Case Study - 300 words]
↓
[Framework/How-To - 300 words]
↓
⭐ PIT STOP (2-5 minutes)
↓
[Transition to next sub-chapter - 100 words]
```

**Never place pit stops:**
- At the start of a chapter (build momentum first)
- After another pit stop (too frequent = annoying)
- Mid-story or mid-explanation (breaks flow)

## Common Use Cases

### Use Case 1: Side Hustle Guide
```
Title: "The $10K Side Hustle Playbook: 90-Day Sprint from Zero to First Sale"

Chapter structure:
1. "Why Your '5-Year Plan' is Already Obsolete"
   - Pit stop: Revenue goal calculator challenge
2. "The 3 Ideas You Should Steal (Not Create)"
   - Pit stop: Idea validation scorecard game
3. "Week 1: Build Your MVP in a Weekend"
   - Pit stop: 48-hour build challenge
[... 5 more chapters]

Target: 22-28 year olds, entrepreneurial mindset
Pit stops: 70% challenges, 20% games, 10% reflection
```

### Use Case 2: Digital Marketing Crash Course
```
Title: "Marketing for Humans: Stop Talking Like a Brand, Start Sounding Like a Friend"

Visual approach:
- Heavy illustration use (every 2 pages)
- Before/after comparison spreads
- "Swipe left/right" style decision trees

Pit stops focus:
- Screenshot challenges (analyze real ads)
- Caption writing contests (with rubric)
- Platform-specific frameworks (TikTok, IG, LinkedIn)

Target: 19-25, aspiring marketers or creators
```

### Use Case 3: Personal Finance for Gen Z
```
Title: "Broke Millennial 2.0: The Gen Z Money Reset"

Pit stop innovation:
- Budget calculator games (interactive)
- Debt payoff race tracker (visual progress)
- Investment simulator (choose-your-adventure style)

Chapters named as:
- "Your College Debt is a Dragon (Here's How to Slay It)"
- "The Ramen Budget: Eating Well on $40/Week"
- "Investing is Not Gambling (But Here's When It Is)"

Target: 20-26, recent grads or early career
```

## Tips for Success

### DO:
✅ Front-load the best ideas (Gen Z won't wait for "good parts")
✅ Use conversational tone ("you" and "I", not "one should")
✅ Make pit stops optional but rewarding (unlock bonus content)
✅ Test chapter names with target audience (A/B test on social media)
✅ Keep visual descriptions specific (not "add a nice graphic")

### DON'T:
❌ Patronize ("Here's how the internet works, kids")
❌ Over-explain basics (Gen Z learns by doing, not reading theory)
❌ Make pit stops feel like homework (make them fun or skip them)
❌ Use outdated references (no 2019 memes, no pre-pandemic examples)
❌ Create fake urgency ("This strategy only works if you start NOW!")

## Next Steps

### Ready to Start?

**Option 1: Generate Full Book Structure**
```
"Claude, design a complete book structure for:
- Topic: [your topic]
- Target: [age range + context]
- Length: [word count or chapter count]
- Style: [tone + vibe]"
```

**Option 2: Improve Existing Book**
```
"Claude, review my chapter structure and:
- Suggest better chapter names
- Add pit stops where missing
- Improve title for Gen Z appeal"
```

**Option 3: Quick Title Test**
```
"Give me 10 title options for [book concept]"
```

### Need More Examples?

Check `references/use-cases.md` for 20+ detailed book breakdowns across:
- Business/entrepreneurship
- Digital marketing
- Personal finance
- Productivity/time management
- Career development
- Tech/coding for beginners

Each use case includes:
- Full title + subtitle
- Chapter naming examples
- Pit stop samples
- Visual direction
- Target audience analysis

---

**Remember:** Gen Z doesn't want another textbook. They want a guide that feels like a conversation with a smart friend who gets it. Make your book that friend.