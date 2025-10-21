---
name: Flutter GetX Clean Architecture
description: Expert guidance for building production-ready Flutter apps with Clean Architecture, GetX state management, Drift database, and comprehensive testing. Use when working on Flutter projects requiring scalable architecture, state management patterns, dependency injection, or when migrating to clean architecture principles.
version: 2.0.0
dependencies: flutter>=3.0.0, get>=4.6.5, dartz>=0.10.1, drift>=2.0.0
---

# Flutter GetX Clean Architecture

Expert skill for building scalable, maintainable Flutter applications using Clean Architecture principles with GetX framework. This skill provides validated patterns from Stack Overflow, GitHub, and industry experts for production-ready mobile development.

## When to use this skill

Use this skill when you need to:
- Design or refactor Flutter apps with clean architecture
- Implement state management with GetX (controllers, bindings, navigation)
- Set up dependency injection patterns
- Create modular, feature-based project structures
- Build offline-first apps with Drift database
- Write testable code with proper separation of concerns
- Optimize Flutter app performance
- Debug memory leaks or state management issues

## Core Architecture Principles

### Three-Layer Architecture

**1. Domain Layer** (Business Logic)
- Pure Dart code, no Flutter dependencies
- Contains: Entities, Use Cases, Repository Interfaces
- Defines business rules and application logic

**2. Data Layer** (Data Management)
- Handles data sources (API, database, cache)
- Contains: Models, Repository Implementations, Data Sources
- Implements offline-first patterns

**3. Presentation Layer** (UI & State)
- GetX controllers and reactive UI
- Contains: Controllers, Views, Widgets, Bindings
- Manages user interactions and state updates

### Project Structure

```
lib/
├── app/
│   ├── core/                  # Shared infrastructure
│   │   ├── base/             # Base classes (controller, usecase, repo)
│   │   ├── constants/        # App constants and configs
│   │   ├── errors/           # Failures and exceptions
│   │   ├── network/          # HTTP client, network info
│   │   └── services/         # Global services (storage, analytics)
│   ├── data/                 # Data layer implementations
│   │   ├── models/           # DTOs with JSON serialization
│   │   ├── repositories/     # Repository implementations
│   │   └── datasources/      # API clients, database DAOs
│   ├── domain/               # Business logic
│   │   ├── entities/         # Domain models
│   │   ├── repositories/     # Repository contracts
│   │   └── usecases/         # Business operations
│   ├── presentation/         # UI layer
│   │   ├── features/         # Feature modules
│   │   │   ├── auth/
│   │   │   ├── home/
│   │   │   └── profile/
│   │   └── shared/           # Shared widgets
│   └── routes/               # Navigation
└── main.dart
```

## Key Implementation Patterns

### 1. Base Controller with State Management

```dart
abstract class BaseController extends GetxController {
  final RxBool _isLoading = false.obs;
  final RxString _errorMessage = ''.obs;

  bool get isLoading => _isLoading.value;
  String get errorMessage => _errorMessage.value;
  bool get hasError => _errorMessage.value.isNotEmpty;

  void setLoading(bool value) => _isLoading.value = value;
  void setError(String message) => _errorMessage.value = message;
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
}
```

### 2. Use Case Pattern with Result Type

```dart
import 'package:dartz/dartz.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams {
  const NoParams();
}

// Example use case
class GetUserUseCase implements UseCase<User, GetUserParams> {
  final UserRepository repository;

  GetUserUseCase(this.repository);

  @override
  Future<Either<Failure, User>> call(GetUserParams params) {
    return repository.getUser(params.userId);
  }
}
```

### 3. Repository Pattern with Offline-First

```dart
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  @override
  Future<Either<Failure, User>> getUser(String id) async {
    try {
      if (await networkInfo.isConnected) {
        final userModel = await remoteDataSource.getUser(id);
        await localDataSource.cacheUser(userModel);
        return Right(userModel.toEntity());
      } else {
        final cachedUser = await localDataSource.getUser(id);
        return Right(cachedUser.toEntity());
      }
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    } on CacheException catch (e) {
      return Left(CacheFailure(e.message));
    }
  }
}
```

### 4. GetX Controller with Best Practices

```dart
class UserController extends BaseController {
  final GetUsersUseCase getUsersUseCase;

  UserController({required this.getUsersUseCase});

  // Only make observable what UI needs to react to
  final RxList<User> _users = <User>[].obs;
  List<User> get users => _users;

  @override
  void initController() {
    loadUsers();
  }

  Future<void> loadUsers() async {
    setLoading(true);
    clearError();

    final result = await getUsersUseCase(const NoParams());

    result.fold(
      (failure) => setError(failure.message),
      (users) => _users.assignAll(users),
    );

    setLoading(false);
  }
}
```

### 5. Reactive UI with Optimized Rebuilding

