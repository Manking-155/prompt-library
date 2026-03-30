# SOP: Dependency Injection with GetIt and Injectable

## Overview

This Standard Operating Procedure (SOP) outlines the process for setting up and managing dependency injection (DI) in our Flutter application using GetIt and Injectable packages.

## Prerequisites

- Flutter SDK installed
- GetIt and Injectable packages configured
- Understanding of dependency injection concepts
- Knowledge of Clean Architecture layers

## Key Concepts

### Dependency Injection Types
- **Constructor Injection**: Dependencies passed through constructor
- **Method Injection**: Dependencies passed through method parameters
- **Property Injection**: Dependencies set as properties

### Service Lifetimes
- **Singleton**: One instance for entire application lifetime
- **Lazy Singleton**: Created when first accessed
- **Factory**: New instance every time
- **Transient**: Disposed when no longer in use

## Step-by-Step Process

### Phase 1: Initial Setup

#### 1.1 Add Dependencies
Add to `pubspec.yaml`:
```yaml
dependencies:
  get_it: ^7.2.0
  injectable: ^1.5.3

dev_dependencies:
  injectable_generator: ^1.5.4
  build_runner: ^2.3.0
```

#### 1.2 Create DI Configuration Structure
```bash
lib/
├── core/
│   ├── di/
│   │   ├── injection_config.dart      # Main DI configuration
│   │   ├── injection_module.dart      # Core services module
│   │   └── injection_resolver.dart    # GetIt instance
```

### Phase 2: Setting Up Core DI Infrastructure

#### 2.1 Create Injection Resolver
Create file: `lib/core/di/injection_resolver.dart`:
```dart
import 'package:get_it/get_it.dart';

/// Global GetIt instance
final GetIt getIt = GetIt.instance;

/// Extension for easier access
extension GetItExtension on GetIt {
  /// Get service of type [T]
  T get<T extends Object>() => getIt<T>();

  /// Get service of type [T] or null
  T? getOrNull<T extends Object>() {
    try {
      return getIt<T>();
    } catch (e) {
      return null;
    }
  }

  /// Check if service is registered
  bool isRegistered<T extends Object>() {
    return getIt.isRegistered<T>();
  }
}
```

#### 2.2 Create Base Module Interface
Create file: `lib/core/di/base_module.dart`:
```dart
import 'package:injectable/injectable.dart';

/// Base interface for DI modules
abstract class BaseModule {
  /// Configure dependencies for this module
  void configureDependencies();
}

/// Abstract module for feature dependencies
@module
abstract class FeatureModule {
  /// Called when module is initialized
  @postConstruct
  void onInit() {
    // Module initialization logic
  }

  /// Called when module is disposed
  @preDestroy
  void onDispose() {
    // Module cleanup logic
  }
}
```

#### 2.3 Create Main DI Configuration
Create file: `lib/core/di/injection_config.dart`:
```dart
import 'package:injectable/injectable.dart';
import 'injection_resolver.dart';

/// Configure dependency injection
@injectableInit
Future<void> configureDependencies() async {
  getIt.init();
}

/// Configure dependencies for a specific environment
Future<void> configureDependenciesForEnvironment(String environment) async {
  await configureDependencies();

  // Environment-specific configurations
  switch (environment) {
    case 'development':
      await _configureDevelopmentDependencies();
      break;
    case 'production':
      await _configureProductionDependencies();
      break;
    case 'testing':
      await _configureTestingDependencies();
      break;
  }
}

Future<void> _configureDevelopmentDependencies() async {
  // Development-specific services
  // getIt.registerSingleton<Logger>(DevelopmentLogger());
}

Future<void> _configureProductionDependencies() async {
  // Production-specific services
  // getIt.registerSingleton<Logger>(ProductionLogger());
}

Future<void> _configureTestingDependencies() async {
  // Testing-specific services
  // getIt.registerSingleton<ApiService>(MockApiService());
}
```

### Phase 3: Registering Core Services

