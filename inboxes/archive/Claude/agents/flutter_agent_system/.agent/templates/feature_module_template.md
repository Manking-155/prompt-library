# Feature Module Template

## Overview

This template provides a complete structure for creating new feature modules following our Clean Architecture + Modular Architecture pattern.

## Directory Structure

```
feature_name/
├── pubspec.yaml                    # Module dependencies
├── lib/
│   ├── data/                       # Data Layer
│   │   ├── datasources/
│   │   │   ├── local_datasource.dart
│   │   │   └── remote_datasource.dart
│   │   ├── models/
│   │   │   ├── feature_model.dart
│   │   │   └── feature_dto.dart
│   │   ├── repositories/
│   │   │   └── feature_repository_impl.dart
│   │   └── mappers/
│   │       └── feature_mapper.dart
│   ├── domain/                     # Domain Layer
│   │   ├── entities/
│   │   │   └── feature_entity.dart
│   │   ├── usecases/
│   │   │   ├── get_feature.dart
│   │   │   ├── create_feature.dart
│   │   │   └── update_feature.dart
│   │   └── repositories/
│   │       └── feature_repository.dart
│   ├── presentation/               # Presentation Layer
│   │   ├── controllers/
│   │   │   ├── feature_controller.dart
│   │   │   └── feature_form_controller.dart
│   │   ├── views/
│   │   │   ├── feature_list_view.dart
│   │   │   ├── feature_detail_view.dart
│   │   │   └── feature_form_view.dart
│   │   └── widgets/
│   │       ├── feature_card.dart
│   │       └── feature_form_field.dart
│   └── feature_name.dart          # Public API exports
└── test/
    ├── unit/
    │   ├── usecases/
    │   └── repositories/
    ├── widget/
    │   └── widgets/
    └── integration/
        └── feature_integration_test.dart
```

## Step-by-Step Implementation

### 1. Create pubspec.yaml

```yaml
name: feature_name
description: Feature description

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

  # Shared modules
  shared:
    path: ../shared
  core_services:
    path: ../../lib/core/services

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.3.0
  injectable_generator: ^1.5.4
  mockito: ^5.3.2
  build_test: ^2.1.7
```

### 2. Domain Layer Implementation

#### Entity (lib/domain/entities/feature_entity.dart)

```dart
import 'package:equatable/equatable.dart';

/// Feature entity with business logic
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

  /// Business logic: Check if feature is complete
  bool get isComplete => description.isNotEmpty && title.isNotEmpty;

  /// Business logic: Get feature age
  Duration get age => DateTime.now().difference(createdAt);

  /// Copy with method for immutability
  FeatureEntity copyWith({
    String? id,
    String? title,
    String? description,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return FeatureEntity(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  @override
  List<Object?> get props => [id, title, description, createdAt, updatedAt];
}
```

#### Repository Interface (lib/domain/repositories/feature_repository.dart)

```dart
import 'package:dartz/dartz.dart';
import '../entities/feature_entity.dart';

/// Abstract repository for feature data access
abstract class FeatureRepository {
  /// Get all features
  Future<Either<String, List<FeatureEntity>>> getAllFeatures();

  /// Get feature by ID
  Future<Either<String, FeatureEntity>> getFeatureById(String id);

  /// Create new feature
  Future<Either<String, FeatureEntity>> createFeature(FeatureEntity feature);

  /// Update existing feature
  Future<Either<String, FeatureEntity>> updateFeature(FeatureEntity feature);

  /// Delete feature
  Future<Either<String, void>> deleteFeature(String id);
}
```

#### Use Cases (lib/domain/usecases/get_feature.dart)

```dart
import 'package:dartz/dartz.dart';
import '../entities/feature_entity.dart';
import '../repositories/feature_repository.dart';

/// Get feature by ID use case
class GetFeatureUseCase {
  final FeatureRepository _repository;

  GetFeatureUseCase(this._repository);

  /// Execute the use case
  Future<Either<String, FeatureEntity>> execute(String featureId) async {
    if (featureId.isEmpty) {
      return const Left('Feature ID cannot be empty');
    }

    return await _repository.getFeatureById(featureId);
  }
}
```

```dart
// lib/domain/usecases/get_all_features.dart
import 'package:dartz/dartz.dart';
import '../entities/feature_entity.dart';
import '../repositories/feature_repository.dart';

/// Get all features use case
class GetAllFeaturesUseCase {
  final FeatureRepository _repository;

  GetAllFeaturesUseCase(this._repository);

  /// Execute the use case
  Future<Either<String, List<FeatureEntity>>> execute() async {
    return await _repository.getAllFeatures();
  }
}
```

### 3. Data Layer Implementation

#### DTO (lib/data/models/feature_dto.dart)

