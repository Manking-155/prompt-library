# Clean Architecture Layers Template

## Overview

This template provides step-by-step implementation of the three Clean Architecture layers: Domain, Data, and Presentation. Each layer has specific responsibilities and dependency rules.

## Architecture Rules

**Dependency Direction**: Only inward dependencies allowed
```
Presentation → Domain ← Data
```

**Layer Responsibilities**:
- **Domain**: Business logic and rules (no dependencies)
- **Data**: Data access and external services (depends on Domain)
- **Presentation**: UI and user interaction (depends on Domain)

## Layer 1: Domain Layer

### Purpose
Contains business logic, entities, use cases, and repository interfaces. Framework-agnostic.

### Directory Structure
```
domain/
├── entities/
│   ├── user_entity.dart
│   └── feature_entity.dart
├── usecases/
│   ├── get_user.dart
│   ├── create_feature.dart
│   └── delete_feature.dart
├── repositories/
│   ├── user_repository.dart
│   └── feature_repository.dart
└── failures/
    ├── failure.dart
    └── server_failure.dart
```

### Step 1: Create Entities

Entities contain business logic and rules:

```dart
// domain/entities/user_entity.dart
import 'package:equatable/equatable.dart';

/// User entity with business logic
class UserEntity extends Equatable {
  final String id;
  final String name;
  final String email;
  final DateTime createdAt;
  final DateTime updatedAt;

  const UserEntity({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
    required this.updatedAt,
  });

  // Business rules
  bool get isValidEmail => _isValidEmail(email);
  bool get isPremiumUser => _hasPremiumAccess();
  Duration get accountAge => DateTime.now().difference(createdAt);

  // Business logic methods
  bool canAccessFeature(String featureName) {
    // Premium users can access all features
    if (isPremiumUser) return true;

    // Regular users have limited access
    const allowedFeatures = ['basic', 'standard'];
    return allowedFeatures.contains(featureName);
  }

  UserEntity copyWith({
    String? id,
    String? name,
    String? email,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return UserEntity(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  // Private business logic methods
  bool _isValidEmail(String email) {
    final emailRegex = RegExp(r'^[^@]+@[^@]+\.[^@]+');
    return emailRegex.hasMatch(email);
  }

  bool _hasPremiumAccess() {
    // Check if user has premium status (simplified)
    return name.startsWith('Premium_');
  }

  @override
  List<Object?> get props => [id, name, email, createdAt, updatedAt];
}
```

### Step 2: Create Repository Interfaces

Abstract contracts for data access:

```dart
// domain/repositories/user_repository.dart
import 'package:dartz/dartz.dart';
import '../entities/user_entity.dart';
import '../failures/failure.dart';

/// Abstract repository for user data operations
abstract class UserRepository {
  /// Get user by ID
  Future<Either<Failure, UserEntity>> getUser(String userId);

  /// Get all users
  Future<Either<Failure, List<UserEntity>>> getAllUsers();

  /// Create new user
  Future<Either<Failure, UserEntity>> createUser(UserEntity user);

  /// Update existing user
  Future<Either<Failure, UserEntity>> updateUser(UserEntity user);

  /// Delete user
  Future<Either<Failure, void>> deleteUser(String userId);

  /// Search users by name
  Future<Either<Failure, List<UserEntity>>> searchUsers(String query);

  /// Authenticate user
  Future<Either<Failure, UserEntity>> authenticate(String email, String password);
}
```

### Step 3: Create Failure Classes

Custom failure types for better error handling:

```dart
// domain/failures/failure.dart
import 'package:equatable/equatable.dart';

/// Base failure class
abstract class Failure extends Equatable {
  final String message;
  final String? code;

  const Failure(this.message, {this.code});

  @override
  List<Object?> get props => [message, code];
}

/// Network failure
class NetworkFailure extends Failure {
  const NetworkFailure(String message, {String? code})
      : super(message, code: code);
}

/// Server failure
class ServerFailure extends Failure {
  const ServerFailure(String message, {String? code})
      : super(message, code: code);
}

/// Validation failure
class ValidationFailure extends Failure {
  const ValidationFailure(String message, {String? code})
      : super(message, code: code);
}

/// Not found failure
class NotFoundFailure extends Failure {
  const NotFoundFailure(String message, {String? code})
      : super(message, code: code);
}

/// Permission denied failure
class PermissionDeniedFailure extends Failure {
  const PermissionDeniedFailure(String message, {String? code})
      : super(message, code: code);
}

/// Cache failure
class CacheFailure extends Failure {
  const CacheFailure(String message, {String? code})
      : super(message, code: code);
}
```

