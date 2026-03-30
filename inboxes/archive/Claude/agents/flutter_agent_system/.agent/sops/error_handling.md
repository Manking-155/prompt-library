# SOP: Error Handling with Result Pattern

## Overview

This Standard Operating Procedure (SOP) outlines the consistent approach for error handling throughout the Flutter application using the Result pattern. This ensures robust error handling, better user experience, and easier debugging.

## Prerequisites

- Understanding of Result/Either pattern
- GetX for state management
- Custom failure classes
- Proper logging implementation

## Key Concepts

### Error Types
- **Network Errors**: Connectivity issues, API failures
- **Validation Errors**: Input validation failures
- **Business Logic Errors**: Domain-specific rule violations
- **System Errors**: Database, file system, hardware issues
- **User Errors**: Permission denied, authentication failures

### Result Pattern
- **Success**: Operation completed successfully
- **Failure**: Operation failed with specific error information

## Step-by-Step Process

### Phase 1: Setting Up Error Handling Infrastructure

#### 1.1 Create Base Result Class
Create file: `lib/core/utils/result.dart`:
```dart
import 'package:equatable/equatable.dart';

/// Result wrapper for operations that can fail
class Result<T> extends Equatable {
  final T? _data;
  final Failure? _failure;

  const Result._(this._data, this._failure);

  /// Create success result
  factory Result.success(T data) => Result._(data, null);

  /// Create failure result
  factory Result.failure(Failure failure) => Result._(null, failure);

  /// Check if result is success
  bool get isSuccess => _failure == null;

  /// Check if result is failure
  bool get isFailure => _failure != null;

  /// Get data (throws if failure)
  T get data {
    if (isFailure) {
      throw Exception('Cannot access data on failure result: ${_failure!.message}');
    }
    return _data as T;
  }

  /// Get data or null
  T? get dataOrNull => _data;

  /// Get failure (throws if success)
  Failure get failure {
    if (isSuccess) {
      throw Exception('Cannot access failure on success result');
    }
    return _failure!;
  }

  /// Get failure or null
  Failure? get failureOrNull => _failure;

  /// Fold result
  R fold<R>(
    R Function(Failure failure) onFailure,
    R Function(T data) onSuccess,
  ) {
    if (isFailure) {
      return onFailure(failure!);
    } else {
      return onSuccess(_data as T);
    }
  }

  /// Map success value
  Result<R> map<R>(R Function(T data) mapper) {
    if (isSuccess) {
      try {
        return Result.success(mapper(_data as T));
      } catch (e) {
        return Result.failure(
          SystemFailure('Mapping failed: ${e.toString()}'),
        );
      }
    } else {
      return Result.failure(_failure!);
    }
  }

  /// Map async success value
  Future<Result<R>> mapAsync<R>(Future<R> Function(T data) mapper) async {
    if (isSuccess) {
      try {
        final result = await mapper(_data as T);
        return Result.success(result);
      } catch (e) {
        return Result.failure(
          SystemFailure('Async mapping failed: ${e.toString()}'),
        );
      }
    } else {
      return Result.failure(_failure!);
    }
  }

  /// Chain with another result-returning function
  Result<R> flatMap<R>(Result<R> Function(T data) mapper) {
    if (isSuccess) {
      try {
        return mapper(_data as T);
      } catch (e) {
        return Result.failure(
          SystemFailure('Flat mapping failed: ${e.toString()}'),
        );
      }
    } else {
      return Result.failure(_failure!);
    }
  }

  /// Chain with another async result-returning function
  Future<Result<R>> flatMapAsync<R>(Future<Result<R>> Function(T data) mapper) async {
    if (isSuccess) {
      try {
        return await mapper(_data as T);
      } catch (e) {
        return Result.failure(
          SystemFailure('Async flat mapping failed: ${e.toString()}'),
        );
      }
    } else {
      return Result.failure(_failure!);
    }
  }

  @override
  List<Object?> get props => [_data, _failure];

  @override
  String toString() => isSuccess ? 'Success($_data)' : 'Failure($_failure)';
}
```

