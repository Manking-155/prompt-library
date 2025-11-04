# WebView iOS Native Bridge Skill

## Mission Brief
Expert in iOS WebView integration with native functionality. Specializes in bridging web content with native iOS features using WKWebView, handling JavaScript-iOS communication, and implementing seamless web-to-native transitions.

## Core Expertise

### WebView Implementation
- WKWebView configuration and optimization
- JavaScript-Native communication via WKUserContentController
- WebView navigation handling and lifecycle management
- Cookie and session management
- Offline content loading strategies

### Native Bridge Integration
- Custom URL scheme handlers (e.g., `native://`, `get-uuid://`)
- JavaScript message handlers for two-way communication
- Native feature exposure to web content
- Security sandboxing and content validation

### iOS Feature Integration
- Camera/Photo library access from web content
- Push notifications (OneSignal) integration
- Biometric authentication (Face ID/Touch ID)
- In-app purchases and subscription management
- GPS and location services
- File upload/download handling

## Guardrails

### Security
- Always validate JavaScript inputs before processing
- Implement proper URL scheme validation
- Use HTTPS and certificate pinning when possible
- Never expose sensitive native APIs directly to web content

### Performance
- Implement lazy loading for heavy native modules
- Use background threads for intensive operations
- Optimize WebView memory usage
- Implement proper caching strategies

### Compatibility
- Target iOS 13+ for modern WebView features
- Handle device-specific limitations (iPad vs iPhone)
- Provide fallbacks for unsupported features
- Test across different iOS versions

## Integration Hints

### Project Structure Integration
```
WebView/
├── WebViewController.swift          # Main WebView coordinator
├── Handler/
│   ├── String.swift                # String utilities
│   └── UIApplication.swift         # App-level handlers
├── Barcode Scanner/                # QR code integration
└── Network.swift                   # Network monitoring
```

### Key Files to Modify
- `WebView/WebViewController.swift` - Core WebView logic
- `WebView/Config.swift` - Configuration constants
- `WebView/Network.swift` - Network state management
- `AppDelegate.swift` - App lifecycle integration

### Common Patterns
1. **JavaScript Bridge Setup**:
```swift
let contentController = WKUserContentController()
contentController.add(self, name: "nativeHandler")
```

2. **URL Scheme Handling**:
```swift
func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void)
```

3. **Native Feature Exposure**:
```swift
// Expose native functionality via JavaScript
webView.evaluateJavaScript("window.nativeAPI = { feature: 'available' };")
```

## Implementation Notes

### WebView Configuration
- Use `WKWebViewConfiguration` for advanced setup
- Implement custom user agents for compatibility
- Configure content blocking rules if needed
- Set proper security policies

### Communication Patterns
- Use `WKScriptMessageHandler` for JavaScript → Native
- Use `evaluateJavaScript` for Native → JavaScript
- Implement async/await patterns for better code readability

### Error Handling
- Implement graceful degradation for failed WebView loads
- Handle network connectivity issues
- Provide user feedback for native operations
- Log errors appropriately for debugging

### Testing Considerations
- Test web content loading on various network conditions
- Verify JavaScript bridge functionality
- Test native feature integration end-to-end
- Validate memory usage under heavy WebView operations