### Step 4: Create Use Cases

Business logic operations:

```dart
// domain/usecases/get_user.dart
import 'package:dartz/dartz.dart';
import '../entities/user_entity.dart';
import '../repositories/user_repository.dart';
import '../failures/failure.dart';

/// Get user by ID use case
class GetUserUseCase {
  final UserRepository _repository;

  GetUserUseCase(this._repository);

  /// Execute the use case
  Future<Either<Failure, UserEntity>> execute(String userId) async {
    // Input validation
    if (userId.isEmpty) {
      return const Left(
        ValidationFailure('User ID cannot be empty', code: 'INVALID_INPUT'),
      );
    }

    // Check if user ID format is valid
    if (!_isValidUserId(userId)) {
      return const Left(
        ValidationFailure('Invalid user ID format', code: 'INVALID_FORMAT'),
      );
    }

    // Execute repository operation
    final result = await _repository.getUser(userId);

    return result.fold(
      (failure) => Left(failure),
      (user) {
        // Business rule: Ensure user is not deleted
        if (_isUserDeleted(user)) {
          return const Left(
            NotFoundFailure('User not found or deleted', code: 'USER_NOT_FOUND'),
          );
        }
        return Right(user);
      },
    );
  }

  /// Business logic for user ID validation
  bool _isValidUserId(String userId) {
    // UUID format validation (simplified)
    final uuidRegex = RegExp(
      r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
      caseSensitive: false,
    );
    return uuidRegex.hasMatch(userId);
  }

  /// Business logic for deleted user check
  bool _isUserDeleted(UserEntity user) {
    // Example: Check if user was deleted more than 30 days ago
    final thirtyDaysAgo = DateTime.now().subtract(const Duration(days: 30));
    return user.updatedAt.isBefore(thirtyDaysAgo) && user.name.startsWith('DELETED_');
  }
}
```

```dart
// domain/usecases/authenticate_user.dart
import 'package:dartz/dartz.dart';
import '../entities/user_entity.dart';
import '../repositories/user_repository.dart';
import '../failures/failure.dart';

/// Authenticate user use case
class AuthenticateUserUseCase {
  final UserRepository _repository;

  AuthenticateUserUseCase(this._repository);

  /// Execute authentication
  Future<Either<Failure, UserEntity>> execute(String email, String password) async {
    // Input validation
    final emailValidation = _validateEmail(email);
    if (emailValidation != null) {
      return Left(emailValidation);
    }

    final passwordValidation = _validatePassword(password);
    if (passwordValidation != null) {
      return Left(passwordValidation);
    }

    // Rate limiting check (business rule)
    if (await _isRateLimited(email)) {
      return const Left(
        PermissionDeniedFailure(
          'Too many login attempts. Please try again later.',
          code: 'RATE_LIMITED',
        ),
      );
    }

    // Execute authentication
    final result = await _repository.authenticate(email, password);

    return result.fold(
      (failure) => Left(failure),
      (user) {
        // Business rule: Log successful login
        _logSuccessfulLogin(user);
        return Right(user);
      },
    );
  }

  ValidationFailure? _validateEmail(String email) {
    if (email.isEmpty) {
      return const ValidationFailure('Email is required', code: 'EMAIL_REQUIRED');
    }

    final emailRegex = RegExp(r'^[^@]+@[^@]+\.[^@]+');
    if (!emailRegex.hasMatch(email)) {
      return const ValidationFailure('Invalid email format', code: 'INVALID_EMAIL');
    }

    return null;
  }

  ValidationFailure? _validatePassword(String password) {
    if (password.isEmpty) {
      return const ValidationFailure('Password is required', code: 'PASSWORD_REQUIRED');
    }

    if (password.length < 8) {
      return const ValidationFailure(
        'Password must be at least 8 characters',
        code: 'PASSWORD_TOO_SHORT',
      );
    }

    return null;
  }

  Future<bool> _isRateLimited(String email) async {
    // Implement rate limiting logic
    // This could use a cache or database to track attempts
    return false; // Simplified for example
  }

  void _logSuccessfulLogin(UserEntity user) {
    // Log successful authentication
    // This could be sent to analytics or audit log
    print('User ${user.id} logged in successfully at ${DateTime.now()}');
  }
}
```

