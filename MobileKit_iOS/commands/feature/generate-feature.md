# Generate iOS Feature Command

Generate a complete iOS feature with SwiftUI views, ViewModels, models, and tests using AI agents.

## Usage
```bash
mki generate-feature --name UserProfile --type swiftui-view
```

## Options
- `--name <name>` - Feature name (PascalCase, e.g., UserProfile)
- `--type <type>` - Feature type: swiftui-view, uikit-controller, complete-feature
- `--include-tests` - Generate XCTest unit and UI tests
- `--accessibility` - Include VoiceOver and accessibility support

## AI Workflow
1. **ios-planner** - Creates implementation plan
2. **ios-researcher** - Researches iOS patterns and APIs
3. **swiftui-designer** - Generates SwiftUI components
4. **ios-tester** - Creates XCTest unit and UI tests
5. **swift-reviewer** - Reviews generated code
6. **ios-docs-manager** - Updates documentation

## Generated Files
- SwiftUI Views (View + ViewModel)
- Data Models
- Unit Tests
- UI Tests  
- Documentation

Example output for `UserProfile`:
```
Features/UserProfile/
├── Views/
│   ├── UserProfileView.swift
│   └── UserProfileDetailView.swift
├── ViewModels/
│   └── UserProfileViewModel.swift
├── Models/
│   └── User.swift
└── Tests/
    ├── UserProfileViewModelTests.swift
    └── UserProfileUITests.swift
```
