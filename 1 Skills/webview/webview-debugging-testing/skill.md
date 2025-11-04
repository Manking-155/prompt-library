# WebView Debugging & Testing Skill

## Mission Brief
Expert in debugging and testing iOS WebView applications. Specializes in comprehensive testing strategies, debugging techniques, and quality assurance for WebView-based iOS applications.

## Core Expertise

### WebView Debugging
- Safari Web Inspector integration
- JavaScript console debugging
- Network request inspection
- Performance profiling tools
- Memory leak detection

### Testing Strategies
- Unit testing for WebView components
- Integration testing for native bridges
- UI testing for WebView interactions
- Network condition simulation
- Device-specific testing

### Debugging Tools & Techniques
- Xcode Instruments profiling
- Safari Developer Tools
- Remote debugging workflows
- Crash log analysis
- Performance bottleneck identification

### Quality Assurance
- Automated testing pipelines
- Cross-device compatibility testing
- Network condition testing
- User experience validation
- Security testing integration

## Guardrails

### Testing Coverage
- Ensure comprehensive test coverage for critical paths
- Test on actual devices, not just simulators
- Validate WebView content across different iOS versions
- Include network failure scenarios in testing

### Debugging Best Practices
- Never ship debugging code to production
- Use proper logging levels and controls
- Implement crash reporting systems
- Maintain debugging documentation

### Quality Standards
- Follow iOS testing best practices
- Implement proper test data management
- Maintain test environment consistency
- Document testing procedures and results

## Integration Hints

### Debugging Setup
```swift
// Enable WebView debugging in development builds
#if DEBUG
if #available(iOS 16.4, *) {
    webView.isInspectable = true
}
#endif
```

### Testing Infrastructure
```
Tests/
├── WebViewTests/
│   ├── WebViewIntegrationTests.swift
│   ├── JavaScriptBridgeTests.swift
│   └── NetworkConditionTests.swift
├── UITests/
│   └── WebViewUITests.swift
└── MockServices/
    ├── MockNetworkService.swift
    └── MockWebViewDelegate.swift
```

### Key Testing Areas
- `WebView/WebViewController.swift` - Core WebView functionality
- JavaScript bridge methods
- Network request handling
- Native feature integration
- Error handling scenarios

### Debugging Tools Integration
- Safari Web Inspector for WebView content debugging
- Xcode Console for native code logging
- Instruments for performance profiling
- Network Link Conditioner for network testing

## Implementation Notes

### WebView Debugging Setup
1. **Enable Remote Debugging**:
   ```swift
   // Debug configuration
   #if DEBUG
   let preferences = WKPreferences()
   preferences.javaScriptEnabled = true
   
   let configuration = WKWebViewConfiguration()
   configuration.preferences = preferences
   
   if #available(iOS 16.4, *) {
       webView.isInspectable = true
   }
   #endif
   ```

2. **Console Logging**:
   ```swift
   // JavaScript console forwarding
   func webView(_ webView: WKWebView, runJavaScriptAlertPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping () -> Void) {
       #if DEBUG
       print("WebView Alert: \(message)")
       #endif
       completionHandler()
   }
   ```

3. **Error Logging**:
   ```swift
   // Comprehensive error logging
   func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
       #if DEBUG
       print("WebView Navigation Error: \(error.localizedDescription)")
       print("URL: \(webView.url?.absoluteString ?? "unknown")")
       #endif
       
       // Handle error appropriately
       handleNavigationError(error)
   }
   ```

### Testing Implementation
1. **Unit Testing WebView Components**:
   ```swift
   import XCTest
   @testable import YourApp
   
   class WebViewUnitTests: XCTestCase {
       var webViewController: WebViewController!
       
       override func setUp() {
           super.setUp()
           webViewController = WebViewController()
       }
       
       func testWebViewConfiguration() {
           // Test WebView setup
           XCTAssertNotNil(webViewController.webView)
           // Add specific configuration tests
       }
   }
   ```

2. **Integration Testing JavaScript Bridge**:
   ```swift
   func testJavaScriptBridgeCommunication() {
       let expectation = XCTestExpectation(description: "JavaScript bridge response")
       
       webViewController.webView.evaluateJavaScript("window.nativeBridge.test()") { result, error in
           XCTAssertNil(error)
           XCTAssertNotNil(result)
           expectation.fulfill()
       }
       
       wait(for: [expectation], timeout: 5.0)
   }
   ```

