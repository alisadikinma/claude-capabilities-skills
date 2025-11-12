#!/usr/bin/env python3
"""
Architecture Diagram Generator
Generates Mermaid diagrams from YAML configuration for system architecture documentation.

Usage:
    python diagram_generator.py --config architecture.yaml
    python diagram_generator.py --config architecture.yaml --output diagrams/
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List


class DiagramGenerator:
    """Generate Mermaid diagrams from architecture configuration."""
    
    def __init__(self, config_path: str, output_dir: str = '.'):
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load architecture configuration."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def generate_all(self):
        """Generate all diagram types."""
        print(f"📐 Generating architecture diagrams from {self.config_path}\n")
        
        # System context diagram (C4 Level 1)
        if 'system_context' in self.config:
            self.generate_system_context()
        
        # Container diagram (C4 Level 2)
        if 'containers' in self.config:
            self.generate_container_diagram()
        
        # Component diagram (C4 Level 3)
        if 'components' in self.config:
            self.generate_component_diagram()
        
        # Sequence diagrams
        if 'sequences' in self.config:
            self.generate_sequence_diagrams()
        
        # Entity relationship diagrams
        if 'data_model' in self.config:
            self.generate_erd()
        
        # Deployment diagram
        if 'deployment' in self.config:
            self.generate_deployment_diagram()
        
        print(f"\n✅ Diagrams generated in {self.output_dir}/")
    
    def generate_system_context(self):
        """Generate C4 System Context diagram."""
        context = self.config['system_context']
        
        diagram = """graph TB
    %% System Context Diagram (C4 Level 1)
    
"""
        
        # External actors
        if 'actors' in context:
            for actor in context['actors']:
                actor_id = actor['id']
                actor_name = actor['name']
                diagram += f"    {actor_id}[<b>{actor_name}</b><br/>External Actor]\n"
        
        # System
        system = context['system']
        system_id = system['id']
        system_name = system['name']
        diagram += f"\n    {system_id}[<b>{system_name}</b><br/>System]\n"
        
        # External systems
        if 'external_systems' in context:
            diagram += "\n"
            for ext_sys in context['external_systems']:
                ext_id = ext_sys['id']
                ext_name = ext_sys['name']
                diagram += f"    {ext_id}[<b>{ext_name}</b><br/>External System]\n"
        
        # Relationships
        diagram += "\n"
        for rel in context['relationships']:
            from_id = rel['from']
            to_id = rel['to']
            label = rel['label']
            diagram += f"    {from_id} -->|{label}| {to_id}\n"
        
        # Styling
        diagram += """
    classDef system fill:#1168bd,stroke:#0b4884,color:#fff
    classDef external fill:#999,stroke:#666,color:#fff
    
"""
        diagram += f"    class {system_id} system\n"
        
        if 'actors' in context:
            actor_ids = ','.join([a['id'] for a in context['actors']])
            diagram += f"    class {actor_ids} external\n"
        
        if 'external_systems' in context:
            ext_ids = ','.join([e['id'] for e in context['external_systems']])
            diagram += f"    class {ext_ids} external\n"
        
        output_path = self.output_dir / '01_system_context.md'
        self._save_diagram(output_path, diagram, "System Context Diagram")
        print(f"✓ Generated: {output_path}")
    
    def generate_container_diagram(self):
        """Generate C4 Container diagram."""
        containers = self.config['containers']
        
        diagram = """graph TB
    %% Container Diagram (C4 Level 2)
    
    subgraph system[System]
"""
        
        # Containers
        for container in containers:
            container_id = container['id']
            container_name = container['name']
            tech = container.get('technology', '')
            
            diagram += f"        {container_id}[<b>{container_name}</b><br/>{tech}]\n"
        
        diagram += "    end\n\n"
        
        # External systems
        if 'external_systems' in self.config:
            for ext_sys in self.config['external_systems']:
                ext_id = ext_sys['id']
                ext_name = ext_sys['name']
                diagram += f"    {ext_id}[<b>{ext_name}</b><br/>External]\n"
        
        # Relationships
        diagram += "\n"
        if 'relationships' in self.config:
            for rel in self.config['relationships']:
                from_id = rel['from']
                to_id = rel['to']
                label = rel.get('label', '')
                tech = rel.get('technology', '')
                
                rel_label = f"{label}<br/>{tech}" if tech else label
                diagram += f"    {from_id} -->|{rel_label}| {to_id}\n"
        
        output_path = self.output_dir / '02_container_diagram.md'
        self._save_diagram(output_path, diagram, "Container Diagram")
        print(f"✓ Generated: {output_path}")
    
    def generate_component_diagram(self):
        """Generate C4 Component diagram."""
        components = self.config['components']
        
        for service_name, service_data in components.items():
            diagram = f"""graph TB
    %% Component Diagram - {service_name}
    
    subgraph {service_name}["{service_name}"]
