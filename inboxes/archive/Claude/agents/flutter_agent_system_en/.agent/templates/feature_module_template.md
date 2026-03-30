# Feature Module Implementation Template

## Overview
This template guides you through creating a new feature module following Modular + Clean Architecture patterns.

## Pre-Implementation Checklist
- [ ] Feature is defined and requirements are clear
- [ ] You've read Clean Architecture & Modular Architecture guides
- [ ] You've identified shared dependencies
- [ ] You've planned entity structure
- [ ] You've identified API endpoints (if applicable)

## Step 1: Create Directory Structure

```bash
# Create feature directory
mkdir -p features/[feature_name]/lib/{data,domain,presentation}
mkdir -p features/[feature_name]/test/{unit,widget}

# Create domain layer
mkdir -p features/[feature_name]/lib/domain/{entities,repositories,usecases}

# Create data layer
mkdir -p features/[feature_name]/lib/data/{datasources,models,repositories}
mkdir -p features/[feature_name]/lib/data/datasources/{local,remote}

# Create presentation layer
mkdir -p features/[feature_name]/lib/presentation/{pages,widgets,controllers,bindings}
```

## Step 2: Create pubspec.yaml

File: `features/[feature_name]/pubspec.yaml`

```yaml
name: [feature_name]
description: "[Feature description]"
version: 1.0.0

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: '>=3.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # Core
  get: ^4.6.5
  get_it: ^7.4.0
  injectable: ^2.1.0
  
  # Data
  dio: ^5.0.0
  drift: ^2.14.0
  sqlite3_flutter_libs: ^0.5.0
  
  # Utilities
  equatable: ^2.0.0
  uuid: ^3.0.0
  
  # Shared feature
  shared:
    path: ../shared

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  build_runner: ^2.4.0
  drift_dev: ^2.14.0
  injectable_generator: ^2.1.0
  mockito: ^5.4.0
```

## Step 3: Create Domain Layer

### 3.1 Entity Definition

File: `lib/domain/entities/[entity_name].dart`

```dart
import 'package:equatable/equatable.dart';

class [EntityName] extends Equatable {
  final String id;
  final String name;
  final String description;
  final DateTime createdAt;
  final DateTime updatedAt;
  
  const [EntityName]({
    required this.id,
    required this.name,
    required this.description,
    required this.createdAt,
    required this.updatedAt,
  });
  
  @override
  List<Object?> get props => [id, name, description, createdAt, updatedAt];
}
```

### 3.2 Repository Interface

File: `lib/domain/repositories/[entity_name]_repository.dart`

```dart
import 'package:shared/shared.dart';

abstract class [EntityName]Repository {
  Future<Result<[EntityName], Exception>> get[EntityName](String id);
  Future<Result<List<[EntityName]>, Exception>> getAll[EntityName]s();
  Future<Result<String, Exception>> create[EntityName]([EntityName] entity);
  Future<Result<void, Exception>> update[EntityName]([EntityName] entity);
  Future<Result<void, Exception>> delete[EntityName](String id);
}
```

### 3.3 Use Cases

File: `lib/domain/usecases/get_[entity_name]_usecase.dart`

```dart
import 'package:shared/shared.dart';
import '../entities/[entity_name].dart';
import '../repositories/[entity_name]_repository.dart';

class Get[EntityName]Usecase {
  final [EntityName]Repository repository;
  
  Get[EntityName]Usecase(this.repository);
  
  Future<Result<[EntityName], Exception>> call(String id) {
    return repository.get[EntityName](id);
  }
}
```

File: `lib/domain/usecases/get_all_[entity_name]s_usecase.dart`

```dart
import 'package:shared/shared.dart';
import '../entities/[entity_name].dart';
import '../repositories/[entity_name]_repository.dart';

class GetAll[EntityName]sUsecase {
  final [EntityName]Repository repository;
  
  GetAll[EntityName]sUsecase(this.repository);
  
  Future<Result<List<[EntityName]>, Exception>> call() {
    return repository.getAll[EntityName]s();
  }
}
```

## Step 4: Create Data Layer

### 4.1 Model (DTO)

File: `lib/data/models/[entity_name]_model.dart`

```dart
import '../../domain/entities/[entity_name].dart';

class [EntityName]Model extends [EntityName] {
  const [EntityName]Model({
    required String id,
    required String name,
    required String description,
    required DateTime createdAt,
    required DateTime updatedAt,
  }) : super(
    id: id,
    name: name,
    description: description,
    createdAt: createdAt,
    updatedAt: updatedAt,
  );
  
  factory [EntityName]Model.fromJson(Map<String, dynamic> json) {
    return [EntityName]Model(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String,
      createdAt: DateTime.parse(json['createdAt'] as String),
      updatedAt: DateTime.parse(json['updatedAt'] as String),
    );
  }
  
  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'description': description,
    'createdAt': createdAt.toIso8601String(),
    'updatedAt': updatedAt.toIso8601String(),
  };
  
  factory [EntityName]Model.fromEntity([EntityName] entity) {
    return [EntityName]Model(
      id: entity.id,
      name: entity.name,
      description: entity.description,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
    );
  }
}
```

