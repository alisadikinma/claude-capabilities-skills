# Technical Tutorial Script Template
**Format:** Step-by-step tutorial  
**Duration:** 45-60 seconds  
**Best for:** How-to, coding tutorials, tool demonstrations

---

## SCRIPT STRUCTURE

### [0-5s] HOOK
**Visual:** Problem on screen (error message, slow loading, broken code)

```
🎯 Script:
"[Struggling with X]? Here's the fix that [specific benefit]"

Examples:
- "Docker container crashing? Here's the 3-line fix"
- "API calls timing out? This caching trick solves it"
- "React re-rendering too much? Watch this"
```

**Shot:** Close-up on problem, quick zoom to face showing confidence

---

### [5-20s] STEP 1: Setup
**Visual:** Screen recording with cursor highlights

```
📝 Script:
"First, [action 1]. This [why it matters]."

Example:
"First, install Redis with 'pip install redis'. This gives us sub-millisecond caching."
```

**Text overlay:** Command/code highlighted  
**Shot:** Screen capture with zoomed-in terminal/editor

---

### [20-35s] STEP 2: Implementation
**Visual:** Live coding, syntax highlighted

```
📝 Script:
"Next, [action 2]. Notice how [key insight]."

Example:
"Next, wrap your function with @cache decorator. Notice how we set TTL to 300 seconds."
```

**Text overlay:** Key code lines with annotation arrows  
**Shot:** Split screen (code + visual result)

---

### [35-50s] STEP 3: Result
**Visual:** Before/after comparison, metrics

```
📝 Script:
"Finally, [action 3]. And boom - [result with number]."

Example:
"Finally, restart the server. And boom - response time drops from 2 seconds to 80ms."
```

**Text overlay:** Metric comparison (2000ms → 80ms)  
**Shot:** Celebratory zoom on graph/metrics

---

### [50-60s] CTA
**Visual:** Face on camera, slight smile

```
📝 Script:
"[Action] for [benefit]. [Optional: tease next video]"

Examples:
- "Follow for daily dev tips that actually work. Tomorrow: scaling this to 1M requests"
- "Save this for your next project. Comment 'CODE' for the full template"
- "Subscribe if you want more performance hacks. Part 2 covers Redis clustering"
```

**Shot:** Direct eye contact, point to subscribe/follow button

---

## PRODUCTION CHECKLIST

- [ ] **Hook shows problem immediately** (no intro fluff)
- [ ] **Each step <15s** (cut ruthlessly)
- [ ] **Code visible and readable** (font size 18+)
- [ ] **Terminal/editor theme** (high contrast, dark mode)
- [ ] **Cursor movements smooth** (not jumpy)
- [ ] **Background music** (low-volume, non-intrusive)
- [ ] **Text overlays animate** (fade in, not static)
- [ ] **Pacing:** Visual change every 3-5 seconds
- [ ] **CTA clear and specific** (not generic "like and subscribe")

---

## VISUAL NOTES FOR EDITOR

**Color Grading:** High contrast, vibrant syntax highlighting  
**Transitions:** Quick cuts, no long fades  
**B-Roll:** None needed - pure tutorial flow  
**Sound Effects:** 
- Typing sounds on Step 1-2
- "Success" chime on Step 3 result
- Subtle "whoosh" on text overlays

**Text Animation Style:** 
- Slide in from left for steps
- Zoom in for metrics/results
- Bounce for CTAs

---

## PLATFORM-SPECIFIC ADJUSTMENTS

### TikTok
- Speed up to 30-45s total
- Combine Steps 2-3 into one
- CTA: "Comment 'CODE' for full version"

### YouTube Shorts
- Full 60s okay
- Can add 5s intro branding
- CTA: "Subscribe for Part 2 where we scale this"

### Instagram Reels
- 45s optimal
- Square 1:1 format option
- CTA: "Save for later + follow for more"

### LinkedIn
- Slower pace okay (60-90s)
- Add professional context hook
- CTA: "Repost if your team needs this"

---

## EXAMPLE: Complete Script

**Topic:** "Fix Slow Python API with Redis Caching"

```
[0-5s] HOOK
VISUAL: API response dashboard showing 2000ms latency, frustrated face
"Your API taking 2 seconds to respond? Here's the 5-minute fix."

[5-20s] STEP 1
VISUAL: Terminal, typing command
"First, install Redis: 'pip install redis'. This gives us lightning-fast caching."
TEXT: pip install redis [animated highlight]

[20-35s] STEP 2  
VISUAL: Code editor, adding decorator
"Next, add this decorator to your slow function. Set TTL to 5 minutes."
TEXT: @cache(expire=300) [annotation arrow]

[35-50s] STEP 3
VISUAL: API dashboard now showing 80ms
"Restart your server. Watch - 2000ms drops to 80ms. That's 25x faster."
TEXT: 2000ms → 80ms [comparison graphic]

[50-60s] CTA
VISUAL: Face, confident smile
"Follow for daily Python tips that actually work. Tomorrow: scaling Redis to 1M requests."
```

**Read-aloud timing:** 55 seconds ✓  
**Visual pacing:** 8 scene changes ✓  
**Hook strength:** Problem + promise ✓  
**CTA specificity:** "daily Python tips" + tease ✓
