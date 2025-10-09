# iOS DrJoy Development Commands

## 🎯 Quick Start

**Most Used Command:**
```bash
/01-dev-workflow "your task description"
```
Command này sẽ tự động xác định stage và thực hiện toàn bộ workflow!

## 📁 Structured Command Organization

Commands được organized theo workflow stages với số thứ tự để dễ dàng theo dõi:

```
.claude/commands/
├── 01-workflow/           # 🚀 Main workflow commands
│   └── 01-dev-workflow.md
├── 02-architecture/       # 🏗️ Architecture exploration
│   ├── 01-quick-arch.md
│   └── 02-architecture-explore.md
├── 03-implementation/     # 🛠️ Code changes & fixes
│   └── 01-ios-fix.md
├── 04-quality/           # 🧪 Testing & review
│   └── 01-review-results.md
├── 05-research/          # 🔍 Research & planning
│   ├── 01-research-pro.md
│   ├── 02-architecture-pro.md
│   └── 03-uiux-proposal.md
└── README.md            # This file
```

## 🎯 Command Usage by Stage

### 🚀 Stage 1: Workflow Management
| Command | Mục đích | Khi nào dùng |
|---------|---------|-------------|
| `/01-dev-workflow` | **Main iOS workflow** | Mọi tác vụ - auto detect stage |

### 🏗️ Stage 2: Architecture Understanding
| Command | Mục đích | Khi nào dùng |
|---------|---------|-------------|
| `/01-quick-arch` | **Architecture nhanh** | Cần hiểu structure ngay |
| `/02-architecture-explore` | **Architecture chi tiết** | Cần deep-dive vào component |

### 🛠️ Stage 3: Implementation
| Command | Mục đích | Khi nào dùng |
|---------|---------|-------------|
| `/01-ios-fix` | **iOS-specific fixes** | Bug cụ thể, cần detailed fix |

### 🧪 Stage 4: Quality Assurance
| Command | Mục đích | Khi nào dùng |
|---------|---------|-------------|
| `/01-review-results` | **Code review & HIPAA** | Review implementation results |

### 🔍 Stage 5: Research & Planning
| Command | Mục đích | Khi nào dùng |
|---------|---------|-------------|
| `/01-research-pro` | **External research** | Research công nghệ/thị trường |
| `/02-architecture-pro` | **New architecture** | Design hệ thống mới |
| `/03-uiux-proposal` | **UI/UX planning** | Design và user flow |

## 🔄 Recommended Workflow

### Approach 1: Simple (Đề xuất cho đa số cases)
```bash
# Một command duy nhất cho mọi thứ
/01-dev-workflow "optimize CPU performance in MainTabContainer"
```

### Approach 2: Step-by-step (Khi cần control)
```bash
# 1. Hiểu architecture trước
/01-quick-arch

# 2. Deep-dive nếu cần
/02-architecture-explore "messaging system architecture"

# 3. Implement hoặc fix
/01-ios-fix "specific iOS bug"

# 4. Review và validate
/01-review-results "changes made"
```

### Approach 3: Research-focused (Khi cần explore options)
```bash
# 1. Research external options
/01-research-pro "framework comparison for real-time communication"

# 2. Design new architecture
/02-architecture-pro "microservices for new telehealth platform"

# 3. Plan UI/UX
/03-uiux-proposal "patient onboarding flow design"
```

## 🎯 Usage Examples

### CPU Performance Issues
```bash
# Approach 1: Simple
/01-dev-workflow "optimize CPU usage in reLayoutBadges function"

# Approach 2: Detailed
/01-quick-arch
/01-ios-fix "main thread blocking in MessageVC semaphore.wait"
/01-review-results "CPU performance improvements"
```

### New Feature Implementation
```bash
# Approach 1: Simple
/01-dev-workflow "add voice message recording to chat"

# Approach 2: Detailed
/02-architecture-explore "messaging system architecture"
/01-ios-fix "voice recording with 3 minute limit"
/01-review-results "voice messaging implementation"
```

### Bug Fixes
```bash
# Approach 1: Simple
/01-dev-workflow "fix memory leak in RxSwift subscriptions"

# Approach 2: Detailed
/01-quick-arch
/01-ios-fix "memory leak in MessageVC presenter"
/01-review-results "memory leak fix"
```

### Architecture Investigation
```bash
# Quick overview
/01-quick-arch

# Deep dive
/02-architecture-explore "chat system real-time messaging architecture"
```

### Research & Planning
```bash
# External technology research
/01-research-pro "real-time database comparison for healthcare apps"

# New system architecture design
/02-architecture-pro "design microservices for new telehealth platform"

# UI/UX planning
/03-uiux-proposal "design patient onboarding flow for better adoption"
```

## 🎪 Advanced Usage

### Focus on Specific Stage
```bash
/01-dev-workflow "investigate architecture" --stage=investigate
/01-dev-workflow "implement feature" --stage=implement
/01-dev-workflow "test changes" --stage=test
```

### Focus on Specific Area
```bash
/01-dev-workflow "optimize CPU" --focus=performance
/01-dev-workflow "fix memory leak" --focus=bugfix
/01-dev-workflow "add chat feature" --focus=feature
/01-dev-workflow "understand structure" --focus=architecture
```

## 💡 Key Benefits of Structured Organization

1. **Clear Progression**: Numbered stages show natural workflow progression
2. **Easy Discovery**: Commands organized by purpose and numbered for quick access
3. **Reduced Overhead**: No more confusion about which command to use when
4. **iOS Specialization**: All commands tailored for healthcare app development
5. **Scalable Structure**: Easy to add new commands in appropriate stages

## 🔧 Command Navigation Tips

- **Start with Stage 1**: Always try `/01-dev-workflow` first for auto-detection
- **Architecture First**: Use Stage 2 commands before making changes
- **Implement Carefully**: Stage 3 for specific iOS fixes and changes
- **Quality Assurance**: Stage 4 for healthcare compliance and review
- **Research & Planning**: Stage 5 for exploring new options and systems

**Remember**: Commands are numbered within each stage for consistency. Use the stage number prefix (like `/01-`, `/02-`) for quick access!

---

**✨ Command structure hoàn chỉnh cho iOS DrJoy healthcare app development!**