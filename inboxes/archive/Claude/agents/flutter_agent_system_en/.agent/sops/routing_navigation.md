# SOP: Routing & Navigation with GetX

## Overview
This document describes how to set up and manage app routing using GetX Router.

## Basic Setup

### 1. Create Routes Configuration

File: `lib/routes/app_routes.dart`

```dart
abstract class AppRoutes {
  // Splash & Auth
  static const SPLASH_ROUTE = '/';
  static const LOGIN_ROUTE = '/login';
  static const REGISTER_ROUTE = '/register';
  static const FORGOT_PASSWORD_ROUTE = '/forgot-password';
  
  // Main
  static const HOME_ROUTE = '/home';
  static const PROFILE_ROUTE = '/profile';
  
  // Features
  static const FLASHCARD_LIST_ROUTE = '/flashcards';
  static const FLASHCARD_DETAIL_ROUTE = '/flashcards/:id';
  static const FLASHCARD_STUDY_ROUTE = '/flashcards/:id/study';
  
  // Settings
  static const SETTINGS_ROUTE = '/settings';
  static const ABOUT_ROUTE = '/about';
}
```

### 2. Create Pages Configuration

File: `lib/routes/app_pages.dart`

```dart
import 'package:get/get.dart';
import 'package:flutter/material.dart';
import 'package:auth/auth.dart';
import 'package:flashcard/flashcard.dart';

class AppPages {
  static final pages = [
    GetPage(
      name: AppRoutes.SPLASH_ROUTE,
      page: () => const SplashPage(),
      transition: Transition.fade,
    ),
    GetPage(
      name: AppRoutes.LOGIN_ROUTE,
      page: () => const LoginPage(),
      binding: LoginBinding(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: AppRoutes.HOME_ROUTE,
      page: () => const HomePage(),
      binding: HomeBinding(),
      transition: Transition.rightToLeft,
      middlewares: [AuthMiddleware()],
    ),
    GetPage(
      name: AppRoutes.FLASHCARD_LIST_ROUTE,
      page: () => const FlashcardListPage(),
      binding: FlashcardBinding(),
      transition: Transition.rightToLeft,
      middlewares: [AuthMiddleware()],
    ),
    GetPage(
      name: AppRoutes.FLASHCARD_DETAIL_ROUTE,
      page: () => FlashcardDetailPage(
        id: Get.parameters['id'] ?? '',
      ),
      binding: FlashcardBinding(),
      transition: Transition.rightToLeft,
      middlewares: [AuthMiddleware()],
    ),
  ];
}
```

### 3. Middleware for Protected Routes

File: `lib/routes/middlewares/auth_middleware.dart`

```dart
class AuthMiddleware extends GetMiddleware {
  @override
  int? get priority => 1;
  
  @override
  RouteSettings? redirect(String? route) {
    final authController = Get.find<AuthController>();
    
    if (!authController.isLoggedIn.value) {
      return RouteSettings(name: AppRoutes.LOGIN_ROUTE);
    }
    
    return null;  // Allow navigation
  }
}
```

### 4. Setup in Main App

File: `lib/main.dart`

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await setupServiceLocator();
  
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'Flutter App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      darkTheme: ThemeData.dark(useMaterial3: true),
      themeMode: ThemeMode.system,
      
      // GetX Router
      initialRoute: AppRoutes.SPLASH_ROUTE,
      getPages: AppPages.pages,
      
      // Transitions
      defaultTransition: Transition.cupertino,
      transitionDuration: const Duration(milliseconds: 300),
      
      // Navigation observers
      navigatorObservers: [GetObserver()],
      
      // Home page (fallback)
      home: const SplashPage(),
    );
  }
}
```

## Navigation Methods

### 1. Named Routes (Recommended)

```dart
// Simple navigation
Get.toNamed(AppRoutes.HOME_ROUTE);

// With parameters
Get.toNamed(
  AppRoutes.FLASHCARD_DETAIL_ROUTE,
  arguments: {'id': '123'},
);

