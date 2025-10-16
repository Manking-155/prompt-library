# SOP: Database Migrations with Drift

## Overview
This document describes how to handle database migrations when making schema changes.

## Prerequisites
- Drift is properly configured in the project
- Database code is already generated
- You understand the current schema

## Migration Types

### Type 1: Adding a New Table

#### Step 1: Create New Table Class
In `lib/core/database/app_database.dart`:

```dart
class Products extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get name => text()();
  RealColumn get price => real()();
  TextColumn get description => text().nullable()();
  IntColumn get categoryId => integer().references(Categories, #id)();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

// Update @DriftDatabase annotation
@DriftDatabase(tables: [Users, Flashcards, Products])
class AppDatabase extends _$AppDatabase {
  // ...
}
```

#### Step 2: Increment Schema Version
```dart
@override
int get schemaVersion => 2;  // Was 1, now 2
```

#### Step 3: Handle Migration
```dart
@override
MigrationStrategy get migration {
  return MigrationStrategy(
    onCreate: (Migrator m) async {
      await m.createAll();
    },
    onUpgrade: (Migrator m, int from, int to) async {
      if (from == 1 && to == 2) {
        await m.create(products);  // Create new table
      }
    },
  );
}
```

#### Step 4: Generate Code
```bash
flutter pub run build_runner build
```

### Type 2: Adding a New Column

#### Step 1: Update Table Definition
```dart
class Users extends Table {
  // ... existing columns ...
  TextColumn get phoneNumber => text().nullable()();  // New column
  BoolColumn get verified => boolean().withDefault(const Constant(false))();
}
```

#### Step 2: Increment Schema Version
```dart
@override
int get schemaVersion => 3;
```

#### Step 3: Handle Migration
```dart
onUpgrade: (Migrator m, int from, int to) async {
  if (from == 1 && to == 2) {
    await m.create(products);
  }
  if (from <= 2 && to >= 3) {
    await m.addColumn(users, users.phoneNumber);
    await m.addColumn(users, users.verified);
  }
}
```

#### Step 4: Generate and Test
```bash
flutter pub run build_runner build
flutter test
```

### Type 3: Modifying a Column

Note: SQLite has limited column modification support. Usually requires data migration.

#### Step 1: Create Migration Script
```dart
onUpgrade: (Migrator m, int from, int to) async {
  if (from <= 2 && to >= 3) {
    // SQLite doesn't support direct column modifications
    // Must use raw SQL for complex changes
    await m.customStatement(
      'ALTER TABLE users RENAME TO users_old'
    );
    
    await m.create(users);  // Create with new schema
    
    // Copy data (handle type conversions if needed)
    await m.customStatement(
      'INSERT INTO users (id, name, email, created_at, updated_at) '
      'SELECT id, name, email, created_at, updated_at FROM users_old'
    );
    
    await m.customStatement('DROP TABLE users_old');
  }
}
```

### Type 4: Removing a Column

#### Step 1: Create Migration
```dart
onUpgrade: (Migrator m, int from, int to) async {
  if (from <= 3 && to >= 4) {
    // Remove the column from table definition first, then migrate
    await m.customStatement(
      'ALTER TABLE users RENAME TO users_old'
    );
    
    await m.create(users);  // Create without old column
    
    // Copy only needed columns
    await m.customStatement(
      'INSERT INTO users (id, name, email, created_at, updated_at) '
      'SELECT id, name, email, created_at, updated_at FROM users_old'
    );
    
    await m.customStatement('DROP TABLE users_old');
  }
}
```

### Type 5: Renaming a Column

#### Step 1: Rename in Schema
```dart
class Users extends Table {
  // Old: TextColumn get firstName => text()();
  // New: TextColumn get givenName => text()();  // Renamed
  TextColumn get givenName => text()();
}
```

#### Step 2: Handle Migration
```dart
onUpgrade: (Migrator m, int from, int to) async {
  if (from <= 4 && to >= 5) {
    await m.customStatement(
      'ALTER TABLE users RENAME COLUMN first_name TO given_name'
    );
  }
}
```

## Step-by-Step Process

### 1. Backup Current Database (Development)
```dart
Future<void> backupDatabase() async {
  final dbFolder = await getApplicationDocumentsDirectory();
  final dbFile = File('${dbFolder.path}/app.db');
  
  if (dbFile.existsSync()) {
    await dbFile.copy('${dbFolder.path}/app.db.backup');
    print('Database backed up');
  }
}
```

