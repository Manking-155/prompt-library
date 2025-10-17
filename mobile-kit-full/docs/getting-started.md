# Getting Started with MobileKit

MobileKit is an AI-powered mobile development toolkit that helps you build high-quality mobile applications faster and more efficiently.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - Required for MobileKit CLI
- **Flutter SDK** (for Flutter projects)
- **Xcode 14+** (for iOS projects)
- **Android Studio** (for Android projects)
- **Node.js 16+** (for React Native projects)
- **AI API Access** (OpenAI, Claude, or local LLM)

## Installation

### 1. Install MobileKit

```bash
pip install mobile-kit
```

### 2. Initialize MobileKit

```bash
mk init
```

### 3. Configure AI Provider

```bash
# For OpenAI
mk config set ai_provider openai
mk config set api_key YOUR_OPENAI_API_KEY

# For Claude
mk config set ai_provider claude
mk config set api_key YOUR_CLAUDE_API_KEY
```

## Quick Start

### Create a New Flutter Project

```bash
# Create a new Flutter project
mk new MyApp --type flutter

# Navigate to project directory
cd MyApp

# Generate a new feature
mk generate user-profile --type crud

# Run tests
mk test --coverage

# Build for release
mk build --platform ios --target app-store
```

### Create a New iOS Project

```bash
# Create a new iOS project
mk new MyIOSApp --type ios-swift

# Navigate to project directory
cd MyIOSApp

# Generate UI components
mk generate login-screen --type ui

# Run tests
mk test

# Build for App Store
mk build --platform ios --target app-store
```

### Create a New React Native Project

```bash
# Create a new React Native project
mk new MyReactApp --type react-native

# Navigate to project directory
cd MyReactApp

# Generate features
mk generate navigation --type service
mk generate home-screen --type ui

# Run tests
mk test

# Build for release
mk build --platform android --target play-store
```

## Project Structure

MobileKit creates a standardized project structure:

```
MyApp/
├── mobilekit.yaml          # MobileKit configuration
├── MOBILE_CONTEXT.md       # Mobile-specific context
├── lib/                    # Source code
│   ├── features/           # Generated features
│   ├── core/              # Core functionality
│   └── main.dart
├── test/                  # Test files
├── assets/                # App assets
└── docs/                  # Documentation
```

## Available Commands

### Project Management
- `mk new <name> --type <type>` - Create new project
- `mk generate <feature> --type <type>` - Generate new feature
- `mk test` - Run tests
- `mk build --platform <platform>` - Build for release

### Workflow Management
- `mk workflow run <workflow>` - Execute workflow
- `mk workflow list` - List available workflows

### Code Management
- `mk review --branch <branch>` - Review code changes
- `mk debug --crash-log <file>` - Debug crashes

### Agent Management
- `mk agent list` - List available agents
- `mk agent run <agent>` - Run specific agent

## Configuration

MobileKit uses a `mobilekit.yaml` configuration file:

```yaml
# Project Configuration
project:
  name: "MyApp"
  type: "flutter"
  platforms: ["ios", "android"]

# AI Configuration
ai:
  provider: "openai"
  model: "gpt-4"
  api_key: "${OPENAI_API_KEY}"

# Build Configuration
build:
  auto_increment_version: true
  generate_release_notes: true

# Testing Configuration
testing:
  coverage_threshold: 80
  devices: ["iPhone 14", "Pixel 7"]
```

## Workflows

MobileKit includes pre-defined workflows for common mobile development tasks:

### New Feature Development
Sequential workflow: Planner → Researcher → UI/UX Designer → Tester → Code Reviewer

```bash
mk workflow run new-feature
```

### Bug Fix Process
Sequential workflow: Debugger → Tester → Code Reviewer → Git Manager → Release Manager

```bash
mk workflow run bug-fix
```

### UI/UX Iteration
Iterative workflow for design improvements

```bash
mk workflow run ui-ux-iteration
```

### App Store Release
Complete release process with testing and submission

```bash
mk workflow run app-store-release
```

## Templates

MobileKit provides templates for different mobile platforms:

### Flutter Templates
- Material Design UI components
- BLoC/Riverpod state management
- Firebase integration
- Testing setup

### iOS Templates
- SwiftUI views
- MVVM architecture
- Core Data models
- XCTest setup

### React Native Templates
- React Navigation
- Redux state management
- API integration
- Jest testing setup

## Next Steps

1. **Explore the Agent System** - Learn about specialized mobile agents
2. **Customize Workflows** - Create workflows for your specific needs
3. **Extend with Plugins** - Add custom functionality
4. **Integrate with CI/CD** - Set up automated builds and deployments

## Support

- **Documentation**: [Full documentation](agent-guide.md)
- **Examples**: [Workflow examples](workflow-examples.md)
- **Issues**: Report bugs and request features
- **Community**: Join our developer community