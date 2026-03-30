# .agent Documentation System

Hệ thống tài liệu được thiết kế dành riêng cho workflow mobile development và AI integration của bạn.

## Quick Navigation

### 🏗️ Architecture & Design
Bắt đầu ở đây để hiểu kiến trúc hệ thống:
- **[Project Architecture](system/project_architecture.md)** - Cấu trúc dự án Flutter/iOS, tech stack, các pattern chính

### 📋 Tasks & Planning
PRDs và implementation plans:
- **[Tasks](tasks/)** - PRD & implementation plans cho mỗi feature/project

### 📚 Templates & Examples
Các template và ví dụ tái sử dụng:
- **[Flutter Feature Template](templates/flutter_feature_template.md)** - Template triển khai feature Flutter

### 🔧 Standard Operating Procedures (SOPs)
Cách thực hiện các tác vụ phát triển thông thường:
- **[AI Tools Integration](sops/ai_tools_integration.md)** - Cách sử dụng AI tools (Claude, Cursor)
- **[Mobile Development Workflow](sops/mobile_dev_workflow.md)** - Quy trình phát triển mobile

## 📋 Directory Structure

```
mobile_dev_agent_system/.agent/
├── tasks/                      # PRD & implementation plans cho mỗi feature/project
├── system/                     # Tài liệu hệ thống và kiến trúc
│   └── project_architecture.md
├── templates/                  # Các template tái sử dụng
│   └── flutter_feature_template.md
├── sops/                       # Standard Operating Procedures
│   ├── ai_tools_integration.md
│   └── mobile_dev_workflow.md
└── readme.md                   # File này
```

### 📁 tasks/
Chứa các PRDs và implementation plans for:
- Mobile app features (Flutter/iOS)
- AI integration projects
- Database design schemas
- API development plans

### 📁 system/
Architecture và technical specifications:
- Flutter project structure
- iOS app architecture
- Database schemas (MySQL/Oracle)
- API documentation
- AI tools integration patterns

### 📁 sops/
Standard Operating Procedures for:
- Mobile development workflow
- AI tools usage (Claude, Cursor)
- Database migration procedures
- Code review processes
- Deployment procedures

### 📁 templates/
Reusable templates for:
- Flutter feature implementation
- API endpoint documentation
- Database table creation
- AI prompt engineering

## 🚀 Getting Started

### For New Team Members
1. Đọc **[Project Architecture](system/project_architecture.md)** (10 phút)
2. Xem **[Mobile Development Workflow](sops/mobile_dev_workflow.md)** (15 phút)
3. Kiểm tra **[AI Tools Integration](sops/ai_tools_integration.md)** để phát triển với AI

### For Starting a New Feature
1. Kiểm tra **[Tasks](tasks/)** để xem PRDs và plans hiện có
2. Sử dụng **[Flutter Feature Template](templates/flutter_feature_template.md)** để triển khai
3. Làm theo **[Mobile Development Workflow](sops/mobile_dev_workflow.md)** SOP

## Sử dụng Documentation System

### Quy tắc cập nhật
1. Luôn đọc `readme.md` trước khi bắt đầu implementation
2. Kiểm tra **[Tasks](tasks/)** để xem PRDs và plans hiện có
3. Cập nhật `.agent/` docs sau khi hoàn thành feature
4. Tạo SOP cho quy trình mới
5. Sử dụng `/compact` để dọn dẹp conversation

### Commands hữu ích
- `/update doc initialize` - Khởi tạo cấu trúc docs
- `/update doc` - Cập nhật documentation
- Read `.agent/readme.md` first for context

## Workflow Integration
Hệ thống này được tối ưu cho:
- Flutter cross-platform development
- AI-assisted coding với Claude/Cursor
- Database-first architecture approach
- Oracle Cloud deployment
- Real-time collaboration

---

*Last updated: October 2025*
