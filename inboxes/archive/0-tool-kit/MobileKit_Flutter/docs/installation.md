# MobileKit Flutter Installation Guide

## Prerequisites

Before installing MobileKit Flutter, ensure you have:

- **macOS**: macOS 12.0 or later
- **Xcode**: Xcode 15.0 or later  
- **Swift**: Swift 5.9+ (included with Xcode)
- **Node.js**: 16.0 or later (for CLI tool)
- **CocoaPods**: Latest version (optional, for dependencies)

## Installation Methods

### Method 1: NPM (Recommended)
```bash
# Install globally
npm install -g mobilekit-ios-cli

# Verify installation
mkf --version
```

### Method 2: Download Release
1. Download the latest release from [GitHub Releases](https://github.com/mobilekit/ios/releases)
2. Extract the archive
3. Run the installer or add to PATH

## Quick Start

### 1. Create New Project
```bash
# Interactive project creation
mkf new

# Or with options
mkf new --template swiftui --name MyFlutterApp --bundle-id com.company.myapp
```

### 2. Generate Features
```bash
# Generate Flutter widgets view
mkf generate-feature --name UserProfile --type swiftui-view

# Generate complete MVVM feature
mkf generate-feature --name ProductCatalog --type complete-feature
```

### 3. Run Tests
```bash
# Run all tests
mkf run-tests

# Run with coverage
mkf run-tests --coverage

# Run on specific devices
mkf run-tests --devices "iPhone 15,iPad Pro"
```

### 4. Build and Deploy
```bash
# Build archive for App Store
mkf build-archive --configuration Release

# Submit to TestFlight
mkf submit-testflight --notes "Beta release with new features"
```

## Troubleshooting

### Common Issues

**1. Command not found: mkf**
```bash
# Reinstall CLI
npm uninstall -g mobilekit-ios-cli
npm install -g mobilekit-ios-cli
```

**2. Xcode build errors**
```bash
# Clean build folder
xcodebuild clean

# Update CocoaPods
pod update
```

For more help, visit our [Documentation](https://mobilekit.dev/ios/docs).
