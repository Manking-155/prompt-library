# WebView Performance Optimization Skill

## Mission Brief
Expert in optimizing iOS WebView applications for maximum performance, memory efficiency, and smooth user experience. Specializes in advanced WKWebView optimization techniques and resource management.

## Core Expertise

### WebView Performance Tuning
- WKWebView configuration optimization
- Memory usage monitoring and management
- CPU usage optimization techniques
- JavaScript execution performance
- Content loading optimization

### Resource Management
- Image and media optimization strategies
- Caching implementation (memory and disk)
- Resource preloading techniques
- Lazy loading implementation
- Bundle size optimization

### Network Optimization
- Request batching and optimization
- HTTP/2 utilization
- Content compression strategies
- Offline functionality implementation
- Network failure handling

### JavaScript Bridge Optimization
- Efficient message passing between WebView and Native
- Asynchronous operation handling
- Memory leak prevention in JavaScript contexts
- Performance monitoring and profiling

## Guardrails

### Memory Management
- Monitor WebView memory usage continuously
- Implement proper cleanup for heavy operations
- Avoid memory leaks in JavaScript bridge
- Handle low memory warnings appropriately

### User Experience
- Maintain smooth 60fps animations
- Implement proper loading states
- Handle network timeouts gracefully
- Provide feedback for long-running operations

### Security Considerations
- Never sacrifice security for performance
- Implement proper content validation
- Use secure caching strategies
- Handle malicious content appropriately

## Integration Hints

### Key Configuration Areas
```swift
// WebView performance configuration
let configuration = WKWebViewConfiguration()
configuration.allowsInlineMediaPlayback = true
configuration.mediaTypesRequiringUserActionForPlayback = []
configuration.suppressesIncrementalRendering = false
```

### Memory Monitoring
```swift
// Memory pressure handling
override func viewDidDisappear(_ animated: Bool) {
    super.viewDidDisappear(animated)
    // Clean up WebView resources
    webView.stopLoading()
    webView.configuration.userContentController.removeAllScriptMessageHandlers()
}
```

### Performance Monitoring Points
- `WebView/WebViewController.swift` - Main performance optimization
- `WebView/Network.swift` - Network performance handling
- `WebView/Config.swift` - Performance-related configurations

### Optimization Targets
- Reduce initial load time to < 3 seconds
- Maintain memory usage under 100MB for typical content
- Achieve smooth scrolling and interactions
- Minimize CPU usage during idle periods

## Implementation Notes

### Loading Performance
1. **Preloading Strategy**:
   - Preload critical resources
   - Implement intelligent caching
   - Use service workers for offline support

2. **Resource Optimization**:
   - Optimize images and media files
   - Minify JavaScript and CSS
   - Implement resource bundling

3. **WebView Configuration**:
   - Enable hardware acceleration
   - Optimize rendering pipeline
   - Configure appropriate caching policies

### Memory Optimization
1. **WebView Lifecycle Management**:
   ```swift
   deinit {
       webView.navigationDelegate = nil
       webView.uiDelegate = nil
       webView.removeFromSuperview()
   }
   ```

2. **Resource Cleanup**:
   - Clear caches periodically
   - Remove unused JavaScript contexts
   - Clean up event listeners

3. **Memory Monitoring**:
   ```swift
   // Monitor memory warnings
   NotificationCenter.default.addObserver(
       self,
       selector: #selector(handleMemoryWarning),
       name: UIApplication.didReceiveMemoryWarningNotification,
       object: nil
   )
   ```

### JavaScript Bridge Optimization
1. **Efficient Message Passing**:
   - Batch multiple operations
   - Use JSON for complex data structures
   - Implement async/await patterns

2. **Performance Monitoring**:
   - Track JavaScript execution times
   - Monitor bridge message frequency
   - Identify performance bottlenecks

### Network Optimization
1. **Request Optimization**:
   - Implement request deduplication
   - Use HTTP/2 when available
   - Optimize header sizes

2. **Caching Strategy**:
   - Implement intelligent caching
   - Use appropriate cache headers
   - Handle cache invalidation properly

### Performance Metrics to Track
- Page load time
- Time to interactive
- Memory usage patterns
- JavaScript execution time
- Network request timing
- User interaction response time

### Common Performance Issues
- Excessive JavaScript execution
- Large image assets
- Inefficient caching strategies
- Memory leaks in WebView contexts
- Blocking operations on main thread
- Over-frequent bridge communications

### Optimization Tools
- Xcode Instruments for profiling
- Safari Web Inspector for WebView debugging
- Network Link Conditioner for testing
- Memory Graph Debugger for leak detection