3. **Network Condition Testing**:
   ```swift
   func testOfflineFunctionality() {
       // Mock network conditions
       let mockNetworkManager = MockNetworkManager()
       mockNetworkManager.isConnected = false
       
       // Test offline behavior
       webViewController.networkManager = mockNetworkManager
       webViewController.handleNetworkDisconnection()
       
       // Verify offline behavior
       XCTAssertTrue(webViewController.isOfflineMode)
   }
   ```

### UI Testing for WebView
1. **WebView Interaction Testing**:
   ```swift
   class WebViewUITests: XCTestCase {
       var app: XCUIApplication!
       
       override func setUp() {
           super.setUp()
           app = XCUIApplication()
           app.launch()
       }
       
       func testWebViewContentLoading() {
           let webView = app.webViews.firstMatch
           XCTAssertTrue(webView.waitForExistence(timeout: 10))
           
           // Test specific content interactions
           let button = webView.buttons["Submit"]
           XCTAssertTrue(button.exists)
           button.tap()
       }
   }
   ```

2. **Native Feature Testing**:
   ```swift
   func testCameraIntegration() {
       // Test camera permission request
       let cameraButton = app.buttons["Open Camera"]
       cameraButton.tap()
       
       // Handle permission dialog
       let allowButton = app.alerts.buttons["Allow"]
       if allowButton.exists {
           allowButton.tap()
       }
       
       // Verify camera interface appears
       XCTAssertTrue(app.otherElements["Camera View"].exists)
   }
   ```

### Performance Testing
1. **Memory Usage Testing**:
   ```swift
   func testMemoryUsage() {
       let initialMemory = getCurrentMemoryUsage()
       
       // Perform WebView operations
       webViewController.loadHeavyContent()
       
       let finalMemory = getCurrentMemoryUsage()
       let memoryIncrease = finalMemory - initialMemory
       
       // Assert acceptable memory increase
       XCTAssertLessThan(memoryIncrease, 50 * 1024 * 1024) // 50MB limit
   }
   ```

2. **Load Time Testing**:
   ```swift
   func testPageLoadPerformance() {
       let startTime = CFAbsoluteTimeGetCurrent()
       
       webViewController.loadURL("https://example.com")
       
       // Wait for load completion
       let expectation = XCTestExpectation(description: "Page load")
       webViewController.onPageLoadComplete = {
           expectation.fulfill()
       }
       
       wait(for: [expectation], timeout: 10.0)
       
       let loadTime = CFAbsoluteTimeGetCurrent() - startTime
       XCTAssertLessThan(loadTime, 5.0) // 5 second limit
   }
   ```

### Debugging Tools Usage
1. **Safari Web Inspector**:
   - Connect device to Mac
   - Enable Web Inspector in Safari settings
   - Use Develop menu to select WebView
   - Debug JavaScript, inspect DOM, analyze network

2. **Xcode Instruments**:
   - Use Time Profiler for performance analysis
   - Use Allocations for memory tracking
   - Use Network Link Conditioner for network testing
   - Use Energy Log for battery usage analysis

3. **Console Logging**:
   ```swift
   // Structured logging
   enum LogLevel: String, CaseIterable {
       case debug, info, warning, error
   }
   
   func log(_ message: String, level: LogLevel = .info) {
       #if DEBUG
       let timestamp = DateFormatter().string(from: Date())
       print("[\(timestamp)] [\(level.rawValue.uppercased())] WebView: \(message)")
       #endif
   }
   ```

### Common Debugging Scenarios
- WebView not loading content
- JavaScript bridge not responding
- Memory leaks in WebView context
- Network requests failing
- UI elements not responding
- Performance bottlenecks
- Crash investigation

### Testing Checklists
- [ ] Unit tests for WebView components
- [ ] Integration tests for native bridges
- [ ] UI tests for WebView interactions
- [ ] Performance testing under load
- [ ] Network condition testing
- [ ] Cross-device compatibility testing
- [ ] Security testing validation
- [ ] Accessibility testing
- [ ] Error handling validation
- [ ] Memory leak detection