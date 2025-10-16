# SOP: Routing and Navigation with GetX

## Overview

This Standard Operating Procedure (SOP) outlines the implementation of routing and navigation in our Flutter application using GetX's routing system. This provides a centralized, type-safe, and efficient navigation solution.

## Prerequisites

- GetX package configured
- Understanding of Flutter navigation concepts
- Knowledge of route definitions and page bindings
- GetX navigation principles

## Key Concepts

### Route Types
- **Routes**: Application navigation paths
- **Pages**: Screen definitions with bindings
- **Bindings**: Dependency injection for routes
- **Middleware**: Navigation guards and interceptors
- **Transitions**: Page transition animations

### Navigation Patterns
- **Simple Navigation**: Push new route
- **Tab Navigation**: Switch between tabs
- **Drawer Navigation**: Side drawer navigation
- **Modal Navigation**: Dialogs and bottom sheets
- **Nested Navigation**: Navigation within navigation

## Step-by-Step Process

### Phase 1: Setting Up Navigation Infrastructure

#### 1.1 Create Route Configuration Structure
```bash
lib/
├── app/
│   ├── routes/
│   │   ├── app_pages.dart           # Main route definitions
│   │   ├── app_routes.dart          # Route constants
│   │   ├── bindings/                # Route bindings
│   │   │   ├── home_binding.dart
│   │   │   ├── auth_binding.dart
│   │   │   └── ...
│   │   └── middleware/              # Navigation middleware
│   │       ├── auth_middleware.dart
│   │       └── ...
│   ├── theme/
│   │   └── transitions.dart        # Custom transitions
│   └── navigation/                 # Navigation utilities
│       ├── navigation_service.dart
│       └── route_generator.dart
```

#### 1.2 Define Route Constants
Create file: `lib/app/routes/app_routes.dart`:
```dart
/// Application route paths
abstract class Routes {
  Routes._();

  // Authentication routes
  static const SPLASH = _Paths.SPLASH;
  static const LOGIN = _Paths.LOGIN;
  static const REGISTER = _Paths.REGISTER;
  static const FORGOT_PASSWORD = _Paths.FORGOT_PASSWORD;

  // Main app routes
  static const HOME = _Paths.HOME;
  static const DASHBOARD = _Paths.DASHBOARD;
  static const PROFILE = _Paths.PROFILE;
  static const SETTINGS = _Paths.SETTINGS;

  // Feature routes
  static const USERS = _Paths.USERS;
  static const USER_DETAIL = _Paths.USER_DETAIL;
  static const USER_CREATE = _Paths.USER_CREATE;
  static const USER_EDIT = _Paths.USER_EDIT;

  // Product routes
  static const PRODUCTS = _Paths.PRODUCTS;
  static const PRODUCT_DETAIL = _Paths.PRODUCT_DETAIL;
  static const PRODUCT_CREATE = _Paths.PRODUCT_CREATE;
  static const PRODUCT_EDIT = _Paths.PRODUCT_EDIT;

  // Error routes
  static const NOT_FOUND = _Paths.NOT_FOUND;
  static const SERVER_ERROR = _Paths.SERVER_ERROR;
}

/// Path definitions
abstract class _Paths {
  _Paths._();

  static const SPLASH = '/splash';
  static const LOGIN = '/login';
  static const REGISTER = '/register';
  static const FORGOT_PASSWORD = '/forgot-password';

  static const HOME = '/home';
  static const DASHBOARD = '/dashboard';
  static const PROFILE = '/profile';
  static const SETTINGS = '/settings';

  static const USERS = '/users';
  static const USER_DETAIL = '/users/:id';
  static const USER_CREATE = '/users/create';
  static const USER_EDIT = '/users/:id/edit';

  static const PRODUCTS = '/products';
  static const PRODUCT_DETAIL = '/products/:id';
  static const PRODUCT_CREATE = '/products/create';
  static const PRODUCT_EDIT = '/products/:id/edit';

  static const NOT_FOUND = '/404';
  static const SERVER_ERROR = '/500';
}
```

