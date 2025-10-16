# ClaudeKit Commands for Agent Systems

## Essential ClaudeKit CLI Commands

### Project Creation & Management
```bash
# Create new project with Engineer Kit (ideal for agent systems)
ck new --dir my-project --kit engineer

# Update existing project with latest kit features
ck update --kit engineer
```

### Agent System Development Commands

#### Project Structure Commands
- `ck init` - Initialize a new ClaudeKit project in current directory
- `ck generate [template]` - Generate code from templates (agent, api, ui, etc.)
- `ck scaffold [feature]` - Create scaffolding for new features

#### Development Workflow Commands
- `ck dev` - Start development server
- `ck build` - Build project for production
- `ck test` - Run test suite
- `ck lint` - Run code linting and formatting
- `ck clean` - Clean build artifacts and cache

#### Agent-Specific Commands
- `ck agent:create [name]` - Create new agent with template
- `ck agent:deploy [name]` - Deploy agent to specified environment
- `ck agent:test [name]` - Run agent-specific tests
- `ck agent:logs [name]` - View agent execution logs

#### Configuration Commands
- `ck config:set [key] [value]` - Set configuration value
- `ck config:get [key]` - Get configuration value
- `ck config:list` - List all configuration settings
- `ck env:load [environment]` - Load environment-specific configuration

#### Package Management Commands
- `ck add [package]` - Add new dependency
- `ck remove [package]` - Remove dependency
- `ck update` - Update all dependencies
- `ck outdated` - Check for outdated dependencies

#### Documentation Commands
- `ck docs:generate` - Generate API documentation
- `ck docs:serve` - Start documentation server
- `ck readme:update` - Update README with project information

## Agent System Templates

### Engineer Kit Features
- Full-stack development framework
- API integration templates
- Database schema management
- Authentication & authorization
- Testing frameworks setup
- CI/CD pipeline templates

### Available Templates for Agent Systems
- `agent-template` - Basic agent structure with system prompts
- `api-agent` - API integration agent with endpoint management
- `workflow-agent` - Multi-step workflow automation agent
- `data-agent` - Data processing and analysis agent
- `ui-agent` - User interface interaction agent

## Best Practices for Agent Development

1. **Project Initialization**: Always use `ck new --dir [name] --kit engineer` for new agent projects
2. **Template Usage**: Start with appropriate agent template for faster development
3. **Environment Management**: Use `ck env` commands for different deployment environments
4. **Testing**: Run `ck test` regularly during development
5. **Documentation**: Keep docs updated with `ck docs:generate`

## Integration with Existing Agent Systems

These ClaudeKit commands are designed to work seamlessly with existing agent system architectures:

- **Solo Expansion System**: Use for building scalable solo developer businesses
- **Mobile Development Agent**: Template for mobile app development workflows
- **Multi-Agent Systems**: Commands for managing multiple coordinated agents

## Additional Resources

- Official documentation: https://claudekit.cc
- GitHub repository: Search for "claudekit" repositories
- Community templates and examples
- Plugin ecosystem for extended functionality

---
*Last updated: Focus on agent system commands and templates for solo developers and expansion systems.*