# Codebase Structure, Architecture & Code Standards

## Directory Structure (Tree View)

```
flutter_app/
├── android/
├── lib/
│   ├── app/                    # App configuration and theme
│   ├── core/                   # Infrastructure and services
│   │   ├── di/                 # Dependency Injection (GetIt + Injectable)
│   │   ├── services/           # Global services (logging, event bus)
│   │   ├── database/           # Drift database configuration
│   │   ├── errors/             # Result wrapper and exceptions
│   │   ├── extensions/         # Dart extensions
│   │   └── constants/          # App constants
│   ├── features/               # Feature modules
│   │   ├── shared/             # Shared code between features
│   │   │   ├── data/           # Shared models and services
│   │   │   ├── domain/         # Shared entities and interfaces
│   │   │   └── presentation/   # Shared widgets and themes
│   │   ├── authentication/     # Feature example
│   │   │   ├── data/           # Repositories and datasources
│   │   │   │   ├── datasources/
│   │   │   │   ├── models/
│   │   │   │   └── repositories/
│   │   │   ├── domain/         # Entities, usecases, interfaces
│   │   │   │   ├── entities/
│   │   │   │   ├── repositories/
│   │   │   │   └── usecases/
│   │   │   └── presentation/   # Pages, widgets, controllers, bindings
│   │   ├── home/               # Another feature example
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   └── profile/            # More features as needed
│   │       ├── data/
│   │       ├── domain/
│   │       └── presentation/
│   ├── routes/                 # Route definitions and navigation
│   │   ├── app_routes.dart
│   │   ├── app_pages.dart
│   │   └── middlewares/
│   └── main.dart               # App entry point
├── ios/
├── macos/
├── test/
│   ├── unit/                   # Unit tests
│   ├── widget/                 # Widget tests
│   └── integration/            # Integration tests
├── web/
├── windows/
├── pubspec.yaml                # Main project dependencies
├── analysis_options.yaml       # Linter rules
└── README.md
```

## Folder & File Explanation

### `lib/features/` - Feature Modules
All features are organized under the features folder using Clean Architecture:
- **`shared/`**: Shared code between features (common entities, widgets, services)
- **`authentication/`**, **`home/`**, **`profile/`**, etc.: Individual feature modules
  - **`data/`**: Repositories, datasources (local/remote), models
  - **`domain/`**: Entities, repository interfaces, usecases
  - **`presentation/`**: Pages, widgets, GetX controllers, bindings

### `lib/core/` - Core Infrastructure
Contains platform-level components not related to specific business logic:
- **`di/`**: GetIt service locator + Injectable code generation
- **`database/`**: Drift database, table definitions, migrations
- **`services/`**: Global services (logging, analytics, event bus)
- **`errors/`**: Result wrapper pattern, custom exceptions
- **`extensions/`**: Dart extensions for common types
- **`constants/`**: App-wide constants

### `lib/routes/` - Navigation
- **`app_routes.dart`**: All route constants
- **`app_pages.dart`**: GetPage definitions with bindings
- **`middlewares/`**: Auth middleware, permission checks

### `lib/main.dart`
- App entry point
- DI initialization
- GetMaterialApp configuration
- Initial route setup

### `test/` - Testing
- **`unit/`**: Test domain logic, usecases
- **`widget/`**: Test UI widgets, pages
- **`integration/`**: Test end-to-end flows

## Architecture Description

This project implements **Clean Architecture** with **Feature-Based Organization**:

### 1. Feature-Based Organization
- Features are organized in `lib/features/` folder
- Each feature contains `data/`, `domain/`, and `presentation/` layers
- Shared code is in the `features/shared` folder
- Single `pubspec.yaml` for the entire app
- Easy to navigate and maintain

### 2. Clean Architecture (3 Layers)
Each feature module follows 3 layers:

#### **Domain Layer** (No dependencies)
- Contains business logic
- Defines entities (business objects)
- Defines repository interfaces (contracts)
- Implements usecases (business operations)
- No framework dependencies (Flutter, GetX, Dio...)

#### **Data Layer** (Framework dependencies OK)
- Implements repository interfaces from domain
- Manages local storage (SQLite via Drift)
- Manages remote API calls (Dio)
- Models (DTOs - Data Transfer Objects)
- Datasources (local/remote)

#### **Presentation Layer** (UI + GetX)
- GetX Controllers for state management
- Pages (full screens)
- Widgets (UI components)
- GetX Bindings for DI
- Calls usecases from domain

### 3. Offline-First Strategy
- Local SQLite database is the source of truth
- Data is saved locally first
- Background sync with backend when network available
- App works offline

### 4. Error Handling - Result Wrapper
Instead of throwing exceptions, use Result wrapper:
```dart
Result<Success, Failure>
  .fold(
    (success) => handleSuccess(),
    (failure) => handleError(),
  )
```
- Type-safe error handling
- Explicit error propagation
- No uncaught exceptions

### 5. State Management - GetX
- GetX Controller for UI state
- Observable properties (`.obs`)
- GetX Bindings for DI
- Automatic cleanup

### 6. Dependency Injection - GetIt
- GetIt service locator
- Injectable code generation
- Lazy loading services
- Per-feature registration

### 7. Database - Drift ORM
- Type-safe SQLite queries
- Auto code generation
- Schema versioning
- Easy migrations

## Naming Conventions

- **Language**: English (code & comments)
- **Files**: `snake_case` (e.g., `user_controller.dart`)
- **Classes**: `PascalCase` (e.g., `UserController`)
- **Variables**: `camelCase` (e.g., `userName`)
- **Constants**: `camelCase` (e.g., `defaultTimeout`)
- **Routes**: `UPPER_SNAKE_CASE` (e.g., `USER_ROUTE`)

## Code Standards & Practices

### Formatting
- Follow `dart format`
- Max 80 characters line length (soft), 100 hard limit
- 2 spaces indentation
- Organized imports

### Linting
- Use `analysis_options.yaml`
- Follow **Effective Dart**
- Full Null Safety

### Error Handling
- Always use Result wrapper
- Custom exceptions for each error type
- Type-safe error propagation

### Testing
- Unit tests for domain logic
- Widget tests for UI
- Integration tests for flows
- Mock external dependencies

## Documentation
All documentation is stored in the `.agent/` folder:
- `.agent/system/` - Architecture & technical specs
- `.agent/templates/` - Implementation guides
- `.agent/sops/` - Standard procedures
- `.agent/readme.md` - Documentation index

**Always start with `.agent/readme.md`** to find relevant documentation.

## Communication Flow

```
User Action
    ↓
GetX Controller (Presentation)
    ↓
Usecase (Domain)
    ↓
Repository (Domain interface → Data impl)
    ↓
Datasources (Local/Remote)
    ↓
SQLite / API
    ↓
Response (Result wrapper)
    ↓
UI Update (Reactive)
```

## Related Documentation

See `.agent/` folder for:
- **Architecture deep dive**: `system/` files
- **Code examples**: `templates/` files
- **How-to guides**: `sops/` files
- **Navigation**: `readme.md`

---

**Remember**: Clean code + Modular design = Easy maintenance & parallel development!