#### 1.3 Create Custom Transitions
Create file: `lib/app/theme/transitions.dart`:
```dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';

/// Custom page transitions
class AppTransitions {
  /// Fade transition
  static Transition fade() => Transition.fade;

  /// Fade in with duration
  static Transition fadeIn({Duration? duration}) => Transition.fadeIn.copyWith(
        duration: duration ?? const Duration(milliseconds: 300),
      );

  /// Right to left transition
  static Transition rightToLeft() => Transition.rightToLeft;

  /// Left to right transition
  static Transition leftToRight() => Transition.leftToRight;

  /// Top to bottom transition
  static Transition topToBottom() => Transition.topToBottom;

  /// Bottom to top transition
  static Transition bottomToTop() => Transition.bottomToTop;

  /// Scale transition
  static Transition scale() => Transition.scale;

  /// Size transition
  static Transition size() => Transition.size;

  /// Right to left with fade
  static Transition rightToLeftWithFade() => Transition.rightToLeftWithFade;

  /// Left to right with fade
  static Transition leftToRightWithFade() => Transition.leftToRightWithFade;

  /// Custom transition for dialogs
  static Widget dialogTransition(
    BuildContext context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
    Widget child,
  ) {
    return ScaleTransition(
      scale: CurvedAnimation(
        parent: animation,
        curve: Curves.easeOutBack,
      ),
      child: child,
    );
  }

  /// Custom transition for bottom sheets
  static Widget bottomSheetTransition(
    BuildContext context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
    Widget child,
  ) {
    return SlideTransition(
      position: Tween<Offset>(
        begin: const Offset(0, 1),
        end: Offset.zero,
      ).animate(CurvedAnimation(
        parent: animation,
        curve: Curves.easeOutCubic,
      )),
      child: child,
    );
  }
}
```

### Phase 2: Creating Route Bindings

#### 2.1 Create Base Binding
Create file: `lib/app/routes/bindings/base_binding.dart`:
```dart
import 'package:get/get.dart';

/// Base binding with common functionality
abstract class BaseBinding extends Bindings {
  /// Services that should be initialized before the page loads
  Future<void> onInit() async {}

  /// Services that should be disposed when the page is removed
  void onDispose() {}

  @override
  void dependencies() {
    // Initialize dependencies
    onDependencies();
  }

  /// Override this method to register dependencies
  void onDependencies();
}
```

#### 2.2 Create Authentication Binding
Create file: `lib/app/routes/bindings/auth_binding.dart`:
```dart
import 'package:get/get.dart';

import '../../../features/auth/presentation/controllers/login_controller.dart';
import '../../../features/auth/presentation/controllers/register_controller.dart';
import '../../../core/services/auth_service.dart';
import '../../../core/services/navigation_service.dart';

class AuthBinding extends BaseBinding {
  @override
  Future<void> onInit() async {
    // Initialize auth service if needed
    super.onInit();
  }

  @override
  void onDependencies() {
    // Lazy create controllers
    Get.lazyPut<LoginController>(() => LoginController(
      authService: Get.find<AuthService>(),
      navigationService: Get.find<NavigationService>(),
    ));

    Get.lazyPut<RegisterController>(() => RegisterController(
      authService: Get.find<AuthService>(),
      navigationService: Get.find<NavigationService>(),
    ));
  }

  @override
  void onDispose() {
    // Clean up resources if needed
    Get.delete<LoginController>();
    Get.delete<RegisterController>();
    super.onDispose();
  }
}
```

#### 2.3 Create User Feature Binding
Create file: `lib/app/routes/bindings/user_binding.dart`:
```dart
import 'package:get/get.dart';

import '../../../features/user/presentation/controllers/user_controller.dart';
import '../../../features/user/presentation/controllers/user_form_controller.dart';
import '../../../features/user/domain/usecases/get_user.dart';
import '../../../features/user/domain/usecases/get_all_users.dart';
import '../../../features/user/domain/usecases/create_user.dart';
import '../../../features/user/domain/usecases/update_user.dart';
import '../../../features/user/domain/usecases/delete_user.dart';
import '../../../core/services/navigation_service.dart';

class UserBinding extends BaseBinding {
  @override
  void onDependencies() {
    // Controllers
    Get.lazyPut<UserController>(() => UserController(
      getAllUsersUseCase: Get.find<GetAllUsersUseCase>(),
      getUserUseCase: Get.find<GetUserUseCase>(),
      deleteUserUseCase: Get.find<DeleteUserUseCase>(),
      navigationService: Get.find<NavigationService>(),
    ));

    Get.lazyPut<UserFormController>(() => UserFormController(
      createUserUseCase: Get.find<CreateUserUseCase>(),
      updateUserUseCase: Get.find<UpdateUserUseCase>(),
      navigationService: Get.find<NavigationService>(),
    ));
  }

  @override
  void onDispose() {
    Get.delete<UserController>();
    Get.delete<UserFormController>();
    super.onDispose();
  }
}
```

