# Codebase Structure, Architecture & Code Standards

## Sơ đồ cấu trúc thư mục (tree view)
```
.
├── android/
├── features/
│   ├── flashcard_import/   # Module tính năng import
│   ├── flashcard_viewer/   # Module tính năng học và xem thẻ
│   └── shared/             # Code dùng chung giữa các feature
├── ios/
├── lib/
│   ├── app/                # Cấu hình và UI chung của app
│   ├── core/               # Các dịch vụ lõi (database, DI, logging...)
│   ├── examples/           # Code mẫu
│   ├── routes/             # Định tuyến và navigation
│   └── main.dart           # Entry point
├── macos/
├── test/
│   ├── unit/
│   ├── widget/
│   └── integration/
├── web/
├── windows/
├── pubspec.yaml
└── README.md
```

## Giải thích vai trò từng thư mục/file chính
- **`features/`**: Chứa các module tính năng độc lập theo kiến trúc Modular. Mỗi feature là một package Dart riêng, có `pubspec.yaml` riêng, giúp giảm sự phụ thuộc và dễ dàng bảo trì.
    - `flashcard_import`: Xử lý logic import từ Anki, CSV, Quizlet...
    - `flashcard_viewer`: Xử lý UI và logic cho các chế độ học.
    - `shared`: Chứa các model, usecase, widget, và service được chia sẻ giữa các feature.
- **`lib/`**: Thư mục code chính của ứng dụng.
    - **`core/`**: Chứa các thành phần nền tảng, không phụ thuộc vào UI hay business logic cụ thể.
        - `database/`: Quản lý database (SQLite + Drift), repository, migration.
        - `di/`: Cấu hình Dependency Injection (sử dụng `get_it` và `injectable`).
        - `services/`: Các dịch vụ toàn cục như logging, event bus, error handling.
    - **`routes/`**: Quản lý định tuyến (navigation) của ứng dụng (sử dụng `get`).
    - **`main.dart`**: File khởi chạy ứng dụng, nơi khởi tạo các dịch vụ cốt lõi và DI container.
- **`test/`**: Chứa toàn bộ code test, được phân chia rõ ràng thành `unit`, `widget`, và `integration` test.
- **`.github/workflows/`**: Định nghĩa CI/CD pipeline, tự động chạy test, build và phân tích code trên GitHub Actions.

## Mô tả kiến trúc
Dự án áp dụng một sự kết hợp của các mẫu kiến trúc hiện đại:
- **Modular Architecture**: Toàn bộ codebase được chia thành các feature module độc lập, giúp đội ngũ phát triển song song và giảm xung đột.
- **Clean Architecture**: Mỗi module tuân thủ nguyên tắc Clean Architecture, phân tách rõ ràng thành 3 lớp:
    - **Presentation**: Chứa UI (Views) và State Management (Controllers/Bindings của GetX).
    - **Domain**: Chứa business logic cốt lõi (Use Cases) và định nghĩa các abstract repository (Models, Repositories). Lớp này không phụ thuộc vào bất kỳ framework nào.
    - **Data**: Cung cấp dữ liệu cho lớp Domain (Repository Implementations), giao tiếp với database, network API, etc.
- **State Management**: Sử dụng **GetX** cho UI state và **GetIt/Injectable** cho Dependency Injection để quản lý vòng đời của các services và repositories.
- **Offline-First**: Kiến trúc được thiết kế để ưu tiên hoạt động offline. Dữ liệu được lưu trữ và truy vấn từ local database (SQLite), và việc đồng bộ hóa với backend (Supabase) được thực hiện ngầm khi có kết nối mạng.

## Các coding standards / naming conventions
- **Ngôn ngữ**: Code được viết bằng tiếng Anh.
- **Formatting**: Tuân thủ nghiêm ngặt theo `dart format`. CI pipeline có bước kiểm tra để đảm bảo code đã được format.
- **Linter**: Sử dụng các quy tắc phân tích tĩnh được định nghĩa trong `analysis_options.yaml` để đảm bảo chất lượng code.
- **Style Guide**: Tuân theo hướng dẫn **Effective Dart**.
- **Null Safety**: Toàn bộ codebase được viết với Dart null safety.
- **Error Handling**: Sử dụng `Result` wrapper để xử lý lỗi một cách tường minh, tránh dùng `try-catch` tràn lan.
