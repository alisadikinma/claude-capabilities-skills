#!/usr/bin/env python3
"""
n8n Template Finder
Search and discover n8n workflow templates using MCP tools.

Usage:
    python template_finder.py --query "email automation"
    python template_finder.py --task "email_automation"
    python template_finder.py --category "marketing" --complexity "simple"
    python template_finder.py --template-id 5230
"""

import json
import sys
import argparse
from typing import Dict, List, Any, Optional

class TemplateFinder:
    """Helper for searching n8n workflow templates."""
    
    def __init__(self):
        self.categories = [
            "marketing", "sales", "customer-support", "devops",
            "data-sync", "content", "automation", "integration"
        ]
        self.complexity_levels = ["simple", "medium", "complex"]
        self.tasks = [
            "email_automation", "social_media", "crm_integration",
            "content_generation", "job_automation", "data_processing",
            "api_integration", "webhook_processing"
        ]
    
    def search_by_text(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search templates by text query.
        
        MCP Tool: search_templates(query, limit)
        """
        return {
            "mcp_tool": "search_templates",
            "parameters": {
                "query": query,
                "limit": limit,
                "fields": ["id", "name", "description", "nodes", "views"]
            },
            "description": f"Search for '{query}' in template names and descriptions"
        }
    
    def search_by_metadata(
        self,
        category: Optional[str] = None,
        complexity: Optional[str] = None,
        max_setup_minutes: Optional[int] = None,
        required_service: Optional[str] = None,
        target_audience: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search templates by AI-generated metadata.
        
        MCP Tool: search_templates_by_metadata(...)
        """
        params = {"limit": limit}
        
        if category:
            params["category"] = category
        if complexity:
            params["complexity"] = complexity
        if max_setup_minutes:
            params["maxSetupMinutes"] = max_setup_minutes
        if required_service:
            params["requiredService"] = required_service
        if target_audience:
            params["targetAudience"] = target_audience
        
        return {
            "mcp_tool": "search_templates_by_metadata",
            "parameters": params,
            "description": "Smart filter using AI metadata"
        }
    
    def get_for_task(self, task: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get curated templates for specific task.
        
        MCP Tool: get_templates_for_task(task, limit)
        """
        if task not in self.tasks:
            print(f"⚠️  Warning: '{task}' not in predefined tasks")
            print(f"   Available: {', '.join(self.tasks)}")
        
        return {
            "mcp_tool": "get_templates_for_task",
            "parameters": {
                "task": task,
                "limit": limit
            },
            "description": f"Get curated templates for {task}"
        }
    
    def get_by_id(self, template_id: int, mode: str = "full") -> Dict[str, Any]:
        """
        Get specific template by ID.
        
        MCP Tool: get_template(templateId, mode)
        Modes: nodes_only, structure, full
        """
        return {
            "mcp_tool": "get_template",
            "parameters": {
                "templateId": template_id,
                "mode": mode
            },
            "description": f"Retrieve template #{template_id} with {mode} details"
        }
    
    def list_node_templates(self, node_types: List[str], limit: int = 10) -> Dict[str, Any]:
        """
        Find templates using specific nodes.
        
        MCP Tool: list_node_templates(nodeTypes, limit)
        """
        return {
            "mcp_tool": "list_node_templates",
            "parameters": {
                "nodeTypes": node_types,
                "limit": limit
            },
            "description": f"Find templates using {', '.join(node_types)}"
        }
    
    def print_usage_examples(self):
        """Print usage examples."""
        examples = """
MCP Tool Call Examples:
========================

1. Search by Text:
   search_templates({
     query: "email marketing",
     limit: 20
   })

2. Search by Metadata:
   search_templates_by_metadata({
     category: "marketing",
     complexity: "simple",
     maxSetupMinutes: 30,
     limit: 20
   })

3. Get Templates for Task:
   get_templates_for_task({
     task: "email_automation",
     limit: 10
   })

4. Get Specific Template:
   get_template({
     templateId: 5230,
     mode: "full"
   })

5. Find Templates by Nodes:
   list_node_templates({
     nodeTypes: ["n8n-nodes-base.openAi", "n8n-nodes-base.gmail"],
     limit: 10
   })

Popular Templates:
==================
#5230 - Content Farming (10 WordPress posts/day, $21/month)
#5676 - HubSpot Customer Onboarding
#5841 - Daily AI Social Media Posts
#2549 - Google Analytics Reporting
#6927 - Multi-Board Job Aggregation
#3363 - AI Interview Scheduling
#7134 - Email Marketing with Brevo

Template Discovery Strategy:
============================
1. Start with task-based search (get_templates_for_task)
2. Refine with metadata filters
3. Check node-specific templates if integrating specific services
4. Retrieve full template JSON for customization
5. Validate before deployment

Categories: {categories}
Complexity: {complexity}
Tasks: {tasks}
""".format(
            categories=", ".join(self.categories),
            complexity=", ".join(self.complexity_levels),
            tasks=", ".join(self.tasks)
        )
        print(examples)

def format_query_output(query_dict: Dict[str, Any]) -> str:
    """Format query dictionary as readable output."""
    output = f"\n🔍 {query_dict['description']}\n"
    output += f"\n📋 MCP Tool: {query_dict['mcp_tool']}\n"
    output += f"\n⚙️  Parameters:\n"
    output += json.dumps(query_dict['parameters'], indent=2)
    output += "\n\n💡 To execute in Claude, call:\n"
    output += f"   {query_dict['mcp_tool']}({json.dumps(query_dict['parameters'])})\n"
    return output

def main():
    parser = argparse.ArgumentParser(
        description='Find n8n workflow templates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "email automation"
  %(prog)s --task "email_automation"
  %(prog)s --category "marketing" --complexity "simple"
  %(prog)s --template-id 5230 --mode full
  %(prog)s --nodes "n8n-nodes-base.openAi" "n8n-nodes-base.gmail"
  %(prog)s --examples
        """
    )
    
    parser.add_argument('--query', help='Text search query')
    parser.add_argument('--task', help='Task type (email_automation, social_media, etc.)')
    parser.add_argument('--category', help='Template category')
    parser.add_argument('--complexity', choices=['simple', 'medium', 'complex'], 
                       help='Complexity level')
    parser.add_argument('--max-setup-minutes', type=int, 
                       help='Maximum setup time in minutes')
    parser.add_argument('--service', help='Required service (openai, slack, etc.)')
    parser.add_argument('--audience', help='Target audience')
    parser.add_argument('--template-id', type=int, help='Specific template ID')
    parser.add_argument('--mode', choices=['nodes_only', 'structure', 'full'],
                       default='full', help='Template retrieval mode')
    parser.add_argument('--nodes', nargs='+', help='Node types to search for')
    parser.add_argument('--limit', type=int, default=10, 
                       help='Maximum results (default: 10)')
    parser.add_argument('--examples', action='store_true',
                       help='Show usage examples')
    
    args = parser.parse_args()
    
    finder = TemplateFinder()
    
    # Show examples
    if args.examples:
        finder.print_usage_examples()
        sys.exit(0)
    
    # Build query based on arguments
    query_dict = None
    
    if args.template_id:
        query_dict = finder.get_by_id(args.template_id, args.mode)
    
    elif args.query:
        query_dict = finder.search_by_text(args.query, args.limit)
    
    elif args.task:
        query_dict = finder.get_for_task(args.task, args.limit)
    
    elif args.nodes:
        query_dict = finder.list_node_templates(args.nodes, args.limit)
    
    elif any([args.category, args.complexity, args.max_setup_minutes, 
              args.service, args.audience]):
        query_dict = finder.search_by_metadata(
            category=args.category,
            complexity=args.complexity,
            max_setup_minutes=args.max_setup_minutes,
            required_service=args.service,
            target_audience=args.audience,
            limit=args.limit
        )
    
    else:
        parser.print_help()
        sys.exit(1)
    
    # Print query
    print(format_query_output(query_dict))

if __name__ == '__main__':
    main()
