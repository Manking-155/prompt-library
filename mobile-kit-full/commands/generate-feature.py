#!/usr/bin/env python3
"""
MobileKit Generate Feature Command
Generates new features using AI agents and predefined templates.
"""

import os
import sys
import argparse
import yaml
from pathlib import Path

def generate_feature(name, feature_type, project_path):
    """Generate a new feature using MobileKit agents"""

    project_path = Path(project_path)
    if not project_path.exists():
        print(f"Error: Project path '{project_path}' does not exist")
        return False

    # Load project configuration
    config_path = project_path / 'mobilekit.yaml'
    if not config_path.exists():
        print(f"Error: mobilekit.yaml not found in project")
        return False

    with open(config_path) as f:
        config = yaml.safe_load(f)

    project_type = config['project']['type']

    # Create feature directory structure
    feature_path = create_feature_structure(project_path, name, feature_type, project_type)

    # Generate feature files
    generate_feature_files(feature_path, name, feature_type, project_type, config)

    # Update project files
    update_project_files(project_path, name, feature_type, project_type)

    print(f"✅ Generated feature '{name}' of type '{feature_type}'")
    return True

def create_feature_structure(project_path, name, feature_type, project_type):
    """Create directory structure for the feature"""

    feature_path = project_path / 'lib' / 'features' / name
    feature_path.mkdir(parents=True, exist_ok=True)

    # Create subdirectories based on project type
    if project_type == 'flutter':
        (feature_path / 'models').mkdir(exist_ok=True)
        (feature_path / 'views').mkdir(exist_ok=True)
        (feature_path / 'controllers').mkdir(exist_ok=True)
        (feature_path / 'services').mkdir(exist_ok=True)
    elif project_type == 'ios-swift':
        (feature_path / 'Models').mkdir(exist_ok=True)
        (feature_path / 'Views').mkdir(exist_ok=True)
        (feature_path / 'Controllers').mkdir(exist_ok=True)
        (feature_path / 'Services').mkdir(exist_ok=True)
    elif project_type == 'react-native':
        (feature_path / 'components').mkdir(exist_ok=True)
        (feature_path / 'screens').mkdir(exist_ok=True)
        (feature_path / 'services').mkdir(exist_ok=True)
        (feature_path / 'store').mkdir(exist_ok=True)

    return feature_path

def generate_feature_files(feature_path, name, feature_type, project_type, config):
    """Generate feature-specific files"""

    class_name = to_pascal_case(name)

    if project_type == 'flutter':
        generate_flutter_files(feature_path, class_name, feature_type)
    elif project_type == 'ios-swift':
        generate_ios_files(feature_path, class_name, feature_type)
    elif project_type == 'react-native':
        generate_react_native_files(feature_path, class_name, feature_type)

def generate_flutter_files(feature_path, class_name, feature_type):
    """Generate Flutter-specific files"""

    # Model file
    model_content = f'''class {class_name}Model {{
  final String id;
  final String name;
  final DateTime createdAt;

  {class_name}Model({{
    required this.id,
    required this.name,
    required this.createdAt,
  }});

  factory {class_name}.fromJson(Map<String, dynamic> json) {{
    return {class_name}Model(
      id: json['id'],
      name: json['name'],
      createdAt: DateTime.parse(json['createdAt']),
    );
  }}

  Map<String, dynamic> toJson() {{
    return {{
      'id': id,
      'name': name,
      'createdAt': createdAt.toIso8601String(),
    }};
  }}
}}
'''
    (feature_path / 'models' / f'{class_name.lower()}_model.dart').write_text(model_content)

def generate_ios_files(feature_path, class_name, feature_type):
    """Generate iOS Swift-specific files"""

    # Model file
    model_content = f'''import Foundation

struct {class_name}Model: Codable {{
    let id: String
    let name: String
    let createdAt: Date

    enum CodingKeys: String, CodingKey {{
        case id, name
        case createdAt = "created_at"
    }}
}}
'''
    (feature_path / 'Models' / f'{class_name}Model.swift').write_text(model_content)

def generate_react_native_files(feature_path, class_name, feature_type):
    """Generate React Native-specific files"""

    # Component file
    component_content = f'''import React from 'react';
import {{ View, Text, StyleSheet }} from 'react-native';

interface {class_name}Props {{
  name: string;
}}

const {class_name}: React.FC<{class_name}Props> = ({{ name }}) => {{
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{class_name}: {{name}}</Text>
    </View>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  }},
  title: {{
    fontSize: 18,
    fontWeight: 'bold',
  }},
}});

export default {class_name};
'''
    (feature_path / 'components' / f'{class_name}.tsx').write_text(component_content)

def to_pascal_case(name):
    """Convert string to PascalCase"""
    return ''.join(word.capitalize() for word in name.replace('-', '_').split('_'))

def update_project_files(project_path, name, feature_type, project_type):
    """Update project files to include the new feature"""

    # Update pubspec.yaml for Flutter projects
    if project_type == 'flutter':
        pubspec_path = project_path / 'pubspec.yaml'
        if pubspec_path.exists():
            # Add new dependencies if needed
            pass

def main():
    parser = argparse.ArgumentParser(description='Generate new feature with MobileKit')
    parser.add_argument('name', help='Feature name')
    parser.add_argument('--type', choices=['crud', 'ui', 'service', 'widget'],
                       default='crud', help='Feature type')
    parser.add_argument('--project', default='.', help='Project path')

    args = parser.parse_args()

    success = generate_feature(args.name, args.type, args.project)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()