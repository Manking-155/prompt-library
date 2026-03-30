# SOP: Database Migrations with Drift

## Overview

This Standard Operating Procedure (SOP) outlines the process for creating and managing database schema migrations using Drift (formerly Moor) in our Flutter application.

## Prerequisites

- Flutter SDK installed
- Drift and related dependencies set up
- Understanding of SQL and database concepts
- Access to project repository
- Git branching strategy understood

## Key Concepts

### Migration Types
- **Schema Changes**: Adding tables, columns, indexes
- **Data Changes**: Modifying existing data
- **Index Changes**: Adding/removing indexes for performance
- **Constraint Changes**: Adding/modifying constraints

### Versioning Strategy
- Incremental version numbers (1, 2, 3, ...)
- Each migration handles one version step
- Forward and backward compatibility considered

## Step-by-Step Process

### Phase 1: Planning the Migration

#### 1.1 Analyze Required Changes
- [ ] Identify schema changes needed
- [ ] Determine data transformation requirements
- [ ] Assess impact on existing features
- [ ] Plan rollback strategy

#### 1.2 Create Migration Branch
```bash
# Create feature branch for migration
git checkout -b feature/database-migration-vX
```

#### 1.3 Design Migration Strategy
Consider:
- Is this a breaking change?
- Do we need to preserve existing data?
- What's the estimated downtime?
- How will we handle migration failures?

### Phase 2: Updating Database Schema

#### 2.1 Update Table Definitions
Modify table classes in `lib/core/database/tables/`:

Example: Adding new column to existing table
```dart
// lib/core/database/tables/users.dart
@DataClassName('User')
class Users extends Table {
  TextColumn get id => text()();
  TextColumn get name => text()();
  TextColumn get email => text().unique()();

  // New column being added
  TextColumn get avatarUrl => text().nullable()(); // NEW

  DateTimeColumn get createdAt => dateTime()();
  DateTimeColumn get updatedAt => dateTime()();

  @override
  Set<Column> get primaryKey => {id};
}
```

Example: Creating new table
```dart
// lib/core/database/tables/user_profiles.dart
@DataClassName('UserProfile')
class UserProfiles extends Table {
  TextColumn get userId => text().references(Users, #id)();
  TextColumn get bio => text().nullable()();
  TextColumn get location => text().nullable()();
  TextColumn get website => text().nullable()();

  DateTimeColumn get createdAt => dateTime()();
  DateTimeColumn get updatedAt => dateTime()();

  @override
  Set<Column> get primaryKey => {userId};
}
```

#### 2.2 Update Database Class
Add new table to database class:

```dart
// lib/core/database/app_drift_database.dart
part 'app_drift_database.g.dart';

@DriftDatabase(tables: [
  Users,
  UserProfiles, // NEW TABLE
  // ... other tables
])
class AppDriftDatabase extends _$AppDriftDatabase {
  AppDriftDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 2; // INCREMENT VERSION

  @override
  MigrationStrategy get migration {
    return MigrationStrategy(
      onCreate: (Migrator m) async {
        await m.createAll();
      },
      onUpgrade: (Migrator m, int from, int to) async {
        // Handle migrations
        if (from < 2) {
          await _migrateToV2(m);
        }
      },
    );
  }

  // Migration methods
  Future<void> _migrateToV2(Migrator m) async {
    // Add new column
    await m.addColumn(users, users.avatarUrl);

    // Create new table
    await m.createTable(userProfiles);

    // Optionally migrate data
    await _migrateUserData();
  }

  Future<void> _migrateUserData() async {
    // Data migration logic if needed
    final allUsers = await select(users).get();

    for (final user in allUsers) {
      // Create default profile for each user
      await into(userProfiles).insert(
        UserProfile(
          userId: user.id,
          bio: null,
          location: null,
          website: null,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        ),
      );
    }
  }
}
```

### Phase 3: Writing Migration Logic

#### 3.1 Simple Column Addition
```dart
Future<void> _migrateToV2(Migrator m) async {
  // Add nullable column (safe)
  await m.addColumn(users, users.avatarUrl);
}
```

#### 3.2 Column with Default Value
```dart
Future<void> _migrateToV3(Migrator m) async {
  // Add column with default value
  await m.addColumn(users, users.isActive);

  // Set default value for existing rows
  await customUpdate(
    'UPDATE users SET is_active = ?',
    variables: [Variable.withBool(true)],
    updates: {users},
  );
}
```

