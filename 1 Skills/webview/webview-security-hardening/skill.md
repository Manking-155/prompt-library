# WebView Security Hardening Skill

## Mission Brief
Security specialist for iOS WebView applications. Expert in implementing comprehensive security measures to protect WebView content, prevent attacks, and ensure safe web-to-native communication.

## Core Expertise

### WebView Security Configuration
- WKWebView security hardening
- Content Security Policy (CSP) implementation
- JavaScript injection prevention
- XSS attack mitigation
- Secure navigation handling

### Network Security
- HTTPS enforcement and certificate pinning
- Network security configuration
- Man-in-the-middle attack prevention
- Secure cookie handling
- API security integration

### Data Protection
- Sensitive data encryption
- Keychain integration for secure storage
- Local data protection
- Secure WebView caching
- Data sanitization and validation

### Authentication & Authorization
- Token management and validation
- Secure session handling
- OAuth integration patterns
- Biometric authentication security
- Multi-factor authentication support

## Guardrails

### Security First Approach
- Never disable security features for convenience
- Always validate and sanitize user inputs
- Implement proper error handling that doesn't leak information
- Follow OWASP security guidelines

### Compliance Requirements
- GDPR compliance for data handling
- App Store security guidelines
- Industry-specific security standards
- Privacy regulation adherence

### Risk Assessment
- Regular security audits and penetration testing
- Vulnerability scanning and remediation
- Security incident response planning
- Security monitoring and alerting

## Integration Hints

### Security Configuration Points
```swift
// Secure WebView configuration
let configuration = WKWebViewConfiguration()
configuration.allowsInlineMediaPlayback = true
configuration.mediaTypesRequiringUserActionForPlayback = [.video, .audio]
configuration.limitsNavigationsToAppBoundDomains = true
```

### Content Security Policy Implementation
```swift
// CSP injection for WebView security
let cspScript = """
let meta = document.createElement('meta');
meta.httpEquiv = 'Content-Security-Policy';
meta.content = 'default-src \\'self\\'; script-src \\'self\\' \\'unsafe-inline\\'; style-src \\'self\\' \\'unsafe-inline\\';';
document.head.appendChild(meta);
"""
```

### Secure JavaScript Bridge
```swift
// Validate all incoming messages
func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
    guard let messageBody = message.body as? [String: Any] else { return }
    // Validate and sanitize messageBody before processing
    processSecureMessage(messageBody)
}
```

### Key Security Files
- `WebView/WebViewController.swift` - Main security implementation
- `WebView/Config.swift` - Security configuration constants
- `AppDelegate.swift` - App-level security setup
- `Network.swift` - Network security handling

## Implementation Notes

### WebView Security Hardening
1. **Content Security Policy**:
   - Implement strict CSP headers
   - Restrict resource loading domains
   - Prevent inline script execution where possible
   - Control media and font loading permissions

2. **Navigation Security**:
   ```swift
   func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
       guard let url = navigationAction.request.url else {
           decisionHandler(.cancel)
           return
       }
       
       // Validate URL and domain
       if isAllowedURL(url) {
           decisionHandler(.allow)
       } else {
           decisionHandler(.cancel)
       }
   }
   ```

3. **JavaScript Security**:
   - Disable unnecessary JavaScript features
   - Implement strict message validation
   - Prevent JavaScript injection attacks
   - Use secure eval() alternatives

### Network Security Implementation
1. **Certificate Pinning**:
   ```swift
   // Implement certificate pinning
   func serverTrustPolicy(forHost host: String) -> ServerTrustPolicy {
       return .pinCertificates(
           certificates: ServerTrustPolicy.certificates(),
           validateCertificateChain: true,
           validateHost: true
       )
   }
   ```

2. **Secure API Communication**:
   - Use token-based authentication
   - Implement request signing
   - Encrypt sensitive data in transit
   - Handle API rate limiting

3. **Cookie Security**:
   - Use HttpOnly and Secure flags
   - Implement SameSite cookie policies
   - Handle cookie expiration properly
   - Clear cookies on logout

### Data Protection Strategies
1. **Keychain Integration**:
   ```swift
   // Secure storage in Keychain
   let keychain = Keychain(service: "com.yourapp.webview")
   try? keychain.set("sensitive_data", key: "userToken")
   ```

2. **Local Encryption**:
   - Encrypt sensitive local data
   - Use strong encryption algorithms
   - Implement proper key management
   - Secure data backup strategies

3. **Cache Security**:
   - Clear sensitive cache data
   - Implement secure cache policies
   - Handle offline data securely
   - Prevent cache-based attacks

### Authentication Security
1. **Token Management**:
   ```swift
   // Secure token handling
   func validateAndRefreshToken() {
       guard let token = Keychain.shared.getToken() else {
           // Handle missing token
           return
       }
       
       // Validate token and refresh if needed
       if isTokenExpired(token) {
           refreshToken()
       }
   }
   ```

2. **Biometric Security**:
   - Secure biometric data handling
   - Implement proper fallback mechanisms
   - Handle authentication failures securely
   - Prevent biometric bypass attempts

### Security Monitoring
1. **Logging and Monitoring**:
   - Implement security event logging
   - Monitor suspicious activities
   - Set up security alerts
   - Track authentication failures

2. **Vulnerability Detection**:
   - Regular security scans
   - Dependency vulnerability checking
   - Static code analysis
   - Dynamic application security testing

### Common Security Vulnerabilities
- Cross-site scripting (XSS)
- Man-in-the-middle attacks
- Insecure data storage
- Weak authentication mechanisms
- Certificate validation bypasses
- JavaScript injection attacks
- Insecure network communications

### Security Best Practices Checklist
- [ ] Implement Content Security Policy
- [ ] Use HTTPS everywhere
- [ ] Validate all user inputs
- [ ] Implement proper authentication
- [ ] Secure sensitive data storage
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Monitor security events
- [ ] Test for common vulnerabilities
- [ ] Document security measures