"""
            
            # Components
            for component in service_data['components']:
                comp_id = component['id']
                comp_name = component['name']
                comp_type = component.get('type', 'Component')
                
                diagram += f"        {comp_id}[<b>{comp_name}</b><br/>{comp_type}]\n"
            
            diagram += "    end\n\n"
            
            # External dependencies
            if 'external_dependencies' in service_data:
                for dep in service_data['external_dependencies']:
                    dep_id = dep['id']
                    dep_name = dep['name']
                    diagram += f"    {dep_id}[<b>{dep_name}</b><br/>External]\n"
            
            # Relationships
            diagram += "\n"
            if 'relationships' in service_data:
                for rel in service_data['relationships']:
                    from_id = rel['from']
                    to_id = rel['to']
                    label = rel.get('label', '')
                    
                    diagram += f"    {from_id} -->|{label}| {to_id}\n"
            
            output_path = self.output_dir / f'03_component_{service_name.lower()}.md'
            self._save_diagram(output_path, diagram, f"Component Diagram - {service_name}")
            print(f"✓ Generated: {output_path}")
    
    def generate_sequence_diagrams(self):
        """Generate sequence diagrams for key flows."""
        sequences = self.config['sequences']
        
        for idx, sequence in enumerate(sequences):
            seq_name = sequence['name']
            
            diagram = f"""sequenceDiagram
    %% {seq_name}
    
"""
            
            # Participants
            if 'participants' in sequence:
                for participant in sequence['participants']:
                    diagram += f"    participant {participant}\n"
                diagram += "\n"
            
            # Steps
            for step in sequence['steps']:
                from_actor = step['from']
                to_actor = step['to']
                message = step['message']
                
                if step.get('type') == 'note':
                    diagram += f"    Note over {from_actor},{to_actor}: {message}\n"
                elif step.get('type') == 'async':
                    diagram += f"    {from_actor}-->>{to_actor}: {message}\n"
                else:
                    diagram += f"    {from_actor}->>{to_actor}: {message}\n"
            
            output_path = self.output_dir / f'04_sequence_{idx+1}_{seq_name.lower().replace(" ", "_")}.md'
            self._save_diagram(output_path, diagram, seq_name)
            print(f"✓ Generated: {output_path}")
    
    def generate_erd(self):
        """Generate Entity Relationship Diagram."""
        data_model = self.config['data_model']
        
        diagram = """erDiagram
    %% Entity Relationship Diagram
    
"""
        
        # Entities
        for entity in data_model['entities']:
            entity_name = entity['name']
            
            diagram += f"    {entity_name} {{\n"
            
            for field in entity['fields']:
                field_name = field['name']
                field_type = field['type']
                constraints = field.get('constraints', '')
                
                diagram += f"        {field_type} {field_name} {constraints}\n"
            
            diagram += "    }\n\n"
        
        # Relationships
        if 'relationships' in data_model:
            for rel in data_model['relationships']:
                from_entity = rel['from']
                to_entity = rel['to']
                cardinality = rel['cardinality']
                label = rel.get('label', '')
                
                diagram += f"    {from_entity} {cardinality} {to_entity} : {label}\n"
        
        output_path = self.output_dir / '05_data_model.md'
        self._save_diagram(output_path, diagram, "Data Model (ERD)")
        print(f"✓ Generated: {output_path}")
    
    def generate_deployment_diagram(self):
        """Generate deployment/infrastructure diagram."""
        deployment = self.config['deployment']
        
        diagram = """graph TB
    %% Deployment Diagram
    
"""
        
        # Cloud provider
        cloud = deployment.get('cloud_provider', 'Cloud')
        diagram += f"    subgraph {cloud}[{cloud}]\n"
        
        # Regions
        for region in deployment['regions']:
            region_name = region['name']
            region_id = region['id']
            
            diagram += f"        subgraph {region_id}[{region_name}]\n"
            
            # Availability zones
            if 'availability_zones' in region:
                for az in region['availability_zones']:
                    az_name = az['name']
                    az_id = az['id']
                    
                    diagram += f"            subgraph {az_id}[{az_name}]\n"
                    
                    # Services
                    if 'services' in az:
                        for service in az['services']:
                            svc_id = service['id']
                            svc_name = service['name']
                            svc_type = service.get('type', '')
                            
                            diagram += f"                {svc_id}[{svc_name}<br/>{svc_type}]\n"
                    
                    diagram += "            end\n"
            
            diagram += "        end\n"
        
        diagram += "    end\n"
        
        # Connections
        if 'connections' in deployment:
            diagram += "\n"
            for conn in deployment['connections']:
                from_id = conn['from']
                to_id = conn['to']
                label = conn.get('label', '')
                
                diagram += f"    {from_id} -->|{label}| {to_id}\n"
        
        output_path = self.output_dir / '06_deployment.md'
        self._save_diagram(output_path, diagram, "Deployment Diagram")
        print(f"✓ Generated: {output_path}")
    
    def _save_diagram(self, output_path: Path, diagram: str, title: str):
        """Save diagram to file with markdown wrapper."""
        content = f"""# {title}

```mermaid
{diagram}```

Generated from: {self.config_path}
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate architecture diagrams')
    parser.add_argument('--config', required=True, help='Path to architecture config (YAML)')
    parser.add_argument('--output', default='.', help='Output directory for diagrams')
    
    args = parser.parse_args()
    
    generator = DiagramGenerator(args.config, args.output)
    generator.generate_all()


if __name__ == '__main__':
    main()