### Phase 3: Implementing Navigation Middleware

#### 3.1 Create Authentication Middleware
Create file: `lib/app/routes/middleware/auth_middleware.dart`:
```dart
import 'package:get/get.dart';

import '../../../core/services/auth_service.dart';
import '../../../core/services/navigation_service.dart';
import '../../routes/app_routes.dart';

/// Middleware to protect routes that require authentication
class AuthMiddleware extends GetMiddleware {
  final AuthService _authService = Get.find<AuthService>();
  final NavigationService _navigationService = Get.find<NavigationService>();

  @override
  RouteSettings? redirect(String? route) {
    // Check if user is authenticated
    if (!_authService.isLoggedIn) {
      // Redirect to login page
      return const RouteSettings(name: Routes.LOGIN);
    }

    // Allow navigation
    return null;
  }

  @override
  int? get priority => 1;

  @override
  List<GetMiddleware>? get onPageCalled => [
    GetMiddleware(
      priority: 0,
      onPageCalled: (GetPage? page) {
        // Log page access for authenticated routes
        print('Accessing authenticated route: ${page?.name}');
      },
    ),
  ];
}
```

#### 3.2 Create Admin Middleware
Create file: `lib/app/routes/middleware/admin_middleware.dart`:
```dart
import 'package:get/get.dart';

import '../../../core/services/auth_service.dart';
import '../../routes/app_routes.dart';

/// Middleware to protect admin-only routes
class AdminMiddleware extends GetMiddleware {
  final AuthService _authService = Get.find<AuthService>();

  @override
  RouteSettings? redirect(String? route) {
    // Check if user is authenticated and is admin
    if (!_authService.isLoggedIn || !_authService.currentUser?.isAdmin ?? false) {
      // Redirect to home or access denied page
      return const RouteSettings(name: Routes.HOME);
    }

    return null;
  }

  @override
  int? get priority => 2; // Higher priority than auth middleware
}
```

#### 3.3 Create Logging Middleware
Create file: `lib/app/routes/middleware/logging_middleware.dart`:
```dart
import 'package:get/get.dart';

import '../../../core/services/logger_service.dart';

/// Middleware to log all navigation events
class LoggingMiddleware extends GetMiddleware {
  final LoggerService _logger = Get.find<LoggerService>();

  @override
  GetPage? onPageCalled(GetPage? page) {
    if (page != null) {
      _logger.info('Navigating to: ${page.name}');
    }
    return page;
  }

  @override
  void onPageDispose(String pageName) {
    _logger.info('Disposing page: $pageName');
    super.onPageDispose(pageName);
  }
}
```

### Phase 4: Configuring App Routes