#### 1.2 Create Failure Classes
Create file: `lib/core/errors/failures.dart`:
```dart
import 'package:equatable/equatable.dart';

/// Base failure class
abstract class Failure extends Equatable {
  final String message;
  final String? code;
  final dynamic originalError;
  final StackTrace? stackTrace;

  const Failure({
    required this.message,
    this.code,
    this.originalError,
    this.stackTrace,
  });

  @override
  List<Object?> get props => [message, code, originalError];

  @override
  String toString() => 'Failure($code): $message';
}

/// Network-related failures
class NetworkFailure extends Failure {
  const NetworkFailure({
    required String message,
    String? code,
    dynamic originalError,
    StackTrace? stackTrace,
  }) : super(
          message: message,
          code: code ?? 'NETWORK_ERROR',
          originalError: originalError,
          stackTrace: stackTrace,
        );

  factory NetworkFailure.noConnection() {
    return const NetworkFailure(
      message: 'No internet connection',
      code: 'NO_CONNECTION',
    );
  }

  factory NetworkFailure.timeout() {
    return const NetworkFailure(
      message: 'Request timed out',
      code: 'TIMEOUT',
    );
  }

  factory NetworkFailure.serverError() {
    return const NetworkFailure(
      message: 'Server error occurred',
      code: 'SERVER_ERROR',
    );
  }
}

/// Validation failures
class ValidationFailure extends Failure {
  const ValidationFailure({
    required String message,
    String? code,
    dynamic originalError,
  }) : super(
          message: message,
          code: code ?? 'VALIDATION_ERROR',
          originalError: originalError,
        );

  factory ValidationFailure.required(String fieldName) {
    return ValidationFailure(
      message: '$fieldName is required',
      code: 'REQUIRED_FIELD',
    );
  }

  factory ValidationFailure.invalidFormat(String fieldName) {
    return ValidationFailure(
      message: '$fieldName has invalid format',
      code: 'INVALID_FORMAT',
    );
  }

  factory ValidationFailure.minLength(String fieldName, int minLength) {
    return ValidationFailure(
      message: '$fieldName must be at least $minLength characters',
      code: 'MIN_LENGTH',
    );
  }
}

/// Authentication failures
class AuthenticationFailure extends Failure {
  const AuthenticationFailure({
    required String message,
    String? code,
    dynamic originalError,
  }) : super(
          message: message,
          code: code ?? 'AUTH_ERROR',
          originalError: originalError,
        );

  factory AuthenticationFailure.invalidCredentials() {
    return const AuthenticationFailure(
      message: 'Invalid email or password',
      code: 'INVALID_CREDENTIALS',
    );
  }

  factory AuthenticationFailure.tokenExpired() {
    return const AuthenticationFailure(
      message: 'Authentication token has expired',
      code: 'TOKEN_EXPIRED',
    );
  }

  factory AuthenticationFailure.accessDenied() {
    return const AuthenticationFailure(
      message: 'Access denied',
      code: 'ACCESS_DENIED',
    );
  }
}

/// Database failures
class DatabaseFailure extends Failure {
  const DatabaseFailure({
    required String message,
    String? code,
    dynamic originalError,
    StackTrace? stackTrace,
  }) : super(
          message: message,
          code: code ?? 'DATABASE_ERROR',
          originalError: originalError,
          stackTrace: stackTrace,
        );

  factory DatabaseFailure.connectionFailed() {
    return const DatabaseFailure(
      message: 'Database connection failed',
      code: 'CONNECTION_FAILED',
    );
  }

  factory DatabaseFailure.queryFailed(String query) {
    return DatabaseFailure(
      message: 'Database query failed: $query',
      code: 'QUERY_FAILED',
    );
  }
}

/// System failures
class SystemFailure extends Failure {
  const SystemFailure({
    required String message,
    String? code,
    dynamic originalError,
    StackTrace? stackTrace,
  }) : super(
          message: message,
          code: code ?? 'SYSTEM_ERROR',
          originalError: originalError,
          stackTrace: stackTrace,
        );
}

/// Business logic failures
class BusinessFailure extends Failure {
  const BusinessFailure({
    required String message,
    String? code,
    dynamic originalError,
  }) : super(
          message: message,
          code: code ?? 'BUSINESS_ERROR',
          originalError: originalError,
        );

  factory BusinessFailure.insufficientBalance() {
    return const BusinessFailure(
      message: 'Insufficient balance',
      code: 'INSUFFICIENT_BALANCE',
    );
  }

  factory BusinessFailure.itemNotFound() {
    return const BusinessFailure(
      message: 'Item not found',
      code: 'ITEM_NOT_FOUND',
    );
  }

  factory BusinessFailure.duplicateItem() {
    return const BusinessFailure(
      message: 'Item already exists',
      code: 'DUPLICATE_ITEM',
    );
  }
}
```

