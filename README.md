# 🧠 Master Prompt Library

Chào mừng bạn đến với Thư Viện Prompt chuẩn hóa. 

## 🗺 Cấu trúc Repository

Mọi Prompt trong kho lưu trữ này đều được quản lý với tư tưởng **Prompt As Code**, có Versioning và YAML Metadata rõ ràng.

Thuộc tính cốt lõi bao gồm:
*   **`prompts/agents/`**: Core Personas, System Prompts được dùng để override rules cho Agents.
*   **`prompts/skills/`**: Các mảnh prompt nhỏ thực thi tác vụ cụ thể.
*   **`prompts/workflows/`**: Chuỗi Prompt cấu thành pipeline tự động.
*   **`prompts/experiments/`**: Khu thử nghiệm A/B Testing, Sandbox.
*   **`inboxes/`**: Chứa Logs thô, CSV data, và Archive (bị Claude ignore để tránh nhiễu).
*   **`docs/`**: Chứa nội dung bài học, guideline và meta data.

## ⚙️ Quy tắc đóng góp
Hãy copy file `.templates/PROMPT_TEMPLATE.md` để khởi tạo một Prompt mới với cấu trúc siêu bền vững!