#### 4.1 Create Main Pages Configuration
Create file: `lib/app/routes/app_pages.dart`:
```dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'app_routes.dart';
import 'bindings/auth_binding.dart';
import 'bindings/user_binding.dart';
import 'bindings/home_binding.dart';
import 'middleware/auth_middleware.dart';
import 'middleware/admin_middleware.dart';
import 'middleware/logging_middleware.dart';
import '../../theme/transitions.dart';

import '../../features/splash/presentation/views/splash_view.dart';
import '../../features/auth/presentation/views/login_view.dart';
import '../../features/auth/presentation/views/register_view.dart';
import '../../features/auth/presentation/views/forgot_password_view.dart';
import '../../features/home/presentation/views/home_view.dart';
import '../../features/user/presentation/views/user_list_view.dart';
import '../../features/user/presentation/views/user_detail_view.dart';
import '../../features/user/presentation/views/user_form_view.dart';
import '../../features/error/presentation/views/not_found_view.dart';
import '../../features/error/presentation/views/server_error_view.dart';

/// Application pages configuration
abstract class AppPages {
  AppPages._();

  /// Initial route
  static const INITIAL = Routes.SPLASH;

  /// Application pages
  static final routes = [
    // Splash page
    GetPage(
      name: _Paths.SPLASH,
      page: () => const SplashView(),
      transition: AppTransitions.fade(),
      transitionDuration: const Duration(milliseconds: 500),
      middlewares: [LoggingMiddleware()],
    ),

    // Authentication pages
    GetPage(
      name: _Paths.LOGIN,
      page: () => const LoginView(),
      binding: AuthBinding(),
      transition: AppTransitions.rightToLeft(),
      middlewares: [LoggingMiddleware()],
    ),
    GetPage(
      name: _Paths.REGISTER,
      page: () => const RegisterView(),
      binding: AuthBinding(),
      transition: AppTransitions.rightToLeft(),
      middlewares: [LoggingMiddleware()],
    ),
    GetPage(
      name: _Paths.FORGOT_PASSWORD,
      page: () => const ForgotPasswordView(),
      binding: AuthBinding(),
      transition: AppTransitions.rightToLeft(),
      middlewares: [LoggingMiddleware()],
    ),

    // Main app pages (require authentication)
    GetPage(
      name: _Paths.HOME,
      page: () => const HomeView(),
      binding: HomeBinding(),
      transition: AppTransitions.fade(),
      middlewares: [
        LoggingMiddleware(),
        AuthMiddleware(),
      ],
    ),

    // User management pages (require authentication)
    GetPage(
      name: _Paths.USERS,
      page: () => const UserListView(),
      binding: UserBinding(),
      transition: AppTransitions.rightToLeft(),
      middlewares: [
        LoggingMiddleware(),
        AuthMiddleware(),
      ],
    ),
    GetPage(
      name: _Paths.USER_DETAIL,
      page: () => const UserDetailView(),
      binding: UserBinding(),
      transition: AppTransitions.rightToLeft(),
      middlewares: [
        LoggingMiddleware(),
        AuthMiddleware(),
      ],
    ),
    GetPage(
      name: _Paths.USER_CREATE,
      page: () => const UserFormView(isEdit: false),
      binding: UserBinding(),
      transition: AppTransitions.bottomToTop(),
      middlewares: [
        LoggingMiddleware(),
        AuthMiddleware(),
      ],
    ),
    GetPage(
      name: _Paths.USER_EDIT,
      page: () => const UserFormView(isEdit: true),
      binding: UserBinding(),
      transition: AppTransitions.rightToLeft(),
      middlewares: [
        LoggingMiddleware(),
        AuthMiddleware(),
      ],
    ),

    // Error pages
    GetPage(
      name: _Paths.NOT_FOUND,
      page: () => const NotFoundView(),
      transition: AppTransitions.fade(),
      middlewares: [LoggingMiddleware()],
    ),
    GetPage(
      name: _Paths.SERVER_ERROR,
      page: () => const ServerErrorView(),
      transition: AppTransitions.fade(),
      middlewares: [LoggingMiddleware()],
    ),
  ];

  /// Unknown route handler
  static GetPage unknownRoute = GetPage(
    name: _Paths.NOT_FOUND,
    page: () => const NotFoundView(),
    transition: AppTransitions.fade(),
  );
}
```

### Phase 5: Creating Navigation Service

#### 5.1 Create Navigation Service Interface
Create file: `lib/app/navigation/navigation_service.dart`:
```dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../routes/app_routes.dart';
import '../theme/transitions.dart';

/// Navigation service for centralized navigation logic
abstract class NavigationService {
  /// Navigate to a route
  Future<T?>? toNamed<T>(
    String routeName, {
    Object? arguments,
    Map<String, String>? parameters,
    bool preventDuplicates = false,
    Transition? transition,
    Duration? transitionDuration,
    Curve? curve,
    bool fullscreenDialog = false,
  });

  /// Navigate to route and clear all previous routes
  Future<T?>? offAllNamed<T>(
    String routeName, {
    Object? arguments,
    Map<String, String>? parameters,
    RouteSettings? settings,
    Transition? transition,
    Duration? transitionDuration,
    Curve? curve,
  });

  /// Navigate to route and replace current
  Future<T?>? offNamed<T>(
    String routeName, {
    Object? arguments,
    Map<String, String>? parameters,
    RouteSettings? settings,
    Transition? transition,
    Duration? transitionDuration,
    Curve? curve,
  });

  /// Navigate back
  void back<T>([T? result]);

  /// Get current route
  String? get currentRoute;

  /// Check if can go back
  bool canGoBack();

  /// Show dialog
  Future<T?> showDialog<T>({
    required Widget dialog,
    bool barrierDismissible = true,
    Color? barrierColor,
    String? barrierLabel,
    bool useSafeArea = true,
  });

  /// Show bottom sheet
  Future<T?> showBottomSheet<T>({
    required Widget bottomSheet,
    Color? backgroundColor,
    double? elevation,
    ShapeBorder? shape,
    Clip? clipBehavior,
    bool isScrollControlled = false,
    bool useRootNavigator = false,
    bool isDismissible = true,
    bool enableDrag = true,
  });

  /// Show snackbar
  void showSnackbar(
    String title,
    String message, {
    Duration? duration,
    SnackPosition? snackPosition,
    Color? backgroundColor,
    Color? textColor,
    double? borderRadius,
    Widget? icon,
  });
}
```

