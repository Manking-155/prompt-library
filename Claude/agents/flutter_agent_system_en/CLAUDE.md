# Flutter Agent System - Documentation

## System Overview

This is a **Modular Clean Architecture** system for Flutter development with GetX state management, Drift database, and Feature-based module organization.

## Documentation Structure

We maintain comprehensive documentation in the `.agent/` folder:

### `.agent/system/` - Architecture & Technical Specs
Technical specifications for the system:
- `project_architecture.md` - Overall architecture, tech stack, folder structure
- `clean_architecture_guide.md` - 3-layer pattern (Presentation/Domain/Data)
- `modular_architecture_guide.md` - Feature modules, independence, shared code
- `code_standards.md` - Naming conventions, formatting, linting, Effective Dart
- `database_schema.md` - Drift ORM, table definitions, migrations, queries

### `.agent/templates/` - Implementation Guides
Reusable templates with code examples:
- `feature_module_template.md` - Complete step-by-step guide for new features
- `state_management_example.md` - GetX patterns, controllers, reactive state
- `clean_architecture_layers.md` - Code snippets for domain/data/presentation layers

### `.agent/sops/` - Standard Operating Procedures
Best practices for common tasks:
- `adding_new_feature.md` - Workflow to create a complete feature module
- `database_migrations.md` - How to modify database schema safely
- `dependency_injection.md` - GetIt setup, service registration, patterns
- `error_handling.md` - Result wrapper, custom exceptions, error patterns
- `routing_navigation.md` - GetX router, deep linking, middleware

### `.agent/readme.md` - Documentation Index
Navigation hub for all documentation with quick links and learning paths.

## Key Principles

1. **Modular Independence**: Features are self-contained with own pubspec.yaml
2. **Clean Separation**: Clear boundaries between Presentation/Domain/Data layers
3. **Type-Safe Errors**: Result wrapper for explicit error handling
4. **Reactive State**: GetX for observable state and automatic UI updates
5. **Offline-First**: Local SQLite database with background sync
6. **Testable**: Clear dependency injection for easy mocking

## Before Implementation

**Always read `.agent/readme.md` first** to understand which documentation applies to your task.

### Reading Order by Task Type

**Adding a Feature**:
1. `.agent/sops/adding_new_feature.md` - Complete workflow
2. `.agent/templates/feature_module_template.md` - Code examples
3. Reference `.agent/system/` docs as needed

**Database Changes**:
1. `.agent/system/database_schema.md` - Schema definitions
2. `.agent/sops/database_migrations.md` - Migration process

**Understanding Architecture**:
1. `.agent/system/project_architecture.md` - Overview
2. `.agent/system/clean_architecture_guide.md` - Detailed explanation
3. `.agent/system/modular_architecture_guide.md` - Module organization

**State Management**:
1. `.agent/templates/state_management_example.md` - Patterns
2. `.agent/system/code_standards.md` - Style guide

## Tech Stack

- **Framework**: Flutter 3.x + Dart 3.x
- **State Management**: GetX
- **Navigation**: Get Router
- **Database**: SQLite + Drift ORM
- **Dependency Injection**: GetIt + Injectable
- **HTTP**: Dio
- **Testing**: Flutter Test + Mockito

## Architecture Layers

```
┌─────────────────────────────────────┐
│   Presentation (UI + GetX)          │ <- Pages, Widgets, Controllers
├─────────────────────────────────────┤
│   Domain (Business Logic)           │ <- Entities, Repositories (abstract), Usecases
├─────────────────────────────────────┤
│   Data (External Sources)           │ <- Models, Datasources, Repositories (impl)
└─────────────────────────────────────┘
         ↕ (Drift ORM)
    SQLite Database
```

## Common Commands

```bash
# Generate Drift code
flutter pub run build_runner build

# Watch for changes
flutter pub run build_runner watch

# Format code
dart format lib

# Analyze
dart analyze lib

# Run tests
flutter test

# Clean rebuild
flutter clean && flutter pub get
```

## Documentation Updates

After implementing features, update relevant docs:
1. Add examples to `.agent/templates/` if creating new patterns
2. Update `.agent/sops/` if workflow changed
3. Add troubleshooting to relevant docs
4. Update `.agent/readme.md` if adding new sections

## Starting a New Feature

1. Read `.agent/readme.md`
2. Check `.agent/sops/adding_new_feature.md`
3. Use `.agent/templates/feature_module_template.md` as guide
4. Reference `.agent/system/` docs during implementation
5. Follow `.agent/system/code_standards.md` for coding style

## Help & Support

- Architecture questions → Check `.agent/system/`
- How to do something → Check `.agent/sops/`
- Code examples → Check `.agent/templates/`
- Navigation → Start at `.agent/readme.md`

## Documentation Rules

1. Always read documentation before asking
2. Update docs when adding new patterns
3. Keep all examples current and tested
4. Use English for all documentation
5. Link related documentation
6. Include troubleshooting sections

---

**Remember**: The `.agent/` documentation is the source of truth for the system.
Always reference it when making architectural decisions or implementing features.

Start with `.agent/readme.md` for quick navigation to relevant docs.
