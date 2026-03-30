# Agent Systems Architecture - Standard Structure

Tài liệu này mô tả cấu trúc thống nhất cho tất cả các agent systems trong thư mục này.

## 📋 Cấu trúc thống nhất

Tất cả các agent systems phải tuân theo cấu trúc `.agent/` như sau:

```
.agent/
├── tasks/          # PRD & implementation plans cho mỗi feature/project
├── system/         # System documentation và architecture
├── sops/           # Standard Operating Procedures
├── templates/      # Reusable templates (optional nhưng recommended)
└── readme.md       # Index của tất cả documentation
```

## 📁 Mô tả các thư mục

### `tasks/`
Chứa các PRD (Product Requirements Document) và implementation plans cho từng feature/project:
- PRD documents
- Implementation plans
- Feature specifications
- Project planning documents

### `system/`
Documentation về current state của system:
- Project structure
- Tech stack
- Integration points
- Database schema
- Core functionalities
- Agent architecture
- LLM layer documentation

### `sops/`
Standard Operating Procedures - Best practices để thực hiện các tác vụ:
- How to add a schema migration
- How to add a new page route
- Development workflows
- Code review processes
- Deployment procedures

### `templates/`
Reusable templates cho development:
- Feature implementation templates
- Code snippets
- Documentation templates
- Project structure templates

### `readme.md`
Index file chứa:
- Quick Navigation links
- Directory Structure diagram
- Getting Started guide
- Documentation standards
- Pre-Implementation Checklist
- Links đến tất cả documentation trong hệ thống

## 🎯 Các Agent Systems

### 1. flutter_agent_system_en
- **Location**: `flutter_agent_system_en/.agent/`
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Language**: English

### 2. mobile_dev_agent_system
- **Location**: `mobile_dev_agent_system/.agent/`
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Language**: Vietnamese

### 3. mobile_dev_agent_system_english
- **Location**: `mobile_dev_agent_system_english/.agent/`
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Language**: English

### 4. solo_expansion_system_agent
- **Location**: `solo_expansion_system_agent/.agent/`
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Language**: English

### 5. solo_expansion_system
- **Location**: `solo_expansion_system/.agent/`
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Language**: Vietnamese

### 6. solo_expansion_system_english
- **Location**: `solo_expansion_system_english/.agent/`
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Language**: English

## 📝 Quy tắc sử dụng

### Khi bắt đầu implementation:
1. **Luôn đọc** `.agent/readme.md` trước để có context
2. Kiểm tra `tasks/` để xem PRDs và plans hiện có
3. Xem `system/` để hiểu architecture
4. Tham khảo `sops/` cho workflows
5. Sử dụng `templates/` khi cần

### Sau khi hoàn thành feature:
1. Cập nhật documentation trong `system/` nếu có thay đổi architecture
2. Tạo/update SOP trong `sops/` nếu có workflow mới
3. Cập nhật `readme.md` nếu cần
4. Tạo PRD trong `tasks/` cho feature tiếp theo

## 🔄 Maintenance

### Chuẩn hóa cấu trúc:
- Tất cả agent systems phải có đầy đủ 4 folders: tasks/, system/, sops/, templates/
- Tất cả phải có `readme.md` trong `.agent/`
- `readme.md` phải có Quick Navigation và Directory Structure

### Cập nhật documentation:
- Luôn cập nhật sau khi implement feature mới
- Giữ documentation đồng bộ với code
- Review định kỳ để đảm bảo tính chính xác

## ✅ Checklist cho Agent System mới

Khi tạo agent system mới, đảm bảo:
- [ ] Tạo `.agent/` folder
- [ ] Tạo `tasks/` folder
- [ ] Tạo `system/` folder
- [ ] Tạo `sops/` folder
- [ ] Tạo `templates/` folder (optional)
- [ ] Tạo `readme.md` với đầy đủ sections:
  - [ ] Quick Navigation
  - [ ] Directory Structure diagram
  - [ ] Getting Started guide
  - [ ] Documentation standards
  - [ ] Pre-Implementation Checklist

## 📚 Tài liệu tham khảo

- Xem `CLAUDE.md` trong mỗi agent system để hiểu cách sử dụng
- Xem `readme.md` trong `.agent/` để biết cấu trúc chi tiết
- Tham khảo các agent systems khác để học best practices

---

**Last Updated**: November 2024
**Maintained by**: Development Team

