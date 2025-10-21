# Dr.JOY iOS - Complete Feature Examples

## Example 1: Attendance Check-In Feature (Complete Implementation)

This example demonstrates a complete feature implementation following Dr.JOY architecture.

### Domain Layer

**AttendanceEntity.swift**
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

    public var isCheckedOut: Bool {
        return checkOutTime != nil
    }

    public var workDuration: TimeInterval? {
        guard let checkOut = checkOutTime else { return nil }
        return checkOut.timeIntervalSince(checkInTime)
    }
}

public struct LocationEntity {
    public let latitude: Double
    public let longitude: Double
    public let address: String?
}

public enum AttendanceStatus: String {
    case present = "PRESENT"
    case absent = "ABSENT"
    case late = "LATE"
    case leave = "LEAVE"
}
```

**AttendanceRepos.swift**
```swift
// Domain/Repository/AttendanceRepos.swift
import RxSwift

public protocol AttendanceRepos {
    func getTodayAttendance(userId: String) -> Observable<AttendanceEntity?>
    func checkIn(userId: String, location: LocationEntity) -> Observable<AttendanceEntity>
    func checkOut(userId: String, location: LocationEntity) -> Observable<AttendanceEntity>
}
```

**CheckInUseCase.swift**
```swift
// Domain/UseCase/CheckInUC.swift
import RxSwift

public class CheckInUC {
    private let repository: AttendanceRepos

    public init(repository: AttendanceRepos) {
        self.repository = repository
    }

    public func exe(userId: String, location: LocationEntity) -> Observable<AttendanceEntity> {
        return repository.checkIn(userId: userId, location: location)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
    }
}
```

### Data Layer

**CheckInAPI.swift**
```swift
// Data/APIs/CheckInAPI.swift
import Foundation
import Alamofire
import SwiftyJSON
import Domain

class CheckInAPI: API<AttendanceEntity> {
    private let userId: String
    private let location: LocationEntity

    init(userId: String, location: LocationEntity) {
        self.userId = userId
        self.location = location
        super.init()
    }

    override func path() -> String {
        return "/api/v1/attendance/check-in"
    }

    override func method() -> HTTPMethod {
        return .post
    }

    override func parameters() -> [String: Any]? {
        return [
            "user_id": userId,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "check_in_time": Date().iso8601String
        ]
    }

    override func convertJson(_ val: Any) throws -> AttendanceEntity {
        guard let dict = val as? NSDictionary else {
            throw APIError.invalidResponse
        }
        return AttendanceEntity(dict)
    }
}
```

**AttendanceRepositoryImpl.swift**
```swift
// Data/Repository/AttendanceRepositoryImpl.swift
import RxSwift
import Domain

class AttendanceRepositoryImpl: AttendanceRepos {
    private let apiClient: APIClient

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func getTodayAttendance(userId: String) -> Observable<AttendanceEntity?> {
        return apiClient.request(GetTodayAttendanceAPI(userId: userId))
            .map { $0 as AttendanceEntity? }
            .catchAndReturn(nil)
    }

    func checkIn(userId: String, location: LocationEntity) -> Observable<AttendanceEntity> {
        return apiClient.request(CheckInAPI(userId: userId, location: location))
    }

    func checkOut(userId: String, location: LocationEntity) -> Observable<AttendanceEntity> {
        return apiClient.request(CheckOutAPI(userId: userId, location: location))
    }
}
```

### Presentation Layer

**AttendanceCheckInPresenter.swift**
```swift
// Drjoy/Presentasion/Presenter/AttendanceCheckInPresenter.swift
import UIKit
import RxSwift
import RxCocoa
import Domain

class AttendanceCheckInPresenter: RxBasePresenter<AttendanceCheckInView> {
    typealias T = AttendanceCheckInView

    weak var view: AttendanceCheckInView?

    private let getTodayAttendanceUC: GetTodayAttendanceUC
    private let checkInUC: CheckInUC
    private let checkOutUC: CheckOutUC

    private let disposeBag = DisposeBag()
    private let isLoading = ActivityIndicator()
    private let errorRelay = PublishRelay<String>()

    var onError: ((String) -> Void)?
    var onCheckInSuccess: ((AttendanceEntity) -> Void)?

    init(getTodayAttendanceUC: GetTodayAttendanceUC,
         checkInUC: CheckInUC,
         checkOutUC: CheckOutUC) {
        self.getTodayAttendanceUC = getTodayAttendanceUC
        self.checkInUC = checkInUC
        self.checkOutUC = checkOutUC
        super.init()
    }

