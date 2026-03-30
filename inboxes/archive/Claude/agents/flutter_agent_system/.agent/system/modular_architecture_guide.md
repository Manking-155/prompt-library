# Modular Architecture Guide

## Overview

Modular Architecture is a software design approach that divides an application into independent, loosely coupled modules. Each module represents a specific feature or functionality and can be developed, tested, and maintained independently.

## Benefits of Modular Architecture

### 1. **Independent Development**
- Teams can work on different features in parallel
- No conflicts between feature implementations
- Faster development cycles

### 2. **Code Reusability**
- Shared modules can be reused across features
- Common functionality centralized
- Reduced code duplication

### 3. **Maintainability**
- Changes to one feature don't affect others
- Easier to locate and fix bugs
- Clear code organization

### 4. **Testability**
- Each module can be tested independently
- Better test coverage and isolation
- Easier to mock dependencies

### 5. **Scalability**
- Easy to add new features as new modules
- Can scale teams by assigning modules
- Better performance through lazy loading

## Module Structure

Each feature module follows this consistent structure:

```
feature_name/
├── pubspec.yaml              # Module-specific dependencies
├── lib/
│   ├── data/                 # Data layer
│   │   ├── datasources/      # Data sources (local/remote)
│   │   ├── models/           # Data transfer objects
│   │   ├── repositories/     # Repository implementations
│   │   └── mappers/          # Data transformation
│   ├── domain/               # Domain layer
│   │   ├── entities/         # Business entities
│   │   ├── usecases/         # Business logic
│   │   └── repositories/     # Repository interfaces
│   ├── presentation/         # Presentation layer
│   │   ├── controllers/      # GetX controllers
│   │   ├── views/            # Screens and pages
│   │   └── widgets/          # Reusable UI components
│   └── feature_name.dart     # Public API exports
└── test/
    ├── unit/                 # Unit tests
    ├── widget/               # Widget tests
    └── integration/          # Integration tests
```

## Module Types

### 1. **Feature Modules**
Contain complete functionality for a specific feature:
- `flashcard_import/` - Import flashcards from various sources
- `flashcard_viewer/` - View and study flashcards
- `user_profile/` - User profile management
- `settings/` - App settings and preferences

### 2. **Shared Modules**
Contain code shared across multiple features:
- `shared/` - Common models, utilities, and widgets
- `ui_components/` - Reusable UI components
- `core_services/` - Shared business services

## Module Dependencies

### Dependency Rules
1. **Feature modules** should not depend on other feature modules
2. **Feature modules** can depend on shared modules
3. **Shared modules** should not create circular dependencies
4. **App-level code** can depend on any module

### Dependency Graph
```
App (main.dart)
    ↓
Feature Modules (flashcard_viewer, flashcard_import, etc.)
    ↓
Shared Modules (shared, ui_components)
    ↓
Core Services (database, networking, DI)
```

## Module Communication

### 1. **Event Bus**
For loose coupling between modules:
```dart
// In shared module
class AppEventBus extends GetxService {
  final _eventController = StreamController<AppEvent>.broadcast();

  Stream<AppEvent> get eventStream => _eventController.stream;

  void emit(AppEvent event) {
    _eventController.add(event);
  }
}

// Usage in feature A
Get.find<AppEventBus>().emit(FlashcardImportedEvent(id: '123'));

// Usage in feature B
Get.find<AppEventBus>().eventStream.listen((event) {
  if (event is FlashcardImportedEvent) {
    // Handle event
  }
});
```

### 2. **Shared Services**
For common functionality:
```dart
// In shared module
abstract class NavigationService {
  void navigateToFlashcard(String id);
  void navigateToSettings();
}

// Implementation in app level
class NavigationServiceImpl implements NavigationService {
  @override
  void navigateToFlashcard(String id) {
    Get.toNamed('/flashcard/$id');
  }
}
```

### 3. **Interface Segregation**
Define interfaces in shared modules:
```dart
// In shared module
abstract class FlashcardRepository {
  Future<List<Flashcard>> getFlashcards();
}

// In feature module
class FlashcardRepositoryImpl implements FlashcardRepository {
  // Implementation specific to this feature
}
```

