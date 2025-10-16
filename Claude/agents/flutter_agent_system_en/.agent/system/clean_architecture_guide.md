# Clean Architecture Guide

## Overview

Clean Architecture is an approach to building software that results in testable, maintainable, and scalable applications. In this project, we implement Clean Architecture with 3 distinct layers:

1. **Presentation Layer** - UI and Controllers
2. **Domain Layer** - Business Logic and Rules
3. **Data Layer** - External Data Sources

## The Three Layers

### 1. Presentation Layer
The outermost layer that directly interacts with users.

**Responsibilities:**
- Display UI components
- Handle user interactions
- Manage local UI state using GetX controllers
- Call domain usecases based on user actions

**Components:**
```
presentation/
├── pages/              # Full-screen widgets
│   └── user_profile_page.dart
├── widgets/            # Reusable UI components
│   └── user_card.dart
├── controllers/        # GetX controllers for state management
│   └── user_controller.dart
└── bindings/           # GetX dependency bindings
    └── user_binding.dart
```

**Key Rules:**
- Only GetX controllers manage state
- Controllers are disposed automatically
- Pages should NOT contain business logic
- Only use widgets for UI rendering

**Example Controller:**
```dart
class UserController extends GetxController {
  final GetUserUsecase getUser;
  
  UserController(this.getUser);
  
  final users = <User>[].obs;
  final isLoading = false.obs;
  
  @override
  void onInit() {
    fetchUsers();
    super.onInit();
  }
  
  Future<void> fetchUsers() async {
    isLoading.value = true;
    final result = await getUser();
    
    result.fold(
      (users) => this.users.value = users,
      (error) => Get.snackbar('Error', error.message),
    );
    
    isLoading.value = false;
  }
}
```

### 2. Domain Layer
The innermost layer containing pure business logic, independent of frameworks.

**Responsibilities:**
- Define business entities
- Declare repository interfaces
- Implement use cases (business rules)

**Components:**
```
domain/
├── entities/          # Business objects (immutable)
│   └── user.dart
├── repositories/      # Abstract repository interfaces
│   └── user_repository.dart
└── usecases/          # Business logic operations
    └── get_user_usecase.dart
```

**Key Rules:**
- NO framework dependencies (no Flutter, no GetX, no HTTP client)
- Entities are immutable
- Repositories are abstract interfaces only
- Usecases orchestrate business logic

**Example Entity:**
```dart
class User {
  final String id;
  final String name;
  final String email;
  
  const User({
    required this.id,
    required this.name,
    required this.email,
  });
}
```

**Example Usecase:**
```dart
class GetUsersUsecase {
  final UserRepository repository;
  
  GetUsersUsecase(this.repository);
  
  Future<Result<List<User>, Exception>> call() async {
    return repository.getUsers();
  }
}
```

### 3. Data Layer
The outermost layer that interacts with external data sources.

**Responsibilities:**
- Implement repository interfaces from domain layer
- Handle API calls and database operations
- Map between data models and domain entities
- Manage data caching and synchronization

**Components:**
```
data/
├── datasources/       # Local and remote data sources
│   ├── local/
│   │   └── user_local_datasource.dart
│   └── remote/
│       └── user_remote_datasource.dart
├── models/            # Data transfer objects (DTOs)
│   └── user_model.dart
└── repositories/      # Repository implementations
    └── user_repository_impl.dart
```

**Key Rules:**
- Repositories implement domain interfaces
- Models handle serialization/deserialization
- Datasources are independent
- Handle both local (SQLite) and remote (API) data

**Example Model (DTO):**
```dart
class UserModel extends User {
  UserModel({
    required String id,
    required String name,
    required String email,
  }) : super(id: id, name: name, email: email);
  
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      name: json['name'],
      email: json['email'],
    );
  }
  
  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'email': email,
  };
}
```

**Example Repository Implementation:**
```dart
class UserRepositoryImpl implements UserRepository {
  final UserLocalDatasource localDatasource;
  final UserRemoteDatasource remoteDatasource;
  
  UserRepositoryImpl(this.localDatasource, this.remoteDatasource);
  
  @override
  Future<Result<List<User>, Exception>> getUsers() async {
    try {
      // Check if we have cached data
      final localUsers = await localDatasource.getUsers();
      if (localUsers.isNotEmpty) {
        return Result.success(localUsers);
      }
      
      // Fetch from remote if no local cache
      final remoteUsers = await remoteDatasource.getUsers();
      await localDatasource.saveUsers(remoteUsers);
      
      return Result.success(remoteUsers);
    } catch (e) {
      return Result.failure(Exception(e.toString()));
    }
  }
}
```

## Data Flow

```
User Action
    ↓
Presentation Controller
    ↓
Domain Usecase
    ↓
Domain Repository (abstract)
    ↓
Data Repository Implementation
    ↓
Datasources (Local/Remote)
    ↓
Database/API
    ↓
Response (Result wrapper)
    ↓
UI Update
```

## Error Handling

All operations use the Result wrapper pattern:

```dart
Result<T, Exception> result;

result.fold(
  (success) => handleSuccess(success),
  (error) => handleError(error),
);
```

This ensures:
- Explicit error handling
- No uncaught exceptions
- Type-safe error propagation

## Testing Strategy

Each layer has corresponding tests:

```
test/
├── unit/
│   ├── domain/         # Test usecases & entities
│   ├── data/           # Test repositories & datasources
│   └── presentation/   # Test controllers
├── widget/             # Test UI components
└── integration/        # Test full user flows
```

## Related Documentation
- Modular Architecture: `system/modular_architecture_guide.md`
- Code Standards: `system/code_standards.md`
- Feature Module Template: `templates/feature_module_template.md`