// Replace current route
Get.offNamed(AppRoutes.HOME_ROUTE);

// Replace all routes (clear stack)
Get.offAllNamed(AppRoutes.LOGIN_ROUTE);

// Back navigation
Get.back();
Get.back(result: 'some_data');

// Until specific route
Get.until((route) => route.settings.name == AppRoutes.HOME_ROUTE);

// Pop multiple routes
Get.back();  // Pop once
Get.back();  // Pop again
```

### 2. Access Parameters

```dart
class FlashcardDetailPage extends StatelessWidget {
  final String id;
  
  const FlashcardDetailPage({required this.id});
  
  @override
  Widget build(BuildContext context) {
    // Access from route parameters
    final routeId = Get.parameters['id'];
    
    // Or use constructor parameter
    return Scaffold(
      appBar: AppBar(title: Text('Flashcard: $id')),
    );
  }
}
```

### 3. With Data Flow

```dart
// Send data to next page
final result = await Get.toNamed<String>(
  AppRoutes.PROFILE_ROUTE,
  arguments: {'userId': '123'},
);

// Receive and use result
print('User result: $result');
```

## Advanced Navigation

### Dynamic Route Parameters

```dart
// Define with parameters
GetPage(
  name: AppRoutes.FLASHCARD_STUDY_ROUTE,  // /flashcards/:id/study
  page: () {
    final id = Get.parameters['id'] ?? '';
    return FlashcardStudyPage(flashcardId: id);
  },
)

// Navigate with parameters
Get.toNamed(
  AppRoutes.FLASHCARD_STUDY_ROUTE.replaceAll(':id', '123'),
);
```

### Query Parameters

```dart
// Navigate with query params
Get.toNamed(
  '${AppRoutes.FLASHCARD_LIST_ROUTE}?category=spanish&level=beginner',
);

// Access query parameters
final category = Get.parameters['category'] ?? '';
final level = Get.parameters['level'] ?? '';
```

### Transitions & Animations

```dart
// Different transition types
Get.toNamed(
  AppRoutes.HOME_ROUTE,
  transition: Transition.fadeIn,        // Fade
  duration: const Duration(ms: 800),
);

Get.toNamed(
  AppRoutes.HOME_ROUTE,
  transition: Transition.rightToLeft,   // Slide
);

Get.toNamed(
  AppRoutes.HOME_ROUTE,
  transition: Transition.upToDown,      // Vertical
);

Get.toNamed(
  AppRoutes.HOME_ROUTE,
  transition: Transition.cupertino,     // iOS style
);

Get.toNamed(
  AppRoutes.HOME_ROUTE,
  transition: Transition.native,        // Native platform
);

// Custom transition
Get.toNamed(
  AppRoutes.HOME_ROUTE,
  customTransition: CustomPageTransition(),
);
```

### Dialog & Bottom Sheet Navigation

```dart
// Dialog
Get.dialog(
  AlertDialog(
    title: const Text('Confirm'),
    content: const Text('Are you sure?'),
    actions: [
      TextButton(
        onPressed: () => Get.back(),
        child: const Text('Cancel'),
      ),
      TextButton(
        onPressed: () {
          Get.back(result: true);
        },
        child: const Text('OK'),
      ),
    ],
  ),
);

// Bottom Sheet
Get.bottomSheet(
  Container(
    color: Colors.white,
    child: ListView(
      children: [
        ListTile(
          title: const Text('Option 1'),
          onTap: () {
            Get.back(result: 'option1');
          },
        ),
        ListTile(
          title: const Text('Option 2'),
          onTap: () {
            Get.back(result: 'option2');
          },
        ),
      ],
    ),
  ),
  backgroundColor: Colors.white,
  shape: const RoundedRectangleBorder(
    borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
  ),
  isScrollControlled: true,
);