### 2. Test Migration Locally

#### 2.1 Use Development Database
```bash
# Delete old database to test migration from scratch
rm -rf ~/Library/Developer/CoreSimulator/Devices/[DEVICE_ID]/data/Containers/Data/Application/*/Documents/app.db
```

#### 2.2 Run App and Test
```bash
flutter run
```

#### 2.3 Verify Data Integrity
- Check that all data is intact
- Verify queries still work
- Test all features depending on modified schema

### 3. Version Control

#### 3.1 Git Commit
```bash
git add lib/core/database/app_database.dart
git commit -m "chore(db): add migration v2 - add products table

- Add Products table with category relationship
- Increment schema version to 2
- Handle migration for existing databases"
```

### 4. Deploy to Production

#### 4.1 User Data Safety
- Always test with backup database
- Have rollback plan
- Monitor for issues in production

#### 4.2 Update Version
```yaml
# pubspec.yaml
version: 1.1.0  # Increment version for schema change
```

## Common Patterns

### Add Foreign Key Relationship

```dart
class Flashcards extends Table {
  IntColumn get userId => integer().references(Users, #id)();
}

@override
MigrationStrategy get migration {
  return MigrationStrategy(
    onUpgrade: (Migrator m, int from, int to) async {
      if (from <= 2 && to >= 3) {
        await m.create(flashcards);
      }
    },
  );
}
```

### Add Unique Constraint

```dart
class Users extends Table {
  TextColumn get email => text().unique()();
}
```

### Add Default Value

```dart
class Posts extends Table {
  BoolColumn get isPublished => boolean().withDefault(const Constant(false))();
  DateTimeColumn get publishedAt => dateTime().withDefault(currentDateAndTime)();
}
```

### Add Index for Performance

```dart
class Flashcards extends Table {
  IntColumn get userId => integer().references(Users, #id)();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
  
  @override
  List<Set<Column>> get uniqueKeys => [
    {userId, createdAt},
  ];
}
```

## Debugging

### View Database Schema
```dart
Future<void> printDatabaseSchema() async {
  final database = Get.find<AppDatabase>();
  final result = await database.customSelect(
    'SELECT name, sql FROM sqlite_master WHERE type="table"'
  ).get();
  
  for (var row in result) {
    print('Table: ${row['name']}');
    print('SQL: ${row['sql']}');
    print('---');
  }
}
```

### Check Current Schema Version
```dart
Future<void> checkSchemaVersion() async {
  final database = Get.find<AppDatabase>();
  final userVersion = await database.customSelect(
    'PRAGMA user_version'
  ).get();
  
  print('Current schema version: ${userVersion.first['user_version']}');
}
```

### Inspect Table Data
```dart
Future<void> inspectTable() async {
  final database = Get.find<AppDatabase>();
  final rows = await database.customSelect(
    'SELECT * FROM users LIMIT 10'
  ).get();
  
  for (var row in rows) {
    print(row.data);
  }
}
```

## Troubleshooting

### Migration Fails on Startup
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter pub run build_runner clean
flutter pub run build_runner build
```

### Schema Mismatch
```dart
// Check if code generation is up to date
flutter pub run build_runner build --verbose
```

### Data Loss During Migration
```dart
// Restore from backup
Future<void> restoreFromBackup() async {
  final backup = File('${(await getApplicationDocumentsDirectory()).path}/app.db.backup');
  final current = File('${(await getApplicationDocumentsDirectory()).path}/app.db');
  
  if (backup.existsSync()) {
    await backup.copy(current.path);
  }
}
```

### Circular Foreign Key References
```dart
// Use nullable foreign keys if needed
class Orders extends Table {
  IntColumn get id => integer().autoIncrement()();
  IntColumn? get shippingAddressId => integer().references(Addresses, #id).nullable()();
}
```

## Best Practices

1. **Test migrations thoroughly**: Always test before deployment
2. **Backup data**: Keep backups of production databases
3. **Incremental migrations**: Keep migration steps small and focused
4. **Document changes**: Comment why changes were made
5. **Version tracking**: Keep schema version consistent with app version
6. **Validate data**: Check data integrity after migrations
7. **Monitor production**: Watch for issues after deploying migrations

## Related Documentation
- Database Schema: `system/database_schema.md`
- Project Architecture: `system/project_architecture.md`