#### 3.3 Table Creation with Data Migration
```dart
Future<void> _migrateToV4(Migrator m) async {
  // Create new table
  await m.createTable(userPreferences);

  // Migrate data from existing table
  await customUpdate(
    '''INSERT INTO user_preferences (user_id, theme, notifications_enabled)
       SELECT id, 'light', 1 FROM users''',
    updates: {userPreferences},
  );
}
```

#### 3.4 Complex Data Transformation
```dart
Future<void> _migrateToV5(Migrator m) async {
  // Add new columns
  await m.addColumn(users, users.firstName);
  await m.addColumn(users, users.lastName);

  // Split existing name into first and last name
  final existingUsers = await select(users).get();

  for (final user in existingUsers) {
    final nameParts = user.name.split(' ');
    final firstName = nameParts.isNotEmpty ? nameParts.first : '';
    final lastName = nameParts.length > 1 ? nameParts.sublist(1).join(' ') : '';

    await (update(users)..where((tbl) => tbl.id.equals(user.id)))
        .write(UsersCompanion(
          firstName: Value(firstName),
          lastName: Value(lastName),
        ));
  }

  // Optionally drop old column after verification
  // await m.deleteColumn(users, users.name);
}
```

#### 3.5 Index Creation
```dart
Future<void> _migrateToV6(Migrator m) async {
  // Create index for performance
  await m.createIndex(users, 'idx_users_email', [users.email]);
  await m.createIndex(users, 'idx_users_created_at', [users.createdAt]);
}
```

### Phase 4: Testing Migrations

#### 4.1 Create Migration Test
Create file: `test/database/migrations_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:sqlite3_flutter_libs/sqlite3_flutter_libs.dart';
import '../../lib/core/database/app_drift_database.dart';

void main() {
  group('Database Migrations', () {
    late AppDriftDatabase database;

    setUp(() {
      database = AppDriftDatabase(DatabaseConnection(NativeDatabase.memory()));
    });

    tearDown(() async {
      await database.close();
    });

    test('should migrate from v1 to v2 correctly', () async {
      // Create database at version 1
      final v1Database = AppDriftDatabase(DatabaseConnection(NativeDatabase.memory()));

      // Insert test data at v1
      await v1Database.into(v1Database.users).insert(
        User(
          id: '1',
          name: 'John Doe',
          email: 'john@example.com',
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        ),
      );

      // Close v1 database
      await v1Database.close();

      // Open same database with new version (triggers migration)
      final v2Database = AppDriftDatabase(DatabaseConnection(NativeDatabase.memory()));

      // Verify migration worked
      final users = await v2Database.select(v2Database.users).get();
      expect(users.length, 1);
      expect(users.first.id, '1');
      expect(users.first.avatarUrl, isNull); // New column should be null

      await v2Database.close();
    });

    test('should migrate user data correctly when splitting name', () async {
      // Setup database with old schema
      final oldDatabase = _createOldVersionDatabase();

      await oldDatabase.customUpdate(
        'INSERT INTO users (id, name, email, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
        variables: [
          Variable.withString('1'),
          Variable.withString('John Doe'),
          Variable.withString('john@example.com'),
          Variable.withDateTime(DateTime.now()),
          Variable.withDateTime(DateTime.now()),
        ],
      );

      await oldDatabase.close();

      // Run migration
      final newDatabase = AppDriftDatabase(DatabaseConnection(NativeDatabase.memory()));

      // Verify data was migrated correctly
      final users = await newDatabase.select(newDatabase.users).get();
      expect(users.first.firstName, 'John');
      expect(users.first.lastName, 'Doe');

      await newDatabase.close();
    });
  });
}

// Helper to create old version database for testing
AppDriftDatabase _createOldVersionDatabase() {
  // This would create a database with the old schema
  // Implementation depends on your specific needs
  return AppDriftDatabase(DatabaseConnection(NativeDatabase.memory()));
}
```

#### 4.2 Test Data Migration
```dart
test('should preserve data during migration', () async {
  // Setup initial data
  await database.into(database.users).insert(
    User(
      id: '1',
      name: 'Test User',
      email: 'test@example.com',
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    ),
  );

  // Get data before migration
  final beforeMigration = await database.select(database.users).get();

  // Trigger migration (this would happen automatically in real app)
  await _runMigration();

  // Verify data is still there
  final afterMigration = await database.select(database.users).get();
  expect(afterMigration.length, beforeMigration.length);
  expect(afterMigration.first.id, beforeMigration.first.id);
  expect(afterMigration.first.email, beforeMigration.first.email);
});
```