#### 3.1 Create Core Services Module
Create file: `lib/core/di/injection_module.dart`:
```dart
import 'package:injectable/injectable.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:dio/dio.dart';
import 'package:sqflite/sqflite.dart';

import '../services/navigation_service.dart';
import '../services/storage_service.dart';
import '../services/api_service.dart';
import '../services/database_service.dart';
import '../services/logger_service.dart';

/// Core services dependency injection module
@module
abstract class CoreModule {
  // Singletons - Created once and live forever

  @singleton
  SharedPreferences get sharedPreferences =>
      throw UnimplementedError('SharedPreferences must be provided at runtime');

  @singleton
  Dio get dio => Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));

  @singleton
  NavigationService get navigationService => NavigationServiceImpl();

  @singleton
  LoggerService get loggerService => LoggerServiceImpl();

  @singleton(preResolve: true)
  Future<StorageService> get storageService async {
    final prefs = await SharedPreferences.getInstance();
    return StorageServiceImpl(prefs);
  }

  @singleton(preResolve: true)
  Future<DatabaseService> get databaseService async {
    return DatabaseServiceImpl();
  }

  @lazySingleton
  ApiService get apiService => ApiServiceImpl(getIt<Dio>(), getIt<LoggerService>());

  // Factories - New instance every time

  @factory
  HttpClient get httpClient => HttpClientImpl(getIt<Dio>());

  // Register with dependencies

  @injectable
  UserService get userService => UserServiceImpl(
    apiService: getIt<ApiService>(),
    storageService: getIt<StorageService>(),
    loggerService: getIt<LoggerService>(),
  );
}
```

#### 3.2 Create Service Interfaces
Create file: `lib/core/services/navigation_service.dart`:
```dart
import 'package:get/get.dart';

/// Abstract navigation service
abstract class NavigationService {
  /// Navigate to a route
  Future<T?>? navigateTo<T>(String routeName, {Object? arguments});

  /// Navigate back
  void goBack<T>([T? result]);

  /// Navigate to a route and clear all previous routes
  Future<T?>? navigateOffAll<T>(String routeName, {Object? arguments});

  /// Navigate to a route and replace current
  Future<T?>? navigateOff<T>(String routeName, {Object? arguments});

  /// Show dialog
  Future<T?> showDialog<T>(Widget dialog);

  /// Show bottom sheet
  Future<T?> showBottomSheet<T>(Widget bottomSheet);

  /// Show snackbar
  void showSnackbar(String title, String message, {Duration? duration});
}

/// Implementation of NavigationService using GetX
class NavigationServiceImpl implements NavigationService {
  @override
  Future<T?>? navigateTo<T>(String routeName, {Object? arguments}) {
    return Get.toNamed<T>(routeName, arguments: arguments);
  }

  @override
  void goBack<T>([T? result]) {
    Get.back<T>(result);
  }

  @override
  Future<T?>? navigateOffAll<T>(String routeName, {Object? arguments}) {
    return Get.offAllNamed<T>(routeName, arguments: arguments);
  }

  @override
  Future<T?>? navigateOff<T>(String routeName, {Object? arguments}) {
    return Get.offNamed<T>(routeName, arguments: arguments);
  }

  @override
  Future<T?> showDialog<T>(Widget dialog) {
    return Get.dialog<T>(dialog);
  }

  @override
  Future<T?> showBottomSheet<T>(Widget bottomSheet) {
    return Get.bottomSheet<T>(bottomSheet);
  }

  @override
  void showSnackbar(String title, String message, {Duration? duration}) {
    Get.snackbar(
      title,
      message,
      duration: duration ?? const Duration(seconds: 3),
    );
  }
}
```

### Phase 4: Feature Module DI Setup

#### 4.1 Create Feature DI Module
Create file for each feature: `lib/features/feature_name/data/di/injection.dart`:
```dart
import 'package:injectable/injectable.dart';

import '../../domain/repositories/feature_repository.dart';
import '../../domain/usecases/get_feature.dart';
import '../../domain/usecases/get_all_features.dart';
import '../../domain/usecases/create_feature.dart';
import '../../domain/usecases/update_feature.dart';
import '../../domain/usecases/delete_feature.dart';
import '../repositories/feature_repository_impl.dart';
import '../datasources/remote/feature_remote_datasource.dart';
import '../datasources/remote/feature_remote_datasource_impl.dart';
import '../datasources/local/feature_local_datasource.dart';
import '../datasources/local/feature_local_datasource_impl.dart';
import '../mappers/feature_mapper.dart';

/// Feature module dependency injection
@module
abstract class FeatureModule {
  // Data sources

  @singleton
  FeatureRemoteDataSource get featureRemoteDataSource =>
      FeatureRemoteDataSourceImpl(
        getIt(), // HttpClient
        getIt(), // LoggerService
      );

  @singleton
  FeatureLocalDataSource get featureLocalDataSource =>
      FeatureLocalDataSourceImpl(
        getIt(), // Database
      );

  // Mappers

  @singleton
  FeatureMapper get featureMapper => FeatureMapper();

  // Repository

  @singleton
  FeatureRepository get featureRepository => FeatureRepositoryImpl(
        featureRemoteDataSource,
        featureLocalDataSource,
        featureMapper,
      );

  // Use cases

  @singleton
  GetFeatureUseCase get getFeatureUseCase =>
      GetFeatureUseCase(featureRepository);

  @singleton
  GetAllFeaturesUseCase get getAllFeaturesUseCase =>
      GetAllFeaturesUseCase(featureRepository);

  @singleton
  CreateFeatureUseCase get createFeatureUseCase =>
      CreateFeatureUseCase(featureRepository);

  @singleton
  UpdateFeatureUseCase get updateFeatureUseCase =>
      UpdateFeatureUseCase(featureRepository);

  @singleton
  DeleteFeatureUseCase get deleteFeatureUseCase =>
      DeleteFeatureUseCase(featureRepository);

  // Controllers

  @factory
  FeatureController get featureController => FeatureController(
        getAllFeaturesUseCase: getIt(),
        getFeatureUseCase: getIt(),
        createFeatureUseCase: getIt(),
        updateFeatureUseCase: getIt(),
        deleteFeatureUseCase: getIt(),
      );
}
```

