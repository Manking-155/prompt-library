# Code Standards & Conventions

## Language
- All code written in **English**
- All comments in English
- Variable, function, and class names in English

## Naming Conventions

### Files
```dart
// Files: snake_case.dart
user_controller.dart
flashcard_repository.dart
user_binding.dart
```

### Classes
```dart
// Classes: PascalCase
class UserController extends GetxController { }
class FlashcardRepository implements FlashcardRepositoryAbstract { }
abstract class UserRepository { }
mixin ErrorHandlingMixin { }
enum UserStatus { active, inactive, pending }
```

### Variables & Properties
```dart
// Variables: camelCase
String userName = 'John';
int totalItems = 10;
bool isLoading = false;

// Private variables: _camelCase
String _privateData = 'secret';

// Observable (GetX): camelCase.obs
final userName = ''.obs;
final isLoading = false.obs;
final items = <String>[].obs;
```

### Constants
```dart
// Constants: camelCase (not UPPER_CASE)
const String apiBaseUrl = 'https://api.example.com';
const int defaultTimeout = 30;
const double defaultPadding = 16.0;
```

### Functions & Methods
```dart
// Functions: camelCase, descriptive names with verbs
Future<Result<User, Exception>> getUser(String id);
void updateUserName(String name);
bool isValidEmail(String email);
List<User> filterActiveUsers(List<User> users);
```

### GetX Controllers
```dart
// Controller classes
class UserController extends GetxController { }

// Bindings
class UserBinding extends Bindings { }

// Routes: UPPER_SNAKE_CASE
const String USER_ROUTE = '/user';
const String USER_DETAIL_ROUTE = '/user/:id';
```

## Code Formatting

### Formatting Rules
- **Formatter**: Use `dart format`
- **Line Length**: Max 80 characters (soft limit, 100 hard limit)
- **Indentation**: 2 spaces (not tabs)
- **Imports**: Organized (dart, package, relative)

```dart
// ✓ Correct - Organized imports
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../domain/usecases/get_user_usecase.dart';
```

### Class Structure
```dart
class UserController extends GetxController {
  // 1. Dependencies
  final GetUserUsecase _getUser;
  
  // 2. Observable state (GetX)
  final users = <User>[].obs;
  final isLoading = false.obs;
  
  // 3. Constructor
  UserController(this._getUser);
  
  // 4. Lifecycle methods
  @override
  void onInit() {
    fetchUsers();
    super.onInit();
  }
  
  @override
  void onClose() {
    super.onClose();
  }
  
  // 5. Public methods
  Future<void> fetchUsers() async { }
  
  // 6. Private helper methods
  void _handleSuccess(List<User> data) { }
  void _handleError(Exception error) { }
}
```

## Comments

### Documentation Comments
```dart
/// Fetches a user by their ID.
/// 
/// Returns a [Result] containing the user if found,
/// or an exception if the operation fails.
Future<Result<User, Exception>> getUser(String id);
```

### Inline Comments
```dart
// Only for complex logic
// Use sparingly - code should be self-documenting

// Calculate total discount with tiered pricing
final discount = price > 100 ? price * 0.15 : price * 0.10;
```

### Avoid Comments
```dart
// ✗ Bad - Obvious comment
// Set loading to true
isLoading.value = true;

// ✓ Good - Clear function name
void _startLoading() => isLoading.value = true;
```

## Error Handling

### Result Wrapper Pattern
```dart
// All operations return Result<Success, Failure>
Future<Result<List<User>, Exception>> getUsers() async {
  try {
    final users = await _datasource.fetchUsers();
    return Result.success(users);
  } catch (e) {
    return Result.failure(Exception('Failed to fetch users: $e'));
  }
}

// Usage
final result = await usecase();
result.fold(
  (users) => _handleSuccess(users),
  (error) => _handleError(error),
);
```

