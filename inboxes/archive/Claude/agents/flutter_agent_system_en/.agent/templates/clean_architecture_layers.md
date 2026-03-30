# Clean Architecture Layers - Code Examples

This template provides detailed code examples for implementing each layer of the Clean Architecture.

## Domain Layer (No Framework Dependencies)

### Entity Example

```dart
// lib/domain/entities/user.dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String email;
  final String name;
  final String? profileImage;
  final DateTime createdAt;
  final DateTime updatedAt;

  const User({
    required this.id,
    required this.email,
    required this.name,
    this.profileImage,
    required this.createdAt,
    required this.updatedAt,
  });

  // Copy with for immutability
  User copyWith({
    String? id,
    String? email,
    String? name,
    String? profileImage,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      name: name ?? this.name,
      profileImage: profileImage ?? this.profileImage,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  @override
  List<Object?> get props => [id, email, name, profileImage, createdAt, updatedAt];
}
```

### Repository Interface

```dart
// lib/domain/repositories/user_repository.dart
import 'package:shared/shared.dart';
import '../entities/user.dart';

abstract class UserRepository {
  /// Fetch user by ID
  Future<Result<User, Exception>> getUser(String id);
  
  /// Get all users
  Future<Result<List<User>, Exception>> getAllUsers();
  
  /// Create new user
  Future<Result<String, Exception>> createUser(User user);
  
  /// Update existing user
  Future<Result<void, Exception>> updateUser(User user);
  
  /// Delete user
  Future<Result<void, Exception>> deleteUser(String id);
  
  /// Watch user changes (stream)
  Stream<User?> watchUser(String id);
}
```

### Usecase Example

```dart
// lib/domain/usecases/get_user_usecase.dart
import 'package:shared/shared.dart';
import '../entities/user.dart';
import '../repositories/user_repository.dart';

class GetUserUsecase {
  final UserRepository _repository;

  GetUserUsecase(this._repository);

  /// Get user by ID
  /// Returns Result with User or Exception
  Future<Result<User, Exception>> call(String userId) async {
    return _repository.getUser(userId);
  }
}

// lib/domain/usecases/get_all_users_usecase.dart
class GetAllUsersUsecase {
  final UserRepository _repository;

  GetAllUsersUsecase(this._repository);

  Future<Result<List<User>, Exception>> call() async {
    return _repository.getAllUsers();
  }
}

// lib/domain/usecases/create_user_usecase.dart
class CreateUserUsecase {
  final UserRepository _repository;

  CreateUserUsecase(this._repository);

  Future<Result<String, Exception>> call(User user) async {
    // Can add business logic here (validation, etc.)
    if (user.email.isEmpty) {
      return Result.failure(Exception('Email cannot be empty'));
    }
    
    return _repository.createUser(user);
  }
}

// lib/domain/usecases/delete_user_usecase.dart
class DeleteUserUsecase {
  final UserRepository _repository;

  DeleteUserUsecase(this._repository);

  Future<Result<void, Exception>> call(String userId) async {
    return _repository.deleteUser(userId);
  }
}
```

## Data Layer (Framework OK, but not Flutter/GetX specific)

### Model (DTO)

```dart
// lib/data/models/user_model.dart
import '../../domain/entities/user.dart';

class UserModel extends User {
  const UserModel({
    required String id,
    required String email,
    required String name,
    String? profileImage,
    required DateTime createdAt,
    required DateTime updatedAt,
  }) : super(
    id: id,
    email: email,
    name: name,
    profileImage: profileImage,
    createdAt: createdAt,
    updatedAt: updatedAt,
  );

  // From JSON (API response)
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String,
      profileImage: json['profileImage'] as String?,
      createdAt: DateTime.parse(json['createdAt'] as String),
      updatedAt: DateTime.parse(json['updatedAt'] as String),
    );
  }

  // To JSON (for API requests)
  Map<String, dynamic> toJson() => {
    'id': id,
    'email': email,
    'name': name,
    'profileImage': profileImage,
    'createdAt': createdAt.toIso8601String(),
    'updatedAt': updatedAt.toIso8601String(),
  };

  // From domain entity
  factory UserModel.fromEntity(User user) {
    return UserModel(
      id: user.id,
      email: user.email,
      name: user.name,
      profileImage: user.profileImage,
      createdAt: user.createdAt,
      updatedAt: user.updatedAt,
    );
  }

  // To domain entity (if needed)
  User toEntity() => this;
}
```

