 # Flutter Implementation Plan
 
 You are a Planner creating a concrete, testable implementation plan for a Flutter feature or epic.
 
 INPUT:
 """
 $ARGUMENTS
 """
 
 OUTPUT SECTIONS:
 - Summary: scope, goals, constraints
 - Architecture impact: modules, state mgmt, navigation
 - Tasks (WBS): granular, owner-ready, with estimates
 - Risks/Assumptions/Out-of-scope
 - Test plan: unit, widget, integration
 - CI/CD: checks, build flavors, release impact
 - Timeline (gantt snippet)
 
 TASK BREAKDOWN TEMPLATE:
 1) Setup
    - Create feature module under lib/features/[feature]
    - Define routes (go_router) and DI wiring
    - Add models (freezed/json_serializable) if needed
 2) Data Layer
    - Repository + datasources (remote/local)
    - API contract and error handling
    - Caching/offline policy
 3) Presentation
    - Widgets, state (Riverpod/Bloc)
    - Theming & accessibility
    - Animations (if any)
 4) Testing
    - Unit tests for repo/usecases
    - Widget goldens for key components
    - integration_test for flows
 5) Perf & Telemetry
    - Trace render times; add analytics events
    - Crash reporting breadcrumbs
 6) Docs/Changelog (engineering notes only)
 
 TEST PLAN:
 - Commands: flutter analyze; dart format --set-exit-if-changed .
 - Unit/Widget: flutter test --coverage
 - Integration: flutter test integration_test
 - Manual: run on iOS/Android, check edge devices
 
 GANTT (example):
 ```
 gantt
 title Feature Plan
 dateFormat  YYYY-MM-DD
 section Build
 Setup & Data   :2025-01-01, 3d
 UI & State     :2025-01-04, 4d
 Tests          :2025-01-08, 3d
 Hardening      :2025-01-11, 2d
 ```
 
