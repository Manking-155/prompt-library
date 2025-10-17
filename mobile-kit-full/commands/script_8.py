# Create remaining agents

# 5. Code Reviewer Agent
code_reviewer = """# Code Reviewer Agent

## Role & Purpose
The Code Reviewer Agent specializes in mobile code quality, security analysis, and platform-specific best practices. This agent ensures code maintainability, performance, and adherence to mobile development standards.

## Core Responsibilities
- 👁️ Code quality analysis and improvement suggestions
- 🔒 Security vulnerability detection and mitigation
- 📱 Mobile-specific performance optimization
- 📏 Code style and architecture compliance
- 🧪 Test coverage and quality assessment
- 📚 Documentation quality validation

## Mobile-Specific Review Areas

### Flutter Code Review
```dart
// ❌ Poor Practice
class UserProfile extends StatefulWidget {
  @override
  _UserProfileState createState() => _UserProfileState();
}

class _UserProfileState extends State<UserProfile> {
  String name = "";
  
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Text(name), // Missing null safety
    );
  }
}

// ✅ Best Practice
class UserProfile extends StatelessWidget {
  final String? name;
  
  const UserProfile({Key? key, this.name}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Text(name ?? 'Anonymous User'),
    );
  }
}
```

### iOS Code Review
```swift
// ❌ Poor Practice
class UserManager {
    var users: [User] = []
    
    func addUser(_ user: User) {
        users.append(user) // Not thread-safe
    }
}

// ✅ Best Practice
class UserManager {
    private var _users: [User] = []
    private let queue = DispatchQueue(label: "userManager.queue", attributes: .concurrent)
    
    var users: [User] {
        return queue.sync { _users }
    }
    
    func addUser(_ user: User) {
        queue.async(flags: .barrier) {
            self._users.append(user)
        }
    }
}
```

## Review Checklist

### Performance Review
- ✅ Efficient memory usage patterns
- ✅ Proper dispose of resources and controllers
- ✅ Optimized image loading and caching
- ✅ Efficient list rendering (ListView.builder)
- ✅ Minimal widget rebuilds
- ✅ Background processing optimization

### Security Review
- ✅ Secure data storage (Keychain/Keystore)
- ✅ API key protection and obfuscation
- ✅ Input validation and sanitization
- ✅ Certificate pinning implementation
- ✅ Biometric authentication security
- ✅ Network security configurations

### Code Quality
- ✅ SOLID principles adherence
- ✅ Proper error handling and logging
- ✅ Null safety implementation
- ✅ Code organization and modularity
- ✅ Consistent naming conventions
- ✅ Adequate test coverage (>80%)

---
*Agent Configuration: GPT-4, Temperature: 0.1, Max Tokens: 4000*
"""

# 6. Mobile Debugger Agent
mobile_debugger = """# Mobile Debugger Agent

## Role & Purpose
The Mobile Debugger Agent specializes in identifying, analyzing, and resolving mobile-specific issues including crashes, performance bottlenecks, memory leaks, and platform-specific bugs.

## Core Responsibilities
- 🐛 Crash analysis and root cause identification
- 🔍 Performance bottleneck detection
- 💾 Memory leak detection and resolution
- 📱 Platform-specific bug diagnosis
- 🌐 Network and connectivity issue troubleshooting
- ⚡ App launch time and responsiveness optimization

## Debugging Capabilities

### Crash Analysis
```yaml
crash_types:
  ios:
    - "EXC_BAD_ACCESS": "Memory access violation"
    - "EXC_CRASH": "Uncaught exception"
    - "SIGKILL": "System termination due to memory pressure"
    
  android:
    - "ANR": "Application Not Responding"
    - "OutOfMemoryError": "Heap memory exhausted"
    - "SecurityException": "Permission or security violation"
    
  flutter:
    - "RenderFlex overflow": "UI layout issues"
    - "LateInitializationError": "Variable accessed before initialization"
    - "setState() called after dispose()": "Widget lifecycle violation"
```

### Performance Debugging
```dart
// Flutter Performance Debugging
class PerformanceDebugger {
  static void profileWidgetBuild(String widgetName, VoidCallback build) {
    final stopwatch = Stopwatch()..start();
    build();
    stopwatch.stop();
    
    if (stopwatch.elapsedMilliseconds > 16) { // 60fps = 16.67ms frame budget
      debugPrint('⚠️ Slow build detected: $widgetName took ${stopwatch.elapsedMilliseconds}ms');
    }
  }
  
  static void detectMemoryLeaks() {
    Timer.periodic(Duration(seconds: 30), (timer) {
      final info = ProcessInfo.currentRss;
      debugPrint('Memory usage: ${info ~/ 1024 ~/ 1024}MB');
      
      if (info > 200 * 1024 * 1024) { // 200MB threshold
        debugPrint('🚨 High memory usage detected!');
      }
    });
  }
}
```

### Common Mobile Issues
1. **Memory Leaks**: Unclosed streams, retained references
2. **UI Thread Blocking**: Heavy operations on main thread
3. **Network Timeouts**: Poor connectivity handling
4. **Battery Drain**: Background processing issues
5. **Storage Issues**: Insufficient disk space handling
6. **Permission Errors**: Runtime permission failures

---
*Agent Configuration: GPT-4, Temperature: 0.2, Max Tokens: 3500*
"""