## Layer 2: Data Layer

### Purpose
Handles data access, external services, and implements repository interfaces.

### Directory Structure
```
data/
├── datasources/
│   ├── local/
│   │   ├── user_local_datasource.dart
│   │   └── user_local_datasource_impl.dart
│   ├── remote/
│   │   ├── user_remote_datasource.dart
│   │   └── user_remote_datasource_impl.dart
│   └── cache/
│       ├── user_cache_datasource.dart
│       └── user_cache_datasource_impl.dart
├── models/
│   ├── user_model.dart
│   └── user_dto.dart
├── repositories/
│   └── user_repository_impl.dart
└── mappers/
    └── user_mapper.dart
```

### Step 1: Create Data Models

Data transfer objects for external communication:

```dart
// data/models/user_model.dart
import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/user_entity.dart';

part 'user_model.g.dart';

/// User model for API communication
@JsonSerializable()
class UserModel {
  @JsonKey(name: 'user_id')
  final String id;
  @JsonKey(name: 'full_name')
  final String name;
  @JsonKey(name: 'email_address')
  final String email;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  @JsonKey(name: 'updated_at')
  final DateTime updatedAt;
  @JsonKey(name: 'avatar_url')
  final String? avatarUrl;
  @JsonKey(name: 'is_active')
  final bool isActive;

  const UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
    required this.updatedAt,
    this.avatarUrl,
    required this.isActive,
  });

  /// From JSON constructor
  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);

  /// To JSON method
  Map<String, dynamic> toJson() => _$UserModelToJson(this);

  /// Convert to domain entity
  UserEntity toEntity() {
    return UserEntity(
      id: id,
      name: name,
      email: email,
      createdAt: createdAt,
      updatedAt: updatedAt,
    );
  }

  /// Convert from domain entity
  factory UserModel.fromEntity(UserEntity entity) {
    return UserModel(
      id: entity.id,
      name: entity.name,
      email: entity.email,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
      isActive: true, // Default value for API
    );
  }

  /// Copy with method
  UserModel copyWith({
    String? id,
    String? name,
    String? email,
    DateTime? createdAt,
    DateTime? updatedAt,
    String? avatarUrl,
    bool? isActive,
  }) {
    return UserModel(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      avatarUrl: avatarUrl ?? this.avatarUrl,
      isActive: isActive ?? this.isActive,
    );
  }
}
```

### Step 2: Create Data Sources

External data access implementations:

```dart
// data/datasources/remote/user_remote_datasource.dart
import 'package:dartz/dartz.dart';
import '../../models/user_model.dart';
import '../../../domain/failures/failure.dart';

/// Abstract remote data source for users
abstract class UserRemoteDataSource {
  /// Get user by ID from remote API
  Future<Either<Failure, UserModel>> getUser(String userId);

  /// Get all users from remote API
  Future<Either<Failure, List<UserModel>>> getAllUsers();

  /// Create user in remote API
  Future<Either<Failure, UserModel>> createUser(UserModel user);

  /// Update user in remote API
  Future<Either<Failure, UserModel>> updateUser(UserModel user);

  /// Delete user from remote API
  Future<Either<Failure, void>> deleteUser(String userId);

  /// Authenticate user with remote API
  Future<Either<Failure, UserModel>> authenticate(String email, String password);
}
```

