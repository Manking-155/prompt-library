# Flutter Project Architecture Overview

## Tech Stack

### Mobile Development
- **Framework**: Flutter 3.x
- **Language**: Dart 3.x (with Null Safety)
- **State Management**: GetX
- **Navigation**: Get Router
- **Local Database**: SQLite + Drift (ORM)
- **Dependency Injection**: GetIt + Injectable
- **HTTP Client**: Dio
- **Code Generation**: Build Runner, Drift CLI

### Development Tools
- **IDE**: VS Code, Cursor IDE, Android Studio
- **AI Assistant**: Claude API, Cursor AI
- **Version Control**: Git, GitHub
- **CI/CD**: GitHub Actions
- **Code Quality**: Dart Analyzer, Dart Format

## Architecture Overview

The project follows a **Clean Architecture** pattern with **Feature-Based Organization**:
1. **Feature-Based Organization**: Features organized in `lib/features/` folder
2. **Clean Architecture**: 3-layer separation (Presentation, Domain, Data)
3. **Offline-First**: Local database as source of truth with background sync
4. **Error Handling**: Result wrapper pattern for type-safe error handling

```
flutter_app/
├── android/
├── ios/
├── lib/
│   ├── app/                          # App configuration & theme
│   ├── core/                         # Core services & infrastructure
│   │   ├── di/                       # GetIt + Injectable setup
│   │   ├── services/                 # Global services (logging, event bus)
│   │   ├── database/                 # Drift database configuration
│   │   ├── errors/                   # Error definitions & Result wrapper
│   │   ├── extensions/               # Dart extensions
│   │   └── constants/                # App constants
│   ├── features/                     # Feature modules
│   │   ├── shared/                   # Shared code between features
│   │   │   ├── data/                 # Shared models and services
│   │   │   ├── domain/               # Shared entities and interfaces
│   │   │   └── presentation/         # Shared widgets and themes
│   │   ├── authentication/           # Feature example
│   │   │   ├── data/                 # Repositories, datasources
│   │   │   ├── domain/               # Entities, usecases, interfaces
│   │   │   └── presentation/         # Pages, widgets, controllers
│   │   ├── home/                     # Another feature
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   └── profile/                  # More features as needed
│   │       ├── data/
│   │       ├── domain/
│   │       └── presentation/
│   ├── routes/                       # Route definitions
│   └── main.dart                     # Application entry point
├── test/
│   ├── unit/                         # Unit tests
│   ├── widget/                       # Widget tests
│   └── integration/                  # Integration tests
├── pubspec.yaml                      # Main project dependencies
└── analysis_options.yaml             # Linter rules
```

## Folder Structure Explanation

### `core/` - Infrastructure Layer
- **`di/`**: GetIt service locator and Injectable setup
- **`services/`**: Global services (analytics, logging, event bus)
- **`errors/`**: Result wrapper, Exception classes, Error handling
- **`extensions/`**: Dart extensions for common types
- **`constants/`**: App-wide constants (API URLs, timeouts, etc.)

### `features/` - Feature Modules
Each feature is organized with Clean Architecture layers:
- **`shared/`**: Common code shared between features
- **`[feature_name]/data/`**: Database, API, local storage implementation
- **`[feature_name]/domain/`**: Business logic, entities, repository interfaces
- **`[feature_name]/presentation/`**: UI screens, GetX controllers, widgets

### `routes/` - Navigation
Centralized route definitions using Get Router:
- Route paths
- Page transitions
- Route parameters
- Middleware

## Key Design Patterns

### 1. Feature-Based Organization
- Features are organized in `lib/features/` folder
- Each feature contains `data/`, `domain/`, and `presentation/` layers
- Shared code goes in `features/shared`
- Single `pubspec.yaml` for entire app

### 2. Clean Architecture (3 Layers)
```
Presentation Layer ↔ Domain Layer ↔ Data Layer
    (GetX)              (Entities)      (Database/API)
```

### 3. Offline-First Strategy
- Local SQLite database is the source of truth
- Drift provides type-safe queries
- Data syncs with backend when network available

### 4. Dependency Injection
- GetIt for service locator
- Injectable for annotations
- Constructor injection through GetIt

### 5. Error Handling
- Result wrapper: `Result<T, Exception>`
- Either monad pattern
- Type-safe error propagation

## Naming Conventions

- **Files**: `snake_case` (e.g., `user_controller.dart`)
- **Classes**: `PascalCase` (e.g., `UserController`)
- **Variables**: `camelCase` (e.g., `userName`)
- **Constants**: `camelCase` (e.g., `defaultTimeout`)

## Code Standards

- **Formatting**: Dart Format (enforced by linter)
- **Analysis**: Follows `analysis_options.yaml` rules
- **Language**: English for all code and comments
- **Null Safety**: Full Null Safety enabled
- **Testing**: Unit, Widget, and Integration tests required

## Related Documentation
- Clean Architecture Guide: `system/clean_architecture_guide.md`
- Modular Architecture: `system/modular_architecture_guide.md`
- Code Standards: `system/code_standards.md`
- Database Schema: `system/database_schema.md`
