# SwinjectStoryboard Performance Implementation Plan

## Overview
Optimize SwinjectStoryboard performance issues causing high CPU usage:
- **696.29 Mc (12.6%)** from `SwinjectStoryboard.instantiateViewController(withIdentifier:)`
- **384.22 Mc (6.9%)** from `SwinjectStoryboard.injectDependency(to:)`

## Implementation Strategy

### Phase 1: Factory Pattern Implementation

#### 1.1 Create ViewControllerFactory
```swift
// File: Drjoy/Common/Factory/ViewControllerFactory.swift
class ViewControllerFactory {
    static let shared = ViewControllerFactory()

    private var storyboardCache: [String: UIStoryboard] = [:]
    private var viewControllerCache: [String: UIViewController] = [:]
    private let cacheQueue = DispatchQueue(label: "com.drjoy.factory.cache", attributes: .concurrent)

    func getViewController<T: UIViewController>(
        storyboardName: String = "Main",
        identifier: String,
        type: T.Type
    ) -> T {
        let cacheKey = "\(storyboardName)_\(identifier)"

        return cacheQueue.sync {
            if let cached = viewControllerCache[cacheKey] as? T {
                return cached
            }

            let storyboard = getStoryboard(name: storyboardName)
            let viewController = storyboard.instantiateViewController(withIdentifier: identifier) as! T

            // Cache lightweight VCs only (no heavy state)
            if shouldCacheViewController(viewController) {
                viewControllerCache[cacheKey] = viewController
            }

            return viewController
        }
    }

    private func getStoryboard(name: String) -> UIStoryboard {
        return cacheQueue.sync {
            if let cached = storyboardCache[name] {
                return cached
            }

            let storyboard = UIStoryboard(name: name, bundle: Bundle.main)
            storyboardCache[name] = storyboard
            return storyboard
        }
    }

    private func shouldCacheViewController(_ vc: UIViewController) -> Bool {
        // Don't cache VCs with heavy state or lifecycle dependencies
        return false // Default to no caching initially
    }

    func clearCache() {
        cacheQueue.async(flags: .barrier) {
            self.viewControllerCache.removeAll()
            // Keep storyboard cache as it's lightweight
        }
    }
}
```

#### 1.2 Update AppDIContainer for Lazy Loading
```swift
// File: Drjoy/Common/DI/AppDIContainer.swift (modifications)
class AppDIContainer {
    static let instance = AppDIContainer()

    // Lazy containers for better performance
    private lazy var _main: Container = {
        let container = SwinjectStoryboard.defaultContainer
        setupMainContainer(container)
        return container
    }()

    var main: Container {
        return _main
    }

    // Add singleton caching for frequently used dependencies
    private var singletonCache: [String: Any] = [:]
    private let cacheQueue = DispatchQueue(label: "com.drjoy.di.cache", attributes: .concurrent)

    func resolveSingleton<T>(_ type: T.Type) -> T {
        let typeName = String(describing: type)

        return cacheQueue.sync {
            if let cached = singletonCache[typeName] as? T {
                return cached
            }

            let instance = main.resolve(type)!
            singletonCache[typeName] = instance
            return instance
        }
    }

    private func setupMainContainer(_ container: Container) {
        // Register dependencies as singletons where appropriate
        container.register(MessagePresenter.self) { resolver in
            // Existing registration logic
        }.inObjectScope(.container) // Add singleton scope

        // Other registrations...
    }
}
```

### Phase 2: Refactor Storyboard Instantiation Patterns

#### 2.1 Replace Direct Storyboard Usage
Files to update (7 files identified):

1. **SearchMessageResultVC.swift**
   ```swift
   // Before:
   let messageVC = UIStoryboard(name: "Main", bundle: Bundle.main).instantiateViewController(withIdentifier: "MessageVC") as? MessageVC

   // After:
   let messageVC = ViewControllerFactory.shared.getViewController(identifier: "MessageVC", type: MessageVC.self)
   ```

2. **EditMrMessageVC.swift**
3. **MessageTabVC.swift**
4. **EditChatRoomVC.swift**
5. **SelectMrMemberVC.swift**
6. **FavoriteMessageVC.swift**
7. **Appdelegate+Route.swift**

#### 2.2 Update MessageTabVC Implementation
```swift
// File: Drjoy/Presentasion/Controller/Chat/MessageTabVC.swift (modifications)
class MessageTabVC: UIViewController {

    // MARK: - Properties
    private var messageVC: MessageVC?
    private let factory = ViewControllerFactory.shared

    override func viewDidLoad() {
        super.viewDidLoad()
        setupMessageVC()
    }

    private func setupMessageVC() {
        messageVC = factory.getViewController(identifier: "MessageVC", type: MessageVC.self)
        messageVC?.delegate = self

        // Add child VC logic
        addChild(messageVC!)
        view.addSubview(messageVC!.view)
        messageVC?.didMove(toParent: self)

        // Setup constraints
        messageVC?.view.snp.makeConstraints { make in
            make.edges.equalToSuperview()
        }
    }

    deinit {
        ViewControllerFactory.shared.clearCache() // Clean up if needed
    }
}
```

### Phase 3: Performance Monitoring