### Local Datasource Interface & Implementation

```dart
// lib/data/datasources/local/user_local_datasource.dart
import '../models/user_model.dart';

abstract class UserLocalDatasource {
  Future<List<UserModel>> getAllUsers();
  Future<UserModel?> getUserById(String id);
  Future<void> saveUsers(List<UserModel> users);
  Future<void> saveUser(UserModel user);
  Future<void> deleteUser(String id);
  Future<void> clearAll();
}

// Implementation
import 'package:core/core.dart';

class UserLocalDatasourceImpl implements UserLocalDatasource {
  final DatabaseService _databaseService;

  UserLocalDatasourceImpl(this._databaseService);

  @override
  Future<List<UserModel>> getAllUsers() async {
    try {
      final users = await _databaseService.getAllUsers();
      return users.map((user) => UserModel.fromJson(user)).toList();
    } catch (e) {
      throw Exception('Failed to get users from local storage: $e');
    }
  }

  @override
  Future<UserModel?> getUserById(String id) async {
    try {
      final user = await _databaseService.getUserById(id);
      return user != null ? UserModel.fromJson(user) : null;
    } catch (e) {
      throw Exception('Failed to get user from local storage: $e');
    }
  }

  @override
  Future<void> saveUsers(List<UserModel> users) async {
    try {
      for (final user in users) {
        await _databaseService.saveUser(user.toJson());
      }
    } catch (e) {
      throw Exception('Failed to save users to local storage: $e');
    }
  }

  @override
  Future<void> saveUser(UserModel user) async {
    try {
      await _databaseService.saveUser(user.toJson());
    } catch (e) {
      throw Exception('Failed to save user to local storage: $e');
    }
  }

  @override
  Future<void> deleteUser(String id) async {
    try {
      await _databaseService.deleteUser(id);
    } catch (e) {
      throw Exception('Failed to delete user from local storage: $e');
    }
  }

  @override
  Future<void> clearAll() async {
    try {
      await _databaseService.clearAllUsers();
    } catch (e) {
      throw Exception('Failed to clear local storage: $e');
    }
  }
}
```

### Remote Datasource Interface & Implementation

```dart
// lib/data/datasources/remote/user_remote_datasource.dart
import 'package:dio/dio.dart';
import '../models/user_model.dart';

abstract class UserRemoteDatasource {
  Future<UserModel> getUser(String id);
  Future<List<UserModel>> getAllUsers();
  Future<UserModel> createUser(UserModel user);
  Future<void> updateUser(UserModel user);
  Future<void> deleteUser(String id);
}

// Implementation
class UserRemoteDatasourceImpl implements UserRemoteDatasource {
  final Dio dio;
  static const String _baseUrl = '/api/users';

  UserRemoteDatasourceImpl(this.dio);

  @override
  Future<UserModel> getUser(String id) async {
    try {
      final response = await dio.get('$_baseUrl/$id');
      
      if (response.statusCode != 200) {
        throw Exception('Failed to fetch user: ${response.statusCode}');
      }
      
      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      throw Exception('Network error: ${e.message}');
    } catch (e) {
      throw Exception('Failed to fetch user: $e');
    }
  }

  @override
  Future<List<UserModel>> getAllUsers() async {
    try {
      final response = await dio.get(_baseUrl);
      
      if (response.statusCode != 200) {
        throw Exception('Failed to fetch users: ${response.statusCode}');
      }
      
      final List<dynamic> data = response.data;
      return data.map((user) => UserModel.fromJson(user)).toList();
    } on DioException catch (e) {
      throw Exception('Network error: ${e.message}');
    } catch (e) {
      throw Exception('Failed to fetch users: $e');
    }
  }

  @override
  Future<UserModel> createUser(UserModel user) async {
    try {
      final response = await dio.post(
        _baseUrl,
        data: user.toJson(),
      );
      
      if (response.statusCode != 201) {
        throw Exception('Failed to create user: ${response.statusCode}');
      }
      
      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      throw Exception('Network error: ${e.message}');
    } catch (e) {
      throw Exception('Failed to create user: $e');
    }
  }

  @override
  Future<void> updateUser(UserModel user) async {
    try {
      final response = await dio.put(
        '$_baseUrl/${user.id}',
        data: user.toJson(),
      );
      
      if (response.statusCode != 200) {
        throw Exception('Failed to update user: ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw Exception('Network error: ${e.message}');
    } catch (e) {
      throw Exception('Failed to update user: $e');
    }
  }

  @override
  Future<void> deleteUser(String id) async {
    try {
      final response = await dio.delete('$_baseUrl/$id');
      
      if (response.statusCode != 204 && response.statusCode != 200) {
        throw Exception('Failed to delete user: ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw Exception('Network error: ${e.message}');
    } catch (e) {
      throw Exception('Failed to delete user: $e');
    }
  }
}
```

