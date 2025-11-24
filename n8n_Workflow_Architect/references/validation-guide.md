# n8n Workflow Validation Guide

Comprehensive multi-level validation strategies for production-ready n8n workflows.

## Validation Strategy Overview

```
Level 1: Pre-Build Validation (<100ms)
  → validate_node_minimal() - Quick requirement check

Level 2: Pre-Deploy Validation (~500ms)
  → validate_node_operation() - Operation-aware validation
  → validate_workflow() - Full structural check

Level 3: Production Validation (API-based)
  → n8n_validate_workflow() - Deployed workflow check
  → n8n_autofix_workflow() - Auto-correction
```

---

## Level 1: Pre-Build Validation

### Purpose
Fast validation during development to catch basic errors early.

### Tool: `validate_node_minimal()`

**When to Use:**
- Rapid iteration during building
- Quick sanity checks
- Before adding nodes to workflow

**What It Checks:**
- Required fields present
- Basic type correctness
- Missing mandatory parameters

**Example:**
```javascript
// Before adding node to workflow
validate_node_minimal({
  nodeType: "n8n-nodes-base.httpRequest",
  config: {
    method: "POST",
    url: "https://api.example.com"
  }
})

// Response
{
  valid: false,
  errors: [
    {
      field: "authentication",
      message: "Authentication method required",
      severity: "error"
    }
  ]
}
```

**Performance:** <100ms average

**Best Practice:**
```javascript
// Validate each node before adding to workflow
const nodesToValidate = [
  { type: "n8n-nodes-base.scheduleTrigger", config: {...}},
  { type: "n8n-nodes-base.httpRequest", config: {...}},
  { type: "n8n-nodes-base.openAi", config: {...}}
];

for (const node of nodesToValidate) {
  const result = await validate_node_minimal({
    nodeType: node.type,
    config: node.config
  });
  
  if (!result.valid) {
    console.log(`Validation failed for ${node.type}:`, result.errors);
  }
}
```

---

## Level 2: Pre-Deploy Validation

### 2A: Operation-Aware Node Validation

**Tool: `validate_node_operation()`**

**Validation Profiles:**

1. **minimal** - Only required fields
2. **runtime** - Runtime requirements (RECOMMENDED)
3. **ai-friendly** - Relaxed for AI generation
4. **strict** - Full compliance check

**Profile Comparison:**
```javascript
// Minimal (fastest, least strict)
validate_node_operation({
  nodeType: "n8n-nodes-base.slack",
  config: {
    resource: "channel"
    // Missing operation - will pass on minimal
  },
  profile: "minimal"
})
// Result: Valid (only checks resource exists)

// Runtime (recommended for production)
validate_node_operation({
  nodeType: "n8n-nodes-base.slack",
  config: {
    resource: "channel"
    // Missing operation - will FAIL on runtime
  },
  profile: "runtime"
})
// Result: Invalid (operation required for runtime execution)

// Strict (most thorough)
validate_node_operation({
  nodeType: "n8n-nodes-base.slack",
  config: {
    resource: "channel",
    operation: "create"
    // Missing channelName - will FAIL on strict
  },
  profile: "strict"
})
// Result: Invalid (all required fields must be present)
```

**Best Practice for Production:**
```javascript
// Always use "runtime" profile before deployment
validate_node_operation({
  nodeType: "n8n-nodes-base.httpRequest",
  config: {
    method: "POST",
    url: "https://api.example.com/endpoint",
    authentication: "predefinedCredentialType",
    nodeCredentialType: "httpBasicAuth",
    sendBody: true,
    bodyParameters: {
      parameters: [
        { name: "data", value: "={{ $json }}" }
      ]
    }
  },
  profile: "runtime"
})
```

### 2B: Comprehensive Workflow Validation

**Tool: `validate_workflow()`**

**What It Checks:**

**1. Node Configuration**
```javascript
// Each node validated against its schema
{
  validateNodes: true,  // Check all node configs
  profile: "runtime"    // Use runtime profile
}
```

**2. Connection Integrity**
```javascript
// Structural validation
{
  validateConnections: true
}
```

**Checks:**
- All referenced nodes exist
- No connection cycles
- At least one trigger node
- Proper IF node branching (TRUE/FALSE)
- AI Agent connections (v2.17.0+)

