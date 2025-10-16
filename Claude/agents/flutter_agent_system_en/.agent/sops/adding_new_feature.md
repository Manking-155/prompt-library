# SOP: Adding a New Feature Module

## Overview
This document outlines the standard procedure for adding a new feature to the Flutter application following Modular + Clean Architecture.

## Prerequisites
- Feature requirements are clearly defined
- You've reviewed the Feature Module Template
- You understand Clean Architecture principles
- You have write access to the repository

## Step-by-Step Process

### Phase 1: Planning & Setup

#### 1.1 Define Feature Scope
- Document what the feature does
- List primary entities and data models
- Identify API endpoints needed
- Note any shared dependencies

#### 1.2 Create Feature Directory
```bash
cd features
mkdir -p [feature_name]/lib/{data,domain,presentation}
mkdir -p [feature_name]/test/{unit,widget}
```

#### 1.3 Create pubspec.yaml
Copy the template and update:
- Feature name and description
- Version number (start with 1.0.0)
- Add only necessary dependencies

### Phase 2: Domain Layer Implementation

#### 2.1 Create Entities
Create `lib/domain/entities/[entity_name].dart`:
- Define immutable data classes
- Use `Equatable` for equality comparison
- Document each property

```dart
class User extends Equatable {
  final String id;
  final String name;
  
  const User({required this.id, required this.name});
  
  @override
  List<Object?> get props => [id, name];
}
```

#### 2.2 Define Repository Interfaces
Create `lib/domain/repositories/[entity_name]_repository.dart`:
- Define abstract methods
- Use Result wrapper for error handling
- Document return types

```dart
abstract class UserRepository {
  Future<Result<User, Exception>> getUser(String id);
  Future<Result<List<User>, Exception>> getAllUsers();
  Future<Result<String, Exception>> createUser(User user);
}
```

#### 2.3 Implement Use Cases
Create `lib/domain/usecases/[usecase_name]_usecase.dart`:
- One usecase per operation
- Inject repository
- Keep logic simple

```dart
class GetUserUsecase {
  final UserRepository repository;
  
  GetUserUsecase(this.repository);
  
  Future<Result<User, Exception>> call(String id) {
    return repository.getUser(id);
  }
}
```

### Phase 3: Data Layer Implementation

#### 3.1 Create Models (DTOs)
Create `lib/data/models/[entity_name]_model.dart`:
- Extend domain entities
- Implement JSON serialization
- Add factory constructors for conversion

```dart
class UserModel extends User {
  const UserModel({required String id, required String name})
    : super(id: id, name: name);
  
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(id: json['id'], name: json['name']);
  }
  
  Map<String, dynamic> toJson() => {'id': id, 'name': name};
}
```

#### 3.2 Implement Local Datasource
Create `lib/data/datasources/local/[entity_name]_local_datasource.dart`:
- Interface for local storage operations
- Implementation using DatabaseService
- Handle database queries

#### 3.3 Implement Remote Datasource
Create `lib/data/datasources/remote/[entity_name]_remote_datasource.dart`:
- Interface for API operations
- Implementation using Dio
- Handle API errors gracefully

#### 3.4 Implement Repository
Create `lib/data/repositories/[entity_name]_repository_impl.dart`:
- Implement domain repository interface
- Coordinate local and remote datasources
- Implement offline-first strategy

### Phase 4: Presentation Layer Implementation

#### 4.1 Create GetX Controller
Create `lib/presentation/controllers/[entity_name]_controller.dart`:
- Inject usecases
- Define observable state
- Implement business logic handlers

#### 4.2 Create GetX Binding
Create `lib/presentation/bindings/[entity_name]_binding.dart`:
- Register all dependencies
- Use lazy loading where applicable
- Follow dependency order

#### 4.3 Create Pages/Widgets
Create `lib/presentation/pages/[entity_name]_page.dart`:
- Use stateless widgets
- Integrate with controller
- Use Obx for reactive updates

### Phase 5: Integration

#### 5.1 Create Public Export File
Create `lib/[feature_name].dart`:
- Export only public APIs
- Hide internal implementation

```dart
export 'domain/entities/user.dart';
export 'domain/repositories/user_repository.dart';
export 'presentation/pages/user_page.dart';
```

