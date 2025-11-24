# n8n Production Workflow Patterns

Real-world production workflow examples with template IDs, costs, and implementation details.

## Table of Contents

1. [Marketing Automation](#marketing-automation)
2. [Job Hunting Automation](#job-hunting-automation)
3. [Content Generation & Distribution](#content-generation--distribution)
4. [Multi-Channel Publishing](#multi-channel-publishing)
5. [CRM Integration](#crm-integration)

---

## Marketing Automation

### Email Campaign Automation

**Template #2452: Automated Email Marketing**

**Architecture:**
```
Schedule Trigger (daily)
  → Google Sheets (fetch contacts)
  → Filter (status = "active")
  → OpenAI GPT (personalize content)
  → Random Wait (2-5 minutes, prevent spam)
  → SMTP Email (send)
  → Google Sheets (update "sent" status)
  → Slack (notification summary)
```

**Key Features:**
- Personalization with AI
- Random delays prevent spam flags
- Status tracking in Sheets
- Team notifications

**Cost:** ~$0.05/day for 100 emails
- OpenAI: $0.002/email
- SMTP: Free (SendGrid free tier: 100/day)

**Configuration Tips:**
```javascript
// OpenAI Personalization
{
  resource: "text",
  operation: "message",
  messages: {
    values: [
      {
        role: "system",
        content: "Personalize email based on user data"
      },
      {
        role: "user",
        content: "Name: {{ $json.name }}, Interest: {{ $json.interest }}"
      }
    ]
  }
}

// Random Wait (prevent spam)
{
  amount: "={{ Math.floor(Math.random() * (300 - 120 + 1)) + 120 }}", // 2-5 min
  unit: "seconds"
}
```

### Social Media Automation

**Template #5841: Daily AI Social Media Posts**

**Architecture:**
```
Schedule Trigger (8 AM daily)
  → OpenAI GPT-4 (content generation)
  → DALL-E (image generation)
  → Split into branches
      ├─> LinkedIn (post)
      ├─> Twitter (post)
      ├─> Facebook (post)
      └─> Instagram (post via Graph API)
  → Merge branches
  → MongoDB (log posts)
  → Slack (success notification)
```

**AI Content Generation:**
```javascript
// Platform-specific content
{
  systemMessage: `Generate platform-optimized content:
    - LinkedIn: Professional, 100-200 words
    - Twitter: Concise, 250 chars, 2-3 hashtags
    - Facebook: Conversational, 150-250 words
    - Instagram: Visual-focused, 50-100 words, 5-8 hashtags`,
  userMessage: "Topic: {{ $json.topic }}, Tone: {{ $json.tone }}"
}
```

**Cost:** ~$0.80/day
- OpenAI GPT-4: $0.30
- DALL-E: $0.50
- APIs: Free (within limits)

### CRM Lead Scoring

**Template #5676: Customer Onboarding Automation**

**Architecture:**
```
Webhook (new lead)
  → HTTP Request (Clearbit enrichment)
  → Code (calculate lead score)
  → IF (score > 70?)
      ├─> TRUE: HubSpot (create contact + deal)
      │           → Email (welcome)
      │           → Wait (2 hours)
      │           → Email (onboarding docs)
      │           → Wait (1 day)
      │           → Email (check-in)
      │           → Wait (2 days)
      │           → Email (success guide)
      │           → HubSpot (update status)
      └─> FALSE: Google Sheets (log for review)
  → Slack (notification)
```

**Lead Scoring Algorithm:**
```javascript
// Code node
const items = $input.all();

return items.map(item => {
  const data = item.json;
  let score = 0;
  
  // Company size
  if (data.company?.employees > 100) score += 30;
  else if (data.company?.employees > 10) score += 15;
  
  // Industry
  const targetIndustries = ['technology', 'finance', 'healthcare'];
  if (targetIndustries.includes(data.company?.industry?.toLowerCase())) {
    score += 25;
  }
  
  // Job title
  const decisionMakers = ['ceo', 'cto', 'vp', 'director', 'manager'];
  const title = data.person?.title?.toLowerCase() || '';
  if (decisionMakers.some(role => title.includes(role))) {
    score += 25;
  }
  
  // Website quality
  if (data.company?.domain) score += 10;
  
  // Email verified
  if (data.person?.email_verified) score += 10;
  
  return {
    json: {
      ...data,
      leadScore: score,
      qualified: score >= 70
    }
  };
});
```

---

## Job Hunting Automation

### Multi-Board Job Aggregation

**Template #6927: Job Scraping + AI Matching**

**Architecture:**
```
Webhook (search keywords + resume)
  → Split into 5 parallel branches
      ├─> Apify (LinkedIn Jobs)
      ├─> Apify (Indeed)
      ├─> Apify (Glassdoor)
      ├─> Apify (Upwork)
      └─> HTTP (Custom job boards)
  → Merge (combine results)
  → Code (deduplication by URL)
  → AI Agent + Google Gemini (resume match scoring)
  → Filter (score >= 3)
  → Sort (by score DESC)
  → Google Sheets (append results)
  → Code (generate tailored resumes)
  → Gmail (send top 5 matches with resumes)
```

**Apify Configuration:**
```javascript
// LinkedIn Jobs Scraper
{
  actorId: "apify/linkedin-jobs-scraper",
  input: {
    positions: ["{{ $json.jobTitle }}"],
    locations: ["{{ $json.location }}"],
    count: 25,
    maxDelay: 5
  }
}
```

**AI Resume Matching:**
```javascript
// AI Agent with Structured Output
{
  systemMessage: `You are a job matching expert. Analyze the job description and candidate resume.
  Return a JSON object with:
  - matchScore: 1-5 (1=poor, 5=excellent)
  - matchedSkills: array of matched skills
  - missingSkills: array of required skills candidate lacks
  - recommendation: string explaining the match`,
  
  tools: [
    {
      name: "analyze_match",
      description: "Analyze job-resume match",
      schema: {
        type: "object",
        properties: {
          matchScore: { type: "number", minimum: 1, maximum: 5 },
          matchedSkills: { type: "array", items: { type: "string" }},
          missingSkills: { type: "array", items: { type: "string" }},
          recommendation: { type: "string" }
        }
      }
    }
  ]
}
```

**Cost:** ~$0.10/search
- Apify credits: $0.08 (5 actors)
- AI matching: $0.02 (Gemini)

### Application Tracking System

**Template #6076: Automated Job Applications**

**Architecture:**
```
Cron (check every 4 hours)
  → Google Sheets (fetch "Ready to Apply" jobs)
  → Code (detect platform: LinkedIn/Indeed/custom)
  → Switch (by platform)
      ├─> LinkedIn: HTTP Request (Easy Apply API)
      ├─> Indeed: HTTP Request (Apply API)
      └─> Custom: Webhook (to Browserflow)
  → Wait (5-10 minutes between applications)
  → HTTP Request (check application status)
  → IF (status = "submitted")
      ├─> TRUE: Sheets (update status + date)
      │         → Slack (success notification)
      └─> FALSE: Sheets (log error)
                 → Telegram (manual review needed)
```

**Rate Limiting:**
```javascript
// Wait node - random delay
{
  amount: "={{ Math.floor(Math.random() * (600 - 300 + 1)) + 300 }}",
  unit: "seconds"  // 5-10 minutes
}
```

**Status Tracking Schema (Google Sheets):**
```
| Job Title | Company | Platform | URL | Status | Applied Date | Follow-up Date | Notes |
|-----------|---------|----------|-----|--------|--------------|----------------|-------|
| Senior Dev| Acme    | LinkedIn | ... | Applied| 2025-01-15   | 2025-01-22     | ...   |
```

### Interview Scheduling

**Template #3363: AI-Powered Interview Scheduling**

**Architecture:**
```
Webhook (public chat)
  → GPT-4o Agent (conversation orchestration)
      → Tool: get_calendar_availability
          → Google Calendar (freebusy API)
          → Code (calculate available 30-min slots)
      → Tool: create_calendar_event
          → Google Calendar (create event)
          → Gmail (send confirmation)
  → Code (generate conversation response)
  → HTTP Response (chat reply)
```

**Calendar Availability Tool:**
```javascript
// Sub-workflow
{
  nodes: [
    {
      type: "googleCalendar",
      operation: "freebusy",
      timeMin: "={{ $now.toISO() }}",
      timeMax: "={{ $now.plus({days: 14}).toISO() }}",
      calendars: ["primary"]
    },
    {
      type: "code",
      code: `
        const busy = $input.first().json.calendars.primary.busy;
        const workHours = { start: 9, end: 17 };
        const days = 14;
        
        // Generate 30-min slots for next 14 weekdays
        const slots = [];
        for (let d = 0; d < days; d++) {
          const date = $now.plus({days: d});
          if (date.weekday >= 6) continue; // Skip weekends
          
          for (let h = workHours.start; h < workHours.end; h++) {
            const slotStart = date.set({hour: h, minute: 0});
            const slotEnd = slotStart.plus({minutes: 30});
            
            // Check if slot overlaps with busy times
            const isBusy = busy.some(b => 
              slotStart < new Date(b.end) && slotEnd > new Date(b.start)
            );
            
            if (!isBusy) {
              slots.push({
                start: slotStart.toISO(),
                end: slotEnd.toISO(),
                display: slotStart.toFormat('EEE, MMM dd @ h:mm a')
              });
            }
          }
        }
        
        return [{ json: { availableSlots: slots.slice(0, 5) }}];
      `
    }
  ]
}
```

**Cost:** $0.02/scheduling interaction (GPT-4o)

---

## Content Generation & Distribution

### Blog Automation (Content Farming v4)

**Template #5230: 10 Posts/Day for $21/month**

**Architecture:**
```
Schedule Trigger (every 2.4 hours)
  → RSS Feed Read (10 sources)
  → Filter (last 24 hours)
  → AI Agent (OpenAI GPT-4)
      → Research phase (PerplexityAI API)
      → Title generation
      → Outline creation
      → Content writing (1000-1500 words)
      → SEO metadata
      → Internal linking (max 20 links)
      → External citation management
  → Leonardo AI (featured image generation)
  → WordPress (publish post)
      → Category assignment
      → Tag management
      → Yoast SEO integration
  → MongoDB (log post data)
  → Google Drive (backup)
  → Slack (success notification)
```

**AI Content Pipeline:**
```javascript
// Research Phase
{
  agent: "OpenAI Functions Agent",
  systemMessage: "Research topic thoroughly using PerplexityAI",
  tools: [
    {
      name: "perplexity_search",
      httpRequest: {
        method: "POST",
        url: "https://api.perplexity.ai/chat/completions",
        body: {
          model: "sonar-pro",
          messages: [...]
        }
      }
    }
  ]
}

// Writing Phase
{
  systemMessage: `Write SEO-optimized blog post:
    - 1000-1500 words
    - Conversational tone
    - Include statistics and data
    - Natural keyword integration
    - Clear H2/H3 structure
    - Add internal links (max 20)
    - Include external citations`,
  temperature: 0.7
}
```

**Cost Breakdown (Monthly):**
- OpenAI GPT-4: $180/month (300 posts × $0.60)
- Leonardo AI: $14/month (300 images)
- PerplexityAI: Variable
- MongoDB: Free (512MB)
- Hosting: $1.25/month

**Optimization for $21/month:**
- Use GPT-4o-mini: $6/month
- Leonardo AI: $14/month
- Self-hosted MongoDB: Free
- **Total: $20/month for 300 posts**

### RSS Feed Aggregation & Digest

**Template #2785: Multi-Source News Digest**

**Architecture:**
```
Schedule Trigger (8 AM daily)
  → Split into 10 parallel branches (RSS feeds)
      → TechCrunch
      → Hacker News
      → The Verge
      → ... (7 more sources)
  → Merge (combine all)
  → Filter (last 7 days)
  → Sort (by pubDate DESC)
  → Limit (top 10)
  → Code (normalize data)
  → OpenAI GPT-4 (generate summary)
  → Code (format HTML email)
  → Split branches
      ├─> Gmail (send digest)
      ├─> Trello (create card)
      └─> WhatsApp (notification)
```

**Deduplication Pattern:**
```javascript
// Code node
const items = $input.all();
const seen = new Set();
const unique = [];

for (const item of items) {
  const key = item.json.link || item.json.title;
  if (!seen.has(key)) {
    seen.add(key);
    unique.push(item);
  }
}

return unique.map(item => ({ json: item.json }));
```

### SEO Keyword Research

**Template #3908: Comprehensive Keyword Research**

**Architecture:**
```
Webhook (seed keyword)
  → Split into parallel branches
      ├─> DataForSEO (keyword data)
      ├─> DataForSEO (related keywords)
      ├─> DataForSEO (autocomplete)
      └─> DataForSEO (PAA questions)
  → Merge (combine results)
  → Code (calculate difficulty score)
  → OpenAI GPT-4 (generate content brief)
  → Split branches
      ├─> NocoDB (store data)
      └─> Notion (create page)
```

**DataForSEO Integration:**
```javascript
// HTTP Request node
{
  method: "POST",
  url: "https://api.dataforseo.com/v3/keywords_data/google/search_volume/live",
  authentication: "httpBasicAuth",
  sendBody: true,
  body: [
    {
      keywords: ["{{ $json.keyword }}"],
      location_code: 2840,  // USA
      language_code: "en"
    }
  ]
}
```

**Cost:** $0.02/keyword (DataForSEO credits)

---

## Multi-Channel Publishing

### Blog to Social Media Repurposing

**Architecture:**
```
RSS Feed Read (blog)
  → r.jina.ai (clean Markdown extraction)
  → OpenAI GPT-4o (platform-specific content)
      → LinkedIn: 100-200 words, professional
      → Twitter: 280 chars, thread format
      → Instagram: 50-100 words, hashtag-heavy
      → Facebook: 150-250 words, conversational
  → Split branches
      ├─> LinkedIn (native post)
      ├─> Twitter (thread)
      ├─> Contentdrips (carousel graphics)
      │       → Instagram (carousel post)
      └─> Facebook (post)
  → MongoDB (log distribution)
  → Slack (analytics summary)
```

**Platform-Specific AI Prompts:**
```javascript
// LinkedIn
{
  systemMessage: `Transform blog content for LinkedIn:
    - Professional tone
    - 100-200 words
    - Start with hook question
    - Include 1-2 key insights
    - End with thought-provoking question
    - Add 3-5 relevant hashtags`,
  userMessage: "{{ $json.blogContent }}"
}

// Twitter Thread
{
  systemMessage: `Convert blog to Twitter thread:
    - First tweet: Hook (280 chars)
    - 3-5 follow-up tweets with key points
    - Final tweet: CTA + link
    - Use 2-3 hashtags
    - Number tweets (1/5, 2/5, etc.)`,
  userMessage: "{{ $json.blogContent }}"
}
```

**Time Saved:** 3-5 hours/day for consistent multi-platform content

### Video to Short-Form Content

**Architecture:**
```
YouTube RSS (new video)
  → YouTube (get video details + transcript)
  → OpenAI GPT-4 (extract key moments)
  → Split branches
      ├─> Twitter (key quotes thread)
      ├─> LinkedIn (summary post)
      ├─> Instagram Reels (script for clips)
      └─> TikTok (caption ideas)
  → Notion (content calendar)
```

---

## CRM Integration

### HubSpot <> Salesforce Sync

**Template: Bi-Directional CRM Sync**

**Architecture:**
```
Schedule Trigger (every 30 minutes)
  → Split branches
      ├─> HubSpot → Salesforce Sync
      │     → HubSpot (get updated contacts)
      │     → Code (check last sync timestamp)
      │     → Filter (modified since last sync)
      │     → Salesforce (upsert contacts)
      │     → MongoDB (log sync)
      └─> Salesforce → HubSpot Sync
            → Salesforce (SOQL query modified records)
            → Code (transform data format)
            → HubSpot (batch update)
            → MongoDB (log sync)
  → IF (any errors?)
      ├─> TRUE: Slack (error alert)
      └─> FALSE: Continue
```

**Data Transformation:**
```javascript
// Code node: HubSpot → Salesforce format
const items = $input.all();

return items.map(item => {
  const hs = item.json;
  return {
    json: {
      FirstName: hs.firstname,
      LastName: hs.lastname,
      Email: hs.email,
      Phone: hs.phone,
      Company: hs.company,
      Title: hs.jobtitle,
      LeadSource: hs.lifecyclestage,
      Status: hs.hs_lead_status,
      Custom_Field__c: hs.custom_property
    }
  };
});
```

---

## Implementation Checklist

### Before Building

- [ ] Check 2,709 templates first
- [ ] Validate node configurations
- [ ] Plan error handling
- [ ] Estimate API costs
- [ ] Design data schema

### During Development

- [ ] Use explicit configuration (no defaults)
- [ ] Add retry logic (3 attempts)
- [ ] Implement rate limiting
- [ ] Log important data
- [ ] Test with real data

### Before Production

- [ ] Full workflow validation
- [ ] Error workflow configured
- [ ] Monitoring setup (Slack/Email alerts)
- [ ] Documentation written
- [ ] Cost analysis completed

### Production Maintenance

- [ ] Monitor execution logs (weekly)
- [ ] Review error rates
- [ ] Optimize bottlenecks
- [ ] Update node versions
- [ ] Archive old executions

---

## Resources

**Official Templates:**
- https://n8n.io/workflows (2,709 templates)
- Search by: Marketing, Content, AI, Integration

**Community Showcases:**
- n8n.io/blog/community
- Real production examples
- Cost breakdowns
- Implementation tips

**Template IDs Referenced:**
- #2452: Email Marketing Automation
- #5841: Daily Social Media Posts
- #5676: Customer Onboarding
- #6927: Job Scraping + AI Matching
- #3363: AI Interview Scheduling
- #5230: Content Farming v4
- #2785: News Digest
- #3908: SEO Keyword Research
