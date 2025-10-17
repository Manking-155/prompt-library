# MobileKit Command Examples

## Project Initialization
```bash
# Create new Flutter project
mk new-project --type flutter --name MyAwesomeApp --platforms ios android

# Create iOS native project  
mk new-project --type ios-swift --name MyiOSApp --platforms ios

# Create with custom template
mk new-project --template social-media --name SocialApp --platforms both
```

## Feature Development
```bash
# Generate complete feature with AI workflow
mk generate-feature --name user-profile --type crud --priority high

# Generate UI screen only
mk generate-feature --name settings-screen --type screen --agents ui-ux-designer

# Generate with specific agents
mk generate-feature --name payment --agents mobile-planner,mobile-researcher,database-architect
```

## Testing & Quality
```bash
# Run comprehensive test suite
mk run-tests --coverage --devices "iPhone 14,Pixel 7"

# Test specific platforms
mk run-tests --platform ios --suite regression

# Performance testing
mk run-tests --type performance --duration 10m --memory-threshold 200MB
```

## Code Review & Debugging
```bash
# AI-powered code review
mk review-code --focus mobile-performance --security

# Debug crash reports
mk debug-crash --crash-file crashes/crash-2024-01-15.txt --reproduce

# Analyze memory leaks
mk debug-memory --profile --device "iPhone 14 Pro"
```

## Release Management
```bash
# Build for app stores
mk build-release --platform both --target app-store

# Prepare release with automation
mk prepare-release --version 1.2.0 --auto-generate-notes

# Deploy to beta testing
mk deploy --track beta --platform ios --testflight
```

## Project Management
```bash
# View project status
mk status --detailed --metrics

# Generate progress report
mk report --sprint current --format pdf

# Plan next sprint
mk plan-sprint --duration 2weeks --capacity 40hours
```