### Phase 5: Handling Edge Cases

#### 5.1 Large Dataset Migration
```dart
Future<void> _migrateLargeDataset(Migrator m) async {
  final batchSize = 100;
  var offset = 0;
  bool hasMore = true;

  while (hasMore) {
    final batch = await (select(users)
          ..limit(batchSize, offset: offset))
        .get();

    if (batch.isEmpty) {
      hasMore = false;
    } else {
      // Process batch
      for (final user in batch) {
        await _processUserForMigration(user);
      }

      offset += batchSize;

      // Add small delay to prevent UI blocking
      await Future.delayed(const Duration(milliseconds: 10));
    }
  }
}
```

#### 5.2 Handling Migration Failures
```dart
@override
MigrationStrategy get migration {
  return MigrationStrategy(
    onUpgrade: (Migrator m, int from, int to) async {
      try {
        if (from < 2) {
          await _migrateToV2(m);
        }
        if (from < 3) {
          await _migrateToV3(m);
        }
      } catch (e) {
        // Log error
        print('Migration failed: $e');

        // Optionally implement rollback logic
        await _rollbackMigration(from);

        // Re-throw to prevent app from starting with corrupted database
        rethrow;
      }
    },
  );
}

Future<void> _rollbackMigration(int fromVersion) async {
  // Implement rollback logic if needed
  print('Rolling back to version $fromVersion');
}
```

#### 5.3 Conditional Migrations
```dart
Future<void> _migrateToV2(Migrator m) async {
  // Check if column already exists (for edge cases)
  final tableInfo = await customSelect('PRAGMA table_info(users)').get();
  final hasAvatarUrl = tableInfo.any((row) => row.read<String>('name') == 'avatar_url');

  if (!hasAvatarUrl) {
    await m.addColumn(users, users.avatarUrl);
  }
}
```

### Phase 6: Code Generation

#### 6.1 Generate Updated Code
```bash
# Navigate to project root
cd/

# Run code generation
flutter packages pub run build_runner build --delete-conflicting-outputs

# Or for development (watch mode)
flutter packages pub run build_runner watch --delete-conflicting-outputs
```

#### 6.2 Verify Generated Code
Check generated files in `.dart_tool/build/generated/`:
- Verify new table classes are generated
- Check migration logic is correct
- Ensure no compilation errors

### Phase 7: Integration Testing

#### 7.1 Test Full App Flow
```dart
test('app should work correctly after migration', () async {
  // Setup database with old version
  final oldDatabase = _setupOldDatabase();
  await _populateTestData(oldDatabase);
  await oldDatabase.close();

  // Start app with new version (triggers migration)
  await _startApp();

  // Test all features that use the database
  await _testUserRegistration();
  await _testUserProfileCreation();
  await _testDataRetrieval();

  // Verify no data corruption
  await _verifyDataIntegrity();
});
```

#### 7.2 Performance Testing
```dart
test('migration should complete within acceptable time', () async {
  final stopwatch = Stopwatch()..start();

  // Run migration on large dataset
  await _runMigrationWithLargeDataset();

  stopwatch.stop();

  // Migration should complete within 30 seconds for typical dataset
  expect(stopwatch.elapsed.inSeconds, lessThan(30));
});
```

### Phase 8: Deployment

#### 8.1 Update Version Information
```dart
// lib/core/database/database_version.dart
class DatabaseVersion {
  static const int current = 2;
  static const String migrationInfo = '''
  v1.0.0: Initial schema
  v2.0.0: Added user profiles and avatar URLs
  ''';
}
```

#### 8.2 Update Changelog
Update `CHANGELOG.md`:
```markdown
## [2.0.0] - 2024-01-15

### Database Changes
- Added `avatar_url` column to `users` table
- Created `user_profiles` table
- Added indexes for performance improvement
- Data migration for existing users

### Migration Notes
- Existing users will have empty profile records created
- Avatar URLs will be null for existing users
- Migration is automatic and backwards compatible
```

