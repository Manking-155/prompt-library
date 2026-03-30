# GetX State Management Examples

## Overview

This document provides comprehensive examples of GetX state management patterns commonly used in our Flutter application. GetX offers three main approaches: Simple State Management, Reactive State Management, and Dependency Injection.

## GetX State Management Types

### 1. Simple State Management (GetBuilder)
Best for simple UI updates that don't require complex state management.

### 2. Reactive State Management (Obx)
Best for reactive UI that automatically updates when state changes.

### 3. Dependency Injection (Get.put/Get.find)
Best for services and controllers that need to be shared across the app.

## Example 1: Counter App (Simple State Management)

### Controller
```dart
// controllers/counter_controller.dart
import 'package:get/get.dart';

class CounterController extends GetxController {
  int count = 0;

  void increment() {
    count++;
    update(); // Rebuild only the widgets using GetBuilder<CounterController>
  }

  void decrement() {
    count--;
    update();
  }

  void reset() {
    count = 0;
    update();
  }
}
```

### View
```dart
// views/counter_view.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/counter_controller.dart';

class CounterView extends StatelessWidget {
  const CounterView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Initialize the controller
    final controller = Get.put(CounterController());

    return Scaffold(
      appBar: AppBar(title: const Text('Counter App')),
      body: Center(
        child: GetBuilder<CounterController>(
          // Only this widget rebuilds when update() is called
          builder: (controller) => Text(
            'Count: ${controller.count}',
            style: const TextStyle(fontSize: 24),
          ),
        ),
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            heroTag: "increment",
            onPressed: controller.increment,
            child: const Icon(Icons.add),
          ),
          const SizedBox(height: 10),
          FloatingActionButton(
            heroTag: "decrement",
            onPressed: controller.decrement,
            child: const Icon(Icons.remove),
          ),
          const SizedBox(height: 10),
          FloatingActionButton(
            heroTag: "reset",
            onPressed: controller.reset,
            child: const Icon(Icons.refresh),
          ),
        ],
      ),
    );
  }
}
```

## Example 2: Todo List (Reactive State Management)

### Controller
```dart
// controllers/todo_controller.dart
import 'package:get/get.dart';

class Todo {
  String id;
  String title;
  bool completed;
  DateTime createdAt;

  Todo({
    required this.id,
    required this.title,
    this.completed = false,
    required this.createdAt,
  });
}

class TodoController extends GetxController {
  // Reactive list
  final todos = <Todo>[].obs;

  // Reactive variables
  final newTodoTitle = ''.obs;
  final isLoading = false.obs;
  final filter = 'all'.obs; // 'all', 'active', 'completed'

  // Computed property
  List<Todo> get filteredTodos {
    switch (filter.value) {
      case 'active':
        return todos.where((todo) => !todo.completed).toList();
      case 'completed':
        return todos.where((todo) => todo.completed).toList();
      default:
        return todos.toList();
    }
  }

  // Getters for computed values
  int get activeCount => todos.where((todo) => !todo.completed).length;
  int get completedCount => todos.where((todo) => todo.completed).length;
  bool get hasCompletedTodos => completedCount > 0;
  String get remainingCountText => '$activeCount items left';

  @override
  void onInit() {
    super.onInit();
    loadTodos();
  }

  void loadTodos() {
    isLoading.value = true;

    // Simulate API call
    Future.delayed(const Duration(seconds: 1), () {
      todos.assignAll([
        Todo(
          id: '1',
          title: 'Learn GetX',
          createdAt: DateTime.now(),
        ),
        Todo(
          id: '2',
          title: 'Build Flutter app',
          createdAt: DateTime.now(),
          completed: true,
        ),
        Todo(
          id: '3',
          title: 'Write documentation',
          createdAt: DateTime.now(),
        ),
      ]);
      isLoading.value = false;
    });
  }

  void addTodo() {
    if (newTodoTitle.value.trim().isEmpty) return;

    final todo = Todo(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: newTodoTitle.value.trim(),
      createdAt: DateTime.now(),
    );

    todos.add(todo);
    newTodoTitle.value = '';
  }

  void toggleTodo(String id) {
    final index = todos.indexWhere((todo) => todo.id == id);
    if (index != -1) {
      todos[index].completed = !todos[index].completed;
      todos.refresh(); // Important for updating object properties
    }
  }

  void deleteTodo(String id) {
    todos.removeWhere((todo) => todo.id == id);
  }

  void updateFilter(String newFilter) {
    filter.value = newFilter;
  }

  void clearCompleted() {
    todos.removeWhere((todo) => todo.completed);
  }

  void toggleAll() {
    final allCompleted = todos.every((todo) => todo.completed);

    for (var todo in todos) {
      todo.completed = !allCompleted;
    }
    todos.refresh();
  }
}
```

