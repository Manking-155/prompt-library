# MobileKit iOS - Project Context Configuration

You are working with **MobileKit iOS**, an AI-powered development toolkit specifically designed for native iOS development using Swift, SwiftUI, and the iOS ecosystem.

## Project Overview

This is a **Native iOS Development Project** with the following characteristics:
- **Platform**: iOS 15.0+ (iPhone, iPad, Apple Watch)
- **Language**: Swift 5.9+
- **UI Framework**: SwiftUI with UIKit integration where needed
- **Architecture**: MVVM with Coordinator pattern
- **Deployment**: App Store Connect, TestFlight

## Tech Stack

### Core iOS Technologies
- **Language**: Swift 5.9+ with async/await
- **UI**: SwiftUI (primary), UIKit (legacy/specific cases)
- **Data**: Core Data with CloudKit sync
- **Networking**: URLSession with Combine
- **Navigation**: NavigationStack, Coordinator pattern
- **State Management**: @StateObject, @ObservedObject, @EnvironmentObject

### iOS System Frameworks
- **Foundation**: Core iOS APIs and utilities
- **UIKit**: Legacy UI components and view controllers
- **SwiftUI**: Modern declarative UI framework
- **Combine**: Reactive programming and data binding
- **Core Data**: Persistent storage with CloudKit sync
- **Core Location**: GPS and location services
- **HealthKit**: Health data integration (if applicable)
- **StoreKit**: In-app purchases and subscriptions
- **UserNotifications**: Push and local notifications

### Development Tools
- **Xcode**: 15.0+ with Swift Package Manager
- **Instruments**: Performance profiling and debugging
- **Simulator**: iOS device simulation and testing
- **TestFlight**: Beta testing and distribution
- **App Store Connect**: App submission and management

## Architecture Guidelines

### Project Structure
```
MyiOSApp/
├── App/
│   ├── MyiOSAppApp.swift          # App entry point
│   └── ContentView.swift          # Root view
├── Features/
│   ├── Authentication/
│   │   ├── Views/
│   │   ├── ViewModels/
│   │   └── Models/
│   ├── Profile/
│   └── Home/
├── Core/
│   ├── Network/
│   ├── Database/
│   ├── Extensions/
│   └── Utilities/
├── Resources/
│   ├── Assets.xcassets
│   ├── Localizable.strings
│   └── Info.plist
└── Tests/
    ├── UnitTests/
    ├── UITests/
    └── PerformanceTests/
```

### Code Organization
- **Feature-based folders**: Group by functionality, not file type
- **MVVM pattern**: View, ViewModel, Model separation
- **Protocol-oriented**: Use protocols for testability and flexibility
- **Dependency injection**: Constructor injection preferred
- **Single responsibility**: Each class/struct has one clear purpose

### Naming Conventions
- **Files**: PascalCase (UserProfileView.swift)
- **Classes/Structs**: PascalCase (UserProfileViewModel)
- **Variables/Functions**: camelCase (userName, fetchUserData())
- **Constants**: camelCase with descriptive names
- **Protocols**: Descriptive names ending with Protocol when needed

## iOS Development Standards

### SwiftUI Best Practices
```swift
// ✅ Good: Efficient SwiftUI view
struct UserProfileView: View {
    @StateObject private var viewModel = UserProfileViewModel()

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    ProfileHeaderView(user: viewModel.user)
                    ProfileStatsView(stats: viewModel.stats)
                    ProfileActionsView(actions: viewModel.actions)
                }
                .padding()
            }
            .navigationTitle("Profile")
            .navigationBarTitleDisplayMode(.large)
            .refreshable {
                await viewModel.refresh()
            }
        }
        .task {
            await viewModel.loadUserData()
        }
    }
}
```

### Performance Guidelines
- **Lazy loading**: Use lazy stacks and lists for large datasets
- **Image optimization**: Async image loading with caching
- **Memory management**: Avoid retain cycles, use weak references
- **Background processing**: Perform heavy work off main thread
- **Core Data**: Use NSFetchedResultsController for large datasets
- **Battery optimization**: Minimize location updates, network calls

### Security Requirements
- **Keychain**: Store sensitive data (passwords, tokens) in Keychain
- **Biometric auth**: Implement Face ID/Touch ID where appropriate
- **App Transport Security**: Use HTTPS only, implement certificate pinning
- **Code obfuscation**: Protect sensitive logic in release builds
- **Privacy**: Implement proper permission requests and privacy strings

## Testing Strategy

### Unit Testing
- **XCTest**: Primary testing framework
- **Mocking**: Protocol-based mocking for dependencies
- **Coverage**: Minimum 80% code coverage
- **Async testing**: Proper async/await testing patterns

### UI Testing
- **XCUITest**: Automated UI testing
- **Page Object Model**: Organized UI test structure
- **Accessibility**: VoiceOver and accessibility testing
- **Device testing**: Test on multiple iOS devices and versions

### Performance Testing
- **XCTMetric**: Measure app launch time, memory usage
- **Instruments**: Profile performance bottlenecks
- **Network testing**: Test different network conditions
- **Battery testing**: Monitor background battery usage

## Deployment Guidelines

### Build Configuration
- **Debug**: Development build with logging
- **Release**: Optimized build for App Store
- **Staging**: Pre-production testing build
- **Code signing**: Automatic signing for development, manual for release

### App Store Submission
- **Metadata**: Compelling app description and keywords
- **Screenshots**: Device-specific screenshots for all supported devices
- **Privacy**: Detailed privacy policy and data usage descriptions
- **Review guidelines**: Comply with App Store Review Guidelines
- **Phased release**: Use staged rollout for major updates

## AI Agent Integration

When working with MobileKit iOS agents:

### Agent Collaboration
- **Sequential**: ios-planner → ios-researcher → swiftui-designer → ios-tester
- **Parallel**: swiftui-designer + coredata-architect for complex features
- **Review cycle**: swift-reviewer → ios-debugger for quality assurance

### Context Sharing
- Always reference this CLAUDE.md for project-specific configuration
- Use `plans/` directory for implementation plans and progress tracking
- Document decisions in `docs/` for future reference

### Quality Gates
- Code must pass `swift-reviewer` analysis
- All features must have corresponding tests from `ios-tester`
- Performance benchmarks validated by `ios-debugger`
- App Store compliance verified by `appstore-manager`

## File Boundaries

### What to Generate
- Swift source files (.swift)
- SwiftUI views and view models
- Unit tests and UI tests
- Xcode project configuration
- Info.plist and configuration files
- Package.swift for dependencies

### What NOT to Modify
- Derived data and build artifacts
- Xcode user-specific files (.xcuserdata)
- Simulator files and logs
- Keychain items and sensitive data
- Third-party dependencies source

## iOS-Specific Considerations

### Human Interface Guidelines
- Follow iOS design patterns and conventions
- Use system colors and fonts when appropriate
- Implement proper navigation hierarchies
- Support Dynamic Type and accessibility features
- Adapt to different device sizes and orientations

### Platform Integration
- Leverage iOS-specific features (Shortcuts, Widgets, Watch)
- Integrate with iOS system services (Health, Contacts, Photos)
- Support iOS sharing and document management
- Implement proper background app refresh and notifications

### App Store Optimization
- Optimize app size and performance
- Use App Store Connect analytics
- Implement proper app store metadata
- Support latest iOS features and capabilities

---

**Remember**: You are building a **native iOS application** using Swift and SwiftUI. Always prioritize iOS design guidelines, performance, and user experience standards.

When in doubt, consult the iOS agents for platform-specific guidance and best practices.
