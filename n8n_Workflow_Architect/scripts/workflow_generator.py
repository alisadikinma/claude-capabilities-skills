#!/usr/bin/env python3
"""
n8n Workflow Generator
Generate n8n workflow JSON structures from scratch or templates.

Usage:
    python workflow_generator.py --name "My Workflow" --output workflow.json
    python workflow_generator.py --template basic-webhook --output webhook.json
    python workflow_generator.py --from-template 5230 --customize
"""

import json
import sys
import argparse
from typing import Dict, List, Any, Optional
from datetime import datetime

class WorkflowGenerator:
    """Generate n8n workflow structures."""
    
    def __init__(self):
        self.node_counter = 0
        self.templates = {
            "basic-webhook": self.create_basic_webhook,
            "scheduled-task": self.create_scheduled_task,
            "api-integration": self.create_api_integration,
            "email-automation": self.create_email_automation,
            "ai-workflow": self.create_ai_workflow
        }
    
    def generate_node_id(self) -> str:
        """Generate unique node ID."""
        self.node_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"node_{timestamp}_{self.node_counter}"
    
    def create_node(
        self,
        name: str,
        node_type: str,
        type_version: int = 1,
        position: tuple = (250, 300),
        parameters: Dict = None
    ) -> Dict[str, Any]:
        """
        Create a workflow node.
        
        Args:
            name: Display name for the node
            node_type: Full node type (e.g., "n8n-nodes-base.webhook")
            type_version: Node version (usually 1 or 2)
            position: (x, y) coordinates in editor
            parameters: Node-specific parameters
        """
        return {
            "id": self.generate_node_id(),
            "name": name,
            "type": node_type,
            "typeVersion": type_version,
            "position": list(position),
            "parameters": parameters or {}
        }
    
    def create_connection(
        self,
        source_id: str,
        target_id: str,
        source_port: str = "main",
        target_port: str = "main",
        branch: Optional[str] = None
    ) -> tuple:
        """
        Create a connection between nodes.
        
        Returns: (source_id, connection_dict)
        """
        connection = {
            "node": target_id,
            "type": target_port,
            "index": 0
        }
        
        if branch:
            connection["branch"] = branch
        
        return (source_id, {
            source_port: [[connection]]
        })
    
    def create_workflow(
        self,
        name: str,
        nodes: List[Dict],
        connections: Dict[str, Any] = None,
        settings: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create complete workflow structure.
        
        Args:
            name: Workflow name
            nodes: List of node dictionaries
            connections: Connection mapping
            settings: Workflow settings
        """
        workflow = {
            "name": name,
            "nodes": nodes,
            "connections": connections or {},
            "active": False,
            "settings": settings or {
                "executionOrder": "v1"
            },
            "versionId": self.generate_node_id(),
            "meta": {
                "templateCredsSetupCompleted": True,
                "instanceId": self.generate_node_id()
            }
        }
        
        return workflow
    
    def create_basic_webhook(self, name: str = "Basic Webhook") -> Dict[str, Any]:
        """Create a basic webhook workflow."""
        # Create nodes
        webhook_node = self.create_node(
            name="Webhook",
            node_type="n8n-nodes-base.webhook",
            position=(250, 300),
            parameters={
                "httpMethod": "POST",
                "path": "webhook-endpoint",
                "responseMode": "responseNode",
                "options": {}
            }
        )
        
        code_node = self.create_node(
            name="Process Data",
            node_type="n8n-nodes-base.code",
            position=(450, 300),
            parameters={
                "mode": "runOnceForAllItems",
                "jsCode": "// Process webhook data\nreturn items.map(item => ({\n  json: {\n    processed: true,\n    data: item.json\n  }\n}));"
            }
        )
        
        response_node = self.create_node(
            name="Respond to Webhook",
            node_type="n8n-nodes-base.respondToWebhook",
            position=(650, 300),
            parameters={
                "options": {}
            }
        )
        
        # Create connections
        connections = {}
        source_id, conn = self.create_connection(
            webhook_node["id"], code_node["id"]
        )
        connections[source_id] = conn
        
        source_id, conn = self.create_connection(
            code_node["id"], response_node["id"]
        )
        connections[source_id] = conn
        
        return self.create_workflow(
            name=name,
            nodes=[webhook_node, code_node, response_node],
            connections=connections
        )
    
    def create_scheduled_task(self, name: str = "Scheduled Task") -> Dict[str, Any]:
        """Create a scheduled task workflow."""
        schedule_node = self.create_node(
            name="Schedule Trigger",
            node_type="n8n-nodes-base.scheduleTrigger",
            position=(250, 300),
            parameters={
                "rule": {
                    "interval": [{"field": "hours", "hoursInterval": 24}]
                }
            }
        )
        
        http_node = self.create_node(
            name="HTTP Request",
            node_type="n8n-nodes-base.httpRequest",
            type_version=4,
            position=(450, 300),
            parameters={
                "method": "GET",
                "url": "https://api.example.com/data",
                "authentication": "none",
                "options": {}
            }
        )
        
        code_node = self.create_node(
            name="Process Response",
            node_type="n8n-nodes-base.code",
            position=(650, 300),
            parameters={
                "mode": "runOnceForAllItems",
                "jsCode": "// Process API response\nreturn items.map(item => ({\n  json: {\n    processed: new Date().toISOString(),\n    data: item.json\n  }\n}));"
            }
        )
        
        connections = {}
        source_id, conn = self.create_connection(
            schedule_node["id"], http_node["id"]
        )
        connections[source_id] = conn
        
        source_id, conn = self.create_connection(
            http_node["id"], code_node["id"]
        )
        connections[source_id] = conn
        
        return self.create_workflow(
            name=name,
            nodes=[schedule_node, http_node, code_node],
            connections=connections
        )
    
    def create_api_integration(self, name: str = "API Integration") -> Dict[str, Any]:
        """Create API integration workflow with error handling."""
        webhook_node = self.create_node(
            name="Webhook",
            node_type="n8n-nodes-base.webhook",
            position=(250, 300),
            parameters={
                "httpMethod": "POST",
                "path": "api-integration"
            }
        )
        
        http_node = self.create_node(
            name="Call External API",
            node_type="n8n-nodes-base.httpRequest",
            type_version=4,
            position=(450, 300),
            parameters={
                "method": "POST",
                "url": "https://api.example.com/endpoint",
                "authentication": "none",
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {
                            "name": "data",
                            "value": "={{ $json.input }}"
                        }
                    ]
                },
                "options": {
                    "retry": {
                        "maxTries": 3,
                        "waitBetweenTries": 1000
                    }
                }
            }
        )
        
        if_node = self.create_node(
            name="Check Success",
            node_type="n8n-nodes-base.if",
            type_version=2,
            position=(650, 300),
            parameters={
                "conditions": {
                    "options": {
                        "caseSensitive": True,
                        "leftValue": ""
                    },
                    "conditions": [
                        {
                            "leftValue": "={{ $json.statusCode }}",
                            "rightValue": 200,
                            "operator": {
                                "type": "number",
                                "operation": "equals"
                            }
                        }
                    ],
                    "combinator": "and"
                }
            }
        )
        
        success_node = self.create_node(
            name="Success Response",
            node_type="n8n-nodes-base.respondToWebhook",
            position=(850, 250),
            parameters={
                "respondWith": "json",
                "responseBody": "={{ { success: true, data: $json } }}"
            }
        )
        
        error_node = self.create_node(
            name="Error Response",
            node_type="n8n-nodes-base.respondToWebhook",
            position=(850, 350),
            parameters={
                "respondWith": "json",
                "responseCode": 500,
                "responseBody": "={{ { success: false, error: $json.error } }}"
            }
        )
        
        connections = {}
        
        # Webhook -> HTTP Request
        source_id, conn = self.create_connection(
            webhook_node["id"], http_node["id"]
        )
        connections[source_id] = conn
        
        # HTTP Request -> IF
        source_id, conn = self.create_connection(
            http_node["id"], if_node["id"]
        )
        connections[source_id] = conn
        
        # IF -> Success (true branch)
        source_id, conn = self.create_connection(
            if_node["id"], success_node["id"], branch="true"
        )
        if source_id in connections:
            connections[source_id]["main"][0].append(conn["main"][0][0])
        else:
            connections[source_id] = conn
        
        # IF -> Error (false branch)
        source_id, conn = self.create_connection(
            if_node["id"], error_node["id"], branch="false"
        )
        if source_id in connections:
            connections[source_id]["main"][0].append(conn["main"][0][0])
        else:
            connections[source_id] = conn
        
        return self.create_workflow(
            name=name,
            nodes=[webhook_node, http_node, if_node, success_node, error_node],
            connections=connections,
            settings={
                "executionOrder": "v1",
                "saveDataErrorExecution": "all",
                "saveDataSuccessExecution": "none"
            }
        )
    
    def create_email_automation(self, name: str = "Email Automation") -> Dict[str, Any]:
        """Create email automation workflow."""
        schedule_node = self.create_node(
            name="Daily Trigger",
            node_type="n8n-nodes-base.scheduleTrigger",
            position=(250, 300),
            parameters={
                "rule": {
                    "interval": [{"field": "hours", "hoursInterval": 24}]
                }
            }
        )
        
        sheets_node = self.create_node(
            name="Get Contact List",
            node_type="n8n-nodes-base.googleSheets",
            position=(450, 300),
            parameters={
                "operation": "read",
                "sheetName": "Contacts",
                "options": {}
            }
        )
        
        gmail_node = self.create_node(
            name="Send Email",
            node_type="n8n-nodes-base.gmail",
            type_version=2,
            position=(650, 300),
            parameters={
                "operation": "send",
                "emailType": "text",
                "toList": "={{ $json.email }}",
                "subject": "Daily Newsletter",
                "message": "={{ $json.message }}",
                "options": {}
            }
        )
        
        connections = {}
        source_id, conn = self.create_connection(
            schedule_node["id"], sheets_node["id"]
        )
        connections[source_id] = conn
        
        source_id, conn = self.create_connection(
            sheets_node["id"], gmail_node["id"]
        )
        connections[source_id] = conn
        
        return self.create_workflow(
            name=name,
            nodes=[schedule_node, sheets_node, gmail_node],
            connections=connections
        )
    
    def create_ai_workflow(self, name: str = "AI Workflow") -> Dict[str, Any]:
        """Create AI-powered workflow with OpenAI."""
        manual_node = self.create_node(
            name="Manual Trigger",
            node_type="n8n-nodes-base.manualTrigger",
            position=(250, 300),
            parameters={}
        )
        
        openai_node = self.create_node(
            name="OpenAI Chat",
            node_type="n8n-nodes-base.openAi",
            type_version=1,
            position=(450, 300),
            parameters={
                "resource": "chat",
                "operation": "message",
                "modelId": "gpt-4o-mini",
                "messages": {
                    "values": [
                        {
                            "role": "user",
                            "content": "={{ $json.prompt }}"
                        }
                    ]
                },
                "options": {}
            }
        )
        
        code_node = self.create_node(
            name="Format Response",
            node_type="n8n-nodes-base.code",
            position=(650, 300),
            parameters={
                "mode": "runOnceForAllItems",
                "jsCode": "return items.map(item => ({\n  json: {\n    input: item.json.prompt,\n    output: item.json.message.content,\n    timestamp: new Date().toISOString()\n  }\n}));"
            }
        )
        
        connections = {}
        source_id, conn = self.create_connection(
            manual_node["id"], openai_node["id"]
        )
        connections[source_id] = conn
        
        source_id, conn = self.create_connection(
            openai_node["id"], code_node["id"]
        )
        connections[source_id] = conn
        
        return self.create_workflow(
            name=name,
            nodes=[manual_node, openai_node, code_node],
            connections=connections
        )

def main():
    parser = argparse.ArgumentParser(
        description='Generate n8n workflow JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Templates:
  basic-webhook       - Simple webhook with response
  scheduled-task      - Daily scheduled API call
  api-integration     - API integration with error handling
  email-automation    - Email automation with Google Sheets
  ai-workflow         - AI workflow with OpenAI

Examples:
  %(prog)s --name "My Workflow" --output workflow.json
  %(prog)s --template basic-webhook --output webhook.json
  %(prog)s --template api-integration --name "Custom API" --output custom.json
        """
    )
    
    parser.add_argument('--name', default='Generated Workflow',
                       help='Workflow name')
    parser.add_argument('--template', 
                       choices=['basic-webhook', 'scheduled-task', 
                               'api-integration', 'email-automation', 'ai-workflow'],
                       help='Template to use')
    parser.add_argument('--output', required=True,
                       help='Output JSON file path')
    parser.add_argument('--pretty', action='store_true',
                       help='Pretty print JSON output')
    
    args = parser.parse_args()
    
    generator = WorkflowGenerator()
    
    # Generate workflow
    if args.template:
        if args.template in generator.templates:
            workflow = generator.templates[args.template](args.name)
        else:
            print(f"❌ Error: Template '{args.template}' not found")
            sys.exit(1)
    else:
        # Create minimal workflow
        manual_trigger = generator.create_node(
            name="Start",
            node_type="n8n-nodes-base.manualTrigger",
            position=(250, 300)
        )
        workflow = generator.create_workflow(
            name=args.name,
            nodes=[manual_trigger],
            connections={}
        )
    
    # Write to file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.pretty:
                json.dump(workflow, f, indent=2)
            else:
                json.dump(workflow, f)
        
        print(f"✅ Workflow generated: {args.output}")
        print(f"   Name: {workflow['name']}")
        print(f"   Nodes: {len(workflow['nodes'])}")
        print(f"   Connections: {len(workflow['connections'])}")
        
    except IOError as e:
        print(f"❌ Error writing file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
