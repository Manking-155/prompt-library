# State Management with GetX - Examples

## Overview

GetX provides a simple and reactive state management solution. This guide shows common patterns and usage.

## Basic Controller

### Simple Reactive State

```dart
class CounterController extends GetxController {
  final count = 0.obs;
  
  void increment() => count.value++;
  void decrement() => count.value--;
}

// Usage
class CounterPage extends StatelessWidget {
  const CounterPage({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GetBuilder<CounterController>(
        builder: (controller) => Obx(
          () => Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('Count: ${controller.count.value}'),
                ElevatedButton(
                  onPressed: controller.increment,
                  child: const Text('Increment'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

## Observable Types

### Simple Types

```dart
class UserController extends GetxController {
  // Primitive types
  final name = ''.obs;
  final age = 0.obs;
  final isActive = false.obs;
  final score = 0.0.obs;
  
  void updateName(String newName) => name.value = newName;
  void updateAge(int newAge) => age.value = newAge;
}

// Usage
controller.name.value = 'John';
controller.age.value = 30;
```

### Nullable Types

```dart
class UserController extends GetxController {
  // Nullable types use Rxn<T>
  final user = Rxn<User>();
  final profile = Rxn<Profile>();
  
  void selectUser(User? newUser) => user.value = newUser;
  void clearUser() => user.value = null;
}

// Safe usage
if (controller.user.value != null) {
  print(controller.user.value!.name);
}

// Or use optional chaining
print(controller.user.value?.name ?? 'No user');
```

### Collections

```dart
class TodoController extends GetxController {
  // Lists
  final todos = <Todo>[].obs;
  
  // Maps
  final data = <String, dynamic>{}.obs;
  
  // Sets
  final tags = <String>{}.obs;
  
  void addTodo(Todo todo) {
    todos.add(todo);  // Automatically notifies listeners
  }
  
  void removeTodo(int index) {
    todos.removeAt(index);
  }
  
  void updateData(String key, dynamic value) {
    data[key] = value;
    data.refresh();  // Force update if needed
  }
}

// Usage
controller.todos.add(Todo(title: 'New Task'));
controller.todos.length;
controller.todos.isEmpty;
controller.todos.clear();
```

## Reactive Operations

### Computed Values

```dart
class UserController extends GetxController {
  final firstName = ''.obs;
  final lastName = ''.obs;
  
  // Computed - automatically recomputes when dependencies change
  late final fullName = Rx<String>('');
  
  @override
  void onInit() {
    ever(firstName, (_) => _updateFullName());
    ever(lastName, (_) => _updateFullName());
    super.onInit();
  }
  
  void _updateFullName() {
    fullName.value = '${firstName.value} ${lastName.value}';
  }
}

// Better: Use Rxn with getter
class UserController extends GetxController {
  final firstName = ''.obs;
  final lastName = ''.obs;
  
  String get fullName => '${firstName.value} ${lastName.value}';
}
```

### List Operations

```dart
class ShoppingController extends GetxController {
  final items = <Item>[].obs;
  
  // Filter
  List<Item> get activeItems => items.where((item) => item.isActive).toList();
  
  // Map
  List<String> get itemNames => items.map((item) => item.name).toList();
  
  // Sum
  double get totalPrice => items.fold<double>(0, (sum, item) => sum + item.price);
  
  // Any/Every
  bool get hasExpensiveItems => items.any((item) => item.price > 100);
  bool get allInStock => items.every((item) => item.inStock);
}

// Usage
controller.items.add(Item(name: 'Apple', price: 1.5));
controller.items.removeWhere((item) => !item.inStock);
controller.items.sort((a, b) => a.price.compareTo(b.price));
```

## Lifecycle Management

### onInit, onReady, onClose

```dart
class DataController extends GetxController {
  late DatabaseService db;
  late ApiService api;
  
  final data = <String>[].obs;
  StreamSubscription? _subscription;
  
  @override
  void onInit() {
    // Called when controller is created
    // Good for initializing variables
    db = Get.find();
    api = Get.find();
    super.onInit();
  }
  
  @override
  void onReady() {
    // Called after widget is rendered
    // Good for loading initial data
    loadData();
    _subscription = Stream.periodic(Duration(seconds: 5))
      .listen((_) => refreshData());
    super.onReady();
  }
  
  @override
  void onClose() {
    // Called when controller is disposed
    // Good for cleanup
    _subscription?.cancel();
    super.onClose();
  }
  
  Future<void> loadData() async {
    final result = await api.fetchData();
    result.fold(
      (items) => data.value = items,
      (error) => Get.snackbar('Error', error.toString()),
    );
  }
  
  Future<void> refreshData() async {
    await loadData();
  }
}
```

## Workers (Reactive Methods)

### Ever - React to Changes

```dart
class FormController extends GetxController {
  final email = ''.obs;
  final password = ''.obs;
  final isFormValid = false.obs;
  
  @override
  void onInit() {
    // Trigger every time email changes
    ever(email, (_) => _validateForm());
    ever(password, (_) => _validateForm());
    super.onInit();
  }
  
