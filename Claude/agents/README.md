# Agent Systems Directory

Thư mục này chứa tất cả các agent systems được chuẩn hóa với cấu trúc thống nhất.

## 📋 Tổng quan

Tất cả các agent systems trong thư mục này tuân theo cấu trúc `.agent/` thống nhất:

```
.agent/
├── tasks/          # PRD & implementation plans cho mỗi feature/project
├── system/         # System documentation và architecture
├── sops/           # Standard Operating Procedures
├── templates/      # Reusable templates (optional nhưng recommended)
└── readme.md       # Index của tất cả documentation
```

## 🎯 Các Agent Systems

### 1. Flutter Agent Systems

#### `flutter_agent_system_en/`
- **Mục đích**: Flutter development với Modular Clean Architecture và GetX
- **Language**: English
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Key Features**: 
  - Clean Architecture (3-layer)
  - Modular Architecture
  - GetX State Management
  - Drift ORM

#### `flutter_agent_system/`
- **Mục đích**: Flutter development system (Vietnamese)
- **Language**: Vietnamese
- **Status**: ⚠️ Cần kiểm tra chuẩn hóa

### 2. Mobile Development Agent Systems

#### `mobile_dev_agent_system/`
- **Mục đích**: Mobile development workflow và AI integration (Vietnamese)
- **Language**: Vietnamese
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Key Features**: 
  - Flutter/iOS development
  - AI tools integration (Claude, Cursor)
  - Database-first architecture

#### `mobile_dev_agent_system_english/`
- **Mục đích**: Mobile development workflow và AI integration (English)
- **Language**: English
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Key Features**: 
  - Flutter/iOS development
  - AI tools integration (Claude, Cursor)
  - Database-first architecture

### 3. Solo Expansion Agent Systems

#### `solo_expansion_system_agent/`
- **Mục đích**: Transition từ employee developer sang solo developer/entrepreneur
- **Language**: English
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md
- **Key Features**: 
  - Business architecture
  - Financial systems
  - Marketing & client acquisition
  - Work-life balance

#### `solo_expansion_system/`
- **Mục đích**: Solo expansion system (Vietnamese)
- **Language**: Vietnamese
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md

#### `solo_expansion_system_english/`
- **Mục đích**: Solo expansion system (English)
- **Language**: English
- **Status**: ✅ Đã chuẩn hóa
- **Structure**: tasks/, system/, sops/, templates/, readme.md

### 4. Other Agent Systems

#### `ai_interaction_habits_system/`
- **Mục đích**: AI interaction habits và optimization
- **Status**: ⚠️ Chưa có .agent/ structure
- **Note**: Cần chuẩn hóa nếu cần sử dụng

## 📚 Documentation Files

### Root Level Documentation:
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Mô tả cấu trúc thống nhất cho tất cả agent systems
- **[AGENT_SYSTEM_TEMPLATE.md](AGENT_SYSTEM_TEMPLATE.md)** - Template để tạo agent system mới
- **[CHANGELOG.md](CHANGELOG.md)** - Ghi lại tất cả thay đổi
- **[CLAUDE.md](CLAUDE.md)** - Hướng dẫn sử dụng agent folder structure

### Verification:
- **[.agent-structure-verification.md](.agent-structure-verification.md)** - Xác nhận tất cả thay đổi đã thực hiện

## 🚀 Sử dụng Agent Systems

### Bắt đầu với Agent System:
1. Đọc `CLAUDE.md` trong agent system để hiểu cách sử dụng
2. Đọc `.agent/readme.md` để có context đầy đủ
3. Kiểm tra `tasks/` để xem PRDs và plans hiện có
4. Xem `system/` để hiểu architecture
5. Tham khảo `sops/` cho workflows
6. Sử dụng `templates/` khi cần

### Quy tắc chung:
- **Luôn đọc** `.agent/readme.md` trước khi bắt đầu implementation
- **Cập nhật** documentation sau khi implement feature mới
- **Tạo PRD** trong `tasks/` cho features mới
- **Follow SOPs** trong `sops/` cho các tasks

## 📝 Tạo Agent System Mới

Để tạo agent system mới:
1. Xem **[AGENT_SYSTEM_TEMPLATE.md](AGENT_SYSTEM_TEMPLATE.md)** để biết cấu trúc
2. Tạo cấu trúc `.agent/` với đầy đủ folders
3. Tạo `readme.md` với Quick Navigation và Directory Structure
4. Tạo `tasks/README.md` để hướng dẫn
5. Tạo system documentation ban đầu
6. Tạo ít nhất 1 SOP và 1 template

## ✅ Checklist cho Agent System Mới

- [ ] Cấu trúc thư mục đầy đủ: tasks/, system/, sops/, templates/
- [ ] CLAUDE.md đã được tạo
- [ ] .agent/readme.md đã được tạo với đầy đủ sections
- [ ] .agent/tasks/README.md đã được tạo
- [ ] System documentation ban đầu đã có
- [ ] Ít nhất 1 SOP đã được tạo
- [ ] Ít nhất 1 template đã được tạo (optional)

## 🔄 Maintenance

### Chuẩn hóa cấu trúc:
- Tất cả agent systems phải có đầy đủ 4 folders: tasks/, system/, sops/, templates/
- Tất cả phải có `readme.md` trong `.agent/`
- `readme.md` phải có Quick Navigation và Directory Structure

### Cập nhật documentation:
- Luôn cập nhật sau khi implement feature mới
- Giữ documentation đồng bộ với code
- Review định kỳ để đảm bảo tính chính xác

## 📊 Status Summary

- **Total Agent Systems**: 7+
- **Standardized Systems**: 6
- **Standardization Rate**: ~85%
- **Documentation Files**: 4
- **Last Updated**: November 2024

## 🎯 Best Practices

1. **Always read** `.agent/readme.md` first
2. **Check tasks/** for existing PRDs before starting
3. **Follow SOPs** for consistent workflows
4. **Update docs** after implementing features
5. **Use templates** for consistency
6. **Keep structure** consistent across all systems

## 📞 Support

- Xem **[ARCHITECTURE.md](ARCHITECTURE.md)** để hiểu cấu trúc thống nhất
- Xem **[AGENT_SYSTEM_TEMPLATE.md](AGENT_SYSTEM_TEMPLATE.md)** để tạo system mới
- Xem **[CHANGELOG.md](CHANGELOG.md)** để track changes
- Xem `.agent/readme.md` trong mỗi system để biết chi tiết

---

**Last Updated**: November 2024
**Maintained by**: Development Team

