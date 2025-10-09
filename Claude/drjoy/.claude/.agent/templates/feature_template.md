# iOS Swift Feature Implementation Template

## Feature Overview
- **Feature Name**: [Feature name]
- **Platform**: iOS Native (Swift)
- **Architecture Pattern**: Clean Architecture with MVP
- **Complexity**: [Low/Medium/High]
- **Estimated Time**: [Timeline]

## Technical Requirements

### Dependencies (Add to Cartfile if needed)
```
# Add required dependencies to Cartfile
github "dr-joy/Alamofire.git" "drjoy-4.9.1"
github "dr-joy/RxSwift.git" "drjoy-6.2.0"
github "dr-joy/SnapKit.git" "drjoy-4.2.0"
```

### Architecture Components
- **Pattern**: Clean Architecture (Domain/Data/Presentation layers)
- **UI Framework**: UIKit with Texture (AsyncDisplayKit) for performance
- **Reactive Programming**: RxSwift 6.x
- **Dependency Injection**: Swinject
- **Auto Layout**: SnapKit
- **Networking**: Alamofire with SwiftyJSON
- **Local Database**: Realm Swift

## Implementation Checklist

### 1. Domain Layer (Domain.xcodeproj)
```
Domain/Domain/
├── Repository/
│   └── [FeatureName]Repos.swift           # Repository protocol
├── Entity/
│   └── [FeatureName]Entity.swift          # Business entity
└── Enum/
    └── [FeatureName]Enum.swift            # Domain enums
```

#### Repository Protocol Template:
```swift
//
//  [FeatureName]Repos.swift
//  Domain
//
//  Created by [Developer] on [Date].
//

import Foundation
import RxSwift

public protocol [FeatureName]Repos {
    func get[FeatureName](id: String) -> Observable<[FeatureName]Entity>
    func create[FeatureName](_ entity: [FeatureName]Entity) -> Observable<Void>
    func update[FeatureName](_ entity: [FeatureName]Entity) -> Observable<[FeatureName]Entity>
    func delete[FeatureName](id: String) -> Observable<Void>
}
```

### 2. Data Layer (Data.xcodeproj)
```
Data/Data/
├── Repository/
│   └── [FeatureName]RepositoryImpl.swift   # Repository implementation
└── APIs/APIs/
    ├── Get[FeatureName]API.swift          # GET API
    ├── Post[FeatureName]API.swift         # POST API
    └── Put[FeatureName]API.swift          # PUT API
```

#### Repository Implementation Template:
```swift
//
//  [FeatureName]RepositoryImpl.swift
//  Data
//
//  Created by [Developer] on [Date].
//

import Foundation
import RxSwift
import Domain

class [FeatureName]RepositoryImpl: [FeatureName]Repos {

    private let apiClient: APIClient

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func get[FeatureName](id: String) -> Observable<[FeatureName]Entity> {
        return apiClient.request(Get[FeatureName]API(id: id))
    }

    func create[FeatureName](_ entity: [FeatureName]Entity) -> Observable<Void> {
        return apiClient.request(Post[FeatureName]API(entity: entity))
    }

    func update[FeatureName](_ entity: [FeatureName]Entity) -> Observable<[FeatureName]Entity> {
        return apiClient.request(Put[FeatureName]API(entity: entity))
    }

    func delete[FeatureName](id: String) -> Observable<Void> {
        return apiClient.request(Delete[FeatureName]API(id: id))
    }
}
```

#### API Implementation Template:
```swift
//
//  Get[FeatureName]API.swift
//  Data
//
//  Created by [Developer] on [Date].
//

import Foundation
import Alamofire
import SwiftyJSON

class Get[FeatureName]API: API<[FeatureName]Entity> {

    private let featureId: String

    init(featureId: String) {
        self.featureId = featureId
        super.init()
    }

    override func path() -> String {
        return "/api/[feature_name]/\(featureId)"
    }

    override func method() -> HTTPMethod {
        return .get
    }

    override func convertJson(_ val: Any) throws -> [FeatureName]Entity {
        guard let jsonArray = val as? [NSDictionary] else {
            throw APIError.invalidResponse
        }
        return jsonArray.map { [FeatureName]Entity($0) }
    }
}
```

