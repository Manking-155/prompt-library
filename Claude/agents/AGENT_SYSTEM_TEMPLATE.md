# Agent System Template

Template này dùng để tạo agent system mới với cấu trúc thống nhất.

## 📋 Cấu trúc thư mục

```
agent_system_name/
├── CLAUDE.md                    # Hướng dẫn sử dụng agent system
├── ARCHITECTURE.md              # (Optional) Architecture documentation
├── README.md                    # (Optional) Overview documentation
└── .agent/
    ├── readme.md               # Index của tất cả documentation
    ├── tasks/                  # PRD & implementation plans
    │   └── README.md           # Index của tasks
    ├── system/                 # System documentation
    │   └── project_architecture.md
    ├── sops/                   # Standard Operating Procedures
    │   └── (add your SOPs here)
    └── templates/              # Reusable templates
        └── (add your templates here)
```

## 📝 Các bước tạo Agent System mới

### 1. Tạo cấu trúc thư mục
```bash
mkdir -p agent_system_name/.agent/{tasks,system,sops,templates}
```

### 2. Tạo CLAUDE.md
Copy từ một agent system khác và customize:
```markdown
# DOCS

We keep all important docs in agent folder and keep updating them, structure like below
.agent
- Tasks: PRD & implementation plan for each feature
- System: Document the current state of the system (project structure, tech stack, integration points,
database schema, and core functionalities such as agent architecture, LLM layer, etc.)
- SOP: Best practices of execute certain tasks (e.g. how to add a schema migration, how to add a new page route, etc.)
- README.md: an index of all the documentations we have so people know what & where to look for things
We should always update agent docs after we implement certain featrue, to make sure it fully reflect the up to date information
Before you plan any implementation, always read the .agent/README first to get context
```

### 3. Tạo .agent/readme.md
Sử dụng template từ các agent systems khác và customize:
- Quick Navigation
- Directory Structure
- Getting Started
- Documentation standards

### 4. Tạo .agent/tasks/README.md
```markdown
# Tasks

This directory contains PRDs and implementation plans for each feature.

## Structure
Each task should be organized as:
- `feature-name.md` - PRD for the feature
- `feature-name-implementation.md` - Implementation plan

## Current Tasks
_(No tasks yet)_
```

### 5. Tạo system documentation
Bắt đầu với `system/project_architecture.md`:
- Project structure
- Tech stack
- Key patterns
- Integration points

### 6. Tạo SOPs
Tạo các SOP cần thiết trong `sops/`:
- Development workflow
- Common tasks
- Best practices

### 7. Tạo templates
Tạo các templates tái sử dụng trong `templates/`:
- Feature templates
- Code snippets
- Documentation templates

## ✅ Checklist

Khi tạo agent system mới, đảm bảo:
- [ ] Cấu trúc thư mục đầy đủ: tasks/, system/, sops/, templates/
- [ ] CLAUDE.md đã được tạo
- [ ] .agent/readme.md đã được tạo với đầy đủ sections
- [ ] .agent/tasks/README.md đã được tạo
- [ ] System documentation ban đầu đã có
- [ ] Ít nhất 1 SOP đã được tạo
- [ ] Ít nhất 1 template đã được tạo (optional)

## 📚 Tham khảo

Xem các agent systems hiện có để học best practices:
- `flutter_agent_system_en` - Flutter development system
- `mobile_dev_agent_system` - Mobile development system
- `solo_expansion_system_agent` - Business expansion system

---

**Last Updated**: November 2024