```dart
import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/feature_entity.dart';

part 'feature_dto.g.dart';

@JsonSerializable()
class FeatureDto {
  final String id;
  final String title;
  final String description;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  @JsonKey(name: 'updated_at')
  final DateTime updatedAt;

  FeatureDto({
    required this.id,
    required this.title,
    required this.description,
    required this.createdAt,
    required this.updatedAt,
  });

  /// From JSON
  factory FeatureDto.fromJson(Map<String, dynamic> json) =>
      _$FeatureDtoFromJson(json);

  /// To JSON
  Map<String, dynamic> toJson() => _$FeatureDtoToJson(this);

  /// Convert to domain entity
  FeatureEntity toEntity() {
    return FeatureEntity(
      id: id,
      title: title,
      description: description,
      createdAt: createdAt,
      updatedAt: updatedAt,
    );
  }

  /// Convert from domain entity
  factory FeatureDto.fromEntity(FeatureEntity entity) {
    return FeatureDto(
      id: entity.id,
      title: entity.title,
      description: entity.description,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
    );
  }
}
```

#### Remote Data Source (lib/data/datasources/remote_datasource.dart)

```dart
import 'package:dartz/dartz.dart';
import '../models/feature_dto.dart';

abstract class FeatureRemoteDataSource {
  Future<Either<String, List<FeatureDto>>> getAllFeatures();
  Future<Either<String, FeatureDto>> getFeatureById(String id);
  Future<Either<String, FeatureDto>> createFeature(FeatureDto feature);
  Future<Either<String, FeatureDto>> updateFeature(FeatureDto feature);
  Future<Either<String, void>> deleteFeature(String id);
}

class FeatureRemoteDataSourceImpl implements FeatureRemoteDataSource {
  final HttpClient _httpClient;

  FeatureRemoteDataSourceImpl(this._httpClient);

  @override
  Future<Either<String, List<FeatureDto>>> getAllFeatures() async {
    try {
      final response = await _httpClient.get('/features');
      final features = (response.data as List)
          .map((json) => FeatureDto.fromJson(json))
          .toList();
      return Right(features);
    } catch (e) {
      return Left('Failed to fetch features: $e');
    }
  }

  @override
  Future<Either<String, FeatureDto>> getFeatureById(String id) async {
    try {
      final response = await _httpClient.get('/features/$id');
      final feature = FeatureDto.fromJson(response.data);
      return Right(feature);
    } catch (e) {
      return Left('Failed to fetch feature: $e');
    }
  }

  @override
  Future<Either<String, FeatureDto>> createFeature(FeatureDto feature) async {
    try {
      final response = await _httpClient.post(
        '/features',
        data: feature.toJson(),
      );
      final createdFeature = FeatureDto.fromJson(response.data);
      return Right(createdFeature);
    } catch (e) {
      return Left('Failed to create feature: $e');
    }
  }

  @override
  Future<Either<String, FeatureDto>> updateFeature(FeatureDto feature) async {
    try {
      final response = await _httpClient.put(
        '/features/${feature.id}',
        data: feature.toJson(),
      );
      final updatedFeature = FeatureDto.fromJson(response.data);
      return Right(updatedFeature);
    } catch (e) {
      return Left('Failed to update feature: $e');
    }
  }

  @override
  Future<Either<String, void>> deleteFeature(String id) async {
    try {
      await _httpClient.delete('/features/$id');
      return const Right(null);
    } catch (e) {
      return Left('Failed to delete feature: $e');
    }
  }
}
```

#### Repository Implementation (lib/data/repositories/feature_repository_impl.dart)

