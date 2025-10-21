# Dr.JOY iOS Architecture - Reference

## Complete Implementation Guides

### Domain Layer

#### Entity Definition
```swift
// Domain/Entity/AttendanceEntity.swift
public struct AttendanceEntity {
    public let id: String
    public let userId: String
    public let userName: String
    public let checkInTime: Date
    public let checkOutTime: Date?
    public let location: LocationEntity
    public let status: AttendanceStatus

    public init(id: String, userId: String, userName: String, 
                checkInTime: Date, checkOutTime: Date?, 
                location: LocationEntity, status: AttendanceStatus) {
        self.id = id
        self.userId = userId
        self.userName = userName
        self.checkInTime = checkInTime
        self.checkOutTime = checkOutTime
        self.location = location
        self.status = status
    }
}

public enum AttendanceStatus: String {
    case present = "PRESENT"
    case absent = "ABSENT"
    case late = "LATE"
    case leave = "LEAVE"
}
```

#### Repository Protocol
```swift
// Domain/Repository/AttendanceRepos.swift
import RxSwift

public protocol AttendanceRepos {
    func getAttendance(id: String) -> Observable<AttendanceEntity>
    func getAttendances(date: Date, page: Int) -> Observable<[AttendanceEntity]>
    func checkIn(userId: String, location: LocationEntity) -> Observable<AttendanceEntity>
    func checkOut(userId: String, location: LocationEntity) -> Observable<AttendanceEntity>
}
```

#### Use Case Implementation
```swift
// Domain/UseCase/GetAttendanceUC.swift
import RxSwift

public class GetAttendanceUC {
    private let repository: AttendanceRepos

    public init(repository: AttendanceRepos) {
        self.repository = repository
    }

    public func exe(id: String) -> Observable<AttendanceEntity> {
        return repository.getAttendance(id: id)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
    }
}
```

---

### Data Layer

#### API Implementation
```swift
// Data/APIs/GetAttendanceAPI.swift
import Foundation
import Alamofire
import SwiftyJSON

class GetAttendanceAPI: API<AttendanceEntity> {
    private let attendanceId: String

    init(attendanceId: String) {
        self.attendanceId = attendanceId
        super.init()
    }

    override func path() -> String {
        return "/api/v1/attendance/\(attendanceId)"
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
```

#### Repository Implementation
```swift
// Data/Repository/AttendanceRepositoryImpl.swift
import RxSwift
import Domain

class AttendanceRepositoryImpl: AttendanceRepos {
    private let apiClient: APIClient

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func getAttendance(id: String) -> Observable<AttendanceEntity> {
        return apiClient.request(GetAttendanceAPI(attendanceId: id))
    }

    func getAttendances(date: Date, page: Int) -> Observable<[AttendanceEntity]> {
        return apiClient.request(GetAttendancesAPI(date: date, page: page))
    }

    func checkIn(userId: String, location: LocationEntity) -> Observable<AttendanceEntity> {
        return apiClient.request(CheckInAPI(userId: userId, location: location))
    }
}
```

---

### Presentation Layer

#### View Protocol
```swift
// Drjoy/Presentasion/Protocol/AttendanceView.swift
import Foundation
import Domain

protocol AttendanceView: AnyObject {
    func onShowProgress()
    func onDismissProgress()
    func onLoadAttendanceSuccess(_ entity: AttendanceEntity)
    func onCheckInSuccess(_ entity: AttendanceEntity)
    func onShowError(_ message: String)
}
```

#### Presenter Implementation
```swift
// Drjoy/Presentasion/Presenter/AttendancePresenter.swift
import UIKit
import RxSwift
import RxCocoa
import Domain

class AttendancePresenter: RxBasePresenter<AttendanceView> {
    typealias T = AttendanceView

    weak var view: AttendanceView?

    private let getAttendanceUC: GetAttendanceUC
    private let checkInUC: CheckInUC
    private let disposeBag = DisposeBag()
    private let isLoading = ActivityIndicator()
    private let errorRelay = PublishRelay<String>()

    var onError: ((String) -> Void)?
    var onLoadingStateChanged: ((Bool) -> Void)?

    init(getAttendanceUC: GetAttendanceUC, checkInUC: CheckInUC) {
        self.getAttendanceUC = getAttendanceUC
        self.checkInUC = checkInUC
        super.init()
    }

    func attachView(_ view: AttendanceView) {
        self.view = view
        setupBindings()
    }

    func detachView() {
        self.view = nil
    }

    private func setupBindings() {
        isLoading
            .drive(onNext: { [weak self] isLoading in
                self?.onLoadingStateChanged?(isLoading)
                isLoading ? self?.view?.onShowProgress() : self?.view?.onDismissProgress()
            })
            .disposed(by: disposeBag)

        errorRelay
            .bind(onNext: { [weak self] error in
                self?.onError?(error)
                self?.view?.onShowError(error)
            })
            .disposed(by: disposeBag)
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
                    self?.errorRelay.accept(error.localizedDescription)
                }
            )
            .disposed(by: disposeBag)
    }

    func checkIn(userId: String, location: LocationEntity) {
        checkInUC
            .exe(userId: userId, location: location)
            .trackActivity(isLoading)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
            .observe(on: MainScheduler.instance)
            .subscribe(
                onNext: { [weak self] entity in
                    self?.view?.onCheckInSuccess(entity)
                },
                onError: { [weak self] error in
                    self?.errorRelay.accept(error.localizedDescription)
                }
            )
            .disposed(by: disposeBag)
    }
}
```