### 4.2 Local Datasource

File: `lib/data/datasources/local/[entity_name]_local_datasource.dart`

```dart
import 'package:core/core.dart';
import '../models/[entity_name]_model.dart';

abstract class [EntityName]LocalDatasource {
  Future<List<[EntityName]Model>> getAll();
  Future<[EntityName]Model?> getById(String id);
  Future<void> save(List<[EntityName]Model> items);
  Future<void> delete(String id);
}

@LazySingleton(as: [EntityName]LocalDatasource)
class [EntityName]LocalDatasourceImpl implements [EntityName]LocalDatasource {
  final DatabaseService databaseService;
  
  [EntityName]LocalDatasourceImpl(this.databaseService);
  
  @override
  Future<List<[EntityName]Model>> getAll() async {
    // Query from Drift database
    final items = await databaseService.getAll[EntityName]s();
    return items.map((item) => [EntityName]Model.fromJson(item.toJson())).toList();
  }
  
  @override
  Future<[EntityName]Model?> getById(String id) async {
    // Query from Drift database
    return null;
  }
  
  @override
  Future<void> save(List<[EntityName]Model> items) async {
    // Save to Drift database
  }
  
  @override
  Future<void> delete(String id) async {
    // Delete from Drift database
  }
}
```

### 4.3 Remote Datasource

File: `lib/data/datasources/remote/[entity_name]_remote_datasource.dart`

```dart
import 'package:dio/dio.dart';
import '../models/[entity_name]_model.dart';

abstract class [EntityName]RemoteDatasource {
  Future<List<[EntityName]Model>> fetchAll();
  Future<[EntityName]Model> fetchById(String id);
  Future<[EntityName]Model> create([EntityName]Model item);
  Future<void> update([EntityName]Model item);
  Future<void> delete(String id);
}

class [EntityName]RemoteDatasourceImpl implements [EntityName]RemoteDatasource {
  final Dio dio;
  static const baseUrl = '/api/[entity_name]s';
  
  [EntityName]RemoteDatasourceImpl(this.dio);
  
  @override
  Future<List<[EntityName]Model>> fetchAll() async {
    try {
      final response = await dio.get(baseUrl);
      return (response.data as List)
        .map((item) => [EntityName]Model.fromJson(item as Map<String, dynamic>))
        .toList();
    } catch (e) {
      throw Exception('Failed to fetch [entity_name]s: $e');
    }
  }
  
  @override
  Future<[EntityName]Model> fetchById(String id) async {
    try {
      final response = await dio.get('$baseUrl/$id');
      return [EntityName]Model.fromJson(response.data);
    } catch (e) {
      throw Exception('Failed to fetch [entity_name]: $e');
    }
  }
  
  @override
  Future<[EntityName]Model> create([EntityName]Model item) async {
    try {
      final response = await dio.post(baseUrl, data: item.toJson());
      return [EntityName]Model.fromJson(response.data);
    } catch (e) {
      throw Exception('Failed to create [entity_name]: $e');
    }
  }
  
  @override
  Future<void> update([EntityName]Model item) async {
    try {
      await dio.put('$baseUrl/${item.id}', data: item.toJson());
    } catch (e) {
      throw Exception('Failed to update [entity_name]: $e');
    }
  }
  
  @override
  Future<void> delete(String id) async {
    try {
      await dio.delete('$baseUrl/$id');
    } catch (e) {
      throw Exception('Failed to delete [entity_name]: $e');
    }
  }
}
```

### 4.4 Repository Implementation

File: `lib/data/repositories/[entity_name]_repository_impl.dart`