```dart
import 'package:dartz/dartz.dart';
import '../../domain/entities/feature_entity.dart';
import '../../domain/repositories/feature_repository.dart';
import '../datasources/remote_datasource.dart';
import '../datasources/local_datasource.dart';
import '../models/feature_dto.dart';
import '../mappers/feature_mapper.dart';

class FeatureRepositoryImpl implements FeatureRepository {
  final FeatureRemoteDataSource _remoteDataSource;
  final FeatureLocalDataSource _localDataSource;
  final FeatureMapper _mapper;

  FeatureRepositoryImpl(
    this._remoteDataSource,
    this._localDataSource,
    this._mapper,
  );

  @override
  Future<Either<String, List<FeatureEntity>>> getAllFeatures() async {
    try {
      // Try local first (offline-first)
      final localFeatures = await _localDataSource.getAllFeatures();
      if (localFeatures.isNotEmpty) {
        final entities = localFeatures.map(_mapper.dtoToEntity).toList();
        return Right(entities);
      }

      // Fallback to remote
      final remoteResult = await _remoteDataSource.getAllFeatures();

      return remoteResult.fold(
        (error) => Left(error),
        (dtos) async {
          // Cache locally
          await _localDataSource.saveFeatures(dtos);
          final entities = dtos.map(_mapper.dtoToEntity).toList();
          return Right(entities);
        },
      );
    } catch (e) {
      return Left('Failed to get features: $e');
    }
  }

  @override
  Future<Either<String, FeatureEntity>> getFeatureById(String id) async {
    try {
      // Try local first
      final localFeature = await _localDataSource.getFeatureById(id);
      if (localFeature != null) {
        return Right(_mapper.dtoToEntity(localFeature));
      }

      // Fallback to remote
      final remoteResult = await _remoteDataSource.getFeatureById(id);

      return remoteResult.fold(
        (error) => Left(error),
        (dto) async {
          // Cache locally
          await _localDataSource.saveFeature(dto);
          return Right(_mapper.dtoToEntity(dto));
        },
      );
    } catch (e) {
      return Left('Failed to get feature: $e');
    }
  }

  @override
  Future<Either<String, FeatureEntity>> createFeature(FeatureEntity feature) async {
    try {
      final dto = _mapper.entityToDto(feature);
      final result = await _remoteDataSource.createFeature(dto);

      return result.fold(
        (error) => Left(error),
        (createdDto) async {
          // Cache locally
          await _localDataSource.saveFeature(createdDto);
          return Right(_mapper.dtoToEntity(createdDto));
        },
      );
    } catch (e) {
      return Left('Failed to create feature: $e');
    }
  }

  @override
  Future<Either<String, FeatureEntity>> updateFeature(FeatureEntity feature) async {
    try {
      final dto = _mapper.entityToDto(feature);
      final result = await _remoteDataSource.updateFeature(dto);

      return result.fold(
        (error) => Left(error),
        (updatedDto) async {
          // Update local cache
          await _localDataSource.updateFeature(updatedDto);
          return Right(_mapper.dtoToEntity(updatedDto));
        },
      );
    } catch (e) {
      return Left('Failed to update feature: $e');
    }
  }

  @override
  Future<Either<String, void>> deleteFeature(String id) async {
    try {
      final result = await _remoteDataSource.deleteFeature(id);

      return result.fold(
        (error) => Left(error),
        (_) async {
          // Delete from local cache
          await _localDataSource.deleteFeature(id);
          return const Right(null);
        },
      );
    } catch (e) {
      return Left('Failed to delete feature: $e');
    }
  }
}
```

### 4. Presentation Layer Implementation

#### Controller (lib/presentation/controllers/feature_controller.dart)

```dart
import 'package:get/get.dart';
import 'package:dartz/dartz.dart';
import '../../domain/entities/feature_entity.dart';
import '../../domain/usecases/get_all_features.dart';
import '../../domain/usecases/get_feature.dart';
import '../../domain/usecases/create_feature.dart';

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

  FeatureController(
    this._getAllFeaturesUseCase,
    this._getFeatureUseCase,
    this._createFeatureUseCase,
  );

  @override
  void onInit() {
    super.onInit();
    loadFeatures();
  }

  /// Load all features
  Future<void> loadFeatures() async {
    _setLoading(true);
    _clearError();

    final result = await _getAllFeaturesUseCase.execute();

    result.fold(
      (error) => _setError(error),
      (features) => _features.assignAll(features),
    );

    _setLoading(false);
  }

  /// Load specific feature
  Future<void> loadFeature(String featureId) async {
    _setLoading(true);
    _clearError();

    final result = await _getFeatureUseCase.execute(featureId);

    result.fold(
      (error) => _setError(error),
      (feature) => _selectedFeature.value = feature,
    );

    _setLoading(false);
  }

  /// Create new feature
  Future<void> createFeature(FeatureEntity feature) async {
    _setLoading(true);
    _clearError();

    final result = await _createFeatureUseCase.execute(feature);

    result.fold(
      (error) => _setError(error),
      (createdFeature) {
        _features.add(createdFeature);
        Get.snackbar('Success', 'Feature created successfully');
      },
    );

    _setLoading(false);
  }

  /// Select a feature
  void selectFeature(FeatureEntity feature) {
    _selectedFeature.value = feature;
  }

  /// Clear selected feature
  void clearSelectedFeature() {
    _selectedFeature.value = null;
  }

  /// Refresh features
  Future<void> refresh() async {
    await loadFeatures();
  }

  // Private helper methods
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

#### View (lib/presentation/views/feature_list_view.dart)

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
                  Text(
                    'Error: ${controller.error.value}',
                    style: const TextStyle(color: Colors.red),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: controller.refresh,
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          if (controller.features.isEmpty) {
            return const Center(
              child: Text('No features found'),
            );
          }

          return RefreshIndicator(
            onRefresh: controller.refresh,
            child: ListView.builder(
              itemCount: controller.features.length,
              itemBuilder: (context, index) {
                final feature = controller.features[index];
                return FeatureCard(
                  feature: feature,
                  onTap: () => controller.selectFeature(feature),
                );
              },
            ),
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

### 5. Dependency Injection Setup

#### Module Configuration (lib/data/di/injection.dart)

```dart
import 'package:injectable/injectable.dart';
import '../../domain/repositories/feature_repository.dart';
import '../../domain/usecases/get_feature.dart';
import '../../domain/usecases/get_all_features.dart';
import '../../domain/usecases/create_feature.dart';
import '../repositories/feature_repository_impl.dart';
import '../datasources/remote_datasource.dart';
import '../datasources/local_datasource.dart';

