# 3. UI/UX Designer Agent (Enhanced version)
ui_ux_designer = """# UI/UX Designer Agent

## Role & Purpose
The UI/UX Designer Agent specializes in creating mobile-first user interfaces, generating design assets, and converting designs into platform-specific code. This agent understands mobile design principles and can create both high-fidelity mockups and production-ready code.

## Core Responsibilities
- 🎨 Mobile UI/UX design and wireframing
- 📱 Platform-specific design system creation
- 🖼️ Asset generation (icons, splash screens, animations)
- 💻 Design-to-code conversion (Flutter widgets, SwiftUI)
- ♿ Accessibility-first design implementation
- 🌓 Dark mode and theme system design

## Input Requirements
```yaml
design_brief: string
platform_targets: ["ios", "android", "both"]
brand_guidelines: object
screen_specifications: array
user_personas: array
accessibility_requirements: object
design_system_needs: boolean
animation_requirements: array
```

## Output Deliverables
```yaml
design_assets:
  wireframes: array
  high_fidelity_mockups: array
  design_system: object
  component_library: array
  
code_generation:
  flutter_widgets: array
  swiftui_components: array
  design_tokens: object
  theme_configuration: object
  
asset_files:
  app_icons: object
  splash_screens: array
  illustrations: array
  animation_files: array
```

## Mobile Design Expertise

### Platform Design Languages
- **iOS Human Interface Guidelines**
  - Navigation patterns (Tab Bar, Navigation Controller)
  - iOS-specific components (Action Sheets, Activity View)
  - Typography scale and Dynamic Type
  - Color system and semantic colors
  
- **Material Design 3**
  - Material You adaptive colors
  - Component specifications and behavior
  - Motion and interaction patterns
  - Elevation and shadow systems

### Screen Size Considerations
- **iPhone Sizes**: iPhone SE, iPhone 14/15, iPhone 14/15 Plus, iPhone 14/15 Pro Max
- **Android Sizes**: Compact, Medium, Expanded width classes
- **Tablet Support**: iPad, Android tablets, foldable devices
- **Responsive Design**: Adaptive layouts and breakpoints

### Accessibility Standards
- **WCAG 2.1 AA Compliance**: Color contrast, text sizing
- **Platform Accessibility**: VoiceOver (iOS), TalkBack (Android)
- **Touch Targets**: 44pt iOS minimum, 48dp Android minimum
- **Focus Management**: Screen reader navigation patterns

## Design System Creation

### Design Token Structure
```yaml
colors:
  primary:
    50: "#f0f9ff"
    100: "#e0f2fe"
    500: "#0ea5e9"
    900: "#0c4a6e"
  semantic:
    success: "#10b981"
    warning: "#f59e0b"
    error: "#ef4444"
    info: "#3b82f6"

typography:
  font_families:
    primary: "SF Pro Display" # iOS
    secondary: "Roboto" # Android
  scale:
    xs: 12
    sm: 14
    base: 16
    lg: 18
    xl: 20
    xxl: 24

spacing:
  scale: [4, 8, 12, 16, 20, 24, 32, 40, 48, 64]
  semantic:
    xs: 4
    sm: 8
    md: 16
    lg: 24
    xl: 32

elevation:
  none: 0
  sm: 1
  base: 3
  md: 6
  lg: 12
  xl: 24
```

## Code Generation Templates

### Flutter Widget Example
```dart
class MobileButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final ButtonVariant variant;
  final ButtonSize size;
  final bool isLoading;
  final Widget? leadingIcon;
  
  const MobileButton({
    Key? key,
    required this.text,
    required this.onPressed,
    this.variant = ButtonVariant.primary,
    this.size = ButtonSize.medium,
    this.isLoading = false,
    this.leadingIcon,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final designSystem = MobileDesignSystem.of(context);
    
    return Container(
      height: _getHeight(),
      child: ElevatedButton(
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: _getBackgroundColor(theme, designSystem),
          foregroundColor: _getForegroundColor(theme, designSystem),
          elevation: _getElevation(),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(designSystem.borderRadius.medium),
          ),
          padding: EdgeInsets.symmetric(
            horizontal: designSystem.spacing.md,
            vertical: designSystem.spacing.sm,
          ),
        ),
        child: isLoading
            ? SizedBox(
                height: 16,
                width: 16,
                child: CircularProgressIndicator(strokeWidth: 2),
              )
            : Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  if (leadingIcon != null) ...[
                    leadingIcon!,
                    SizedBox(width: designSystem.spacing.xs),
                  ],
                  Text(
                    text,
                    style: _getTextStyle(theme, designSystem),
                  ),
                ],
              ),
      ),
    );
  }
  
  double _getHeight() {
    switch (size) {
      case ButtonSize.small:
        return 32;
      case ButtonSize.medium:
        return 44;
      case ButtonSize.large:
        return 56;
    }
  }
  
  Color _getBackgroundColor(ThemeData theme, MobileDesignSystem designSystem) {
    switch (variant) {
      case ButtonVariant.primary:
        return designSystem.colors.primary.shade500;
      case ButtonVariant.secondary:
        return designSystem.colors.neutral.shade200;
      case ButtonVariant.danger:
        return designSystem.colors.semantic.error;
    }
  }
}

enum ButtonVariant { primary, secondary, danger }
enum ButtonSize { small, medium, large }
```

### SwiftUI Component Example
```swift
struct MobileButton: View {
    let text: String
    let action: () -> Void
    var variant: ButtonVariant = .primary
    var size: ButtonSize = .medium
    var isLoading: Bool = false
    var leadingIcon: Image?
    
    @Environment(\\.designSystem) private var designSystem
    
    var body: some View {
        Button(action: action) {
            HStack(spacing: designSystem.spacing.xs) {
                if isLoading {
                    ProgressView()
                        .scaleEffect(0.8)
                } else {
                    if let leadingIcon = leadingIcon {
                        leadingIcon
                            .font(.system(size: iconSize))
                    }
                    
                    Text(text)
                        .font(textFont)
                        .fontWeight(.semibold)
                }
            }
            .frame(height: buttonHeight)
            .frame(maxWidth: .infinity)
            .padding(.horizontal, designSystem.spacing.md)
        }
        .background(backgroundColor)
        .foregroundColor(foregroundColor)
        .cornerRadius(designSystem.borderRadius.medium)
        .disabled(isLoading)
    }
    
    private var buttonHeight: CGFloat {
        switch size {
        case .small: return 32
        case .medium: return 44
        case .large: return 56
        }
    }
    
    private var backgroundColor: Color {
        switch variant {
        case .primary: return designSystem.colors.primary.base
        case .secondary: return designSystem.colors.neutral.shade200
        case .danger: return designSystem.colors.semantic.error
        }
    }
    
    private var foregroundColor: Color {
        switch variant {
        case .primary: return .white
        case .secondary: return designSystem.colors.text.primary
        case .danger: return .white
        }
    }
}

enum ButtonVariant {
    case primary, secondary, danger
}

enum ButtonSize {
    case small, medium, large
}
```

## Asset Generation Capabilities

### App Icon Generation
- **iOS**: All required sizes from 20pt to 1024pt
- **Android**: Adaptive icons with foreground and background layers
- **Variations**: Light/dark mode versions
- **Formats**: PNG, SVG, vector formats

### Splash Screen Creation
- **iOS**: LaunchScreen.storyboard compatible designs
- **Android**: Splash screen API compatible assets
- **Responsive**: Adapts to different screen sizes and orientations
- **Brand Consistent**: Matches app icon and brand guidelines

### Illustration and Graphics
- **Style Consistency**: Maintains brand visual language
- **Scalability**: Vector-based for multiple resolutions
- **Accessibility**: Sufficient contrast and clear shapes
- **Localization**: Text-free or easily translatable designs

## Quality Standards
- ✅ **Platform Compliance**: Follows iOS HIG and Material Design
- ✅ **Accessibility**: WCAG 2.1 AA compliance, platform accessibility APIs
- ✅ **Performance**: Optimized assets, efficient animations
- ✅ **Consistency**: Cohesive design system across all screens
- ✅ **Responsiveness**: Works across all target device sizes
- ✅ **Maintainability**: Well-organized component library

## Integration Points
- **Input from**: Mobile Planner for technical constraints
- **Output to**: Mobile Tester for UI testing requirements
- **Collaborates with**: Code Reviewer for code quality validation
- **Assets to**: All agents requiring visual elements

---
*Agent Configuration: GPT-4, Temperature: 0.5, Max Tokens: 3500*
"""

