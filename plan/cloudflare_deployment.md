# Kế Hoạch Triển Khai Master Prompt Lên Cloudflare

Tài liệu này vạch ra chiến lược để đưa bộ nhớ MCP (Semantic Search) của `prompt-library` lên hệ sinh thái Cloudflare, phục vụ cho việc truy cập từ xa 24/7.

Do môi trường điện toán mây của Cloudflare khác biệt so với local (không chạy trực tiếp được Python/ChromaDB), tài liệu này phác thảo 2 hướng đi tối ưu nhất:

---

## Phương Án A: Cloudflare Tunnels (Giữ lại Code Python Local)

Phương pháp nhanh nhất, an toàn nhất, ít tốn chi phí lập trình lại. Nó thiết lập một đường hầm bảo mật từ máy Mac của bạn ra Internet.

### Quy Trình Triển Khai
1. **Cài đặt Cloudflared:** Dùng Homebrew `brew install cloudflared`.
2. **Khởi chạy Python FastMCP Server:** Lắng nghe ở một port cục bộ (Ví dụ `localhost:8000`). Mặc định FastMCP có lệnh `fastmcp dev server.py`.
3. **Mở Hầm (Tunnel):** Chạy lệnh `cloudflared tunnel --url http://localhost:8000`.
4. **Cấu hình trên AI Client:** Ở một máy tính khác, điền đường dẫn URL của Tunnel vào Cursor hoặc Claude Desktop.

**Ưu điểm:** Giữ nguyên 100% sức mạnh code hiện hành và dữ liệu ở local.
**Nhược điểm:** Phụ thuộc máy tính phát (Mac) phải luôn bật.

---

## Phương Án B: Cloudflare Workers AI + Vectorize (Serverless 100%)

Đây là phương án tối thượng để giải quyết dứt điểm tính phụ thuộc. Không cần bật máy tính, mô hình AI tự xử lý bằng sức mạnh hạ tầng Cloudflare.

### Kiến Trúc Mới
1. **Database:** Dùng [Cloudflare Vectorize](https://developers.cloudflare.com/vectorize/) làm VectorDB thay cho ChromaDB.
2. **Embeddings:** Gọi Model [@cf/baai/bge-small-en-v1.5](https://developers.cloudflare.com/workers-ai/models/bge-small-en-v1.5/) của Cloudflare Workers AI để thực hiện việc nhúng ngữ nghĩa siêu tốc.
3. **Lưu Trữ Text:** Lưu raw Markdown vào định dạng JSON trên Cloudflare KV.
4. **API Server:** Viết lại `server.py` bằng **TypeScript** sử dụng bộ thư viện chính chủ `@modelcontextprotocol/sdk`. Deploy dưới dạng một Cloudflare Worker.

### Các Bước Thực Thi Cụ Thể (Task List)
- [] **Bước 1 (Backend Core):** Khởi tạo project Wrangler TS (`npm create clouflare`).
- [] **Bước 2 (Mã Hóa):** Cấu hình Binding cho KV, Vectorize và AI AI trong `wrangler.toml`.
- [] **Bước 3 (Ingest Data):** Tạo một script TypeScript đẩy toàn bộ file `.md` trong thư mục `prompts/` lên KV và gọi lệnh insert Vector vào Vectorize.
- [] **Bước 4 (MCP Endpoint):** Lập trình SSE (Server-Sent Events) endpoint thông qua `McpServer` class của SDK. Xử lý các logic Search và Fetch prompt content.
- [] **Bước 5 (Deploy & Bảo Mật):** `wrangler deploy` và set các Service Token (Cloudflare Access) để đảm bảo không ai ngoại trừ bạn được quyền gọi API này hòng đánh cắp kho tri thức.

---
## Khuyến Nghị Tiếp Theo
Bạn có thể cân nhắc bắt đầu với **Phương Án A** để thẩm định mức độ lợi ích của việc "remote Call" trước khi đầu tư nhân lực lập trình TS dời đô hoàn toàn bằng **Phương Án B**.