### View
```dart
// views/todo_view.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/todo_controller.dart';

class TodoView extends StatelessWidget {
  const TodoView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final controller = Get.put(TodoController());

    return Scaffold(
      appBar: AppBar(
        title: const Text('Todo List'),
        elevation: 0,
      ),
      body: Column(
        children: [
          // Input section
          _buildInputSection(controller),

          // Filter tabs
          _buildFilterTabs(controller),

          // Todo list
          Expanded(
            child: Obx(() {
              if (controller.isLoading.value) {
                return const Center(child: CircularProgressIndicator());
              }

              if (controller.filteredTodos.isEmpty) {
                return const Center(
                  child: Text(
                    'No todos yet',
                    style: TextStyle(fontSize: 18, color: Colors.grey),
                  ),
                );
              }

              return ListView.builder(
                itemCount: controller.filteredTodos.length,
                itemBuilder: (context, index) {
                  final todo = controller.filteredTodos[index];
                  return _buildTodoItem(controller, todo);
                },
              );
            }),
          ),

          // Bottom actions
          _buildBottomActions(controller),
        ],
      ),
    );
  }

  Widget _buildInputSection(TodoController controller) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        children: [
          Obx(
            () => Checkbox(
              value: controller.todos.isNotEmpty &&
                  controller.todos.every((todo) => todo.completed),
              onChanged: (_) => controller.toggleAll(),
            ),
          ),
          Expanded(
            child: TextField(
              onChanged: (value) => controller.newTodoTitle.value = value,
              onSubmitted: (_) => controller.addTodo(),
              decoration: const InputDecoration(
                hintText: 'What needs to be done?',
                border: OutlineInputBorder(),
              ),
            ),
          ),
          const SizedBox(width: 8),
          Obx(
            () => IconButton(
              icon: const Icon(Icons.add),
              onPressed: controller.newTodo.value.trim().isEmpty
                  ? null
                  : controller.addTodo,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFilterTabs(TodoController controller) {
    return Obx(
      () => Row(
        children: [
          _buildFilterTab('All', 'all', controller.filter.value == 'all',
              () => controller.updateFilter('all')),
          _buildFilterTab('Active', 'active', controller.filter.value == 'active',
              () => controller.updateFilter('active')),
          _buildFilterTab('Completed', 'completed',
              controller.filter.value == 'completed',
              () => controller.updateFilter('completed')),
        ],
      ),
    );
  }

  Widget _buildFilterTab(
      String label, String value, bool isSelected, VoidCallback onTap) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: isSelected ? Colors.blue : Colors.transparent,
            border: Border.all(color: Colors.grey),
          ),
          child: Text(
            label,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: isSelected ? Colors.white : Colors.black,
              fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTodoItem(TodoController controller, Todo todo) {
    return Dismissible(
      key: Key(todo.id),
      onDismissed: (_) => controller.deleteTodo(todo.id),
      background: Container(
        color: Colors.red,
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 20),
        child: const Icon(Icons.delete, color: Colors.white),
      ),
      child: ListTile(
        leading: Obx(
          () => Checkbox(
            value: todo.completed,
            onChanged: (_) => controller.toggleTodo(todo.id),
          ),
        ),
        title: Text(
          todo.title,
          style: TextStyle(
            decoration: todo.completed ? TextDecoration.lineThrough : null,
            color: todo.completed ? Colors.grey : Colors.black,
          ),
        ),
        trailing: IconButton(
          icon: const Icon(Icons.delete, color: Colors.red),
          onPressed: () => controller.deleteTodo(todo.id),
        ),
      ),
    );
  }

  Widget _buildBottomActions(TodoController controller) {
    return Obx(
      () => Container(
        padding: const EdgeInsets.all(16),
        decoration: const BoxDecoration(
          border: Border(top: BorderSide(color: Colors.grey)),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(controller.remainingCountText),
            if (controller.hasCompletedTodos)
              TextButton(
                onPressed: controller.clearCompleted,
                child: const Text('Clear completed'),
              ),
          ],
        ),
      ),
    );
  }
}
```

