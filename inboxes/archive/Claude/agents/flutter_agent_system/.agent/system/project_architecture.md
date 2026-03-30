# Flutter Project Architecture

## Tech Stack

### Core Technologies
- **Flutter**: Cross-platform UI framework
- **Dart**: Programming language with null safety
- **GetX**: State management & dependency injection
- **GetIt**: Service locator for dependency injection
- **Injectable**: Code generation for GetIt
- **Drift (Moor)**: Type-safe SQL database wrapper
- **SQLite**: Local database engine
- **Get Router**: Navigation and routing

### Backend Integration
- **Supabase**: Backend-as-a-Service (optional)
- **REST APIs**: Custom backend integration

## Architecture Overview

### Modular Architecture
The app follows a modular architecture where each feature is an independent module:

```
features/
├── flashcard_import/
│   ├── pubspec.yaml          # Independent dependencies
│   ├── lib/
│   │   ├── data/            # Data layer
│   │   ├── domain/          # Business logic
│   │   └── presentation/    # UI and state management
│   └── test/
├── flashcard_viewer/
│   ├── pubspec.yaml
│   ├── lib/
│   └── test/
└── shared/
    ├── pubspec.yaml
    ├── lib/
    └── test/
```

### Clean Architecture (3-Layer)
Each module follows Clean Architecture principles:

#### 1. Presentation Layer
- **UI Components**: Screens, widgets, views
- **State Management**: GetX controllers
- **Navigation**: Get Router navigation
- **Forms**: Input validation and handling

#### 2. Domain Layer
- **Use Cases**: Business logic operations
- **Entities**: Core business objects
- **Repository Interfaces**: Abstract data contracts
- **Models**: Domain-specific models

#### 3. Data Layer
- **Repository Implementations**: Concrete data sources
- **Data Sources**: Local (SQLite) and remote (API) data
- **DTOs**: Data transfer objects
- **Mappers**: Convert between data representations

## Directory Structure

```
.
├── android/                  # Android-specific code
├── ios/                      # iOS-specific code
├── features/                 # Feature modules
│   ├── feature_1/           # Independent feature module
│   │   ├── pubspec.yaml     # Feature-specific dependencies
│   │   ├── lib/
│   │   │   ├── data/        # Data layer
│   │   │   │   ├── datasources/
│   │   │   │   ├── models/
│   │   │   │   ├── repositories/
│   │   │   │   └── mappers/
│   │   │   ├── domain/      # Business logic
│   │   │   │   ├── entities/
│   │   │   │   ├── usecases/
│   │   │   │   └── repositories/
│   │   │   └── presentation/ # UI layer
│   │   │       ├── controllers/
│   │   │       ├── views/
│   │   │       └── widgets/
│   │   └── test/
│   └── shared/              # Shared code between features
├── lib/                     # App-level code
│   ├── app/                 # App configuration
│   │   ├── bindings/
│   │   ├── config/
│   │   ├── routes/
│   │   └── themes/
│   ├── core/                # Core services
│   │   ├── database/
│   │   ├── di/
│   │   ├── services/
│   │   ├── utils/
│   │   └── constants/
│   ├── examples/
│   └── main.dart           # Entry point
├── test/                   # App-level tests
│   ├── unit/
│   ├── widget/
│   └── integration/
├── pubspec.yaml            # App dependencies
└── README.md
```

## Key Principles

### 1. Feature Independence
- Each feature has its own `pubspec.yaml`
- Features can be developed and tested independently
- Minimal coupling between features

### 2. Offline-First Strategy
- Local database (SQLite + Drift) as primary data source
- Background synchronization with remote APIs
- Cached data for offline functionality

### 3. Dependency Injection
- GetIt + Injectable for service location
- Clear separation of concerns
- Easy testing and mocking

### 4. State Management
- GetX for UI state management
- Reactive programming with streams
- Clear data flow patterns

### 5. Error Handling
- Result wrapper pattern for operations
- Consistent error reporting
- User-friendly error messages

## Development Workflow

1. **Feature Creation**: Use feature module template
2. **Implementation**: Follow Clean Architecture layers
3. **Testing**: Unit, widget, and integration tests
4. **Integration**: Add feature to app routing
5. **Code Review**: Ensure architecture compliance

## Benefits

- **Scalability**: Easy to add new features
- **Maintainability**: Clear separation of concerns
- **Testability**: Each layer can be tested independently
- **Team Collaboration**: Teams can work on different features in parallel
- **Code Reusability**: Shared components across features