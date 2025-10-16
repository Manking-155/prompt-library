# SOP: Adding New Feature Module

## Overview

This Standard Operating Procedure (SOP) outlines the step-by-step process for adding a new feature module to our Flutter application following the Modular + Clean Architecture pattern.

## Prerequisites

- Flutter SDK installed
- Project cloned and set up
- Understanding of Clean Architecture and Modular Architecture
- Access to project repository
- Required permissions to create new files and directories

## Step-by-Step Process

### Phase 1: Planning and Setup

#### 1.1 Feature Analysis
- [ ] Define feature requirements and user stories
- [ ] Identify data models and entities needed
- [ ] Plan API endpoints (if applicable)
- [ ] Identify navigation routes
- [ ] Determine dependencies on other modules

#### 1.2 Create Feature Directory Structure
```bash
# Navigate to features directory
cd features

# Create new feature directory
mkdir feature_name
cd feature_name

# Create subdirectories
mkdir -p lib/{data/{datasources/{local,remote},models,repositories,mappers},domain/{entities,usecases,repositories},presentation/{controllers,views,widgets}}
mkdir -p test/{unit/{usecases,repositories},widget/{widgets},integration}
```

### Phase 2: Domain Layer Implementation

#### 2.1 Create Entity
Create file: `lib/domain/entities/feature_entity.dart`
```dart
import 'package:equatable/equatable.dart';

class FeatureEntity extends Equatable {
  final String id;
  final String title;
  final String description;
  final DateTime createdAt;
  final DateTime updatedAt;

  const FeatureEntity({
    required this.id,
    required this.title,
    required this.description,
    required this.createdAt,
    required this.updatedAt,
  });

  // Business logic methods
  bool get isValid => title.isNotEmpty && description.isNotEmpty;

  @override
  List<Object?> get props => [id, title, description, createdAt, updatedAt];
}
```

#### 2.2 Create Repository Interface
Create file: `lib/domain/repositories/feature_repository.dart`
```dart
import 'package:dartz/dartz.dart';
import '../entities/feature_entity.dart';
import '../../shared/failures/failure.dart';

abstract class FeatureRepository {
  Future<Either<Failure, List<FeatureEntity>>> getAllFeatures();
  Future<Either<Failure, FeatureEntity>> getFeatureById(String id);
  Future<Either<Failure, FeatureEntity>> createFeature(FeatureEntity feature);
  Future<Either<Failure, FeatureEntity>> updateFeature(FeatureEntity feature);
  Future<Either<Failure, void>> deleteFeature(String id);
}
```

#### 2.3 Create Use Cases
Create file: `lib/domain/usecases/get_feature.dart`
```dart
import 'package:dartz/dartz.dart';
import '../entities/feature_entity.dart';
import '../repositories/feature_repository.dart';
import '../../shared/failures/failure.dart';

class GetFeatureUseCase {
  final FeatureRepository _repository;

  GetFeatureUseCase(this._repository);

  Future<Either<Failure, FeatureEntity>> execute(String featureId) async {
    if (featureId.isEmpty) {
      return const Left(ValidationFailure('Feature ID cannot be empty'));
    }
    return await _repository.getFeatureById(featureId);
  }
}
```

Repeat for other use cases (create, update, delete, get all).

### Phase 3: Data Layer Implementation

#### 3.1 Create Data Models
Create file: `lib/data/models/feature_model.dart`
```dart
import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/feature_entity.dart';

part 'feature_model.g.dart';

@JsonSerializable()
class FeatureModel {
  final String id;
  final String title;
  final String description;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  @JsonKey(name: 'updated_at')
  final DateTime updatedAt;

  FeatureModel({
    required this.id,
    required this.title,
    required this.description,
    required this.createdAt,
    required this.updatedAt,
  });

  factory FeatureModel.fromJson(Map<String, dynamic> json) =>
      _$FeatureModelFromJson(json);

  Map<String, dynamic> toJson() => _$FeatureModelToJson(this);

  FeatureEntity toEntity() {
    return FeatureEntity(
      id: id,
      title: title,
      description: description,
      createdAt: createdAt,
      updatedAt: updatedAt,
    );
  }

  factory FeatureModel.fromEntity(FeatureEntity entity) {
    return FeatureModel(
      id: entity.id,
      title: entity.title,
      description: entity.description,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
    );
  }
}
```

