# Modular Architecture Guide

## Overview

Modular Architecture breaks the application into independent, self-contained feature modules. Each module has its own:
- Dependencies (`pubspec.yaml`)
- Code structure
- Business logic
- UI components

This approach enables:
- Parallel development
- Reduced merge conflicts
- Independent testing
- Better code organization
- Easier feature toggling

## Feature Module Structure

### Basic Structure
```
features/
├── [feature_name]/
│   ├── lib/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   ├── models/
│   │   │   └── repositories/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── repositories/
│   │   │   └── usecases/
│   │   ├── presentation/
│   │   │   ├── pages/
│   │   │   ├── widgets/
│   │   │   ├── controllers/
│   │   │   └── bindings/
│   │   └── [feature_name].dart  # Public exports
│   └── pubspec.yaml
└── shared/                        # Shared between features
    ├── lib/
    │   ├── domain/
    │   ├── data/
    │   └── presentation/
    └── pubspec.yaml
```

## Creating a New Feature Module

### Step 1: Create Directory Structure
```bash
mkdir -p features/[feature_name]/lib/{data,domain,presentation}
```

### Step 2: Create pubspec.yaml
```yaml
name: [feature_name]
version: 0.1.0

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
  
  # Shared code
  shared: # reference to shared feature
    path: ../shared

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.0
  drift_dev: ^2.14.0
  injectable_generator: ^2.1.0
```

### Step 3: Create Public Export File
Create `lib/[feature_name].dart`:
```dart
// Domain
export 'domain/entities/user.dart';
export 'domain/repositories/user_repository.dart';
export 'domain/usecases/get_user_usecase.dart';

// Presentation
export 'presentation/controllers/user_controller.dart';
export 'presentation/pages/user_page.dart';
```

### Step 4: Implement Clean Architecture Layers

**Domain Layer** (No dependencies):
```dart
// domain/entities/user.dart
class User {
  final String id;
  final String name;
  
  const User({required this.id, required this.name});
}

// domain/repositories/user_repository.dart
abstract class UserRepository {
  Future<Result<User, Exception>> getUser(String id);
}

// domain/usecases/get_user_usecase.dart
class GetUserUsecase {
  final UserRepository repository;
  
  GetUserUsecase(this.repository);
  
  Future<Result<User, Exception>> call(String id) {
    return repository.getUser(id);
  }
}
```

**Data Layer** (Implements domain):
```dart
// data/models/user_model.dart
class UserModel extends User {
  UserModel({required String id, required String name})
    : super(id: id, name: name);
  
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      name: json['name'],
    );
  }
}

// data/repositories/user_repository_impl.dart
class UserRepositoryImpl implements UserRepository {
  final UserLocalDatasource localDatasource;
  
  UserRepositoryImpl(this.localDatasource);
  
  @override
  Future<Result<User, Exception>> getUser(String id) async {
    try {
      final user = await localDatasource.getUser(id);
      return Result.success(user);
    } catch (e) {
      return Result.failure(Exception(e.toString()));
    }
  }
}
```

**Presentation Layer** (UI and state):
```dart
// presentation/controllers/user_controller.dart
class UserController extends GetxController {
  final GetUserUsecase getUser;
  
  UserController(this.getUser);
  
  final user = Rxn<User>();
  final isLoading = false.obs;
  
  Future<void> fetchUser(String id) async {
    isLoading.value = true;
    final result = await getUser(id);
    
    result.fold(
      (user) => this.user.value = user,
      (error) => Get.snackbar('Error', error.toString()),
    );
    
    isLoading.value = false;
  }
}

// presentation/pages/user_page.dart
class UserPage extends StatelessWidget {
  const UserPage({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return GetBuilder<UserController>(
      builder: (controller) {
        if (controller.isLoading.value) {
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }
        
        return Scaffold(
          appBar: AppBar(title: const Text('User')),
          body: Center(
            child: Text(controller.user.value?.name ?? 'No user'),
          ),
        );
      },
    );
  }
}

// presentation/bindings/user_binding.dart
class UserBinding extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => GetUserUsecase(Get.find()));
    Get.lazyPut(() => UserController(Get.find()));
  }
}
```

## Feature Communication

### Within Feature
Use local GetX controllers and services.

### Between Features
Use a shared event bus or navigation:

```dart
// Emit event
Get.find<EventBus>().emit('user_updated', userData);

// Listen
Get.find<EventBus>().on('user_updated', (data) {
  // Handle event
});
```

## Shared Feature Module

The `shared` module contains code used by multiple features:

```
features/shared/lib/
├── domain/
│   ├── entities/           # Common entities
│   ├── repositories/       # Interfaces
│   └── usecases/          # Common operations
├── data/
│   ├── datasources/       # Local/Remote shared
│   ├── models/            # Shared models
│   └── repositories/      # Implementations
└── presentation/
    ├── widgets/           # Reusable UI components
    ├── themes/            # Theme configuration
    └── mixins/            # UI mixins
```

## Dependency Injection Setup

Register each feature's dependencies:

```dart
// main.dart
void main() async {
  await setupServiceLocator();
  runApp(const MyApp());
}

Future<void> setupServiceLocator() async {
  // Shared
  _setupSharedDependencies();
  
  // Feature 1
  _setupFlashcardImportDependencies();
  
  // Feature 2
  _setupFlashcardViewerDependencies();
}

void _setupFlashcardImportDependencies() {
  Get.lazyPut(() => UserRepository(
    localDatasource: Get.find(),
  ));
  
  Get.lazyPut(() => GetUserUsecase(Get.find()));
  Get.lazyPut(() => UserController(Get.find()));
}
```

## Best Practices

1. **Independence**: Feature should not import from other features
2. **Public API**: Only export what's necessary through `[feature_name].dart`
3. **Shared Code**: Common code goes in `shared` feature
4. **Testing**: Each feature has independent tests
5. **Versioning**: Update `pubspec.yaml` version for breaking changes
6. **Documentation**: Document feature-specific setup in README

## Related Documentation
- Clean Architecture Guide: `system/clean_architecture_guide.md`
- Feature Module Template: `templates/feature_module_template.md`
- Adding New Feature SOP: `sops/adding_new_feature.md`
