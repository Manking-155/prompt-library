# Dr.JOY iOS Architecture Diagram

## Project Structure

```
ios-drjoy/
├── Drjoy.xcodeproj/                    # Main Application
│   └── Drjoy/
│       └── Presentasion/               # Presentation Layer
│           ├── Controller/             # UIViewControllers
│           │   ├── Attendance/
│           │   ├── Timesheet/
│           │   ├── Request/
│           │   └── Settings/
│           ├── Presenter/              # MVP Presenters
│           │   ├── Attendance/
│           │   ├── Timesheet/
│           │   └── Request/
│           ├── View/                  # Custom UI Components
│           ├── Protocol/              # View Protocols
│           ├── Provider/              # Data Providers
│           └── Service/               # External Services
│
├── Domain/                            # Business Logic Layer
│   └── Domain.xcodeproj/
│       └── Domain/
│           ├── Repository/            # Repository Protocols
│           │   ├── AttendanceRepos.swift
│           │   ├── TimesheetRepos.swift
│           │   └── RequestRepos.swift
│           ├── Entity/                # Domain Entities
│           │   ├── AttendanceEntity.swift
│           │   ├── TimesheetEntity.swift
│           │   └── UserEntity.swift
│           ├── UseCase/              # Use Cases
│           │   ├── Attendance/
│           │   ├── Timesheet/
│           │   └── Request/
│           └── Enum/                 # Domain Enums
│
├── Data/                             # Data Layer
│   └── Data.xcodeproj/
│       └── Data/
│           ├── Repository/           # Repository Implementations
│           │   ├── AttendanceRepositoryImpl.swift
│           │   ├── TimesheetRepositoryImpl.swift
│           │   └── RequestRepositoryImpl.swift
│           ├── APIs/                # API Layer
│           │   ├── APIs/           # API Implementations
│           │   │   ├── Attendance/
│           │   │   ├── Timesheet/
│           │   │   └── Request/
│           │   └── Configuration/  # API Configuration
│           └── Network/            # Networking Utilities
│
└── Common/                          # Shared Utilities
    └── Common.xcodeproj/
        └── Common/
            ├── Extension/          # Swift Extensions
            ├── Utils/              # Utility Classes
            └── Thirdparty/         # Third-party Integrations
```

## Clean Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │ViewController│◄─────┤   Presenter  │─────►│   View   │  │
│  │   (UIKit)    │      │   (MVP)      │      │ Protocol │  │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│         │                      │                             │
└─────────┼──────────────────────┼─────────────────────────────┘
          │                      │
          ▼                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                            │
│         ┌──────────────┐      ┌──────────────┐              │
│         │   UseCase    │      │  Repository  │              │
│         │              │─────►│   Protocol   │              │
│         └──────────────┘      └──────────────┘              │
│                │                      │                      │
│         ┌──────▼──────┐              │                      │
│         │   Entity    │              │                      │
│         └─────────────┘              │                      │
└──────────────────────────────────────┼──────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────┐
│                       Data Layer                              │
│         ┌──────────────┐      ┌──────────────┐               │
│         │  Repository  │      │     API      │               │
│         │    Impl      │─────►│  Alamofire   │               │
│         └──────────────┘      └──────────────┘               │
│                │                      │                       │
│         ┌──────▼──────┐      ┌───────▼──────┐                │
│         │    Realm    │      │   Firebase   │                │
│         │  Database   │      │   Services   │                │
│         └─────────────┘      └──────────────┘                │
└───────────────────────────────────────────────────────────────┘
```

## Dependency Injection with Swinject

```
AppDIContainer
     │
     ├─► NetworkLayer (APIClient, Alamofire)
     │
     ├─► Repositories (AttendanceRepos, TimesheetRepos)
     │
     ├─► UseCases (GetAttendanceUC, CheckInUC)
     │
     └─► Presenters (AttendancePresenter, TimesheetPresenter)
```

## RxSwift Data Flow

```
User Action
     │
     ▼
ViewController
     │
     │ presenter.loadData()
     ▼
Presenter
     │
     │ useCase.exe()
     ▼
UseCase
     │
     │ repository.getData()
     ▼
Repository
     │
     │ apiClient.request()
     ▼
API Layer (Alamofire)
     │
     │ Observable<Entity>
     ▼
Repository
     │
     │ Observable<Entity>
     ▼
UseCase
     │
     │ Observable<Entity>
     ▼
Presenter
     │
     │ view.onSuccess()
     ▼
ViewController
     │
     ▼
Update UI
```

## Key Technologies

- **Swift 5.x**: Modern Swift features
- **UIKit + Texture**: High-performance UI
- **RxSwift 6.x**: Reactive programming
- **Swinject**: Dependency injection
- **Alamofire 4.x**: Networking
- **Realm Swift 10.x**: Local database
- **SnapKit**: Auto Layout DSL
- **Firebase**: Analytics, Auth, Messaging, etc.
