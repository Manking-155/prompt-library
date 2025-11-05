# Quick Reference Guide - Agent Systems

Hướng dẫn nhanh để sử dụng agent systems.

## 🚀 Quick Start

### 1. Chọn Agent System phù hợp
- **Flutter Development**: `flutter_agent_system_en/`
- **Mobile Development**: `mobile_dev_agent_system/` hoặc `mobile_dev_agent_system_english/`
- **Solo Expansion**: `solo_expansion_system_agent/`

### 2. Đọc documentation
```bash
# Đọc CLAUDE.md trong agent system
cat agent_system_name/CLAUDE.md

# Đọc .agent/readme.md để có context
cat agent_system_name/.agent/readme.md
```

### 3. Bắt đầu implementation
```bash
# Kiểm tra tasks/ để xem PRDs hiện có
ls agent_system_name/.agent/tasks/

# Xem system architecture
ls agent_system_name/.agent/system/

# Xem SOPs
ls agent_system_name/.agent/sops/

# Xem templates
ls agent_system_name/.agent/templates/
```

## 📋 Cấu trúc thống nhất

Tất cả agent systems có cấu trúc:
```
.agent/
├── tasks/          # PRD & implementation plans
├── system/         # System documentation
├── sops/           # Standard Operating Procedures
├── templates/      # Reusable templates
└── readme.md       # Index file
```

## 🎯 Common Tasks

### Tạo task mới:
1. Tạo PRD trong `tasks/`
2. Tạo implementation plan trong `tasks/`
3. Update `tasks/README.md` nếu cần

### Thêm SOP:
1. Tạo file trong `sops/`
2. Update `readme.md` với link mới

### Thêm template:
1. Tạo file trong `templates/`
2. Update `readme.md` với link mới

### Cập nhật system docs:
1. Update files trong `system/`
2. Update `readme.md` nếu có thay đổi lớn

## 📚 File Locations

### Documentation Files:
- **Root**: `ARCHITECTURE.md`, `AGENT_SYSTEM_TEMPLATE.md`, `CHANGELOG.md`
- **Agent System**: `CLAUDE.md`, `.agent/readme.md`
- **Tasks**: `.agent/tasks/README.md`
- **System**: `.agent/system/`
- **SOPs**: `.agent/sops/`
- **Templates**: `.agent/templates/`

## ✅ Checklist trước khi bắt đầu

- [ ] Đã đọc `CLAUDE.md` trong agent system
- [ ] Đã đọc `.agent/readme.md`
- [ ] Đã kiểm tra `tasks/` để xem PRDs hiện có
- [ ] Đã hiểu `system/` architecture
- [ ] Đã xem `sops/` cho workflows
- [ ] Đã check `templates/` nếu cần

## 🔧 Quick Commands

### List all agent systems:
```bash
ls -d */ | grep -E "(flutter|mobile|solo)"
```

### Check structure:
```bash
# Check if .agent/ exists
ls -la agent_system_name/.agent/

# Check folders
ls -la agent_system_name/.agent/{tasks,system,sops,templates}/
```

### Find readme files:
```bash
find . -name "readme.md" -path "*/.agent/*"
```

## 📝 Documentation Standards

Tất cả `readme.md` phải có:
- ✅ Quick Navigation
- ✅ Directory Structure diagram
- ✅ Getting Started guide
- ✅ Documentation standards
- ✅ Pre-Implementation Checklist

## 🎯 Agent Systems Map

| Agent System | Purpose | Language | Status |
|-------------|---------|----------|--------|
| `flutter_agent_system_en` | Flutter development | English | ✅ |
| `mobile_dev_agent_system` | Mobile development | Vietnamese | ✅ |
| `mobile_dev_agent_system_english` | Mobile development | English | ✅ |
| `solo_expansion_system_agent` | Solo expansion | English | ✅ |
| `solo_expansion_system` | Solo expansion | Vietnamese | ✅ |
| `solo_expansion_system_english` | Solo expansion | English | ✅ |

## 💡 Tips

1. **Always start** with `.agent/readme.md`
2. **Check tasks/** before creating new ones
3. **Follow SOPs** for consistency
4. **Update docs** as you go
5. **Use templates** when available
6. **Keep structure** consistent

---

**Last Updated**: November 2024