## Example 3: User Authentication (Service + Controller)

### Service
```dart
// services/auth_service.dart
import 'package:get/get.dart';

class AuthService extends GetxService {
  // Reactive authentication state
  final _isLoggedIn = false.obs;
  final _currentUser = Rxn<String>();
  final _isLoading = false.obs;
  final _error = Rxn<String>();

  // Getters
  bool get isLoggedIn => _isLoggedIn.value;
  String? get currentUser => _currentUser.value;
  bool get isLoading => _isLoading.value;
  String? get error => _error.value;

  @override
  Future<void> onInit() async {
    super.onInit();
    await checkAuthStatus();
  }

  Future<void> checkAuthStatus() async {
    _isLoading.value = true;
    _error.value = null;

    try {
      // Simulate checking stored token/session
      await Future.delayed(const Duration(milliseconds: 500));

      // In real app, check secure storage
      final storedUser = 'john_doe'; // Mock stored user

      if (storedUser != null) {
        _currentUser.value = storedUser;
        _isLoggedIn.value = true;
      }
    } catch (e) {
      _error.value = 'Failed to check auth status: $e';
    } finally {
      _isLoading.value = false;
    }
  }

  Future<bool> login(String email, String password) async {
    _isLoading.value = true;
    _error.value = null;

    try {
      // Simulate API call
      await Future.delayed(const Duration(seconds: 1));

      // Mock validation
      if (email == 'user@example.com' && password == 'password123') {
        _currentUser.value = 'john_doe';
        _isLoggedIn.value = true;

        // Store user session (in real app, use secure storage)
        await _storeUserSession();

        return true;
      } else {
        _error.value = 'Invalid email or password';
        return false;
      }
    } catch (e) {
      _error.value = 'Login failed: $e';
      return false;
    } finally {
      _isLoading.value = false;
    }
  }

  Future<void> logout() async {
    _isLoading.value = true;

    try {
      // Simulate API call
      await Future.delayed(const Duration(milliseconds: 500));

      // Clear session
      await _clearUserSession();

      _currentUser.value = null;
      _isLoggedIn.value = false;
      _error.value = null;
    } catch (e) {
      _error.value = 'Logout failed: $e';
    } finally {
      _isLoading.value = false;
    }
  }

  Future<void> _storeUserSession() async {
    // In real app, use flutter_secure_storage
    await Future.delayed(const Duration(milliseconds: 100));
  }

  Future<void> _clearUserSession() async {
    // In real app, use flutter_secure_storage
    await Future.delayed(const Duration(milliseconds: 100));
  }

  void clearError() {
    _error.value = null;
  }
}
```

### Controller
```dart
// controllers/auth_controller.dart
import 'package:get/get.dart';
import '../services/auth_service.dart';

class AuthController extends GetxController {
  final AuthService _authService = Get.find<AuthService>();

  // Form state
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final isPasswordVisible = false.obs;
  final rememberMe = false.obs;

  // Computed properties
  bool get isLoggedIn => _authService.isLoggedIn;
  String? get currentUser => _authService.currentUser;
  bool get isLoading => _authService.isLoading;
  String? get error => _authService.error;

  bool get canLogin => emailController.text.isNotEmpty &&
                      passwordController.text.isNotEmpty &&
                      !_authService.isLoading;

  @override
  void onClose() {
    emailController.dispose();
    passwordController.dispose();
    super.onClose();
  }

  Future<void> login() async {
    if (!canLogin) return;

    final success = await _authService.login(
      emailController.text.trim(),
      passwordController.text,
    );

    if (success) {
      Get.offAllNamed('/home'); // Navigate to home and clear stack
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    Get.offAllNamed('/login'); // Navigate to login and clear stack
  }

  void togglePasswordVisibility() {
    isPasswordVisible.value = !isPasswordVisible.value;
  }

  void clearError() {
    _authService.clearError();
  }

  void clearForm() {
    emailController.clear();
    passwordController.clear();
    isPasswordVisible.value = false;
    rememberMe.value = false;
    clearError();
  }
}
```

