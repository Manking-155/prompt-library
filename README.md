# 🧠 Master Prompt Library

Chào mừng bạn đến với Thư Viện Prompt chuẩn hóa (Version 2.0). 

**AI / agent map:** see [`.docs/SITE.md`](.docs/SITE.md) for responsibilities, key paths, and link to Moboco portfolio doc canon (`ios-knowledge`).

## 🗺 Cấu trúc Repository

Mọi Prompt trong kho lưu trữ này đều được quản lý với tư tưởng **Prompt As Code**, có Versioning và YAML Metadata rõ ràng.

Thuộc tính cốt lõi bao gồm:
*   **`prompts/meta/`**: Các meta-prompt dùng để gen ra prompters, digital-twins, và interactive structures.
*   **`prompts/roles/`**: Các Specialist Personas (Mentor, SEO, Marketing, Developer, v.v.).
*   **`prompts/workflows/`**: Quy trình SOPs, Research Pipeline và quy trình nội bộ.
*   **`prompts/tasks/`**: Các task cụ thể (Campaign Strategy, Paid Ads, Social Media, v.v.).
*   **`prompts/guidelines/`**: Tone of Voice guidelines, tiêu chuẩn hành văn AI-friendly.
*   **`prompts/components/`**: Các khối ngữ cảnh cố định (vd: Agency Context Loader).
*   **`inboxes/`**: Chứa Logs thô, CSV data, và Archive (bị Claude ignore để tránh nhiễu).
*   **`docs/`**: Chứa nội dung bài học, guideline và meta data.

## ⚙️ Quy tắc đóng góp
Hãy sử dụng format chuẩn YAML Metadata được quy định tại `AGENTS.md` (phiên bản 1.1) để cấu trúc prompt mới nhất quán.
Tham khảo `prompts/guidelines/obsidian-prompt-guide.md` để tích hợp chuẩn với Obsidian PKM workflow.