#### 3.1 Add Performance Metrics
```swift
// File: Drjoy/Common/Performance/PerformanceMonitor.swift
class PerformanceMonitor {
    static let shared = PerformanceMonitor()

    func measureExecutionTime<T>(
        operation: String,
        block: () -> T
    ) -> T {
        let startTime = CFAbsoluteTimeGetCurrent()
        let result = block()
        let timeElapsed = CFAbsoluteTimeGetCurrent() - startTime

        print("⏱️ [Performance] \(operation): \(timeElapsed * 1000)ms")

        // Log to analytics if needed
        if timeElapsed > 0.1 { // Log slow operations > 100ms
            Analytics.logEvent("slow_operation", parameters: [
                "operation": operation,
                "duration_ms": timeElapsed * 1000
            ])
        }

        return result
    }
}
```

#### 3.2 Update Factory with Performance Monitoring
```swift
// Add to ViewControllerFactory
func getViewController<T: UIViewController>(
    storyboardName: String = "Main",
    identifier: String,
    type: T.Type
) -> T {
    return PerformanceMonitor.shared.measureExecutionTime(
        operation: "VC_Factory_\(identifier)"
    ) {
        // Existing implementation
    }
}
```

## Implementation Checklist

### Phase 1: Foundation (Days 1-2)
- [ ] Create `ViewControllerFactory.swift` in `Drjoy/Common/Factory/`
- [ ] Implement storyboard caching mechanism
- [ ] Add thread-safe cache operations
- [ ] Update `AppDIContainer.swift` for lazy loading
- [ ] Add singleton caching for frequently used dependencies
- [ ] Add performance monitoring utilities

### Phase 2: Refactoring (Days 3-4)
- [ ] Update `SearchMessageResultVC.swift` storyboard instantiation
- [ ] Update `EditMrMessageVC.swift` storyboard instantiation
- [ ] Update `MessageTabVC.swift` storyboard instantiation
- [ ] Update `EditChatRoomVC.swift` storyboard instantiation
- [ ] Update `SelectMrMemberVC.swift` storyboard instantiation
- [ ] Update `FavoriteMessageVC.swift` storyboard instantiation
- [ ] Update `Appdelegate+Route.swift` storyboard instantiation
- [ ] Add factory method to `MessageTabVC` for proper lifecycle management

### Phase 3: Testing & Validation (Day 5)
- [ ] Add unit tests for `ViewControllerFactory`
- [ ] Test performance improvements with Instruments
- [ ] Validate memory usage doesn't increase significantly
- [ ] Test cache invalidation scenarios
- [ ] Verify no regression in existing functionality

### Phase 4: Documentation & Monitoring (Day 6)
- [ ] Document performance improvements
- [ ] Add performance metrics to analytics
- [ ] Update development SOPs with new patterns
- [ ] Create performance regression tests

## Expected Performance Improvements

### CPU Usage Reduction
- **Storyboard Instantiation**: 696.29 Mc → ~50-100 Mc (85-93% reduction)
- **Dependency Injection**: 384.22 Mc → ~100-150 Mc (60-75% reduction)
- **Total Improvement**: 1,080 Mc → ~200-300 Mc (70-80% reduction)

### Metrics to Track
1. **Time Profiler**: Measure actual CPU time reduction
2. **Memory Usage**: Monitor cache memory consumption
3. **App Launch Time**: Measure improvement in cold start
4. **Navigation Speed**: Test VC transition performance

### Success Criteria
- [ ] CPU usage from SwinjectStoryboard methods reduced by >60%
- [ ] No increase in memory usage >5%
- [ ] No functional regressions in existing features
- [ ] Improved app responsiveness in navigation
- [ ] Performance monitoring in place for future tracking

## Risk Mitigation

### Potential Issues
1. **Memory Leaks**: Cache may retain VCs indefinitely
   - **Mitigation**: Implement weak reference caching or LRU eviction
2. **State Conflicts**: Cached VCs may retain previous state
   - **Mitigation**: Only cache stateless VCs or implement proper reset
3. **Thread Safety**: Concurrent access to cache
   - **Mitigation**: Use concurrent queue with barrier for writes

### Rollback Plan
- Keep original instantiation patterns commented out for quick rollback
- Implement feature flags to enable/disable factory pattern
- Monitor performance closely after each phase

## Files to Create/Modify

### New Files
1. `Drjoy/Common/Factory/ViewControllerFactory.swift`
2. `Drjoy/Common/Performance/PerformanceMonitor.swift`
3. `DrjoyTests/Common/Factory/ViewControllerFactoryTests.swift`

### Modified Files
1. `Drjoy/Common/DI/AppDIContainer.swift`
2. `Drjoy/Presentasion/Controller/Chat/SearchMessageResultVC.swift`
3. `Drjoy/Presentasion/Controller/Chat/EditMrMessageVC.swift`
4. `Drjoy/Presentasion/Controller/Chat/MessageTabVC.swift`
5. `Drjoy/Presentasion/Controller/Chat/EditChatRoomVC.swift`
6. `Drjoy/Presentasion/Controller/Common/SelectMemberVC/SelectMrMemberVC.swift`
7. `Drjoy/Presentasion/Controller/Common/FavoriteMessageVC.swift`
8. `Drjoy/Infrastructure/Appdelegate+Route.swift`

## Next Steps
1. Review implementation plan with team
2. Create feature branch for implementation
3. Implement Phase 1 (Foundation)
4. Test performance improvements after each phase
5. Deploy to staging for comprehensive testing
6. Monitor production performance after release