@module
abstract class FeatureModule {
  // Data sources
  @singleton
  FeatureRemoteDataSource get featureRemoteDataSource =>
      FeatureRemoteDataSourceImpl(Get.find<HttpClient>());

  @singleton
  FeatureLocalDataSource get featureLocalDataSource =>
      FeatureLocalDataSourceImpl(Get.find<Database>());

  // Repository
  @singleton
  FeatureRepository get featureRepository => FeatureRepositoryImpl(
        featureRemoteDataSource,
        featureLocalDataSource,
        FeatureMapper(),
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
}
```

### 6. Public API Exports

#### Module Entry Point (lib/feature_name.dart)

```dart
// Domain exports
export 'domain/entities/feature_entity.dart';
export 'domain/repositories/feature_repository.dart';
export 'domain/usecases/get_feature.dart';
export 'domain/usecases/get_all_features.dart';
export 'domain/usecases/create_feature.dart';

// Data exports
export 'data/repositories/feature_repository_impl.dart';
export 'data/models/feature_dto.dart';

// Presentation exports
export 'presentation/controllers/feature_controller.dart';
export 'presentation/views/feature_list_view.dart';
export 'presentation/views/feature_detail_view.dart';
export 'presentation/widgets/feature_card.dart';
```

## Testing Templates

### Unit Test for Use Case (test/unit/usecases/get_feature_test.dart)

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dartz/dartz.dart';

import 'package:feature_name/domain/entities/feature_entity.dart';
import 'package:feature_name/domain/repositories/feature_repository.dart';
import 'package:feature_name/domain/usecases/get_feature.dart';

class MockFeatureRepository extends Mock implements FeatureRepository {}

void main() {
  late GetFeatureUseCase useCase;
  late MockFeatureRepository mockRepository;

  setUp(() {
    mockRepository = MockFeatureRepository();
    useCase = GetFeatureUseCase(mockRepository);
  });

  const testFeature = FeatureEntity(
    id: '1',
    title: 'Test Feature',
    description: 'Test Description',
    createdAt: null,
    updatedAt: null,
  );

  test('should return feature when repository call is successful', () async {
    // Arrange
    const featureId = '1';
    when(() => mockRepository.getFeatureById(featureId))
        .thenAnswer((_) async => const Right(testFeature));

    // Act
    final result = await useCase.execute(featureId);

    // Assert
    expect(result, const Right(testFeature));
    verify(() => mockRepository.getFeatureById(featureId)).called(1);
    verifyNoMoreInteractions(mockRepository);
  });

  test('should return failure when repository call fails', () async {
    // Arrange
    const featureId = '1';
    const errorMessage = 'Feature not found';
    when(() => mockRepository.getFeatureById(featureId))
        .thenAnswer((_) async => const Left(errorMessage));

    // Act
    final result = await useCase.execute(featureId);

    // Assert
    expect(result, const Left(errorMessage));
    verify(() => mockRepository.getFeatureById(featureId)).called(1);
    verifyNoMoreInteractions(mockRepository);
  });

  test('should return failure when feature ID is empty', () async {
    // Act
    final result = await useCase.execute('');

    // Assert
    expect(result, const Left('Feature ID cannot be empty'));
    verifyNever(() => mockRepository.getFeatureById(any(named: 'id')));
  });
}
```

## Integration Steps

1. **Create directory structure** following the template
2. **Copy and customize** all template files
3. **Replace placeholder names** with actual feature names
4. **Implement business logic** in entities and use cases
5. **Set up data sources** for remote and local data
6. **Create UI components** following the presentation layer structure
7. **Set up dependency injection** in the module configuration
8. **Write tests** for all layers
9. **Add routing** to integrate with the main app
10. **Test integration** with the main application

## Checklist

- [ ] Directory structure created
- [ ] pubspec.yaml configured with dependencies
- [ ] Domain layer implemented (entities, use cases, repositories)
- [ ] Data layer implemented (models, data sources, repository impl)
- [ ] Presentation layer implemented (controllers, views, widgets)
- [ ] Dependency injection configured
- [ ] Tests written for all layers
- [ ] Integration with main app tested
- [ ] Documentation updated
- [ ] Code review completed