#### 3.2 Create Data Sources
Create file: `lib/data/datasources/remote/feature_remote_datasource.dart`
```dart
import 'package:dartz/dartz.dart';
import '../../models/feature_model.dart';
import '../../../shared/failures/failure.dart';

abstract class FeatureRemoteDataSource {
  Future<Either<Failure, List<FeatureModel>>> getAllFeatures();
  Future<Either<Failure, FeatureModel>> getFeatureById(String id);
  Future<Either<Failure, FeatureModel>> createFeature(FeatureModel feature);
  Future<Either<Failure, FeatureModel>> updateFeature(FeatureModel feature);
  Future<Either<Failure, void>> deleteFeature(String id);
}
```

Create file: `lib/data/datasources/remote/feature_remote_datasource_impl.dart`
```dart
import 'package:dartz/dartz.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'feature_remote_datasource.dart';
import '../../models/feature_model.dart';
import '../../../shared/failures/failure.dart';

class FeatureRemoteDataSourceImpl implements FeatureRemoteDataSource {
  final http.Client _client;
  final String _baseUrl;

  FeatureRemoteDataSourceImpl(this._client, this._baseUrl);

  @override
  Future<Either<Failure, List<FeatureModel>>> getAllFeatures() async {
    try {
      final response = await _client.get(
        Uri.parse('$_baseUrl/features'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> jsonList = json.decode(response.body);
        final features = jsonList
            .map((json) => FeatureModel.fromJson(json))
            .toList();
        return Right(features);
      } else {
        return Left(ServerFailure('Failed to load features'));
      }
    } catch (e) {
      return Left(NetworkFailure('Network error: $e'));
    }
  }

  // Implement other methods similarly...
}
```

#### 3.3 Create Repository Implementation
Create file: `lib/data/repositories/feature_repository_impl.dart`
```dart
import 'package:dartz/dartz.dart';
import '../../domain/entities/feature_entity.dart';
import '../../domain/repositories/feature_repository.dart';
import '../../domain/failures/failure.dart';
import '../datasources/remote/feature_remote_datasource.dart';
import '../datasources/local/feature_local_datasource.dart';
import '../models/feature_model.dart';

class FeatureRepositoryImpl implements FeatureRepository {
  final FeatureRemoteDataSource _remoteDataSource;
  final FeatureLocalDataSource _localDataSource;

  FeatureRepositoryImpl(
    this._remoteDataSource,
    this._localDataSource,
  );

  @override
  Future<Either<Failure, List<FeatureEntity>>> getAllFeatures() async {
    try {
      // Try local first (offline-first)
      final localFeatures = await _localDataSource.getAllFeatures();
      if (localFeatures.isNotEmpty) {
        return Right(localFeatures.map((f) => f.toEntity()).toList());
      }

      // Fallback to remote
      final remoteResult = await _remoteDataSource.getAllFeatures();

      return remoteResult.fold(
        (failure) => Left(failure),
        (features) async {
          // Cache locally
          await _localDataSource.saveFeatures(features);
          return Right(features.map((f) => f.toEntity()).toList());
        },
      );
    } catch (e) {
      return Left(CacheFailure('Failed to get features: $e'));
    }
  }

  // Implement other methods similarly...
}
```

### Phase 4: Presentation Layer Implementation