### Repository Implementation

```dart
// lib/data/repositories/user_repository_impl.dart
import 'package:shared/shared.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/user_repository.dart';
import '../datasources/local/user_local_datasource.dart';
import '../datasources/remote/user_remote_datasource.dart';
import '../models/user_model.dart';

class UserRepositoryImpl implements UserRepository {
  final UserLocalDatasource _localDatasource;
  final UserRemoteDatasource _remoteDatasource;

  UserRepositoryImpl(this._localDatasource, this._remoteDatasource);

  @override
  Future<Result<User, Exception>> getUser(String id) async {
    try {
      // Try local first (offline-first strategy)
      final localUser = await _localDatasource.getUserById(id);
      if (localUser != null) {
        return Result.success(localUser);
      }

      // If not found locally, fetch from remote
      final remoteUser = await _remoteDatasource.getUser(id);
      
      // Save to local for future access
      await _localDatasource.saveUser(remoteUser);
      
      return Result.success(remoteUser);
    } catch (e) {
      return Result.failure(Exception('Failed to get user: $e'));
    }
  }

  @override
  Future<Result<List<User>, Exception>> getAllUsers() async {
    try {
      // Get from local first
      final localUsers = await _localDatasource.getAllUsers();
      
      if (localUsers.isNotEmpty) {
        return Result.success(localUsers);
      }

      // If empty, fetch from remote
      final remoteUsers = await _remoteDatasource.getAllUsers();
      
      // Save to local
      await _localDatasource.saveUsers(remoteUsers);
      
      return Result.success(remoteUsers);
    } catch (e) {
      return Result.failure(Exception('Failed to get all users: $e'));
    }
  }

  @override
  Future<Result<String, Exception>> createUser(User user) async {
    try {
      final userModel = UserModel.fromEntity(user);
      final created = await _remoteDatasource.createUser(userModel);
      
      // Save to local
      await _localDatasource.saveUser(created);
      
      return Result.success(created.id);
    } catch (e) {
      return Result.failure(Exception('Failed to create user: $e'));
    }
  }

  @override
  Future<Result<void, Exception>> updateUser(User user) async {
    try {
      final userModel = UserModel.fromEntity(user);
      
      // Update remote
      await _remoteDatasource.updateUser(userModel);
      
      // Update local
      await _localDatasource.saveUser(userModel);
      
      return Result.success(null);
    } catch (e) {
      return Result.failure(Exception('Failed to update user: $e'));
    }
  }

  @override
  Future<Result<void, Exception>> deleteUser(String id) async {
    try {
      // Delete from remote
      await _remoteDatasource.deleteUser(id);
      
      // Delete from local
      await _localDatasource.deleteUser(id);
      
      return Result.success(null);
    } catch (e) {
      return Result.failure(Exception('Failed to delete user: $e'));
    }
  }

  @override
  Stream<User?> watchUser(String id) {
    return _localDatasource.watchUserById(id);
  }
}
```

## Presentation Layer (GetX + Flutter)

### GetX Controller

