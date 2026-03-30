# Flutter Agent System

A comprehensive agent system for Flutter development following Clean Architecture + Modular Architecture patterns with GetX state management.

## 📁 Directory Structure

```
flutter_agent_system/.agent/
├── system/                    # System documentation and architecture
│   ├── project_architecture.md
│   ├── clean_architecture_guide.md
│   ├── modular_architecture_guide.md
│   ├── code_standards.md
│   └── database_schema.md
├── templates/                 # Code templates for faster development
│   ├── feature_module_template.md
│   ├── clean_architecture_layers.md
│   └── state_management_example.md
├── sops/                      # Standard Operating Procedures
│   ├── adding_new_feature.md
│   ├── database_migrations.md
│   ├── dependency_injection.md
│   ├── error_handling.md
│   └── routing_navigation.md
└── README.md                  # This file
```

## 🏗️ Architecture Overview

Our Flutter application follows a combination of proven architectural patterns:

### Clean Architecture
- **Domain Layer**: Business logic, entities, use cases, repository interfaces
- **Data Layer**: Data sources, models, repository implementations
- **Presentation Layer**: UI, controllers, views, state management

### Modular Architecture
- **Feature Modules**: Independent, self-contained features
- **Shared Modules**: Common code reused across features
- **Core Services**: Application-wide services and utilities

### Technology Stack
- **Flutter**: Cross-platform UI framework
- **GetX**: State management, dependency injection, navigation
- **GetIt + Injectable**: Service location and DI
- **Drift (Moor)**: Type-safe SQLite database
- **Dartz**: Functional programming with Either/Result pattern

## 🚀 Quick Start

### 1. Understanding the Architecture

Start with these documents to understand our architectural approach:

1. **[Project Architecture](system/project_architecture.md)** - High-level overview of our tech stack and structure
2. **[Clean Architecture Guide](system/clean_architecture_guide.md)** - Detailed explanation of the 3-layer architecture
3. **[Modular Architecture Guide](system/modular_architecture_guide.md)** - How we structure feature modules

### 2. Development Standards

Before writing code, review our standards:

- **[Code Standards](system/code_standards.md)** - Naming conventions, formatting, and best practices
- **[Database Schema](system/database_schema.md)** - Database design and Drift ORM usage

### 3. Adding New Features

Follow our SOP for adding new features:

- **[Adding New Feature SOP](sops/adding_new_feature.md)** - Step-by-step guide for creating feature modules

### 4. Using Templates

Speed up development with our templates:

- **[Feature Module Template](templates/feature_module_template.md)** - Complete template for new features
- **[Clean Architecture Layers Template](templates/clean_architecture_layers.md)** - Layer-by-layer implementation guide
- **[State Management Examples](templates/state_management_example.md)** - GetX patterns and examples

### 5. Common Operations

Reference our SOPs for common development tasks:

- **[Database Migrations](sops/database_migrations.md)** - Managing database schema changes
- **[Dependency Injection](sops/dependency_injection.md)** - Setting up DI with GetIt and Injectable
- **[Error Handling](sops/error_handling.md)** - Consistent error handling with Result pattern
- **[Routing and Navigation](sops/routing_navigation.md)** - Navigation setup with GetX

## 📋 Development Workflow

### 1. Feature Development
1. **Plan**: Review requirements and create feature plan
2. **Structure**: Use [feature module template](templates/feature_module_template.md)
3. **Implement**: Follow [Clean Architecture layers](templates/clean_architecture_layers.md)
4. **Test**: Write unit, widget, and integration tests
5. **Integrate**: Add routes and dependencies
6. **Review**: Ensure code quality and architecture compliance

### 2. Code Quality Checklist
- [ ] Follows [code standards](system/code_standards.md)
- [ ] Implements proper error handling
- [ ] Uses dependency injection correctly
- [ ] Has comprehensive tests
- [ ] Documents business logic
- [ ] Handles edge cases

### 3. Testing Strategy
- **Unit Tests**: Test use cases and business logic
- **Widget Tests**: Test UI components in isolation
- **Integration Tests**: Test complete user flows
- **Architecture Tests**: Verify Clean Architecture compliance

## 🎯 Key Patterns

