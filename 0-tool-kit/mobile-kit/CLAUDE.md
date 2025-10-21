# CLAUDE.md

## Project
name: MobileKit (Claude Code)
stack:
  - Flutter (Dart)
  - iOS (Swift/SwiftUI)
  - React Native (JS/TS)
goals:
  - Ship features fast with clear AI collaboration, strong tests, and release readiness

## Architecture Patterns
- Clean architecture, clear module boundaries
- Stateless UI where possible; side effects via services
- Separate API layer and DTOs with explicit mapping

## Code Style
- Strict linting (Dart/Swift/TS); meaningful names; no dead code
- Small, composable widgets/components; minimize rebuilds

## File Boundaries & Restrictions
- No secrets in repo or logs
- Environment-specific config (.env/.xcconfig/gradle.properties)

## Testing Requirements
- Unit + widget/UI + integration tests; target ≥80% coverage
- Performance checks (jank, memory, battery) for critical flows

## Security Standards
- Use Keychain/Keystore for secrets
- Validate/sanitize inputs; HTTPS/TLS; consider cert pinning
- Never log tokens, keys, or PII

## Deployment Workflows
- iOS: archive → TestFlight/App Store
- Android: bundle → Play Console
- Versioning, release notes, and rollback plan

## Mobile Guidelines
- iOS HIG and Material Design compliance
- Responsive & accessibility (VoiceOver/TalkBack)