#### 5.2 Implement Navigation Service
Create file: `lib/app/navigation/navigation_service_impl.dart`:
```dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'navigation_service.dart';
import '../routes/app_routes.dart';
import '../theme/transitions.dart';

/// Implementation of NavigationService using GetX
class NavigationServiceImpl implements NavigationService {
  @override
  Future<T?>? toNamed<T>(
    String routeName, {
    Object? arguments,
    Map<String, String>? parameters,
    bool preventDuplicates = false,
    Transition? transition,
    Duration? transitionDuration,
    Curve? curve,
    bool fullscreenDialog = false,
  }) {
    return Get.toNamed<T>(
      routeName,
      arguments: arguments,
      parameters: parameters,
      preventDuplicates: preventDuplicates,
      transition: transition ?? AppTransitions.rightToLeft(),
      duration: transitionDuration,
      curve: curve,
      fullscreenDialog: fullscreenDialog,
    );
  }

  @override
  Future<T?>? offAllNamed<T>(
    String routeName, {
    Object? arguments,
    Map<String, String>? parameters,
    RouteSettings? settings,
    Transition? transition,
    Duration? transitionDuration,
    Curve? curve,
  }) {
    return Get.offAllNamed<T>(
      routeName,
      arguments: arguments,
      parameters: parameters,
      settings: settings,
      transition: transition ?? AppTransitions.fade(),
      duration: transitionDuration,
      curve: curve,
    );
  }

  @override
  Future<T?>? offNamed<T>(
    String routeName, {
    Object? arguments,
    Map<String, String>? parameters,
    RouteSettings? settings,
    Transition? transition,
    Duration? transitionDuration,
    Curve? curve,
  }) {
    return Get.offNamed<T>(
      routeName,
      arguments: arguments,
      parameters: parameters,
      settings: settings,
      transition: transition ?? AppTransitions.rightToLeft(),
      duration: transitionDuration,
      curve: curve,
    );
  }

  @override
  void back<T>([T? result]) {
    Get.back<T>(result);
  }

  @override
  String? get currentRoute => Get.currentRoute;

  @override
  bool canGoBack() => Get.navigator.canPop();

  @override
  Future<T?> showDialog<T>({
    required Widget dialog,
    bool barrierDismissible = true,
    Color? barrierColor,
    String? barrierLabel,
    bool useSafeArea = true,
  }) {
    return Get.dialog<T>(
      dialog,
      barrierDismissible: barrierDismissible,
      barrierColor: barrierColor,
      barrierLabel: barrierLabel,
      useSafeArea: useSafeArea,
      transitionCurve: Curves.easeOutBack,
    );
  }

  @override
  Future<T?> showBottomSheet<T>({
    required Widget bottomSheet,
    Color? backgroundColor,
    double? elevation,
    ShapeBorder? shape,
    Clip? clipBehavior,
    bool isScrollControlled = false,
    bool useRootNavigator = false,
    bool isDismissible = true,
    bool enableDrag = true,
  }) {
    return Get.bottomSheet<T>(
      bottomSheet,
      backgroundColor: backgroundColor,
      elevation: elevation,
      shape: shape,
      clipBehavior: clipBehavior,
      isScrollControlled: isScrollControlled,
      useRootNavigator: useRootNavigator,
      isDismissible: isDismissible,
      enableDrag: enableDrag,
      enterBottomSheetDuration: const Duration(milliseconds: 300),
      exitBottomSheetDuration: const Duration(milliseconds: 200),
    );
  }

  @override
  void showSnackbar(
    String title,
    String message, {
    Duration? duration,
    SnackPosition? snackPosition,
    Color? backgroundColor,
    Color? textColor,
    double? borderRadius,
    Widget? icon,
  }) {
    Get.snackbar(
      title,
      message,
      duration: duration ?? const Duration(seconds: 3),
      snackPosition: snackPosition ?? SnackPosition.TOP,
      backgroundColor: backgroundColor ?? Colors.grey[800],
      colorText: textColor ?? Colors.white,
      borderRadius: borderRadius ?? 8,
      icon: icon,
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
    );
  }
}
```

