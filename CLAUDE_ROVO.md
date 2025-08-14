# CLAUDE_ROVO — Context & Conventions

Audience & Purpose
- Audience: Dev, Sales, OA tại công ty phát triển app quản lý bệnh viện ở Nhật
- Mục tiêu: Deck nội bộ cho talk 10' + 5' Q&A về kỹ thuật viết prompt (structured prompting)
- Yêu cầu: Không dùng dữ liệu thật; ví dụ synthetic, ẩn danh. Tuân thủ phân quyền báo cáo/tiếp cận dữ liệu.

Operating mode (Safety-first)
- Agent luôn xin phép trước khi chạy lệnh hệ thống (git, npm, npx) hoặc thay đổi nhiều file
- Không chèn secrets; không commit thông tin nhạy cảm; không đưa PII vào ví dụ
- Tuân thủ chuẩn review: PR nhỏ gọn theo batch, mô tả rõ ràng, có checklist "how to run"

Directory & Tooling
- src/slides.md: deck chính (Marp front-matter) — 7–10 slides, 1 ý/slide, có speaker notes
- src/partials/*: block tái sử dụng (before/after, checklist, template 5 phần)
- themes/marp.css: CSS cho Marp (font Noto Sans/Arial, màu an toàn; Before/After high-contrast)
- themes/reference.pptx: PPTX template tối giản (placeholder — thay bằng template brand nội bộ khi sẵn sàng)
- reveal/*.css|json: cấu hình reveal-md để preview HTML
- dist/: output (PPTX/PDF) — không commit file build

Commands
- Dev/Preview (HTML): `npm run dev` (watch) hoặc `npm run preview`
- Build Marp PPTX: `npm run build:pptx`
- Build Marp PDF: `npm run build:pdf`
- Build Pandoc PPTX: `npm run build:pandoc` (cần cài pandoc hệ thống)
- Build tất cả: `npm run build:all`

Conventions & Style
- Mỗi slide 1 ý, ≤ 6 bullet; ưu tiên ngắn gọn, actionable
- Prompt theo khung 5 phần: Role & Objective, Instructions, Examples, Context, Final instructions/Step-by-step
- Output có thể test/traceable (JSON/CSV schema + acceptance)
- Nhấn mạnh bối cảnh Nhật (thoroughness, chất lượng, kiểm soát truy cập)

Review Checklist (rút gọn)
- [ ] Không dùng dữ liệu thật / PII
- [ ] Có đủ 5 phần & acceptance
- [ ] Output testable (schema + điều kiện kiểm thử)
- [ ] Phản ánh phân quyền/tuân thủ trong bối cảnh EHR/reporting
- [ ] Nội dung phù hợp Dev/Sales/OA

Prompt suggestions (để cập nhật deck theo sprint/ticket Jira)
- "Cập nhật slide How-to với template checklist mới ở ticket JIRA-123, thêm bước 'security review'"
- "Sinh thêm 1 cặp Before/After cho flow 'đổi lịch hẹn' (rescheduling) với acceptance JSON"
- "Điền ví dụ CSV 5 dòng synthetic cho KPI quý 2, không PII"
- "Tạo slide backup về 'LLM guardrails' — boundaries cho Sales demo"

Notes
- Nếu `themes/reference.pptx` là placeholder, hãy thay bằng template brand thật trước khi `npm run build:pandoc`
- Với reveal-md, fragments và progress đã bật trong `reveal/reveal.config.json`
