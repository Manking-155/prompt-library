# iOS Swift Mobile Development Workflow SOP

## Daily Development Routine

### Morning Setup (5-10 minutes)
1. **Context Review**
   ```bash
   # Read context from documentation
   cat .agent/readme.md
   cat .agent/system/project_architecture.md
   ```
2. **Check Current Tasks**
   - Review current feature requirements
   - Check related SOPs and previous implementations
   - Review GitHub issues and PR discussions
3. **Environment Check**
   ```bash
   # Verify development environment
   xcodebuild -version
   swift --version
   carthage version
   swiftlint version
   git status
   ```

### Environment Preparation
```bash
# Ensure Xcode is properly configured
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
xcode-select -p

# Update dependencies if needed
carthage bootstrap --platform iOS --use-xcframeworks
carthage build --platform iOS --use-xcframeworks --no-skip-current

# Run code quality checks
swiftlint
```

## Feature Implementation Process

### 1. Planning Phase (15-30 minutes)
```bash
# Use plan mode in Claude
/plan implement [feature_name] using iOS Swift Clean Architecture with MVP

# Read relevant documentation first
cat .agent/system/project_architecture.md
cat .agent/templates/feature_template.md
```

**Pre-Implementation Checklist:**
- [ ] Read existing documentation and project structure
- [ ] Define feature requirements clearly
- [ ] Identify which Xcode modules need changes (Drjoy/Domain/Data/Common)
- [ ] Plan repository interfaces and implementations
- [ ] Identify API endpoints needed
- [ ] Plan MVP components (Presenter/View/Controller)
- [ ] Consider RxSwift reactive flows
- [ ] Plan Swinject dependency injection setup
- [ ] Define testing strategy

### 2. Domain Layer Implementation

**Create Domain Structure:**
```bash
# In Domain.xcodeproj
mkdir -p Domain/Domain/Repository/[FeatureName]
mkdir -p Domain/Domain/Entity/[FeatureName]
mkdir -p Domain/Domain/UseCase/[FeatureName]
mkdir -p Domain/Domain/Enum/[FeatureName]
```

**Development Order - Domain:**
1. Create `[FeatureName]Entity.swift` - Business entity
2. Create `[FeatureName]Repos.swift` - Repository protocol
3. Create use cases (`Get[FeatureName]UC.swift`, `Create[FeatureName]UC.swift`, etc.)

### 3. Data Layer Implementation

**Create Data Structure:**
```bash
# In Data.xcodeproj
mkdir -p Data/Data/Repository/[FeatureName]
mkdir -p Data/Data/APIs/APIs/[FeatureName]
mkdir -p Data/Data/Network/[FeatureName]
```

**Development Order - Data:**
1. Create `[FeatureName]RepositoryImpl.swift` - Repository implementation
2. Create API classes (`Get[FeatureName]API.swift`, `Post[FeatureName]API.swift`, etc.)
3. Add network configuration if needed
4. Implement error handling

### 4. Presentation Layer Implementation

**Create Presentation Structure:**
```bash
# In Drjoy.xcodeproj
mkdir -p Drjoy/Presentasion/Controller/[FeatureName]
mkdir -p Drjoy/Presentasion/Presenter/[FeatureName]
mkdir -p Drjoy/Presentasion/View/[FeatureName]
mkdir -p Drjoy/Presentasion/Protocol/[FeatureName]
mkdir -p Drjoy/Presentasion/Provider/[FeatureName]
```

**Development Order - Presentation:**
1. Create `[FeatureName]View.swift` - View protocol
2. Create `[FeatureName]Presenter.swift` - MVP presenter with RxSwift
3. Create `[FeatureName]ViewController.swift` - UIViewController
4. Create custom views and cells if needed
5. Add navigation setup

### 5. Dependency Injection Setup

**Add to Swinject Container:**
```swift
// In Drjoy/Common/DI/AppDIContainer.swift
// MARK: - [FeatureName] Registration
container.register([FeatureName]Repos.self) { resolver in
    let apiClient = resolver.resolve(APIClient.self)!
    return [FeatureName]RepositoryImpl(apiClient: apiClient)
}

container.register([FeatureName]Presenter.self) { resolver in
    let getUC = resolver.resolve(Get[FeatureName]UC.self)!
    let createUC = resolver.resolve(Create[FeatureName]UC.self)!
    // ... other use cases
    return [FeatureName]Presenter(get[FeatureName]UC: getUC,
                                  create[FeatureName]UC: createUC)
}
```

## Code Quality and Testing

### 1. Code Quality Checks
```bash
# Run SwiftLint
swiftlint

# Auto-correct minor issues
swiftlint autocorrect

# Check for specific issues
swiftlint --reporter json > lint-report.json
```

