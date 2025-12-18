#!/usr/bin/env python3
"""
n8n Workflow Validator
Validates n8n workflows using multiple validation levels.

Usage:
    python validate.py workflow.json --level full
    python validate.py workflow.json --level connections
    python validate.py workflow.json --autofix --preview
"""

import json
import sys
import argparse
from typing import Dict, List, Any, Tuple

def load_workflow(filepath: str) -> Dict[str, Any]:
    """Load workflow from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
        sys.exit(1)

def validate_structure(workflow: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate basic workflow structure."""
    errors = []
    
    # Check required top-level fields
    if 'nodes' not in workflow:
        errors.append("Missing 'nodes' array")
    if 'connections' not in workflow:
        errors.append("Missing 'connections' object")
    
    # Validate nodes
    if 'nodes' in workflow:
        if not isinstance(workflow['nodes'], list):
            errors.append("'nodes' must be an array")
        elif len(workflow['nodes']) == 0:
            errors.append("Workflow must have at least one node")
        else:
            for idx, node in enumerate(workflow['nodes']):
                if 'id' not in node:
                    errors.append(f"Node {idx} missing 'id' field")
                if 'name' not in node:
                    errors.append(f"Node {idx} missing 'name' field")
                if 'type' not in node:
                    errors.append(f"Node {idx} missing 'type' field")
                if 'typeVersion' not in node:
                    errors.append(f"Node {idx} missing 'typeVersion' field")
                if 'parameters' not in node:
                    errors.append(f"Node {idx} missing 'parameters' field")
    
    # Validate connections
    if 'connections' in workflow and not isinstance(workflow['connections'], dict):
        errors.append("'connections' must be an object")
    
    return (len(errors) == 0, errors)