    func attachView(_ view: AttendanceCheckInView) {
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

        errorRelay
            .bind(onNext: { [weak self] error in
                self?.onError?(error)
                self?.view?.onShowError(error)
            })
            .disposed(by: disposeBag)
    }

    func loadTodayAttendance(userId: String) {
        getTodayAttendanceUC
            .exe(userId: userId)
            .trackActivity(isLoading)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
            .observe(on: MainScheduler.instance)
            .subscribe(
                onNext: { [weak self] attendance in
                    if let attendance = attendance {
                        self?.view?.onLoadAttendanceSuccess(attendance)
                    } else {
                        self?.view?.onNoAttendanceToday()
                    }
                },
                onError: { [weak self] error in
                    self?.errorRelay.accept(error.localizedDescription)
                }
            )
            .disposed(by: disposeBag)
    }

    func performCheckIn(userId: String, location: LocationEntity) {
        checkInUC
            .exe(userId: userId, location: location)
            .trackActivity(isLoading)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
            .observe(on: MainScheduler.instance)
            .subscribe(
                onNext: { [weak self] attendance in
                    self?.onCheckInSuccess?(attendance)
                    self?.view?.onCheckInSuccess(attendance)
                },
                onError: { [weak self] error in
                    self?.errorRelay.accept(error.localizedDescription)
                }
            )
            .disposed(by: disposeBag)
    }

    func performCheckOut(userId: String, location: LocationEntity) {
        checkOutUC
            .exe(userId: userId, location: location)
            .trackActivity(isLoading)
            .subscribe(on: SerialDispatchQueueScheduler(qos: .default))
            .observe(on: MainScheduler.instance)
            .subscribe(
                onNext: { [weak self] attendance in
                    self?.view?.onCheckOutSuccess(attendance)
                },
                onError: { [weak self] error in
                    self?.errorRelay.accept(error.localizedDescription)
                }
            )
            .disposed(by: disposeBag)
    }
}
```

**AttendanceCheckInViewController.swift**
```swift
// Drjoy/Presentasion/Controller/AttendanceCheckInViewController.swift
import UIKit
import RxSwift
import Domain
import CoreLocation

class AttendanceCheckInViewController: UIViewController {

    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var checkInTimeLabel: UILabel!
    @IBOutlet weak var checkInButton: UIButton!
    @IBOutlet weak var checkOutButton: UIButton!
    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!
    @IBOutlet weak var mapView: UIView!

    var presenter: AttendanceCheckInPresenter!
    private let disposeBag = DisposeBag()
    private let locationManager = CLLocationManager()
    private var currentLocation: CLLocation?

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupLocation()
        setupBindings()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        presenter.attachView(self)
        loadTodayAttendance()
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        presenter.detachView()
    }

    private func setupUI() {
        title = "Check In/Out"
        checkInButton.layer.cornerRadius = 8
        checkOutButton.layer.cornerRadius = 8
        checkOutButton.isEnabled = false
    }

    private func setupLocation() {
        locationManager.delegate = self
        locationManager.requestWhenInUseAuthorization()
        locationManager.startUpdatingLocation()
    }

    private func setupBindings() {
        checkInButton.rx.tap
            .subscribe(onNext: { [weak self] in
                self?.handleCheckIn()
            })
            .disposed(by: disposeBag)

        checkOutButton.rx.tap
            .subscribe(onNext: { [weak self] in
                self?.handleCheckOut()
            })
            .disposed(by: disposeBag)
    }

    private func loadTodayAttendance() {
        let userId = UserSession.shared.currentUserId
        presenter.loadTodayAttendance(userId: userId)
    }

    private func handleCheckIn() {
        guard let location = currentLocation else {
            showAlert(title: "Error", message: "Location not available")
            return
        }

        let userId = UserSession.shared.currentUserId
        let locationEntity = LocationEntity(
            latitude: location.coordinate.latitude,
            longitude: location.coordinate.longitude,
            address: nil
        )

        presenter.performCheckIn(userId: userId, location: locationEntity)
    }

    private func handleCheckOut() {
        guard let location = currentLocation else {
            showAlert(title: "Error", message: "Location not available")
            return
        }

        let userId = UserSession.shared.currentUserId
        let locationEntity = LocationEntity(
            latitude: location.coordinate.latitude,
            longitude: location.coordinate.longitude,
            address: nil
        )

        presenter.performCheckOut(userId: userId, location: locationEntity)
    }

    private func showAlert(title: String, message: String) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
}

