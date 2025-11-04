# iOS Native Features Integration Skill

## Mission Brief
Specialist in integrating native iOS features with WebView-based applications. Expert in implementing camera access, push notifications, biometric authentication, and other iOS-specific functionalities within WebView contexts.

## Core Expertise

### Camera & Media Integration
- AVFoundation for camera access
- Photo library integration with PHPickerViewController
- QR code scanning using SwiftQRScanner
- Video recording and playback
- Image processing and filters

### Authentication & Security
- Face ID / Touch ID integration using LocalAuthentication
- Biometric authentication workflows
- Passcode validation
- Keychain integration for secure storage
- App tracking transparency compliance

### Push Notifications
- OneSignal integration setup
- Firebase Cloud Messaging (FCM)
- Rich notifications with images/videos
- Local and remote notifications
- Notification handling and deep linking

### Device Hardware Access
- Flashlight control via AVFoundation
- Vibration and haptic feedback
- Battery level monitoring
- Network connectivity status
- Device orientation handling

### Location Services
- CoreLocation integration
- GPS coordinates access
- Geofencing capabilities
- Map integration with MapKit
- Location permission handling

## Guardrails

### Permission Management
- Always request permissions with clear user explanations
- Handle permission denial gracefully
- Provide fallbacks when permissions are not granted
- Follow Apple's Human Interface Guidelines for permission requests

### Privacy & Security
- Never access sensitive features without explicit permission
- Implement proper data encryption for stored information
- Follow iOS security best practices
- Handle app backgrounding/foregrounding properly

### Performance Considerations
- Optimize camera operations for battery life
- Implement proper resource cleanup
- Use background queues for heavy operations
- Monitor memory usage during media operations

## Integration Hints

### Project Structure Integration
```
WebView/
├── FlashLightManager.swift          # Flashlight control
├── QrcodeVC.swift                   # QR scanning
├── Network.swift                    # Network monitoring
├── GoogleMobileAdsConsentManager.swift
└── Barcode Scanner/                 # Complete QR scanner module
    ├── CameraViewController.swift
    ├── BarcodeScannerViewController.swift
    └── VideoPermissionService.swift
```

### Key Dependencies
- `SwiftQRScanner` - QR code scanning
- `OneSignal` - Push notifications
- `GoogleMobileAds` - Ad integration
- `SwiftyGif` - GIF handling
- `Firebase` - Analytics and services

### Permission Request Patterns
```swift
// Camera permission
AVCaptureDevice.requestAccess(for: .video) { granted in
    DispatchQueue.main.async {
        if granted {
            // Proceed with camera operation
        } else {
            // Handle denial
        }
    }
}

// Location permission
locationManager.requestWhenInUseAuthorization()
```

### Native Feature Exposure to WebView
```swift
// Create JavaScript bridge for native features
func setupNativeBridge() {
    let userScript = WKUserScript(
        source: "window.nativeFeatures = { camera: true, flashlight: true };",
        injectionTime: .atDocumentStart,
        forMainFrameOnly: true
    )
    webView.configuration.userContentController.addUserScript(userScript)
}
```

## Implementation Notes

### Camera Integration
- Configure AVCaptureSession for camera operations
- Handle device orientation changes
- Implement proper camera permission flow
- Support both front and back cameras

### Push Notification Setup
- Configure OneSignal in AppDelegate
- Handle notification permissions properly
- Implement rich notification support
- Set up deep linking from notifications

### Biometric Authentication
- Use LAContext for Face ID/Touch ID
- Implement fallback to passcode
- Handle authentication failures gracefully
- Provide user feedback during authentication

### Network Monitoring
- Use SystemConfiguration for network status
- Implement offline detection
- Handle network state changes
- Provide user feedback for connectivity issues

### Error Handling Best Practices
- Implement try-catch blocks for async operations
- Provide meaningful error messages to users
- Log technical details for debugging
- Implement retry mechanisms for failed operations

### Testing Strategy
- Test on physical devices (camera, biometrics)
- Simulate network conditions
- Test permission flows thoroughly
- Validate background/foreground transitions