#### 1.3 Create Error Handler Service
Create file: `lib/core/services/error_handler_service.dart`:
```dart
import 'package:get/get.dart';
import 'package:flutter/foundation.dart';

import '../errors/failures.dart';
import '../utils/result.dart';
import 'logger_service.dart';
import 'navigation_service.dart';

/// Service for handling errors throughout the application
class ErrorHandlerService extends GetxService {
  final LoggerService _logger = Get.find<LoggerService>();
  final NavigationService _navigationService = Get.find<NavigationService>();

  /// Handle result and show appropriate UI feedback
  void handleResult<T>(Result<T> result, {
    void Function(T data)? onSuccess,
    String? customSuccessMessage,
    bool showErrorDialog = false,
    bool showSnackBar = true,
  }) {
    result.fold(
      (failure) => _handleFailure(
        failure,
        showErrorDialog: showErrorDialog,
        showSnackBar: showSnackBar,
      ),
      (data) {
        if (onSuccess != null) {
          onSuccess(data);
        }
        if (customSuccessMessage != null) {
          _showSuccess(customSuccessMessage);
        }
      },
    );
  }

  /// Handle failure with appropriate UI feedback
  void _handleFailure(
    Failure failure, {
    bool showErrorDialog = false,
    bool showSnackBar = true,
  }) {
    // Log the error
    _logFailure(failure);

    // Show UI feedback
    if (showErrorDialog) {
      _showErrorDialog(failure);
    } else if (showSnackBar) {
      _showErrorSnackBar(failure);
    }

    // Handle specific failure types
    _handleSpecificFailure(failure);
  }

  /// Log failure to logger service
  void _logFailure(Failure failure) {
    switch (failure.runtimeType) {
      case NetworkFailure:
        _logger.error('Network failure: ${failure.message}', failure.originalError, failure.stackTrace);
        break;
      case AuthenticationFailure:
        _logger.warn('Authentication failure: ${failure.message}');
        break;
      case DatabaseFailure:
        _logger.error('Database failure: ${failure.message}', failure.originalError, failure.stackTrace);
        break;
      case SystemFailure:
        _logger.error('System failure: ${failure.message}', failure.originalError, failure.stackTrace);
        break;
      case ValidationFailure:
        _logger.info('Validation failure: ${failure.message}');
        break;
      case BusinessFailure:
        _logger.info('Business failure: ${failure.message}');
        break;
      default:
        _logger.error('Unknown failure: ${failure.message}', failure.originalError, failure.stackTrace);
    }
  }

  /// Show error dialog
  void _showErrorDialog(Failure failure) {
    _navigationService.showDialog(
      AlertDialog(
        title: Text(_getErrorTitle(failure)),
        content: Text(_getErrorMessage(failure)),
        actions: [
          TextButton(
            onPressed: () => _navigationService.goBack(),
            child: const Text('OK'),
          ),
          if (failure is AuthenticationFailure && failure.code == 'TOKEN_EXPIRED')
            TextButton(
              onPressed: () {
                _navigationService.goBack();
                _navigateToLogin();
              },
              child: const Text('Login'),
            ),
        ],
      ),
    );
  }

  /// Show error snackbar
  void _showErrorSnackBar(Failure failure) {
    _navigationService.showSnackbar(
      _getErrorTitle(failure),
      _getErrorMessage(failure),
    );
  }

  /// Show success message
  void _showSuccess(String message) {
    _navigationService.showSnackbar('Success', message);
  }

  /// Handle specific failure types with custom logic
  void _handleSpecificFailure(Failure failure) {
    switch (failure.runtimeType) {
      case AuthenticationFailure:
        final authFailure = failure as AuthenticationFailure;
        if (authFailure.code == 'TOKEN_EXPIRED') {
          _handleTokenExpired();
        }
        break;
      case NetworkFailure:
        final networkFailure = failure as NetworkFailure;
        if (networkFailure.code == 'NO_CONNECTION') {
          _handleNoConnection();
        }
        break;
    }
  }

  /// Handle expired authentication token
  void _handleTokenExpired() {
    // Clear user session
    // Get.find<AuthService>().logout();

    // Navigate to login after delay
    Future.delayed(const Duration(seconds: 2), () {
      _navigateToLogin();
    });
  }

  /// Handle no network connection
  void _handleNoConnection() {
    // Could implement offline mode or show specific UI
    _logger.info('Device is offline');
  }

  /// Navigate to login screen
  void _navigateToLogin() {
    _navigationService.navigateOffAll('/login');
  }

  /// Get user-friendly error title
  String _getErrorTitle(Failure failure) {
    switch (failure.runtimeType) {
      case NetworkFailure:
        return 'Network Error';
      case AuthenticationFailure:
        return 'Authentication Error';
      case ValidationFailure:
        return 'Validation Error';
      case DatabaseFailure:
        return 'Database Error';
      case SystemFailure:
        return 'System Error';
      case BusinessFailure:
        return 'Operation Failed';
      default:
        return 'Error';
    }
  }

  /// Get user-friendly error message
  String _getErrorMessage(Failure failure) {
    // In development, show detailed error
    if (kDebugMode && failure.originalError != null) {
      return '${failure.message}\n\nDetails: ${failure.originalError}';
    }

    // In production, show user-friendly message
    switch (failure.code) {
      case 'NO_CONNECTION':
        return 'Please check your internet connection and try again.';
      case 'TIMEOUT':
        return 'Request timed out. Please try again.';
      case 'INVALID_CREDENTIALS':
        return 'Invalid email or password. Please try again.';
      case 'TOKEN_EXPIRED':
        return 'Your session has expired. Please log in again.';
      case 'ACCESS_DENIED':
        return 'You don\'t have permission to perform this action.';
      case 'REQUIRED_FIELD':
        return failure.message;
      case 'INVALID_FORMAT':
        return failure.message;
      default:
        return failure.message;
    }
  }
}
```

