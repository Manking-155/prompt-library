# Database Schema & Drift Integration

## Overview

This project uses **Drift** (formerly moor) as the database ORM layer. Drift provides:
- Type-safe SQL queries
- Automatic migrations
- Support for complex queries
- Compile-time verification

## Technology Stack

- **Database**: SQLite (local storage)
- **ORM**: Drift
- **Encryption**: Optional (use sqlite_crypt for sensitive data)
- **Sync**: Manual background sync to backend

## Database Configuration

### pubspec.yaml Dependencies
```yaml
dependencies:
  drift: ^2.14.0
  sqlite3_flutter_libs: ^0.5.0
  
dev_dependencies:
  build_runner: ^2.4.0
  drift_dev: ^2.14.0
```

### Creating Database File

Create `lib/core/database/app_database.dart`:

```dart
import 'dart:io';
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

part 'app_database.g.dart';

// Define tables here
// ...

@DriftDatabase(tables: [Users, Flashcards])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());
  
  @override
  int get schemaVersion => 1;
  
  @override
  MigrationStrategy get migration {
    return MigrationStrategy(
      onCreate: (Migrator m) async {
        await m.createAll();
      },
      onUpgrade: (Migrator m, int from, int to) async {
        // Handle migrations here
      },
    );
  }
}

LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'app.db'));
    return NativeDatabase(file);
  });
}
```

## Table Definition Example

### Users Table

```dart
class Users extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get email => text().unique()();
  TextColumn get name => text()();
  TextColumn get profileImage => text().nullable()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
  DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();
}

@DataClassName('User')
class UsersData extends DataClass implements Insertable<UsersData> {
  final int id;
  final String email;
  final String name;
  final String? profileImage;
  final DateTime createdAt;
  final DateTime updatedAt;
  
  UsersData({
    required this.id,
    required this.email,
    required this.name,
    this.profileImage,
    required this.createdAt,
    required this.updatedAt,
  });
  
  @override
  Map<String, Expression> toColumns(bool nullByDefault) => {
    'id': Variable(id),
    'email': Variable(email),
    'name': Variable(name),
    'profile_image': Variable(profileImage),
    'created_at': Variable(createdAt),
    'updated_at': Variable(updatedAt),
  };
}
```

### Flashcards Table

```dart
class Flashcards extends Table {
  IntColumn get id => integer().autoIncrement()();
  IntColumn get userId => integer().references(Users, #id)();
  TextColumn get question => text()();
  TextColumn get answer => text()();
  IntColumn get category => integer().nullable()();
  BoolColumn get isStarred => boolean().withDefault(const Constant(false))();
  IntColumn get reviewCount => integer().withDefault(const Constant(0))();
  DateTimeColumn get lastReviewedAt => dateTime().nullable()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
  DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();
}
```

## Queries with Drift

### Creating Records
```dart
Future<int> insertUser(UsersCompanion user) {
  return into(users).insert(user);
}

// Usage
await database.insertUser(
  UsersCompanion(
    email: const Value('john@example.com'),
    name: const Value('John Doe'),
  ),
);
```

### Reading Records
```dart
// Get all users
Future<List<UsersData>> getAllUsers() {
  return select(users).get();
}

// Get user by ID
Future<UsersData?> getUserById(int id) {
  return (select(users)..where((tbl) => tbl.id.equals(id))).getSingleOrNull();
}

// Complex query
Future<List<FlashcardsData>> getUserFlashcards(int userId) {
  return (select(flashcards)
    ..where((tbl) => tbl.userId.equals(userId))
    ..orderBy([(t) => OrderingTerm(expression: t.createdAt, mode: OrderingMode.desc)]))
    .get();
}
```

### Updating Records
```dart
Future<bool> updateUser(int id, UsersCompanion user) {
  return (update(users)..where((tbl) => tbl.id.equals(id))).write(user);
}

// Usage
await database.updateUser(
  1,
  UsersCompanion(
    name: const Value('Jane Doe'),
  ),
);
```

### Deleting Records
```dart
Future<int> deleteUser(int id) {
  return (delete(users)..where((tbl) => tbl.id.equals(id))).go();
}

// Delete all
Future<int> deleteAllUsers() {
  return delete(users).go();
}
```

## Transactions

```dart
Future<void> transferFlashcards(int fromUserId, int toUserId) {
  return transaction(() async {
    // Atomically execute multiple operations
    await customUpdate(
      'UPDATE flashcards SET user_id = ? WHERE user_id = ?',
      variables: [Variable(toUserId), Variable(fromUserId)],
    );
  });
}
```

## Streaming Data

```dart
// Listen to real-time changes
Stream<List<UsersData>> watchAllUsers() {
  return select(users).watch();
}

// Usage in GetX controller
@override
void onInit() {
  watchAllUsers().listen((users) {
    this.users.value = users;
  });
  super.onInit();
}
```

## Database Service

Create `lib/core/services/database_service.dart`:

```dart
@lazySingleton
class DatabaseService {
  final AppDatabase _database;
  
  DatabaseService(this._database);
  
  // Users
  Future<int> createUser(String email, String name) {
    return _database.into(_database.users).insert(
      UsersCompanion(
        email: Value(email),
        name: Value(name),
      ),
    );
  }
  
  Stream<List<UsersData>> watchAllUsers() {
    return _database.select(_database.users).watch();
  }
  
  // Flashcards
  Future<int> createFlashcard(int userId, String question, String answer) {
    return _database.into(_database.flashcards).insert(
      FlashcardsCompanion(
        userId: Value(userId),
        question: Value(question),
        answer: Value(answer),
      ),
    );
  }
  
  Stream<List<FlashcardsData>> watchUserFlashcards(int userId) {
    return (_database.select(_database.flashcards)
      ..where((t) => t.userId.equals(userId)))
      .watch();
  }
}
```

## DI Setup

```dart
@InjectableInit()
void configureDependencies() {
  getIt.init();
}

// In main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  configureDependencies();
  
  // Initialize database
  await getIt<AppDatabase>().customStatement('PRAGMA journal_mode=WAL');
  
  runApp(const MyApp());
}
```

## Migrations

### Version 1 → 2

```dart
@override
MigrationStrategy get migration {
  return MigrationStrategy(
    onCreate: (Migrator m) async {
      await m.createAll();
    },
    onUpgrade: (Migrator m, int from, int to) async {
      if (from == 1 && to == 2) {
        // Add new column
        await m.addColumn(
          users,
          users.lastLoginAt,
        );
      }
    },
  );
}
```

## Backup & Restore

```dart
Future<void> backupDatabase() async {
  final dbPath = (await getApplicationDocumentsDirectory()).path;
  final dbFile = File('$dbPath/app.db');
  
  final backupPath = (await getApplicationDocumentsDirectory()).path;
  await dbFile.copy('$backupPath/app.db.backup');
}

Future<void> restoreDatabase() async {
  final backupPath = (await getApplicationDocumentsDirectory()).path;
  final backupFile = File('$backupPath/app.db.backup');
  
  final dbPath = (await getApplicationDocumentsDirectory()).path;
  await backupFile.copy('$dbPath/app.db');
}
```

## Generate Database Code

```bash
# Generate code
flutter pub run build_runner build

# Watch mode (rebuilds on file changes)
flutter pub run build_runner watch

# Clean and rebuild
flutter pub run build_runner clean
flutter pub run build_runner build
```

## Related Documentation
- Project Architecture: `system/project_architecture.md`
- Data Layer Implementation: `system/clean_architecture_guide.md`
- Database Migrations SOP: `sops/database_migrations.md`