```dart
class UserListView extends GetView<UserController> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Users')),
      body: Obx(() {
        if (controller.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }

        if (controller.hasError) {
          return ErrorWidget(
            message: controller.errorMessage,
            onRetry: controller.loadUsers,
          );
        }

        return ListView.builder(
          itemCount: controller.users.length,
          itemBuilder: (context, index) {
            final user = controller.users[index];
            return UserListTile(user: user);
          },
        );
      }),
    );
  }
}
```

### 6. Dependency Injection with Bindings

```dart
class UserBinding extends Bindings {
  @override
  void dependencies() {
    // Data Sources - lazy initialization
    Get.lazyPut<UserRemoteDataSource>(
      () => UserRemoteDataSourceImpl(dio: Get.find()),
    );

    Get.lazyPut<UserLocalDataSource>(
      () => UserLocalDataSourceImpl(database: Get.find()),
    );

    // Repository
    Get.lazyPut<UserRepository>(
      () => UserRepositoryImpl(
        remoteDataSource: Get.find(),
        localDataSource: Get.find(),
        networkInfo: Get.find(),
      ),
    );

    // Use Cases
    Get.lazyPut(() => GetUsersUseCase(Get.find()));

    // Controller
    Get.lazyPut(() => UserController(getUsersUseCase: Get.find()));
  }
}
```

## Advanced Patterns

### Workers for Reactive Side Effects

```dart
class SearchController extends BaseController {
  final RxString _searchQuery = ''.obs;
  String get searchQuery => _searchQuery.value;

  Worker? _searchWorker;

  @override
  void initController() {
    // Debounce search - wait 500ms after user stops typing
    _searchWorker = debounce(
      _searchQuery,
      (query) => _performSearch(query),
      time: const Duration(milliseconds: 500),
    );
  }

  @override
  void disposeController() {
    _searchWorker?.dispose();
  }
}
```

### Pagination Pattern

```dart
class PaginatedListController extends BaseController {
  final RxList<Item> _items = <Item>[].obs;
  final RxBool _isLoadingMore = false.obs;
  int _currentPage = 1;
  bool _hasMore = true;

  Future<void> loadMore() async {
    if (_isLoadingMore.value || !_hasMore) return;

    _isLoadingMore.value = true;
    final result = await getItemsUseCase(GetItemsParams(page: _currentPage + 1));

    result.fold(
      (failure) => setError(failure.message),
      (newItems) {
        if (newItems.isEmpty) {
          _hasMore = false;
        } else {
          _items.addAll(newItems);
          _currentPage++;
        }
      },
    );

    _isLoadingMore.value = false;
  }
}
```

## Best Practices (Validated by Community)

### State Management
✅ Use `.obs` only for state that triggers UI updates
✅ Prefer `Obx` for automatic reactivity, `GetBuilder` for manual control
✅ Use workers (`debounce`, `ever`, `once`) for side effects
✅ Dispose controllers properly in `onClose()`

### Dependency Injection
✅ Use `Get.lazyPut()` for lazy loading and memory optimization
✅ Avoid injecting controllers into other controllers via constructor
✅ Use `Get.find()` to retrieve dependencies when needed
✅ Use `permanent: true` sparingly to prevent memory leaks

### Testing
✅ Enable `Get.testMode = true` in test setup
✅ Mock controllers with Mockito properly
✅ Use `Get.reset()` in tearDown to clean up
✅ Test business logic in use cases independently

### Performance
✅ Use selective widget rebuilding with GetBuilder IDs
✅ Implement pagination and lazy loading for large datasets
✅ Leverage automatic memory cleanup on route removal
✅ Use debounce for search/input operations

### Database (Drift)
✅ Use guided migrations with `drift_dev` commands
✅ Test migrations thoroughly with generated test files
✅ Implement offline-first caching strategy
✅ Use proper schema versioning

## Common Pitfalls to Avoid

❌ Don't inject controllers into other controllers via constructor
❌ Don't make everything observable - only UI-dependent state
❌ Don't use `permanent: true` everywhere - causes memory leaks
❌ Don't forget to dispose controllers, workers, and text controllers
❌ Don't skip testing - especially for critical business logic
❌ Don't tightly couple UI to data layer - always go through domain

## Testing Strategy

### Unit Testing Controllers

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
    verify(mockUseCase(const NoParams())).called(1);
  });
}
```

## Navigation and Routing

```dart
// Define routes
abstract class Routes {
  static const HOME = '/home';
  static const USER_DETAIL = '/users/:id';
}

// Configure pages
class AppPages {
  static final routes = [
    GetPage(
      name: Routes.HOME,
      page: () => const HomeView(),
      binding: HomeBinding(),
      middlewares: [AuthMiddleware()],
    ),
  ];
}

// Navigate
Get.toNamed(Routes.USER_DETAIL, parameters: {'id': '123'});
```

## Resources

For advanced patterns, edge cases, and detailed examples, see:
- `reference.md` - Comprehensive API reference and patterns
- `examples.md` - Real-world code examples

## Version History

- **2.0.0** (Oct 2025): Enhanced with community best practices, offline-first patterns, performance optimizations
- **1.0.0**: Initial release with basic clean architecture patterns