### Phase 2: Error Handling in Different Layers

#### 2.1 Domain Layer Error Handling
```dart
// lib/features/user/domain/usecases/create_user.dart
import '../../../../core/utils/result.dart';
import '../../../../core/errors/failures.dart';
import '../repositories/user_repository.dart';

class CreateUserUseCase {
  final UserRepository _repository;

  CreateUserUseCase(this._repository);

  Future<Result<User>> execute(CreateUserParams params) async {
    // Input validation
    final validation = _validateInput(params);
    if (validation != null) {
      return Result.failure(validation);
    }

    try {
      // Check if user already exists
      final existingUser = await _repository.getUserByEmail(params.email);
      if (existingUser != null) {
        return Result.failure(
          BusinessFailure.duplicateItem(),
        );
      }

      // Create user
      final user = User(
        id: _generateId(),
        name: params.name,
        email: params.email,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      return await _repository.createUser(user);
    } catch (e) {
      return Result.failure(
        SystemFailure(
          message: 'Failed to create user',
          originalError: e,
        ),
      );
    }
  }

  ValidationFailure? _validateInput(CreateUserParams params) {
    if (params.name.trim().isEmpty) {
      return ValidationFailure.required('Name');
    }

    if (params.email.trim().isEmpty) {
      return ValidationFailure.required('Email');
    }

    if (!_isValidEmail(params.email)) {
      return ValidationFailure.invalidFormat('Email');
    }

    if (params.name.trim().length < 2) {
      return ValidationFailure.minLength('Name', 2);
    }

    return null;
  }

  bool _isValidEmail(String email) {
    final emailRegex = RegExp(r'^[^@]+@[^@]+\.[^@]+');
    return emailRegex.hasMatch(email);
  }

  String _generateId() {
    return DateTime.now().millisecondsSinceEpoch.toString();
  }
}

class CreateUserParams {
  final String name;
  final String email;

  CreateUserParams({
    required this.name,
    required this.email,
  });
}
```