```dart
// lib/presentation/controllers/user_controller.dart
import 'package:get/get.dart';
import 'package:shared/shared.dart';
import '../../domain/entities/user.dart';
import '../../domain/usecases/get_user_usecase.dart';
import '../../domain/usecases/get_all_users_usecase.dart';
import '../../domain/usecases/create_user_usecase.dart';
import '../../domain/usecases/delete_user_usecase.dart';

class UserController extends GetxController {
  final GetUserUsecase _getUser;
  final GetAllUsersUsecase _getAllUsers;
  final CreateUserUsecase _createUser;
  final DeleteUserUsecase _deleteUser;

  UserController(
    this._getUser,
    this._getAllUsers,
    this._createUser,
    this._deleteUser,
  );

  // Observable state
  final users = <User>[].obs;
  final selectedUser = Rxn<User>();
  final isLoading = false.obs;
  final error = Rxn<String>();

  @override
  void onInit() {
    fetchAllUsers();
    super.onInit();
  }

  Future<void> fetchAllUsers() async {
    isLoading.value = true;
    error.value = null;

    final result = await _getAllUsers();
    result.fold(
      (data) => users.value = data,
      (failure) => error.value = failure.toString(),
    );

    isLoading.value = false;
  }

  Future<void> fetchUser(String id) async {
    isLoading.value = true;
    error.value = null;

    final result = await _getUser(id);
    result.fold(
      (user) => selectedUser.value = user,
      (failure) => error.value = failure.toString(),
    );

    isLoading.value = false;
  }

  Future<void> createNewUser(User user) async {
    isLoading.value = true;
    error.value = null;

    final result = await _createUser(user);
    result.fold(
      (userId) {
        Get.snackbar('Success', 'User created: $userId');
        fetchAllUsers();
      },
      (failure) => error.value = failure.toString(),
    );

    isLoading.value = false;
  }

  Future<void> deleteUserById(String id) async {
    isLoading.value = true;
    error.value = null;

    final result = await _deleteUser(id);
    result.fold(
      (_) {
        Get.snackbar('Success', 'User deleted');
        fetchAllUsers();
      },
      (failure) => error.value = failure.toString(),
    );

    isLoading.value = false;
  }

  @override
  void onClose() {
    super.onClose();
  }
}
```

### GetX Binding

```dart
// lib/presentation/bindings/user_binding.dart
import 'package:get/get.dart';
import 'package:core/core.dart';
import '../../data/datasources/local/user_local_datasource.dart';
import '../../data/datasources/remote/user_remote_datasource.dart';
import '../../data/repositories/user_repository_impl.dart';
import '../../domain/repositories/user_repository.dart';
import '../../domain/usecases/get_user_usecase.dart';
import '../../domain/usecases/get_all_users_usecase.dart';
import '../../domain/usecases/create_user_usecase.dart';
import '../../domain/usecases/delete_user_usecase.dart';
import '../controllers/user_controller.dart';

class UserBinding extends Bindings {
  @override
  void dependencies() {
    // Datasources
    Get.lazyPut<UserLocalDatasource>(
      () => UserLocalDatasourceImpl(Get.find()),
    );

    Get.lazyPut<UserRemoteDatasource>(
      () => UserRemoteDatasourceImpl(Get.find()),
    );

    // Repository
    Get.lazyPut<UserRepository>(
      () => UserRepositoryImpl(Get.find(), Get.find()),
    );

    // Usecases
    Get.lazyPut(() => GetUserUsecase(Get.find()));
    Get.lazyPut(() => GetAllUsersUsecase(Get.find()));
    Get.lazyPut(() => CreateUserUsecase(Get.find()));
    Get.lazyPut(() => DeleteUserUsecase(Get.find()));

    // Controller
    Get.lazyPut(() => UserController(Get.find(), Get.find(), Get.find(), Get.find()));
  }
}
```

### Page/View

```dart
// lib/presentation/pages/user_list_page.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/user_controller.dart';
import '../widgets/user_tile.dart';

class UserListPage extends StatelessWidget {
  const UserListPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Users'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => Get.find<UserController>().fetchAllUsers(),
          ),
        ],
      ),
      body: GetBuilder<UserController>(
        builder: (controller) => Obx(
          () {
            if (controller.isLoading.value) {
              return const Center(child: CircularProgressIndicator());
            }

            if (controller.error.value != null) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('Error: ${controller.error.value}'),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: controller.fetchAllUsers,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              );
            }

            if (controller.users.isEmpty) {
              return const Center(child: Text('No users found'));
            }

            return ListView.builder(
              itemCount: controller.users.length,
              itemBuilder: (context, index) {
                final user = controller.users[index];
                return UserTile(
                  user: user,
                  onDelete: () => controller.deleteUserById(user.id),
                );
              },
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Get.toNamed('/user/create'),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## Data Flow Summary

```
User interaction (UI)
    ↓
Controller.method()
    ↓
Usecase.call()
    ↓
Repository interface
    ↓
Repository implementation
    ├─ LocalDatasource (SQLite)
    └─ RemoteDatasource (API)
    ↓
Result wrapper
    ↓
Controller updates .obs
    ↓
GetBuilder/Obx rebuilds UI
```

## Related Documentation
- Clean Architecture Guide: `system/clean_architecture_guide.md`
- Feature Module Template: `feature_module_template.md`
- Code Standards: `system/code_standards.md`
