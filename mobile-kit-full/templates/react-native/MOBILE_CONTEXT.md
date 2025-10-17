# MOBILE_CONTEXT.md - Project Configuration Template

## Project Information
- **Project Name**: {{PROJECT_NAME}}
- **Project Type**: {{PROJECT_TYPE}} (flutter/ios-swift/react-native)
- **Target Platforms**: {{TARGET_PLATFORMS}} (iOS, Android, or both)
- **Minimum iOS Version**: 12.0
- **Minimum Android SDK**: 21
- **Created**: {{CREATED_DATE}}
- **Last Updated**: {{UPDATED_DATE}}

## Technical Stack

### Frontend Framework
- **Primary**: {{FRAMEWORK}} (Flutter, Swift/SwiftUI, React Native)
- **UI Library**: {{UI_LIBRARY}} (Material Design, Cupertino, Custom)
- **State Management**: {{STATE_MANAGEMENT}} (Provider, Riverpod, Redux, etc.)
- **Navigation**: {{NAVIGATION}} (Navigator 2.0, React Navigation, etc.)

### Backend & APIs
- **API Type**: {{API_TYPE}} (REST, GraphQL, Firebase)
- **Base URL**: {{API_BASE_URL}}
- **Authentication**: {{AUTH_METHOD}} (JWT, OAuth, Firebase Auth)
- **Real-time**: {{REALTIME}} (WebSocket, Server-Sent Events, Firebase)

### Database & Storage
- **Local Database**: {{LOCAL_DB}} (SQLite, Hive, CoreData, AsyncStorage)
- **Cloud Database**: {{CLOUD_DB}} (Firebase, AWS, Custom)
- **File Storage**: {{FILE_STORAGE}} (Local, Cloud Storage, CDN)
- **Offline Strategy**: {{OFFLINE_STRATEGY}} (Cache-first, Network-first, Hybrid)

### External Services
- **Analytics**: {{ANALYTICS}} (Firebase Analytics, Mixpanel, Custom)
- **Crash Reporting**: {{CRASH_REPORTING}} (Firebase Crashlytics, Sentry)
- **Push Notifications**: {{PUSH_NOTIFICATIONS}} (Firebase, OneSignal, APNs)
- **Maps**: {{MAPS}} (Google Maps, Apple Maps, OpenStreetMap)
- **Payment**: {{PAYMENT}} (Stripe, Apple Pay, Google Pay, In-App Purchase)

## Architecture & Patterns

### Code Architecture
- **Pattern**: {{ARCHITECTURE_PATTERN}} (MVVM, Clean Architecture, MVC)
- **Dependency Injection**: {{DI_FRAMEWORK}} (GetIt, Provider, Dagger)
- **Code Organization**: {{CODE_ORGANIZATION}} (Feature-based, Layer-based)

### Design Patterns
- **Repository Pattern**: {{REPOSITORY_USAGE}} (Yes/No)
- **Singleton Usage**: {{SINGLETON_USAGE}} (Limited/Avoided)
- **Observer Pattern**: {{OBSERVER_USAGE}} (Yes/No)
- **Factory Pattern**: {{FACTORY_USAGE}} (Yes/No)

## Development Guidelines

### Code Style
- **Language**: {{PRIMARY_LANGUAGE}} (Dart, Swift, JavaScript/TypeScript)
- **Code Formatter**: {{CODE_FORMATTER}} (dartfmt, SwiftFormat, Prettier)
- **Linting**: {{LINTER}} (flutter_lints, SwiftLint, ESLint)
- **Line Length**: {{LINE_LENGTH}} (80/100/120 characters)
- **Naming Convention**: {{NAMING_CONVENTION}} (camelCase, snake_case)

### File Organization
```
{{FILE_STRUCTURE}}
lib/
├── core/
│   ├── constants/
│   ├── errors/
│   ├── network/
│   └── utils/
├── features/
│   ├── authentication/
│   ├── profile/
│   └── home/
├── shared/
│   ├── widgets/
│   ├── models/
│   └── services/
└── main.dart
```

