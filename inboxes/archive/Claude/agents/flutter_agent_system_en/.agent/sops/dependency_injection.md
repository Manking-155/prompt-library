# SOP: Dependency Injection Setup with GetIt + Injectable

## Overview
This document describes how to set up and manage dependency injection using GetIt service locator and Injectable code generation.

## Setup

### Prerequisites
- GetIt package installed
- Injectable package installed
- Build runner configured

### Add Dependencies to pubspec.yaml
```yaml
dependencies:
  get_it: ^7.4.0
  injectable: ^2.1.0

dev_dependencies:
  build_runner: ^2.4.0
  injectable_generator: ^2.1.0
```

### Create DI Configuration

File: `lib/core/di/injectable_config.dart`

```dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';

final getIt = GetIt.instance;

@injectableInit
void configureDependencies() => getIt.init();
```

### Generate Configuration
```bash
flutter pub run build_runner build
```

This generates `lib/core/di/injectable_config.config.dart`.

## Registration Strategies

### Strategy 1: LazySingleton

Register once, instantiate on first access.

```dart
@lazySingleton
class DatabaseService {
  DatabaseService();
  
  Future<void> initialize() async {
    // Initialize database
  }
}

// Generated code will call once per app lifetime
final db = getIt<DatabaseService>();
```

**Use for:**
- Heavy initialization costs
- Services used once or infrequently
- Database connections
- Shared preferences

### Strategy 2: Singleton

Register once, reuse same instance.

```dart
@singleton
class AppSettings {
  String? theme;
  
  AppSettings();
}

// Same instance accessed everywhere
final settings1 = getIt<AppSettings>();
final settings2 = getIt<AppSettings>();
// settings1 == settings2  // true
```

**Use for:**
- Stateful services
- Caching layers
- Configuration managers

### Strategy 3: Factory

Create new instance on each access.

```dart
@factoryMethod
Future<ApiClient> provideApiClient() async {
  final dio = Dio();
  return ApiClient(dio);
}

// New instance each time
final client1 = getIt<ApiClient>();
final client2 = getIt<ApiClient>();
// client1 != client2  // true
```

**Use for:**
- Stateless utilities
- Short-lived objects
- Objects with state isolation

### Strategy 4: Named Registration

Register multiple implementations of same interface.

```dart
abstract class Logger {
  void log(String message);
}

@singleton
class ConsoleLogger implements Logger {
  @override
  void log(String message) => print(message);
}

@singleton
class FileLogger implements Logger {
  @override
  void log(String message) => _writeToFile(message);
}

// Register with names
void configureDependencies() {
  getIt.registerSingleton<Logger>(ConsoleLogger(), instanceName: 'console');
  getIt.registerSingleton<Logger>(FileLogger(), instanceName: 'file');
}

// Access by name
final consoleLogger = getIt<Logger>(instanceName: 'console');
final fileLogger = getIt<Logger>(instanceName: 'file');
```

## Common Setup Patterns

### Service Layer Setup

```dart
// Datasources
@lazySingleton
class UserLocalDatasource {
  final DatabaseService db;
  UserLocalDatasource(this.db);
}

@lazySingleton
class UserRemoteDatasource {
  final Dio dio;
  UserRemoteDatasource(this.dio);
}

// Repositories
@lazySingleton
class UserRepositoryImpl implements UserRepository {
  final UserLocalDatasource local;
  final UserRemoteDatasource remote;
  
  UserRepositoryImpl(this.local, this.remote);
}

// Usecases
@lazySingleton
class GetUserUsecase {
  final UserRepository repository;
  GetUserUsecase(this.repository);
}

// Controllers
@lazySingleton
class UserController extends GetxController {
  final GetUserUsecase getUser;
  UserController(this.getUser);
}
```

### Database Setup

```dart
@lazySingleton
Future<AppDatabase> provideDatabase() async {
  final database = AppDatabase();
  // Initialize database
  await database.customStatement('PRAGMA journal_mode=WAL');
  return database;
}

// Also register service
@lazySingleton
class DatabaseService {
  final AppDatabase database;
  DatabaseService(this.database);
  
  Future<List<User>> getUsers() async {
    return database.select(database.users).get();
  }
}
```

### API Client Setup

```dart
@lazySingleton
Dio provideDio() {
  final dio = Dio();
  
  dio.options.baseUrl = 'https://api.example.com';
  dio.options.connectTimeout = const Duration(seconds: 30);
  dio.options.receiveTimeout = const Duration(seconds: 30);
  
  dio.interceptors.add(
    InterceptorsWrapper(
      onRequest: (options, handler) {
        // Add auth token
        final token = getIt<AuthService>().token;
        options.headers['Authorization'] = 'Bearer $token';
        return handler.next(options);
      },
    ),
  );
  
  return dio;
}

@lazySingleton
class ApiClient {
  final Dio dio;
  ApiClient(this.dio);
}
```

