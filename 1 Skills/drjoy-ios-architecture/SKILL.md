---
name: Dr.JOY iOS Clean Architecture
description: Expert guidance for Dr.JOY iOS app development using Clean Architecture with MVP, RxSwift, Texture (AsyncDisplayKit), and Swinject. Use when developing features for Dr.JOY attendance management app, implementing MVP presenters, integrating with Firebase services, or debugging performance issues with Texture framework.
version: 1.0.0
dependencies: Swift>=5.0, RxSwift>=6.2.0, Texture, Swinject, Alamofire>=4.9.1, Realm>=10.0, SnapKit>=4.2.0
---

# Dr.JOY iOS Clean Architecture

Expert skill for building and maintaining the Dr.JOY iOS application using Clean Architecture principles with MVP pattern, RxSwift reactive programming, and Texture (AsyncDisplayKit) for high-performance UI.

## When to use this skill

Use this skill when you need to:
- Develop new features for Dr.JOY attendance management app
- Implement MVP presenters with RxSwift
- Create high-performance lists with Texture (AsyncDisplayKit)
- Set up dependency injection with Swinject
- Integrate Firebase services (Auth, Analytics, Messaging, etc.)
- Debug memory leaks or performance issues
- Implement reactive programming patterns with RxSwift
- Create custom UI components with SnapKit
- Work with Realm database for offline support

## Tech Stack Overview

### Core Frameworks
- **Language**: Swift 5.x
- **Architecture**: Clean Architecture + MVP (Model-View-Presenter)
- **UI Framework**: UIKit with Texture (AsyncDisplayKit)
- **Reactive Programming**: RxSwift 6.x + RxSwiftExt
- **Dependency Injection**: Swinject
- **Networking**: Alamofire 4.x with SwiftyJSON
- **Database**: Realm Swift 10.x
- **Auto Layout**: SnapKit
- **Firebase**: Full suite (Auth, Analytics, Crashlytics, Messaging, etc.)

### Project Structure

```
ios-drjoy/
├── Drjoy.xcodeproj/              # Main app
│   └── Drjoy/Presentasion/
│       ├── Controller/           # UIViewControllers (Views in MVP)
│       ├── Presenter/            # MVP Presenters
│       ├── View/                # Custom UI components
│       ├── Protocol/            # View protocols
│       └── Provider/            # Data providers
├── Domain/                      # Business logic layer
│   └── Domain/
│       ├── Repository/          # Repository protocols
│       ├── Entity/              # Business entities
│       └── UseCase/             # Use cases
├── Data/                        # Data layer
│   └── Data/
│       ├── Repository/          # Repository implementations
│       └── APIs/                # API implementations
└── Common/                      # Shared utilities
    └── Common/
        ├── Extension/           # Swift extensions
        └── Utils/               # Utility classes
```

## Core Architecture Patterns

### 1. MVP Pattern with RxSwift

**Presenter Base Class**:
```swift
class RxBasePresenter<T>: Presenter {
    weak var view: T?
    private let disposeBag = DisposeBag()
    private let isLoading = ActivityIndicator()

    func attachView(_ view: T) {
        self.view = view
        setupBindings()
    }

    func detachView() {
        self.view = nil
    }

    private func setupBindings() {
        isLoading
            .drive(onNext: { [weak self] isLoading in
                isLoading ? self?.view?.onShowProgress() : self?.view?.onDismissProgress()
            })
            .disposed(by: disposeBag)
    }
}
```

**Feature Presenter Example**:
```swift
class AttendancePresenter: RxBasePresenter<AttendanceView> {
    private let getAttendanceUC: GetAttendanceUC
    private let disposeBag = DisposeBag()

    init(getAttendanceUC: GetAttendanceUC) {
        self.getAttendanceUC = getAttendanceUC
        super.init()
    }

    func loadAttendance(date: Date) {
        getAttendanceUC
            .exe(date: date)
            .trackActivity(isLoading)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
            .observe(on: MainScheduler.instance)
            .subscribe(
                onNext: { [weak self] attendance in
                    self?.view?.onLoadAttendanceSuccess(attendance)
                },
                onError: { [weak self] error in
                    self?.view?.onShowError(error.localizedDescription)
                }
            )
            .disposed(by: disposeBag)
    }
}
```

### 2. Repository Pattern

**Domain Layer (Protocol)**:
```swift
public protocol AttendanceRepos {
    func getAttendance(date: Date) -> Observable<AttendanceEntity>
    func checkIn(location: Location) -> Observable<Void>
    func checkOut(location: Location) -> Observable<Void>
}
```

