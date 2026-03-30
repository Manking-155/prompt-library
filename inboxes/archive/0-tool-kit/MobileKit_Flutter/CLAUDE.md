# MobileKit Flutter - Project Context Configuration

You are working with **MobileKit Flutter**, an AI-powered development toolkit specifically designed for cross-platform mobile development using Flutter and Dart.

## Project Overview

This is a **Cross-Platform Flutter Project** with the following characteristics:
- **Platforms**: iOS, Android (with potential Web/Desktop support)
- **Language**: Dart 3.0+ with null safety
- **UI Framework**: Flutter 3.16+ with Material Design 3
- **Architecture**: MVVM with Provider/Riverpod state management
- **Deployment**: Google Play Store, Apple App Store

## Tech Stack

### Core Flutter Technologies
- **Language**: Dart 3.0+ with null safety and records
- **Framework**: Flutter 3.16+ with Material Design 3
- **State Management**: Riverpod (recommended) or Provider/Bloc
- **Navigation**: GoRouter for declarative routing
- **HTTP**: Dio with Retrofit for API integration
- **Local Storage**: Hive or Drift for local database
- **Async**: Streams, Futures, async/await patterns

### Flutter Packages Ecosystem
- **UI**: Material 3, Cupertino widgets, custom components
- **State**: riverpod, flutter_riverpod, hooks_riverpod
- **Navigation**: go_router, auto_route
- **Storage**: hive, drift, shared_preferences
- **Network**: dio, retrofit, chopper
- **Images**: cached_network_image, image_picker
- **Utils**: freezed, json_annotation, build_runner

### Development Tools
- **IDE**: VS Code, Android Studio, IntelliJ IDEA
- **DevTools**: Flutter Inspector, Performance profiler
- **Testing**: flutter_test, integration_test, golden_toolkit
- **CI/CD**: GitHub Actions, Codemagic, Bitrise
- **Distribution**: Firebase App Distribution, TestFlight

## Architecture Guidelines

### Project Structure
```
my_flutter_app/
├── lib/
│   ├── main.dart                  # App entry point
│   ├── app.dart                   # Root app widget
│   ├── core/
│   │   ├── constants/
│   │   ├── errors/
│   │   ├── network/
│   │   └── utils/
│   ├── features/
│   │   ├── authentication/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── profile/
│   │   └── home/
│   ├── shared/
│   │   ├── widgets/
│   │   ├── models/
│   │   └── services/
│   └── config/
│       ├── theme/
│       ├── routes/
│       └── env/
├── test/
├── integration_test/
├── assets/
└── pubspec.yaml
```

### Code Organization
- **Feature-first**: Organize by features, not layers
- **Clean Architecture**: Presentation, Domain, Data layers
- **SOLID principles**: Single responsibility, open/closed, etc.
- **Dependency injection**: Use providers for dependency management
- **Immutable data**: Use freezed for data classes

### Naming Conventions
- **Files**: snake_case (user_profile_view.dart)
- **Classes**: PascalCase (UserProfileView, UserViewModel)
- **Variables/Functions**: camelCase (userName, fetchUserData())
- **Constants**: lowerCamelCase or SCREAMING_SNAKE_CASE
- **Private members**: Leading underscore (_privateMethod)

## Flutter Development Standards

### Widget Best Practices
```dart
// ✅ Good: Efficient Flutter widget
class UserProfileView extends ConsumerWidget {
  const UserProfileView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProfileProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
      ),
      body: userAsync.when(
        data: (user) => _buildProfileContent(user),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => ErrorWidget(error.toString()),
      ),
    );
  }

  Widget _buildProfileContent(User user) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ProfileHeader(user: user),
          const SizedBox(height: 24),
          ProfileStats(stats: user.stats),
          const SizedBox(height: 24),
          ProfileActions(user: user),
        ],
      ),
    );
  }
}
```

### State Management with Riverpod
```dart
// User repository provider
final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepositoryImpl(
    apiService: ref.watch(apiServiceProvider),
    localStorage: ref.watch(localStorageProvider),
  );
});

// User profile provider
final userProfileProvider = AsyncNotifierProvider<UserProfileNotifier, User>(
  UserProfileNotifier.new,
);

class UserProfileNotifier extends AsyncNotifier<User> {
  @override
  Future<User> build() async {
    return await ref.read(userRepositoryProvider).getCurrentUser();
  }

  Future<void> updateProfile(User updatedUser) async {
    state = const AsyncLoading();

    state = await AsyncValue.guard(() async {
      await ref.read(userRepositoryProvider).updateUser(updatedUser);
      return updatedUser;
    });
  }
}
```