#### 2.2 Data Layer Error Handling
```dart
// lib/features/user/data/repositories/user_repository_impl.dart
import '../../../../core/utils/result.dart';
import '../../../../core/errors/failures.dart';
import '../../domain/repositories/user_repository.dart';
import '../datasources/remote/user_remote_datasource.dart';
import '../datasources/local/user_local_datasource.dart';
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
  Future<Result<User>> createUser(User user) async {
    try {
      // Try remote first
      final remoteResult = await _remoteDataSource.createUser(_mapper.entityToModel(user));

      return remoteResult.fold(
        (failure) {
          // If remote fails, try local (offline mode)
          return _createUserLocally(user);
        },
        (userModel) {
          // Success: save to local cache
          _localDataSource.saveUser(userModel);
          return Result.success(_mapper.modelToEntity(userModel));
        },
      );
    } catch (e) {
      return Result.failure(
        SystemFailure(
          message: 'Failed to create user',
          originalError: e,
        ),
      );
    }
  }

  Future<Result<User>> _createUserLocally(User user) async {
    try {
      final userModel = _mapper.entityToModel(user);
      await _localDataSource.saveUser(userModel);
      return Result.success(user);
    } catch (e) {
      return Result.failure(
        DatabaseFailure(
          message: 'Failed to save user locally',
          originalError: e,
        ),
      );
    }
  }

  @override
  Future<Result<User>> getUser(String userId) async {
    try {
      // Try local first (offline-first)
      final localUser = await _localDataSource.getUser(userId);
      if (localUser != null) {
        return Result.success(_mapper.modelToEntity(localUser));
      }

      // Fallback to remote
      final remoteResult = await _remoteDataSource.getUser(userId);

      return remoteResult.fold(
        (failure) => Result.failure(failure),
        (userModel) {
          // Cache locally
          _localDataSource.saveUser(userModel);
          return Result.success(_mapper.modelToEntity(userModel));
        },
      );
    } catch (e) {
      return Result.failure(
        SystemFailure(
          message: 'Failed to get user',
          originalError: e,
        ),
      );
    }
  }
}
```