#### 4.2 Create Controller Factory
Create file: `lib/core/di/controller_factory.dart`:
```dart
import 'package:get/get.dart';
import 'injection_resolver.dart';

/// Factory for creating GetX controllers with dependency injection
class ControllerFactory {
  /// Create controller of type [T]
  static T create<T extends GetxController>() {
    return getIt<T>();
  }

  /// Create and register controller of type [T]
  static T register<T extends GetxController>({String? tag}) {
    final controller = create<T>();
    Get.put<T>(controller, tag: tag);
    return controller;
  }

  /// Find controller of type [T]
  static T find<T extends GetxController>({String? tag}) {
    return Get.find<T>(tag: tag);
  }

  /// Lazy create controller of type [T]
  static T lazyPut<T extends GetxController>(
    T Function() factory, {
    String? tag,
  }) {
    return Get.lazyPut<T>(() => factory(), tag: tag);
  }
}
```

### Phase 5: Application Initialization

#### 5.1 Update Main.dart
Update `lib/main.dart`:
```dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'core/di/injection_config.dart';
import 'core/di/injection_resolver.dart';
import 'core/services/initialization_service.dart';
import 'app/routes/app_pages.dart';
import 'app/theme/app_theme.dart';

Future<void> main() async {
  // Ensure Flutter bindings are initialized
  WidgetsFlutterBinding.ensureInitialized();

  // Load environment variables
  await dotenv.load(fileName: '.env');

  // Configure dependency injection
  await configureDependenciesForEnvironment(
    dotenv.env['ENVIRONMENT'] ?? 'development',
  );

  // Initialize core services
  await Get.putAsync(() => InitializationService().init());

  // Run app
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'Flutter App',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      initialRoute: AppPages.INITIAL,
      getPages: AppPages.routes,
      defaultTransition: Transition.fadeIn,
      debugShowCheckedModeBanner: false,
    );
  }
}
```

#### 5.2 Create Initialization Service
Create file: `lib/core/services/initialization_service.dart`:
```dart
import 'package:get/get.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'database_service.dart';
import 'storage_service.dart';
import 'api_service.dart';
import 'logger_service.dart';

/// Service responsible for initializing app components
class InitializationService extends GetxService {
  final DatabaseService _databaseService = getIt<DatabaseService>();
  final StorageService _storageService = getIt<StorageService>();
  final ApiService _apiService = getIt<ApiService>();
  final LoggerService _loggerService = getIt<LoggerService>();

  /// Initialize all core services
  Future<InitializationService> init() async {
    try {
      _loggerService.info('Starting app initialization...');

      // Initialize storage
      await _storageService.init();
      _loggerService.info('Storage initialized');

      // Initialize database
      await _databaseService.init();
      _loggerService.info('Database initialized');

      // Initialize API service
      await _apiService.init();
      _loggerService.info('API service initialized');

      // Load user preferences
      await _loadUserPreferences();
      _loggerService.info('User preferences loaded');

      _loggerService.info('App initialization completed');
      return this;
    } catch (e, stackTrace) {
      _loggerService.error('App initialization failed', e, stackTrace);
      rethrow;
    }
  }

  Future<void> _loadUserPreferences() async {
    // Load theme preference
    final themeMode = _storageService.getString('theme_mode');
    if (themeMode != null) {
      Get.changeThemeMode(ThemeMode.values.firstWhere(
        (mode) => mode.name == themeMode,
        orElse: () => ThemeMode.system,
      ));
    }

    // Load language preference
    final languageCode = _storageService.getString('language_code');
    if (languageCode != null) {
      Get.updateLocale(Locale(languageCode));
    }
  }
}
```

