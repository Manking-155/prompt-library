# MobileKit Installation & Setup Guide

## 🚀 Quick Start

### 1. System Requirements
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher (for React Native projects)
- **Flutter SDK**: 3.10 or higher (for Flutter projects)
- **Xcode**: 14 or higher (for iOS development)
- **Android Studio**: Latest version (for Android development)

### 2. Installation

```bash
# Install MobileKit
pip install mobilekit

# Or install from source
git clone https://github.com/your-org/mobilekit.git
cd mobilekit
pip install -e .
```

### 3. Initial Configuration

```bash
# Initialize MobileKit
mk init

# Configure AI provider
mk configure --ai-provider openai --api-key your-api-key

# Or configure for Claude
mk configure --ai-provider claude --api-key your-claude-key
```

### 4. Create Your First Project

```bash
# Create a new Flutter project
mk new-project --type flutter --name MyAwesomeApp --platforms ios android

# Navigate to project
cd MyAwesomeApp

# Generate your first feature
mk generate-feature --name welcome-screen --type screen
```

## 📁 Directory Structure After Installation

```
your-project/
├── .mobilekit/                 # MobileKit configuration
│   ├── config.yaml            # Project-specific settings
│   └── agents/                # Custom agent configurations
├── MOBILE_CONTEXT.md          # Project context file
├── lib/                       # Source code (Flutter)
├── test/                      # Test files
├── integration_test/          # Integration tests
├── assets/                    # Static assets
└── pubspec.yaml              # Dependencies (Flutter)
```

## ⚙️ Configuration Options

### Global Configuration (~/.mobilekit/config.yaml)
```yaml
ai_provider: "openai"          # openai, claude, huggingface
api_key: "your-api-key"
model: "gpt-4"                 # Model to use
max_tokens: 4000               # Token limit per request
temperature: 0.3               # Creativity level

# Default project settings
default_project_type: "flutter"
default_platforms: ["ios", "android"]

# Testing configuration
testing:
  device_farm: "firebase"      # firebase, browserstack, aws
  coverage_threshold: 80
  auto_run_tests: true

# Release configuration
release:
  auto_increment_build: true
  submit_for_review: false
  staged_rollout: 10           # Percentage
```

### Project Configuration (.mobilekit/config.yaml)
```yaml
project_name: "MyAwesomeApp"
project_type: "flutter"
target_platforms: ["ios", "android"]
created_date: "2024-01-15"

# Custom agent settings
agents:
  mobile-planner:
    temperature: 0.2           # More deterministic planning
  ui-ux-designer:
    temperature: 0.7           # More creative designs

# Workflow preferences
workflows:
  new_feature:
    auto_generate_tests: true
    auto_update_docs: true
    require_code_review: true
```

## 🤖 Agent Customization

### Creating Custom Agents
```bash
# Create a new agent
mk create-agent --name custom-agent --template base

# Edit agent definition
# Edit .mobilekit/agents/custom-agent.md
```

### Agent Definition Template
```markdown
# Custom Agent

## Role Description
Your custom agent's role and responsibilities.

## Input Requirements
- input1: Description
- input2: Description

## Output Deliverables
- output1: Description
- output2: Description

## Quality Standards
- Standard 1
- Standard 2

## Mobile-Specific Considerations
- Mobile consideration 1
- Mobile consideration 2
```

## 🔄 Workflow Customization

### Creating Custom Workflows
```bash
# Create new workflow
mk create-workflow --name custom-feature-workflow

# Edit workflow definition  
# Edit .mobilekit/workflows/custom-feature-workflow.yaml
```

### Workflow Definition Template
```yaml
name: "custom-workflow"
description: "Description of your custom workflow"

inputs:
  - name: "input_param"
    type: "string"
    required: true

steps:
  - name: "step1"
    agent: "mobile-planner"
    type: "sequential"
    inputs:
      - input_param
    outputs:
      - step1_output

  - name: "step2"
    agent: "ui-ux-designer"
    type: "parallel"
    depends_on: ["step1"]
    inputs:
      - step1_output
```