## Creating a New Module

### 1. Directory Setup
```bash
mkdir features/new_feature
cd features/new_feature
```

### 2. pubspec.yaml
```yaml
name: new_feature
description: New feature module

environment:
  sdk: '>=2.17.0 <3.0.0'
  flutter: ">=3.0.0"

dependencies:
  flutter:
    sdk: flutter

  # App dependencies
  get: ^4.6.5
  get_it: ^7.2.0
  injectable: ^1.5.3
  drift: ^2.8.0

  # Shared modules
  shared:
    path: ../shared
  core_services:
    path: ../../lib/core/services

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.3.0
  injectable_generator: ^1.5.4
  drift_dev: ^2.8.0
```

### 3. Module Entry Point
```dart
// lib/new_feature.dart
export 'data/datasources/remote_datasource.dart';
export 'data/models/feature_model.dart';
export 'data/repositories/repository_impl.dart';
export 'domain/entities/feature_entity.dart';
export 'domain/usecases/get_feature.dart';
export 'domain/repositories/repository.dart';
export 'presentation/controllers/feature_controller.dart';
export 'presentation/views/feature_view.dart';
```

### 4. Dependency Injection
```dart
// lib/data/di/injection.dart
import 'package:injectable/injectable.dart';
import 'package:get_it/get_it.dart';

import 'domain/repositories/repository.dart';
import 'data/repositories/repository_impl.dart';
import 'domain/usecases/usecase.dart';

@module
abstract class FeatureModule {
  @singleton
  FeatureRepository get repository => FeatureRepositoryImpl();

  @singleton
  GetFeatureUseCase get getFeatureUseCase => GetFeatureUseCase(repository);
}
```

## Best Practices

### 1. **Module Boundaries**
- Keep module interfaces minimal and clear
- Avoid leaking internal implementation details
- Use dependency injection for external dependencies

### 2. **Shared Code**
- Put truly shared code in shared modules
- Avoid creating large shared modules
- Consider splitting shared modules by functionality

### 3. **Testing**
- Each module should have its own test suite
- Mock external dependencies when testing modules
- Test module integration at the app level

### 4. **Documentation**
- Document each module's purpose and API
- Include usage examples in module README
- Maintain dependency documentation

## Module Lifecycle

### 1. **Initialization**
- Modules are initialized through dependency injection
- Use `@module` annotations for Injectable setup
- Initialize core services before feature modules

### 2. **Lazy Loading**
- Load modules only when needed
- Use GetX lazy loading for controllers
- Implement route-based module loading

### 3. **Cleanup**
- Properly dispose resources when module is not needed
- Clean up streams and subscriptions
- Remove unused dependencies

## Common Patterns

### 1. **Feature Toggle**
```dart
class FeatureToggleService {
  bool isFeatureEnabled(String featureName) {
    // Implementation based on remote config or local settings
  }
}
```

### 2. **Module Registry**
```dart
class ModuleRegistry {
  final Map<String, Module> _modules = {};

  void registerModule(String name, Module module) {
    _modules[name] = module;
  }

  Module? getModule(String name) => _modules[name];
}
```

### 3. **Cross-Module Navigation**
```dart
class NavigationService {
  void navigateToFeature(String featureName, Map<String, dynamic>? arguments) {
    // Dynamic navigation based on feature name
  }
}
```

## Migration Strategy

When converting an existing app to modular architecture:

1. **Identify Features**: Group existing code into logical features
2. **Create Shared Modules**: Extract common code first
3. **Migrate Incrementally**: Move one feature at a time
4. **Update Dependencies**: Fix import statements and dependencies
5. **Test Thoroughly**: Ensure functionality is preserved
6. **Update Documentation**: Keep documentation up to date

## Tools and Resources

- **Dependency Injection**: GetIt + Injectable
- **Code Generation**: build_runner for DI and model generation
- **Testing**: flutter_test with mock dependencies
- **Linting**: analysis_options.yaml for module-specific rules