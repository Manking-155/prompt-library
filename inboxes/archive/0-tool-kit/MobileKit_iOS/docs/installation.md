# MobileKit iOS Installation Guide

## Prerequisites

Before installing MobileKit iOS, ensure you have:

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
mki --version
```

### Method 2: Download Release
1. Download the latest release from [GitHub Releases](https://github.com/mobilekit/ios/releases)
2. Extract the archive
3. Run the installer or add to PATH

## Quick Start

### 1. Create New Project
```bash
# Interactive project creation
mki new

# Or with options
mki new --template swiftui --name MyiOSApp --bundle-id com.company.myapp
```

### 2. Generate Features
```bash
# Generate SwiftUI view
mki generate-feature --name UserProfile --type swiftui-view

# Generate complete MVVM feature
mki generate-feature --name ProductCatalog --type complete-feature
```

### 3. Run Tests
```bash
# Run all tests
mki run-tests

# Run with coverage
mki run-tests --coverage

# Run on specific devices
mki run-tests --devices "iPhone 15,iPad Pro"
```

### 4. Build and Deploy
```bash
# Build archive for App Store
mki build-archive --configuration Release

# Submit to TestFlight
mki submit-testflight --notes "Beta release with new features"
```

## Troubleshooting

### Common Issues

**1. Command not found: mki**
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
