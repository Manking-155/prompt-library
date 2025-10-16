# Database Schema and Management

## Overview

This project uses SQLite as the local database with Drift (formerly Moor) as the type-safe ORM. Drift provides compile-time safety, reactive queries, and powerful migrations.

## Technology Stack

- **SQLite**: Local database engine
- **Drift**: Type-safe ORM for Dart/Flutter
- **drift_dev**: Code generation for Drift
- **sqlite3_flutter_libs**: SQLite bindings for Flutter
- **path_provider**: For finding database file locations

## Database Architecture

### Database Location
```dart
// lib/core/database/app_database.dart
class AppDatabase {
  static AppDatabase? _instance;
  static AppDatabase get instance {
    _instance ??= AppDatabase._();
    return _instance!;
  }

  Database? _database;

  Future<Database> get database async {
    _database ??= await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    final databasesPath = await getDatabasesPath();
    final path = join(databasesPath, 'app_database.db');

    return await openDatabase(
      path,
      version: AppDatabase.version,
      onCreate: _onCreate,
      onUpgrade: _onUpgrade,
    );
  }
}
```

### Drift Database Setup
```dart
// lib/core/database/app_drift_database.dart
part 'app_drift_database.g.dart';

@DriftDatabase(tables: [
  Users,
  Flashcards,
  Decks,
  StudySessions,
])
class AppDriftDatabase extends _$AppDriftDatabase {
  AppDriftDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  @override
  MigrationStrategy get migration {
    return MigrationStrategy(
      onCreate: (Migrator m) async {
        await m.createAll();
      },
      onUpgrade: (Migrator m, int from, int to) async {
        // Handle migrations
      },
    );
  }
}

LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'db.sqlite'));
    return NativeDatabase(file);
  });
}
```

## Core Tables

### Users Table
```dart
// lib/core/database/tables/users.dart
@DataClassName('User')
class Users extends Table {
  TextColumn get id => text()();
  TextColumn get name => text()();
  TextColumn get email => text().unique()();
  TextColumn get passwordHash => text()();
  DateTimeColumn get createdAt => dateTime()();
  DateTimeColumn get updatedAt => dateTime()();
  BoolColumn get isActive => boolean().withDefault(const Constant(true))();

  @override
  Set<Column> get primaryKey => {id};
}
```

### Flashcards Table
```dart
// lib/core/database/tables/flashcards.dart
@DataClassName('Flashcard')
class Flashcards extends Table {
  TextColumn get id => text()();
  TextColumn get deckId => text().references(Decks, #id)();
  TextColumn get frontText => text()();
  TextColumn get backText => text()();
  TextColumn get frontImagePath => text().nullable()();
  TextColumn get backImagePath => text().nullable()();
  IntColumn get difficulty => integer().withDefault(const Constant(1))();
  IntColumn get reviewCount => integer().withDefault(const Constant(0))();
  DateTimeColumn get lastReviewedAt => dateTime().nullable()();
  DateTimeColumn get nextReviewAt => dateTime().nullable()();
  DateTimeColumn get createdAt => dateTime()();
  DateTimeColumn get updatedAt => dateTime()();
  BoolColumn get isActive => boolean().withDefault(const Constant(true))();

  @override
  Set<Column> get primaryKey => {id};
}
```

### Decks Table
```dart
// lib/core/database/tables/decks.dart
@DataClassName('Deck')
class Decks extends Table {
  TextColumn get id => text()();
  TextColumn get userId => text().references(Users, #id)();
  TextColumn get name => text()();
  TextColumn get description => text().nullable()();
  TextColumn get coverImagePath => text().nullable()();
  IntColumn get cardCount => integer().withDefault(const Constant(0))();
  IntColumn get studyCount => integer().withDefault(const Constant(0))();
  DateTimeColumn get createdAt => dateTime()();
  DateTimeColumn get updatedAt => dateTime()();
  BoolColumn get isActive => boolean().withDefault(const Constant(true))();

  @override
  Set<Column> get primaryKey => {id};
}
```

### Study Sessions Table
```dart
// lib/core/database/tables/study_sessions.dart
@DataClassName('StudySession')
class StudySessions extends Table {
  TextColumn get id => text()();
  TextColumn get userId => text().references(Users, #id)();
  TextColumn get deckId => text().references(Decks, #id)();
  DateTimeColumn get startedAt => dateTime()();
  DateTimeColumn get endedAt => dateTime().nullable()();
  IntColumn get cardsStudied => integer().withDefault(const Constant(0))();
  IntColumn get correctAnswers => integer().withDefault(const Constant(0))();
  IntColumn get incorrectAnswers => integer().withDefault(const Constant(0))();
  TextColumn get studyMode => text()(); // 'review', 'new', 'mixed'
  TextColumn get notes => text().nullable()();

  @override
  Set<Column> get primaryKey => {id};
}
```

