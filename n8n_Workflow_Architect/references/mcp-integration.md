# n8n MCP Server Integration Guide

Complete reference for n8n Model Context Protocol (MCP) server integration with Claude.

## Table of Contents

1. [Installation & Configuration](#installation--configuration)
2. [Node Discovery Tools](#node-discovery-tools)
3. [Template Discovery Tools](#template-discovery-tools)
4. [Validation Tools](#validation-tools)
5. [Workflow Management Tools](#workflow-management-tools)
6. [Best Practices](#best-practices)

---

## Installation & Configuration

### Quick Start

**NPX (Zero-Installation):**
```bash
npx -y n8n-mcp@latest
```

**Docker (Production):**
```bash
docker run -it \
  -e N8N_API_URL=https://n8n.example.com \
  -e N8N_API_KEY=your-api-key \
  ghcr.io/romualdczl/n8n-mcp:latest
```

### Claude Desktop Configuration

**File Location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "MCP_MODE": "stdio",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "LOG_LEVEL": "error",
        "N8N_API_URL": "https://your-n8n-instance.com",
        "N8N_API_KEY": "n8n_api_xxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

**Critical Settings:**
- `MCP_MODE: "stdio"` - Prevents JSON parsing errors
- `DISABLE_CONSOLE_OUTPUT: "true"` - Clean protocol communication
- `LOG_LEVEL: "error"` - Minimize noise

**⚠️ Restart Claude Desktop after changes!**

### VS Code / Cursor Configuration

**File: `.cursor/mcp.json` or `.vscode/settings.json`**

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "MCP_MODE": "stdio",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://n8n.example.com",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

---

## Node Discovery Tools

### 1. `search_nodes(query, options)`

**Purpose:** Full-text search across 543 documented nodes

**Parameters:**
```javascript
{
  query: string,              // Search terms (1-6 words optimal)
  limit?: number,             // Max results (default: 20)
  mode?: "OR" | "AND" | "FUZZY",  // Search mode (default: OR)
  includeExamples?: boolean   // Include real-world configs (default: false)
}
```

**Examples:**
```javascript
// Basic search
search_nodes({ query: "email" })

// With real-world examples (RECOMMENDED)
search_nodes({ 
  query: "slack", 
  includeExamples: true 
})

// Fuzzy search (typo-tolerant)
search_nodes({ 
  query: "datbase", 
  mode: "FUZZY" 
})
```

**Returns:**
- Node metadata (type, version, description)
- Top 2 real-world configurations (if `includeExamples: true`)
- Average tokens: 300-800 per node

### 2. `list_nodes(options)`

**Purpose:** Browse nodes by category/package

**Parameters:**
```javascript
{
  limit?: number,           // Max results (default: 50, use 200 for all)
  category?: string,        // "trigger" | "transform" | "output" | "input" | "AI"
  package?: string,         // "n8n-nodes-base" | "@n8n/n8n-nodes-langchain"
  isAITool?: boolean,       // Filter AI-capable nodes
  developmentStyle?: string // "programmatic" | "declarative"
}
```

**Examples:**
```javascript
// List all triggers
list_nodes({ category: "trigger", limit: 200 })

// List AI/LangChain nodes
list_nodes({ package: "@n8n/n8n-nodes-langchain" })

// List AI-capable nodes (271 total)
list_nodes({ isAITool: true, limit: 200 })

// Get all nodes (543 total)
list_nodes({ limit: 543 })
```

### 3. `get_node(nodeType, options)`

**Purpose:** Get detailed node information with progressive detail levels

**Parameters:**
```javascript
{
  nodeType: string,          // Full type: "n8n-nodes-base.slack"
  detail?: string,           // "minimal" | "standard" | "full" (default: standard)
  mode?: string,             // "info" | "versions" | "compare" | "breaking"
  includeExamples?: boolean, // Include template configs (default: false)
  includeTypeInfo?: boolean  // Include type metadata (default: false)
}
```

**Detail Levels:**
- **minimal** (~200 tokens): Name, type, description only
- **standard** (~1-2K tokens): 10-20 critical properties (RECOMMENDED)
- **full** (~3-8K tokens): Complete schema with all 200+ properties

**Examples:**
```javascript
// Get essentials (RECOMMENDED for building)
get_node({
  nodeType: "n8n-nodes-base.httpRequest",
  detail: "standard",
  includeExamples: true
})

// Version history
get_node({
  nodeType: "n8n-nodes-base.slack",
  mode: "versions"
})

// Compare versions
get_node({
  nodeType: "n8n-nodes-base.openAi",
  mode: "compare",
  fromVersion: "1.0",
  toVersion: "2.0"
})
```

### 4. `get_node_documentation(nodeType)`

**Purpose:** Get human-readable documentation with examples

**Parameters:**
```javascript
{
  nodeType: string  // Format: "nodes-base.slack" or "n8n-nodes-base.slack"
}
```

**Coverage:** 87% of nodes (459/543)

**Returns:**
- Authentication methods
- Common patterns
- Code examples
- Best practices
- Known limitations

**Example:**
```javascript
get_node_documentation({ 
  nodeType: "nodes-base.httpRequest" 
})
```

### 5. `search_node_properties(nodeType, query)`

**Purpose:** Find specific properties within a node

**Parameters:**
```javascript
{
  nodeType: string,  // Full node type
  query: string,     // Property to find: "auth", "header", "body"
  maxResults?: number // Default: 20
}
```

**Example:**
```javascript
search_node_properties({
  nodeType: "n8n-nodes-base.httpRequest",
  query: "authentication"
})
```

### 6. `get_node_as_tool_info(nodeType)`

**Purpose:** Learn how to use ANY node as an AI tool

**Key Insight:** ANY node can be an AI tool, not just the 271 auto-detected!

**Example:**
```javascript
get_node_as_tool_info({ 
  nodeType: "n8n-nodes-base.googleSheets" 
})
```

**Returns:**
- Tool connection requirements
- Use cases
- Configuration examples
- Best practices

---

## Template Discovery Tools

### Database Stats
- **Total Templates:** 2,709
- **Metadata Coverage:** 100% (AI-generated)
- **Categories:** Marketing, Content, AI, Integration, Data Processing

### 1. `search_templates(query, options)`

**Purpose:** Text search across template names/descriptions

**Parameters:**
```javascript
{
  query: string,          // Search keyword
  limit?: number,         // Max results (default: 20, max: 100)
  offset?: number,        // Pagination (default: 0)
  fields?: string[]       // Fields to include (default: all)
}
```

**Field Options:**
`["id", "name", "description", "author", "nodes", "views", "created", "url", "metadata"]`

**Examples:**
```javascript
// Basic search
search_templates({ query: "chatbot" })

// Minimal response (fast)
search_templates({
  query: "email automation",
  fields: ["id", "name", "description"],
  limit: 10
})

// Pagination
search_templates({
  query: "content",
  limit: 20,
  offset: 20  // Page 2
})
```

### 2. `search_templates_by_metadata(filters)`

**Purpose:** Smart filtering by AI-generated metadata

**Parameters:**
```javascript
{
  category?: string,         // "automation", "integration", "data processing"
  complexity?: string,       // "simple" | "medium" | "complex"
  minSetupMinutes?: number,  // 5-480
  maxSetupMinutes?: number,  // 5-480
  requiredService?: string,  // "openai", "slack", "google"
  targetAudience?: string,   // "developers", "marketers", "analysts"
  limit?: number,            // Default: 20, max: 100
  offset?: number            // Pagination
}
```

**Examples:**
```javascript
// Simple marketing workflows
search_templates_by_metadata({
  category: "automation",
  complexity: "simple",
  maxSetupMinutes: 15,
  targetAudience: "marketers"
})

// Complex AI workflows requiring OpenAI
search_templates_by_metadata({
  category: "AI",
  complexity: "complex",
  requiredService: "openai"
})
```

### 3. `get_templates_for_task(task, options)`

**Purpose:** Curated recommendations for common automation scenarios

**Available Tasks:**
```javascript
[
  "ai_automation",
  "data_sync",
  "webhook_processing",
  "email_automation",
  "slack_integration",
  "data_transformation",
  "file_processing",
  "scheduling",
  "api_integration",
  "database_operations"
]
```

**Example:**
```javascript
get_templates_for_task({ 
  task: "email_automation",
  limit: 10
})
```

### 4. `list_node_templates(nodeTypes, options)`

**Purpose:** Find templates using specific nodes

**Parameters:**
```javascript
{
  nodeTypes: string[],  // FULL types: "n8n-nodes-base.slack"
  limit?: number,       // Default: 10, max: 100
  offset?: number       // Pagination
}
```

**Example:**
```javascript
list_node_templates({
  nodeTypes: [
    "n8n-nodes-base.httpRequest",
    "n8n-nodes-base.openAi"
  ],
  limit: 20
})
```

### 5. `get_template(templateId, mode)`

**Purpose:** Retrieve complete template

**Modes:**
- **nodes_only**: Just node list (minimal)
- **structure**: Nodes + connections
- **full**: Complete workflow JSON (RECOMMENDED)

**Example:**
```javascript
get_template({ 
  templateId: 5230,  // Content Farming v4
  mode: "full" 
})
```

**⚠️ MANDATORY ATTRIBUTION:**
When using templates, ALWAYS include:
```markdown
Template: [Template Name] by [Author] (@username)
Source: https://n8n.io/workflows/[templateId]
```

---

## Validation Tools

### Validation Strategy (Multi-Level)

```
Pre-Build:
  validate_node_minimal() - <100ms, quick check

Pre-Deploy:
  validate_node_operation() - Operation-aware, profile-based
  validate_workflow() - Full structural check

Production:
  n8n_validate_workflow() - API-level validation
  n8n_autofix_workflow() - Auto-correct common errors
```

### 1. `validate_node_minimal(nodeType, config)`

**Purpose:** Quick validation (<100ms) for rapid iteration

**Parameters:**
```javascript
{
  nodeType: string,  // Full type
  config: object     // Node configuration (can be empty {})
}
```

**Example:**
```javascript
validate_node_minimal({
  nodeType: "n8n-nodes-base.httpRequest",
  config: {}
})
```

**Returns:**
- Required fields
- Missing parameters
- Basic type errors

### 2. `validate_node_operation(nodeType, config, profile)`

**Purpose:** Operation-aware validation with configurable strictness

**Parameters:**
```javascript
{
  nodeType: string,
  config: object,
  profile?: string  // "minimal" | "runtime" | "ai-friendly" | "strict"
}
```

**Profiles:**
- **minimal**: Only required fields
- **runtime**: Runtime requirements (RECOMMENDED)
- **ai-friendly**: Relaxed for AI generation
- **strict**: Full compliance check

**Example:**
```javascript
validate_node_operation({
  nodeType: "n8n-nodes-base.slack",
  config: {
    resource: "channel",
    operation: "create",
    channelName: "my-channel"
  },
  profile: "runtime"
})
```

### 3. `validate_workflow(workflow, options)`

**Purpose:** Comprehensive workflow validation

**Parameters:**
```javascript
{
  workflow: object,  // Complete workflow JSON
  options?: {
    validateNodes?: boolean,      // Default: true
    validateConnections?: boolean,  // Default: true
    validateExpressions?: boolean,  // Default: true
    profile?: string               // For node validation
  }
}
```

**Checks:**
- Node configuration errors
- Connection integrity (no cycles, proper triggers)
- Expression syntax ({{ $json }}, {{ $node["Name"] }})
- AI Agent connections (v2.17.0+)
- Streaming mode constraints

**Example:**
```javascript
validate_workflow({
  workflow: {
    nodes: [...],
    connections: {...}
  },
  options: {
    profile: "runtime"
  }
})
```

### 4. `validate_workflow_connections(workflow)`

**Purpose:** Check structural integrity only (fast)

**Validates:**
- All referenced nodes exist
- No connection cycles
- At least one trigger node
- Proper IF node branching
- AI tool connections

### 5. `validate_workflow_expressions(workflow)`

**Purpose:** Check n8n expression syntax

**Validates:**
- `{{ }}` syntax correctness
- Variable references ($json, $node)
- Method calls ($input.all())
- Expression scope

---

## Workflow Management Tools

**⚠️ Requires N8N_API_URL + N8N_API_KEY configuration**

### 1. `n8n_create_workflow(name, nodes, connections, settings)`

**Purpose:** Deploy new workflow to n8n instance

**Parameters:**
```javascript
{
  name: string,        // Required
  nodes: array,        // Required: node objects
  connections: object, // Required: connection map
  settings?: object    // Optional workflow settings
}
```

**Node Format:**
```javascript
{
  id: "unique-id",
  name: "Node Name",
  type: "n8n-nodes-base.httpRequest",
  typeVersion: 1,
  position: [x, y],
  parameters: {
    // Node-specific config
  }
}
```

**Connection Format:**
```javascript
{
  "sourceNodeId": {
    "main": [
      [
        {
          node: "targetNodeId",
          type: "main",
          index: 0
        }
      ]
    ]
  }
}
```

**Example:**
```javascript
n8n_create_workflow({
  name: "Email Campaign Automation",
  nodes: [
    {
      id: "trigger",
      name: "Schedule Trigger",
      type: "n8n-nodes-base.scheduleTrigger",
      typeVersion: 1,
      position: [250, 300],
      parameters: {
        rule: { interval: [{ field: "days", value: 1 }] }
      }
    },
    {
      id: "http",
      name: "Fetch Contacts",
      type: "n8n-nodes-base.httpRequest",
      typeVersion: 4,
      position: [450, 300],
      parameters: {
        method: "GET",
        url: "https://api.example.com/contacts"
      }
    }
  ],
  connections: {
    "trigger": {
      "main": [[{ node: "http", type: "main", index: 0 }]]
    }
  }
})
```

### 2. `n8n_update_partial_workflow(workflowId, operations, options)`

**Purpose:** Incremental updates with 80-90% token savings

**Parameters:**
```javascript
{
  id: string,
  operations: array,     // Diff operations
  continueOnError?: boolean,  // Best-effort mode
  validateOnly?: boolean      // Preview without applying
}
```

**Operation Types:**

**Update Node:**
```javascript
{
  type: "updateNode",
  nodeId: "HTTP_Request",
  updates: {
    parameters: { url: "https://new-api.com" }
  }
}
```

**Add Node:**
```javascript
{
  type: "addNode",
  node: {
    id: "NewNode",
    name: "OpenAI",
    type: "n8n-nodes-base.openAi",
    typeVersion: 1,
    position: [500, 300],
    parameters: { resource: "chat", operation: "message" }
  }
}
```

**Add Connection:**
```javascript
{
  type: "addConnection",
  source: "SourceNodeId",
  target: "TargetNodeId",
  sourcePort: "main",
  targetPort: "main",
  branch: "true"  // For IF nodes
}
```

**Other Operations:**
- `removeNode`, `moveNode`, `enable/disableNode`
- `removeConnection`, `cleanStaleConnections`
- `updateSettings`, `updateName`
- `add/removeTag`

**Example:**
```javascript
n8n_update_partial_workflow({
  id: "workflow-id-123",
  operations: [
    {
      type: "updateNode",
      nodeId: "HTTP1",
      updates: { parameters: { url: "https://new-api.com" }}
    },
    {
      type: "addConnection",
      source: "HTTP1",
      target: "OpenAI",
      sourcePort: "main",
      targetPort: "main"
    }
  ]
})
```

### 3. `n8n_validate_workflow(workflowId, options)`

**Purpose:** Production readiness check for deployed workflow

**Example:**
```javascript
n8n_validate_workflow({
  id: "workflow-id-123",
  options: {
    profile: "runtime",
    validateConnections: true,
    validateExpressions: true
  }
})
```

### 4. `n8n_autofix_workflow(workflowId, options)`

**Purpose:** Automatically correct common configuration errors

**Parameters:**
```javascript
{
  id: string,
  applyFixes?: boolean,        // Default: false (preview only)
  fixTypes?: string[],         // Specific fix types
  confidenceThreshold?: string, // "high" | "medium" | "low"
  maxFixes?: number            // Default: 50
}
```

**Fix Types:**
```javascript
[
  "expression-format",       // {{ }} syntax
  "typeversion-correction",  // Outdated versions
  "error-output-config",     // Error handling
  "node-type-correction",    // Deprecated nodes
  "webhook-missing-path",    // Webhook configs
  "typeversion-upgrade",     // Safe upgrades
  "version-migration"        // Auto-migrations
]
```

**Example:**
```javascript
// Preview fixes
n8n_autofix_workflow({
  id: "workflow-id-123",
  applyFixes: false
})

// Apply high-confidence fixes
n8n_autofix_workflow({
  id: "workflow-id-123",
  applyFixes: true,
  confidenceThreshold: "high"
})
```

### 5. `n8n_get_execution(executionId, mode, options)`

**Purpose:** Retrieve execution details with smart filtering

**Modes:**
- **preview**: Structure & counts (fast, no data)
- **summary**: 2 samples per node (DEFAULT)
- **filtered**: Custom filtering (itemsLimit, nodeNames)
- **full**: Complete data (use with caution!)

**Example:**
```javascript
// Preview structure first (RECOMMENDED)
n8n_get_execution({
  id: "exec-123",
  mode: "preview"
})

// Get specific nodes only
n8n_get_execution({
  id: "exec-123",
  mode: "filtered",
  nodeNames: ["HTTP Request", "OpenAI"],
  itemsLimit: 5
})
```

### 6. `n8n_trigger_webhook_workflow(webhookUrl, options)`

**Purpose:** Test webhook workflows

**Parameters:**
```javascript
{
  webhookUrl: string,     // Full URL from n8n
  httpMethod?: string,    // GET, POST, PUT, DELETE (default: matches config)
  data?: object,          // Payload
  headers?: object,       // Additional headers
  waitForResponse?: boolean  // Default: true
}
```

**Example:**
```javascript
n8n_trigger_webhook_workflow({
  webhookUrl: "https://n8n.example.com/webhook/abc-123",
  httpMethod: "POST",
  data: {
    email: "user@example.com",
    action: "subscribe"
  },
  waitForResponse: true
})
```

---

## Best Practices

### 1. Always Check Templates First

```javascript
// DON'T: Build from scratch immediately
search_nodes({ query: "email" })

// DO: Check 2,709 templates first
search_templates({ query: "email automation" })
get_templates_for_task({ task: "email_automation" })
```

### 2. Use includeExamples for Real Configs

```javascript
// DON'T: Guess configuration
get_node({ nodeType: "n8n-nodes-base.slack" })

// DO: Get real-world examples
search_nodes({ 
  query: "slack", 
  includeExamples: true  // Top 2 configs from 2,646 templates
})
```

### 3. Explicit Configuration > Defaults

```javascript
// DON'T: Trust default values (number one failure source!)
{
  parameters: {}
}

// DO: Explicitly set ALL parameters
{
  parameters: {
    method: "POST",
    url: "https://api.example.com/endpoint",
    authentication: "predefinedCredentialType",
    nodeCredentialType: "httpBasicAuth",
    sendBody: true,
    bodyParameters: { ... }
  }
}
```

### 4. Multi-Level Validation

```javascript
// Pre-build: Quick check
validate_node_minimal({ nodeType, config })

// Pre-deploy: Full validation
validate_workflow({ workflow })

// Production: API-level check
n8n_validate_workflow({ id: workflowId })
```

### 5. Incremental Updates

```javascript
// DON'T: Replace entire workflow (wastes 80-90% tokens)
n8n_update_full_workflow({ id, nodes, connections })

// DO: Use partial updates
n8n_update_partial_workflow({ 
  id, 
  operations: [
    { type: "updateNode", nodeId, updates },
    { type: "addConnection", source, target }
  ]
})
```

### 6. IF Node Connection Pattern

**CRITICAL:** IF nodes require `branch` parameter!

```javascript
// Add TRUE branch connection
{
  type: "addConnection",
  source: "IF_Node",
  target: "SuccessHandler",
  sourcePort: "main",
  targetPort: "main",
  branch: "true"  // REQUIRED for IF nodes
}

// Add FALSE branch connection
{
  type: "addConnection",
  source: "IF_Node",
  target: "ErrorHandler",
  sourcePort: "main",
  targetPort: "main",
  branch: "false"  // REQUIRED for IF nodes
}
```

### 7. Parallel Tool Execution

```javascript
// Execute multiple searches in parallel
await Promise.all([
  search_nodes({ query: "email" }),
  search_nodes({ query: "slack" }),
  search_templates({ query: "automation" })
])
```

### 8. Template Attribution (Mandatory)

```markdown
## Based on n8n Template

**Template:** Content Farming v4  
**Author:** Jan Oberhauser (@janober)  
**Source:** https://n8n.io/workflows/5230  
**Modified:** Added custom error handling and rate limiting
```

### 9. Production Safety

```javascript
// NEVER edit production workflows directly
// 1. Copy workflow
// 2. Test changes
// 3. Validate
// 4. Deploy

// Example workflow
const prodId = "prod-workflow-123";
const testWorkflow = await n8n_get_workflow({ id: prodId });

// Modify and test
// ... make changes ...

// Validate before deploying
await n8n_validate_workflow({ id: testId });

// Deploy to production
await n8n_update_partial_workflow({ 
  id: prodId, 
  operations: [...] 
});
```

---

## Performance Metrics

### Query Performance
- **Node Search:** ~12ms average (FTS5 full-text search)
- **Template Search:** ~15ms average
- **Validation:** <100ms (minimal), ~500ms (full)

### Token Efficiency
- **Node (standard):** ~1-2K tokens (vs 3-8K for full)
- **Partial Updates:** 80-90% savings vs full replacements
- **Example Configs:** ~200-400 tokens per example

### Database Stats
- **Total Nodes:** 543 (99% property coverage)
- **Documentation:** 87% coverage (459 nodes)
- **Templates:** 2,709 (100% metadata coverage)
- **Example Configs:** 2,646 pre-extracted

---

## Troubleshooting

### MCP Connection Issues

**Problem:** MCP server not connecting

**Solutions:**
1. Check config file location (see Installation section)
2. Verify `MCP_MODE: "stdio"` is set
3. Restart Claude Desktop
4. Check logs: `%APPDATA%\Claude\logs\` (Windows)

### API Access Required

**Problem:** Workflow management tools not available

**Solution:** Configure N8N_API_URL and N8N_API_KEY in environment

**Get API Key:**
```
n8n Settings → API → Generate API Key
```

### Validation Failures

**Problem:** Validate returns errors

**Debug Steps:**
```javascript
// 1. Check node config
validate_node_minimal({ nodeType, config })

// 2. Check expressions
validate_workflow_expressions({ workflow })

// 3. Check connections
validate_workflow_connections({ workflow })

// 4. Full validation
validate_workflow({ workflow })
```

---

## Quick Reference Card

```
DISCOVERY
  search_nodes(query, includeExamples: true)
  search_templates(query)
  get_templates_for_task(task)

CONFIGURATION
  get_node(nodeType, detail: "standard", includeExamples: true)
  validate_node_minimal(nodeType, config)

VALIDATION
  validate_workflow(workflow)
  n8n_validate_workflow(id)
  n8n_autofix_workflow(id, applyFixes: false)

DEPLOYMENT
  n8n_create_workflow(name, nodes, connections)
  n8n_update_partial_workflow(id, operations)

TESTING
  n8n_trigger_webhook_workflow(webhookUrl, data)
  n8n_get_execution(id, mode: "preview")
```

---

**External Resources:**
- **n8n MCP Docs:** https://n8n-mcp.com
- **GitHub:** https://github.com/romualdczlonkowski/n8n-mcp
- **n8n Docs:** https://docs.n8n.io
- **Community:** https://community.n8n.io