**Data Layer (Implementation)**:
```swift
class AttendanceRepositoryImpl: AttendanceRepos {
    private let apiClient: APIClient

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func getAttendance(date: Date) -> Observable<AttendanceEntity> {
        return apiClient.request(GetAttendanceAPI(date: date))
    }
}
```

### 3. AsyncListPresenter for Pagination

```swift
class AttendanceListPresenter: AsyncListPresenter<AttendanceCell, AttendanceEntity> {
    private let getAttendancesUC: GetAttendancesUC

    override func loadData(page: Int, completion: @escaping ([AttendanceEntity], Bool) -> Void) {
        getAttendancesUC
            .exe(page: page, pageSize: 20)
            .subscribe(
                onNext: { entities in
                    let hasMore = entities.count >= 20
                    completion(entities, hasMore)
                },
                onError: { error in
                    completion([], false)
                }
            )
            .disposed(by: disposeBag)
    }

    override func cellNode(for entity: AttendanceEntity) -> AttendanceCell {
        return AttendanceCell(entity: entity)
    }
}
```

### 4. Texture (AsyncDisplayKit) Integration

**Custom Cell Node**:
```swift
class AttendanceCell: ASCellNode {
    private let nameTextNode = ASTextNode()
    private let timeTextNode = ASTextNode()
    private let statusNode = ASImageNode()

    init(entity: AttendanceEntity) {
        super.init()
        automaticallyManagesSubnodes = true

        nameTextNode.attributedText = NSAttributedString(
            string: entity.userName,
            attributes: [.font: UIFont.systemFont(ofSize: 16)]
        )

        timeTextNode.attributedText = NSAttributedString(
            string: entity.checkInTime,
            attributes: [.font: UIFont.systemFont(ofSize: 14)]
        )
    }

    override func layoutSpecThatFits(_ constrainedSize: ASSizeRange) -> ASLayoutSpec {
        let textStack = ASStackLayoutSpec.vertical()
        textStack.children = [nameTextNode, timeTextNode]
        textStack.spacing = 4

        let mainStack = ASStackLayoutSpec.horizontal()
        mainStack.children = [textStack, statusNode]
        mainStack.justifyContent = .spaceBetween

        return ASInsetLayoutSpec(insets: UIEdgeInsets(top: 12, left: 16, bottom: 12, right: 16), child: mainStack)
    }
}
```

### 5. Dependency Injection with Swinject

**DI Container Setup**:
```swift
class AppDIContainer {
    let container = Container()

    func registerDependencies() {
        // Networking
        container.register(APIClient.self) { _ in
            APIClient()
        }.inObjectScope(.container)

        // Repository
        container.register(AttendanceRepos.self) { resolver in
            AttendanceRepositoryImpl(apiClient: resolver.resolve(APIClient.self)!)
        }

        // Use Case
        container.register(GetAttendanceUC.self) { resolver in
            GetAttendanceUC(repository: resolver.resolve(AttendanceRepos.self)!)
        }

        // Presenter
        container.register(AttendancePresenter.self) { resolver in
            AttendancePresenter(getAttendanceUC: resolver.resolve(GetAttendanceUC.self)!)
        }
    }
}
```

## Feature Implementation Workflow

### 1. Create Domain Layer
```swift
// Domain/Entity/AttendanceEntity.swift
public struct AttendanceEntity {
    public let id: String
    public let userId: String
    public let checkInTime: Date
    public let checkOutTime: Date?
    public let status: AttendanceStatus
}

// Domain/Repository/AttendanceRepos.swift
public protocol AttendanceRepos {
    func getAttendance(id: String) -> Observable<AttendanceEntity>
}

// Domain/UseCase/GetAttendanceUC.swift
public class GetAttendanceUC {
    private let repository: AttendanceRepos

    public init(repository: AttendanceRepos) {
        self.repository = repository
    }

    public func exe(id: String) -> Observable<AttendanceEntity> {
        return repository.getAttendance(id: id)
    }
}
```

### 2. Create Data Layer
```swift
// Data/APIs/GetAttendanceAPI.swift
class GetAttendanceAPI: API<AttendanceEntity> {
    private let attendanceId: String

    init(attendanceId: String) {
        self.attendanceId = attendanceId
        super.init()
    }

    override func path() -> String {
        return "/api/attendance/\(attendanceId)"
    }

    override func method() -> HTTPMethod {
        return .get
    }

    override func convertJson(_ val: Any) throws -> AttendanceEntity {
        guard let dict = val as? NSDictionary else {
            throw APIError.invalidResponse
        }
        return AttendanceEntity(dict)
    }
}

// Data/Repository/AttendanceRepositoryImpl.swift
class AttendanceRepositoryImpl: AttendanceRepos {
    private let apiClient: APIClient

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func getAttendance(id: String) -> Observable<AttendanceEntity> {
        return apiClient.request(GetAttendanceAPI(attendanceId: id))
    }
}
```