### Views
```dart
// views/login_view.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/auth_controller.dart';

class LoginView extends StatelessWidget {
  const LoginView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final controller = Get.put(AuthController());

    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(
                Icons.lock,
                size: 100,
                color: Colors.blue,
              ),
              const SizedBox(height: 32),
              const Text(
                'Welcome Back',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              const Text(
                'Sign in to continue',
                style: TextStyle(fontSize: 16, color: Colors.grey),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),

              // Email field
              TextField(
                controller: controller.emailController,
                keyboardType: TextInputType.emailAddress,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  hintText: 'Enter your email',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.email),
                ),
              ),
              const SizedBox(height: 16),

              // Password field
              Obx(
                () => TextField(
                  controller: controller.passwordController,
                  obscureText: !controller.isPasswordVisible.value,
                  decoration: InputDecoration(
                    labelText: 'Password',
                    hintText: 'Enter your password',
                    border: const OutlineInputBorder(),
                    prefixIcon: const Icon(Icons.lock),
                    suffixIcon: IconButton(
                      icon: Icon(
                        controller.isPasswordVisible.value
                            ? Icons.visibility
                            : Icons.visibility_off,
                      ),
                      onPressed: controller.togglePasswordVisibility,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // Remember me checkbox
              Obx(
                () => Row(
                  children: [
                    Checkbox(
                      value: controller.rememberMe.value,
                      onChanged: (value) => controller.rememberMe.value = value!,
                    ),
                    const Text('Remember me'),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Error message
              Obx(
                () => controller.error != null
                    ? Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.red.shade50,
                          border: Border.all(color: Colors.red.shade200),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          children: [
                            Icon(Icons.error, color: Colors.red.shade600),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                controller.error!,
                                style: TextStyle(color: Colors.red.shade600),
                              ),
                            ),
                            IconButton(
                              icon: const Icon(Icons.close),
                              onPressed: controller.clearError,
                            ),
                          ],
                        ),
                      )
                    : const SizedBox.shrink(),
              ),

              const SizedBox(height: 16),

              // Login button
              Obx(
                () => ElevatedButton(
                  onPressed: controller.canLogin ? controller.login : null,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: controller.isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                          ),
                        )
                      : const Text('Login', style: TextStyle(fontSize: 16)),
                ),
              ),
              const SizedBox(height: 16),

              // Forgot password
              TextButton(
                onPressed: () {
                  // Navigate to forgot password
                },
                child: const Text('Forgot Password?'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

## Example 4: Shopping Cart (Complex State Management)

### Controller
```dart
// controllers/shopping_cart_controller.dart
import 'package:get/get.dart';

class Product {
  final String id;
  final String name;
  final double price;
  final String imageUrl;

  Product({
    required this.id,
    required this.name,
    required this.price,
    required this.imageUrl,
  });
}

class CartItem {
  final Product product;
  int quantity;

  CartItem({
    required this.product,
    this.quantity = 1,
  });
}

class ShoppingCartController extends GetxController {
  final cartItems = <CartItem>[].obs;
  final isLoading = false.obs;

  // Computed properties
  int get totalItems => cartItems.fold(0, (sum, item) => sum + item.quantity);
  double get totalPrice => cartItems.fold(
      0.0, (sum, item) => sum + (item.product.price * item.quantity));

  List<CartItem> get uniqueItems => cartItems;

  @override
  void onInit() {
    super.onInit();
    loadCart();
  }

  void loadCart() {
    // Load cart from local storage
    // Mock data for demo
    final mockCart = [
      CartItem(
        product: Product(
          id: '1',
          name: 'Flutter Book',
          price: 29.99,
          imageUrl: 'https://picsum.photos/100/100?random=1',
        ),
        quantity: 2,
      ),
    ];
    cartItems.assignAll(mockCart);
  }

  void addToCart(Product product) {
    final existingIndex = cartItems.indexWhere(
      (item) => item.product.id == product.id,
    );

    if (existingIndex != -1) {
      cartItems[existingIndex].quantity++;
    } else {
      cartItems.add(CartItem(product: product));
    }

    cartItems.refresh();
    _showAddToCartSnackbar(product);
  }