#### 2.3 Presentation Layer Error Handling
```dart
// lib/features/user/presentation/controllers/user_controller.dart
import 'package:get/get.dart';
import '../../../../core/utils/result.dart';
import '../../../../core/errors/failures.dart';
import '../../../../core/services/error_handler_service.dart';
import '../../domain/usecases/create_user.dart';
import '../../domain/entities/user.dart';

class UserController extends GetxController {
  final CreateUserUseCase _createUserUseCase;
  final ErrorHandlerService _errorHandler;

  // Reactive state
  final _isLoading = false.obs;
  final _error = Rx<Failure?>(null);
  final _user = Rx<User?>(null);

  // Getters
  bool get isLoading => _isLoading.value;
  Failure? get error => _error.value;
  User? get user => _user.value;

  UserController({
    required CreateUserUseCase createUserUseCase,
    required ErrorHandlerService errorHandler,
  })  : _createUserUseCase = createUserUseCase,
        _errorHandler = errorHandler;

  Future<void> createUser({
    required String name,
    required String email,
  }) async {
    _setLoading(true);
    _clearError();

    final params = CreateUserParams(name: name, email: email);
    final result = await _createUserUseCase.execute(params);

    result.fold(
      (failure) => _handleFailure(failure),
      (user) => _handleSuccess(user),
    );

    _setLoading(false);
  }

  void _handleFailure(Failure failure) {
    _error.value = failure;
    _errorHandler.handleResult(Result.failure(failure));
  }

  void _handleSuccess(User user) {
    _user.value = user;
    _errorHandler.handleResult(
      Result.success(user),
      customSuccessMessage: 'User created successfully',
    );
    Get.back(); // Navigate back
  }

  void _setLoading(bool loading) {
    _isLoading.value = loading;
  }

  void _clearError() {
    _error.value = null;
  }

  void retryCreateUser({
    required String name,
    required String email,
  }) {
    createUser(name: name, email: email);
  }
}
```

### Phase 3: API Error Handling

#### 3.1 Create API Error Handler
Create file: `lib/core/data/api_error_handler.dart`:
```dart
import 'package:dio/dio.dart';

import '../errors/failures.dart';
import '../utils/result.dart';

class ApiErrorHandler {
  static Result<T> handleDioError<T>(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return Result.failure(NetworkFailure.timeout());

      case DioExceptionType.badResponse:
        return _handleHttpError<T>(error.response!);

      case DioExceptionType.cancel:
        return Result.failure(
          NetworkFailure(
            message: 'Request was cancelled',
            code: 'CANCELLED',
          ),
        );

      case DioExceptionType.connectionError:
        return Result.failure(NetworkFailure.noConnection());

      case DioExceptionType.unknown:
        return Result.failure(
          NetworkFailure(
            message: 'Unknown network error occurred',
            originalError: error,
          ),
        );

      default:
        return Result.failure(
          NetworkFailure(
            message: 'Unexpected network error',
            originalError: error,
          ),
        );
    }
  }

  static Result<T> _handleHttpError<T>(Response response) {
    final statusCode = response.statusCode;
    final data = response.data;

    // Extract error message from response
    String? message;
    String? code;

    if (data is Map<String, dynamic>) {
      message = data['message'] as String?;
      code = data['code'] as String?;
    } else if (data is String) {
      message = data;
    }

    // Default messages
    message ??= _getDefaultMessageForStatus(statusCode);

    switch (statusCode) {
      case 400:
        return Result.failure(
          ValidationFailure(
            message: message,
            code: code ?? 'BAD_REQUEST',
          ),
        );

      case 401:
        if (code == 'TOKEN_EXPIRED') {
          return Result.failure(AuthenticationFailure.tokenExpired());
        } else {
          return Result.failure(AuthenticationFailure.invalidCredentials());
        }

      case 403:
        return Result.failure(AuthenticationFailure.accessDenied());

      case 404:
        return Result.failure(
          BusinessFailure(
            message: message,
            code: code ?? 'NOT_FOUND',
          ),
        );

      case 409:
        return Result.failure(
          BusinessFailure(
            message: message,
            code: code ?? 'CONFLICT',
          ),
        );

      case 422:
        return Result.failure(
          ValidationFailure(
            message: message,
            code: code ?? 'VALIDATION_FAILED',
          ),
        );

      case 429:
        return Result.failure(
          NetworkFailure(
            message: 'Too many requests. Please try again later.',
            code: 'RATE_LIMITED',
          ),
        );

      case 500:
      case 502:
      case 503:
      case 504:
        return Result.failure(NetworkFailure.serverError());

      default:
        return Result.failure(
          NetworkFailure(
            message: message,
            code: code ?? 'HTTP_ERROR_$statusCode',
          ),
        );
    }
  }

  static String _getDefaultMessageForStatus(int statusCode) {
    switch (statusCode) {
      case 400:
        return 'Bad request';
      case 401:
        return 'Unauthorized';
      case 403:
        return 'Forbidden';
      case 404:
        return 'Not found';
      case 409:
        return 'Conflict';
      case 422:
        return 'Validation failed';
      case 429:
        return 'Too many requests';
      case 500:
        return 'Internal server error';
      case 502:
        return 'Bad gateway';
      case 503:
        return 'Service unavailable';
      case 504:
        return 'Gateway timeout';
      default:
        return 'Request failed with status $statusCode';
    }
  }
}
```