**3. Expression Syntax**
```javascript
// n8n expression validation
{
  validateExpressions: true
}
```

**Checks:**
- `{{ }}` syntax correctness
- Variable references ($json, $node)
- Method calls ($input.all())
- Expression scope

**Complete Example:**
```javascript
validate_workflow({
  workflow: {
    name: "Production Workflow",
    nodes: [
      {
        id: "trigger",
        name: "Schedule Trigger",
        type: "n8n-nodes-base.scheduleTrigger",
        typeVersion: 1,
        position: [250, 300],
        parameters: {
          rule: { interval: [{ field: "hours", value: 1 }] }
        }
      },
      {
        id: "http",
        name: "API Request",
        type: "n8n-nodes-base.httpRequest",
        typeVersion: 4,
        position: [450, 300],
        parameters: {
          method: "GET",
          url: "={{ $json.apiUrl }}",  // Expression validation
          authentication: "predefinedCredentialType"
        }
      }
    ],
    connections: {
      "trigger": {
        "main": [[{ node: "http", type: "main", index: 0 }]]
      }
    }
  },
  options: {
    validateNodes: true,
    validateConnections: true,
    validateExpressions: true,
    profile: "runtime"
  }
})
```

**Response Format:**
```javascript
{
  valid: false,
  errors: [
    {
      nodeId: "http",
      nodeName: "API Request",
      field: "authentication.credentials",
      message: "Credential type 'httpBasicAuth' not configured",
      severity: "error",
      fixSuggestion: "Configure credentials in node settings"
    }
  ],
  warnings: [
    {
      nodeId: "http",
      message: "Using expression in URL - ensure data validation",
      severity: "warning"
    }
  ],
  summary: {
    totalNodes: 2,
    validNodes: 1,
    totalConnections: 1,
    validConnections: 1,
    expressionCount: 1,
    validExpressions: 1
  }
}
```

### 2C: Focused Validation Tools

**Connection-Only Validation:**
```javascript
// Fast structural check
validate_workflow_connections({
  workflow: { nodes: [...], connections: {...} }
})
```

**Use When:**
- Quick structural integrity check
- After connection changes
- Before full validation

**Expression-Only Validation:**
```javascript
// Check n8n expressions only
validate_workflow_expressions({
  workflow: { nodes: [...], connections: {...} }
})
```

**Use When:**
- After adding/modifying expressions
- Before deploying expression-heavy workflows
- Debugging expression errors

---

## Level 3: Production Validation

### 3A: API-Level Validation

**Tool: `n8n_validate_workflow()`**

**Purpose:** Validate deployed workflows in production environment

**When to Use:**
- After deployment
- Before activating workflow
- Regular health checks
- After n8n version upgrades

**Example:**
```javascript
// Validate deployed workflow
n8n_validate_workflow({
  id: "workflow-id-123",
  options: {
    validateNodes: true,
    validateConnections: true,
    validateExpressions: true,
    profile: "runtime"
  }
})
```

**Response:**
```javascript
{
  workflowId: "workflow-id-123",
  workflowName: "Email Campaign",
  valid: true,
  active: true,
  lastExecution: "2025-01-15T10:30:00Z",
  executionStatus: "success",
  errors: [],
  warnings: [
    {
      message: "Node 'HTTP Request' uses deprecated typeVersion 3",
      recommendation: "Update to typeVersion 4"
    }
  ]
}
```

### 3B: Auto-Fix Workflow Errors

**Tool: `n8n_autofix_workflow()`**

**Common Fix Types:**

**1. Expression Format**
```javascript
// Before
"url": "$json.apiUrl"  // Missing {{ }}

// After
"url": "={{ $json.apiUrl }}"  // Auto-fixed
```

**2. TypeVersion Correction**
```javascript
// Before
typeVersion: 2  // Outdated

// After
typeVersion: 4  // Updated to latest
```

**3. Error Output Config**
```javascript
// Before
continueOnFail: true
// (Missing error handling)

// After
continueOnFail: true,
alwaysOutputData: true  // Added for proper error flow
```

**4. Webhook Missing Path**
```javascript
// Before
{
  httpMethod: "POST"
  // Missing path
}

// After
{
  httpMethod: "POST",
  path: "webhook"  // Auto-generated
}
```

**Usage Examples:**