### State Management with GetX
```dart
class UserController extends GetxController {
  final _users = <User>[].obs;
  final _isLoading = false.obs;

  List<User> get users => _users;
  bool get isLoading => _isLoading.value;

  Future<void> loadUsers() async {
    _isLoading.value = true;
    // Load data...
    _isLoading.value = false;
  }
}
```

### Error Handling with Result Pattern
```dart
Future<Result<User>> getUser(String id) async {
  try {
    final user = await repository.getUser(id);
    return Result.success(user);
  } catch (e) {
    return Result.failure(NetworkFailure('Failed to load user'));
  }
}
```

### Dependency Injection
```dart
@module
abstract class UserModule {
  @singleton
  UserRepository get userRepository => UserRepositoryImpl();

  @singleton
  GetUserUseCase get getUserUseCase => GetUserUseCase(repository);
}
```

## 🔧 Tools and Commands

### Development
```bash
# Install dependencies
flutter pub get

# Run code generation
flutter packages pub run build_runner build --delete-conflicting-outputs

# Run tests
flutter test

# Build app
flutter build apk
```

### Code Quality
```bash
# Format code
dart format .

# Analyze code
dart analyze

# Run lints
flutter analyze
```

## 📚 Best Practices

### Architecture
- **Dependency Rule**: Dependencies can only point inward
- **Single Responsibility**: Each class has one reason to change
- **Interface Segregation**: Clients shouldn't depend on unused interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

### Code Quality
- **English Language**: All code and comments in English
- **Null Safety**: Use Dart null safety throughout
- **Error Handling**: Use Result pattern for operations that can fail
- **Testing**: Write tests for all layers

### Performance
- **Lazy Loading**: Load data only when needed
- **Caching**: Implement offline-first strategy
- **Efficient Widgets**: Use const constructors and proper widget lifecycle

## 🐛 Common Issues and Solutions

### Issue: Navigation not working
**Solution**: Check route definitions in `AppPages` and ensure bindings are properly set up.

### Issue: Database migration failed
**Solution**: Follow the [database migration SOP](sops/database_migrations.md) and test migrations thoroughly.

### Issue: Dependency injection errors
**Solution**: Verify all dependencies are registered in the correct modules and check for circular dependencies.

### Issue: State not updating
**Solution**: Ensure you're using `.obs` for reactive variables and wrapping UI components with `Obx()` or `GetBuilder()`.

## 🤖 Using with AI Assistants

This agent system is designed to work seamlessly with AI assistants like Claude Code. When working with an AI assistant:

1. **Provide Context**: Start by mentioning you're using the Flutter Agent System
2. **Reference Documents**: Point to specific SOPs or templates when needed
3. **Follow Patterns**: Ask the AI to follow the established patterns and standards
4. **Review Output**: Always review AI-generated code against our standards

### Example Prompt
> "I need to create a new user management feature using the Flutter Agent System. Please follow the [Adding New Feature SOP](sops/adding_new_feature.md) and use the [Feature Module Template](templates/feature_module_template.md)."

## 📈 Continuous Improvement

This agent system is continuously evolving. To contribute improvements:

1. **Document Patterns**: Add new patterns and best practices
2. **Update Templates**: Keep templates up to date with latest practices
3. **Refine SOPs**: Improve SOPs based on real-world usage
4. **Share Knowledge**: Document lessons learned and solutions

## 🔗 External Resources

### Official Documentation
- [Flutter Documentation](https://flutter.dev/docs)
- [GetX Documentation](https://pub.dev/packages/get)
- [Drift Documentation](https://drift.simonbinder.eu/)
- [Dart Style Guide](https://dart.dev/guides/language/effective-dart)

### Learning Resources
- [Clean Architecture in Flutter](https://resocoder.com/flutter-clean-architecture-tutorial/)
- [GetX State Management](https://pub.dev/packages/get#getx-state-management)
- [Flutter Testing Guide](https://flutter.dev/docs/cookbook/testing)

## 📞 Support

For questions about this agent system:

1. **Check Documentation**: Review the relevant SOPs and templates
2. **Search Examples**: Look at template implementations
3. **Ask the Team**: Consult with senior developers
4. **Create Issues**: Document bugs and improvement suggestions

---

**Remember**: This agent system is a living document. Keep it updated as you discover new patterns and improve existing ones. The goal is to make Flutter development faster, more consistent, and more enjoyable for everyone on the team.

**Happy Coding! 🚀**