### Exception Naming
```dart
// Custom exceptions
class NetworkException implements Exception {
  final String message;
  NetworkException(this.message);
}

class ValidationException implements Exception {
  final String message;
  ValidationException(this.message);
}
```

## Null Safety

- **Full Null Safety**: All code must be null-safe
- **Non-nullable by default**: Variables are non-nullable unless marked with `?`

```dart
// ✓ Correct
String name = 'John';  // Non-nullable
String? nickname;      // Nullable
User? user = Get.find();

// ✓ Safe null handling
final displayName = user?.name ?? 'Unknown';

// ✓ Using late keyword carefully
late String _apiKey;

@override
void onInit() {
  _apiKey = _loadApiKey();  // Initialize in onInit
  super.onInit();
}
```

## GetX Usage Patterns

### Controllers
```dart
class UserController extends GetxController {
  // Use Rxn for nullable values
  final user = Rxn<User>();
  
  // Use obs for simple values
  final isLoading = false.obs;
  
  // Use RxList for collections
  final users = <User>[].obs;
  
  // Use RxMap for maps
  final data = <String, dynamic>{}.obs;
}
```

### Bindings
```dart
class UserBinding extends Bindings {
  @override
  void dependencies() {
    // Use lazyPut for performance
    Get.lazyPut(() => UserRepository(Get.find()));
    Get.lazyPut(() => GetUserUsecase(Get.find()));
    Get.lazyPut(() => UserController(Get.find()));
  }
}
```

### Views
```dart
class UserPage extends StatelessWidget {
  const UserPage({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return GetBuilder<UserController>(
      builder: (controller) => Scaffold(
        body: Obx(
          () => ListView(
            children: controller.users
              .map((user) => UserTile(user: user))
              .toList(),
          ),
        ),
      ),
    );
  }
}
```

## Testing Conventions

### Test File Naming
```dart
// lib/features/user/domain/usecases/get_user_usecase.dart
// test/features/user/domain/usecases/get_user_usecase_test.dart
```

### Test Structure
```dart
void main() {
  group('GetUserUsecase', () {
    late GetUserUsecase usecase;
    late MockUserRepository mockRepository;
    
    setUp(() {
      mockRepository = MockUserRepository();
      usecase = GetUserUsecase(mockRepository);
    });
    
    test('should return user when repository succeeds', () async {
      // Arrange
      const testUser = User(id: '1', name: 'John');
      when(mockRepository.getUser('1'))
        .thenAnswer((_) async => Result.success(testUser));
      
      // Act
      final result = await usecase('1');
      
      // Assert
      expect(result.isSuccess, true);
      expect(result.getOrNull(), testUser);
    });
  });
}
```

## Analysis Options