  void updateQuantity(String productId, int quantity) {
    if (quantity <= 0) {
      removeFromCart(productId);
      return;
    }

    final index = cartItems.indexWhere(
      (item) => item.product.id == productId,
    );

    if (index != -1) {
      cartItems[index].quantity = quantity;
      cartItems.refresh();
    }
  }

  void removeFromCart(String productId) {
    cartItems.removeWhere((item) => item.product.id == productId);
    _showRemoveFromCartSnackbar();
  }

  void clearCart() {
    cartItems.clear();
    _showClearCartSnackbar();
  }

  CartItem? getItemByProductId(String productId) {
    try {
      return cartItems.firstWhere((item) => item.product.id == productId);
    } catch (e) {
      return null;
    }
  }

  int getItemQuantity(String productId) {
    final item = getItemByProductId(productId);
    return item?.quantity ?? 0;
  }

  void _showAddToCartSnackbar(Product product) {
    Get.snackbar(
      'Added to Cart',
      '${product.name} has been added to your cart',
      icon: const Icon(Icons.check_circle, color: Colors.green),
      duration: const Duration(seconds: 2),
    );
  }

  void _showRemoveFromCartSnackbar() {
    Get.snackbar(
      'Removed from Cart',
      'Item has been removed from your cart',
      icon: const Icon(Icons.remove_circle, color: Colors.orange),
      duration: const Duration(seconds: 2),
    );
  }

  void _showClearCartSnackbar() {
    Get.snackbar(
      'Cart Cleared',
      'All items have been removed from your cart',
      icon: const Icon(Icons.delete_sweep, color: Colors.red),
      duration: const Duration(seconds: 2),
    );
  }
}
```

### Shopping Cart Widget
```dart
// widgets/shopping_cart_widget.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/shopping_cart_controller.dart';

class ShoppingCartWidget extends StatelessWidget {
  const ShoppingCartWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final controller = Get.find<ShoppingCartController>();

    return Container(
      decoration: BoxDecoration(
        color: Colors.grey.shade100,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Obx(
        () => controller.cartItems.isEmpty
            ? _buildEmptyCart()
            : _buildCartContent(controller),
      ),
    );
  }

  Widget _buildEmptyCart() {
    return const Padding(
      padding: EdgeInsets.all(32),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.shopping_cart_outlined,
            size: 64,
            color: Colors.grey,
          ),
          SizedBox(height: 16),
          Text(
            'Your cart is empty',
            style: TextStyle(
              fontSize: 18,
              color: Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCartContent(ShoppingCartController controller) {
    return Column(
      children: [
        // Cart items
        Expanded(
          child: ListView.builder(
            itemCount: controller.cartItems.length,
            itemBuilder: (context, index) {
              final item = controller.cartItems[index];
              return _buildCartItem(controller, item);
            },
          ),
        ),

        // Cart summary
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: const BorderRadius.vertical(
              bottom: Radius.circular(12),
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.1),
                blurRadius: 4,
                offset: const Offset(0, -2),
              ),
            ],
          ),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Total Items:',
                    style: TextStyle(fontSize: 16),
                  ),
                  Obx(
                    () => Text(
                      '${controller.totalItems}',
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Total Price:',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Obx(
                    () => Text(
                      '\$${controller.totalPrice.toStringAsFixed(2)}',
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.green,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: controller.cartItems.isNotEmpty
                      ? () {
                          // Proceed to checkout
                          Get.toNamed('/checkout');
                        }
                      : null,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: const Text('Proceed to Checkout'),
                ),
              ),
              const SizedBox(height: 8),
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: controller.clearCart,
                  child: const Text('Clear Cart'),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildCartItem(ShoppingCartController controller, CartItem item) {
    return Container(
      margin: const EdgeInsets.all(8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 2,
            offset: const Offset(0, 1),
          ),
        ],
      ),
      child: Row(
        children: [
          // Product image
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.network(
              item.product.imageUrl,
              width: 60,
              height: 60,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) {
                return Container(
                  width: 60,
                  height: 60,
                  color: Colors.grey.shade300,
                  child: const Icon(Icons.image, color: Colors.grey),
                );
              },
            ),
          ),
          const SizedBox(width: 12),

          // Product details
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  item.product.name,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '\$${item.product.price.toStringAsFixed(2)}',
                  style: TextStyle(
                    color: Colors.green.shade600,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),

          // Quantity controls
          Row(
            children: [
              IconButton(
                icon: const Icon(Icons.remove_circle_outline),
                onPressed: () {
                  controller.updateQuantity(
                    item.product.id,
                    item.quantity - 1,
                  );
                },
              ),
              Obx(
                () => Text(
                  '${item.quantity}',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              IconButton(
                icon: const Icon(Icons.add_circle_outline),
                onPressed: () {
                  controller.updateQuantity(
                    item.product.id,
                    item.quantity + 1,
                  );
                },
              ),
              IconButton(
                icon: const Icon(Icons.delete, color: Colors.red),
                onPressed: () {
                  controller.removeFromCart(item.product.id);
                },
              ),
            ],
          ),
        ],
      ),
    );
  }
}
```

## Best Practices

### 1. Controller Lifecycle
```dart
class MyController extends GetxController {
  @override
  void onInit() {
    super.onInit();
    // Initialize data
  }

