#!/usr/bin/env python3
"""
MobileKit New Project Command
Creates a new mobile project with the specified template and configuration.
"""

import os
import sys
import argparse
import yaml
from pathlib import Path

def create_project(name, project_type, template_dir=None):
    """Create a new mobile project"""

    project_path = Path(name)
    if project_path.exists():
        print(f"Error: Directory '{name}' already exists")
        return False

    # Create project directory
    project_path.mkdir(parents=True)

    # Copy template files
    if template_dir:
        template_path = Path(template_dir) / project_type
        if template_path.exists():
            copy_template_files(template_path, project_path)

    # Create initial configuration
    create_project_config(project_path, name, project_type)

    print(f"✅ Created new {project_type} project: {name}")
    return True

def copy_template_files(template_path, project_path):
    """Copy template files to project directory"""
    import shutil

    for item in template_path.rglob('*'):
        if item.is_file():
            relative_path = item.relative_to(template_path)
            dest_path = project_path / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_path)

def create_project_config(project_path, name, project_type):
    """Create project configuration file"""
    config = {
        'project': {
            'name': name,
            'type': project_type,
            'version': '1.0.0',
            'created_with': 'MobileKit'
        },
        'mobilekit': {
            'version': '1.0.0',
            'agents_enabled': True,
            'workflows_enabled': True
        }
    }

    config_path = project_path / 'mobilekit.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(description='Create new MobileKit project')
    parser.add_argument('name', help='Project name')
    parser.add_argument('--type', choices=['flutter', 'ios-swift', 'react-native'],
                       required=True, help='Project type')
    parser.add_argument('--template', help='Custom template directory')

    args = parser.parse_args()

    template_dir = args.template or Path(__file__).parent.parent / 'templates'

    success = create_project(args.name, args.type, template_dir)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()