```dart
// data/datasources/remote/user_remote_datasource_impl.dart
import 'package:dartz/dartz.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'user_remote_datasource.dart';
import '../../models/user_model.dart';
import '../../../domain/failures/failure.dart';

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final http.Client _client;
  final String _baseUrl;

  UserRemoteDataSourceImpl(this._client, this._baseUrl);

  @override
  Future<Either<Failure, UserModel>> getUser(String userId) async {
    try {
      final response = await _client.get(
        Uri.parse('$_baseUrl/users/$userId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body) as Map<String, dynamic>;
        final userModel = UserModel.fromJson(jsonData);
        return Right(userModel);
      } else if (response.statusCode == 404) {
        return const Left(NotFoundFailure('User not found', code: 'USER_NOT_FOUND'));
      } else {
        return Left(ServerFailure(
          'Failed to get user: ${response.statusCode}',
          code: 'SERVER_ERROR',
        ));
      }
    } on SocketException {
      return const Left(NetworkFailure('No internet connection', code: 'NO_INTERNET'));
    } catch (e) {
      return Left(ServerFailure('Unexpected error: $e', code: 'UNKNOWN_ERROR'));
    }
  }

  @override
  Future<Either<Failure, List<UserModel>>> getAllUsers() async {
    try {
      final response = await _client.get(
        Uri.parse('$_baseUrl/users'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body) as List;
        final users = jsonData
            .map((userJson) => UserModel.fromJson(userJson as Map<String, dynamic>))
            .toList();
        return Right(users);
      } else {
        return Left(ServerFailure(
          'Failed to get users: ${response.statusCode}',
          code: 'SERVER_ERROR',
        ));
      }
    } on SocketException {
      return const Left(NetworkFailure('No internet connection', code: 'NO_INTERNET'));
    } catch (e) {
      return Left(ServerFailure('Unexpected error: $e', code: 'UNKNOWN_ERROR'));
    }
  }

  @override
  Future<Either<Failure, UserModel>> authenticate(String email, String password) async {
    try {
      final response = await _client.post(
        Uri.parse('$_baseUrl/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'email': email,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body) as Map<String, dynamic>;
        final userModel = UserModel.fromJson(jsonData['user'] as Map<String, dynamic>);
        return Right(userModel);
      } else if (response.statusCode == 401) {
        return const Left(
          ValidationFailure('Invalid email or password', code: 'INVALID_CREDENTIALS'),
        );
      } else {
        return Left(ServerFailure(
          'Authentication failed: ${response.statusCode}',
          code: 'AUTH_ERROR',
        ));
      }
    } on SocketException {
      return const Left(NetworkFailure('No internet connection', code: 'NO_INTERNET'));
    } catch (e) {
      return Left(ServerFailure('Unexpected error: $e', code: 'UNKNOWN_ERROR'));
    }
  }

  @override
  Future<Either<Failure, UserModel>> createUser(UserModel user) async {
    // Implementation similar to above methods
    try {
      final response = await _client.post(
        Uri.parse('$_baseUrl/users'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(user.toJson()),
      );

      if (response.statusCode == 201) {
        final jsonData = json.decode(response.body) as Map<String, dynamic>;
        final createdUser = UserModel.fromJson(jsonData);
        return Right(createdUser);
      } else {
        return Left(ServerFailure(
          'Failed to create user: ${response.statusCode}',
          code: 'CREATE_ERROR',
        ));
      }
    } catch (e) {
      return Left(ServerFailure('Unexpected error: $e', code: 'UNKNOWN_ERROR'));
    }
  }

  @override
  Future<Either<Failure, UserModel>> updateUser(UserModel user) async {
    // Implementation similar to above methods
    try {
      final response = await _client.put(
        Uri.parse('$_baseUrl/users/${user.id}'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(user.toJson()),
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body) as Map<String, dynamic>;
        final updatedUser = UserModel.fromJson(jsonData);
        return Right(updatedUser);
      } else if (response.statusCode == 404) {
        return const Left(NotFoundFailure('User not found', code: 'USER_NOT_FOUND'));
      } else {
        return Left(ServerFailure(
          'Failed to update user: ${response.statusCode}',
          code: 'UPDATE_ERROR',
        ));
      }
    } catch (e) {
      return Left(ServerFailure('Unexpected error: $e', code: 'UNKNOWN_ERROR'));
    }
  }

  @override
  Future<Either<Failure, void>> deleteUser(String userId) async {
    try {
      final response = await _client.delete(
        Uri.parse('$_baseUrl/users/$userId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 204) {
        return const Right(null);
      } else if (response.statusCode == 404) {
        return const Left(NotFoundFailure('User not found', code: 'USER_NOT_FOUND'));
      } else {
        return Left(ServerFailure(
          'Failed to delete user: ${response.statusCode}',
          code: 'DELETE_ERROR',
        ));
      }
    } catch (e) {
      return Left(ServerFailure('Unexpected error: $e', code: 'UNKNOWN_ERROR'));
    }
  }
}
```