## 🧪 Testing Setup

### Device Testing Configuration
```yaml
# .mobilekit/testing.yaml
devices:
  ios:
    - "iPhone 14"
    - "iPhone 14 Pro Max"
    - "iPad Pro 12.9"
  android:
    - "Pixel 7"
    - "Samsung Galaxy S23"
    - "OnePlus 11"

test_suites:
  - name: "smoke_tests"
    coverage_threshold: 60
  - name: "regression_tests"
    coverage_threshold: 90

device_farm:
  provider: "firebase"          # firebase, browserstack, aws_device_farm
  api_key: "your-device-farm-key"
  parallel_executions: 3
```

### Running Tests
```bash
# Run tests on specific devices
mk run-tests --devices "iPhone 14,Pixel 7" --coverage

# Run full regression suite
mk run-tests --suite regression --all-devices

# Run performance tests
mk run-tests --type performance --duration 10m
```

## 🚀 Release Configuration

### App Store Configuration
```yaml
# .mobilekit/release.yaml
ios:
  team_id: "YOUR_TEAM_ID"
  bundle_id: "com.yourcompany.app"
  provisioning_profile: "App Store"
  certificate: "iOS Distribution"

android:
  package_name: "com.yourcompany.app"
  keystore: "path/to/keystore.jks"
  key_alias: "your_key_alias"

stores:
  app_store:
    auto_submit: false
    staged_rollout: true
    rollout_percentage: 10

  google_play:
    auto_submit: false
    track: "internal"           # internal, alpha, beta, production
```

### Release Commands
```bash
# Build for release
mk build-release --platform ios --target app-store

# Submit to stores
mk submit --platform both --track beta

# Monitor release
mk release-status --version 1.2.0
```

## 🔧 Troubleshooting

### Common Issues

1. **AI API Key Issues**
```bash
# Verify API key
mk verify-config

# Update API key
mk configure --ai-provider openai --api-key new-key
```

2. **Build Issues**
```bash
# Clean build cache
mk clean

# Rebuild dependencies
mk rebuild-deps

# Check system requirements
mk doctor
```

3. **Agent Execution Issues**
```bash
# Check agent status
mk status

# Restart specific agent
mk restart-agent mobile-planner

# View agent logs
mk logs --agent mobile-planner --tail 50
```

### Debug Mode
```bash
# Enable debug logging
mk --debug generate-feature --name test-feature

# Verbose output
mk --verbose run-tests
```

### Getting Help
```bash
# General help
mk --help

# Command-specific help
mk generate-feature --help

# Show examples
mk examples

# Check system status
mk doctor
```

## 🌐 Integration Examples

### CI/CD Integration (GitHub Actions)
```yaml
# .github/workflows/mobilekit.yml
name: MobileKit CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup MobileKit
      run: |
        pip install mobilekit
        mk configure --ai-provider ${{ secrets.AI_PROVIDER }} --api-key ${{ secrets.AI_API_KEY }}

    - name: Run Tests
      run: mk run-tests --coverage --ci-mode

    - name: Code Review
      run: mk review-code --branch ${{ github.head_ref }}
```

### Slack Integration
```yaml
# .mobilekit/integrations.yaml
slack:
  webhook_url: "your-slack-webhook"
  channels:
    notifications: "#mobile-dev"
    alerts: "#mobile-alerts"

notifications:
  workflow_start: true
  workflow_complete: true
  build_failure: true
  test_failure: true
```

## 📚 Next Steps

1. **Explore Examples**: Check out the `examples/` directory for sample projects
2. **Read Agent Guides**: Learn about each agent's capabilities in `docs/agents/`
3. **Custom Workflows**: Create workflows specific to your development process
4. **Team Setup**: Configure MobileKit for team collaboration
5. **Advanced Features**: Explore integrations with your existing tools

---

For more detailed documentation, visit: [MobileKit Documentation](https://mobilekit.dev/docs)
For support, join our community: [MobileKit Discord](https://discord.gg/mobilekit)