**Preview Fixes (Recommended First Step):**
```javascript
// Don't apply, just preview
n8n_autofix_workflow({
  id: "workflow-id-123",
  applyFixes: false  // Preview only
})

// Response shows what would be fixed
{
  workflowId: "workflow-id-123",
  previewMode: true,
  fixes: [
    {
      nodeId: "HTTP1",
      fixType: "expression-format",
      before: { url: "$json.apiUrl" },
      after: { url: "={{ $json.apiUrl }}" },
      confidence: "high"
    },
    {
      nodeId: "Webhook",
      fixType: "webhook-missing-path",
      before: { httpMethod: "POST" },
      after: { httpMethod: "POST", path: "webhook-abc" },
      confidence: "medium"
    }
  ]
}
```

**Apply High-Confidence Fixes:**
```javascript
n8n_autofix_workflow({
  id: "workflow-id-123",
  applyFixes: true,
  confidenceThreshold: "high",  // Only high-confidence fixes
  maxFixes: 50
})
```

**Apply Specific Fix Types:**
```javascript
n8n_autofix_workflow({
  id: "workflow-id-123",
  applyFixes: true,
  fixTypes: [
    "expression-format",
    "typeversion-correction"
  ]
})
```

**Confidence Levels:**
- **high** (90%+): Safe to auto-apply
- **medium** (70-90%): Review recommended
- **low** (<70%): Manual review required

---

## Validation Workflow

### Recommended Validation Flow

```
1. DEVELOPMENT
   ↓
   For each node:
     → validate_node_minimal()
   ↓
   
2. PRE-DEPLOY
   ↓
   → validate_workflow() (full)
   ↓
   If errors: Fix and retry
   ↓
   
3. DEPLOY
   ↓
   → n8n_create_workflow()
   ↓
   
4. POST-DEPLOY
   ↓
   → n8n_validate_workflow()
   ↓
   If warnings/errors:
     → n8n_autofix_workflow(applyFixes: false) - Preview
     → Review fixes
     → n8n_autofix_workflow(applyFixes: true) - Apply
   ↓
   
5. PRODUCTION
   ↓
   → Activate workflow
   → Monitor executions
```

### Validation Checklist

**Before Building:**
- [ ] Check templates for similar workflows
- [ ] Plan node structure
- [ ] Define data schema
- [ ] Identify error-prone operations

**During Development:**
- [ ] Validate each node with `validate_node_minimal()`
- [ ] Test expressions in isolation
- [ ] Check connections as you build
- [ ] Add error handling early

**Before Deployment:**
- [ ] Full workflow validation (`validate_workflow()`)
- [ ] All errors resolved
- [ ] Warnings reviewed and addressed
- [ ] Test with sample data
- [ ] Error workflow configured

**After Deployment:**
- [ ] API-level validation (`n8n_validate_workflow()`)
- [ ] Review auto-fix suggestions
- [ ] Test workflow execution
- [ ] Monitor first 10 executions
- [ ] Document any issues

**Regular Maintenance:**
- [ ] Weekly validation checks
- [ ] Review error rates
- [ ] Update deprecated nodes
- [ ] Re-validate after n8n upgrades

---

## Common Validation Errors

### Error 1: Missing Required Fields

**Error:**
```javascript
{
  field: "parameters.url",
  message: "URL is required",
  severity: "error"
}
```

**Fix:**
```javascript
// Before
{
  parameters: {
    method: "GET"
  }
}

// After
{
  parameters: {
    method: "GET",
    url: "https://api.example.com/endpoint"
  }
}
```

### Error 2: Invalid Expression Syntax

**Error:**
```javascript
{
  nodeId: "Set",
  field: "parameters.values[0].value",
  message: "Invalid expression syntax: Missing closing }",
  severity: "error"
}
```

**Fix:**
```javascript
// Before
"={{ $json.field }"  // Missing closing brace

// After
"={{ $json.field }}"  // Correct
```

### Error 3: Connection Cycle Detected

**Error:**
```javascript
{
  message: "Connection cycle detected: Node1 → Node2 → Node1",
  severity: "error"
}
```

**Fix:** Remove circular connection, restructure workflow

### Error 4: AI Agent Missing Language Model

**Error (v2.17.0+):**
```javascript
{
  nodeId: "AI_Agent",
  message: "AI Agent must have language model connected to ai_languageModel port",
  severity: "error"
}
```

