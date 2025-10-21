# Flutter GetX Clean Architecture - Reference Documentation

## Table of Contents
1. [Core Components](#core-components)
2. [API Integration](#api-integration)
3. [Database with Drift](#database-with-drift)
4. [Form Handling](#form-handling)
5. [Local Storage](#local-storage)
6. [Advanced State Management](#advanced-state-management)
7. [Testing Guidelines](#testing-guidelines)
8. [Performance Optimization](#performance-optimization)

---

## Core Components

### Base Controller (Full Implementation)

```dart
import 'package:get/get.dart';
import 'package:dartz/dartz.dart';

abstract class BaseController extends GetxController {
  final RxBool _isLoading = false.obs;
  final RxString _errorMessage = ''.obs;
  final RxBool _isEmpty = false.obs;

  bool get isLoading => _isLoading.value;
  String get errorMessage => _errorMessage.value;
  bool get isEmpty => _isEmpty.value;
  bool get hasError => _errorMessage.value.isNotEmpty;

  void setLoading(bool value) => _isLoading.value = value;
  void setError(String message) => _errorMessage.value = message;
  void setEmpty(bool value) => _isEmpty.value = value;
  void clearError() => _errorMessage.value = '';

  @override
  void onInit() {
    super.onInit();
    initController();
  }

  void initController();

  @override
  void onClose() {
    disposeController();
    super.onClose();
  }

  void disposeController() {}

  /// Helper method for handling use case results
  Future<T?> handleUseCaseResult<T>({
    required Future<Either<Failure, T>> Function() execute,
    required Function(T data) onSuccess,
    Function(Failure failure)? onFailure,
  }) async {
    setLoading(true);
    clearError();

    final result = await execute();

    result.fold(
      (failure) {
        setError(failure.message);
        onFailure?.call(failure);
      },
      (data) {
        onSuccess(data);
      },
    );

    setLoading(false);
    return result.fold((_) => null, (data) => data);
  }
}
```

### Base Use Case

```dart
import 'package:dartz/dartz.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

abstract class StreamUseCase<Type, Params> {
  Stream<Either<Failure, Type>> call(Params params);
}

class NoParams {
  const NoParams();
}

// Failures
abstract class Failure {
  final String message;
  final int? code;
  const Failure(this.message, [this.code]);
}

class ServerFailure extends Failure {
  const ServerFailure([super.message = 'Server error occurred', super.code]);
}

class CacheFailure extends Failure {
  const CacheFailure([super.message = 'Cache error occurred', super.code]);
}

class NetworkFailure extends Failure {
  const NetworkFailure([super.message = 'No internet connection', super.code]);
}

// Exceptions
class ServerException implements Exception {
  final String message;
  final int? statusCode;
  const ServerException(this.message, [this.statusCode]);
}

class CacheException implements Exception {
  final String message;
  const CacheException(this.message);
}

class NetworkException implements Exception {
  final String message;
  const NetworkException(this.message);
}
```

### Base Repository

```dart
import 'package:dartz/dartz.dart';

abstract class BaseRepository {
  Future<Either<Failure, T>> safeCall<T>(
    Future<T> Function() call, {
    String? errorMessage,
  }) async {
    try {
      final result = await call();
      return Right(result);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message, e.statusCode));
    } on CacheException catch (e) {
      return Left(CacheFailure(e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(e.message));
    } catch (e) {
      return Left(ServerFailure(errorMessage ?? e.toString()));
    }
  }
}
```

---

## API Integration

### Dio Service Setup

```dart
import 'package:dio/dio.dart';
import 'package:get/get.dart' as getx;

class DioService extends getx.GetxService {
  late Dio _dio;
  Dio get dio => _dio;

  @override
  void onInit() {
    super.onInit();
    _initializeDio();
  }

  void _initializeDio() {
    _dio = Dio(BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
    ));

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        final token = getx.Get.find<AuthController>().token;
        if (token.isNotEmpty) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
    ));
  }
}
```

### Remote Data Source

```dart
abstract class UserRemoteDataSource {
  Future<UserModel> getUser(String id);
  Future<List<UserModel>> getUsers();
}

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final Dio dio;
  UserRemoteDataSourceImpl({required this.dio});

  @override
  Future<List<UserModel>> getUsers() async {
    try {
      final response = await dio.get('/users');
      final List<dynamic> data = response.data['data'];
      return data.map((json) => UserModel.fromJson(json)).toList();
    } on DioException catch (e) {
      throw ServerException(e.message ?? 'Server error');
    }
  }
}
```

---

## Database with Drift

### Database Setup

```dart
import 'package:drift/drift.dart';
import 'package:drift_flutter/drift_flutter.dart';

class Users extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get name => text()();
  TextColumn get email => text().unique()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

@DriftDatabase(tables: [Users])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  static QueryExecutor _openConnection() {
    return driftDatabase(name: 'app_database');
  }
}
```

### Local Data Source

```dart
abstract class UserLocalDataSource {
  Future<List<UserModel>> getCachedUsers();
  Future<void> cacheUsers(List<UserModel> users);
}

class UserLocalDataSourceImpl implements UserLocalDataSource {
  final AppDatabase database;
  UserLocalDataSourceImpl({required this.database});

  @override
  Future<List<UserModel>> getCachedUsers() async {
    final users = await database.select(database.users).get();
    return users.map((u) => UserModel.fromDrift(u)).toList();
  }

  @override
  Future<void> cacheUsers(List<UserModel> users) async {
    await database.batch((batch) {
      batch.insertAll(
        database.users,
        users.map((u) => u.toDriftCompanion()).toList(),
        mode: InsertMode.insertOrReplace,
      );
    });
  }
}
```

---

## Form Handling

### Form Controller

```dart
class LoginController extends BaseController {
  final formKey = GlobalKey<FormState>();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  String? validateEmail(String? value) {
    if (value == null || value.isEmpty) return 'Email is required';
    if (!GetUtils.isEmail(value)) return 'Invalid email';
    return null;
  }

  Future<void> login() async {
    if (!(formKey.currentState?.validate() ?? false)) return;

    await handleUseCaseResult(
      execute: () => loginUseCase(LoginParams(
        email: emailController.text.trim(),
        password: passwordController.text,
      )),
      onSuccess: (authResponse) {
        Get.find<AuthService>().setAuthToken(authResponse.token);
        Get.offAllNamed(Routes.HOME);
      },
    );
  }

  @override
  void disposeController() {
    emailController.dispose();
    passwordController.dispose();
  }
}
```

---

## Testing

### Unit Testing

```dart
@GenerateMocks([GetUsersUseCase])
void main() {
  late UserController controller;
  late MockGetUsersUseCase mockUseCase;

  setUp(() {
    Get.testMode = true;
    mockUseCase = MockGetUsersUseCase();
    controller = UserController(getUsersUseCase: mockUseCase);
  });

  tearDown(() => Get.reset());

  test('should load users successfully', () async {
    final testUsers = [User(id: '1', name: 'John')];
    when(mockUseCase(any)).thenAnswer((_) async => Right(testUsers));

    await controller.loadUsers();

    expect(controller.users.length, 1);
    expect(controller.isLoading, false);
  });
}
```

---

For more detailed examples and complete implementations, see `examples.md`.
