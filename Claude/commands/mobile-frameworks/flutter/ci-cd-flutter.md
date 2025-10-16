 # Flutter CI/CD Workflow
 
 Goals: deterministic builds for Android/iOS with flavors, tests, and signing.
 
 PIPELINE STAGES:
 1) Setup
    - actions/setup-java@v4 (temurin 21)
    - subosito/flutter-action@v2 (channel: stable)
    - cache pub/.gradle/.dartTool
 2) Lint & Test
    - flutter analyze; dart format --set-exit-if-changed .
    - flutter test --coverage; upload coverage artifact
 3) Build Android
    - ./gradlew :app:bundleProdRelease (or apk)
    - Use signing via env secrets (keystore base64, alias, pass)
 4) Build iOS
    - xcodebuild -workspace ios/Runner.xcworkspace -scheme Runner -configuration Release -destination 'generic/platform=iOS' -archivePath build/Runner.xcarchive archive
    - xcodebuild -exportArchive ... with App Store Connect API key
 5) Artifacts
    - Upload AAB/IPA, mapping files, symbols (Sentry)
 6) Deploy (manual/staged)
    - Android: Play Developer API
    - iOS: App Store Connect API (Transporter)
 
 SECRETS REQUIRED:
 - ANDROID_KEYSTORE_BASE64, ANDROID_KEY_ALIAS, ANDROID_KEY_PASSWORD
 - APP_STORE_CONNECT_API_KEY_ID, ISSUER_ID, PRIVATE_KEY
 - SENTRY_AUTH_TOKEN (optional)
 
 SAMPLE GitHub Actions (simplified):
 ```yaml
 name: flutter-ci
 on: [push, pull_request]
 jobs:
   build:
     runs-on: macos-latest
     steps:
       - uses: actions/checkout@v4
       - uses: subosito/flutter-action@v2
         with: { channel: stable }
       - run: flutter pub get
       - run: flutter analyze
       - run: dart format --set-exit-if-changed .
       - run: flutter test --coverage
       - run: flutter build appbundle --flavor prod -t lib/main_prod.dart
 ```
 