  @override
  void onReady() {
    super.onReady();
    // Called after widget is built
  }

  @override
  void onClose() {
    // Clean up resources
    super.onClose();
  }
}
```

### 2. Dependency Injection Patterns
```dart
// Singleton - created once and lives forever
Get.put(AuthService(), permanent: true);

// Factory - new instance every time
Get.lazyPut(() => UserService());

// Temporary - disposed when not in use
Get.put(TemporaryService(), fenix: true);

// Find existing instance
final controller = Get.find<MyController>();
```

### 3. Error Handling in GetX
```dart
class MyController extends GetxController {
  final error = Rxn<String>();
  final isLoading = false.obs;

  Future<void> performOperation() async {
    try {
      isLoading.value = true;
      error.value = null;

      // Perform async operation
      await someAsyncOperation();
    } catch (e) {
      error.value = e.toString();
      Get.snackbar('Error', e.toString());
    } finally {
      isLoading.value = false;
    }
  }
}
```

### 4. Performance Optimization
```dart
// Use Obx only when needed
Obx(() => Text(controller.someValue));

// Use GetBuilder for simple rebuilds
GetBuilder<MyController>(
  builder: (controller) => Text(controller.someValue),
),

// Use GetX for more control
GetX<MyController>(
  builder: (controller) => Text(controller.someValue),
  initState: (controller) => controller.load(),
  dispose: (controller) => controller.dispose(),
),
```

## Common Patterns

### 1. Form Validation
```dart
class FormController extends GetxController {
  final formKey = GlobalKey<FormState>();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final isFormValid = false.obs;

  void validateForm() {
    isFormValid.value = formKey.currentState?.validate() ?? false;
  }

  void submit() {
    if (formKey.currentState?.validate() ?? false) {
      // Submit form
    }
  }
}
```

### 2. Pagination
```dart
class PaginatedController extends GetxController {
  final items = <Item>[].obs;
  final currentPage = 1.obs;
  final isLoading = false.obs;
  final hasReachedMax = false.obs;

  Future<void> loadMore() async {
    if (isLoading.value || hasReachedMax.value) return;

    isLoading.value = true;
    final newItems = await fetchItems(currentPage.value);

    if (newItems.isEmpty) {
      hasReachedMax.value = true;
    } else {
      items.addAll(newItems);
      currentPage.value++;
    }

    isLoading.value = false;
  }
}
```

### 3. Search/Filter
```dart
class SearchController extends GetxController {
  final allItems = <Item>[].obs;
  final filteredItems = <Item>[].obs;
  final searchQuery = ''.obs;

  @override
  void onInit() {
    super.onInit();
    ever(searchQuery, _filterItems);
  }

  void _filterItems(String query) {
    if (query.isEmpty) {
      filteredItems.assignAll(allItems);
    } else {
      filteredItems.assignAll(
        allItems.where((item) =>
            item.name.toLowerCase().contains(query.toLowerCase())),
      );
    }
  }
}
```

These examples cover the most common state management scenarios you'll encounter in Flutter development with GetX. Choose the appropriate pattern based on the complexity of your feature and the specific requirements of your application.