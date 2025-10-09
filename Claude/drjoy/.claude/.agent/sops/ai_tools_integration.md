# AI Tools Integration SOP for iOS Swift Development

## AI Tools Setup and Configuration

### Claude Code Integration
```bash
# Claude Code setup for iOS development
# Environment variables
export CLAUDE_API_KEY="your-api-key"
export DEVELOPMENT_TEAM="your-team-id"
export CODE_SIGN_IDENTITY="iPhone Developer"

# Context template for iOS development
IOS_SWIFT_CONTEXT = """
You are helping with iOS native development using Swift and Clean Architecture.
Current tech stack:
- Swift 5.x with UIKit
- Architecture: Clean Architecture with MVP pattern
- UI Framework: UIKit + Texture (AsyncDisplayKit) for performance
- Reactive Programming: RxSwift 6.x
- Dependency Injection: Swinject
- Auto Layout: SnapKit
- Networking: Alamofire with SwiftyJSON
- Local Database: Realm Swift 10.x
- Dependency Management: Carthage with XCFrameworks
- Build System: Xcode projects with multiple modules
- CI/CD: Fastlane with GitHub Actions

Project structure:
- Drjoy.xcodeproj (Main app)
- Domain.xcodeproj (Business logic)
- Data.xcodeproj (Data layer)
- Common.xcodeproj (Shared utilities)

Code standards:
- SwiftLint configuration (150 char warning, 180 char error)
- No force unwrapping, use optional binding
- Weak self in closures to prevent retain cycles
- Functions under 30 lines
- camelCase naming conventions
"""
```

### Cursor IDE Configuration
```json
// .cursor/settings.json
{
  "swift.path": "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swift",
  "swift.enabled": true,
  "ai.contextLength": 200000,
  "ai.model": "claude-3-sonnet-20241022",
  "ai.temperature": 0.1,
  "swift.buildPath": "xcodebuild",
  "swift.sdk": "iphoneos",
  "customRules": [
    "Always use Clean Architecture with MVP pattern",
    "Follow iOS Swift best practices and SwiftLint rules",
    "Use RxSwift for reactive programming",
    "Include comprehensive error handling with do-catch",
    "Prefer weak self in closures to prevent retain cycles",
    "Write tests using XCTest framework",
    "Follow dependency injection with Swinject",
    "Use SnapKit for Auto Layout constraints"
  ],
  "codeCompletion": {
    "showCompletionSnippets": true,
    "includeCompletionsFrom": [
      "frameworks",
      "modules",
      "sdk"
    ]
  }
}
```

## AI-Assisted Development Workflow

### 1. Feature Planning with Claude
```bash
# Template prompt for feature planning
Plan implementation for [feature_name] in iOS Swift:

Context: Read from .agent/system/ project_architecture.md
Requirements: [Specific requirements]
Constraints: [Technical constraints, performance requirements]

Please provide:
1. Clean Architecture overview (Domain/Data/Presentation layers)
2. Xcode project structure and file organization
3. Key classes following MVP pattern
4. RxSwift reactive programming approach
5. Swinject dependency injection setup
6. Implementation steps with testing strategy
7. SwiftLint compliance considerations
```

### 2. Code Generation with Cursor
**Best Practices for iOS Development:**
- Use Cmd+K for code generation
- Provide specific iOS/Swift context
- Reference existing MVP patterns in codebase
- Always include proper error handling
- Follow Swift naming conventions
- Include memory management (weak/unowned self)
- Add RxSwift bindings where appropriate

**Example Prompts:**
```bash
# Generate a new presenter
Create a [FeatureName]Presenter following MVP pattern with:
- RxBasePresenter inheritance
- Weak self in closures
- ActivityIndicator for loading states
- Error handling with PublishRelay
- Dependency injection in init

# Generate API class
Create a Get[FeatureName]API class with:
- Alamofire HTTPMethod override
- SwiftyJSON parsing in convertJson
- Proper error handling
- Path and params methods
```

### 3. Xcode Integration

**AI-Assisted Refactoring:**
```swift
// Example: Claude helps optimize RxSwift chains
// Before (inefficient)
apiClient.request()
    .subscribe(on: MainScheduler.instance)
    .subscribe(onNext: { result in
        // UI update
    })
    .disposed(by: disposeBag)

// After (AI-optimized)
apiClient.request()
    .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
    .observe(on: MainScheduler.instance)
    .subscribe(onNext: { [weak self] result in
        self?.updateUI(with: result)
    })
    .disposed(by: self?.disposeBag ?? DisposeBag())
```

**Code Quality Improvements:**
```swift
// AI suggests SwiftLint-compliant alternatives
// Before (force unwrap)
let user = getUser()!

// After (safe optional binding)
guard let user = getUser() else { return }
```

## Development Environment Setup

### 1. Local Development
```bash
# Verify environment
xcodebuild -version
swift --version
carthage version
swiftlint version

# Build dependencies
carthage bootstrap --platform iOS --use-xcframeworks
carthage build --platform iOS --use-xcframeworks --no-skip-current

# Code quality check
swiftlint
swiftlint autocorrect
```

### 2. AI Tool Integration
```bash
# Claude Code initialization
claude auth login
claude init

# Cursor setup with AI context
cursor --install-extension apple.apple-language
cursor --set-setting ai.context $IOS_SWIFT_CONTEXT
```

## AI-Powered Testing

### 1. Test Generation
```swift
// AI generates unit tests for presenters
class [FeatureName]PresenterTests: XCTestCase {
    var presenter: [FeatureName]Presenter!
    var mockView: Mock[FeatureName]View!
    var mockRepository: Mock[FeatureName]Repository!

    override func setUp() {
        super.setUp()
        // Setup mocks and presenter
    }

    func testLoadFeatureName_Success() {
        // Given
        let expectedEntity = [FeatureName]Entity()
        mockRepository.getFeatureNameReturnValue = .just(expectedEntity)

        // When
        presenter.loadFeatureName(id: "123")

        // Then
        XCTAssertEqual(mockView.onLoadFeatureNameSuccessCallCount, 1)
    }
}
```

### 2. UI Test Generation
```swift
// AI helps generate UI tests
func testFeatureNameFlow_UserInteraction() {
    let app = XCUIApplication()
    app.launch()

    // Navigate to feature
    app.buttons["[FeatureName]"].tap()

    // Verify elements exist
    XCTAssertTrue(app.textFields["featureInput"].exists)
    XCTAssertTrue(app.buttons["saveButton"].exists)

    // Test user interaction
    app.textFields["featureInput"].typeText("Test Value")
    app.buttons["saveButton"].tap()

    // Verify result
    XCTAssertTrue(app.alerts["Success"].exists)
}
```

## AI-Assisted Debugging

### 1. Crash Analysis
```bash
# Claude analyzes crash reports
claude analyze-crash --file crash.crash --context ios-swift
```

### 2. Performance Optimization
```swift
// AI suggests performance improvements
// Memory leak detection
private var cancellables = Set<AnyCancellable>()

// AI suggests proper cancellation
deinit {
    cancellables.removeAll()
}
```

## Related Documentation
- Mobile Development Workflow: `sops/mobile_dev_workflow.md`
- Project Architecture: `system/project_architecture.md`
- iOS Swift Templates: `templates/feature_template.md`
- Code Standards: `../copilot-instructions.md`
- Build Configuration: `fastlane/Fastfile`