#### 4.1 Create Controller
Create file: `lib/presentation/controllers/feature_controller.dart`
```dart
import 'package:get/get.dart';
import 'package:dartz/dartz.dart';
import '../../domain/entities/feature_entity.dart';
import '../../domain/usecases/get_all_features.dart';
import '../../domain/usecases/get_feature.dart';
import '../../domain/usecases/create_feature.dart';
import '../../domain/failures/failure.dart';

class FeatureController extends GetxController {
  final GetAllFeaturesUseCase _getAllFeaturesUseCase;
  final GetFeatureUseCase _getFeatureUseCase;
  final CreateFeatureUseCase _createFeatureUseCase;

  // Reactive state
  final _features = <FeatureEntity>[].obs;
  final _selectedFeature = Rx<FeatureEntity?>(null);
  final _isLoading = false.obs;
  final _error = Rx<String?>(null);

  // Getters
  List<FeatureEntity> get features => _features;
  FeatureEntity? get selectedFeature => _selectedFeature.value;
  bool get isLoading => _isLoading.value;
  String? get error => _error.value;

  FeatureController({
    required GetAllFeaturesUseCase getAllFeaturesUseCase,
    required GetFeatureUseCase getFeatureUseCase,
    required CreateFeatureUseCase createFeatureUseCase,
  })  : _getAllFeaturesUseCase = getAllFeaturesUseCase,
        _getFeatureUseCase = getFeatureUseCase,
        _createFeatureUseCase = createFeatureUseCase;

  @override
  void onInit() {
    super.onInit();
    loadFeatures();
  }

  Future<void> loadFeatures() async {
    _setLoading(true);
    _clearError();

    final result = await _getAllFeaturesUseCase.execute();

    result.fold(
      (failure) => _setError(failure.message),
      (features) => _features.assignAll(features),
    );

    _setLoading(false);
  }

  Future<void> loadFeature(String featureId) async {
    _setLoading(true);
    _clearError();

    final result = await _getFeatureUseCase.execute(featureId);

    result.fold(
      (failure) => _setError(failure.message),
      (feature) => _selectedFeature.value = feature,
    );

    _setLoading(false);
  }

  Future<void> createFeature(FeatureEntity feature) async {
    _setLoading(true);
    _clearError();

    final result = await _createFeatureUseCase.execute(feature);

    result.fold(
      (failure) => _setError(failure.message),
      (createdFeature) {
        _features.add(createdFeature);
        Get.snackbar('Success', 'Feature created successfully');
        Get.back();
      },
    );

    _setLoading(false);
  }

  void selectFeature(FeatureEntity feature) {
    _selectedFeature.value = feature;
  }

  void clearSelectedFeature() {
    _selectedFeature.value = null;
  }

  Future<void> refresh() async {
    await loadFeatures();
  }

  void _setLoading(bool loading) {
    _isLoading.value = loading;
  }

  void _setError(String error) {
    _error.value = error;
    Get.snackbar('Error', error);
  }

  void _clearError() {
    _error.value = null;
  }
}
```

#### 4.2 Create Views
Create file: `lib/presentation/views/feature_list_view.dart`
```dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/feature_controller.dart';
import '../widgets/feature_card.dart';

class FeatureListView extends GetView<FeatureController> {
  const FeatureListView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Features'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: controller.refresh,
          ),
        ],
      ),
      body: Obx(
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
                  ElevatedButton(
                    onPressed: controller.refresh,
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          if (controller.features.isEmpty) {
            return const Center(child: Text('No features found'));
          }

          return ListView.builder(
            itemCount: controller.features.length,
            itemBuilder: (context, index) {
              final feature = controller.features[index];
              return FeatureCard(
                feature: feature,
                onTap: () => controller.selectFeature(feature),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Get.toNamed('/feature/create'),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

#### 4.3 Create Widgets
Create file: `lib/presentation/widgets/feature_card.dart`
```dart
import 'package:flutter/material.dart';
import '../../domain/entities/feature_entity.dart';

class FeatureCard extends StatelessWidget {
  final FeatureEntity feature;
  final VoidCallback? onTap;

  const FeatureCard({
    Key? key,
    required this.feature,
    this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(8),
      child: ListTile(
        title: Text(feature.title),
        subtitle: Text(feature.description),
        trailing: const Icon(Icons.arrow_forward_ios),
        onTap: onTap,
      ),
    );
  }
}
```

### Phase 5: Configuration and Integration

#### 5.1 Create pubspec.yaml
Create file: `pubspec.yaml`
```yaml
name: feature_name
description: New feature module

environment:
  sdk: '>=2.17.0 <3.0.0'
  flutter: ">=3.0.0"

dependencies:
  flutter:
    sdk: flutter

  # Core dependencies
  get: ^4.6.5
  get_it: ^7.2.0
  injectable: ^1.5.3
  dartz: ^0.10.1
  equatable: ^2.0.5
  json_annotation: ^4.8.1

  # Shared modules
  shared:
    path: ../shared

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.3.0
  injectable_generator: ^1.5.4
  json_serializable: ^6.7.1
  mockito: ^5.3.2
```

#### 5.2 Create Dependency Injection Module
Create file: `lib/data/di/injection.dart`
```dart
import 'package:injectable/injectable.dart';
import '../../domain/repositories/feature_repository.dart';
import '../../domain/usecases/get_all_features.dart';
import '../../domain/usecases/get_feature.dart';
import '../../domain/usecases/create_feature.dart';
import '../repositories/feature_repository_impl.dart';
import '../datasources/remote/feature_remote_datasource.dart';
import '../datasources/remote/feature_remote_datasource_impl.dart';
import '../datasources/local/feature_local_datasource.dart';
import '../datasources/local/feature_local_datasource_impl.dart';

@module
abstract class FeatureModule {
  // Data sources
  @singleton
  FeatureRemoteDataSource get featureRemoteDataSource =>
      FeatureRemoteDataSourceImpl(Get.find());

