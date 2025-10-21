# Dr.JOY iOS Clean Architecture Skill

A comprehensive Claude AI skill for developing the Dr.JOY attendance management iOS application using Clean Architecture, MVP pattern, RxSwift, and Texture (AsyncDisplayKit).

## What's Included

- **SKILL.md**: Main skill file with architecture patterns and best practices
- **reference.md**: Detailed implementation guides for all layers
- **examples.md**: Complete feature implementation examples
- **templates/**: Ready-to-use code templates
- **resources/**: Project structure and dependency information

## About Dr.JOY

Dr.JOY is an enterprise attendance management and HR application for iOS featuring:
- Daily attendance tracking with check-in/check-out
- Timesheet management
- Leave request workflows
- Real-time notifications
- Offline support with local database
- Firebase integration

## Tech Stack

- **Swift 5.x** - Modern Swift features
- **Clean Architecture + MVP** - Separation of concerns
- **RxSwift 6.x** - Reactive programming
- **Texture (AsyncDisplayKit)** - High-performance UI
- **Swinject** - Dependency injection
- **Alamofire 4.x** - Networking
- **Realm Swift 10.x** - Local database
- **SnapKit** - Auto Layout DSL
- **Firebase Suite** - Analytics, Auth, Messaging, etc.

## Installation

### For Claude.ai
1. Download `drjoy-ios-architecture.zip`
2. Go to https://claude.ai/skills
3. Click "Upload Skill"
4. Select the ZIP file
5. Done!

### For Claude Code
1. Place the skill folder in your Claude Code skills directory
2. Restart Claude Code
3. The skill will be automatically available

## Usage

This skill is automatically invoked when you:
- Work on Dr.JOY iOS app features
- Need help with MVP presenter implementation
- Implement reactive patterns with RxSwift
- Create high-performance lists with Texture
- Integrate Firebase services
- Debug memory leaks or performance issues
- Set up dependency injection with Swinject

## Examples

**Ask Claude:**
- "How do I implement a new attendance feature with MVP pattern?"
- "Show me how to create a Texture list with pagination"
- "Help me debug memory leaks in RxSwift subscriptions"
- "How do I integrate Firebase Analytics for this feature?"
- "Create a presenter for timesheet management"

## Architecture Layers

```
ios-drjoy/
├── Domain/          # Business logic & entities
├── Data/            # Repository implementations & APIs
└── Drjoy/           # Presentation layer (MVP)
    └── Presentasion/
        ├── Controller/
        ├── Presenter/
        ├── View/
        └── Protocol/
```

## Key Features

✅ Clean Architecture (3-layer separation)
✅ MVP Pattern with RxSwift
✅ Texture (AsyncDisplayKit) for performance
✅ Swinject Dependency Injection
✅ Firebase Full Integration
✅ Realm Offline Support
✅ Network Retry Logic
✅ Memory Leak Prevention
✅ SwiftLint Code Quality

## Structure

```
drjoy-ios-architecture/
├── SKILL.md                   # Main skill file (required)
├── README.md                  # This file
├── reference.md               # Detailed reference
├── examples.md                # Feature examples
├── templates/
│   └── feature_template.md    # Feature implementation template
└── resources/
    └── architecture_diagram.md # Project architecture
```

## Requirements

- Xcode (latest version)
- Swift 5.x or later
- iOS 13.0+ deployment target
- Carthage for dependency management

## Version

Current version: **1.0.0** (October 2025)

## Related Projects

- Backend API: Dr.JOY REST API
- Android App: Dr.JOY Android (Kotlin)
- Web Dashboard: Dr.JOY Admin Panel

## License

Proprietary - Dr.JOY No,054

## Contributing

This skill is maintained for internal Dr.JOY development team use.

## Support

For questions or issues with this skill:
1. Check the examples.md for similar implementations
2. Review the reference.md for detailed patterns
3. Consult the feature_template.md for step-by-step guidance