### Performance Guidelines
- **Image Optimization**: Use appropriate formats (WebP, SVG)
- **Bundle Size**: Target < {{BUNDLE_SIZE_TARGET}}MB
- **Memory Usage**: Monitor and optimize for {{MEMORY_TARGET}}MB
- **Battery Usage**: Implement efficient background processing
- **Network**: Implement caching and offline capabilities

## UI/UX Standards

### Design System
- **Color Palette**: {{COLOR_PALETTE}}
  - Primary: {{PRIMARY_COLOR}}
  - Secondary: {{SECONDARY_COLOR}}
  - Accent: {{ACCENT_COLOR}}
  - Error: {{ERROR_COLOR}}
- **Typography**: {{TYPOGRAPHY_SYSTEM}}
  - Primary Font: {{PRIMARY_FONT}}
  - Secondary Font: {{SECONDARY_FONT}}
- **Spacing System**: {{SPACING_SYSTEM}} (8px grid, 4px grid)
- **Border Radius**: {{BORDER_RADIUS_SYSTEM}}

### Platform Guidelines
- **iOS**: Follow Human Interface Guidelines
  - Use native navigation patterns
  - Implement iOS-specific gestures
  - Support Dynamic Type
  - Handle safe areas properly
- **Android**: Follow Material Design Guidelines
  - Use Material components
  - Implement proper elevation
  - Support different screen densities
  - Handle navigation gestures

### Accessibility
- **Screen Reader**: Full VoiceOver/TalkBack support
- **Color Contrast**: WCAG 2.1 AA compliance
- **Touch Targets**: Minimum 44pt (iOS) / 48dp (Android)
- **Dynamic Text**: Support system font sizes
- **High Contrast**: Support high contrast mode

## Testing Strategy

### Test Types
- **Unit Tests**: Business logic and utilities
- **Widget Tests**: UI components and user interactions
- **Integration Tests**: End-to-end user flows
- **Golden Tests**: Visual regression testing
- **Performance Tests**: Memory, CPU, and battery usage

### Test Coverage
- **Target Coverage**: {{TEST_COVERAGE_TARGET}}% minimum
- **Critical Paths**: 100% coverage required
- **UI Tests**: All user-facing features
- **API Tests**: All network interactions

### Test Environments
- **Local Testing**: Emulators and simulators
- **Device Testing**: Physical devices via {{DEVICE_FARM}}
- **Automated Testing**: CI/CD pipeline integration
- **Beta Testing**: {{BETA_TESTING_PLATFORM}} (TestFlight, Firebase App Distribution)

## Security & Privacy

### Data Protection
- **Encryption**: {{ENCRYPTION_METHOD}} for sensitive data
- **Keychain/Keystore**: Secure storage for credentials
- **Network Security**: Certificate pinning, HTTPS only
- **Biometric Auth**: {{BIOMETRIC_SUPPORT}} (Face ID, Touch ID, Fingerprint)

### Privacy Compliance
- **GDPR**: {{GDPR_COMPLIANCE}} compliance implemented
- **CCPA**: {{CCPA_COMPLIANCE}} compliance implemented
- **Data Collection**: {{DATA_COLLECTION_POLICY}}
- **Third-party SDKs**: Audit for privacy compliance

### Security Measures
- **Code Obfuscation**: {{OBFUSCATION_ENABLED}} for release builds
- **Root/Jailbreak Detection**: {{ROOT_DETECTION_ENABLED}}
- **API Security**: Rate limiting, input validation
- **Certificate Pinning**: {{CERT_PINNING_ENABLED}}

## Build & Deployment

### Build Configuration
- **Build Variants**: Debug, Release, Staging
- **Environment Config**: {{ENV_CONFIG_METHOD}}
- **Code Signing**: {{CODE_SIGNING_SETUP}}
- **Build Automation**: {{BUILD_AUTOMATION_TOOL}}