### Step 3: Create Repository Implementation

Concrete implementation of domain repository:

```dart
// data/repositories/user_repository_impl.dart
import 'package:dartz/dartz.dart';
import '../../domain/entities/user_entity.dart';
import '../../domain/repositories/user_repository.dart';
import '../../domain/failures/failure.dart';
import '../datasources/remote/user_remote_datasource.dart';
import '../datasources/local/user_local_datasource.dart';
import '../models/user_model.dart';
import '../mappers/user_mapper.dart';

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource _remoteDataSource;
  final UserLocalDataSource _localDataSource;
  final UserMapper _mapper;

  UserRepositoryImpl(
    this._remoteDataSource,
    this._localDataSource,
    this._mapper,
  );

  @override
  Future<Either<Failure, UserEntity>> getUser(String userId) async {
    try {
      // Offline-first: Try local cache first
      final localUser = await _localDataSource.getUser(userId);
      if (localUser != null) {
        // Update in background if data is stale
        _updateUserInBackground(userId);
        return Right(localUser);
      }

      // Fallback to remote
      final remoteResult = await _remoteDataSource.getUser(userId);

      return remoteResult.fold(
        (failure) => Left(failure),
        (userModel) async {
          // Cache locally for offline use
          final userEntity = _mapper.modelToEntity(userModel);
          await _localDataSource.saveUser(userModel);
          return Right(userEntity);
        },
      );
    } catch (e) {
      return Left(CacheFailure('Failed to get user: $e', code: 'CACHE_ERROR'));
    }
  }

  @override
  Future<Either<Failure, List<UserEntity>>> getAllUsers() async {
    try {
      // Try local first
      final localUsers = await _localDataSource.getAllUsers();
      if (localUsers.isNotEmpty) {
        final entities = localUsers.map(_mapper.modelToEntity).toList();
        return Right(entities);
      }

      // Fallback to remote
      final remoteResult = await _remoteDataSource.getAllUsers();

      return remoteResult.fold(
        (failure) => Left(failure),
        (userModels) async {
          // Cache locally
          await _localDataSource.saveAllUsers(userModels);
          final entities = userModels.map(_mapper.modelToEntity).toList();
          return Right(entities);
        },
      );
    } catch (e) {
      return Left(CacheFailure('Failed to get users: $e', code: 'CACHE_ERROR'));
    }
  }

  @override
  Future<Either<Failure, UserEntity>> authenticate(String email, String password) async {
    final remoteResult = await _remoteDataSource.authenticate(email, password);

    return remoteResult.fold(
      (failure) => Left(failure),
      (userModel) async {
        // Cache authenticated user
        final userEntity = _mapper.modelToEntity(userModel);
        await _localDataSource.saveUser(userModel);

        // Save authentication state
        await _localDataSource.saveAuthToken(userModel.id);

        return Right(userEntity);
      },
    );
  }

  @override
  Future<Either<Failure, UserEntity>> createUser(UserEntity user) async {
    final userModel = _mapper.entityToModel(user);
    final remoteResult = await _remoteDataSource.createUser(userModel);

    return remoteResult.fold(
      (failure) => Left(failure),
      (createdModel) async {
        // Cache locally
        final createdEntity = _mapper.modelToEntity(createdModel);
        await _localDataSource.saveUser(createdModel);
        return Right(createdEntity);
      },
    );
  }

  @override
  Future<Either<Failure, UserEntity>> updateUser(UserEntity user) async {
    final userModel = _mapper.entityToModel(user);
    final remoteResult = await _remoteDataSource.updateUser(userModel);

    return remoteResult.fold(
      (failure) => Left(failure),
      (updatedModel) async {
        // Update local cache
        final updatedEntity = _mapper.modelToEntity(updatedModel);
        await _localDataSource.updateUser(updatedModel);
        return Right(updatedEntity);
      },
    );
  }

  @override
  Future<Either<Failure, void>> deleteUser(String userId) async {
    final remoteResult = await _remoteDataSource.deleteUser(userId);

    return remoteResult.fold(
      (failure) => Left(failure),
      (_) async {
        // Remove from local cache
        await _localDataSource.deleteUser(userId);
        return const Right(null);
      },
    );
  }

  @override
  Future<Either<Failure, List<UserEntity>>> searchUsers(String query) async {
    // Try local search first
    final localResults = await _localDataSource.searchUsers(query);
    if (localResults.isNotEmpty) {
      final entities = localResults.map(_mapper.modelToEntity).toList();
      return Right(entities);
    }

    // Fallback to remote search
    // This would require implementing search in remote data source
    // For now, return empty list
    return const Right([]);
  }

  /// Background update method to refresh stale data
  Future<void> _updateUserInBackground(String userId) async {
    try {
      final remoteResult = await _remoteDataSource.getUser(userId);
      remoteResult.fold(
        (failure) => null, // Ignore errors in background
        (userModel) async {
          await _localDataSource.updateUser(userModel);
        },
      );
    } catch (e) {
      // Ignore errors in background update
    }
  }
}
```