### Phase 6: Navigation Utilities

#### 6.1 Create Route Arguments Helper
Create file: `lib/app/navigation/route_arguments.dart`:
```dart
import 'package:get/get.dart';

/// Helper class for managing route arguments
class RouteArguments {
  static const String userIdKey = 'userId';
  static const String productIdKey = 'productId';
  static const String editModeKey = 'editMode';
  static const String returnUrlKey = 'returnUrl';

  /// Get user ID from arguments
  static String? getUserId() {
    return Get.parameters[userIdKey] ?? Get.arguments as String?;
  }

  /// Get product ID from arguments
  static String? getProductId() {
    return Get.parameters[productIdKey] ?? Get.arguments as String?;
  }

  /// Get edit mode from arguments
  static bool getEditMode() {
    return Get.parameters[editModeKey] == 'true' || Get.arguments as bool? ?? false;
  }

  /// Get return URL from arguments
  static String? getReturnUrl() {
    return Get.parameters[returnUrlKey] ?? Get.arguments as String?;
  }

  /// Create arguments for user routes
  static Map<String, String> createUserArgs(String userId, {String? returnUrl}) {
    final args = {userIdKey: userId};
    if (returnUrl != null) {
      args[returnUrlKey] = returnUrl;
    }
    return args;
  }

  /// Create arguments for product routes
  static Map<String, String> createProductArgs(String productId, {bool editMode = false}) {
    return {
      productIdKey: productId,
      if (editMode) editModeKey: 'true',
    };
  }
}
```

#### 6.2 Create Navigation Helper
Create file: `lib/app/navigation/navigation_helper.dart`:
```dart
import 'package:get/get.dart';

import '../routes/app_routes.dart';
import 'navigation_service.dart';
import 'route_arguments.dart';

/// Helper methods for common navigation patterns
class NavigationHelper {
  static final NavigationService _navigation = Get.find<NavigationService>();

  /// Authentication navigation
  static Future<void> goToLogin({String? returnUrl}) {
    final args = returnUrl != null
        ? {RouteArguments.returnUrlKey: returnUrl}
        : null;
    return _navigation.toNamed(Routes.LOGIN, arguments: args);
  }

  static Future<void> goToRegister() {
    return _navigation.toNamed(Routes.REGISTER);
  }

  static Future<void> goToForgotPassword() {
    return _navigation.toNamed(Routes.FORGOT_PASSWORD);
  }

  /// Main app navigation
  static Future<void> goToHome() {
    return _navigation.offAllNamed(Routes.HOME);
  }

  static Future<void> goToDashboard() {
    return _navigation.toNamed(Routes.DASHBOARD);
  }

  /// User management navigation
  static Future<void> goToUsers() {
    return _navigation.toNamed(Routes.USERS);
  }

  static Future<void> goToUserDetail(String userId, {String? returnUrl}) {
    return _navigation.toNamed(
      Routes.USER_DETAIL,
      parameters: RouteArguments.createUserArgs(userId, returnUrl: returnUrl),
    );
  }

  static Future<void> goToCreateUser() {
    return _navigation.toNamed(Routes.USER_CREATE);
  }

  static Future<void> goToEditUser(String userId) {
    return _navigation.toNamed(
      Routes.USER_EDIT,
      parameters: RouteArguments.createUserArgs(userId),
    );
  }

  /// Product navigation
  static Future<void> goToProducts() {
    return _navigation.toNamed(Routes.PRODUCTS);
  }

  static Future<void> goToProductDetail(String productId, {bool editMode = false}) {
    return _navigation.toNamed(
      Routes.PRODUCT_DETAIL,
      parameters: RouteArguments.createProductArgs(productId, editMode: editMode),
    );
  }

  static Future<void> goToCreateProduct() {
    return _navigation.toNamed(Routes.PRODUCT_CREATE);
  }

  static Future<void> goToEditProduct(String productId) {
    return _navigation.toNamed(
      Routes.PRODUCT_EDIT,
      parameters: RouteArguments.createProductArgs(productId, editMode: true),
    );
  }

  /// Profile navigation
  static Future<void> goToProfile() {
    return _navigation.toNamed(Routes.PROFILE);
  }

  static Future<void> goToSettings() {
    return _navigation.toNamed(Routes.SETTINGS);
  }

  /// Error navigation
  static Future<void> goToNotFound() {
    return _navigation.toNamed(Routes.NOT_FOUND);
  }

  static Future<void> goToServerError() {
    return _navigation.toNamed(Routes.SERVER_ERROR);
  }

  /// Utility methods
  static void goBack() {
    _navigation.back();
  }

  static void goBackToLogin() {
    _navigation.offAllNamed(Routes.LOGIN);
  }

  static Future<void> goBackAndRefresh() {
    final returnUrl = RouteArguments.getReturnUrl();
    if (returnUrl != null) {
      _navigation.offAllNamed(returnUrl);
    } else {
      _navigation.back();
    }
  }
}
```

