# n8n Workflow Templates

Production-ready workflow templates untuk berbagai use cases.

## Template List

### 1. basic-webhook.json
**Use Case**: Simple webhook dengan data processing dan response  
**Nodes**: Webhook → Code → Respond to Webhook  
**Perfect for**: API integrations, webhook receivers, form processing

**Quick Start**:
1. Import ke n8n
2. Activate workflow
3. Test dengan POST request ke webhook URL
4. Customize code node untuk use case spesifik

---

### 2. email-automation.json
**Use Case**: Automated email campaigns dari Google Sheets  
**Nodes**: Schedule → Google Sheets → Filter → Gmail → Update Status  
**Perfect for**: Newsletter automation, customer outreach, drip campaigns

**Requirements**:
- Google Sheets OAuth2 credentials
- Gmail OAuth2 credentials
- Spreadsheet dengan columns: name, email, status, last_sent

**Quick Start**:
1. Setup Google Sheets + Gmail credentials
2. Create spreadsheet dengan required columns
3. Configure sheet ID di nodes
4. Test dengan manual trigger sebelum activate schedule

**Sheet Structure**:
```
| name      | email               | status | last_sent           |
|-----------|---------------------|--------|---------------------|
| John Doe  | john@example.com    | active | 2024-01-15T10:00:00Z|
```

---

### 3. ai-content-generation.json
**Use Case**: AI-powered content generation dengan OpenAI  
**Nodes**: Manual → Set Topic → Generate Outline → Generate Content → Generate SEO → Format Output  
**Perfect for**: Blog automation, content marketing, social media content

**Requirements**:
- OpenAI API credentials (GPT-4o + GPT-4o-mini)

**Features**:
- Multi-stage generation (outline → content → SEO)
- Configurable topic, tone, word count
- Automatic SEO metadata (title, description, keywords, slug)
- Cost-optimized ($0.05-0.15 per article)

**Quick Start**:
1. Setup OpenAI credentials
2. Edit "Set Topic" node values:
   - topic: "Your topic here"
   - tone: "professional" | "casual" | "technical"
   - word_count: 500 | 1000 | 1500
3. Execute manually untuk test
4. Integrate dengan publishing nodes (WordPress, Ghost, Medium)

**Output Schema**:
```json
{
  "title": "SEO-optimized title",
  "slug": "url-friendly-slug",
  "content": "Full article content",
  "excerpt": "First 200 characters",
  "meta": {
    "description": "SEO meta description",
    "keywords": ["keyword1", "keyword2"]
  },
  "word_count": 523,
  "generated_at": "2024-01-15T10:00:00Z"
}
```

---

### 4. job-scraping.json
**Use Case**: Automated job hunting dengan AI matching dan notifications  
**Nodes**: Schedule → HTTP Scrape → Parse → Filter → Save to Sheets + AI Summary → Email Alert  
**Perfect for**: Passive job search, career monitoring, opportunity tracking

**Requirements**:
- Job board API or scraping endpoint
- Google Sheets OAuth2 credentials
- OpenAI API credentials
- Gmail OAuth2 credentials

**Features**:
- Daily automated scraping
- Smart matching algorithm (customizable)
- Google Sheets tracking
- AI-powered job analysis
- HTML email notifications

**Quick Start**:
1. Replace HTTP node URL dengan job board API
2. Customize matching logic di "Parse Jobs" code node:
   ```javascript
   const requiredSkills = ['javascript', 'react', 'node.js'];
   ```
3. Setup credentials (Sheets, OpenAI, Gmail)
4. Update email recipient di "Send Email Alert" node
5. Test dengan manual trigger

**Customization Options**:
- **Scraping**: Use Apify actors untuk LinkedIn/Indeed/Glassdoor
- **Matching**: Update requiredSkills, salary range filters
- **Storage**: Switch ke Notion, Airtable, atau database
- **Notifications**: Add Slack, Telegram, or webhooks

**Cost Estimate**:
- Daily: $0.10-0.30
- Monthly: $3-9
- Scraping (Apify): $0.10
- AI summary: $0.01 (GPT-4o-mini)

**Legal Notes**:
⚠️ Most job boards prohibit scraping in ToS. Use official APIs when available or for personal use only.

---

## Usage Workflow

### Import Template
1. Copy template JSON
2. Buka n8n → "Add workflow" → "Import from File"
3. Paste JSON atau upload file
4. Save workflow

### Configure Credentials
1. Klik node yang perlu credentials (merah indicator)
2. "Create new credentials"
3. Follow OAuth flow atau enter API keys
4. Test credentials

### Customize & Test
1. Edit node parameters sesuai kebutuhan
2. Use "Test Workflow" button
3. Check output di each node
4. Iterate sampai hasil sesuai

### Validate & Deploy
1. Run validation:
   ```bash
   python scripts/validate.py workflow.json
   ```
2. Fix errors kalau ada
3. Activate workflow
4. Monitor executions

---

## Template Modification Tips

### Adding Error Handling
```json
{
  "continueOnFail": true,
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 1000
}
```

### Adding Conditional Logic
Use IF node atau Switch node:
```javascript
// IF node condition
{{ $json.status === 'active' ? true : false }}
```

### Adding Rate Limiting
Insert Wait node:
```json
{
  "name": "Wait",
  "type": "n8n-nodes-base.wait",
  "parameters": {
    "amount": 5,
    "unit": "seconds"
  }
}
```

### Adding Logging
Insert Google Sheets append atau Code node:
```javascript
console.log('Processing:', $json.id);
```

---

## Best Practices

### Before Activation
- [ ] Test dengan manual trigger
- [ ] Validate all connections
- [ ] Check error handling
- [ ] Review credentials
- [ ] Set execution timeout
- [ ] Configure error workflow (optional)

### Production Settings
```json
{
  "settings": {
    "executionOrder": "v1",
    "saveDataErrorExecution": "all",
    "saveDataSuccessExecution": "none",
    "executionTimeout": 3600
  }
}
```

### Monitoring
- Check "Executions" tab regularly
- Setup error notifications (Slack/Email)
- Review execution logs
- Track success rate

---

## Common Modifications

### Multi-Platform Publishing
Add nodes setelah content generation:
- WordPress node
- Ghost node  
- Medium (HTTP Request)
- LinkedIn node
- Twitter node

### Database Storage
Replace Google Sheets dengan:
- PostgreSQL node
- MongoDB node
- Airtable node
- Notion node

### Advanced AI Features
- Add image generation (DALL-E, Leonardo AI)
- Add translation nodes
- Add sentiment analysis
- Add content categorization

---

## Resources

- **n8n Docs**: https://docs.n8n.io
- **Template Library**: https://n8n.io/workflows (2,709 templates)
- **Community Forum**: https://community.n8n.io
- **MCP Tools**: Use n8n MCP server untuk discovery & validation

---

## Support

Gunakan scripts di `scripts/` folder untuk:
- `validate.py` - Validate workflow structure
- `template_finder.py` - Search 2,709+ templates
- `workflow_generator.py` - Generate new workflows

**Pro Tip**: Always check existing templates sebelum build from scratch! Use MCP tools:
```
search_templates({ query: "your use case" })
get_templates_for_task({ task: "email_automation" })
```