## Layer 3: Presentation Layer

### Purpose
Handles UI, user interaction, and state management.

### Directory Structure
```
presentation/
├── controllers/
│   ├── user_controller.dart
│   └── auth_controller.dart
├── views/
│   ├── user_list_view.dart
│   ├── user_detail_view.dart
│   └── login_view.dart
├── widgets/
│   ├── user_card.dart
│   ├── user_form.dart
│   └── loading_widget.dart
└── bindings/
    └── user_binding.dart
```

### Step 1: Create GetX Controllers

State management and business logic coordination:

```dart
// presentation/controllers/user_controller.dart
import 'package:get/get.dart';
import 'package:dartz/dartz.dart';
import '../../domain/entities/user_entity.dart';
import '../../domain/usecases/get_user.dart';
import '../../domain/usecases/get_all_users.dart';
import '../../domain/usecases/create_user.dart';
import '../../domain/usecases/update_user.dart';
import '../../domain/usecases/delete_user.dart';
import '../../domain/failures/failure.dart';

class UserController extends GetxController {
  final GetAllUsersUseCase _getAllUsersUseCase;
  final GetUserUseCase _getUserUseCase;
  final CreateUserUseCase _createUserUseCase;
  final UpdateUserUseCase _updateUserUseCase;
  final DeleteUserUseCase _deleteUserUseCase;

  // Reactive state
  final _users = <UserEntity>[].obs;
  final _selectedUser = Rx<UserEntity?>(null);
  final _isLoading = false.obs;
  final _error = Rx<String?>(null);
  final _searchQuery = ''.obs;

  // Computed properties
  List<UserEntity> get users => _filteredUsers;
  UserEntity? get selectedUser => _selectedUser.value;
  bool get isLoading => _isLoading.value;
  String? get error => _error.value;
  String get searchQuery => _searchQuery.value;

  List<UserEntity> get _filteredUsers {
    if (_searchQuery.value.isEmpty) {
      return _users;
    }
    return _users.where((user) =>
        user.name.toLowerCase().contains(_searchQuery.value.toLowerCase()) ||
        user.email.toLowerCase().contains(_searchQuery.value.toLowerCase())
    ).toList();
  }

  UserController({
    required GetAllUsersUseCase getAllUsersUseCase,
    required GetUserUseCase getUserUseCase,
    required CreateUserUseCase createUserUseCase,
    required UpdateUserUseCase updateUserUseCase,
    required DeleteUserUseCase deleteUserUseCase,
  })  : _getAllUsersUseCase = getAllUsersUseCase,
        _getUserUseCase = getUserUseCase,
        _createUserUseCase = createUserUseCase,
        _updateUserUseCase = updateUserUseCase,
        _deleteUserUseCase = deleteUserUseCase;

  @override
  void onInit() {
    super.onInit();
    loadUsers();
  }

  /// Load all users
  Future<void> loadUsers() async {
    _setLoading(true);
    _clearError();

    final result = await _getAllUsersUseCase.execute();

    result.fold(
      (failure) => _handleFailure(failure),
      (users) => _users.assignAll(users),
    );

    _setLoading(false);
  }

  /// Load specific user
  Future<void> loadUser(String userId) async {
    _setLoading(true);
    _clearError();

    final result = await _getUserUseCase.execute(userId);

    result.fold(
      (failure) => _handleFailure(failure),
      (user) => _selectedUser.value = user,
    );

    _setLoading(false);
  }

  /// Create new user
  Future<void> createUser(UserEntity user) async {
    _setLoading(true);
    _clearError();

    final result = await _createUserUseCase.execute(user);

    result.fold(
      (failure) => _handleFailure(failure),
      (createdUser) {
        _users.add(createdUser);
        _selectedUser.value = createdUser;
        Get.snackbar('Success', 'User created successfully');
        Get.back(); // Go back to previous screen
      },
    );

    _setLoading(false);
  }

  /// Update existing user
  Future<void> updateUser(UserEntity user) async {
    _setLoading(true);
    _clearError();

    final result = await _updateUserUseCase.execute(user);

    result.fold(
      (failure) => _handleFailure(failure),
      (updatedUser) {
        final index = _users.indexWhere((u) => u.id == updatedUser.id);
        if (index != -1) {
          _users[index] = updatedUser;
        }
        if (_selectedUser.value?.id == updatedUser.id) {
          _selectedUser.value = updatedUser;
        }
        Get.snackbar('Success', 'User updated successfully');
        Get.back();
      },
    );

    _setLoading(false);
  }

  /// Delete user
  Future<void> deleteUser(String userId) async {
    _setLoading(true);
    _clearError();

    final result = await _deleteUserUseCase.execute(userId);

    result.fold(
      (failure) => _handleFailure(failure),
      (_) {
        _users.removeWhere((user) => user.id == userId);
        if (_selectedUser.value?.id == userId) {
          _selectedUser.value = null;
        }
        Get.snackbar('Success', 'User deleted successfully');
        Get.back();
      },
    );

    _setLoading(false);
  }

  /// Select a user
  void selectUser(UserEntity user) {
    _selectedUser.value = user;
  }

  /// Clear selected user
  void clearSelectedUser() {
    _selectedUser.value = null;
  }

  /// Update search query
  void updateSearchQuery(String query) {
    _searchQuery.value = query;
  }

  /// Clear search
  void clearSearch() {
    _searchQuery.value = '';
  }

  /// Refresh users
  Future<void> refresh() async {
    await loadUsers();
  }

  // Private helper methods
  void _setLoading(bool loading) {
    _isLoading.value = loading;
  }

  void _setError(String error) {
    _error.value = error;
    Get.snackbar('Error', error, backgroundColor: Colors.red);
  }

  void _clearError() {
    _error.value = null;
  }

  void _handleFailure(Failure failure) {
    switch (failure.runtimeType) {
      case NetworkFailure:
        _setError('Network error. Please check your internet connection.');
        break;
      case ServerFailure:
        _setError('Server error. Please try again later.');
        break;
      case ValidationFailure:
        _setError(failure.message);
        break;
      case NotFoundFailure:
        _setError('User not found.');
        break;
      case PermissionDeniedFailure:
        _setError('Permission denied. You don\'t have access to this resource.');
        break;
      case CacheFailure:
        _setError('Cache error. Please try refreshing.');
        break;
      default:
        _setError('An unexpected error occurred. Please try again.');
    }
  }
}
```

