#!/usr/bin/env python3
"""
MobileKit CLI - Main entry point for MobileKit commands
"""

import os
import sys
import argparse
from pathlib import Path

# Add commands directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'commands'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'orchestrator'))

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='MobileKit - AI-Powered Mobile Development Toolkit',
        prog='mk'
    )

    parser.add_argument('--version', action='version', version='MobileKit 1.0.0')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # New project command
    new_parser = subparsers.add_parser('new', help='Create new mobile project')
    new_parser.add_argument('name', help='Project name')
    new_parser.add_argument('--type', choices=['flutter', 'ios-swift', 'react-native'],
                           required=True, help='Project type')
    new_parser.add_argument('--template', help='Custom template directory')

    # Generate feature command
    generate_parser = subparsers.add_parser('generate', help='Generate new feature')
    generate_parser.add_argument('name', help='Feature name')
    generate_parser.add_argument('--type', choices=['crud', 'ui', 'service', 'widget'],
                                default='crud', help='Feature type')
    generate_parser.add_argument('--project', default='.', help='Project path')

    # Run tests command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    test_parser.add_argument('--devices', help='Target devices (comma-separated)')
    test_parser.add_argument('--project', default='.', help='Project path')

    # Review code command
    review_parser = subparsers.add_parser('review', help='Review code changes')
    review_parser.add_argument('--branch', help='Branch to review')
    review_parser.add_argument('--files', help='Specific files to review')
    review_parser.add_argument('--project', default='.', help='Project path')

    # Build release command
    build_parser = subparsers.add_parser('build', help='Build for release')
    build_parser.add_argument('--platform', choices=['ios', 'android', 'all'],
                             required=True, help='Target platform')
    build_parser.add_argument('--target', help='Build target (app-store, play-store, etc.)')
    build_parser.add_argument('--project', default='.', help='Project path')

    # Debug crash command
    debug_parser = subparsers.add_parser('debug', help='Debug crashes and issues')
    debug_parser.add_argument('--crash-log', help='Path to crash log file')
    debug_parser.add_argument('--device', help='Target device')
    debug_parser.add_argument('--project', default='.', help='Project path')

    # Workflow commands
    workflow_parser = subparsers.add_parser('workflow', help='Manage workflows')
    workflow_subparsers = workflow_parser.add_subparsers(dest='workflow_command')

    run_workflow_parser = workflow_subparsers.add_parser('run', help='Run workflow')
    run_workflow_parser.add_argument('workflow_name', help='Workflow to run')
    run_workflow_parser.add_argument('--project', default='.', help='Project path')

    list_workflow_parser = workflow_subparsers.add_parser('list', help='List available workflows')

    # Config commands
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_subparsers = config_parser.add_subparsers(dest='config_command')

    set_config_parser = config_subparsers.add_parser('set', help='Set configuration value')
    set_config_parser.add_argument('key', help='Configuration key')
    set_config_parser.add_argument('value', help='Configuration value')

    get_config_parser = config_subparsers.add_parser('get', help='Get configuration value')
    get_config_parser.add_argument('key', help='Configuration key')

    # Agent commands
    agent_parser = subparsers.add_parser('agent', help='Manage agents')
    agent_subparsers = agent_parser.add_subparsers(dest='agent_command')

    list_agents_parser = agent_subparsers.add_parser('list', help='List available agents')
    run_agent_parser = agent_subparsers.add_parser('run', help='Run specific agent')
    run_agent_parser.add_argument('agent_name', help='Agent to run')
    run_agent_parser.add_argument('--input', help='Input data (JSON string)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        # Execute the appropriate command
        if args.command == 'new':
            from new_project import main as new_main
            sys.argv = ['new-project.py', args.name, '--type', args.type]
            if args.template:
                sys.argv.extend(['--template', args.template])
            return new_main()

        elif args.command == 'generate':
            from generate_feature import main as generate_main
            sys.argv = ['generate-feature.py', args.name, '--type', args.type,
                       '--project', args.project]
            return generate_main()

        elif args.command == 'test':
            from run_tests import main as test_main
            sys.argv = ['run-tests.py']
            if args.coverage:
                sys.argv.append('--coverage')
            if args.devices:
                sys.argv.extend(['--devices', args.devices])
            sys.argv.extend(['--project', args.project])
            return test_main()

        elif args.command == 'review':
            from review_code import main as review_main
            sys.argv = ['review-code.py']
            if args.branch:
                sys.argv.extend(['--branch', args.branch])
            if args.files:
                sys.argv.extend(['--files', args.files])
            sys.argv.extend(['--project', args.project])
            return review_main()

        elif args.command == 'build':
            from build_release import main as build_main
            sys.argv = ['build-release.py', '--platform', args.platform]
            if args.target:
                sys.argv.extend(['--target', args.target])
            sys.argv.extend(['--project', args.project])
            return build_main()

        elif args.command == 'debug':
            from debug_crash import main as debug_main
            sys.argv = ['debug-crash.py']
            if args.crash_log:
                sys.argv.extend(['--crash-log', args.crash_log])
            if args.device:
                sys.argv.extend(['--device', args.device])
            sys.argv.extend(['--project', args.project])
            return debug_main()

        elif args.command == 'workflow':
            return handle_workflow_command(args)

        elif args.command == 'config':
            return handle_config_command(args)

        elif args.command == 'agent':
            return handle_agent_command(args)

        else:
            print(f"Unknown command: {args.command}")
            return 1

    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        return 1

def handle_workflow_command(args):
    """Handle workflow-related commands"""
    if args.workflow_command == 'run':
        from workflow_engine import WorkflowEngine
        engine = WorkflowEngine(Path(args.project))
        result = engine.run_workflow(args.workflow_name)
        print(f"Workflow '{args.workflow_name}' completed: {result}")
        return 0
    elif args.workflow_command == 'list':
        workflows_dir = Path(args.project) / 'workflows'
        if workflows_dir.exists():
            workflows = list(workflows_dir.glob('*.yaml'))
            print("Available workflows:")
            for workflow in workflows:
                print(f"  - {workflow.stem}")
        else:
            print("No workflows found")
        return 0
    else:
        print("Unknown workflow command")
        return 1

def handle_config_command(args):
    """Handle configuration commands"""
    config_file = Path('mobilekit.yaml')

    if args.config_command == 'set':
        # Implementation for setting config values
        print(f"Setting {args.key} = {args.value}")
        return 0
    elif args.config_command == 'get':
        # Implementation for getting config values
        print(f"Getting value for {args.key}")
        return 0
    else:
        print("Unknown config command")
        return 1

def handle_agent_command(args):
    """Handle agent-related commands"""
    from agent_manager import AgentManager

    agents_dir = Path(__file__).parent.parent / 'agents'
    agent_manager = AgentManager(agents_dir)

    if args.agent_command == 'list':
        agents = agent_manager.list_agents()
        print("Available agents:")
        for agent in agents:
            print(f"  - {agent}")
        return 0
    elif args.agent_command == 'run':
        import json
        input_data = {}
        if args.input:
            input_data = json.loads(args.input)

        result = agent_manager.execute_agent(args.agent_name, input_data)
        print(f"Agent execution result: {result}")
        return 0
    else:
        print("Unknown agent command")
        return 1

if __name__ == '__main__':
    sys.exit(main())