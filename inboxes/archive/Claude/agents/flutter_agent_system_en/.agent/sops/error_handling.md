# SOP: Error Handling with Result Wrapper

## Overview
This document describes the error handling pattern using Result wrapper for type-safe error propagation.

## Result Wrapper Pattern

### Overview
Instead of using exceptions, we use a Result wrapper that can hold either a success value or a failure:

```dart
sealed class Result<T, E> {
  const Result();
  
  bool get isSuccess => this is Success;
  bool get isFailure => this is Failure;
  
  factory Result.success(T value) => Success(value);
  factory Result.failure(E error) => Failure(error);
  
  R fold<R>(
    R Function(T success) onSuccess,
    R Function(E failure) onFailure,
  ) {
    return switch (this) {
      Success(value: final value) => onSuccess(value),
      Failure(error: final error) => onFailure(error),
    };
  }
  
  T? getOrNull() => fold((value) => value, (_) => null);
  E? errorOrNull() => fold((_) => null, (error) => error);
}

class Success<T, E> extends Result<T, E> {
  final T value;
  const Success(this.value);
}

class Failure<T, E> extends Result<T, E> {
  final E error;
  const Failure(this.error);
}
```

## Exception Hierarchy

Define custom exceptions for different error scenarios:

```dart
// Base exception
sealed class AppException implements Exception {
  final String message;
  const AppException(this.message);
  
  @override
  String toString() => message;
}

// Network errors
class NetworkException extends AppException {
  const NetworkException([String message = 'Network error occurred'])
    : super(message);
}

class TimeoutException extends NetworkException {
  TimeoutException([String message = 'Request timeout'])
    : super(message);
}

class ServerException extends AppException {
  final int? statusCode;
  const ServerException({
    String message = 'Server error',
    this.statusCode,
  }) : super(message);
}

// Local errors
class DatabaseException extends AppException {
  const DatabaseException([String message = 'Database error'])
    : super(message);
}

class CacheException extends AppException {
  const CacheException([String message = 'Cache error'])
    : super(message);
}

// Validation errors
class ValidationException extends AppException {
  final Map<String, String> errors;
  ValidationException({
    required this.errors,
    String message = 'Validation failed',
  }) : super(message);
}

// Authentication errors
class AuthException extends AppException {
  const AuthException([String message = 'Authentication failed'])
    : super(message);
}

class UnauthorizedException extends AuthException {
  const UnauthorizedException([String message = 'Unauthorized'])
    : super(message);
}

// Generic error
class UnknownException extends AppException {
  final dynamic originalError;
  UnknownException([this.originalError])
    : super('An unknown error occurred');
}
```

## Usage Patterns

### In Repositories

```dart
class UserRepositoryImpl implements UserRepository {
  final UserLocalDatasource local;
  final UserRemoteDatasource remote;
  
  UserRepositoryImpl(this.local, this.remote);
  
  @override
  Future<Result<User, AppException>> getUser(String id) async {
    try {
      // Try local first
      final localUser = await local.getById(id);
      if (localUser != null) {
        return Result.success(localUser);
      }
      
      // Fetch from remote
      final remoteUser = await remote.getUser(id);
      
      // Save to local
      await local.save(remoteUser);
      
      return Result.success(remoteUser);
    } on NetworkException catch (e) {
      return Result.failure(e);
    } on ServerException catch (e) {
      return Result.failure(e);
    } on DatabaseException catch (e) {
      return Result.failure(e);
    } catch (e) {
      return Result.failure(UnknownException(e));
    }
  }
}
```

### In Usecases

```dart
class GetUserUsecase {
  final UserRepository repository;
  
  GetUserUsecase(this.repository);
  
  Future<Result<User, AppException>> call(String id) {
    return repository.getUser(id);
  }
}
```

### In Controllers

```dart
class UserController extends GetxController {
  final GetUserUsecase getUser;
  
  final user = Rxn<User>();
  final isLoading = false.obs;
  final error = Rxn<String>();
  
  UserController(this.getUser);
  
  Future<void> loadUser(String id) async {
    isLoading.value = true;
    error.value = null;
    
    final result = await getUser(id);
    result.fold(
      (user) => this.user.value = user,
      (failure) => error.value = failure.message,
    );
    
    isLoading.value = false;
  }
}
```

### In Views/Pages

```dart
class UserPage extends StatelessWidget {
  const UserPage({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return GetBuilder<UserController>(
      builder: (controller) => Scaffold(
        body: Obx(
          () {
            if (controller.isLoading.value) {
              return const Center(child: CircularProgressIndicator());
            }
            
            if (controller.error.value != null) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(controller.error.value!),
                    ElevatedButton(
                      onPressed: () => controller.loadUser('123'),
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              );
            }
            
            if (controller.user.value != null) {
              return Center(
                child: Text(controller.user.value!.name),
              );
            }
            
            return const SizedBox();
          },
        ),
      ),
    );
  }
}
```

## API Error Handling

### Dio Interceptor