### Step 2: Create Views

UI components that observe controller state:

```dart
// presentation/views/user_list_view.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/user_controller.dart';
import '../widgets/user_card.dart';
import '../widgets/loading_widget.dart';
import '../widgets/empty_state_widget.dart';
import '../widgets/search_bar_widget.dart';

class UserListView extends GetView<UserController> {
  const UserListView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Users'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: controller.refresh,
            tooltip: 'Refresh',
          ),
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: _showSearchDialog,
            tooltip: 'Search',
          ),
        ],
      ),
      body: Column(
        children: [
          // Search bar (shown when there's a search query)
          Obx(() => controller.searchQuery.isNotEmpty
              ? SearchBarWidget(
                  query: controller.searchQuery,
                  onChanged: controller.updateSearchQuery,
                  onClear: controller.clearSearch,
                )
              : const SizedBox.shrink()),

          // Main content
          Expanded(
            child: Obx(() {
              if (controller.isLoading.value) {
                return const LoadingWidget();
              }

              if (controller.error.value != null) {
                return _buildErrorState();
              }

              if (controller.users.isEmpty) {
                return const EmptyStateWidget(
                  title: 'No Users Found',
                  subtitle: 'Start by adding your first user',
                  icon: Icons.people_outline,
                );
              }

              return RefreshIndicator(
                onRefresh: controller.refresh,
                child: ListView.builder(
                  itemCount: controller.users.length,
                  itemBuilder: (context, index) {
                    final user = controller.users[index];
                    return UserCard(
                      user: user,
                      onTap: () => _navigateToUserDetail(user),
                      onEdit: () => _navigateToEditUser(user),
                      onDelete: () => _showDeleteConfirmation(user),
                    );
                  },
                ),
              );
            }),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _navigateToCreateUser,
        child: const Icon(Icons.add),
        tooltip: 'Add User',
      ),
    );
  }

  Widget _buildErrorState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(
            Icons.error_outline,
            size: 64,
            color: Colors.red,
          ),
          const SizedBox(height: 16),
          Text(
            'Error: ${controller.error.value}',
            style: const TextStyle(
              fontSize: 16,
              color: Colors.red,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: controller.refresh,
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  }

  void _showSearchDialog() {
    Get.dialog(
      AlertDialog(
        title: const Text('Search Users'),
        content: TextField(
          onChanged: controller.updateSearchQuery,
          decoration: const InputDecoration(
            hintText: 'Enter name or email...',
            border: OutlineInputBorder(),
          ),
          autofocus: true,
        ),
        actions: [
          TextButton(
            onPressed: () {
              controller.clearSearch();
              Get.back();
            },
            child: const Text('Clear'),
          ),
          TextButton(
            onPressed: Get.back,
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  void _navigateToUserDetail(UserEntity user) {
    controller.selectUser(user);
    Get.toNamed('/users/${user.id}', arguments: user);
  }

  void _navigateToEditUser(UserEntity user) {
    controller.selectUser(user);
    Get.toNamed('/users/${user.id}/edit', arguments: user);
  }

  void _navigateToCreateUser() {
    Get.toNamed('/users/create');
  }

  void _showDeleteConfirmation(UserEntity user) {
    Get.dialog(
      AlertDialog(
        title: const Text('Delete User'),
        content: Text('Are you sure you want to delete ${user.name}?'),
        actions: [
          TextButton(
            onPressed: Get.back,
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Get.back();
              controller.deleteUser(user.id);
            },
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Delete'),
          ),
        ],
      ),
    );
  }
}
```