#### View Controller Implementation
```swift
// Drjoy/Presentasion/Controller/AttendanceViewController.swift
import UIKit
import RxSwift
import Domain

class AttendanceViewController: UIViewController {

    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var checkInButton: UIButton!
    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!

    var presenter: AttendancePresenter!
    private let disposeBag = DisposeBag()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupBindings()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        presenter.attachView(self)
        presenter.loadAttendance(id: currentUserId)
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        presenter.detachView()
    }

    private func setupUI() {
        title = "Attendance"
        setupTableView()
        setupButtons()
    }

    private func setupTableView() {
        tableView.delegate = self
        tableView.dataSource = self
        tableView.register(UINib(nibName: "AttendanceCell", bundle: nil),
                          forCellReuseIdentifier: "AttendanceCell")
    }

    private func setupButtons() {
        checkInButton.addTarget(self, action: #selector(checkInTapped), for: .touchUpInside)
    }

    private func setupBindings() {
        presenter.onLoadingStateChanged = { [weak self] isLoading in
            DispatchQueue.main.async {
                self?.activityIndicator?.isHidden = !isLoading
            }
        }

        presenter.onError = { [weak self] error in
            self?.showAlert(title: "Error", message: error)
        }
    }

    @objc private func checkInTapped() {
        let location = getCurrentLocation()
        presenter.checkIn(userId: currentUserId, location: location)
    }

    private func showAlert(title: String, message: String) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
}

extension AttendanceViewController: AttendanceView {
    func onShowProgress() {
        activityIndicator?.startAnimating()
    }

    func onDismissProgress() {
        activityIndicator?.stopAnimating()
    }

    func onLoadAttendanceSuccess(_ entity: AttendanceEntity) {
        // Update UI
        tableView.reloadData()
    }

    func onCheckInSuccess(_ entity: AttendanceEntity) {
        showAlert(title: "Success", message: "Check-in successful")
    }

    func onShowError(_ message: String) {
        showAlert(title: "Error", message: message)
    }
}
```

---

### Texture (AsyncDisplayKit) Patterns

#### AsyncListPresenter Base Class
```swift
import AsyncDisplayKit
import RxSwift

class AsyncListPresenter<CellType: ASCellNode, EntityType>: NSObject, ASTableDataSource {

    private var entities: [EntityType] = []
    private let disposeBag = DisposeBag()
    private var isLoadingMore = false

    func loadData(page: Int, completion: @escaping ([EntityType], Bool) -> Void) {
        // Override in subclass
    }

    func cellNode(for entity: EntityType) -> CellType {
        // Override in subclass
        fatalError("Must override cellNode")
    }

    func tableNode(_ tableNode: ASTableNode, numberOfRowsInSection section: Int) -> Int {
        return entities.count
    }

    func tableNode(_ tableNode: ASTableNode, nodeForRowAt indexPath: IndexPath) -> ASCellNode {
        let entity = entities[indexPath.row]
        return cellNode(for: entity)
    }

    func shouldBatchFetch(for tableNode: ASTableNode) -> Bool {
        return !isLoadingMore
    }

    func tableNode(_ tableNode: ASTableNode, willBeginBatchFetchWith context: ASBatchContext) {
        isLoadingMore = true
        let nextPage = (entities.count / 20) + 1

        loadData(page: nextPage) { [weak self] newEntities, hasMore in
            self?.entities.append(contentsOf: newEntities)
            self?.isLoadingMore = false
            tableNode.reloadData()
            context.completeBatchFetching(true)
        }
    }
}
```

---

### Swinject Dependency Injection

#### Complete DI Setup
```swift
// Drjoy/Common/DI/AppDIContainer.swift
import Swinject
import Domain
import Data

class AppDIContainer {
    static let shared = AppDIContainer()
    let container = Container()

    private init() {
        registerNetworking()
        registerRepositories()
        registerUseCases()
        registerPresenters()
    }

    private func registerNetworking() {
        container.register(APIClient.self) { _ in
            APIClient()
        }.inObjectScope(.container)
    }

    private func registerRepositories() {
        container.register(AttendanceRepos.self) { resolver in
            AttendanceRepositoryImpl(apiClient: resolver.resolve(APIClient.self)!)
        }
    }

    private func registerUseCases() {
        container.register(GetAttendanceUC.self) { resolver in
            GetAttendanceUC(repository: resolver.resolve(AttendanceRepos.self)!)
        }

        container.register(CheckInUC.self) { resolver in
            CheckInUC(repository: resolver.resolve(AttendanceRepos.self)!)
        }
    }

    private func registerPresenters() {
        container.register(AttendancePresenter.self) { resolver in
            AttendancePresenter(
                getAttendanceUC: resolver.resolve(GetAttendanceUC.self)!,
                checkInUC: resolver.resolve(CheckInUC.self)!
            )
        }
    }
}
```

---

This reference covers the essential patterns. For complete feature templates, see `templates/feature_template.md`.