### Release Process
- **Version Strategy**: {{VERSIONING_STRATEGY}} (Semantic, Build number)
- **Release Notes**: Auto-generated from {{RELEASE_NOTES_SOURCE}}
- **Staged Rollout**: {{STAGED_ROLLOUT_PERCENTAGE}}% initial release
- **Rollback Plan**: {{ROLLBACK_STRATEGY}}

### App Store Optimization
- **App Store**: {{APP_STORE_OPTIMIZATION_STRATEGY}}
- **Play Store**: {{PLAY_STORE_OPTIMIZATION_STRATEGY}}
- **Keywords**: {{APP_STORE_KEYWORDS}}
- **Screenshots**: {{SCREENSHOT_STRATEGY}}
- **Localization**: {{LOCALIZATION_LANGUAGES}}

## Monitoring & Analytics

### Performance Monitoring
- **Crash Reporting**: {{CRASH_REPORTING_TOOL}}
- **Performance**: {{PERFORMANCE_MONITORING_TOOL}}
- **Network Monitoring**: {{NETWORK_MONITORING_TOOL}}
- **User Experience**: {{UX_MONITORING_TOOL}}

### Business Analytics
- **User Behavior**: {{USER_ANALYTICS_TOOL}}
- **Conversion Tracking**: {{CONVERSION_TRACKING_SETUP}}
- **A/B Testing**: {{AB_TESTING_PLATFORM}}
- **Custom Events**: {{CUSTOM_EVENTS_STRATEGY}}

## Team & Workflow

### Development Workflow
- **Git Strategy**: {{GIT_WORKFLOW}} (GitFlow, GitHub Flow)
- **Branch Naming**: {{BRANCH_NAMING_CONVENTION}}
- **PR Reviews**: {{PR_REVIEW_REQUIREMENTS}}
- **CI/CD**: {{CICD_PLATFORM}} (GitHub Actions, Bitrise, Codemagic)

### Team Structure
- **Team Size**: {{TEAM_SIZE}} developers
- **Roles**: {{TEAM_ROLES}}
- **Communication**: {{COMMUNICATION_TOOLS}}
- **Project Management**: {{PROJECT_MANAGEMENT_TOOL}}

### Quality Assurance
- **Code Review**: Required for all changes
- **Automated Testing**: Required passing tests
- **Manual Testing**: {{MANUAL_TESTING_STRATEGY}}
- **Bug Tracking**: {{BUG_TRACKING_TOOL}}

## Agent-Specific Instructions

### Mobile Planner
- Consider platform differences early in planning
- Plan for offline capabilities from the start
- Include platform-specific features in roadmap
- Estimate effort for cross-platform compatibility

### UI/UX Designer  
- Follow platform-specific design guidelines
- Design for multiple screen sizes and orientations
- Consider accessibility from the design phase
- Create adaptive layouts for tablets and phones

### Mobile Tester
- Test on physical devices, not just emulators
- Include platform-specific testing scenarios
- Test network conditions and offline behavior
- Verify accessibility features work correctly

### Code Reviewer
- Check for platform-specific best practices
- Verify memory management and performance
- Ensure proper error handling for mobile scenarios
- Review security implications of mobile features

### Mobile Debugger
- Focus on device-specific issues first
- Check memory leaks and performance bottlenecks
- Analyze crash logs from both platforms
- Consider network and battery impact

## Custom Instructions

### Project-Specific Notes
{{CUSTOM_INSTRUCTIONS}}

### Known Issues & Workarounds
{{KNOWN_ISSUES}}

### Future Enhancements
{{FUTURE_ENHANCEMENTS}}

---
*This file is automatically updated by MobileKit agents. Manual changes may be overwritten.*
*Last updated by: {{LAST_UPDATED_BY}} on {{LAST_UPDATED_DATE}}*