### Phase 6: Usage Patterns

#### 6.1 Using Dependencies in Controllers
```dart
// lib/features/user/presentation/controllers/user_controller.dart
import 'package:get/get.dart';
import '../../../core/di/injection_resolver.dart';

class UserController extends GetxController {
  final UserService _userService = getIt<UserService>();
  final NavigationService _navigationService = getIt<NavigationService>();
  final LoggerService _loggerService = getIt<LoggerService>();

  final users = <User>[].obs;
  final isLoading = false.obs;

  Future<void> loadUsers() async {
    try {
      isLoading.value = true;
      final result = await _userService.getUsers();
      users.assignAll(result);
    } catch (e) {
      _loggerService.error('Failed to load users', e);
      _navigationService.showSnackbar('Error', e.toString());
    } finally {
      isLoading.value = false;
    }
  }
}
```

#### 6.2 Using Dependencies in Use Cases
```dart
// lib/features/user/domain/usecases/get_user.dart
import '../../../core/di/injection_resolver.dart';

class GetUserUseCase {
  final UserRepository _repository = getIt<UserRepository>();
  final LoggerService _loggerService = getIt<LoggerService>();

  Future<Result<User>> execute(String userId) async {
    try {
      _loggerService.info('Getting user: $userId');
      return await _repository.getUser(userId);
    } catch (e) {
      _loggerService.error('Failed to get user: $userId', e);
      return Result.failure(e.toString());
    }
  }
}
```

#### 6.3 Using Dependencies in Repositories
```dart
// lib/features/user/data/repositories/user_repository_impl.dart
import '../../../core/di/injection_resolver.dart';

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource _remoteDataSource = getIt<UserRemoteDataSource>();
  final UserLocalDataSource _localDataSource = getIt<UserLocalDataSource>();
  final LoggerService _loggerService = getIt<LoggerService>();

  @override
  Future<Result<User>> getUser(String userId) async {
    try {
      _loggerService.debug('Getting user from remote: $userId');
      final result = await _remoteDataSource.getUser(userId);

      if (result.isSuccess) {
        // Cache locally
        await _localDataSource.saveUser(result.data);
      }

      return result;
    } catch (e) {
      _loggerService.error('Remote fetch failed, trying local: $userId', e);

      // Try local cache
      return await _localDataSource.getUser(userId);
    }
  }
}
```

### Phase 7: Testing with DI

#### 7.1 Create Test DI Setup
Create file: `test/core/di/test_injection_config.dart`:
```dart
import 'package:injectable/injectable.dart';
import 'package:mockito/annotations.dart';

import '../../lib/core/di/injection_resolver.dart';

@GenerateMocks([
  ApiService,
  UserRepository,
  NavigationService,
])
import 'test_injection_config.mocks.dart';

/// Configure dependencies for testing
Future<void> configureTestDependencies() async {
  getIt.reset();

  // Register mock services
  getIt.registerSingleton<ApiService>(MockApiService());
  getIt.registerSingleton<UserRepository>(MockUserRepository());
  getIt.registerSingleton<NavigationService>(MockNavigationService());

  // Register real services that don't need mocking
  getIt.registerSingleton<LoggerService>(TestLoggerService());
}

/// Reset all test dependencies
void resetTestDependencies() {
  getIt.reset();
}
```

#### 7.2 Write Test with Mock Dependencies
Create file: `test/features/user/presentation/controllers/user_controller_test.dart`:
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

import '../../../lib/core/di/injection_resolver.dart';
import '../../../lib/features/user/presentation/controllers/user_controller.dart';
import '../../core/di/test_injection_config.dart';