## Repository Pattern with Drift

### Base Repository
```dart
// lib/core/database/base_repository.dart
abstract class BaseRepository<T extends Table, D> {
  final AppDriftDatabase _database;

  BaseRepository(this._database);

  TableInfo<T, D> get table;

  Future<List<D>> getAll() async {
    return await (_database.select(table)).get();
  }

  Future<D?> getById(String id) async {
    return await (_database.select(table)..where((t) => t.id.equals(id)))
        .getSingleOrNull();
  }

  Future<void> insert(D data) async {
    await _database.into(table).insert(data);
  }

  Future<void> update(D data) async {
    await _database.update(table).replace(data);
  }

  Future<void> delete(String id) async {
    await (_database.delete(table)..where((t) => t.id.equals(id))).go();
  }
}
```

### Flashcard Repository
```dart
// lib/features/flashcard_viewer/data/repositories/flashcard_repository.dart
class FlashcardRepository extends BaseRepository<Flashcards, Flashcard> {
  FlashcardRepository(AppDriftDatabase database) : super(database);

  @override
  TableInfo<Flashcards, Flashcard> get table => database.flashcards;

  Future<List<Flashcard>> getCardsByDeck(String deckId) async {
    return await (database.select(database.flashcards)
          ..where((f) => f.deckId.equals(deckId))
          ..orderBy([(f) => OrderingTerm(expression: f.createdAt)]))
        .get();
  }

  Future<List<Flashcard>> getCardsForReview() async {
    final now = DateTime.now();
    return await (database.select(database.flashcards)
          ..where((f) => f.nextReviewAt.isSmallerThanValue(now) |
                        f.nextReviewAt.isNull())
          ..orderBy([(f) => OrderingTerm(expression: f.nextReviewAt)]))
        .get();
  }

  Future<void> updateReviewStats(String flashcardId, bool isCorrect) async {
    final flashcard = await getById(flashcardId);
    if (flashcard != null) {
      final newCount = flashcard.reviewCount + 1;
      final lastReviewed = DateTime.now();
      final nextReview = _calculateNextReview(lastReviewed, isCorrect);

      final updatedFlashcard = flashcard.copyWith(
        reviewCount: newCount,
        lastReviewedAt: lastReviewed,
        nextReviewAt: nextReview,
      );

      await update(updatedFlashcard);
    }
  }

  DateTime _calculateNextReview(DateTime lastReview, bool isCorrect) {
    // Spaced repetition algorithm implementation
    final interval = isCorrect ? 7 : 1; // Simple implementation
    return lastReview.add(Duration(days: interval));
  }
}
```

## Database Migrations

### Migration Strategy
```dart
// lib/core/database/migrations/migration_v1_to_v2.dart
class MigrationV1ToV2 {
  static const int fromVersion = 1;
  static const int toVersion = 2;

  static Future<void> migrate(Migrator m, AppDriftDatabase database) async {
    // Add new column to flashcards table
    await m.addColumn(database.flashcards, 'category');

    // Create new table
    await m.createTable(database.categories);

    // Migrate existing data
    await _migrateFlashcardData(database);
  }

  static Future<void> _migrateFlashcardData(AppDriftDatabase database) async {
    final flashcards = await database.select(database.flashcards).get();

    for (final flashcard in flashcards) {
      // Set default category based on deck
      final deck = await (database.select(database.decks)
            ..where((d) => d.id.equals(flashcard.deckId)))
          .getSingleOrNull();

      if (deck != null) {
        final updatedFlashcard = flashcard.copyWith(
          category: deck.name,
        );
        await database.update(database.flashcards).replace(updatedFlashcard);
      }
    }
  }
}
```

### Migration Manager
```dart
// lib/core/database/migrations/migration_manager.dart
class MigrationManager {
  static final List<Migration> migrations = [
    // Add migrations here
  ];

  static Future<void> runMigrations(
    Migrator m,
    AppDriftDatabase database,
    int fromVersion,
    int toVersion,
  ) async {
    for (final migration in migrations) {
      if (migration.fromVersion >= fromVersion &&
          migration.toVersion <= toVersion) {
        await migration.migrate(m, database);
      }
    }
  }
}
```

## Database Initialization and Setup