### 3. Presentation Layer (Drjoy.xcodeproj)
```
Drjoy/Presentasion/
├── Controller/[FeatureName]/
│   ├── [FeatureName]ViewController.swift     # Main view controller
│   └── [FeatureName]ListViewController.swift # List view controller
├── Presenter/[FeatureName]/
│   ├── [FeatureName]Presenter.swift         # Main presenter
│   └── [FeatureName]ListPresenter.swift     # List presenter (if needed)
├── View/[FeatureName]/
│   ├── [FeatureName]View.swift              # Custom view components
│   └── [FeatureName]Cell.swift              # Table/collection view cells
├── Protocol/[FeatureName]/
│   └── [FeatureName]View.swift              # View protocol
└── Provider/[FeatureName]/
    └── [FeatureName]Provider.swift          # Data providers
```

#### Presenter Template:
```swift
//
//  [FeatureName]Presenter.swift
//  Drjoy
//
//  Created by [Developer] on [Date].
//  Copyright © [Year] Dr.JOY No,054. All rights reserved.
//

import UIKit
import RxSwift
import RxCocoa
import Domain

class [FeatureName]Presenter: RxBasePresenter<[FeatureName]ViewController], Presenter {

    // MARK: - UI Properties
    typealias T = [FeatureName]View

    weak var view: [FeatureName]View?

    // MARK: - Properties
    private let get[FeatureName]UC: Get[FeatureName]UC
    private let create[FeatureName]UC: Create[FeatureName]UC
    private let update[FeatureName]UC: Update[FeatureName]UC
    private let delete[FeatureName]UC: Delete[FeatureName]UC

    private let disposeBag = DisposeBag()
    private let isLoading = ActivityIndicator()
    private let errorRelay = PublishRelay<String>()

    // MARK: - Callbacks
    var onError: ((String) -> Void)?
    var onLoadingStateChanged: ((Bool) -> Void)?
    var onDataUpdated: (([FeatureName]Entity) -> Void)?

    // MARK: - Lifecycle
    func attachView(_ view: [FeatureName]View) {
        self.view = view
        setupBindings()
    }

    func detachView() {
        self.view = nil
    }

    init(get[FeatureName]UC: Get[FeatureName]UC,
         create[FeatureName]UC: Create[FeatureName]UC,
         update[FeatureName]UC: Update[FeatureName]UC,
         delete[FeatureName]UC: Delete[FeatureName]UC) {
        self.get[FeatureName]UC = get[FeatureName]UC
        self.create[FeatureName]UC = create[FeatureName]UC
        self.update[FeatureName]UC = update[FeatureName]UC
        self.delete[FeatureName]UC = delete[FeatureName]UC
        super.init()
    }

    // MARK: - Private Methods
    private func setupBindings() {
        isLoading
            .drive(onNext: { [weak self] isLoading in
                self?.onLoadingStateChanged?(isLoading)
                isLoading ? self?.view?.onShowProgress() : self?.view?.onDismissProgress()
            })
            .disposed(by: disposeBag)

        errorRelay
            .bind(onNext: { [weak self] errorMessage in
                self?.onError?(errorMessage)
                self?.view?.onShowError(errorMessage)
            })
            .disposed(by: disposeBag)
    }

    // MARK: - Public Methods
    func load[FeatureName](id: String) {
        get[FeatureName]UC
            .exe(id: id)
            .trackActivity(isLoading)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
            .observe(on: MainScheduler.instance)
            .subscribe(
                onNext: { [weak self] entity in
                    self?.onDataUpdated?([entity])
                    self?.view?.onLoad[FeatureName]Success(entity)
                },
                onError: { [weak self] error in
                    self?.errorRelay.accept(error.localizedDescription)
                }
            )
            .disposed(by: disposeBag)
    }

    func create[FeatureName](_ entity: [FeatureName]Entity) {
        create[FeatureName]UC
            .exe(entity: entity)
            .trackActivity(isLoading)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
            .observe(on: MainScheduler.instance)
            .subscribe(
                onNext: { [weak self] in
                    self?.view?.onCreate[FeatureName]Success()
                },
                onError: { [weak self] error in
                    self?.errorRelay.accept(error.localizedDescription)
                }
            )
            .disposed(by: disposeBag)
    }
}
```

