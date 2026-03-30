# MobileKit Agent Guide

MobileKit uses specialized AI agents to handle different aspects of mobile development. Each agent is optimized for specific tasks and follows mobile development best practices.

## Available Agents

### 1. Mobile Planner
**Role**: Architecture planning and technical requirements

**Input**: Project requirements, target platforms, performance constraints
**Output**: Technical architecture, implementation plan, timeline

**Use Cases**:
- Define app architecture and data flow
- Plan platform-specific implementations
- Create technical roadmaps
- Estimate development effort

**Example**:
```bash
mk agent run mobile-planner --input '{"project_type": "ecommerce", "platforms": ["ios", "android"]}'
```

### 2. Mobile Researcher
**Role**: Research packages, frameworks, and best practices

**Input**: Technical requirements, feature specifications
**Output**: Recommended packages, implementation approaches, comparison analysis

**Use Cases**:
- Find appropriate Flutter packages
- Compare iOS frameworks
- Research third-party libraries
- Analyze implementation alternatives

**Example**:
```bash
mk agent run mobile-researcher --input '{"feature": "payment_integration", "requirements": ["apple_pay", "google_pay"]}'
```

### 3. UI/UX Designer
**Role**: Generate UI mockups and convert to code

**Input**: Design requirements, brand guidelines, user stories
**Output**: UI mockups, Flutter widgets, SwiftUI code, assets

**Use Cases**:
- Design app interfaces
- Generate responsive layouts
- Create custom components
- Follow platform guidelines

**Example**:
```bash
mk agent run ui-ux-designer --input '{"screen": "user_profile", "platform": "ios", "style": "minimalist"}'
```

### 4. Database Architect
**Role**: Design data storage and offline strategies

**Input**: Data requirements, performance needs, sync requirements
**Output**: Database schema, migration scripts, offline sync strategy

**Use Cases**:
- Design SQLite databases
- Plan Core Data models
- Create offline-first architecture
- Design data synchronization

**Example**:
```bash
mk agent run database-architect --input '{"entities": ["user", "product", "order"], "offline_required": true}'
```

### 5. Mobile Tester
**Role**: Create comprehensive test suites

**Input**: Feature specifications, code implementation
**Output**: Unit tests, integration tests, UI tests, device compatibility tests

**Use Cases**:
- Write widget tests for Flutter
- Create XCTest suites for iOS
- Design device compatibility tests
- Generate performance tests

**Example**:
```bash
mk agent run mobile-tester --input '{"feature": "login_flow", "platforms": ["ios", "android"], "test_types": ["unit", "ui", "integration"]}'
```

### 6. Code Reviewer
**Role**: Review code for mobile best practices

**Input**: Code changes, pull requests
**Output**: Code review comments, security analysis, performance recommendations

**Use Cases**:
- Review Flutter code for performance
- Check iOS memory management
- Validate mobile security practices
- Ensure platform compliance

**Example**:
```bash
mk agent run code-reviewer --input '{"files": ["lib/main.dart", "lib/screens/home.dart"], "focus": "performance"}'
```

### 7. Mobile Debugger
**Role**: Analyze and fix mobile-specific issues

**Input**: Crash reports, performance logs, bug reports
**Output**: Root cause analysis, fix recommendations, debugging steps

**Use Cases**:
- Analyze Flutter crash logs
- Debug iOS memory issues
- Solve performance bottlenecks
- Fix platform-specific bugs

**Example**:
```bash
mk agent run mobile-debugger --input '{"crash_log": "crash.txt", "platform": "android", "symptoms": ["app_freezes"]}'
```

### 8. Docs Manager
**Role**: Maintain documentation and user guides

**Input**: Code changes, feature updates
**Output**: Updated documentation, API docs, user guides

**Use Cases**:
- Update API documentation
- Create user guides
- Document new features
- Maintain code comments

**Example**:
```bash
mk agent run docs-manager --input '{"features": ["user_authentication", "data_sync"], "doc_types": ["api", "user_guide"]}'
```

### 9. Git Manager
**Role**: Manage version control for mobile projects

**Input**: Code changes, release requirements
**Output**: Branch management, release tags, CI/CD configuration