#### 3.2 Create Safe API Client
Create file: `lib/core/data/safe_api_client.dart`:
```dart
import 'package:dio/dio.dart';

import '../errors/failures.dart';
import '../utils/result.dart';
import 'api_error_handler.dart';

class SafeApiClient {
  final Dio _dio;

  SafeApiClient(this._dio);

  Future<Result<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      final response = await _dio.get<T>(
        path,
        queryParameters: queryParameters,
        options: options,
      );
      return Result.success(response.data!);
    } on DioException catch (e) {
      return ApiErrorHandler.handleDioError<T>(e);
    } catch (e) {
      return Result.failure(
        SystemFailure(
          message: 'Unexpected error during GET request',
          originalError: e,
        ),
      );
    }
  }

  Future<Result<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      final response = await _dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
      return Result.success(response.data!);
    } on DioException catch (e) {
      return ApiErrorHandler.handleDioError<T>(e);
    } catch (e) {
      return Result.failure(
        SystemFailure(
          message: 'Unexpected error during POST request',
          originalError: e,
        ),
      );
    }
  }

  Future<Result<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      final response = await _dio.put<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
      return Result.success(response.data!);
    } on DioException catch (e) {
      return ApiErrorHandler.handleDioError<T>(e);
    } catch (e) {
      return Result.failure(
        SystemFailure(
          message: 'Unexpected error during PUT request',
          originalError: e,
        ),
      );
    }
  }

  Future<Result<T>> delete<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      final response = await _dio.delete<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
      return Result.success(response.data!);
    } on DioException catch (e) {
      return ApiErrorHandler.handleDioError<T>(e);
    } catch (e) {
      return Result.failure(
        SystemFailure(
          message: 'Unexpected error during DELETE request',
          originalError: e,
        ),
      );
    }
  }
}
```

### Phase 4: Testing Error Handling

#### 4.1 Test Result Pattern
```dart
// test/core/utils/result_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:your_app/core/utils/result.dart';
import 'package:your_app/core/errors/failures.dart';

void main() {
  group('Result', () {
    test('should create success result', () {
      final result = Result.success('test data');

      expect(result.isSuccess, true);
      expect(result.isFailure, false);
      expect(result.data, 'test data');
    });

    test('should create failure result', () {
      final failure = NetworkFailure('test error');
      final result = Result.failure(failure);

      expect(result.isSuccess, false);
      expect(result.isFailure, true);
      expect(result.failure, failure);
    });

    test('should map success result', () {
      final result = Result.success(5);
      final mapped = result.map((data) => data * 2);

      expect(mapped.isSuccess, true);
      expect(mapped.data, 10);
    });

    test('should handle error in map', () {
      final result = Result.success('test');
      final mapped = result.map((data) => throw Exception('Mapping failed'));

      expect(mapped.isFailure, true);
      expect(mapped.failure, isA<SystemFailure>());
    });

    test('should fold result correctly', () {
      final successResult = Result.success('success');
      final failureResult = Result.failure(NetworkFailure('error'));

      final successFolded = successResult.fold(
        (failure) => 'error: ${failure.message}',
        (data) => 'success: $data',
      );

      final failureFolded = failureResult.fold(
        (failure) => 'error: ${failure.message}',
        (data) => 'success: $data',
      );

      expect(successFolded, 'success: success');
      expect(failureFolded, 'error: error');
    });
  });
}
```