  @singleton
  FeatureLocalDataSource get featureLocalDataSource =>
      FeatureLocalDataSourceImpl(Get.find());

  // Repository
  @singleton
  FeatureRepository get featureRepository => FeatureRepositoryImpl(
        featureRemoteDataSource,
        featureLocalDataSource,
      );

  // Use cases
  @singleton
  GetAllFeaturesUseCase get getAllFeaturesUseCase =>
      GetAllFeaturesUseCase(featureRepository);

  @singleton
  GetFeatureUseCase get getFeatureUseCase =>
      GetFeatureUseCase(featureRepository);

  @singleton
  CreateFeatureUseCase get createFeatureUseCase =>
      CreateFeatureUseCase(featureRepository);
}
```

#### 5.3 Create Public API Export
Create file: `lib/feature_name.dart`
```dart
// Domain exports
export 'domain/entities/feature_entity.dart';
export 'domain/repositories/feature_repository.dart';
export 'domain/usecases/get_all_features.dart';
export 'domain/usecases/get_feature.dart';
export 'domain/usecases/create_feature.dart';

// Data exports
export 'data/repositories/feature_repository_impl.dart';
export 'data/models/feature_model.dart';

// Presentation exports
export 'presentation/controllers/feature_controller.dart';
export 'presentation/views/feature_list_view.dart';
export 'presentation/widgets/feature_card.dart';
```

#### 5.4 Update Main App Dependencies
In main app's `pubspec.yaml`:
```yaml
dependencies:
  # ... other dependencies
  feature_name:
    path: features/feature_name
```

#### 5.5 Update Main App DI Configuration
In main app's dependency injection setup:
```dart
import 'package:feature_name/data/di/injection.dart' as feature_module;

@injectableInit
Future<void> configureDependencies() async {
  getIt.init();
  // Register feature module
  // Note: This might need adjustment based on your DI setup
}
```

#### 5.6 Add Routes to Main App
In main app's routing configuration:
```dart
// lib/app/routes/app_pages.dart
abstract class AppPages {
  static const INITIAL = Routes.HOME;

  static final routes = [
    // ... existing routes
    GetPage(
      name: '/features',
      page: () => const FeatureListView(),
      binding: FeatureBinding(),
    ),
    GetPage(
      name: '/feature/create',
      page: () => const FeatureCreateView(),
      binding: FeatureBinding(),
    ),
    GetPage(
      name: '/feature/:id',
      page: () => const FeatureDetailView(),
      binding: FeatureBinding(),
    ),
  ];
}
```

#### 5.7 Create Binding
Create file: `lib/presentation/bindings/feature_binding.dart`
```dart
import 'package:get/get.dart';
import '../controllers/feature_controller.dart';

class FeatureBinding extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut(
      () => FeatureController(
        getAllFeaturesUseCase: Get.find(),
        getFeatureUseCase: Get.find(),
        createFeatureUseCase: Get.find(),
      ),
    );
  }
}
```

### Phase 6: Testing

#### 6.1 Write Unit Tests
Create file: `test/unit/usecases/get_feature_test.dart`
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dartz/dartz.dart';

import 'package:feature_name/domain/entities/feature_entity.dart';
import 'package:feature_name/domain/repositories/feature_repository.dart';
import 'package:feature_name/domain/usecases/get_feature.dart';
import 'package:feature_name/shared/failures/failure.dart';

class MockFeatureRepository extends Mock implements FeatureRepository {}

void main() {
  late GetFeatureUseCase useCase;
  late MockFeatureRepository mockRepository;

  setUp(() {
    mockRepository = MockFeatureRepository();
    useCase = GetFeatureUseCase(mockRepository);
  });

  test('should return feature when repository call is successful', () async {
    // Arrange
    const featureId = '1';
    const feature = FeatureEntity(
      id: '1',
      title: 'Test Feature',
      description: 'Test Description',
      createdAt: null,
      updatedAt: null,
    );

    when(() => mockRepository.getFeatureById(featureId))
        .thenAnswer((_) async => const Right(feature));

    // Act
    final result = await useCase.execute(featureId);

    // Assert
    expect(result, const Right(feature));
    verify(() => mockRepository.getFeatureById(featureId)).called(1);
  });

  test('should return failure when repository call fails', () async {
    // Arrange
    const featureId = '1';
    const failure = ServerFailure('Feature not found');

    when(() => mockRepository.getFeatureById(featureId))
        .thenAnswer((_) async => const Left(failure));

    // Act
    final result = await useCase.execute(featureId);

    // Assert
    expect(result, const Left(failure));
  });
}
```