#### View Controller Template:
```swift
//
//  [FeatureName]ViewController.swift
//  Drjoy
//
//  Created by [Developer] on [Date].
//  Copyright © [Year] Dr.JOY No,054. All rights reserved.
//

import UIKit
import RxSwift

class [FeatureName]ViewController: UIViewController {

    // MARK: - IBOutlets
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!

    // MARK: - Properties
    var presenter: [FeatureName]Presenter!
    private let disposeBag = DisposeBag()

    // MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupBindings()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        presenter.attachView(self)
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        presenter.detachView()
    }

    // MARK: - Private Methods
    private func setupUI() {
        title = "[Feature Name]"
        setupTableView()
        setupNavigationBar()
    }

    private func setupTableView() {
        tableView.delegate = self
        tableView.dataSource = self
        tableView.register(UINib(nibName: "[FeatureName]Cell", bundle: nil),
                          forCellReuseIdentifier: "[FeatureName]Cell")
    }

    private func setupNavigationBar() {
        // Setup navigation bar items
    }

    private func setupBindings() {
        presenter.onLoadingStateChanged = { [weak self] isLoading in
            DispatchQueue.main.async {
                self?.activityIndicator?.isHidden = !isLoading
                isLoading ? self?.activityIndicator?.startAnimating() : self?.activityIndicator?.stopAnimating()
            }
        }

        presenter.onError = { [weak self] errorMessage in
            DispatchQueue.main.async {
                self?.showAlert(title: "Error", message: errorMessage)
            }
        }
    }

    private func showAlert(title: String, message: String) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
}

// MARK: - [FeatureName]View Protocol
extension [FeatureName]ViewController: [FeatureName]View {

    func onShowProgress() {
        activityIndicator?.isHidden = false
        activityIndicator?.startAnimating()
    }

    func onDismissProgress() {
        activityIndicator?.isHidden = true
        activityIndicator?.stopAnimating()
    }

    func onLoad[FeatureName]Success(_ entity: [FeatureName]Entity) {
        // Update UI with loaded data
    }

    func onCreate[FeatureName]Success() {
        // Handle successful creation
    }

    func onShowError(_ message: String) {
        showAlert(title: "Error", message: message)
    }
}

// MARK: - UITableViewDataSource, UITableViewDelegate
extension [FeatureName]ViewController: UITableViewDataSource, UITableViewDelegate {

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // Return number of items
        return 0
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: "[FeatureName]Cell", for: indexPath) as? [FeatureName]Cell else {
            return UITableViewCell()
        }

        // Configure cell
        return cell
    }

    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        // Handle cell selection
    }
}
```

#### View Protocol Template:
```swift
//
//  [FeatureName]View.swift
//  Drjoy
//
//  Created by [Developer] on [Date].
//  Copyright © [Year] Dr.JOY No,054. All rights reserved.
//

import Foundation

protocol [FeatureName]View: AnyObject {
    func onShowProgress()
    func onDismissProgress()
    func onLoad[FeatureName]Success(_ entity: [FeatureName]Entity)
    func onCreate[FeatureName]Success()
    func onShowError(_ message: String)
}
```