#### 4.2 Test Controller Error Handling
```dart
// test/features/user/presentation/controllers/user_controller_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:your_app/core/errors/failures.dart';
import 'package:your_app/core/utils/result.dart';
import 'package:your_app/features/user/presentation/controllers/user_controller.dart';
import 'package:your_app/features/user/domain/usecases/create_user.dart';

class MockCreateUserUseCase extends Mock implements CreateUserUseCase {}
class MockErrorHandlerService extends Mock implements ErrorHandlerService {}

void main() {
  late UserController controller;
  late MockCreateUserUseCase mockCreateUserUseCase;
  late MockErrorHandlerService mockErrorHandlerService;

  setUp(() {
    mockCreateUserUseCase = MockCreateUserUseCase();
    mockErrorHandlerService = MockErrorHandlerService();
    controller = UserController(
      createUserUseCase: mockCreateUserUseCase,
      errorHandler: mockErrorHandlerService,
    );
  });

  test('should handle successful user creation', () async {
    // Arrange
    const name = 'John Doe';
    const email = 'john@example.com';
    const user = User(
      id: '1',
      name: name,
      email: email,
      createdAt: null,
      updatedAt: null,
    );

    when(mockCreateUserUseCase.execute(any))
        .thenAnswer((_) async => Result.success(user));

    // Act
    await controller.createUser(name: name, email: email);

    // Assert
    expect(controller.user, user);
    expect(controller.error, null);
    verify(mockErrorHandlerService.handleResult(any)).called(1);
  });

  test('should handle validation error', () async {
    // Arrange
    const name = '';
    const email = 'invalid-email';

    when(mockCreateUserUseCase.execute(any))
        .thenAnswer((_) async => Result.failure(ValidationFailure.required('Name')));

    // Act
    await controller.createUser(name: name, email: email);

    // Assert
    expect(controller.user, null);
    expect(controller.error, isA<ValidationFailure>());
    verify(mockErrorHandlerService.handleResult(any)).called(1);
  });

  test('should handle network error', () async {
    // Arrange
    const name = 'John Doe';
    const email = 'john@example.com';

    when(mockCreateUserUseCase.execute(any))
        .thenAnswer((_) async => Result.failure(NetworkFailure.noConnection()));

    // Act
    await controller.createUser(name: name, email: email);

    // Assert
    expect(controller.user, null);
    expect(controller.error, isA<NetworkFailure>());
    verify(mockErrorHandlerService.handleResult(any)).called(1);
  });
}
```

## Verification Checklist

### Implementation
- [ ] Result pattern implemented correctly
- [ ] All failure types created
- [ ] Error handler service implemented
- [ ] API error handling in place
- [ ] UI feedback mechanisms working

### Testing
- [ ] Result pattern tested
- [ ] Error handling tested in each layer
- [ ] Controller error handling tested
- [ ] API error scenarios tested
- [ ] User feedback tested

### User Experience
- [ ] Error messages are user-friendly
- [ ] Loading states shown during operations
- [ ] Success feedback provided
- [ ] Recovery options available
- [ ] Consistent error presentation

## Best Practices

1. **Always use Result pattern for operations that can fail**
2. **Handle errors at each layer appropriately**
3. **Provide user-friendly error messages**
4. **Log errors for debugging**
5. **Test both success and failure scenarios**
6. **Don't expose internal errors to users**
7. **Provide recovery mechanisms when possible**
8. **Be consistent in error handling approach**

## Common Issues and Solutions

### Issue: Unhandled exceptions
**Solution**: Ensure all async operations are wrapped in try-catch blocks and return Results.

### Issue: Generic error messages
**Solution**: Create specific failure types and provide detailed, contextual error messages.

### Issue: No user feedback
**Solution**: Always provide UI feedback for both success and failure scenarios.

### Issue: Error information lost
**Solution**: Include original error and stack trace in failure objects for debugging.

## Resources

- [Result Pattern in Dart](https://pub.dev/packages/dartz)
- [Error Handling Best Practices](https://dart.dev/guides/language/error-handling)
- [GetX State Management](https://pub.dev/packages/get)