#### 6.2 Write Widget Tests
Create file: `test/widget/widgets/feature_card_test.dart`
```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:feature_name/presentation/widgets/feature_card.dart';
import 'package:feature_name/domain/entities/feature_entity.dart';

void main() {
  group('FeatureCard', () {
    testWidgets('displays feature information correctly', (tester) async {
      // Arrange
      const feature = FeatureEntity(
        id: '1',
        title: 'Test Feature',
        description: 'Test Description',
        createdAt: null,
        updatedAt: null,
      );

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: FeatureCard(feature: feature),
          ),
        ),
      );

      // Assert
      expect(find.text('Test Feature'), findsOneWidget);
      expect(find.text('Test Description'), findsOneWidget);
    });

    testWidgets('calls onTap when tapped', (tester) async {
      // Arrange
      const feature = FeatureEntity(
        id: '1',
        title: 'Test Feature',
        description: 'Test Description',
        createdAt: null,
        updatedAt: null,
      );

      bool wasTapped = false;

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: FeatureCard(
              feature: feature,
              onTap: () => wasTapped = true,
            ),
          ),
        ),
      );

      await tester.tap(find.byType(FeatureCard));
      await tester.pump();

      // Assert
      expect(wasTapped, true);
    });
  });
}
```

### Phase 7: Code Generation

#### 7.1 Run Code Generation
```bash
# Navigate to feature directory
cd features/feature_name

# Generate JSON serialization
flutter packages pub run build_runner build --delete-conflicting-outputs

# Generate dependency injection (if applicable)
flutter packages pub run build_runner build
```

### Phase 8: Documentation

#### 8.1 Update Documentation
- Update project README with new feature
- Create feature-specific documentation
- Update API documentation
- Update changelog

#### 8.2 Create Feature README
Create file: `README.md`
```markdown
# Feature Name Module

## Description
Brief description of what this feature does.

## Architecture
- **Domain Layer**: Entities, use cases, repository interfaces
- **Data Layer**: Data sources, models, repository implementation
- **Presentation Layer**: Controllers, views, widgets

## Usage
```dart
import 'package:feature_name/feature_name.dart';

// Example usage
final controller = Get.find<FeatureController>();
await controller.loadFeatures();
```

## Dependencies
- get: ^4.6.5
- dartz: ^0.10.1
- equatable: ^2.0.5

## Testing
Run tests with:
```bash
flutter test
```
```

## Verification Checklist

### Code Quality
- [ ] All code follows project style guidelines
- [ ] Proper error handling implemented
- [ ] No hardcoded values
- [ ] Proper null safety implementation
- [ ] Comments and documentation added

### Architecture Compliance
- [ ] Clean Architecture layers properly separated
- [ ] Dependency rule followed (only inward dependencies)
- [ ] Modular architecture principles followed
- [ ] Proper dependency injection setup

### Testing
- [ ] Unit tests written for use cases
- [ ] Unit tests written for repositories
- [ ] Widget tests written for UI components
- [ ] Integration tests written if needed
- [ ] All tests passing

### Integration
- [ ] Feature successfully added to main app
- [ ] Routes configured correctly
- [ ] Dependencies resolved
- [ ] Build successful
- [ ] App runs without errors

### Performance
- [ ] No memory leaks
- [ ] Efficient data loading
- [ ] Proper state management
- [ ] Responsive UI

## Common Issues and Solutions

### Issue: Module not found
**Solution**: Ensure the module is properly added to main app's `pubspec.yaml` and run `flutter pub get`.

### Issue: Code generation failed
**Solution**: Run `flutter packages pub run build_runner clean` then `flutter packages pub run build_runner build`.

### Issue: Dependency injection errors
**Solution**: Verify all dependencies are properly registered in the DI container.

### Issue: Navigation not working
**Solution**: Check route configuration and ensure bindings are properly set up.

## Tools and Commands

### Development Commands
```bash
# Install dependencies
flutter pub get

# Run code generation
flutter packages pub run build_runner build

# Run tests
flutter test

# Build app
flutter build apk
```

### Useful VS Code Extensions
- Dart
- Flutter
- GetX Snippets
- Flutter Tree

## Resources

- [GetX Documentation](https://pub.dev/packages/get)
- [Clean Architecture in Flutter](https://resocoder.com/2019/08/27/flutter-clean-architecture-part-1-decoupling-your-project-with-dependency-injection/)
- [Flutter Documentation](https://flutter.dev/docs)
```

This SOP provides a comprehensive guide for adding new features while maintaining consistency with our architectural patterns and code quality standards.