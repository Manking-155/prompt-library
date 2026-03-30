# Clean Architecture Guide

## Overview

Clean Architecture is a software design philosophy that separates the code into layers with well-defined responsibilities. In our Flutter project, we implement a 3-layer Clean Architecture pattern.

## The Three Layers

### 1. Presentation Layer (UI Layer)
**Purpose**: Handle all UI-related logic and user interactions

**Components**:
- **Views/Screens**: UI components that display data
- **Controllers**: GetX controllers that manage UI state
- **Widgets**: Reusable UI components
- **Navigation**: Route handling and navigation logic

**Responsibilities**:
- Display data to users
- Handle user input and interactions
- Manage UI state (loading, error, success)
- Navigate between screens
- Validate user input

**Dependencies**: Depends on Domain Layer

### 2. Domain Layer (Business Logic Layer)
**Purpose**: Contains the core business logic and rules of the application

**Components**:
- **Entities**: Core business objects with business rules
- **Use Cases**: Application-specific business rules
- **Repository Interfaces**: Abstract contracts for data access
- **Domain Models**: Business-specific data models

**Responsibilities**:
- Implement business logic
- Define data contracts (repositories)
- Handle business rules and validation
- Remain framework-independent

**Dependencies**: No dependencies on other layers

### 3. Data Layer (Infrastructure Layer)
**Purpose**: Handle data access and external service integration

**Components**:
- **Repository Implementations**: Concrete implementations of repository interfaces
- **Data Sources**: Local (SQLite) and remote (API) data access
- **DTOs**: Data transfer objects for external data
- **Mappers**: Convert between external data and domain models

**Responsibilities**:
- Retrieve data from external sources
- Cache data locally
- Handle network operations
- Map data between different representations

**Dependencies**: Depends on Domain Layer

## Dependency Rule

**Rule**: Dependencies can only point inward

```
┌──────────────────────────────────────────────┐
│                 Presentation                 │
│            (Controllers, Views)              │
├──────────────────────────────────────────────┤
│                   Domain                     │
│        (Use Cases, Entities, Repos)          │
├──────────────────────────────────────────────┤
│                    Data                      │
│      (Repositories, Data Sources, APIs)      │
└──────────────────────────────────────────────┘
```

## Implementation Examples

### Domain Layer Example

#### Entity (User Entity)
```dart
// lib/domain/entities/user.dart
class User {
  final String id;
  final String name;
  final String email;

  User({
    required this.id,
    required this.name,
    required this.email,
  });

  // Business rules
  bool get isValidEmail => email.contains('@');
}
```

#### Repository Interface
```dart
// lib/domain/repositories/user_repository.dart
abstract class UserRepository {
  Future<Result<User>> getUser(String id);
  Future<Result<List<User>>> getAllUsers();
  Future<Result<void>> saveUser(User user);
}
```

#### Use Case
```dart
// lib/domain/usecases/get_user.dart
class GetUserUseCase {
  final UserRepository _repository;

  GetUserUseCase(this._repository);

  Future<Result<User>> execute(String userId) {
    return _repository.getUser(userId);
  }
}
```

### Data Layer Example

#### Repository Implementation
```dart
// lib/data/repositories/user_repository_impl.dart
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource _remoteDataSource;
  final UserLocalDataSource _localDataSource;

  UserRepositoryImpl(
    this._remoteDataSource,
    this._localDataSource,
  );

  @override
  Future<Result<User>> getUser(String id) async {
    try {
      // Try local first (offline-first)
      final localUser = await _localDataSource.getUser(id);
      if (localUser != null) {
        return Result.success(localUser.toEntity());
      }

      // Fallback to remote
      final remoteUser = await _remoteDataSource.getUser(id);
      await _localDataSource.saveUser(remoteUser);
      return Result.success(remoteUser.toEntity());
    } catch (e) {
      return Result.failure(e.toString());
    }
  }
}
```

### Presentation Layer Example

#### GetX Controller
```dart
// lib/presentation/controllers/user_controller.dart
class UserController extends GetxController {
  final GetUserUseCase _getUserUseCase;

  final _user = Rx<User?>(null);
  final _isLoading = false.obs;
  final _error = Rx<String?>(null);

  User? get user => _user.value;
  bool get isLoading => _isLoading.value;
  String? get error => _error.value;

  UserController(this._getUserUseCase);

  Future<void> loadUser(String userId) async {
    _isLoading.value = true;
    _error.value = null;

    final result = await _getUserUseCase.execute(userId);

    result.fold(
      (error) => _error.value = error,
      (user) => _user.value = user,
    );

    _isLoading.value = false;
  }
}
```

## Error Handling Pattern

### Result Wrapper
```dart
// lib/core/utils/result.dart
class Result<T> {
  final T? _data;
  final String? _error;

  Result.success(T data) : _data = data, _error = null;
  Result.failure(String error) : _data = null, _error = error;

  bool get isSuccess => _error == null;
  bool get isFailure => _error != null;

  T get data => _data!;
  String get error => _error!;

  R fold<R>(R Function(String error) onFailure, R Function(T data) onSuccess) {
    if (isFailure) {
      return onFailure(error);
    } else {
      return onSuccess(data);
    }
  }
}
```

## Benefits of Clean Architecture

1. **Testability**: Each layer can be tested independently
2. **Independence**: Business logic is independent of UI and external services
3. **Flexibility**: Easy to change implementations without affecting other layers
4. **Maintainability**: Clear separation of concerns makes code easier to maintain
5. **Reusability**: Domain logic can be reused across different platforms

## Best Practices

1. **Dependency Inversion**: High-level modules should not depend on low-level modules
2. **Single Responsibility**: Each class should have only one reason to change
3. **Interface Segregation**: Clients should not be forced to depend on interfaces they don't use
4. **Framework Independence**: Domain layer should not depend on any framework
5. **Test Coverage**: Write tests for each layer independently

## Common Pitfalls to Avoid

1. **Leaking Dependencies**: Don't let framework dependencies leak into the domain layer
2. **Fat Controllers**: Keep controllers thin, move business logic to use cases
3. **Anemic Models**: Include business logic in entities, not just data
4. **Ignoring the Dependency Rule**: Always ensure dependencies point inward
5. **Mixing Concerns**: Don't mix UI logic with business logic