// MARK: - AttendanceCheckInView Protocol
extension AttendanceCheckInViewController: AttendanceCheckInView {
    func onShowProgress() {
        activityIndicator.startAnimating()
        view.isUserInteractionEnabled = false
    }

    func onDismissProgress() {
        activityIndicator.stopAnimating()
        view.isUserInteractionEnabled = true
    }

    func onLoadAttendanceSuccess(_ entity: AttendanceEntity) {
        statusLabel.text = "Status: \(entity.status.rawValue)"
        checkInTimeLabel.text = "Check-in: \(entity.checkInTime.formatted())"

        checkInButton.isEnabled = false
        checkOutButton.isEnabled = !entity.isCheckedOut
    }

    func onNoAttendanceToday() {
        statusLabel.text = "Status: Not checked in"
        checkInTimeLabel.text = ""
        checkInButton.isEnabled = true
        checkOutButton.isEnabled = false
    }

    func onCheckInSuccess(_ entity: AttendanceEntity) {
        showAlert(title: "Success", message: "Checked in successfully")
        loadTodayAttendance()
    }

    func onCheckOutSuccess(_ entity: AttendanceEntity) {
        showAlert(title: "Success", message: "Checked out successfully")
        loadTodayAttendance()
    }

    func onShowError(_ message: String) {
        showAlert(title: "Error", message: message)
    }
}

// MARK: - CLLocationManagerDelegate
extension AttendanceCheckInViewController: CLLocationManagerDelegate {
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        currentLocation = locations.last
    }
}
```

---

## Example 2: Attendance List with Texture Pagination

**AttendanceListPresenter.swift**
```swift
import AsyncDisplayKit
import RxSwift
import Domain

class AttendanceListPresenter: AsyncListPresenter<AttendanceCell, AttendanceEntity> {

    private let getAttendancesUC: GetAttendancesUC
    private let selectedDate: Date

    init(getAttendancesUC: GetAttendancesUC, selectedDate: Date) {
        self.getAttendancesUC = getAttendancesUC
        self.selectedDate = selectedDate
        super.init()
    }

    override func loadData(page: Int, completion: @escaping ([AttendanceEntity], Bool) -> Void) {
        getAttendancesUC
            .exe(date: selectedDate, page: page, pageSize: 20)
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

**AttendanceCell.swift (Texture Node)**
```swift
import AsyncDisplayKit
import Domain

class AttendanceCell: ASCellNode {

    private let nameNode = ASTextNode()
    private let timeNode = ASTextNode()
    private let statusNode = ASTextNode()
    private let avatarNode = ASNetworkImageNode()

    init(entity: AttendanceEntity) {
        super.init()
        automaticallyManagesSubnodes = true

        // Configure nodes
        nameNode.attributedText = NSAttributedString(
            string: entity.userName,
            attributes: [
                .font: UIFont.boldSystemFont(ofSize: 16),
                .foregroundColor: UIColor.black
            ]
        )

        timeNode.attributedText = NSAttributedString(
            string: entity.checkInTime.formatted(),
            attributes: [
                .font: UIFont.systemFont(ofSize: 14),
                .foregroundColor: UIColor.gray
            ]
        )

        statusNode.attributedText = NSAttributedString(
            string: entity.status.rawValue,
            attributes: [
                .font: UIFont.systemFont(ofSize: 14),
                .foregroundColor: entity.status.color
            ]
        )

        avatarNode.cornerRadius = 20
        avatarNode.style.preferredSize = CGSize(width: 40, height: 40)
    }

    override func layoutSpecThatFits(_ constrainedSize: ASSizeRange) -> ASLayoutSpec {
        // Text stack
        let textStack = ASStackLayoutSpec.vertical()
        textStack.children = [nameNode, timeNode]
        textStack.spacing = 4

        // Main horizontal stack
        let mainStack = ASStackLayoutSpec.horizontal()
        mainStack.children = [avatarNode, textStack, statusNode]
        mainStack.spacing = 12
        mainStack.alignItems = .center
        mainStack.justifyContent = .spaceBetween

        // Inset
        return ASInsetLayoutSpec(
            insets: UIEdgeInsets(top: 12, left: 16, bottom: 12, right: 16),
            child: mainStack
        )
    }
}
```

---

These examples demonstrate complete feature implementations following Dr.JOY architecture patterns.
