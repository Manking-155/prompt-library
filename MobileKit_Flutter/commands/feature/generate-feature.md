# Generate Flutter Feature Command

Generate a complete Flutter feature with widgets, providers, models, and tests using AI agents.

## Usage
```bash
mkf generate-feature --name user_profile --type complete-feature
```

## Options
- `--name <name>` - Feature name (snake_case, e.g., user_profile)
- `--type <type>` - Feature type: widget, screen, provider, complete-feature
- `--state <pattern>` - State management: riverpod, provider, bloc, getx
- `--responsive` - Generate responsive layouts
- `--tests` - Include widget and integration tests

## AI Workflow
1. **flutter-planner** - Creates implementation plan
2. **flutter-researcher** - Researches packages and patterns
3. **widget-designer** - Generates Flutter widgets
4. **flutter-data-architect** - Designs data models and repositories
5. **flutter-tester** - Creates widget and integration tests
6. **dart-reviewer** - Reviews generated code

## Generated Files
- Flutter Widgets (Stateless/Stateful)
- Providers/Notifiers (Riverpod)
- Data Models
- Repository Classes
- Widget Tests
- Integration Tests

Example output for `user_profile`:
```
lib/features/user_profile/
├── presentation/
│   ├── pages/
│   │   └── user_profile_page.dart
│   ├── widgets/
│   │   └── profile_card.dart
│   └── providers/
│       └── user_profile_provider.dart
├── domain/
│   ├── entities/
│   │   └── user.dart
│   └── repositories/
│       └── user_repository.dart
└── data/
    ├── models/
    │   └── user_model.dart
    └── repositories/
        └── user_repository_impl.dart
```