```dart
class AppInterceptor extends QueuedInterceptorsWrapper {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    final appException = _mapDioException(err);
    handler.reject(DioException(
      requestOptions: err.requestOptions,
      response: err.response,
      type: err.type,
      error: appException,
    ));
  }
  
  AppException _mapDioException(DioException err) {
    switch (err.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.sendTimeout:
        return TimeoutException();
        
      case DioExceptionType.badResponse:
        return ServerException(
          message: err.response?.data['message'] ?? 'Server error',
          statusCode: err.response?.statusCode,
        );
        
      case DioExceptionType.connectionError:
        return const NetworkException();
        
      case DioExceptionType.cancel:
        return const NetworkException('Request cancelled');
        
      case DioExceptionType.unknown:
        return UnknownException(err.error);
        
      case DioExceptionType.badCertificate:
        return const NetworkException('Bad certificate');
      
      case DioExceptionType.badRequest:
        return const ServerException(message: 'Bad request');
    }
  }
}

// Setup in Dio
final dio = Dio();
dio.interceptors.add(AppInterceptor());
```

### Remote Datasource

```dart
class UserRemoteDatasourceImpl implements UserRemoteDatasource {
  final Dio dio;
  
  UserRemoteDatasourceImpl(this.dio);
  
  @override
  Future<User> getUser(String id) async {
    try {
      final response = await dio.get('/users/$id');
      
      if (response.statusCode == 200) {
        return UserModel.fromJson(response.data);
      } else {
        throw ServerException(
          message: 'Failed to fetch user',
          statusCode: response.statusCode,
        );
      }
    } on DioException catch (e) {
      throw e.error as AppException;
    } catch (e) {
      throw UnknownException(e);
    }
  }
}
```

## Validation Error Handling

```dart
class ValidationService {
  Result<bool, ValidationException> validateEmail(String email) {
    const emailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$';
    final regex = RegExp(emailPattern);
    
    if (!regex.hasMatch(email)) {
      return Result.failure(
        ValidationException(
          errors: {'email': 'Invalid email format'},
        ),
      );
    }
    
    return Result.success(true);
  }
  
  Result<bool, ValidationException> validatePassword(String password) {
    if (password.length < 8) {
      return Result.failure(
        ValidationException(
          errors: {'password': 'Password must be at least 8 characters'},
        ),
      );
    }
    
    if (!password.contains(RegExp(r'[A-Z]'))) {
      return Result.failure(
        ValidationException(
          errors: {'password': 'Password must contain uppercase letter'},
        ),
      );
    }
    
    return Result.success(true);
  }
  
  Result<bool, ValidationException> validateForm(LoginFormData form) {
    final errors = <String, String>{};
    
    if (form.email.isEmpty) {
      errors['email'] = 'Email is required';
    } else if (!_isValidEmail(form.email)) {
      errors['email'] = 'Invalid email format';
    }
    
    if (form.password.isEmpty) {
      errors['password'] = 'Password is required';
    } else if (form.password.length < 8) {
      errors['password'] = 'Password must be at least 8 characters';
    }
    
    if (errors.isNotEmpty) {
      return Result.failure(
        ValidationException(errors: errors),
      );
    }
    
    return Result.success(true);
  }
}

// Usage in controller
class LoginController extends GetxController {
  final ValidationService validation;
  final emailErrors = ''.obs;
  final passwordErrors = ''.obs;
  
  LoginController(this.validation);
  
  Future<void> login(String email, String password) async {
    // Validate
    final validationResult = validation.validateForm(
      LoginFormData(email: email, password: password),
    );
    
    validationResult.fold(
      (_) => _performLogin(email, password),
      (error) {
        emailErrors.value = error.errors['email'] ?? '';
        passwordErrors.value = error.errors['password'] ?? '';
      },
    );
  }
  
  Future<void> _performLogin(String email, String password) async {
    // Perform login
  }
}
```

## Error Recovery Strategies

### Retry Logic

```dart
Future<Result<T, AppException>> retryable<T>(
  Future<Result<T, AppException>> Function() operation, {
  int maxRetries = 3,
  Duration delay = const Duration(seconds: 1),
}) async {
  for (int i = 0; i < maxRetries; i++) {
    final result = await operation();
    
    if (result.isSuccess) {
      return result;
    }
    
    // Only retry on network errors
    if (result.errorOrNull() is NetworkException) {
      if (i < maxRetries - 1) {
        await Future.delayed(delay * (i + 1));
        continue;
      }
    } else {
      // Don't retry other errors
      return result;
    }
  }
  
  return Result.failure(
    const NetworkException('Max retries exceeded'),
  );
}

// Usage
final result = await retryable(
  () => userRepository.getUser(id),
  maxRetries: 3,
  delay: const Duration(seconds: 2),
);
```

### Fallback Values

```dart
class UserController extends GetxController {
  final users = <User>[].obs;
  
  Future<void> loadUsers() async {
    final result = await userRepository.getUsers();
    
    result.fold(
      (data) => users.value = data,
      (error) {
        // Use cached/fallback data if available
        users.value = _getCachedUsers();
        Get.snackbar('Warning', 'Using cached data: ${error.message}');
      },
    );
  }
  
  List<User> _getCachedUsers() {
    // Return last known good data
    return [];
  }
}
```

## Best Practices

1. **Always return Result**: Never throw exceptions from business logic
2. **Be specific with errors**: Use appropriate exception types
3. **Provide context**: Include meaningful error messages
4. **Handle at appropriate layer**: Handle in controller, propagate from repo
5. **User-friendly messages**: Display appropriate messages to UI
6. **Log errors**: Log for debugging and monitoring
7. **Retry on network**: Only retry transient network errors
8. **Validate early**: Validate input before operations

## Related Documentation
- Clean Architecture Guide: `system/clean_architecture_guide.md`
- Code Standards: `system/code_standards.md`
- Feature Module Template: `templates/feature_module_template.md`