#### 8.3 Create Migration Backup Script
```bash
#!/bin/bash
# scripts/backup_database.sh

# Backup existing database before migration
DB_PATH="$HOME/Documents/app_data/database.db"
BACKUP_PATH="$HOME/Documents/app_data/backups/database_v1_backup_$(date +%Y%m%d_%H%M%S).db"

mkdir -p "$(dirname "$BACKUP_PATH")"
cp "$DB_PATH" "$BACKUP_PATH"

echo "Database backed up to: $BACKUP_PATH"
```

### Phase 9: Monitoring and Rollback

#### 9.1 Add Migration Monitoring
```dart
// lib/core/services/migration_service.dart
class MigrationService extends GetxService {
  final _migrationStatus = Rx<MigrationStatus>(MigrationStatus.notStarted);

  MigrationStatus get status => _migrationStatus.value;

  Future<void> runMigration() async {
    _migrationStatus.value = MigrationStatus.inProgress;

    try {
      final database = AppDriftDatabase();
      await database.customSelect('SELECT 1').get(); // Test connection

      _migrationStatus.value = MigrationStatus.completed;
      Get.snackbar('Success', 'Database migration completed');
    } catch (e) {
      _migrationStatus.value = MigrationStatus.failed;
      Get.snackbar('Error', 'Migration failed: $e');

      // Log to analytics
      await _logMigrationFailure(e);
    }
  }

  Future<void> _logMigrationFailure(dynamic error) async {
    // Send error to monitoring service
    print('Migration failed: $error');
  }
}
```

#### 9.2 Rollback Plan
```dart
// lib/core/services/rollback_service.dart
class RollbackService {
  Future<bool> rollbackToVersion(int targetVersion) async {
    try {
      // Close current database
      await Get.find<AppDriftDatabase>().close();

      // Restore backup
      final backupPath = _getLatestBackup(targetVersion);
      if (backupPath != null) {
        await _restoreDatabase(backupPath);

        // Restart app with old database
        Get.offAllNamed('/login'); // Force restart

        return true;
      }

      return false;
    } catch (e) {
      print('Rollback failed: $e');
      return false;
    }
  }
}
```

## Verification Checklist

### Before Migration
- [ ] Migration plan documented
- [ ] Backup strategy in place
- [ ] Test data prepared
- [ ] Rollback plan ready
- [ ] Performance impact assessed

### During Migration
- [ ] Migration runs without errors
- [ ] Data integrity maintained
- [ ] Performance within acceptable limits
- [ ] No app crashes

### After Migration
- [ ] All features working correctly
- [ ] Data verification complete
- [ ] Performance tests passed
- [ ] Error handling tested
- [ ] Documentation updated

### Code Quality
- [ ] No hardcoded values in migration
- [ ] Proper error handling
- [ ] Transaction management
- [ ] Logging implemented
- [ ] Code review completed

## Common Issues and Solutions

### Issue: Migration takes too long
**Solution**:
- Use batch processing for large datasets
- Add progress indicators
- Consider background migration

### Issue: Data corruption during migration
**Solution**:
- Use transactions
- Implement backup and restore
- Add data validation after migration

### Issue: Migration fails on some devices
**Solution**:
- Check available disk space
- Handle edge cases in data
- Add robust error handling

### Issue: App crashes after migration
**Solution**:
- Verify all code references updated columns
- Check generated code compatibility
- Test with different data scenarios

## Tools and Commands

### Development Commands
```bash
# Generate migration code
flutter packages pub run build_runner build

# Run database tests
flutter test test/database/

# Clean build cache
flutter packages pub run build_runner clean

# Reset database (development only)
rm -rf path/to/database.db
```

### Useful VS Code Extensions
- SQLite Viewer
- Drift Extension
- Database Client

### Debugging Tools
- Drift Inspector
- SQLite Database Browser
- Flutter DevTools

## Best Practices

1. **Always test migrations with real data**
2. **Use transactions for data consistency**
3. **Implement proper error handling**
4. **Monitor migration performance**
5. **Have rollback strategy ready**
6. **Document all schema changes**
7. **Version control all migration scripts**
8. **Test on different database sizes**

## Resources

- [Drift Documentation](https://drift.simonbinder.eu/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Flutter Testing Guide](https://flutter.dev/docs/cookbook/testing)
- [Database Migration Best Practices](https://medium.com/flutter-community/flutter-database-migrations-with-drift-5c8b9c8e0e1)