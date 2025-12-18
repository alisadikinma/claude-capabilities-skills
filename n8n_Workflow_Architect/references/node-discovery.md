# n8n Node Discovery & Categories Guide

Comprehensive guide to n8n's 543 nodes across trigger, core, AI, database, communication, and file processing categories.

## Table of Contents

1. [Node Categories Overview](#node-categories-overview)
2. [Trigger Nodes](#trigger-nodes)
3. [Core Logic Nodes](#core-logic-nodes)
4. [AI & LangChain Nodes](#ai--langchain-nodes)
5. [Database Nodes](#database-nodes)
6. [Communication Nodes](#communication-nodes)
7. [File Processing Nodes](#file-processing-nodes)
8. [Common Usage Patterns](#common-usage-patterns)

---

## Node Categories Overview

### Package Distribution

| Package | Nodes | Purpose |
|---------|-------|---------|
| **n8n-nodes-base** | 493 | Core integrations & utilities |
| **@n8n/n8n-nodes-langchain** | 50 | AI/LangChain capabilities |

### Category Breakdown

```
Total: 543 nodes
├── Trigger: 104 nodes (19%)
├── Transform: 215 nodes (40%)
├── Output: 138 nodes (25%)
├── Input: 86 nodes (16%)
└── AI-Capable: 271 nodes (50%)
```

### Documentation Coverage

- **87%** (459/543) nodes have human-readable docs
- **99%** property coverage with detailed schemas
- **2,646** real-world configuration examples extracted from templates

---

## Trigger Nodes

**Purpose:** Initiate workflow execution

### Manual & Schedule

**Manual Trigger** (`n8n-nodes-base.manualTrigger`)
- Button-based execution
- Development & testing
- No configuration required

**Schedule Trigger** (`n8n-nodes-base.scheduleTrigger`)
```javascript
{
  rule: {
    interval: [
      { field: "seconds", value: 30 },  // Every 30 seconds
      { field: "minutes", value: 15 },  // Every 15 minutes
      { field: "hours", value: 6 },     // Every 6 hours
      { field: "days", value: 1 }       // Daily
    ]
  }
}
```

**Cron Expression:**
```javascript
{
  mode: "cron",
  cronExpression: "0 9 * * MON-FRI"  // Weekdays at 9 AM
}
```

### Webhook Trigger

**Webhook** (`n8n-nodes-base.webhook`)
```javascript
{
  httpMethod: "POST",
  path: "my-webhook",
  responseMode: "onReceived",  // or "lastNode"
  authentication: "basicAuth"
}
```

**Usage:**
- External system notifications
- Form submissions
- Payment confirmations
- Real-time events

**Testing:**
```
Test URL: https://n8n.example.com/webhook-test/my-webhook
Prod URL: https://n8n.example.com/webhook/my-webhook
```

### Chat Trigger

**Chat Trigger** (`@n8n/n8n-nodes-langchain.chatTrigger`)
- Conversational interfaces
- AI chatbot workflows
- Real-time responses

### Application-Specific Triggers

**Email:**
- Email Trigger (IMAP/Gmail)
- Outlook Trigger (Microsoft 365)

**CRM:**
- HubSpot Trigger (contacts, deals, companies)
- Salesforce Trigger (records, events)

**Communication:**
- Slack Trigger (messages, events)
- Discord Trigger (server events)
- Telegram Trigger (messages, commands)

**Files:**
- Local File Trigger (filesystem monitoring)
- Google Drive Trigger (new/updated files)
- Dropbox Trigger (file events)

**Database:**
- MongoDB Trigger (change streams)
- PostgreSQL Trigger (listen/notify)

---

## Core Logic Nodes

### Code Node

**Code** (`n8n-nodes-base.code`)

**Run Mode: "Run Once for All Items"** (RECOMMENDED)
```javascript
// Access all input items
const items = $input.all();

// Transform all items
return items.map(item => ({
  json: {
    original: item.json,
    calculated: item.json.price * 1.2,
    timestamp: new Date().toISOString()
  }
}));
```

**Run Mode: "Run Once for Each Item"**
```javascript
// Access single item
const item = $input.item;

return {
  json: {
    name: item.json.name,
    email: item.json.email.toLowerCase(),
    domain: item.json.email.split('@')[1]
  }
};
```

**Common Patterns:**
```javascript
// Aggregate items
const items = $input.all();
const total = items.reduce((sum, item) => sum + item.json.amount, 0);
return [{ json: { total }}];

// Filter items
return items.filter(item => item.json.status === 'active');

// Enrich data
return items.map(item => ({
  json: {
    ...item.json,
    enriched: true,
    processedAt: $now.toISO()
  }
}));
```

### Conditional Logic

**IF** (`n8n-nodes-base.if`)
```javascript
{
  conditions: {
    boolean: [
      {
        value1: "={{ $json.age }}",
        operation: "larger",
        value2: 18
      }
    ]
  }
}
```

**Operations:**
- `equal`, `notEqual`
- `larger`, `largerEqual`, `smaller`, `smallerEqual`
- `contains`, `notContains`
- `startsWith`, `endsWith`
- `isEmpty`, `isNotEmpty`

**⚠️ Important:** IF nodes create TRUE/FALSE branches
```javascript
// TRUE branch connection
{
  type: "addConnection",
  source: "IF_Node",
  target: "Success_Handler",
  branch: "true"  // Required!
}

// FALSE branch connection
{
  type: "addConnection",
  source: "IF_Node",
  target: "Error_Handler",
  branch: "false"  // Required!
}
```

**Switch** (`n8n-nodes-base.switch`)
- Multiple branches based on values
- More powerful than IF for multi-way routing

### Data Manipulation

**Edit Fields (Set)** (`n8n-nodes-base.set`)
```javascript
{
  mode: "manual",
  options: {},
  fields: {
    values: [
      {
        name: "fullName",
        stringValue: "={{ $json.firstName }} {{ $json.lastName }}"
      },
      {
        name: "email",
        stringValue: "={{ $json.email.toLowerCase() }}"
      }
    ]
  }
}
```

**Merge** (`n8n-nodes-base.merge`)
- Combine data from multiple branches
- Modes: "Append", "Merge By Key", "Merge By Position"

**Split Out** (`n8n-nodes-base.splitOut`)
- Convert arrays into separate items
- Example: `[1,2,3]` → 3 items

**Aggregate** (`n8n-nodes-base.aggregate`)
- Group items together
- Aggregation functions: sum, average, count, min, max

### HTTP Request

**HTTP Request** (`n8n-nodes-base.httpRequest`)
```javascript
{
  method: "POST",
  url: "https://api.example.com/endpoint",
  authentication: "predefinedCredentialType",
  nodeCredentialType: "httpBasicAuth",
  sendHeaders: true,
  headerParameters: {
    parameters: [
      {
        name: "Content-Type",
        value: "application/json"
      }
    ]
  },
  sendBody: true,
  bodyParameters: {
    parameters: [
      {
        name: "data",
        value: "={{ $json }}"
      }
    ]
  }
}
```

**Authentication Types:**
- None
- Basic Auth
- Header Auth (API Key)
- OAuth1, OAuth2
- Custom Auth

---

## AI & LangChain Nodes

### Architecture: Cluster Model

**Root Nodes** (Start Points):
- AI Agent
- Basic LLM Chain
- LangChain Code

**Sub-Nodes** (Connected via AI ports):
- Chat Models (OpenAI, Google Gemini, Anthropic, etc.)
- Tools (HTTP Request Tool, Code Tool, Workflow Tool)
- Memory (Buffer, Postgres, Redis)
- Document Loaders
- Output Parsers

### AI Agent

**AI Agent** (`@n8n/n8n-nodes-langchain.agent`)

**Agent Types:**
- **Tools Agent**: Function calling with tools
- **SQL Agent**: Database queries
- **Conversational Agent**: Chat with memory
- **OpenAI Functions Agent**: Native OpenAI function calling

**Configuration:**
```javascript
{
  agentType: "toolsAgent",
  systemMessage: "You are a helpful assistant...",
  maxIterations: 10
}
```

**⚠️ Critical Validation (v2.17.0+):**
- MUST have language model connected to `ai_languageModel` port
- Tools connected to `ai_tool` port
- Optional memory via `ai_memory` port

### Chat Models

**OpenAI Chat Model** (`@n8n/n8n-nodes-langchain.lmChatOpenAi`)
```javascript
{
  model: "gpt-4o",
  temperature: 0.7,
  maxTokens: 2000
}
```

**Google Gemini** (`@n8n/n8n-nodes-langchain.lmChatGoogleGemini`)
```javascript
{
  modelName: "gemini-1.5-pro",
  temperature: 0.7
}
```

**Anthropic Claude** (`@n8n/n8n-nodes-langchain.lmChatAnthropic`)
```javascript
{
  model: "claude-3-5-sonnet-20241022",
  temperature: 0.7
}
```

### Tools

**HTTP Request Tool** (`@n8n/n8n-nodes-langchain.toolHttpRequest`)
- AI makes API calls
- JSON schema for parameters
- Response parsing

**Code Tool** (`@n8n/n8n-nodes-langchain.toolCode`)
- Execute JavaScript/Python
- AI-generated code execution
- Sandboxed environment

**Workflow Tool** (`@n8n/n8n-nodes-langchain.toolWorkflow`)
- Call other n8n workflows
- Modular AI capabilities
- Sub-workflow execution

**Custom Tool** (`@n8n/n8n-nodes-langchain.toolAi`)
- **ANY node can be a tool!**
- Connect any node to AI Agent's tool port
- Enables powerful integrations

### Memory

**Buffer Memory** (`@n8n/n8n-nodes-langchain.memoryBufferMemory`)
- In-memory conversation history
- Session-based
- No persistence

**Postgres Chat Memory** (`@n8n/n8n-nodes-langchain.memoryPostgresChat`)
- Persistent conversation history
- User session tracking
- Cross-workflow memory

### Output Parsers

**Structured Output Parser** (`@n8n/n8n-nodes-langchain.outputParserStructured`)
```javascript
{
  jsonSchema: {
    type: "object",
    properties: {
      name: { type: "string" },
      email: { type: "string" },
      score: { type: "number" }
    },
    required: ["name", "email"]
  }
}
```

**Auto-fixing Output Parser** (`@n8n/n8n-nodes-langchain.outputParserAutofixing`)
- Automatically corrects malformed JSON
- Retries with error feedback
- Robust for production

### AI Node Discovery

**Find AI-Capable Nodes:**
```javascript
// List all 271 AI nodes
list_nodes({ isAITool: true, limit: 300 })

// Search AI nodes
search_nodes({ 
  query: "AI langchain", 
  includeExamples: true 
})

// Get AI node details
get_node({
  nodeType: "@n8n/n8n-nodes-langchain.agent",
  detail: "standard"
})
```

---

## Database Nodes

### Supported Databases

| Database | Node Type | Operations |
|----------|-----------|------------|
| PostgreSQL | `n8n-nodes-base.postgres` | CRUD, Query |
| MySQL | `n8n-nodes-base.mySql` | CRUD, Query |
| Microsoft SQL | `n8n-nodes-base.microsoftSql` | CRUD, Query |
| SQLite | `n8n-nodes-base.sqlite` | CRUD, Query |
| MongoDB | `n8n-nodes-base.mongoDb` | CRUD, Aggregation |
| Redis | `n8n-nodes-base.redis` | Get, Set, Delete |
| Supabase | `n8n-nodes-base.supabase` | Table ops, RPC |

### PostgreSQL Example

**Query with Parameters** (Prevents SQL Injection)
```javascript
{
  operation: "executeQuery",
  query: "SELECT * FROM users WHERE email = $1 AND status = $2",
  queryParameters: [
    "={{ $json.email }}",
    "active"
  ]
}
```

**Insert:**
```javascript
{
  operation: "insert",
  table: "users",
  columns: "email,name,created_at",
  values: [
    {
      email: "user@example.com",
      name: "John Doe",
      created_at: "={{ $now.toISO() }}"
    }
  ]
}
```

### MongoDB Example

**Find Documents:**
```javascript
{
  operation: "find",
  collection: "users",
  query: {
    status: "active",
    age: { $gte: 18 }
  },
  limit: 100
}
```

**Aggregation:**
```javascript
{
  operation: "aggregate",
  collection: "orders",
  pipeline: [
    { $match: { status: "completed" }},
    { $group: { 
      _id: "$customerId", 
      total: { $sum: "$amount" }
    }},
    { $sort: { total: -1 }},
    { $limit: 10 }
  ]
}
```

---

## Communication Nodes

### Slack

**Slack** (`n8n-nodes-base.slack`)

**Send Message:**
```javascript
{
  resource: "message",
  operation: "post",
  channel: "#general",
  text: "Workflow completed successfully!",
  attachments: [
    {
      color: "#36a64f",
      title: "Results",
      text: "{{ $json.summary }}"
    }
  ]
}
```

**File Upload:**
```javascript
{
  resource: "file",
  operation: "upload",
  channels: "#reports",
  binaryData: true,
  binaryPropertyName: "data"
}
```

### Email

**Gmail** (`n8n-nodes-base.gmail`)
```javascript
{
  resource: "message",
  operation: "send",
  to: "recipient@example.com",
  subject: "Report - {{ $now.toFormat('yyyy-MM-dd') }}",
  message: "Please see attached report.",
  attachments: "data"
}
```

**SendGrid** (via HTTP Request)
```javascript
{
  method: "POST",
  url: "https://api.sendgrid.com/v3/mail/send",
  authentication: "predefinedCredentialType",
  nodeCredentialType: "sendGridApi",
  sendBody: true,
  bodyParameters: {
    personalizations: [{
      to: [{ email: "user@example.com" }]
    }],
    from: { email: "noreply@example.com" },
    subject: "Welcome!",
    content: [{
      type: "text/html",
      value: "<h1>Welcome</h1>"
    }]
  }
}
```

### Discord

**Discord** (`n8n-nodes-base.discord`)
```javascript
{
  resource: "message",
  operation: "send",
  webhookUrl: "https://discord.com/api/webhooks/...",
  content: "Alert: {{ $json.message }}"
}
```

---

## File Processing Nodes

### Local Files

**Read/Write Files from Disk** (`n8n-nodes-base.readWriteFile`)
```javascript
// Read
{
  operation: "read",
  filePath: "/data/input.csv",
  dataPropertyName: "data"
}

// Write
{
  operation: "write",
  fileName: "output-{{ $now.toFormat('yyyyMMdd') }}.json",
  dataPropertyName: "data"
}
```

### File Conversion

**Convert to File** (`n8n-nodes-base.convertToFile`)
- JSON → CSV
- JSON → JSON file
- HTML → HTML file
- Array → iCal

**Extract from File** (`n8n-nodes-base.extractFromFile`)
- CSV → JSON
- Binary → Text
- Excel → JSON
- PDF → Text (via pdftotext)

### Cloud Storage

**S3** (`n8n-nodes-base.awsS3`)
```javascript
{
  resource: "file",
  operation: "upload",
  bucketName: "my-bucket",
  fileName: "reports/{{ $json.filename }}",
  binaryData: true,
  binaryPropertyName: "data"
}
```

**Google Drive** (`n8n-nodes-base.googleDrive`)
```javascript
{
  resource: "file",
  operation: "upload",
  name: "Report.pdf",
  folderId: "1abc...",
  binaryData: true
}
```

---

## Common Usage Patterns

### Pattern 1: Data Enrichment Pipeline

```
┌───────────────┐
│ Webhook       │  Receive lead data
└───────┬───────┘
        │
┌───────▼───────┐
│ HTTP Request  │  Enrich with Clearbit API
└───────┬───────┘
        │
┌───────▼───────┐
│ Code          │  Calculate lead score
└───────┬───────┘
        │
┌───────▼───────┐
│ IF            │  Score > 70?
└───┬───────┬───┘
    │       │
    │ YES   │ NO
    │       │
┌───▼──┐  ┌─▼───────┐
│Slack │  │ Database│
└──────┘  └─────────┘
```

### Pattern 2: Error Handling

```
┌───────────────┐
│ HTTP Request  │  API call with retry
│ maxTries: 3   │
│ waitBetween:  │
│   5000ms      │
└───────┬───────┘
        │
        │ On error → Error workflow
        │
┌───────▼───────┐
│ Error Trigger │  Error workflow
└───────┬───────┘
        │
┌───────▼───────┐
│ Slack         │  Alert team
└───────┬───────┘
        │
┌───────▼───────┐
│ Database      │  Log error
└───────────────┘
```

### Pattern 3: Multi-Source Aggregation

```
┌──────────┐ ┌──────────┐ ┌──────────┐
│ CRM API  │ │ DB Query │ │ Sheets   │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     └────────────┼────────────┘
                  │
          ┌───────▼───────┐
          │ Merge         │
          └───────┬───────┘
                  │
          ┌───────▼───────┐
          │ Code          │  Transform
          └───────┬───────┘
                  │
          ┌───────▼───────┐
          │ Google Sheets │  Output
          └───────────────┘
```

### Pattern 4: AI Processing Pipeline

```
┌───────────────┐
│ Schedule      │  Daily trigger
└───────┬───────┘
        │
┌───────▼───────┐
│ RSS Read      │  Fetch articles
└───────┬───────┘
        │
┌───────▼───────┐
│ AI Agent      │  Summarize + categorize
│ + OpenAI      │
│ + Tool        │
└───────┬───────┘
        │
┌───────▼───────┐
│ IF            │  Category?
└───┬───────┬───┘
    │       │
Tech│    Business│
    │       │
┌───▼──┐  ┌─▼──────┐
│Slack │  │ Email  │
└──────┘  └────────┘
```

---

## Node Discovery Cheatsheet

```bash
# Find nodes by keyword
search_nodes({ query: "database", includeExamples: true })

# List by category
list_nodes({ category: "trigger" })
list_nodes({ category: "AI" })

# Get node essentials
get_node({ 
  nodeType: "n8n-nodes-base.httpRequest",
  detail: "standard",
  includeExamples: true
})

# Get documentation
get_node_documentation({ 
  nodeType: "nodes-base.slack" 
})

# Find AI-capable nodes
list_nodes({ isAITool: true, limit: 300 })

# Search properties
search_node_properties({
  nodeType: "n8n-nodes-base.httpRequest",
  query: "authentication"
})
```

---

## Best Practices

### 1. Node Selection Priority

1. **Check if standard node exists** (543 nodes cover most cases)
2. **Use HTTP Request for APIs** (universal, flexible)
3. **Code node for custom logic** (when no node matches)
4. **Sub-workflows for reusability** (modular design)

### 2. Configuration Guidelines

- **Explicit > Implicit**: Set all parameters
- **Validate early**: Use `validate_node_minimal()`
- **Use examples**: `includeExamples: true` for real configs
- **Check documentation**: 87% coverage available

### 3. Error Handling

- **Node-level retry**: Set `maxTries: 3`
- **Error workflows**: Configure in settings
- **Continue on fail**: For non-critical nodes
- **Always Output Data**: For debugging

### 4. Performance

- **Batch operations**: Use Code node for loops
- **Parallel execution**: Multiple branches
- **Limit items**: Use `limit` parameter
- **Database optimization**: Parameterized queries

---

## Quick Reference

### Most Used Nodes

```
Triggers:
  - scheduleTrigger (cron/interval)
  - webhook (HTTP endpoints)
  - manualTrigger (testing)

Logic:
  - code (custom JavaScript/Python)
  - if (conditional routing)
  - set (data transformation)

AI:
  - agent (LangChain workflows)
  - lmChatOpenAi (GPT models)
  - outputParserStructured (JSON schema)

Data:
  - httpRequest (API calls)
  - postgres/mysql (SQL databases)
  - mongoDb (NoSQL)

Communication:
  - slack (team notifications)
  - gmail (email)
  - discord (webhooks)

Files:
  - readWriteFile (local filesystem)
  - convertToFile (format conversion)
  - awsS3 (cloud storage)
```

---

**Resources:**
- **Node Search:** Use MCP `search_nodes()` with examples
- **Documentation:** 87% coverage via `get_node_documentation()`
- **Real Configs:** 2,646 examples from templates
- **n8n Docs:** https://docs.n8n.io/integrations/builtin/