// Snackbar
Get.snackbar(
  'Success',
  'Operation completed',
  snackPosition: SnackPosition.BOTTOM,
  duration: const Duration(seconds: 3),
  backgroundColor: Colors.green,
  colorText: Colors.white,
);

// Toast
Get.snackbar(
  '',
  'Quick notification',
  snackPosition: SnackPosition.TOP,
  backgroundColor: Colors.grey,
  colorText: Colors.white,
  messageText: const Text(''),
);
```

## Route Guards & Middleware

### Authentication Middleware

```dart
class AuthMiddleware extends GetMiddleware {
  @override
  int? get priority => 1;
  
  @override
  RouteSettings? redirect(String? route) {
    final authController = Get.find<AuthController>();
    
    if (!authController.isLoggedIn.value) {
      // Store intended route
      authController.intendedRoute = route;
      return RouteSettings(name: AppRoutes.LOGIN_ROUTE);
    }
    
    return null;  // Allow
  }
}
```

### Permission Middleware

```dart
class PermissionMiddleware extends GetMiddleware {
  @override
  int? get priority => 2;
  
  @override
  RouteSettings? redirect(String? route) {
    final userController = Get.find<UserController>();
    
    if (route == AppRoutes.ADMIN_ROUTE && !userController.isAdmin) {
      Get.snackbar('Error', 'Admin access required');
      return RouteSettings(name: AppRoutes.HOME_ROUTE);
    }
    
    return null;
  }
}

// Usage
GetPage(
  name: AppRoutes.ADMIN_ROUTE,
  page: () => const AdminPage(),
  middlewares: [AuthMiddleware(), PermissionMiddleware()],
)
```

## Deep Linking

```dart
// Setup deep links in GetMaterialApp
GetMaterialApp(
  deepLinkingStrategy: DeepLinkingStrategy.path,
  initialRoute: AppRoutes.SPLASH_ROUTE,
  getPages: AppPages.pages,
  navigatorObservers: [
    GetObserver(),
    FirebaseAnalyticsObserver(analytics: analytics),
  ],
)

// Deep link examples
// myapp://flashcards/123
// myapp://profile?userId=456
// myapp://settings
```

## Controller-Based Navigation

```dart
class AuthController extends GetxController {
  late AuthService authService;
  
  @override
  void onInit() {
    authService = Get.find();
    _checkAuthStatus();
    super.onInit();
  }
  
  void _checkAuthStatus() {
    ever(isLoggedIn, (loggedIn) {
      if (loggedIn) {
        Get.offAllNamed(AppRoutes.HOME_ROUTE);
      } else {
        Get.offAllNamed(AppRoutes.LOGIN_ROUTE);
      }
    });
  }
  
  Future<void> logout() async {
    await authService.logout();
    isLoggedIn.value = false;
  }
}
```

## Best Practices

1. **Use named routes**: Better readability and type safety
2. **Centralize routes**: Keep all route definitions in one place
3. **Use middlewares**: For authentication and permissions
4. **Provide context**: Include meaningful data in navigation
5. **Handle back button**: Use appropriate transitions
6. **Test navigation**: Write tests for route changes
7. **Deep linking**: Support external navigation
8. **Clear naming**: Use descriptive route names

## Troubleshooting

### Route not found
```dart
// Check route definition in AppPages
// Ensure exact match with route name
GetPage(
  name: '/flashcards/detail/:id',  // Must match exactly
  page: () => const FlashcardDetailPage(),
)
```

### Parameters not accessible
```dart
// Ensure parameters are passed correctly
Get.toNamed(
  AppRoutes.FLASHCARD_DETAIL_ROUTE.replaceAll(':id', '123'),
);

// Access in page
final id = Get.parameters['id'];
```

### Back button not working
```dart
// Add back navigation handler
@override
void onWillPop() async {
  if (await showConfirmDialog()) {
    Get.back();
  }
}
```

## Related Documentation
- Adding New Feature: `sops/adding_new_feature.md`
- Code Standards: `system/code_standards.md`
- State Management: `templates/state_management_example.md`
