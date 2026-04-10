# 🪵 Obsidian Prompt Guide — prompt-library Library

> **Context:** Hệ thống này được tối ưu hóa cho người dùng **Obsidian** để quản lý tri thức (PKM) và vận hành multi-agent workflow.

---

## 1. Setup Obsidian Library

### Cấu trúc Vault Khuyến nghị
Bạn nên mount folder `prompt-library/prompts` trực tiếp vào Vault hoặc sử dụng symlink:

```bash
ln -s /path/to/prompt-library/prompts ~/ObsidianVault/Prompts
```

### Obsidian Plugins Hữu ích
- **Templater**: Để chèn nhanh các role/context vào note hiện tại.
- **Dataview**: Để tạo dashboard catalog tự động dựa trên YAML frontmatter.
- **Smart Connections**: Để AI tự động tìm prompt liên quan đến nội dung bạn đang viết.

---

## 2. Cách Sử dụng Prompts

### Pattern 1: Role Activation (Templater)
Khi bạn cần một chuyên gia (VD: SEO Specialist), tạo note mới và dùng Templater để nạp role:

```markdown
# [Project Name] Strategy
<% tp.file.include("[[seo-specialist]]") %>
```

### Pattern 2: Context Linking
Sử dụng tính năng **Internal Link** của Obsidian để liên kết các thành phần:

- Liên kết Project Brief với **[[marketing-campaign-generator]]**
- Liên kết Result với **[[seo-content-auditor]]** để review.

---

## 3. Quản lý Meta-Data
Tất cả prompt mới đều có chuẩn YAML frontmatter:

```yaml
---
name: role-name
category: role|task|workflow
version: "1.1"
tags: [ios, marketing]
---
```

Bạn có thể dùng **Dataview** để liệt kê nhanh:

```dataview
TABLE category, version, tags
FROM "Prompts"
WHERE category = "role"
SORT name ASC
```

---

## 4. Workflow Thực tế (Swarm Operator)

1. **Step 1: Planning**
   Mở **[[deep-research-assistant]]** để xây dựng kế hoạch nghiên cứu thị trường.
   
2. **Step 2: Execution**
   Sử dụng **[[marketing-campaign-generator]]** kết hợp với **[[context-wave-agency]]** để tạo chiến dịch.
   
3. **Step 3: Refinement**
   Dùng các **Tone Guides** (như **[[tone-thought-leader]]**) để tinh chỉnh giọng văn AI cho Obsidian notes.

---

## 5. Lưu ý quan trọng
- **Không chỉnh sửa nội dung gốc**: Nếu muốn customize, hãy copy sang note mới hoặc sử dụng Obsidian Properties để ghi đè.
- **Version Control**: Thư viện này được quản lý bằng Git (prompt-library), hãy `git pull` thường xuyên để cập nhật các frameworks mới.