  void _validateForm() {
    isFormValid.value = email.isNotEmpty && password.isNotEmpty;
  }
}
```

### Once - React to First Change

```dart
class AuthController extends GetxController {
  final authToken = Rxn<String>();
  
  @override
  void onInit() {
    // Trigger only first time authToken changes
    once(authToken, (token) {
      if (token != null) {
        Get.offAllNamed('/home');
      }
    });
    super.onInit();
  }
}
```

### Debounce - Delayed Reaction

```dart
class SearchController extends GetxController {
  final searchQuery = ''.obs;
  final searchResults = <String>[].obs;
  
  @override
  void onInit() {
    // Wait 500ms after user stops typing
    debounce(
      searchQuery,
      (_) => _performSearch(),
      time: const Duration(milliseconds: 500),
    );
    super.onInit();
  }
  
  void _performSearch() {
    if (searchQuery.value.isEmpty) {
      searchResults.clear();
      return;
    }
    // Perform search
  }
}
```

### Throttle - Limit Frequency

```dart
class ScrollController extends GetxController {
  final scrollPosition = 0.0.obs;
  
  @override
  void onInit() {
    // Update UI only every 100ms
    throttle(
      scrollPosition,
      (_) => _handleScroll(),
      time: const Duration(milliseconds: 100),
    );
    super.onInit();
  }
  
  void _handleScroll() {
    // Handle scroll logic
  }
}
```

## Advanced Patterns

### Multiple Controllers Communication

```dart
class AuthController extends GetxController {
  final isLoggedIn = false.obs;
  final user = Rxn<User>();
  
  void logout() {
    isLoggedIn.value = false;
    user.value = null;
  }
}

class ProfileController extends GetxController {
  late AuthController _authController;
  
  @override
  void onInit() {
    _authController = Get.find();
    super.onInit();
  }
  
  void deleteAccount() {
    // Perform deletion...
    _authController.logout();  // Trigger logout in other controller
  }
}
```

### Conditional UI Updates

```dart
class PageController extends GetxController {
  final state = 'initial'.obs;
  
  Future<void> loadData() async {
    state.value = 'loading';
    try {
      await Future.delayed(const Duration(seconds: 2));
      state.value = 'success';
    } catch (e) {
      state.value = 'error';
    }
  }
}

class PageView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetBuilder<PageController>(
      builder: (controller) => Obx(
        () {
          switch (controller.state.value) {
            case 'loading':
              return const Center(child: CircularProgressIndicator());
            case 'success':
              return const Center(child: Text('Success'));
            case 'error':
              return const Center(child: Text('Error'));
            default:
              return const SizedBox();
          }
        },
      ),
    );
  }
}
```

### Form State Management

```dart
class LoginController extends GetxController {
  final formKey = GlobalKey<FormState>();
  final email = TextEditingController();
  final password = TextEditingController();
  
  final isLoading = false.obs;
  final emailError = ''.obs;
  final passwordError = ''.obs;
  
  Future<void> login() async {
    if (!formKey.currentState!.validate()) return;
    
    isLoading.value = true;
    
    try {
      final result = await authService.login(email.text, password.text);
      result.fold(
        (_) => Get.offAllNamed('/home'),
        (error) => _handleError(error),
      );
    } finally {
      isLoading.value = false;
    }
  }
  
  void _handleError(Exception error) {
    Get.snackbar('Login Error', error.toString());
  }
  
  @override
  void onClose() {
    email.dispose();
    password.dispose();
    super.onClose();
  }
}

class LoginPage extends StatelessWidget {
  const LoginPage({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return GetBuilder<LoginController>(
      builder: (controller) => Scaffold(
        body: Obx(
          () => Form(
            key: controller.formKey,
            child: Column(
              children: [
                TextField(
                  controller: controller.email,
                  decoration: InputDecoration(
                    hintText: 'Email',
                    errorText: controller.emailError.value.isEmpty
                        ? null
                        : controller.emailError.value,
                  ),
                ),
                TextField(
                  controller: controller.password,
                  obscureText: true,
                  decoration: InputDecoration(
                    hintText: 'Password',
                    errorText: controller.passwordError.value.isEmpty
                        ? null
                        : controller.passwordError.value,
                  ),
                ),
                ElevatedButton(
                  onPressed: controller.isLoading.value ? null : controller.login,
                  child: controller.isLoading.value
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Login'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

## Best Practices

1. **Use GetBuilder for UI updates**: Efficiently rebuilds only when needed
2. **Use Obx for reactive widgets**: Automatically listens to observable changes
3. **Lazy load controllers**: Use `Get.lazyPut()` to avoid unnecessary initialization
4. **Proper cleanup**: Always implement `onClose()` to dispose resources
5. **Avoid nested Obx**: Can impact performance
6. **Type-safe queries**: Use `Get.find<ControllerType>()` for safety
7. **Business logic in controller**: Keep views simple

## Related Documentation
- Clean Architecture Guide: `system/clean_architecture_guide.md`
- Code Standards: `system/code_standards.md`
- Feature Module Template: `templates/feature_module_template.md`