### Phase 7: Using Navigation in Components

#### 7.1 Navigation in Controllers
```dart
// lib/features/user/presentation/controllers/user_controller.dart
import 'package:get/get.dart';

import '../../../app/navigation/navigation_helper.dart';
import '../../../core/services/navigation_service.dart';

class UserController extends GetxController {
  final NavigationService _navigationService = Get.find<NavigationService>();

  Future<void> navigateToUserDetail(String userId) async {
    await NavigationHelper.goToUserDetail(userId);
  }

  Future<void> navigateToCreateUser() async {
    await NavigationHelper.goToCreateUser();
  }

  Future<void> navigateToEditUser(String userId) async {
    await NavigationHelper.goToEditUser(userId);
  }

  void navigateBack() {
    _navigationService.back();
  }

  void navigateToHome() {
    NavigationHelper.goToHome();
  }

  Future<void> showUserDeleteDialog(String userId) async {
    final result = await _navigationService.showDialog<bool>(
      AlertDialog(
        title: const Text('Delete User'),
        content: const Text('Are you sure you want to delete this user?'),
        actions: [
          TextButton(
            onPressed: () => _navigationService.back(false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => _navigationService.back(true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (result == true) {
      await deleteUser(userId);
    }
  }

  Future<void> showUserFormBottomSheet({String? userId}) async {
    await _navigationService.showBottomSheet(
      UserFormBottomSheet(userId: userId),
      isScrollControlled: true,
      enableDrag: true,
    );
  }

  void showSuccessMessage(String message) {
    _navigationService.showSnackbar(
      'Success',
      message,
      icon: const Icon(Icons.check_circle, color: Colors.green),
    );
  }

  void showErrorMessage(String message) {
    _navigationService.showSnackbar(
      'Error',
      message,
      icon: const Icon(Icons.error, color: Colors.red),
    );
  }
}
```

#### 7.2 Navigation in Views
```dart
// lib/features/user/presentation/views/user_list_view.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../controllers/user_controller.dart';
import '../../../app/navigation/navigation_helper.dart';

class UserListView extends GetView<UserController> {
  const UserListView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Users'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => controller.navigateToCreateUser(),
            tooltip: 'Add User',
          ),
        ],
      ),
      body: Obx(() {
        if (controller.isLoading.value) {
          return const Center(child: CircularProgressIndicator());
        }

        return ListView.builder(
          itemCount: controller.users.length,
          itemBuilder: (context, index) {
            final user = controller.users[index];
            return UserListTile(
              user: user,
              onTap: () => controller.navigateToUserDetail(user.id),
              onEdit: () => controller.navigateToEditUser(user.id),
              onDelete: () => controller.showUserDeleteDialog(user.id),
            );
          },
        );
      }),
      floatingActionButton: FloatingActionButton(
        onPressed: () => controller.navigateToCreateUser(),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### Phase 8: Deep Linking

#### 8.1 Configure Deep Linking
```dart
// lib/app/navigation/deep_link_handler.dart
import 'package:get/get.dart';

