---
marp: true
title: Ky thuat viet prompt (10' talk + 5' Q&A)
paginate: true
theme: default
---

<!-- Slide 1: Hook -->
# Prompt tệ → Kết quả tệ

- Đặt lịch khám/Truy vấn dashboard với câu lệnh mơ hồ
- Mất thời gian hỏi lại, rủi ro QA/bug
- Structured prompting giúp tiết kiệm thời gian, nâng chất lượng

<!-- Speaker notes: 45s -->
<!--
Ví dụ mơ hồ: "Đặt lịch cho bệnh nhân tuần sau"; hệ thống không biết khoa, bác sĩ, giờ JST.
Nhấn mạnh: 10' talk + 5' Q&A, mục tiêu đưa framework áp dụng ngay.
-->

---

<!-- Slide 2: Vấn đề -->
# Vì sao Structured Prompting quan trọng?

- Giảm mơ hồ → ít vòng hỏi đáp
- Kết quả có thể test/traceable
- Tăng năng suất Dev/Sales/OA, giảm QA/bug

<!-- Speaker notes: 60s -->
<!--
Liên hệ bối cảnh Nhật: thoroughness, chất lượng, đồng thuận. Chuẩn hóa giúp scale.
-->

---

<!-- Slide 3: Framework 5 phần -->
# Framework 5 phần

1) Role & Objective  
2) Instructions  
3) Examples  
4) Context  
5) Final instructions / Step-by-step

<!-- Speaker notes: 60s -->
<!--
Nêu rõ mỗi phần có vai trò gì; sample ở slide sau.
-->

---

<!-- Slide 4: Before/After 1 (Booking) -->
# Before/After: Đặt lịch khám

<div class="two-col">

| Before | After |
|---|---|
| "Đặt lịch cho bệnh nhân A tuần sau" | 5 phần: Role, Instructions, Examples, Context, Steps |
| Mơ hồ: khoa/giờ/doctor | Rõ constraint JST, slot, khoa mặc định |
| Không output schema | JSON schema + acceptance |

</div>

<!-- Speaker notes: 90s -->
<!--
Dẫn nhập từ partials. Nhấn mạnh callouts cải thiện: JST, slot, schema, hỏi lại khi thiếu.
-->

---

<!-- Slide 5: Before/After 2 (EHR/Report) -->
# Before/After: Báo cáo EHR

<div class="two-col">

| Before | After |
|---|---|
| "Xuất danh sách bệnh nhân ĐTĐ Q1" | 5 phần đầy đủ + tuân thủ |
| Không tiêu chí lâm sàng | HbA1c>=6.5% hoặc ICD-10 E11.* (synthetic) |
| Rủi ro PII | Ẩn danh, CSV header rõ ràng |

</div>

<!-- Speaker notes: 90s -->
<!--
Nhấn mạnh phân quyền, không PII, tiêu chí traceable, dễ test (validate header).
-->

---

<!-- Slide 6: Component breakdown -->
# Viết tốt từng phần + Anti-patterns

- Role & Objective: nêu vai trò hệ thống + mục tiêu đo được
- Instructions: ràng buộc, lỗi phổ biến: quá dài, mâu thuẫn
- Examples: ít nhưng đại diện, lỗi: ví dụ không khớp bối cảnh
- Context: metadata cần thiết, lỗi: lộ dữ liệu thật
- Final steps: yêu cầu output + acceptance; lỗi: không có schema

<!-- Speaker notes: 75s -->

---

<!-- Slide 7: Business impact (Nhật) -->
# Business impact (Nhật)

- Phù hợp văn hóa thoroughness, chất lượng cao
- Dev: giảm vòng QA, logs dễ truy vết
- Sales: demo/PoC ổn định, dễ tuỳ biến
- OA: thao tác chuẩn, giảm sai lệch

<!-- Speaker notes: 60s -->

---

<!-- Slide 8: How-to team áp dụng -->
# How-to áp dụng trong team

- Dùng template 5 phần + checklist review
- Mapping từ ticket → prompt (acceptance rõ)
- Lưu prompt vào repo (partials), versioning qua PR

<!-- Speaker notes: 60s -->

---

<!-- Slide 9: Call-to-action -->
# Call-to-action (Sprint này)

- Chọn 1 flow: đặt lịch hoặc EHR report
- Viết prompt 5 phần + acceptance
- PR review theo checklist; demo cuối sprint

<!-- Speaker notes: 30s -->

---

<!-- Slide 10: Backup FAQs -->
# FAQs (Backup)

- Structured có làm chậm? → Ban đầu có, nhưng giảm vòng QA → tổng thể nhanh hơn
- Dữ liệu thật? → Không; dùng synthetic + ẩn danh, kiểm soát truy cập
- Guardrails & Rescheduling? → Xem partials: `src/partials/guardrails.md`, `src/partials/before_after_reschedule.md`
- Tooling? → Marp/Pandoc/Reveal; xuất PPTX/PDF/HTML dễ chia sẻ

<!-- Speaker notes: 30s -->

---

<!-- Slide 11: Backup — LLM Guardrails -->
# LLM Guardrails (Backup)

- Data minimization, access control, no PII in outputs
- Ask once for missing info; refuse out-of-scope/jailbreak
- Constrain outputs to JSON/CSV schemas
- Xem: `src/partials/guardrails.md`

<!-- Speaker notes: 30s -->