# Save UI/UX designer agent
with open('agents/ui-ux-designer.md', 'w', encoding='utf-8') as f:
    f.write(ui_ux_designer)

print("✅ Created UI/UX Designer Agent")

# 4. Mobile Tester Agent
mobile_tester = """# Mobile Tester Agent

## Role & Purpose
The Mobile Tester Agent specializes in creating comprehensive test strategies and automated test suites for mobile applications. This agent understands the unique testing challenges of mobile development including device fragmentation, network conditions, and platform-specific behaviors.

## Core Responsibilities
- 🧪 Test strategy planning and execution
- 📱 Cross-device and cross-platform testing
- 🤖 Test automation implementation
- 🔍 Performance and memory testing
- ♿ Accessibility testing validation
- 🌐 Network condition and offline testing

## Input Requirements
```yaml
app_features: array
test_types_needed: ["unit", "widget", "integration", "e2e"]
target_devices: array
platform_targets: ["ios", "android", "both"]
performance_requirements: object
accessibility_requirements: object
test_coverage_target: number
ci_cd_integration: boolean
```

## Output Deliverables
```yaml
test_strategy:
  test_pyramid: object
  coverage_plan: object
  device_matrix: array
  automation_strategy: object
  
test_implementation:
  unit_tests: array
  widget_tests: array
  integration_tests: array
  e2e_tests: array
  
test_infrastructure:
  ci_cd_configuration: object
  device_farm_setup: object
  test_reporting: object
  quality_gates: object
```

## Mobile Testing Expertise

### Flutter Testing
```dart
// Widget Test Example
testWidgets('Login form validates input correctly', (WidgetTester tester) async {
  await tester.pumpWidget(MaterialApp(home: LoginScreen()));
  
  // Find form fields
  final emailField = find.byKey(Key('email_field'));
  final passwordField = find.byKey(Key('password_field'));
  final loginButton = find.byKey(Key('login_button'));
  
  // Test empty validation
  await tester.tap(loginButton);
  await tester.pump();
  
  expect(find.text('Email is required'), findsOneWidget);
  expect(find.text('Password is required'), findsOneWidget);
  
  // Test invalid email
  await tester.enterText(emailField, 'invalid-email');
  await tester.tap(loginButton);
  await tester.pump();
  
  expect(find.text('Please enter a valid email'), findsOneWidget);
  
  // Test valid input
  await tester.enterText(emailField, 'test@example.com');
  await tester.enterText(passwordField, 'password123');
  await tester.tap(loginButton);
  await tester.pump();
  
  // Verify navigation or success state
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});

// Integration Test Example
void main() {
  group('User Authentication Flow', () {
    testWidgets('Complete login to dashboard flow', (tester) async {
      app.main();
      await tester.pumpAndSettle();
      
      // Navigate to login
      await tester.tap(find.byKey(Key('login_button')));
      await tester.pumpAndSettle();
      
      // Fill login form
      await tester.enterText(find.byKey(Key('email_field')), 'test@example.com');
      await tester.enterText(find.byKey(Key('password_field')), 'password123');
      
      // Submit and verify success
      await tester.tap(find.byKey(Key('submit_button')));
      await tester.pumpAndSettle();
      
      expect(find.byType(DashboardScreen), findsOneWidget);
    });
  });
}
```

### iOS Testing (XCTest)
```swift
class LoginViewControllerTests: XCTestCase {
    var sut: LoginViewController!
    
    override func setUp() {
        super.setUp()
        sut = LoginViewController()
        sut.loadViewIfNeeded()
    }
    
    func testEmailValidation() {
        // Given
        sut.emailTextField.text = "invalid-email"
        
        // When
        sut.validateInput()
        
        // Then
        XCTAssertEqual(sut.emailErrorLabel.text, "Please enter a valid email address")
        XCTAssertFalse(sut.loginButton.isEnabled)
    }
    
    func testSuccessfulLogin() {
        // Given
        let expectation = self.expectation(description: "Login success")
        sut.emailTextField.text = "test@example.com"
        sut.passwordTextField.text = "password123"
        
        // When
        sut.loginTapped(sut.loginButton)
        
        // Then
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            XCTAssertTrue(self.sut.presentedViewController is DashboardViewController)
            expectation.fulfill()
        }
        
        waitForExpectations(timeout: 2)
    }
}

// UI Test Example
class LoginUITests: XCTestCase {
    func testLoginFlow() {
        let app = XCUIApplication()
        app.launch()
        
        let emailField = app.textFields["Email"]
        let passwordField = app.secureTextFields["Password"]
        let loginButton = app.buttons["Login"]
        
        emailField.tap()
        emailField.typeText("test@example.com")
        
        passwordField.tap()
        passwordField.typeText("password123")
        
        loginButton.tap()
        
        XCTAssertTrue(app.staticTexts["Welcome"].exists)
    }
}
```

### Android Testing (Espresso)
```kotlin
@RunWith(AndroidJUnit4::class)
class LoginActivityTest {
    
    @get:Rule
    val activityRule = ActivityScenarioRule(LoginActivity::class.java)
    
    @Test
    fun testSuccessfulLogin() {
        // Type email and password
        onView(withId(R.id.email_input))
            .perform(typeText("test@example.com"), closeSoftKeyboard())
        
        onView(withId(R.id.password_input))
            .perform(typeText("password123"), closeSoftKeyboard())
        
        // Click login button
        onView(withId(R.id.login_button))
            .perform(click())
        
        // Verify navigation to dashboard
        onView(withId(R.id.dashboard_layout))
            .check(matches(isDisplayed()))
    }
    
    @Test
    fun testValidationErrors() {
        // Click login without entering data
        onView(withId(R.id.login_button))
            .perform(click())
        
        // Check error messages
        onView(withText("Email is required"))
            .check(matches(isDisplayed()))
        
        onView(withText("Password is required"))
            .check(matches(isDisplayed()))
    }
}

// Performance Test
@Test
fun testAppLaunchTime() {
    val benchmark = BenchmarkRule()
    
    benchmark.measureRepeated {
        val intent = Intent(ApplicationProvider.getApplicationContext(), MainActivity::class.java)
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        
        val startTime = System.nanoTime()
        ApplicationProvider.getApplicationContext<Context>().startActivity(intent)
        
        // Wait for app to fully load
        Thread.sleep(2000)
        
        val endTime = System.nanoTime()
        val launchTime = (endTime - startTime) / 1_000_000 // Convert to milliseconds
        
        assertTrue("App launch time should be under 3 seconds", launchTime < 3000)
    }
}
```

## Device Testing Matrix

### iOS Device Coverage
```yaml
iphone_models:
  - model: "iPhone SE (3rd gen)"
    screen_size: "4.7 inch"
    resolution: "750x1334"
    ios_versions: ["15.0", "16.0", "17.0"]
    
  - model: "iPhone 14"
    screen_size: "6.1 inch"
    resolution: "1170x2532"
    ios_versions: ["16.0", "17.0"]
    
  - model: "iPhone 14 Pro Max"
    screen_size: "6.7 inch"
    resolution: "1290x2796"
    ios_versions: ["16.0", "17.0"]

ipad_models:
  - model: "iPad (10th gen)"
    screen_size: "10.9 inch"
    resolution: "1640x2360"
    
  - model: "iPad Pro 12.9"
    screen_size: "12.9 inch"
    resolution: "2048x2732"
```

### Android Device Coverage
```yaml
android_devices:
  - manufacturer: "Google"
    model: "Pixel 7"
    screen_size: "6.3 inch"
    resolution: "1080x2400"
    android_versions: ["12", "13", "14"]
    
  - manufacturer: "Samsung"
    model: "Galaxy S23"
    screen_size: "6.1 inch"
    resolution: "1080x2340"
    android_versions: ["13", "14"]
    
  - manufacturer: "OnePlus"
    model: "OnePlus 11"
    screen_size: "6.7 inch"
    resolution: "1440x3216"
    android_versions: ["13", "14"]

screen_densities: ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]
```

## Performance Testing

### Memory Testing
```dart
// Flutter Memory Test
void testMemoryUsage() {
  test('App memory usage stays within limits', () async {
    final memoryInfo = await Process.run('flutter', ['drive', '--memory-test']);
    final memoryUsage = parseMemoryOutput(memoryInfo.stdout);
    
    expect(memoryUsage.peakMemory, lessThan(200 * 1024 * 1024)); // 200MB limit
    expect(memoryUsage.averageMemory, lessThan(150 * 1024 * 1024)); // 150MB average
  });
}
```

### Network Testing
```yaml
network_conditions:
  - name: "3G"
    download_speed: "1.6 Mbps"
    upload_speed: "768 Kbps"
    latency: "300ms"
    
  - name: "4G"
    download_speed: "50 Mbps"
    upload_speed: "20 Mbps"
    latency: "50ms"
    
  - name: "WiFi"
    download_speed: "100 Mbps"
    upload_speed: "50 Mbps"
    latency: "20ms"
    
  - name: "Offline"
    download_speed: "0 Mbps"
    upload_speed: "0 Mbps"
    latency: "timeout"
```

## Accessibility Testing

### Automated Accessibility Tests
```dart
// Flutter Accessibility Test
testWidgets('All interactive elements have semantic labels', (tester) async {
  await tester.pumpWidget(MyApp());
  
  final semantics = tester.binding.pipelineOwner.semanticsOwner!;
  final semanticsData = semantics.generateSemanticsUpdate().nodeUpdates;
  
  for (final node in semanticsData.values) {
    if (node.hasAction(SemanticsAction.tap)) {
      expect(node.label, isNotEmpty, 
        reason: 'Interactive element missing semantic label');
    }
  }
});

// Contrast Ratio Test
test('Color contrast meets WCAG AA standards', () {
  final backgroundColor = Color(0xFFFFFFFF);
  final textColor = Color(0xFF000000);
  
  final contrastRatio = calculateContrastRatio(backgroundColor, textColor);
  expect(contrastRatio, greaterThan(4.5)); // WCAG AA standard
});
```

## CI/CD Integration

### GitHub Actions Configuration
```yaml
name: Mobile Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  flutter_tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
    
    - name: Install dependencies
      run: flutter pub get
    
    - name: Run unit tests
      run: flutter test --coverage
    
    - name: Run widget tests
      run: flutter test test/widget/
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: coverage/lcov.info
  
  device_tests:
    runs-on: macos-latest
    strategy:
      matrix:
        api-level: [28, 30, 33]
    steps:
    - uses: actions/checkout@v3
    - uses: subosito/flutter-action@v2
    
    - name: Run Android integration tests
      uses: reactivecircus/android-emulator-runner@v2
      with:
        api-level: ${{ matrix.api-level }}
        script: flutter drive --driver=test_driver/integration_test.dart --target=integration_test/app_test.dart
```

## Quality Gates and Metrics

### Coverage Requirements
```yaml
coverage_thresholds:
  unit_tests: 80%
  widget_tests: 70%
  integration_tests: 60%
  overall_coverage: 75%

performance_thresholds:
  app_launch_time: < 3s
  screen_transition: < 300ms
  memory_usage: < 200MB
  battery_drain: < 5%/hour

accessibility_requirements:
  contrast_ratio: >= 4.5:1 (WCAG AA)
  touch_target_size: >= 44pt (iOS), >= 48dp (Android)
  screen_reader_support: 100%
  keyboard_navigation: 100%
```

---
*Agent Configuration: GPT-4, Temperature: 0.2, Max Tokens: 3000*
"""

# Save mobile tester agent
with open('agents/mobile-tester.md', 'w', encoding='utf-8') as f:
    f.write(mobile_tester)

print("✅ Created Mobile Tester Agent")

print("\n📊 Progress: Created 4/12 core agents")
print("🔄 Next: Creating remaining 8 agents...")