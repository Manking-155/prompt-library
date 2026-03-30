#!/usr/bin/env python3
"""
MobileKit Agent Manager
Manages and coordinates AI agents for mobile development workflows.
"""

import os
import yaml
import importlib
from pathlib import Path
from typing import Dict, List, Any, Optional

class AgentManager:
    """Manages AI agents for mobile development tasks"""

    def __init__(self, agents_dir: Path):
        self.agents_dir = agents_dir
        self.agents = {}
        self.load_agents()

    def load_agents(self):
        """Load all agent definitions from agents directory"""
        for agent_file in self.agents_dir.glob("*.md"):
            agent_name = agent_file.stem
            self.agents[agent_name] = self.load_agent_definition(agent_file)

    def load_agent_definition(self, agent_file: Path) -> Dict[str, Any]:
        """Load agent definition from markdown file"""
        with open(agent_file, 'r') as f:
            content = f.read()

        # Parse agent metadata from content
        metadata = self.parse_agent_metadata(content)

        return {
            'name': metadata.get('name', agent_file.stem),
            'role': metadata.get('role', ''),
            'description': metadata.get('description', ''),
            'capabilities': metadata.get('capabilities', []),
            'input_types': metadata.get('input_types', []),
            'output_types': metadata.get('output_types', []),
            'file_path': str(agent_file),
            'content': content
        }

    def parse_agent_metadata(self, content: str) -> Dict[str, Any]:
        """Parse metadata from agent markdown content"""
        metadata = {}
        lines = content.split('\n')

        for line in lines:
            if line.startswith('**Role**:'):
                metadata['role'] = line.replace('**Role**:', '').strip()
            elif line.startswith('**Input**:'):
                metadata['input_types'] = [item.strip() for item in
                    line.replace('**Input**:', '').strip().split(',')]
            elif line.startswith('**Output**:'):
                metadata['output_types'] = [item.strip() for item in
                    line.replace('**Output**:', '').strip().split(',')]
            elif line.startswith('**Description**:'):
                metadata['description'] = line.replace('**Description**:', '').strip()

        return metadata

    def get_agent(self, name: str) -> Optional[Dict[str, Any]]:
        """Get agent by name"""
        return self.agents.get(name)

    def get_agents_by_capability(self, capability: str) -> List[Dict[str, Any]]:
        """Get agents that have specific capability"""
        return [agent for agent in self.agents.values()
                if capability in agent.get('capabilities', [])]

    def list_agents(self) -> List[str]:
        """List all available agent names"""
        return list(self.agents.keys())

    def execute_agent(self, agent_name: str, input_data: Dict[str, Any],
                     context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute an agent with input data"""
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")

        # Prepare execution context
        execution_context = {
            'agent': agent,
            'input': input_data,
            'context': context or {},
            'working_directory': os.getcwd()
        }

        # Simulate agent execution (in real implementation, this would call AI APIs)
        result = self.simulate_agent_execution(execution_context)

        return result

    def simulate_agent_execution(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate agent execution for demonstration"""
        agent = context['agent']
        input_data = context['input']

        return {
            'agent_name': agent['name'],
            'agent_role': agent['role'],
            'input_received': input_data,
            'output': f"Processed by {agent['name']} based on {agent['role']}",
            'status': 'completed',
            'execution_time': 0.5
        }

    def create_agent_chain(self, workflow_definition: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a chain of agents based on workflow definition"""
        agent_chain = []

        for agent_name in workflow_definition.get('execution_order', []):
            agent = self.get_agent(agent_name)
            if agent:
                agent_chain.append(agent)
            else:
                print(f"Warning: Agent '{agent_name}' not found in workflow")

        return agent_chain

    def validate_workflow(self, workflow_definition: Dict[str, Any]) -> bool:
        """Validate that all agents in workflow exist"""
        required_agents = workflow_definition.get('execution_order', [])

        for agent_name in required_agents:
            if agent_name not in self.agents:
                print(f"Error: Required agent '{agent_name}' not found")
                return False

        return True