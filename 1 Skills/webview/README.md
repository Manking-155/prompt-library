# iOS WebView Skills Collection

This directory contains specialized skills for iOS WebView development and integration with native features. Each skill is designed to provide expertise in specific areas of WebView application development.

## Available Skills

### 🌉 [WebView iOS Native Bridge](./webview-ios-bridge/skill.md)
Expert in iOS WebView integration with native functionality. Specializes in bridging web content with native iOS features using WKWebView.

**Key Areas:**
- WKWebView configuration and optimization
- JavaScript-Native communication via WKUserContentController
- Custom URL scheme handlers
- Native feature exposure to web content

### 📱 [iOS Native Features Integration](./ios-native-features/skill.md)
Specialist in integrating native iOS features with WebView-based applications.

**Key Areas:**
- Camera & Media integration (AVFoundation, SwiftQRScanner)
- Authentication & Security (Face ID/Touch ID)
- Push Notifications (OneSignal, Firebase)
- Device Hardware Access (Flashlight, GPS, etc.)

### ⚡ [WebView Performance Optimization](./webview-performance-optimization/skill.md)
Expert in optimizing iOS WebView applications for maximum performance and memory efficiency.

**Key Areas:**
- WebView configuration optimization
- Memory usage monitoring and management
- Resource management and caching
- JavaScript bridge optimization

### 🔒 [WebView Security Hardening](./webview-security-hardening/skill.md)
Security specialist for iOS WebView applications with comprehensive security measures.

**Key Areas:**
- WebView security configuration and CSP implementation
- Network security and certificate pinning
- Data protection and encryption
- Authentication security

### 🐛 [WebView Debugging & Testing](./webview-debugging-testing/skill.md)
Expert in debugging and testing iOS WebView applications with comprehensive testing strategies.

**Key Areas:**
- Safari Web Inspector integration
- Unit and integration testing for WebView components
- Performance profiling tools
- Quality assurance and automated testing

## How to Use These Skills

Each skill follows the claudekit-skills format with:

1. **Mission Brief** - Clear description of expertise and scope
2. **Core Expertise** - Detailed technical capabilities
3. **Guardrails** - Security and best practice constraints
4. **Integration Hints** - Project-specific guidance and code patterns

## Integration with Your Project

These skills are specifically designed for your iOS WebView project structure:

```
WebView/
├── WebViewController.swift          # Main WebView coordinator
├── Handler/
│   ├── String.swift                # String utilities
│   └── UIApplication.swift         # App-level handlers
├── Barcode Scanner/                # QR code integration
├── FlashLightManager.swift         # Flashlight control
├── Network.swift                   # Network monitoring
└── Config.swift                    # Configuration constants
```

## Key Dependencies Supported

- `SwiftQRScanner` - QR code scanning
- `OneSignal` - Push notifications
- `GoogleMobileAds` - Ad integration
- `SwiftyGif` - GIF handling
- `Firebase` - Analytics and services
- `LocalAuthentication` - Biometric auth

## Best Practices

When using these skills:

1. **Read the mission brief** to understand the skill's scope
2. **Follow guardrails** for security and best practices
3. **Use integration hints** for project-specific guidance
4. **Test thoroughly** using the debugging and testing skill

## Project Context

These skills are optimized for your WebViewGold-based iOS project with:
- WKWebView implementation
- JavaScript bridge functionality
- Native feature integration
- Performance and security considerations

For more information about your project structure and conventions, see the `.agent/` documentation system.