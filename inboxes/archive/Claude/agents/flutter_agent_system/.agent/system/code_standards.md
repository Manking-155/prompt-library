# Code Standards and Guidelines

## Overview

This document defines the coding standards, conventions, and best practices for Flutter development in this project. Following these standards ensures consistency, maintainability, and code quality across the entire codebase.

## Language and Formatting

### Dart Language Standards
- **Language Version**: Dart 3.0+ with null safety
- **Code Style**: Follow [Effective Dart](https://dart.dev/guides/language/effective-dart) guidelines
- **Formatting**: Use `dart format` with default settings
- **Linting**: Follow rules defined in `analysis_options.yaml`

### Formatting Rules
```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true

linter:
  rules:
    # Dart rules
    - prefer_const_constructors
    - prefer_const_literals_to_create_immutables
    - prefer_final_fields
    - prefer_final_locals
    - avoid_print
    - avoid_unnecessary_containers
    - use_key_in_widget_constructors
    - prefer_single_quotes
    - lines_longer_than_80_chars: false
```

## Naming Conventions

### Files and Directories
- **Files**: `snake_case` (e.g., `user_controller.dart`, `flashcard_service.dart`)
- **Directories**: `snake_case` (e.g., `data/`, `domain/`, `presentation/`)
- **Private files**: Prefix with underscore (e.g., `_internal_helper.dart`)

### Classes and Types
- **Classes**: `PascalCase` (e.g., `UserController`, `FlashcardEntity`)
- **Abstract classes**: Prefix with `Base` or `Abstract` (e.g., `BaseRepository`)
- **Mixins**: `PascalCase` (e.g., `Loggable`, `Cacheable`)

### Variables and Methods
- **Variables**: `camelCase` (e.g., `userName`, `isLoading`)
- **Private members**: Prefix with underscore (e.g., `_privateMethod`, `_privateField`)
- **Constants**: `SCREAMING_SNAKE_CASE` (e.g., `API_BASE_URL`, `MAX_RETRY_COUNT`)
- **Methods**: `camelCase` with descriptive verbs (e.g., `getUserData()`, `validateInput()`)

### Files Organization
```dart
// Copyright notice
// File description

import 'package:flutter/material.dart';
import 'package:get/get.dart';

/// Widget description
class MyWidget extends StatelessWidget {
  // Constants
  static const double _defaultPadding = 16.0;

  // Public fields
  final String title;
  final VoidCallback? onTap;

  // Private fields
  final _isLoading = false.obs;

  // Constructor
  const MyWidget({
    Key? key,
    required this.title,
    this.onTap,
  }) : super(key: key);

  // Build method
  @override
  Widget build(BuildContext context) {
    return Container();
  }

  // Private methods
  void _handleTap() {
    // Implementation
  }
}
```

## Architecture Standards

### Clean Architecture Implementation

#### Domain Layer
```dart
// Entity
class User {
  final String id;
  final String name;

  const User({
    required this.id,
    required this.name,
  });

  // Business logic methods
  bool get isValid => name.isNotEmpty;
}

// Repository Interface
abstract class UserRepository {
  Future<Result<User>> getUser(String id);
}

// Use Case
class GetUserUseCase {
  final UserRepository _repository;

  GetUserUseCase(this._repository);

  Future<Result<User>> execute(String userId) {
    return _repository.getUser(userId);
  }
}
```

#### Data Layer
```dart
// DTO (Data Transfer Object)
class UserDto {
  final String id;
  final String name;

  UserDto({required this.id, required this.name});

  // From JSON
  factory UserDto.fromJson(Map<String, dynamic> json) {
    return UserDto(
      id: json['id'] as String,
      name: json['name'] as String,
    );
  }

  // To Entity
  User toEntity() {
    return User(id: id, name: name);
  }
}

// Repository Implementation
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource _remoteDataSource;

  UserRepositoryImpl(this._remoteDataSource);

  @override
  Future<Result<User>> getUser(String id) async {
    try {
      final dto = await _remoteDataSource.getUser(id);
      return Result.success(dto.toEntity());
    } catch (e) {
      return Result.failure(e.toString());
    }
  }
}
```

#### Presentation Layer
```dart
// GetX Controller
class UserController extends GetxController {
  final GetUserUseCase _getUserUseCase;

  // Reactive variables
  final _user = Rx<User?>(null);
  final _isLoading = false.obs;
  final _error = Rx<String?>(null);

  // Getters
  User? get user => _user.value;
  bool get isLoading => _isLoading.value;
  String? get error => _error.value;

  // Constructor
  UserController(this._getUserUseCase);

  // Public methods
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

## Error Handling Standards

### Result Pattern Implementation
```dart
// Result wrapper
class Result<T> {
  final T? _data;
  final String? _error;

  const Result._(this._data, this._error);

  factory Result.success(T data) => Result._(data, null);
  factory Result.failure(String error) => Result._(null, error);

  bool get isSuccess => _error == null;
  bool get isFailure => _error != null;

  T get data => _data!;
  String get error => _error!;

  R fold<R>(
    R Function(String error) onFailure,
    R Function(T data) onSuccess,
  ) {
    if (isFailure) {
      return onFailure(error);
    } else {
      return onSuccess(data);
    }
  }

  Result<R> map<R>(R Function(T data) mapper) {
    if (isSuccess) {
      return Result.success(mapper(data));
    } else {
      return Result.failure(error);
    }
  }
}
```

### Error Handling in Controllers
```dart
Future<void> performOperation() async {
  try {
    _isLoading.value = true;
    _error.value = null;

    final result = await _useCase.execute();

    result.fold(
      (error) => _error.value = _handleError(error),
      (data) => _handleSuccess(data),
    );
  } catch (e) {
    _error.value = 'Unexpected error occurred';
    _logError(e);
  } finally {
    _isLoading.value = false;
  }
}
```

## State Management Standards

### GetX Best Practices
```dart
class ProductController extends GetxController {
  // Use reactive variables
  final _products = <Product>[].obs;
  final _selectedProduct = Rx<Product?>(null);
  final _isLoading = false.obs;

  // Expose getters, not the reactive variables directly
  List<Product> get products => _products;
  Product? get selectedProduct => _selectedProduct.value;
  bool get isLoading => _isLoading.value;

  // Methods should be descriptive
  Future<void> loadProducts() async {
    _isLoading.value = true;

    try {
      final result = await _productService.getProducts();
      result.fold(
        (error) => Get.snackbar('Error', error),
        (products) => _products.assignAll(products),
      );
    } finally {
      _isLoading.value = false;
    }
  }

  void selectProduct(Product product) {
    _selectedProduct.value = product;
  }
}
```

## Dependency Injection Standards

### Injectable Setup
```dart
// lib/core/di/injection_config.dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';

final GetIt getIt = GetIt.instance;

@injectableInit
Future<void> configureDependencies() async {
  getIt.init();
}

// In use cases
@injectable
class GetUserUseCase {
  final UserRepository _repository;

  GetUserUseCase(this._repository);

  Future<Result<User>> execute(String userId) {
    return _repository.getUser(userId);
  }
}

// In repositories
@injectable
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource _remoteDataSource;
  final UserLocalDataSource _localDataSource;

  UserRepositoryImpl(
    this._remoteDataSource,
    this._localDataSource,
  );

  // Implementation
}
```

## Testing Standards

### Unit Tests
```dart
// test/unit/usecases/get_user_test.dart
void main() {
  late GetUserUseCase useCase;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    useCase = GetUserUseCase(mockRepository);
  });

  group('GetUserUseCase', () {
    test('should return user when repository returns success', () async {
      // Arrange
      const userId = '1';
      const expectedUser = User(id: userId, name: 'John Doe');

      when(() => mockRepository.getUser(userId))
          .thenAnswer((_) async => Result.success(expectedUser));

      // Act
      final result = await useCase.execute(userId);

      // Assert
      expect(result.isSuccess, true);
      expect(result.data, expectedUser);
      verify(() => mockRepository.getUser(userId)).called(1);
    });

    test('should return failure when repository returns error', () async {
      // Arrange
      const userId = '1';
      const errorMessage = 'User not found';

      when(() => mockRepository.getUser(userId))
          .thenAnswer((_) async => Result.failure(errorMessage));

      // Act
      final result = await useCase.execute(userId);

      // Assert
      expect(result.isFailure, true);
      expect(result.error, errorMessage);
    });
  });
}
```

### Widget Tests
```dart
// test/widget/user_profile_test.dart
void main() {
  testWidgets('UserProfile displays user information correctly', (tester) async {
    // Arrange
    const user = User(id: '1', name: 'John Doe');

    // Act
    await tester.pumpWidget(
      GetMaterialApp(
        home: UserProfile(user: user),
      ),
    );

    // Assert
    expect(find.text('John Doe'), findsOneWidget);
    expect(find.text('ID: 1'), findsOneWidget);
  });
}
```

## Documentation Standards

### Code Documentation
```dart
/// A service for managing user authentication.
///
/// This service handles user login, logout, and token management.
/// It uses secure storage to persist authentication tokens.
///
/// Example usage:
/// ```dart
/// final authService = Get.find<AuthService>();
/// final result = await authService.login('user@example.com', 'password');
/// ```
class AuthService {
  /// Authenticates a user with email and password.
  ///
  /// [email] The user's email address
  /// [password] The user's password
  ///
  /// Returns a [Result] containing the user token on success
  /// or an error message on failure.
  ///
  /// Throws:
  /// - [ArgumentError] if email or password is empty
  /// - [NetworkException] if network is unavailable
  Future<Result<String>> login(String email, String password) async {
    // Implementation
  }
}
```

## Performance Guidelines

### Widget Performance
- Use `const` constructors where possible
- Prefer `ListView.builder` for long lists
- Avoid unnecessary widget rebuilds
- Use `AutomaticKeepAliveClientMixin` for complex widgets

### Memory Management
- Dispose controllers and streams properly
- Use weak references where appropriate
- Avoid memory leaks in long-running operations

### Network Optimization
- Implement proper caching strategies
- Use pagination for large datasets
- Handle network timeouts gracefully

## Security Guidelines

### Data Security
- Never store sensitive information in plain text
- Use flutter_secure_storage for sensitive data
- Validate all user inputs
- Implement proper authentication and authorization

### API Security
- Use HTTPS for all network requests
- Implement proper error handling without exposing sensitive information
- Use API keys and tokens securely
- Implement rate limiting and request validation

## Git Conventions

### Commit Messages
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build process or auxiliary tool changes

Examples:
```
feat(auth): add user login functionality
- Implement login use case
- Add login screen with form validation
- Integrate with authentication API

fix(database): resolve user table migration issue
- Update migration script to handle null values
- Add proper error handling for migration failures
```

## Review Process

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] Error handling is implemented
- [ ] No hardcoded values
- [ ] Dependencies are properly declared
- [ ] Security best practices are followed
- [ ] Performance considerations are addressed