Configure `analysis_options.yaml`:
```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    - always_declare_return_types
    - always_put_control_body_on_new_line
    - always_put_required_named_parameters_first
    - annotate_overrides
    - avoid_bool_literals_in_conditional_expressions
    - avoid_double_and_int_checks
    - avoid_empty_else
    - avoid_field_initializers_in_const_classes
    - avoid_function_literals_in_foreach_calls
    - avoid_init_to_null
    - avoid_null_checks_in_equality_operators
    - avoid_positional_boolean_parameters
    - avoid_private_typedef_functions
    - avoid_renaming_method_parameters
    - avoid_returning_null
    - avoid_returning_null_for_future
    - avoid_returning_this
    - avoid_setters_without_getters
    - avoid_shadowing_type_parameters
    - avoid_slow_async_io
    - avoid_types_as_parameter_names
    - avoid_types_on_closure_parameters
    - avoid_unnecessary_containers
    - avoid_void_async
    - await_only_futures
    - camel_case_extensions
    - camel_case_types
    - cascade_invocations
    - cast_nullable_to_non_nullable
    - close_sinks
    - comment_references
    - conditional_uri_does_not_exist
    - constant_identifier_names
    - curly_braces_in_flow_control_structures
    - directives_ordering
    - empty_catches
    - empty_constructor_bodies
    - eol_only_unix_line_endings
    - file_names
    - implementation_imports
    - invariant_booleans
    - leading_newlines_in_multiline_strings
    - library_names
    - library_prefixes
    - library_private_types_in_public_api
    - lines_longer_than_80_chars
    - no_adjacent_strings_in_list
    - no_leading_underscores_for_library_prefixes
    - null_check_on_nullable_type_parameter
    - null_closures
    - omit_local_variable_types
    - one_member_abstracts
    - only_throw_errors
    - overridden_fields
    - package_api_docs
    - package_names
    - package_prefixed_library_names
    - parameter_assignments
    - prefer_adjacent_string_concatenation
    - prefer_asserts_in_initializer_lists
    - prefer_asserts_with_message
    - prefer_collection_literals
    - prefer_conditional_assignment
    - prefer_const_constructors
    - prefer_const_constructors_in_immutables
    - prefer_const_declarations
    - prefer_const_literals_to_create_immutables
    - prefer_constructors_over_static_methods
    - prefer_contains
    - prefer_equal_for_default_values
    - prefer_expression_function_bodies
    - prefer_final_fields
    - prefer_final_in_for_each
    - prefer_final_locals
    - prefer_for_elements_to_map_fromIterable
    - prefer_foreach
    - prefer_function_declarations_over_variables
    - prefer_generic_function_type_aliases
    - prefer_getters_setters
    - prefer_if_elements_to_conditional_expressions
    - prefer_if_null_to_conditional_expressions
    - prefer_if_on_single_line_blocks
    - prefer_initializing_formals
    - prefer_inlined_adds
    - prefer_int_literals
    - prefer_interpolation_to_compose_strings
    - prefer_is_empty
    - prefer_is_not_empty
    - prefer_is_not_operator
    - prefer_is_null_check_on_nullable_type_parameter
    - prefer_iterable_whereType
    - prefer_null_aware_operators
    - prefer_relative_imports
    - prefer_single_quotes
    - prefer_spread_collections
    - provide_deprecation_message
    - recursive_getters
    - sized_box_for_whitespace
    - sized_box_shrink_expand
    - slash_for_doc_comments
    - sort_child_properties_last
    - sort_constructors_first
    - sort_pub_dependencies
    - sort_unnamed_constructors_first
    - tighten_type_of_initializing_formals
    - type_annotate_public_apis
    - type_init_formals
    - unawaited_futures
    - unnecessary_await_in_return
    - unnecessary_brace_in_string_interps
    - unnecessary_const
    - unnecessary_constructor_name
    - unnecessary_getters_setters
    - unnecessary_lambdas
    - unnecessary_null_aware_assignments
    - unnecessary_null_checks
    - unnecessary_null_in_if_null_operators
    - unnecessary_null_on_extension_on_nullable_type
    - unnecessary_nullable_for_final_variable_declarations
    - unnecessary_overrides
    - unnecessary_parenthesis
    - unnecessary_statements
    - unnecessary_string_escapes
    - unnecessary_string_interpolations
    - unnecessary_this
    - unnecessary_to_list_in_spreads
    - unrelated_type_equality_checks
    - unsafe_html
    - use_build_context_synchronously
    - use_full_hex_values_for_flutter_colors
    - use_function_type_syntax_for_parameters
    - use_getters_to_query_properties
    - use_if_null_to_convert_nulls
    - use_is_even_rather_than_modulo
    - use_key_in_widget_constructors
    - use_late_for_private_fields_and_variables
    - use_raw_strings
    - use_rethrow_when_possible
    - use_setters_to_change_properties
    - use_string_buffers
    - use_test_throws_matchers
    - use_to_close_resource_list
    - void_checks
```

## Related Documentation
- Clean Architecture Guide: `system/clean_architecture_guide.md`
- Project Architecture: `system/project_architecture.md`