### 3. Create Presentation Layer
```swift
// Drjoy/Presentasion/Protocol/AttendanceView.swift
protocol AttendanceView: AnyObject {
    func onShowProgress()
    func onDismissProgress()
    func onLoadAttendanceSuccess(_ entity: AttendanceEntity)
    func onShowError(_ message: String)
}

// Drjoy/Presentasion/Presenter/AttendancePresenter.swift
class AttendancePresenter: RxBasePresenter<AttendanceView> {
    private let getAttendanceUC: GetAttendanceUC
    private let disposeBag = DisposeBag()

    init(getAttendanceUC: GetAttendanceUC) {
        self.getAttendanceUC = getAttendanceUC
    }

    func loadAttendance(id: String) {
        getAttendanceUC
            .exe(id: id)
            .trackActivity(isLoading)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
            .observe(on: MainScheduler.instance)
            .subscribe(
                onNext: { [weak self] entity in
                    self?.view?.onLoadAttendanceSuccess(entity)
                },
                onError: { [weak self] error in
                    self?.view?.onShowError(error.localizedDescription)
                }
            )
            .disposed(by: disposeBag)
    }
}

// Drjoy/Presentasion/Controller/AttendanceViewController.swift
class AttendanceViewController: UIViewController {
    var presenter: AttendancePresenter!

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        presenter.attachView(self)
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        presenter.detachView()
    }
}

extension AttendanceViewController: AttendanceView {
    func onShowProgress() {
        // Show loading indicator
    }

    func onDismissProgress() {
        // Hide loading indicator
    }

    func onLoadAttendanceSuccess(_ entity: AttendanceEntity) {
        // Update UI with attendance data
    }

    func onShowError(_ message: String) {
        // Show error alert
    }
}
```

## Best Practices

### RxSwift Patterns
✅ Always use `[weak self]` in closures to prevent retain cycles
✅ Dispose subscriptions properly with DisposeBag
✅ Use `trackActivity()` for loading states
✅ Subscribe on background, observe on main thread
✅ Handle errors in `onError` handler

### Memory Management
✅ Use `weak` references for delegates and view references
✅ Dispose of observers in `deinit` or when view disappears
✅ Avoid retain cycles in Texture node closures
✅ Use `automaticallyManagesSubnodes = true` in Texture

### Performance
✅ Use Texture (AsyncDisplayKit) for complex lists
✅ Implement batch fetching with `AsyncListPresenter`
✅ Cache images with PINRemoteImage
✅ Use background threads for heavy computations
✅ Profile with Instruments regularly

### Code Quality
✅ Follow SwiftLint rules (150 char line limit)
✅ Use meaningful variable names (camelCase)
✅ Keep functions under 30 lines
✅ Add MARK: comments for organization
✅ Document complex logic with comments

## Common Patterns

### Firebase Integration
```swift
// Firebase Analytics
Analytics.logEvent("attendance_checked", parameters: [
    "user_id": userId,
    "timestamp": Date()
])

// Firebase Messaging
Messaging.messaging().token { token, error in
    if let token = token {
        // Send token to backend
    }
}
```

### Realm Database
```swift
class AttendanceRealmObject: Object {
    @objc dynamic var id = ""
    @objc dynamic var userId = ""
    @objc dynamic var checkInTime = Date()

    override static func primaryKey() -> String? {
        return "id"
    }
}

// Save to Realm
let realm = try! Realm()
try! realm.write {
    realm.add(attendance, update: .modified)
}

// Query from Realm
let attendances = realm.objects(AttendanceRealmObject.self)
    .filter("userId == %@", currentUserId)
```

### Network Retry Logic
```swift
func requestWithRetry<T>(_ api: API<T>) -> Observable<T> {
    return apiClient.request(api)
        .retryWhen { errors in
            errors.enumerated().flatMap { attempt, error -> Observable<Int> in
                if attempt < 3 {
                    return Observable<Int>.timer(.seconds(2), scheduler: MainScheduler.instance)
                }
                return Observable.error(error)
            }
        }
}
```

## Resources

For detailed examples, templates, and advanced patterns, see:
- `reference.md` - Complete API reference and implementation details
- `examples.md` - Real-world feature implementations
- `templates/` - Code templates for common features

## Version History

- **1.0.0** (Oct 2025): Initial release with Dr.JOY iOS architecture patterns