**Use Cases**:
- Manage feature branches
- Create release tags
- Set up CI/CD pipelines
- Handle merge strategies

**Example**:
```bash
mk agent run git-manager --input '{"release_version": "2.1.0", "features": ["payment_integration"], "hotfix": false}'
```

### 10. Release Manager
**Role**: Handle app store deployments

**Input**: Build artifacts, release notes
**Output**: App store submissions, TestFlight releases, deployment status

**Use Cases**:
- Submit to App Store
- Deploy to Google Play
- Manage TestFlight
- Handle release notes

**Example**:
```bash
mk agent run release-manager --input '{"platform": "ios", "build_number": "2.1.0", "release_notes": "Added payment features"}'
```

### 11. Content Writer
**Role**: Create app store content and communications

**Input**: Feature descriptions, target audience
**Output**: App store descriptions, release notes, marketing copy

**Use Cases**:
- Write App Store descriptions
- Create marketing copy
- Generate release notes
- Optimize for app stores

**Example**:
```bash
mk agent run content-writer --input '{"app_name": "ShoppingApp", "features": ["barcode_scanner", "price_comparison"], "tone": "professional"}'
```

### 12. Project Tracker
**Role**: Track development progress and coordination

**Input**: Sprint goals, team capacity
**Output**: Progress reports, milestone tracking, resource allocation

**Use Cases**:
- Track sprint progress
- Monitor development velocity
- Generate progress reports
- Plan resource allocation

**Example**:
```bash
mk agent run project-tracker --input '{"sprint": "Sprint 12", "team_size": 3, "goals": ["complete_user_auth", "implement_payments"]}'
```

## Agent Configuration

Each agent can be configured in your `mobilekit.yaml`:

```yaml
agents:
  mobile-planner:
    timeout: 300
    max_tokens: 4000
    temperature: 0.3

  ui-ux-designer:
    timeout: 600
    max_tokens: 6000
    temperature: 0.7
    style_guide: "material_design"

  mobile-tester:
    timeout: 400
    max_tokens: 3000
    temperature: 0.2
    coverage_threshold: 80
```

## Creating Custom Agents

You can create custom agents by adding markdown files to the `agents/` directory:

```markdown
# Custom Agent

**Role**: [Describe the agent's primary role]

**Input**: [List input types]

**Output**: [List output types]

**Description**:
[Detailed description of what the agent does]

**Capabilities**:
- [List specific capabilities]

**Mobile Focus**:
[Mobile-specific considerations]

**Example Usage**:
[Example of how to use the agent]
```

## Best Practices

### 1. Choose the Right Agent
- Use **Mobile Planner** for architecture decisions
- Use **UI/UX Designer** for interface design
- Use **Mobile Tester** for quality assurance
- Use **Code Reviewer** for code quality

### 2. Provide Clear Input
- Be specific about requirements
- Include relevant context
- Specify target platforms
- Define success criteria

### 3. Review Agent Output
- Verify generated code follows best practices
- Test implementations thoroughly
- Validate against requirements
- Iterate as needed

### 4. Use Workflows for Complex Tasks
- Combine multiple agents for comprehensive solutions
- Use predefined workflows for common patterns
- Create custom workflows for specific needs
- Track progress through multi-agent processes

## Integration with Development Tools

### IDE Integration
MobileKit agents can be integrated with popular IDEs:

- **VS Code**: Use MobileKit extension
- **Android Studio**: Plugin support
- **Xcode**: Script integration

### CI/CD Integration
Agents can be integrated into CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Run MobileKit Code Review
  run: mk agent run code-reviewer --input '{"files": "changed_files.txt"}'

- name: Generate Tests
  run: mk agent run mobile-tester --input '{"feature": "${{ github.event.head_commit.message }}"}'
```

## Troubleshooting

### Common Issues

1. **Agent Timeouts**: Increase timeout in configuration
2. **Poor Quality Output**: Adjust temperature and provide more specific input
3. **Platform Compatibility**: Ensure agent supports target platform
4. **Memory Issues**: Limit context window and use focused queries

### Getting Help

- Check agent logs for detailed error information
- Review configuration for proper setup
- Consult documentation for specific agent usage
- Report issues with reproduction steps