void main() {
  late UserController controller;
  late MockUserService mockUserService;
  late MockNavigationService mockNavigationService;

  setUp(() async {
    await configureTestDependencies();

    controller = UserController();
    mockUserService = getIt<MockUserService>();
    mockNavigationService = getIt<MockNavigationService>();
  });

  tearDown(() {
    resetTestDependencies();
  });

  test('should load users successfully', () async {
    // Arrange
    final mockUsers = [
      User(id: '1', name: 'John', email: 'john@example.com'),
      User(id: '2', name: 'Jane', email: 'jane@example.com'),
    ];

    when(mockUserService.getUsers())
        .thenAnswer((_) async => Result.success(mockUsers));

    // Act
    await controller.loadUsers();

    // Assert
    expect(controller.users.length, 2);
    expect(controller.users.first.name, 'John');
    expect(controller.isLoading.value, false);

    verify(mockUserService.getUsers()).called(1);
  });

  test('should handle error when loading users fails', () async {
    // Arrange
    when(mockUserService.getUsers())
        .thenThrow(Exception('Network error'));

    // Act
    await controller.loadUsers();

    // Assert
    expect(controller.users.isEmpty, true);
    expect(controller.isLoading.value, false);

    verify(mockNavigationService.showSnackbar(
      'Error',
      'Exception: Network error',
    )).called(1);
  });
}
```

### Phase 8: Code Generation

#### 8.1 Generate DI Code
```bash
# Generate dependency injection code
flutter packages pub run build_runner build --delete-conflicting-outputs

# Or in watch mode during development
flutter packages pub run build_runner watch --delete-conflicting-outputs
```

#### 8.2 Verify Generated Files
Check generated files:
- `.dart_tool/build/generated/core/di/injection_config.dart`
- Verify all modules are properly registered
- Check for any circular dependencies

## Advanced Patterns

### 1. Conditional Registration
```dart
@module
abstract class ConditionalModule {
  @singleton
  ApiService get apiService {
    if (getIt<String>(instanceName: 'environment') == 'testing') {
      return MockApiService();
    }
    return RealApiService();
  }
}
```

### 2. Named Dependencies
```dart
@module
abstract class NamedModule {
  @singleton
  @Named('primary')
  Database get primaryDatabase => DatabaseImpl('primary');

  @singleton
  @Named('cache')
  Database get cacheDatabase => DatabaseImpl('cache');
}

// Usage
final primaryDb = getIt<Database>(instanceName: 'primary');
final cacheDb = getIt<Database>(instanceName: 'cache');
```

### 3. Async Dependencies
```dart
@module
abstract class AsyncModule {
  @preResolve
  @singleton
  Future<StorageService> get storageService async {
    final prefs = await SharedPreferences.getInstance();
    return StorageServiceImpl(prefs);
  }
}
```

## Verification Checklist

### Configuration
- [ ] All dependencies registered correctly
- [ ] No circular dependencies
- [ ] Proper lifetimes configured
- [ ] Generated code compiles without errors

### Testing
- [ ] Test DI setup works correctly
- [ ] Mock dependencies can be injected
- [ ] Test isolation maintained
- [ ] No test interference

### Performance
- [ ] Singletons not recreated unnecessarily
- [ ] Lazy loading working correctly
- [ ] Memory usage acceptable
- [ ] Startup time within limits

### Code Quality
- [ ] Interface-based programming
- [ ] Proper separation of concerns
- [ ] No hardcoded dependencies
- [ ] Documentation added

## Common Issues and Solutions

### Issue: Circular Dependency
**Solution**:
- Review dependency graph
- Extract common dependencies to separate module
- Use lazy singleton or factory pattern

### Issue: Service Not Found
**Solution**:
- Check if dependency is registered
- Verify module is included in configuration
- Check for typos in service names

### Issue: Memory Leaks
**Solution**:
- Review singleton usage
- Implement proper disposal methods
- Use factory pattern for short-lived services

### Issue: Test Dependencies
**Solution**:
- Create separate test configuration
- Use mock implementations
- Reset DI container between tests

## Tools and Commands

### Development Commands
```bash
# Generate DI code
flutter packages pub run build_runner build

# Watch for changes
flutter packages pub run build_runner watch

# Clean generated files
flutter packages pub run build_runner clean

# Run tests with DI
flutter test test/core/di/
```

### Useful VS Code Extensions
- Injectable Dart
- Dependency Graph Visualizer
- Flutter Inspector

## Best Practices

1. **Program to interfaces, not implementations**
2. **Use singletons sparingly**
3. **Prefer lazy loading when possible**
4. **Keep dependency graph shallow**
5. **Test with mock implementations**
6. **Document all registered dependencies**
7. **Avoid service locator pattern where possible**
8. **Use constructor injection for required dependencies**

## Resources

- [GetIt Documentation](https://pub.dev/packages/get_it)
- [Injectable Documentation](https://pub.dev/packages/injectable)
- [Dependency Injection in Flutter](https://flutter.dev/docs/development/data-and-backend/state-mgmt/dependency-injection)
- [Clean Architecture DI Patterns](https://resocoder.com/2019/09/10/flutter-dependency-injection-with-getit/)