#!/usr/bin/env python3
"""
MobileKit Context Loader
Loads and manages project context for mobile development workflows.
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional

class ContextLoader:
    """Loads and manages mobile project context"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.context = {}

    def load_project_context(self) -> Dict[str, Any]:
        """Load complete project context"""
        self.context = {
            'project_info': self.load_project_info(),
            'mobile_context': self.load_mobile_context(),
            'build_configuration': self.load_build_configuration(),
            'dependencies': self.load_dependencies(),
            'platform_specific': self.load_platform_specific_context()
        }

        return self.context

    def load_project_info(self) -> Dict[str, Any]:
        """Load basic project information"""
        config_file = self.project_path / 'mobilekit.yaml'

        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)

        # Try to detect project type from existing files
        return self.detect_project_type()

    def detect_project_type(self) -> Dict[str, Any]:
        """Detect project type from existing files"""
        project_path = self.project_path

        if (project_path / 'pubspec.yaml').exists():
            return {
                'project': {
                    'type': 'flutter',
                    'language': 'dart',
                    'framework': 'flutter'
                }
            }
        elif (project_path / 'package.json').exists():
            with open(project_path / 'package.json', 'r') as f:
                package_json = json.load(f)
                if 'react-native' in package_json.get('dependencies', {}):
                    return {
                        'project': {
                            'type': 'react-native',
                            'language': 'typescript',
                            'framework': 'react-native'
                        }
                    }
        elif (project_path / '.xcodeproj').exists():
            return {
                'project': {
                    'type': 'ios-swift',
                    'language': 'swift',
                    'framework': 'ios'
                }
            }

        return {'project': {'type': 'unknown'}}

    def load_mobile_context(self) -> Dict[str, Any]:
        """Load mobile-specific context from MOBILE_CONTEXT.md"""
        context_file = self.project_path / 'MOBILE_CONTEXT.md'

        if context_file.exists():
            with open(context_file, 'r') as f:
                content = f.read()
            return self.parse_mobile_context(content)

        return self.get_default_mobile_context()

    def parse_mobile_context(self, content: str) -> Dict[str, Any]:
        """Parse mobile context from markdown content"""
        context = {}
        current_section = None

        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                current_section = line[2:].lower().replace(' ', '_')
                context[current_section] = []
            elif current_section and line.startswith('- '):
                context[current_section].append(line[2:])

        return context

    def get_default_mobile_context(self) -> Dict[str, Any]:
        """Get default mobile context for new projects"""
        return {
            'target_platforms': ['iOS', 'Android'],
            'min_sdk_versions': {'iOS': '15.0', 'Android': '21'},
            'supported_devices': ['iPhone', 'iPad', 'Android Phone', 'Android Tablet'],
            'ui_framework': 'Material Design',
            'architecture_pattern': 'MVVM'
        }

    def load_build_configuration(self) -> Dict[str, Any]:
        """Load build configuration based on project type"""
        project_info = self.load_project_info()
        project_type = project_info.get('project', {}).get('type')

        if project_type == 'flutter':
            return self.load_flutter_build_config()
        elif project_type == 'ios-swift':
            return self.load_ios_build_config()
        elif project_type == 'react-native':
            return self.load_react_native_build_config()

        return {}

    def load_flutter_build_config(self) -> Dict[str, Any]:
        """Load Flutter build configuration"""
        pubspec_file = self.project_path / 'pubspec.yaml'

        if pubspec_file.exists():
            with open(pubspec_file, 'r') as f:
                pubspec = yaml.safe_load(f)

            return {
                'flutter_version': pubspec.get('environment', {}).get('flutter'),
                'dart_version': pubspec.get('environment', {}).get('sdk'),
                'dependencies': list(pubspec.get('dependencies', {}).keys()),
                'dev_dependencies': list(pubspec.get('dev_dependencies', {}).keys())
            }

        return {}

    def load_ios_build_config(self) -> Dict[str, Any]:
        """Load iOS build configuration"""
        # Parse Xcode project files if they exist
        return {
            'xcode_version': '14.0+',
            'ios_deployment_target': '15.0+',
            'swift_version': '5.7+'
        }

    def load_react_native_build_config(self) -> Dict[str, Any]:
        """Load React Native build configuration"""
        package_file = self.project_path / 'package.json'

        if package_file.exists():
            with open(package_file, 'r') as f:
                package_json = json.load(f)

            return {
                'react_version': package_json.get('dependencies', {}).get('react'),
                'react_native_version': package_json.get('dependencies', {}).get('react-native'),
                'dependencies': list(package_json.get('dependencies', {}).keys())
            }

        return {}

    def load_dependencies(self) -> Dict[str, Any]:
        """Load project dependencies"""
        build_config = self.load_build_configuration()
        return {
            'flutter': build_config.get('dependencies', []),
            'ios': build_config.get('dependencies', []),
            'react_native': build_config.get('dependencies', [])
        }

    def load_platform_specific_context(self) -> Dict[str, Any]:
        """Load platform-specific context and requirements"""
        project_info = self.load_project_info()
        project_type = project_info.get('project', {}).get('type')

        context = {
            'project_type': project_type,
            'platforms': self.get_target_platforms(project_type),
            'guidelines': self.get_platform_guidelines(project_type),
            'testing_framework': self.get_testing_framework(project_type)
        }

        return context

    def get_target_platforms(self, project_type: str) -> List[str]:
        """Get target platforms based on project type"""
        if project_type == 'flutter':
            return ['iOS', 'Android', 'Web', 'Desktop']
        elif project_type == 'ios-swift':
            return ['iOS', 'iPadOS', 'macOS']
        elif project_type == 'react-native':
            return ['iOS', 'Android']

        return []

    def get_platform_guidelines(self, project_type: str) -> Dict[str, str]:
        """Get platform design guidelines"""
        guidelines = {
            'ios': 'Apple Human Interface Guidelines',
            'android': 'Material Design Guidelines',
            'flutter': 'Material Design & Cupertino (iOS-style) Guidelines'
        }

        return {
            platform: guidelines.get(platform, 'Platform-specific guidelines')
            for platform in self.get_target_platforms(project_type)
        }

    def get_testing_framework(self, project_type: str) -> str:
        """Get recommended testing framework"""
        frameworks = {
            'flutter': 'Flutter Testing (Unit, Widget, Integration)',
            'ios-swift': 'XCTest (Unit, UI, Performance)',
            'react-native': 'Jest + React Native Testing Library'
        }

        return frameworks.get(project_type, 'Platform-specific testing framework')

    def update_context(self, updates: Dict[str, Any]):
        """Update context with new information"""
        self.context.update(updates)

    def get_context_value(self, key_path: str, default: Any = None) -> Any:
        """Get value from context using dot notation"""
        keys = key_path.split('.')
        value = self.context

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value