## Implementation Checklist

### Domain Layer
- [ ] Entities created with business logic
- [ ] Repository interfaces defined
- [ ] Use cases implemented with business rules
- [ ] Failure classes created
- [ ] Input validation in use cases

### Data Layer
- [ ] Data models (DTOs) created
- [ ] Remote data source implemented
- [ ] Local data source implemented
- [ ] Repository implementation created
- [ ] Mappers between models and entities
- [ ] Offline-first strategy implemented

### Presentation Layer
- [ ] GetX controllers created
- [ ] Reactive state management
- [ ] Views implemented
- [ ] Widgets created
- [ ] Error handling in UI
- [ ] Loading states handled

### Integration
- [ ] Dependency injection configured
- [ ] Navigation set up
- [ ] Testing implemented
- [ ] Error handling across layers
- [ ] Logging implemented
- [ ] Performance optimization

## Best Practices

1. **Keep layers separate** - Never skip layers in dependency flow
2. **Use dependency injection** - Make testing and swapping implementations easy
3. **Handle errors properly** - Use Either/Result pattern consistently
4. **Implement offline-first** - Cache data locally for better UX
5. **Write tests** - Test each layer independently
6. **Use reactive programming** - Leverage GetX reactive variables
7. **Follow naming conventions** - Be consistent across the codebase
8. **Document your code** - Explain business logic and architectural decisions