### Database Service
```dart
// lib/core/services/database_service.dart
@singleton
class DatabaseService extends GetxService {
  late final AppDriftDatabase _database;
  late final FlashcardRepository _flashcardRepository;
  late final DeckRepository _deckRepository;
  late final UserRepository _userRepository;

  Future<void> init() async {
    _database = AppDriftDatabase();

    // Initialize repositories
    _flashcardRepository = FlashcardRepository(_database);
    _deckRepository = DeckRepository(_database);
    _userRepository = UserRepository(_database);

    // Register with GetIt
    GetIt.instance.registerSingleton<FlashcardRepository>(_flashcardRepository);
    GetIt.instance.registerSingleton<DeckRepository>(_deckRepository);
    GetIt.instance.registerSingleton<UserRepository>(_userRepository);
  }

  AppDriftDatabase get database => _database;
  FlashcardRepository get flashcardRepository => _flashcardRepository;
  DeckRepository get deckRepository => _deckRepository;
  UserRepository get userRepository => _userRepository;

  @override
  void onClose() {
    _database.close();
    super.onClose();
  }
}
```

## Performance Optimization

### Indexing Strategy
```dart
// Add indexes to frequently queried columns
class Flashcards extends Table {
  // ... existing columns

  // Create indexes for performance
  IntColumn get deckIdIndex => index()();
  IntColumn get nextReviewIndex => index()();
  IntColumn get userIdIndex => index()();
}
```

### Query Optimization
```dart
// Efficient querying with joins
Future<List<FlashcardWithDeck>> getFlashcardsWithDeck(String userId) async {
  final query = database.select(database.flashcards).join([
    innerJoin(
      database.decks,
      database.flashcards.deckId.equalsExp(database.decks.id),
    ),
  ])..where(database.decks.userId.equals(userId));

  final results = await query.get();

  return results.map((row) {
    final flashcard = row.readTable(database.flashcards);
    final deck = row.readTable(database.decks);
    return FlashcardWithDeck(flashcard: flashcard, deck: deck);
  }).toList();
}
```

## Testing Database Operations

### Mock Database for Testing
```dart
// test/mocks/mock_database.dart
class MockAppDriftDatabase extends Mock implements AppDriftDatabase {}

class MockFlashcardRepository {
  final _flashcards = <Flashcard>[];

  Future<List<Flashcard>> getAll() async {
    return _flashcards;
  }

  Future<Flashcard?> getById(String id) async {
    return _flashcards.firstWhereOrNull((f) => f.id == id);
  }

  Future<void> insert(Flashcard flashcard) async {
    _flashcards.add(flashcard);
  }

  Future<void> update(Flashcard flashcard) async {
    final index = _flashcards.indexWhere((f) => f.id == flashcard.id);
    if (index != -1) {
      _flashcards[index] = flashcard;
    }
  }

  Future<void> delete(String id) async {
    _flashcards.removeWhere((f) => f.id == id);
  }
}
```

### Database Tests
```dart
// test/unit/repositories/flashcard_repository_test.dart
void main() {
  late AppDriftDatabase database;
  late FlashcardRepository repository;

  setUp(() async {
    database = AppDriftDatabase.memory();
    repository = FlashcardRepository(database);
  });

  tearDown(() async {
    await database.close();
  });

  group('FlashcardRepository', () {
    test('should insert and retrieve flashcard', () async {
      // Arrange
      const flashcard = Flashcard(
        id: '1',
        deckId: 'deck1',
        frontText: 'Test',
        backText: 'Answer',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      // Act
      await repository.insert(flashcard);
      final result = await repository.getById('1');

      // Assert
      expect(result, isNotNull);
      expect(result!.frontText, 'Test');
    });

    test('should get cards by deck', () async {
      // Arrange
      final flashcards = [
        const Flashcard(
          id: '1',
          deckId: 'deck1',
          frontText: 'Test 1',
          backText: 'Answer 1',
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        ),
        const Flashcard(
          id: '2',
          deckId: 'deck1',
          frontText: 'Test 2',
          backText: 'Answer 2',
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        ),
      ];

      for (final flashcard in flashcards) {
        await repository.insert(flashcard);
      }

      // Act
      final result = await repository.getCardsByDeck('deck1');

      // Assert
      expect(result.length, 2);
      expect(result.first.frontText, 'Test 1');
    });
  });
}
```

## Best Practices

### 1. **Transaction Management**
```dart
Future<void> batchInsertFlashcards(List<Flashcard> flashcards) async {
  await database.transaction(() async {
    for (final flashcard in flashcards) {
      await database.into(database.flashcards).insert(flashcard);
    }
  });
}
```

### 2. **Error Handling**
```dart
Future<Result<List<Flashcard>>> getFlashcardsSafely() async {
  try {
    final flashcards = await getAll();
    return Result.success(flashcards);
  } catch (e) {
    return Result.failure('Failed to load flashcards: $e');
  }
}
```

### 3. **Connection Management**
- Always close database connections when done
- Use connection pooling for high-load scenarios
- Handle database locks gracefully

### 4. **Data Validation**
- Validate data before insertion
- Use database constraints for data integrity
- Implement proper error handling for constraint violations

### 5. **Backup and Recovery**
- Implement regular database backups
- Provide data export/import functionality
- Handle database corruption scenarios