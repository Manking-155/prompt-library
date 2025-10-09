# Dr.JOY iOS App Architecture Overview

## Current Tech Stack

### iOS Native Development
- **Language**: Swift 5.x
- **UI Framework**: UIKit with AsyncDisplayKit (Texture) for performance
- **Architecture Pattern**: Clean Architecture with MVP (Model-View-Presenter)
- **Dependency Injection**: Swinject
- **Reactive Programming**: RxSwift 6.x with RxSwiftExt
- **Auto Layout**: SnapKit
- **Networking**: Alamofire 4.x
- **JSON Parsing**: SwiftyJSON
- **Local Database**: Realm Swift 10.x
- **Image Processing**: PINRemoteImage, WebP support
- **UI Components**: SkeletonView, IQKeyboardManager, FSPagerView

### Cross-Platform & Analytics
- **Firebase Suite**: Analytics, Auth, Database, Crashlytics, Messaging, RemoteConfig, Storage, Performance
- **Validation**: SwiftValidator
- **Keychain Storage**: keychain-swift
- **WebSocket**: SwiftWebSocket
- **File Compression**: ZipArchive
- **Network Debugging**: netfox

### Development Tools & Build System
- **IDE**: Xcode (latest version)
- **Dependency Management**: Carthage with XCFrameworks
- **Code Quality**: SwiftLint with custom configuration
- **Build Automation**: Fastlane
- **Version Control**: Git with GitHub
- **CI/CD**: GitHub Actions
- **Documentation**: Inline with AI assistant integration

## Clean Architecture Implementation

### Multi-Module Structure
The iOS app follows Clean Architecture principles with clearly separated modules:

```
ios-drjoy/
├── Drjoy.xcodeproj/              # Main application project
│   └── Drjoy/
│       └── Presentasion/         # Presentation layer (note: "Presentasion" typo in original)
│           ├── Controller/       # UIViewController implementations
│           ├── Presenter/        # MVP Presenters
│           ├── View/            # Custom Views & UI Components
│           ├── CustomView/      # Specialized UI components
│           ├── Provider/        # Data providers & services
│           ├── Protocol/        # Protocol definitions
│           ├── Manager/         # Business logic managers
│           └── Service/         # External service integrations
├── Domain/                      # Business logic & entities
│   └── Domain.xcodeproj/
│       └── Domain/
│           ├── Repository/      # Repository protocols (Clean Architecture)
│           ├── Entity/          # Business entities
│           └── Enum/            # Domain enums
├── Data/                        # Data layer implementation
│   └── Data.xcodeproj/
│       └── Data/
│           ├── Repository/      # Repository implementations
│           ├── APIs/           # API layer
│           │   ├── APIs/       # Specific API implementations
│           │   └── Configuration/ # API configuration
│           └── Network/        # Networking utilities
└── Common/                      # Shared utilities
    └── Common.xcodeproj/
        └── Common/
            ├── Extension/      # Swift extensions
            ├── Utils/          # Utility classes
            └── Thirdparty/     # Third-party integrations
```

### Key Architecture Patterns

#### 1. MVP (Model-View-Presenter) Pattern
- **Presenters**: Handle business logic, coordinate between View and Model
- **Controllers**: UIViewController implementations (Views in MVP)
- **Protocols**: Define contracts between layers
- **AsyncListPresenter**: Specialized presenter for paginated lists with batch fetching

#### 2. Repository Pattern
- **Domain Layer**: Defines repository protocols (e.g., `AttendanceSettingRepos`, `EditTimesheetRepos`)
- **Data Layer**: Implements repository protocols with actual data sources
- **Abstraction**: Clean separation between business logic and data access

#### 3. Reactive Programming with RxSwift
- **RxBasePresentering**: Base protocol for reactive presenters
- **Async Operations**: Batch fetching with `ASBatchContext` integration
- **Network Retry Logic**: Automatic retry on network reconnection
- **Data Binding**: Reactive binding between UI and data models

## Core Components Analysis

### 1. Presentation Layer
- **AsyncListPresenter**: Generic presenter for paginated lists
  - Supports batch fetching with Texture's `ASBatchContext`
  - Handles network retry logic automatically
  - Manages loading states and pagination
- **Feature-Specific Presenters**: Attendance, Timesheets, Request Management
- **Controllers**: UIViewController implementations with Texture support

### 2. Domain Layer
- **Repository Protocols**: Clean contracts for data access
- **Entities**: Business objects with no external dependencies
- **Use Cases**: Encapsulated business logic operations
- **Domain Services**: Complex business operations

### 3. Data Layer
- **API Layer**: Alamofire-based networking with SwiftyJSON parsing
- **Repository Implementations**: Concrete implementations of domain repositories
- **Network Layer**: Configuration, reachability, and networking utilities
- **Configuration Management**: Client secrets, API endpoints

### 4. Dependency Injection
- **Swinject**: IoC container for dependency management
- **AppDIContainer**: Centralized dependency registration
- **Protocol-Based Injection**: Clean interface-based dependencies

## Performance Optimizations

### 1. Texture (AsyncDisplayKit) Integration
- **Async Rendering**: Non-blocking UI rendering
- **Batch Fetching**: Efficient list loading with `AsyncListPresenter`
- **Memory Management**: Automatic node recycling and memory optimization

### 2. Network Layer
- **RxSwift Integration**: Reactive network operations
- **Automatic Retry**: Network-aware retry logic
- **Image Caching**: PINRemoteImage with WebP support
- **Background Processing**: Efficient background network operations

### 3. Database Operations
- **Realm Swift**: Efficient local database with reactive queries
- **Offline Support**: Local caching with background sync
- **Data Synchronization**: Conflict resolution and sync strategies

## Code Quality & Standards

### SwiftLint Configuration
- **Line Length**: 150 characters (warning), 180 characters (error)
- **File Length**: 700 lines (warning), 1200 lines (error)
- **Function Length**: No strict limit (disabled rule)
- **Force Casts**: Allowed with warning severity
- **Naming Conventions**: camelCase with meaningful names

### Development Workflow
1. **Pre-commit Hooks**: Automatic SwiftLint validation
2. **Code Review**: GitHub-based PR process
3. **Testing**: Unit tests and UI tests with XCTest
4. **Documentation**: Inline documentation with AI assistant integration

## Key Business Domains

### 1. Attendance Management
- **Checking Daily**: Daily attendance tracking
- **Timesheets**: Work hour management
- **Request Management**: Leave/approval workflows
- **Settings**: Configuration and preferences

### 2. Communication
- **Real-time Features**: WebSocket integration
- **Push Notifications**: Firebase Messaging
- **File Sharing**: Image and document handling

### 3. User Management
- **Authentication**: Firebase Auth integration
- **Profiles**: User data management
- **Permissions**: Role-based access control

## Integration Points

### External Services
- **Firebase**: Analytics, Auth, Database, Storage, Messaging
- **Backend APIs**: RESTful services with Alamofire
- **Keychain Storage**: Secure credential management
- **Network Debugging**: netfox for development debugging

### Third-Party Libraries
- **Texture**: High-performance UI framework
- **RxSwift**: Reactive programming
- **SnapKit**: Auto Layout DSL
- **Swinject**: Dependency injection
- **Realm**: Local database

## Related Documentation
- Database Schema: `system/database_schema.md`
- API Documentation: `system/api_endpoints.md`
- Development Workflow: `sops/mobile_dev_workflow.md`
- AI Tools Integration: `sops/ai_tools_integration.md`