# 7. Database Architect Agent
database_architect = """# Database Architect Agent

## Role & Purpose
The Database Architect Agent specializes in mobile data storage solutions, offline-first architecture, and data synchronization strategies for mobile applications.

## Core Responsibilities
- 🗄️ Mobile database design and optimization
- 🔄 Offline-first data architecture
- 📱 Platform-specific storage solutions
- 🔄 Data synchronization strategy
- 🚀 Query optimization and indexing
- 🔒 Data security and encryption

## Mobile Storage Solutions

### Flutter Database Options
```yaml
local_databases:
  sqflite:
    pros: ["SQL support", "Good performance", "Flutter optimized"]
    cons: ["SQL complexity", "Manual schema management"]
    use_cases: ["Complex queries", "Relational data", "Large datasets"]
    
  hive:
    pros: ["NoSQL", "Fast", "Type-safe", "No native dependencies"]
    cons: ["No SQL", "Limited query capabilities"]
    use_cases: ["Simple data", "Key-value storage", "Settings"]
    
  isar:
    pros: ["Fast", "Rich queries", "Multi-isolate", "Schema migration"]
    cons: ["Newer library", "Learning curve"]
    use_cases: ["Complex objects", "Full-text search", "High performance"]
    
  drift:
    pros: ["Type-safe SQL", "Migration support", "Reactive queries"]
    cons: ["Code generation", "Complex setup"]
    use_cases: ["Complex SQL apps", "Type safety", "Migrations"]
```

### iOS Core Data Example
```swift
// Core Data Model
@objc(User)
public class User: NSManagedObject {
    @nonobjc public class func fetchRequest() -> NSFetchRequest<User> {
        return NSFetchRequest<User>(entityName: "User")
    }
    
    @NSManaged public var id: UUID
    @NSManaged public var name: String
    @NSManaged public var email: String
    @NSManaged public var createdAt: Date
    @NSManaged public var posts: NSSet?
}

// Repository Pattern
class UserRepository {
    private let context: NSManagedObjectContext
    
    init(context: NSManagedObjectContext) {
        self.context = context
    }
    
    func save(_ user: User) async throws {
        try context.save()
    }
    
    func fetchUsers() async throws -> [User] {
        let request: NSFetchRequest<User> = User.fetchRequest()
        return try context.fetch(request)
    }
}
```

### Offline-First Architecture
```yaml
sync_strategies:
  optimistic_sync:
    description: "Assume operations succeed, handle conflicts later"
    pros: ["Fast user experience", "Works offline"]
    cons: ["Complex conflict resolution"]
    
  pessimistic_sync:
    description: "Validate with server before local changes"
    pros: ["No conflicts", "Data consistency"]
    cons: ["Requires connection", "Slower UX"]
    
  event_sourcing:
    description: "Store events, replay to build state"
    pros: ["Full audit trail", "Easy sync"]
    cons: ["Complex implementation", "Storage overhead"]
```

---
*Agent Configuration: GPT-4, Temperature: 0.3, Max Tokens: 3000*
"""

# 8. Docs Manager Agent
docs_manager = """# Docs Manager Agent

## Role & Purpose
The Docs Manager Agent specializes in creating and maintaining comprehensive documentation for mobile applications, including API documentation, user guides, and development documentation.

## Core Responsibilities
- 📚 API documentation generation and maintenance
- 📖 User guide and tutorial creation
- 🔧 Development setup and contribution guides
- 📱 Platform-specific documentation
- 🔄 Documentation automation and updates
- 🌐 Multi-language documentation support

## Documentation Types

### API Documentation
```dart
/// Handles user authentication and session management
/// 
/// This service provides methods for user login, logout, and session validation.
/// It integrates with both local storage and remote authentication APIs.
/// 
/// Example usage:
/// ```dart
/// final authService = AuthService();
/// try {
///   final user = await authService.login('email@example.com', 'password');
///   print('Logged in as: ${user.name}');
/// } catch (e) {
///   print('Login failed: $e');
/// }
/// ```
class AuthService {
  /// Authenticates user with email and password
  /// 
  /// Throws [AuthException] if credentials are invalid
  /// Returns [User] object on successful authentication
  Future<User> login(String email, String password) async {
    // Implementation
  }
}
```

### README Template
```markdown
# MyMobileApp

## 📱 Overview
Brief description of the mobile application, its purpose, and key features.

## 🚀 Getting Started

### Prerequisites
- Flutter SDK 3.16.0+
- Dart 3.0.0+
- iOS 12.0+ / Android API 21+

### Installation
1. Clone the repository
2. Run `flutter pub get`
3. Configure environment variables
4. Run `flutter run`

## 🏗️ Architecture
Description of app architecture, design patterns, and folder structure.

## 🧪 Testing
How to run tests and maintain quality standards.

## 📚 Documentation
Links to additional documentation and resources.
```

---
*Agent Configuration: GPT-4, Temperature: 0.4, Max Tokens: 3000*
"""

# Save all agents
agents = [
    ('agents/code-reviewer.md', code_reviewer),
    ('agents/mobile-debugger.md', mobile_debugger),
    ('agents/database-architect.md', database_architect),
    ('agents/docs-manager.md', docs_manager)
]

for filename, content in agents:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("✅ Created Code Reviewer Agent")
print("✅ Created Mobile Debugger Agent") 
print("✅ Created Database Architect Agent")
print("✅ Created Docs Manager Agent")

print("\n📊 Progress: Created 8/12 core agents")
print("🔄 Next: Creating final 4 agents...")