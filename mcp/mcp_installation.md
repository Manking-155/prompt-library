# Hướng Dẫn Tích Hợp Memory MCP Server

Bộ MCP tĩnh (Memory Server) dùng để trích xuất prompt tự động thông qua Semantic Search hiện đã hoàn tất cài đặt nội bộ.

Để kích hoạt tính năng này vào **Claude Desktop** hoặc **Cursor**, bạn làm theo các bước sau.

## 1. Cài đặt Python Dependencies
Mở Terminal tại thư mục gốc của repo này (`master_prompt/`) và chạy:
```bash
pip install -r mcp/requirements.txt
```

## 2. Nạp dữ liệu (Index Data)
Luôn chạy lệnh sau mỗi khi bạn thêm mới hoặc thay đổi bất kỳ file `.md` nào trong thư viện `prompts/`:
```bash
python mcp/indexer.py
```
*(Script sẽ tự động chạy encode câu thành ma trận Vector và lưu cục bộ vào `.chroma_db/`. Nhờ MD5, nó sẽ bỏ qua các file không đổi).*

## 3. Cấu hình vào Client

### Đối với Claude Desktop
Mở file `claude_desktop_config.json` (Trên MacOS: `~/Library/Application Support/Claude/claude_desktop_config.json`) và thêm block sau:

```json
{
  "mcpServers": {
    "MasterPromptMemory": {
      "command": "fastmcp",
      "args": [
        "run",
        "/absolute/path/to/master_prompt/mcp/server.py"
      ]
    }
  }
}
```
*(Nhớ đổi đường dẫn `/absolute/path/.../` cho đúng với máy tính của bạn).*

### Đối với Cursor
1. Mở Cài đặt (**Cursor Settings** -> **Features** -> **MCP**).
2. Nhấn `+ Add New MCP Server`.
3. Điền thông tin:
   - **Name**: `MasterPromptMemory`
   - **Type**: `command`
   - **Command**: `fastmcp run /Users/djv033/Downloads/iOS_Post/master_prompt/mcp/server.py`
4. Khởi động lại ứng dụng nếu cần.

---
Từ nay về sau, khi bạn chat với Claude/Cursor, bạn chỉ cần gõ:
- *"Tìm giúp tôi prompt đóng vai chuyên gia về React Native"*
- *"Load prompt `tdd-orchestrator.md` vào bộ nhớ và tạo unit test cho class này giúp tôi"*. 

Hệ thống sẽ tự móc nối, tra ChromaDB và nạp thẳng code prompt đó vào Context!