#### 5.2 Update Main App Routes
Edit `lib/routes/app_routes.dart`:
- Add route constants
- Add page configuration with binding

```dart
static const USER_ROUTE = '/user';

GetPage(
  name: AppRoutes.USER_ROUTE,
  page: () => const UserPage(),
  binding: UserBinding(),
),
```

#### 5.3 Add Feature Dependency
Edit `pubspec.yaml`:
- Add feature to path dependency if needed

### Phase 6: Testing

#### 6.1 Write Unit Tests
Create `test/unit/domain/usecases/[usecase_name]_test.dart`:
- Test each usecase
- Mock repositories
- Cover success and error cases

#### 6.2 Write Widget Tests
Create `test/widget/presentation/pages/[entity_name]_page_test.dart`:
- Test page rendering
- Test user interactions
- Test controller integration

#### 6.3 Write Integration Tests (Optional)
Create `test/integration/[feature_name]_integration_test.dart`:
- Test end-to-end flows
- Test with real or mock backend

### Phase 7: Code Quality

#### 7.1 Run Linter
```bash
dart analyze lib
```

#### 7.2 Format Code
```bash
dart format lib
```

#### 7.3 Run Tests
```bash
flutter test
```

#### 7.4 Check for Issues
```bash
flutter analyze
```

### Phase 8: Documentation

#### 8.1 Create Feature README
Create `features/[feature_name]/README.md`:
- Feature description
- Dependencies
- Key components
- Setup instructions

#### 8.2 Update Agent Docs
Update `.agent/system/` and `.agent/templates/`:
- Document any custom patterns used
- Update examples if needed

### Phase 9: Review & Merge

#### 9.1 Code Review Checklist
- [ ] All files follow naming conventions
- [ ] Domain layer has no dependencies
- [ ] Data layer implements domain interfaces
- [ ] Presentation layer uses GetX correctly
- [ ] Proper error handling with Result wrapper
- [ ] All tests passing
- [ ] Code formatted and linted
- [ ] Documentation updated

#### 9.2 Git Commit
```bash
git add .
git commit -m "feat: add [feature_name] module

- Implement domain entities and usecases
- Add data layer with local and remote datasources
- Create presentation layer with GetX controller
- Add unit and widget tests"
```

#### 9.3 Create Pull Request
- Link to requirements/issue
- Describe what was implemented
- Request review from team

## Quick Reference

### File Structure Created
```
features/[feature_name]/
├── lib/
│   ├── data/
│   │   ├── datasources/local/[entity]_local_datasource.dart
│   │   ├── datasources/remote/[entity]_remote_datasource.dart
│   │   ├── models/[entity]_model.dart
│   │   └── repositories/[entity]_repository_impl.dart
│   ├── domain/
│   │   ├── entities/[entity].dart
│   │   ├── repositories/[entity]_repository.dart
│   │   └── usecases/[usecase]_usecase.dart
│   ├── presentation/
│   │   ├── bindings/[entity]_binding.dart
│   │   ├── controllers/[entity]_controller.dart
│   │   ├── pages/[entity]_page.dart
│   │   └── widgets/[entity]_widget.dart
│   └── [feature_name].dart
├── test/
│   ├── unit/
│   └── widget/
├── pubspec.yaml
└── README.md
```

### Common Commands
```bash
# Run tests for feature
flutter test features/[feature_name]

# Generate code
flutter pub run build_runner build

# Format code
dart format features/[feature_name]

# Analyze code
dart analyze features/[feature_name]

# Watch for changes
flutter pub run build_runner watch
```

## Troubleshooting

### Build Issues
```bash
# Clean build
flutter clean
flutter pub get
flutter pub run build_runner clean
flutter pub run build_runner build
```

### Import Errors
- Ensure pubspec.yaml is in features/[feature_name]/
- Check path dependency configuration
- Verify export file includes all necessary classes

### Test Failures
- Check mock setup
- Verify repository interfaces match implementations
- Ensure dependencies are properly injected

## Related Documentation
- Feature Module Template: `templates/feature_module_template.md`
- Clean Architecture Guide: `system/clean_architecture_guide.md`
- Modular Architecture: `system/modular_architecture_guide.md`
- Dependency Injection SOP: `sops/dependency_injection.md`
