#!/usr/bin/env python3
"""
Project Scaffolder - Web_Architect_Pro
Generate project boilerplate for common web stacks

Usage:
    python project_scaffolder.py nextjs-fastapi my-project
    python project_scaffolder.py vue-laravel my-project
"""

import os
import sys
import subprocess
from pathlib import Path

TEMPLATES = {
    "nextjs-fastapi": {
        "frontend": {
            "commands": [
                "npx create-next-app@latest {name}-frontend --typescript --tailwind --app",
                "cd {name}-frontend && npm install zustand axios @tanstack/react-query",
            ],
        },
        "backend": {
            "commands": [
                "mkdir -p {name}-backend/app",
                "cd {name}-backend && python -m venv venv",
            ],
            "files": {
                "requirements.txt": "fastapi==0.104.1\nuvicorn[standard]==0.24.0\nsqlalchemy==2.0.23",
                "app/main.py": '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is running"}
''',
            }
        }
    },
}

def scaffold_project(template: str, project_name: str):
    if template not in TEMPLATES:
        print(f"Unknown template: {template}")
        sys.exit(1)
    
    print(f"\nScaffolding {template} project: {project_name}\n")
    
    project_path = Path.cwd() / project_name
    if project_path.exists():
        print(f"Directory {project_name} already exists")
        sys.exit(1)
    
    project_path.mkdir()
    print(f"✓ Created: {project_name}\n")
    
    config = TEMPLATES[template]
    
    # Frontend
    print("Setting up frontend...")
    for cmd in config["frontend"]["commands"]:
        print(f"  Running: {cmd.format(name=project_name)}")
        subprocess.run(cmd.format(name=project_name), shell=True, check=True)
    
    # Backend
    print("\nSetting up backend...")
    backend_path = project_path / f"{project_name}-backend"
    backend_path.mkdir(exist_ok=True)
    
    for cmd in config["backend"]["commands"]:
        print(f"  Running: {cmd.format(name=project_name)}")
        subprocess.run(cmd.format(name=project_name), shell=True, check=True)
    
    if "files" in config["backend"]:
        for file_path, content in config["backend"]["files"].items():
            full_path = backend_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content.strip())
            print(f"  ✓ Created: {file_path}")
    
    print(f"\n✅ Project {project_name} created!")

def main():
    if len(sys.argv) < 3:
        print("Usage: python project_scaffolder.py <template> <project-name>")
        print(f"\nTemplates: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)
    
    scaffold_project(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