import '../routes/app_routes.dart';
import 'navigation_helper.dart';

/// Handle deep links and app links
class DeepLinkHandler {
  static Future<void> handleIncomingLink(String link) async {
    try {
      final uri = Uri.parse(link);

      switch (uri.path) {
        case '/users':
          if (uri.pathSegments.length > 1) {
            final userId = uri.pathSegments[1];
            await NavigationHelper.goToUserDetail(userId);
          } else {
            await NavigationHelper.goToUsers();
          }
          break;

        case '/products':
          if (uri.pathSegments.length > 1) {
            final productId = uri.pathSegments[1];
            await NavigationHelper.goToProductDetail(productId);
          } else {
            await NavigationHelper.goToProducts();
          }
          break;

        case '/reset-password':
          final token = uri.queryParameters['token'];
          if (token != null) {
            await NavigationHelper.goToForgotPassword();
          }
          break;

        default:
          await NavigationHelper.goToNotFound();
      }
    } catch (e) {
      await NavigationHelper.goToNotFound();
    }
  }

  /// Generate shareable links
  static String generateUserLink(String userId) {
    return 'https://yourapp.com/users/$userId';
  }

  static String generateProductLink(String productId) {
    return 'https://yourapp.com/products/$productId';
  }
}
```

### Phase 9: Testing Navigation

#### 9.1 Test Navigation Service
```dart
// test/app/navigation/navigation_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:get/get.dart';
import 'package:mockito/mockito.dart';

import 'package:your_app/app/navigation/navigation_service.dart';
import 'package:your_app/app/routes/app_routes.dart';

class MockGetNavigation extends Mock {
  @override
  Future<T?>? toNamed<T>(String routeName, {Object? arguments}) =>
      super.noSuchMethod(Invocation.method(#toNamed, [routeName], {#arguments: arguments}));

  @override
  void back<T>([T? result]) => super.noSuchMethod(Invocation.method(#back, [], {#result: result}));
}

void main() {
  group('NavigationService', () {
    late NavigationService navigationService;

    setUp(() {
      Get.testMode = true;
      navigationService = NavigationServiceImpl();
    });

    test('should navigate to route', () {
      // Act
      navigationService.toNamed(Routes.HOME);

      // Assert
      verify(Get.toNamed(Routes.HOME)).called(1);
    });

    test('should navigate back', () {
      // Act
      navigationService.back();

      // Assert
      verify(Get.back()).called(1);
    });
  });
}
```

## Verification Checklist

### Configuration
- [ ] All routes defined in AppPages
- [ ] Route constants defined
- [ ] Bindings created for all routes
- [ ] Middleware configured correctly
- [ ] Transitions defined

### Functionality
- [ ] Navigation works between all routes
- [ ] Parameters passed correctly
- [ ] Deep links handled properly
- [ ] Middleware applied correctly
- [ ] Error routes work

### User Experience
- [ ] Transitions are smooth
- [ ] Back navigation works
- [ ] Loading states shown
- [ ] Error handling in place
- [ ] Consistent navigation behavior

## Best Practices

1. **Use centralized navigation service** for consistent behavior
2. **Define route constants** to avoid string typos
3. **Use middleware for authentication** and authorization
4. **Implement proper error routing** for invalid routes
5. **Use semantic route names** that describe their purpose
6. **Handle deep links** for better user experience
7. **Test navigation flows** thoroughly
8. **Document navigation patterns** for the team

## Common Issues and Solutions

### Issue: Routes not found
**Solution**: Ensure routes are properly defined in AppPages and route constants match.

### Issue: Middleware not working
**Solution**: Check middleware priority and ensure it's properly attached to routes.

### Issue: Arguments not passed correctly
**Solution**: Use RouteArguments helper and ensure proper parameter handling.

### Issue: Navigation not disposing controllers
**Solution**: Implement proper binding disposal and use Get.off() when appropriate.

## Resources

- [GetX Navigation Documentation](https://pub.dev/packages/get#navigation)
- [Flutter Navigation](https://flutter.dev/docs/cookbook/navigation)
- [Deep Linking in Flutter](https://flutter.dev/docs/cookbook/navigation/navigation-with-arguments)