### Auth Service Setup

```dart
@singleton
class AuthService {
  String? _token;
  final TokenStorage storage;
  
  AuthService(this.storage);
  
  @override
  void onInit() {
    _loadToken();
    super.onInit();
  }
  
  Future<void> _loadToken() async {
    _token = await storage.getToken();
  }
  
  String? get token => _token;
  
  Future<void> setToken(String token) async {
    _token = token;
    await storage.saveToken(token);
  }
  
  Future<void> logout() async {
    _token = null;
    await storage.deleteToken();
  }
}
```

## Initialization in main.dart

```dart
import 'core/di/injectable_config.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize DI
  configureDependencies();
  
  // Initialize core services
  await getIt<DatabaseService>().initialize();
  await getIt<AuthService>().loadToken();
  
  runApp(const MyApp());
}
```

## Module-Based Registration

Register dependencies per feature module:

```dart
// features/user/lib/di/user_di.dart
void setupUserDependencies() {
  // Datasources
  getIt.registerLazySingleton<UserLocalDatasource>(
    () => UserLocalDatasourceImpl(getIt()),
  );
  
  getIt.registerLazySingleton<UserRemoteDatasource>(
    () => UserRemoteDatasourceImpl(getIt()),
  );
  
  // Repository
  getIt.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(getIt(), getIt()),
  );
  
  // Usecases
  getIt.registerLazySingleton(() => GetUserUsecase(getIt()));
  
  // Controller
  getIt.registerLazySingleton(() => UserController(getIt()));
}
```

In main.dart:
```dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  configureDependencies();
  setupUserDependencies();
  setupFlashcardDependencies();
  
  runApp(const MyApp());
}
```

## GetX Binding Integration

While GetIt is for global DI, GetX Bindings are for page-specific DI:

```dart
// Use GetX Bindings for page-specific controllers
class UserBinding extends Bindings {
  @override
  void dependencies() {
    // Use GetIt for shared services
    Get.lazyPut(() => GetUserUsecase(getIt()));
    
    // Register page-specific controller
    Get.lazyPut(() => UserController(Get.find()));
  }
}

// In routes
GetPage(
  name: '/user',
  page: () => const UserPage(),
  binding: UserBinding(),
)
```

## Advanced Patterns

### Conditional Registration Based on Environment

```dart
@pragma('vm:entry-point')
void setupServiceLocator(Environment env) {
  if (env == Environment.production) {
    getIt.registerSingleton<Logger>(ProductionLogger());
  } else {
    getIt.registerSingleton<Logger>(DebugLogger());
  }
}

enum Environment { production, staging, development }
```

### Reset for Testing

```dart
Future<void> setupTestDependencies() async {
  // Reset GetIt
  await getIt.reset();
  
  // Register test mocks
  getIt.registerSingleton<MockUserRepository>(MockUserRepository());
  getIt.registerSingleton<MockDatabaseService>(MockDatabaseService());
}
```

## Accessing Dependencies

### Method 1: Direct Access
```dart
final userService = getIt<UserService>();
```

### Method 2: In GetX Controller
```dart
class MyController extends GetxController {
  late final UserService userService;
  
  @override
  void onInit() {
    userService = Get.find();
    super.onInit();
  }
}
```

### Method 3: Constructor Injection (Recommended)
```dart
class UserController extends GetxController {
  final UserService userService;
  
  UserController(this.userService);
}

// Automatically injected via binding
class UserBinding extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => UserController(getIt()));
  }
}
```

## Troubleshooting

### "Could not find type in registry"
```dart
// Ensure registration is called before access
void main() async {
  configureDependencies();  // Must be called first
  // Now safe to access
  final service = getIt<MyService>();
}
```

### Circular Dependencies
```dart
// Use lazy registration to break cycles
@lazySingleton
class ServiceA {
  late ServiceB serviceB;
  
  @override
  void onInit() {
    serviceB = getIt<ServiceB>();  // Resolve on first use
    super.onInit();
  }
}
```

### Need to Clear and Rebuild
```bash
flutter pub run build_runner clean
flutter pub run build_runner build
```

## Best Practices

1. **Use LazySingleton for most services**: Efficient initialization
2. **Constructor injection**: Prefer over Get.find() in tests
3. **Register in order**: Core services first, then features
4. **Name instances**: Use `instanceName` for multiple implementations
5. **Abstract interfaces**: Register as interface type
6. **Module separation**: Keep feature DI modular
7. **Test setup**: Create separate test DI configuration
8. **Environment aware**: Register different implementations per environment

## Related Documentation
- Adding New Feature: `sops/adding_new_feature.md`
- Clean Architecture Guide: `system/clean_architecture_guide.md`
- Code Standards: `system/code_standards.md`