### 4. Use Cases (Domain Layer)
```
Domain/Domain/
└── UseCase/[FeatureName]/
    ├── Get[FeatureName]UC.swift
    ├── Create[FeatureName]UC.swift
    ├── Update[FeatureName]UC.swift
    └── Delete[FeatureName]UC.swift
```

#### Use Case Template:
```swift
//
//  Get[FeatureName]UC.swift
//  Domain
//
//  Created by [Developer] on [Date].
//

import Foundation
import RxSwift

class Get[FeatureName]UC {

    private let repository: [FeatureName]Repos

    init(repository: [FeatureName]Repos) {
        self.repository = repository
    }

    func exe(id: String) -> Observable<[FeatureName]Entity> {
        return repository.get[FeatureName](id: id)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
    }
}
```

### 5. Dependency Injection
Add to `Drjoy/Common/DI/AppDIContainer.swift`:
```swift
// MARK: - [FeatureName] Registration
container.register([FeatureName]Repos.self) { resolver in
    let apiClient = resolver.resolve(APIClient.self)!
    return [FeatureName]RepositoryImpl(apiClient: apiClient)
}

container.register(Get[FeatureName]UC.self) { resolver in
    let repository = resolver.resolve([FeatureName]Repos.self)!
    return Get[FeatureName]UC(repository: repository)
}

container.register([FeatureName]Presenter.self) { resolver in
    let getUC = resolver.resolve(Get[FeatureName]UC.self)!
    let createUC = resolver.resolve(Create[FeatureName]UC.self)!
    let updateUC = resolver.resolve(Update[FeatureName]UC.self)!
    let deleteUC = resolver.resolve(Delete[FeatureName]UC.self)!
    return [FeatureName]Presenter(get[FeatureName]UC: getUC,
                                  create[FeatureName]UC: createUC,
                                  update[FeatureName]UC: updateUC,
                                  delete[FeatureName]UC: deleteUC)
}
```

### 6. Testing
```
DrjoyTests/
└── [FeatureName]/
    ├── [FeatureName]PresenterTests.swift
    ├── [FeatureName]ViewControllerTests.swift
    └── [FeatureName]RepositoryTests.swift
```

## Implementation Steps

### 1. Setup Domain Layer
- [ ] Create entity models
- [ ] Define repository protocols
- [ ] Create use cases
- [ ] Add domain enums

### 2. Setup Data Layer
- [ ] Implement repository classes
- [ ] Create API classes
- [ ] Add network configuration
- [ ] Handle error responses

### 3. Setup Presentation Layer
- [ ] Create view controllers
- [ ] Implement presenters
- [ ] Create custom views and cells
- [ ] Define view protocols

### 4. UI Implementation
- [ ] Create responsive layouts with SnapKit
- [ ] Add loading states with ActivityIndicator
- [ ] Handle error states with user-friendly messages
- [ ] Implement pull-to-refresh (if applicable)
- [ ] Add Texture support for performance (if needed)

### 5. Integration
- [ ] Register dependencies in DI container
- [ ] Add navigation routes
- [ ] Configure deep linking (if needed)
- [ ] Add analytics tracking

### 6. Testing
- [ ] Write unit tests for use cases
- [ ] Write unit tests for presenters
- [ ] Write UI tests for view controllers
- [ ] Add integration tests

## Code Quality Checklist
- [ ] Follow SwiftLint configuration (150 char line limit)
- [ ] Use weak self in closures to prevent retain cycles
- [ ] Handle optionals safely (avoid force unwrapping)
- [ ] Add proper error handling
- [ ] Include documentation comments
- [ ] Use meaningful variable names (camelCase)
- [ ] Keep functions under 30 lines
- [ ] Remove unused code and imports

## Related Documentation
- Project Architecture: `system/project_architecture.md`
- Database Schema: `system/database_schema.md`
- API Documentation: `system/api_endpoints.md`
- Development Workflow: `sops/mobile_dev_workflow.md`
- Code Standards: `../copilot-instructions.md`