def validate_connections(workflow: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate workflow connections."""
    errors = []
    nodes = {node['id']: node for node in workflow.get('nodes', [])}
    connections = workflow.get('connections', {})
    
    # Check all source nodes exist
    for source_id in connections.keys():
        if source_id not in nodes:
            errors.append(f"Connection source '{source_id}' not found in nodes")
    
    # Check all target nodes exist
    for source_id, outputs in connections.items():
        for output_type, connections_list in outputs.items():
            for connection_group in connections_list:
                for conn in connection_group:
                    target_id = conn.get('node')
                    if target_id and target_id not in nodes:
                        errors.append(f"Connection target '{target_id}' not found in nodes")
    
    # Check for at least one trigger node
    trigger_types = [
        'n8n-nodes-base.scheduleTrigger',
        'n8n-nodes-base.webhook',
        'n8n-nodes-base.manualTrigger',
        '@n8n/n8n-nodes-langchain.chatTrigger'
    ]
    has_trigger = any(
        node['type'] in trigger_types or 'Trigger' in node['type']
        for node in workflow.get('nodes', [])
    )
    if not has_trigger:
        errors.append("Workflow must have at least one trigger node")
    
    return (len(errors) == 0, errors)

def validate_expressions(workflow: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate n8n expressions in workflow."""
    errors = []
    
    def check_expressions(obj: Any, path: str = "") -> None:
        """Recursively check for expression syntax errors."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                check_expressions(value, f"{path}.{key}" if path else key)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                check_expressions(item, f"{path}[{idx}]")
        elif isinstance(obj, str):
            # Check for common expression errors
            if '={{' in obj:
                # Count braces
                open_count = obj.count('{{')
                close_count = obj.count('}}')
                if open_count != close_count:
                    errors.append(f"Mismatched braces in expression at {path}")
                
                # Check for common variables
                if '$json' not in obj and '$node' not in obj and '$input' not in obj:
                    # Might be using literal text, check if intentional
                    pass
    
    for node in workflow.get('nodes', []):
        check_expressions(node.get('parameters', {}), f"node:{node.get('name')}")
    
    return (len(errors) == 0, errors)

def validate_ai_nodes(workflow: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate AI Agent nodes (v2.17.0+)."""
    errors = []
    warnings = []
    
    # Find AI Agent nodes
    ai_agents = [
        node for node in workflow.get('nodes', [])
        if '@n8n/n8n-nodes-langchain.agent' in node['type']
    ]
    
    if not ai_agents:
        return (True, [])  # No AI agents, validation passes
    
    # Check connections for AI nodes
    connections = workflow.get('connections', {})
    for agent in ai_agents:
        agent_id = agent['id']
        
        # Check if language model is connected
        has_language_model = False
        for source_id, outputs in connections.items():
            for output_type, connections_list in outputs.items():
                if 'ai_languageModel' in output_type:
                    for conn_group in connections_list:
                        for conn in conn_group:
                            if conn.get('node') == agent_id:
                                has_language_model = True
                                break
        
        if not has_language_model:
            errors.append(
                f"AI Agent '{agent['name']}' must have language model "
                f"connected to ai_languageModel port"
            )
    
    return (len(errors) == 0, errors + warnings)

def full_validation(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """Run complete validation."""
    results = {
        'valid': True,
        'structure': {},
        'connections': {},
        'expressions': {},
        'ai_nodes': {},
        'summary': {}
    }
    
    # Structure validation
    structure_valid, structure_errors = validate_structure(workflow)
    results['structure'] = {
        'valid': structure_valid,
        'errors': structure_errors
    }
    
    # Connection validation
    connections_valid, connections_errors = validate_connections(workflow)
    results['connections'] = {
        'valid': connections_valid,
        'errors': connections_errors
    }
    
    # Expression validation
    expressions_valid, expressions_errors = validate_expressions(workflow)
    results['expressions'] = {
        'valid': expressions_valid,
        'errors': expressions_errors
    }
    
    # AI node validation
    ai_valid, ai_errors = validate_ai_nodes(workflow)
    results['ai_nodes'] = {
        'valid': ai_valid,
        'errors': ai_errors
    }
    
    # Overall validation
    results['valid'] = all([
        structure_valid,
        connections_valid,
        expressions_valid,
        ai_valid
    ])
    
    # Summary
    total_errors = sum([
        len(structure_errors),
        len(connections_errors),
        len(expressions_errors),
        len(ai_errors)
    ])
    
    results['summary'] = {
        'total_nodes': len(workflow.get('nodes', [])),
        'total_connections': sum(
            len(conns)
            for outputs in workflow.get('connections', {}).values()
            for connections_list in outputs.values()
            for conns in connections_list
        ),
        'total_errors': total_errors,
        'validation_passed': results['valid']
    }
    
    return results

def print_results(results: Dict[str, Any], verbose: bool = False) -> None:
    """Print validation results."""
    if results['valid']:
        print("\n✅ Workflow validation PASSED")
    else:
        print("\n❌ Workflow validation FAILED")
    
    print(f"\n📊 Summary:")
    print(f"   Nodes: {results['summary']['total_nodes']}")
    print(f"   Connections: {results['summary']['total_connections']}")
    print(f"   Errors: {results['summary']['total_errors']}")
    
    # Print errors by category
    categories = ['structure', 'connections', 'expressions', 'ai_nodes']
    for category in categories:
        if results[category]['errors']:
            print(f"\n❌ {category.title()} Errors:")
            for error in results[category]['errors']:
                print(f"   • {error}")
    
    if verbose:
        print(f"\n🔍 Detailed Results:")
        print(json.dumps(results, indent=2))

def main():
    parser = argparse.ArgumentParser(
        description='Validate n8n workflows',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s workflow.json
  %(prog)s workflow.json --level full
  %(prog)s workflow.json --level connections
  %(prog)s workflow.json --verbose
        """
    )
    
    parser.add_argument('workflow', help='Path to workflow JSON file')
    parser.add_argument(
        '--level',
        choices=['structure', 'connections', 'expressions', 'ai', 'full'],
        default='full',
        help='Validation level (default: full)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed results'
    )
    
    args = parser.parse_args()
    
    # Load workflow
    workflow = load_workflow(args.workflow)
    
    # Run validation based on level
    if args.level == 'structure':
        valid, errors = validate_structure(workflow)
        results = {'valid': valid, 'structure': {'errors': errors}}
    elif args.level == 'connections':
        valid, errors = validate_connections(workflow)
        results = {'valid': valid, 'connections': {'errors': errors}}
    elif args.level == 'expressions':
        valid, errors = validate_expressions(workflow)
        results = {'valid': valid, 'expressions': {'errors': errors}}
    elif args.level == 'ai':
        valid, errors = validate_ai_nodes(workflow)
        results = {'valid': valid, 'ai_nodes': {'errors': errors}}
    else:
        results = full_validation(workflow)
    
    # Print results
    print_results(results, args.verbose)
    
    # Exit with appropriate code
    sys.exit(0 if results['valid'] else 1)

if __name__ == '__main__':
    main()
