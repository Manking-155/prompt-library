 # Flutter Build/Sign/Release Checklist
 
 ANDROID:
 - app/build.gradle: productFlavors { dev, staging, prod }
 - signingConfigs via gradle.properties + env
 - Command: flutter build appbundle --flavor prod -t lib/main_prod.dart
 - Upload: Play Console (internal → production staged)
 - ProGuard/R8 mapping upload to crash tool
 
 IOS:
 - Schemes/Configurations: Dev/Staging/Prod
 - Provisioning profiles & Certificates; Automatic signing where possible
 - Command: flutter build ipa --flavor prod -t lib/main_prod.dart
 - Upload: App Store Connect (Transporter/API)
 - App Privacy details; TestFlight phased release
 
 COMMON:
 - Versioning: bump buildName/buildNumber
 - Changelog; release notes; feature flags toggles
 - Crash/Analytics symbols upload; release health
 - Store metadata review (screenshots, privacy, permissions)
 