### Performance Guidelines
- **const constructors**: Use const for immutable widgets
- **Builder patterns**: Use builder widgets for large lists
- **Image optimization**: Implement proper image caching
- **Animation optimization**: Use AnimationController properly
- **Memory management**: Dispose controllers and subscriptions
- **Bundle size**: Minimize dependencies and assets

### Cross-Platform Considerations
```dart
// Platform-specific behavior
Widget getPlatformButton(String text, VoidCallback onPressed) {
  if (Platform.isIOS) {
    return CupertinoButton(
      onPressed: onPressed,
      child: Text(text),
    );
  } else {
    return ElevatedButton(
      onPressed: onPressed,
      child: Text(text),
    );
  }
}

// Responsive design
class ResponsiveLayout extends StatelessWidget {
  final Widget mobile;
  final Widget? tablet; 
  final Widget? desktop;

  const ResponsiveLayout({
    super.key,
    required this.mobile,
    this.tablet,
    this.desktop,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth >= 1200) {
          return desktop ?? tablet ?? mobile;
        } else if (constraints.maxWidth >= 768) {
          return tablet ?? mobile;
        }
        return mobile;
      },
    );
  }
}
```

## Testing Strategy

### Widget Testing
```dart
void main() {
  group('UserProfileView', () {
    testWidgets('displays user information correctly', (tester) async {
      final container = ProviderContainer(
        overrides: [
          userProfileProvider.overrideWith(() => MockUserProfileNotifier()),
        ],
      );

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: UserProfileView(),
          ),
        ),
      );

      expect(find.text('John Doe'), findsOneWidget);
      expect(find.byType(ProfileHeader), findsOneWidget);
    });
  });
}
```

### Integration Testing
- **E2E flows**: Complete user journeys across platforms
- **Platform testing**: iOS and Android specific behaviors
- **Performance testing**: Frame rate, memory usage
- **Network testing**: Various connectivity conditions

## Deployment Guidelines

### Build Configuration
- **Debug**: Development with hot reload
- **Profile**: Performance profiling build
- **Release**: Production-optimized build
- **Flavors**: Different environments (dev, staging, prod)

### Platform-Specific Builds
```yaml
# Android
flutter build appbundle --release --target-platform android-arm,android-arm64

# iOS  
flutter build ios --release --no-codesign
```

### Store Submission
- **Google Play**: AAB format, signed release
- **App Store**: IPA format, proper provisioning
- **Metadata**: Platform-specific store listings
- **Screenshots**: Device-specific screenshots for both stores

## AI Agent Integration

When working with MobileKit Flutter agents:

### Agent Collaboration
- **Sequential**: flutter-planner → flutter-researcher → widget-designer → flutter-tester
- **Parallel**: widget-designer + flutter-data-architect for complex features
- **Review cycle**: dart-reviewer → flutter-debugger for quality assurance

### Context Sharing
- Always reference this CLAUDE.md for project-specific configuration
- Use `plans/` directory for implementation plans and progress tracking
- Document decisions in `docs/` for future reference

### Quality Gates
- Code must pass `dart-reviewer` analysis
- All features must have corresponding tests from `flutter-tester`
- Performance benchmarks validated by `flutter-debugger`
- Cross-platform compatibility verified by `flutter-release-manager`

## File Boundaries

### What to Generate
- Dart source files (.dart)
- Flutter widgets and screens
- Unit tests and widget tests
- pubspec.yaml dependencies
- Asset configurations
- Platform-specific configurations

### What NOT to Modify
- Build outputs and generated files
- Platform-specific native code (unless required)
- IDE-specific files and configurations
- Third-party package source files
- Git and version control files

## Flutter-Specific Considerations

### Material Design Guidelines
- Follow Material Design 3 principles
- Use Material components and theming
- Implement proper color schemes and typography
- Support dark mode and dynamic colors

### Cross-Platform Best Practices
- Design for both iOS and Android platforms
- Handle platform differences gracefully
- Optimize for different screen sizes and orientations
- Consider platform-specific UI patterns when needed

### Performance Optimization
- Minimize widget rebuilds with proper state management
- Use efficient list rendering techniques
- Optimize image loading and caching
- Profile and monitor app performance regularly

---

**Remember**: You are building a **cross-platform Flutter application** using Dart and modern Flutter practices. Always prioritize performance, user experience, and platform-appropriate design patterns.

When in doubt, consult the Flutter agents for framework-specific guidance and best practices.