**Quality Checklist:**
- [ ] Follow SwiftLint configuration (150 char line limit)
- [ ] Use weak self in closures
- [ ] Handle optionals safely (no force unwrapping)
- [ ] Include proper error handling
- [ ] Use meaningful variable names
- [ ] Keep functions under 30 lines
- [ ] Remove unused imports and variables

### 2. Testing Implementation

**Create Test Structure:**
```bash
# In DrjoyTests.xcodeproj
mkdir -p DrjoyTests/[FeatureName]
mkdir -p DrjoyUITests/[FeatureName]
```

**Testing Order:**
1. Unit tests for use cases
2. Unit tests for presenters
3. Unit tests for repositories
4. UI tests for view controllers
5. Integration tests

**Test Template:**
```swift
import XCTest
import RxSwift
import RxTest
@testable import Drjoy
@testable import Domain

class [FeatureName]PresenterTests: XCTestCase {
    var presenter: [FeatureName]Presenter!
    var mockView: Mock[FeatureName]View!
    var mockRepository: Mock[FeatureName]Repository!
    var scheduler: TestScheduler!
    var disposeBag: DisposeBag!

    override func setUp() {
        super.setUp()
        scheduler = TestScheduler(initialClock: 0)
        disposeBag = DisposeBag()
        // Setup mocks
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

## Build and Deployment Process

### 1. Local Build
```bash
# Build specific scheme
xcodebuild -workspace Drjoy.xcworkspace \
           -scheme Drjoy-dev \
           -configuration Debug \
           -destination 'platform=iOS Simulator,name=iPhone 14' \
           build

# Run tests
xcodebuild test -workspace Drjoy.xcworkspace \
               -scheme Drjoy-dev \
               -destination 'platform=iOS Simulator,name=iPhone 14'
```

### 2. Fastlane Integration
```bash
# Development build
cd fastlane
fastlane dev

# Release build
fastlane release

# Custom build with options
fastlane build match_type:adhoc export_method:ad-hoc
```

### 3. Git Workflow
```bash
# Create feature branch
git checkout -b feature/[feature_name]

# Commit changes with proper messages
git add .
git commit -m "feat: implement [feature_name] with MVP pattern

- Added [FeatureName]Entity in Domain layer
- Implemented [FeatureName]Repository with Alamofire
- Created [FeatureName]Presenter with RxSwift
- Added [FeatureName]ViewController with UIKit
- Included unit tests

🤖 Generated with [Claude Code](https://claude.ai/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push and create PR
git push origin feature/[feature_name]
```

## Performance Optimization

### 1. Memory Management
```swift
// Always use weak self in closures
apiClient.request()
    .subscribe(onNext: { [weak self] result in
        self?.updateUI(with: result)
    })
    .disposed(by: disposeBag)

// Proper cleanup in deinit
deinit {
    disposeBag = nil
    cancellables.removeAll()
}
```

### 2. RxSwift Best Practices
```swift
// Use proper schedulers
apiClient.request()
    .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
    .observe(on: MainScheduler.instance)
    .subscribe(onNext: { [weak self] result in
        self?.handleResult(result)
    })
    .disposed(by: disposeBag)

// Share streams to avoid multiple subscriptions
let sharedStream = apiClient.request()
    .share(replay: 1, scope: .whileConnected)
```

## Debugging and Troubleshooting

### 1. Common Issues
- **Build Errors**: Check Carthage dependencies and Xcode settings
- **Runtime Crashes**: Check for retain cycles and force unwrapping
- **Memory Leaks**: Use Instruments Leaks tool
- **Performance Issues**: Profile with Time Profiler

### 2. Debugging Tools
```bash
# Enable debug symbols
export NSUnbufferedIO=YES

# Check simulator logs
xcrun simctl spawn booted log stream --predicate 'subsystem == "com.apple.UIKit"'

# Analyze crash reports
xcrun dwarfdump --arch=arm64 --uuid <app-binary>
```

## Documentation Updates

### After Feature Completion:
1. **Update .agent/ documentation**
   - Update `system/project_architecture.md` if architecture changed
   - Create new SOPs if new patterns were introduced
   - Update `templates/feature_template.md` if new patterns discovered

2. **Code Documentation**
   - Add inline documentation for complex logic
   - Update README files in modules
   - Document API endpoints in Data layer

3. **Testing Documentation**
   - Document test coverage requirements
   - Update testing strategies
   - Document performance benchmarks

## Related Documentation
- Project Architecture: `system/project_architecture.md`
- iOS Swift Templates: `templates/feature_template.md`
- AI Tools Integration: `sops/ai_tools_integration.md`
- Code Standards: `../copilot-instructions.md`
- Build Configuration: `fastlane/Fastfile`
- Database Schema: `system/database_schema.md`
- API Documentation: `system/api_endpoints.md`