```dart
import 'package:shared/shared.dart';
import '../../domain/entities/[entity_name].dart';
import '../../domain/repositories/[entity_name]_repository.dart';
import '../datasources/local/[entity_name]_local_datasource.dart';
import '../datasources/remote/[entity_name]_remote_datasource.dart';

@LazySingleton(as: [EntityName]Repository)
class [EntityName]RepositoryImpl implements [EntityName]Repository {
  final [EntityName]LocalDatasource localDatasource;
  final [EntityName]RemoteDatasource remoteDatasource;
  
  [EntityName]RepositoryImpl(this.localDatasource, this.remoteDatasource);
  
  @override
  Future<Result<[EntityName], Exception>> get[EntityName](String id) async {
    try {
      // Try local first
      final local = await localDatasource.getById(id);
      if (local != null) {
        return Result.success(local);
      }
      
      // Fetch from remote
      final remote = await remoteDatasource.fetchById(id);
      await localDatasource.save([remote]);
      
      return Result.success(remote);
    } catch (e) {
      return Result.failure(Exception(e.toString()));
    }
  }
  
  @override
  Future<Result<List<[EntityName]>, Exception>> getAll[EntityName]s() async {
    try {
      final items = await localDatasource.getAll();
      return Result.success(items);
    } catch (e) {
      return Result.failure(Exception(e.toString()));
    }
  }
  
  @override
  Future<Result<String, Exception>> create[EntityName]([EntityName] entity) async {
    try {
      final model = [EntityName]Model.fromEntity(entity);
      final result = await remoteDatasource.create(model);
      await localDatasource.save([result]);
      return Result.success(result.id);
    } catch (e) {
      return Result.failure(Exception(e.toString()));
    }
  }
  
  @override
  Future<Result<void, Exception>> update[EntityName]([EntityName] entity) async {
    try {
      final model = [EntityName]Model.fromEntity(entity);
      await remoteDatasource.update(model);
      await localDatasource.save([model]);
      return Result.success(null);
    } catch (e) {
      return Result.failure(Exception(e.toString()));
    }
  }
  
  @override
  Future<Result<void, Exception>> delete[EntityName](String id) async {
    try {
      await remoteDatasource.delete(id);
      await localDatasource.delete(id);
      return Result.success(null);
    } catch (e) {
      return Result.failure(Exception(e.toString()));
    }
  }
}
```

## Step 5: Create Presentation Layer

### 5.1 GetX Controller

File: `lib/presentation/controllers/[entity_name]_controller.dart`

```dart
import 'package:get/get.dart';
import 'package:shared/shared.dart';
import '../../domain/entities/[entity_name].dart';
import '../../domain/usecases/get_[entity_name]_usecase.dart';
import '../../domain/usecases/get_all_[entity_name]s_usecase.dart';

class [EntityName]Controller extends GetxController {
  final Get[EntityName]Usecase get[EntityName];
  final GetAll[EntityName]sUsecase getAll[EntityName]s;
  
  [EntityName]Controller(this.get[EntityName], this.getAll[EntityName]s);
  
  final items = <[EntityName]>[].obs;
  final selectedItem = Rxn<[EntityName]>();
  final isLoading = false.obs;
  final errorMessage = ''.obs;
  
  @override
  void onInit() {
    loadAll();
    super.onInit();
  }
  
  Future<void> loadAll() async {
    isLoading.value = true;
    errorMessage.value = '';
    
    final result = await getAll[EntityName]s();
    result.fold(
      (data) => items.value = data,
      (error) => errorMessage.value = error.toString(),
    );
    
    isLoading.value = false;
  }
  
  Future<void> loadItem(String id) async {
    isLoading.value = true;
    errorMessage.value = '';
    
    final result = await get[EntityName](id);
    result.fold(
      (data) => selectedItem.value = data,
      (error) => errorMessage.value = error.toString(),
    );
    
    isLoading.value = false;
  }
}
```

### 5.2 GetX Binding

File: `lib/presentation/bindings/[entity_name]_binding.dart`

```dart
import 'package:get/get.dart';
import '../../data/repositories/[entity_name]_repository_impl.dart';
import '../../data/datasources/local/[entity_name]_local_datasource.dart';
import '../../data/datasources/remote/[entity_name]_remote_datasource.dart';
import '../../domain/repositories/[entity_name]_repository.dart';
import '../../domain/usecases/get_[entity_name]_usecase.dart';
import '../../domain/usecases/get_all_[entity_name]s_usecase.dart';
import '../controllers/[entity_name]_controller.dart';

class [EntityName]Binding extends Bindings {
  @override
  void dependencies() {
    // Datasources
    Get.lazyPut<[EntityName]LocalDatasource>(
      () => [EntityName]LocalDatasourceImpl(Get.find()),
    );
    Get.lazyPut<[EntityName]RemoteDatasource>(
      () => [EntityName]RemoteDatasourceImpl(Get.find()),
    );
    
    // Repository
    Get.lazyPut<[EntityName]Repository>(
      () => [EntityName]RepositoryImpl(Get.find(), Get.find()),
    );
    
    // Usecases
    Get.lazyPut(() => Get[EntityName]Usecase(Get.find()));
    Get.lazyPut(() => GetAll[EntityName]sUsecase(Get.find()));
    
    // Controller
    Get.lazyPut(() => [EntityName]Controller(Get.find(), Get.find()));
  }
}
```

### 5.3 Page/View

File: `lib/presentation/pages/[entity_name]_list_page.dart`

```dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/[entity_name]_controller.dart';

class [EntityName]ListPage extends StatelessWidget {
  const [EntityName]ListPage({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return GetBuilder<[EntityName]Controller>(
      builder: (controller) => Scaffold(
        appBar: AppBar(title: const Text('[EntityName]s')),
        body: Obx(
          () {
            if (controller.isLoading.value) {
              return const Center(child: CircularProgressIndicator());
            }
            
            if (controller.errorMessage.value.isNotEmpty) {
              return Center(child: Text(controller.errorMessage.value));
            }
            
            if (controller.items.isEmpty) {
              return const Center(child: Text('No items'));
            }
            
            return ListView.builder(
              itemCount: controller.items.length,
              itemBuilder: (context, index) {
                final item = controller.items[index];
                return ListTile(
                  title: Text(item.name),
                  subtitle: Text(item.description),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
```

## Step 6: Create Public Export File

File: `lib/[feature_name].dart`

```dart
// Domain
export 'domain/entities/[entity_name].dart';
export 'domain/repositories/[entity_name]_repository.dart';
export 'domain/usecases/get_[entity_name]_usecase.dart';

// Presentation
export 'presentation/pages/[entity_name]_list_page.dart';
export 'presentation/controllers/[entity_name]_controller.dart';
export 'presentation/bindings/[entity_name]_binding.dart';
```

## Step 7: Update Main App Routes

File: `lib/routes/app_routes.dart`

```dart
import 'package:[feature_name]/[feature_name].dart';

abstract class AppRoutes {
  static const [FEATURE_NAME]_ROUTE = '/[feature_name]';
}

class AppPages {
  static final pages = [
    GetPage(
      name: AppRoutes.[FEATURE_NAME]_ROUTE,
      page: () => const [EntityName]ListPage(),
      binding: [EntityName]Binding(),
    ),
  ];
}
```

## Step 8: Testing

Create unit tests in `test/unit/domain/usecases/get_[entity_name]_usecase_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:[feature_name]/domain/entities/[entity_name].dart';
import 'package:[feature_name]/domain/repositories/[entity_name]_repository.dart';
import 'package:[feature_name]/domain/usecases/get_[entity_name]_usecase.dart';
import 'package:shared/shared.dart';

class Mock[EntityName]Repository extends Mock implements [EntityName]Repository {}

void main() {
  group('Get[EntityName]Usecase', () {
    late Get[EntityName]Usecase usecase;
    late Mock[EntityName]Repository mockRepository;
    
    setUp(() {
      mockRepository = Mock[EntityName]Repository();
      usecase = Get[EntityName]Usecase(mockRepository);
    });
    
    const testId = 'test-id';
    const test[EntityName] = [EntityName](
      id: testId,
      name: 'Test Name',
      description: 'Test Description',
      createdAt: null,
      updatedAt: null,
    );
    
    test('should return [EntityName] when repository call is successful', () async {
      // Arrange
      when(mockRepository.get[EntityName](testId))
        .thenAnswer((_) async => Result.success(test[EntityName]));
      
      // Act
      final result = await usecase(testId);
      
      // Assert
      expect(result.isSuccess, true);
      verify(mockRepository.get[EntityName](testId)).called(1);
    });
  });
}
```

## Step 9: Register in DI Container

Update `lib/core/di/injectable_config.dart`:

```dart
// Add to imports
import 'package:[feature_name]/data/datasources/local/[entity_name]_local_datasource.dart';
import 'package:[feature_name]/data/datasources/remote/[entity_name]_remote_datasource.dart';
import 'package:[feature_name]/domain/repositories/[entity_name]_repository.dart';

// Register in setupServiceLocator()
void setupServiceLocator() {
  // [FeatureName]
  getIt.registerSingleton<[EntityName]LocalDatasource>(
    [EntityName]LocalDatasourceImpl(getIt()),
  );
  
  getIt.registerSingleton<[EntityName]RemoteDatasource>(
    [EntityName]RemoteDatasourceImpl(getIt()),
  );
  
  getIt.registerSingleton<[EntityName]Repository>(
    [EntityName]RepositoryImpl(getIt(), getIt()),
  );
}
```

## Checklist After Implementation

- [ ] All files created following naming conventions
- [ ] Domain layer has no dependencies
- [ ] Data layer implements domain interfaces
- [ ] Presentation layer uses only GetX
- [ ] Entity, Model, and DTO are properly defined
- [ ] Public export file exports all necessary classes
- [ ] Unit tests cover usecases
- [ ] Widget tests cover pages
- [ ] DI is properly configured
- [ ] Routes are added to main app
- [ ] Code follows analysis_options.yaml
- [ ] Code formatted with dart format
- [ ] No linter warnings

## Related Documentation
- Clean Architecture Guide: `system/clean_architecture_guide.md`
- Modular Architecture: `system/modular_architecture_guide.md`
- Code Standards: `system/code_standards.md`