**Fix:**
```javascript
// Add connection
{
  type: "addConnection",
  source: "OpenAI_Model",
  target: "AI_Agent",
  sourcePort: "ai_languageModel",
  targetPort: "ai_languageModel"
}
```

### Error 5: IF Node Missing Branch Parameter

**Error:**
```javascript
{
  message: "Connection to IF node requires 'branch' parameter",
  severity: "error"
}
```

**Fix:**
```javascript
// Before
{
  type: "addConnection",
  source: "IF_Node",
  target: "Success",
  sourcePort: "main",
  targetPort: "main"
}

// After
{
  type: "addConnection",
  source: "IF_Node",
  target: "Success",
  sourcePort: "main",
  targetPort: "main",
  branch: "true"  // REQUIRED!
}
```

---

## Performance Metrics

### Validation Speed

| Validation Type | Average Time | Use Case |
|----------------|--------------|----------|
| validate_node_minimal | <100ms | Rapid iteration |
| validate_node_operation | ~200ms | Pre-deploy check |
| validate_workflow | ~500ms | Full validation |
| validate_workflow_connections | ~150ms | Structural only |
| validate_workflow_expressions | ~250ms | Expression only |
| n8n_validate_workflow | ~1000ms | API validation |

### Token Costs

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Minimal validation | ~50 | Basic check |
| Node operation | ~200 | With errors |
| Full workflow | ~1000 | 10-node workflow |
| Autofix preview | ~500 | Fix suggestions |

---

## Best Practices

### 1. Validate Early and Often

```javascript
// DON'T: Build entire workflow then validate
// Errors compound, harder to debug

// DO: Validate as you build
for (const node of nodes) {
  await validate_node_minimal({ nodeType: node.type, config: node.config });
}
```

### 2. Use Appropriate Validation Level

```javascript
// Development: Fast validation
validate_node_minimal(...)

// Pre-Deploy: Comprehensive
validate_workflow({ workflow, options: { profile: "runtime" }})

// Production: API-level
n8n_validate_workflow({ id })
```

### 3. Always Preview Autofixes

```javascript
// DON'T: Blindly apply fixes
n8n_autofix_workflow({ id, applyFixes: true })

// DO: Preview first
const preview = await n8n_autofix_workflow({ 
  id, 
  applyFixes: false 
});

// Review, then apply
if (preview.fixes.every(f => f.confidence === "high")) {
  await n8n_autofix_workflow({ id, applyFixes: true });
}
```

### 4. Test with Real Data

```javascript
// After validation, test execution
const result = await n8n_trigger_webhook_workflow({
  webhookUrl: "https://n8n.example.com/webhook-test/abc",
  data: { /* real sample data */ }
});
```

### 5. Document Validation Results

```javascript
// Log validation for audit trail
const validation = await validate_workflow({ workflow });

if (!validation.valid) {
  console.log({
    timestamp: new Date().toISOString(),
    workflowName: workflow.name,
    errors: validation.errors,
    warnings: validation.warnings
  });
}
```

---

## Troubleshooting

### Problem: Validation passes but execution fails

**Cause:** Runtime errors not caught by static validation

**Solution:**
1. Test with real data
2. Add try-catch in Code nodes
3. Enable "Continue On Fail" for non-critical nodes
4. Configure error workflows

### Problem: Too many false positives

**Cause:** Using "strict" profile unnecessarily

**Solution:** Use "runtime" profile for production

### Problem: Autofix breaks workflow

**Cause:** Low-confidence fixes applied

**Solution:** Only apply high-confidence fixes, manual review others

---

## Quick Reference

```bash
# Pre-Build (Fast)
validate_node_minimal({ nodeType, config })

# Pre-Deploy (Comprehensive)
validate_workflow({ 
  workflow, 
  options: { profile: "runtime" }
})

# Production (API)
n8n_validate_workflow({ id })

# Auto-Fix (Preview)
n8n_autofix_workflow({ 
  id, 
  applyFixes: false 
})

# Auto-Fix (Apply)
n8n_autofix_workflow({ 
  id, 
  applyFixes: true,
  confidenceThreshold: "high"
})
```

---

**Resources:**
- **n8n Error Handling**: https://docs.n8n.io/workflows/error-handling/
- **Expression Syntax**: https://docs.n8n.io/code/expressions/
- **Node Types**: https://docs.n8n.io/integrations/builtin/
