# Flutter GetX Clean Architecture - Examples

Complete, ready-to-use examples demonstrating real-world implementations.

## Example 1: User Management Feature (Complete)

### Domain Layer

**entities/user.dart**
```dart
class User {
  final String id;
  final String name;
  final String email;
  final String? avatarUrl;
  final DateTime createdAt;

  const User({
    required this.id,
    required this.name,
    required this.email,
    this.avatarUrl,
    required this.createdAt,
  });

  User copyWith({String? name, String? email}) {
    return User(
      id: id,
      name: name ?? this.name,
      email: email ?? this.email,
      avatarUrl: avatarUrl,
      createdAt: createdAt,
    );
  }
}
```

**repositories/user_repository.dart**
```dart
abstract class UserRepository {
  Future<Either<Failure, User>> getUser(String id);
  Future<Either<Failure, List<User>>> getUsers();
  Future<Either<Failure, User>> updateUser(User user);
}
```

**usecases/get_users_usecase.dart**
```dart
class GetUsersUseCase implements UseCase<List<User>, NoParams> {
  final UserRepository repository;
  GetUsersUseCase(this.repository);

  @override
  Future<Either<Failure, List<User>>> call(NoParams params) {
    return repository.getUsers();
  }
}
```

### Data Layer

**models/user_model.dart**
```dart
@JsonSerializable()
class UserModel {
  final String id;
  final String name;
  final String email;
  @JsonKey(name: 'avatar_url')
  final String? avatarUrl;
  @JsonKey(name: 'created_at')
  final String createdAt;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
    this.avatarUrl,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);

  Map<String, dynamic> toJson() => _$UserModelToJson(this);

  User toEntity() {
    return User(
      id: id,
      name: name,
      email: email,
      avatarUrl: avatarUrl,
      createdAt: DateTime.parse(createdAt),
    );
  }
}
```

**repositories/user_repository_impl.dart**
```dart
class UserRepositoryImpl extends BaseRepository implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    return safeCall(() async {
      if (await networkInfo.isConnected) {
        final users = await remoteDataSource.getUsers();
        await localDataSource.cacheUsers(users);
        return users.map((model) => model.toEntity()).toList();
      } else {
        final cachedUsers = await localDataSource.getCachedUsers();
        return cachedUsers.map((model) => model.toEntity()).toList();
      }
    });
  }
}
```

### Presentation Layer

**controllers/user_controller.dart**
```dart
class UserController extends BaseController {
  final GetUsersUseCase getUsersUseCase;

  UserController({required this.getUsersUseCase});

  final RxList<User> _users = <User>[].obs;
  List<User> get users => _users;

  @override
  void initController() {
    loadUsers();
  }

  Future<void> loadUsers() async {
    await handleUseCaseResult(
      execute: () => getUsersUseCase(const NoParams()),
      onSuccess: (users) {
        _users.assignAll(users);
        setEmpty(users.isEmpty);
      },
    );
  }
}
```

**pages/user_list_view.dart**
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
            return UserListTile(user: controller.users[index]);
          },
        );
      }),
    );
  }
}
```

**bindings/user_binding.dart**
```dart
class UserBinding extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut<UserRemoteDataSource>(
      () => UserRemoteDataSourceImpl(dio: Get.find()),
    );
    Get.lazyPut<UserLocalDataSource>(
      () => UserLocalDataSourceImpl(database: Get.find()),
    );
    Get.lazyPut<UserRepository>(
      () => UserRepositoryImpl(
        remoteDataSource: Get.find(),
        localDataSource: Get.find(),
        networkInfo: Get.find(),
      ),
    );
    Get.lazyPut(() => GetUsersUseCase(Get.find()));
    Get.lazyPut(() => UserController(getUsersUseCase: Get.find()));
  }
}
```

---

## Example 2: Search with Debounce

**controllers/search_controller.dart**
```dart
class SearchController extends BaseController {
  final SearchItemsUseCase searchItemsUseCase;

  final RxString _query = ''.obs;
  String get query => _query.value;
  set query(String value) => _query.value = value;

  final RxList<SearchResult> _results = <SearchResult>[].obs;
  List<SearchResult> get results => _results;

  Worker? _debounceWorker;

  @override
  void initController() {
    _debounceWorker = debounce(
      _query,
      (query) => _performSearch(query),
      time: const Duration(milliseconds: 500),
    );
  }

  Future<void> _performSearch(String query) async {
    if (query.isEmpty) return;

    await handleUseCaseResult(
      execute: () => searchItemsUseCase(SearchParams(query)),
      onSuccess: (results) => _results.assignAll(results),
    );
  }

  @override
  void disposeController() {
    _debounceWorker?.dispose();
  }
}
```

---

## Example 3: Pagination

**controllers/paginated_list_controller.dart**
```dart
class PaginatedListController extends BaseController {
  final RxList<Item> _items = <Item>[].obs;
  List<Item> get items => _items;

  final RxBool _isLoadingMore = false.obs;
  bool get isLoadingMore => _isLoadingMore.value;

  int _currentPage = 1;
  bool _hasMore = true;

  Future<void> loadMore() async {
    if (_isLoadingMore.value || !_hasMore) return;

    _isLoadingMore.value = true;

    final result = await getItemsUseCase(
      GetItemsParams(page: _currentPage + 1),
    );

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

---

These examples demonstrate production-ready implementations following all best practices.
