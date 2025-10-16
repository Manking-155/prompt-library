# Flutter Agent System - Documentation Index

Welcome to the Flutter Agent System documentation. This system implements **Modular Clean Architecture** with GetX state management for Flutter applications.

## Quick Navigation

### 🏗️ Architecture & Design
Start here to understand the system architecture:
- **[Project Architecture](system/project_architecture.md)** - Tech stack, folder structure, key patterns
- **[Clean Architecture Guide](system/clean_architecture_guide.md)** - 3-layer separation (Presentation/Domain/Data)
- **[Modular Architecture Guide](system/modular_architecture_guide.md)** - Feature-based modules and organization
- **[Code Standards](system/code_standards.md)** - Naming conventions, formatting, linting rules

### 💾 Database & Data
Learn about data persistence and schema management:
- **[Database Schema & Drift Integration](system/database_schema.md)** - SQLite with Drift ORM, queries, migrations

### 📚 Templates & Examples
Copy-paste templates and detailed examples:
- **[Feature Module Template](templates/feature_module_template.md)** - Complete step-by-step guide to create new features
- **[State Management Examples](templates/state_management_example.md)** - GetX patterns, controllers, reactive state
- **[Clean Architecture Layers](templates/clean_architecture_layers.md)** - Code snippets for each layer

### 🔧 Standard Operating Procedures (SOPs)
How to perform common development tasks:
- **[Adding a New Feature](sops/adding_new_feature.md)** - Complete workflow for adding features
- **[Database Migrations](sops/database_migrations.md)** - Adding/modifying tables, data migrations
- **[Dependency Injection](sops/dependency_injection.md)** - GetIt setup, service registration
- **[Error Handling](sops/error_handling.md)** - Result wrapper, exception handling patterns
- **[Routing & Navigation](sops/routing_navigation.md)** - GetX routes, deep linking, middleware

## 🚀 Getting Started

### For New Team Members
1. Read **[Project Architecture](system/project_architecture.md)** (10 min)
2. Read **[Clean Architecture Guide](system/clean_architecture_guide.md)** (15 min)
3. Skim **[Code Standards](system/code_standards.md)** (10 min)
4. Review **[Feature Module Template](templates/feature_module_template.md)** as reference

### For Adding a Feature
1. Check **[Adding a New Feature](sops/adding_new_feature.md)**
2. Use **[Feature Module Template](templates/feature_module_template.md)** for implementation
3. Reference **[State Management Examples](templates/state_management_example.md)** for GetX patterns

### For Database Changes
1. Read **[Database Schema](system/database_schema.md)**
2. Follow **[Database Migrations](sops/database_migrations.md)** SOP

### For Debugging
1. Check **[Error Handling](sops/error_handling.md)** for exception patterns
2. Read **[Code Standards](system/code_standards.md)** troubleshooting section
3. Review **[Dependency Injection](sops/dependency_injection.md)** if DI issues occur

## 📋 Project Structure

```
flutter_app/
├── lib/
│   ├── app/                    # App configuration & theme
│   ├── core/                   # Core services & infrastructure
│   │   ├── di/                 # GetIt + Injectable setup
│   │   ├── database/           # Drift database
│   │   ├── services/           # Global services
│   │   ├── errors/             # Result wrapper & exceptions
│   ├── features/               # Feature modules
│   │   ├── shared/             # Shared code between features
│   │   ├── [feature_name]/
│   │   │   ├── lib/
│   │   │   │   ├── data/       # Repositories & datasources
│   │   │   │   ├── domain/     # Entities, interfaces, usecases
│   │   │   │   └── presentation/  # UI, controllers, bindings
│   │   │   └── pubspec.yaml
│   ├── routes/                 # Route definitions
│   └── main.dart               # App entry point
├── test/
│   ├── unit/
│   ├── widget/
│   └── integration/
└── pubspec.yaml
```

## 🎯 Key Concepts

### Modular Architecture
- Each feature is a self-contained module
- Features have independent `pubspec.yaml`
- No circular dependencies between features
- Enables parallel development

### Clean Architecture
- **Presentation**: UI & State Management (GetX)
- **Domain**: Business Logic & Interfaces
- **Data**: Repository Implementations & Datasources

### Error Handling
- Use `Result<T, E>` wrapper instead of exceptions
- Custom exception hierarchy for different error types
- Type-safe error propagation through layers

### State Management
- GetX Controllers for reactive state
- Observable properties (`.obs`)
- Bindings for dependency injection
- Automatic cleanup and disposal

### Database
- SQLite for local storage
- Drift ORM for type-safe queries
- Offline-first strategy
- Background sync with backend

## 📞 Support & Questions

If you have questions:
1. Check the relevant documentation section first
2. Search for similar patterns in existing features
3. Review error handling documentation
4. Ask team lead with specific context

## 🔄 Updating Documentation

After implementing a new feature or pattern:
1. Add examples to relevant template if applicable
2. Update SOP if workflow changes
3. Document any non-standard patterns in comments
4. Share knowledge with team

## 📝 Documentation Standards

- All documentation in English
- Provide real code examples
- Include troubleshooting sections
- Link to related documentation
- Keep examples simple and focused

## 🎓 Learning Path

**Beginner**:
1. Project Architecture
2. Clean Architecture Guide
3. Simple Feature Implementation

**Intermediate**:
1. State Management Examples
2. Database Migrations
3. Error Handling Patterns

**Advanced**:
1. Modular Architecture Details
2. Custom DI Patterns
3. Deep Linking & Navigation

## ✅ Pre-Implementation Checklist

Before starting any implementation:
- [ ] Requirements are clear
- [ ] You've read relevant documentation
- [ ] Team agrees on approach
- [ ] You have a development database/environment
- [ ] You understand error handling patterns
- [ ] You know where your code fits in architecture

## 🚨 Common Issues & Solutions

### "Module not found" errors
→ Check **[Dependency Injection](sops/dependency_injection.md)**

### Circular dependencies
→ Review **[Modular Architecture](system/modular_architecture_guide.md)**

### State not updating
→ Check **[State Management Examples](templates/state_management_example.md)**

### Migration failures
→ Follow **[Database Migrations](sops/database_migrations.md)**

### Route not working
→ See **[Routing & Navigation](sops/routing_navigation.md)**

---

**Last Updated**: October 2024

For questions or documentation improvements, contact the development team.
