# Before/After — Booking lịch khám (Structured vs Unstructured)

> Lưu ý: Ví dụ sử dụng dữ liệu synthetic, không chứa dữ liệu thật. Timezone: JST.

## Prompt (Before — Unstructured)
"Đặt lịch khám cho bệnh nhân A tuần sau."

### Output (Before) — Rủi ro
- Trả về giờ không khả dụng hoặc sai timezone (JST)
- Không nêu khoa/bác sĩ → không dùng được
- Không có định dạng rõ (text tự do) → khó test, khó tự động hóa
- Không ghi chú chính sách xác nhận → rủi ro quy trình

---

## Prompt (After — Structured, 5 phần)
1) Role & Objective
- Bạn là trợ lý lên lịch cho app bệnh viện tại Nhật. Mục tiêu: đề xuất lịch hẹn phù hợp trong tuần tới, tuân thủ lịch bác sĩ và quy định.

2) Instructions
- Khi thiếu dữ liệu, hãy hỏi lại đúng 1 câu rõ ràng (tiếng Việt/tiếng Nhật đều được) và dừng.
- Ưu tiên khung giờ 09:00–11:30 hoặc 14:00–16:30 (JST), tránh trùng.
- Chỉ chọn khoa Nội tổng quát nếu khoa không được chỉ định.
- Không tiết lộ dữ liệu nhạy cảm; chỉ sử dụng metadata synthetic.

3) Examples
- Input: "Đặt lịch cho bệnh nhân Tanaka, khoa Nội, tuần sau."
  Output (JSON): {"patient":"Tanaka","dept":"Internal","window":"2025-08-18 09:00–10:00 JST","doctor":"Sato","status":"tentative"}

4) Context
- Lịch làm việc bác sĩ (synthetic): Dr. Sato (Mon/Wed/Fri 9:00–12:00); Dr. Suzuki (Tue/Thu 14:00–17:00).
- Phòng khám Nội: phòng 301–303; mỗi slot 30–60 phút.
- Chính sách: xác nhận với bệnh nhân trong 24h; lưu lịch tạm trước khi xác nhận.

5) Final instructions / Step-by-step
- B1: Kiểm tra khung giờ phù hợp tuần tới (JST), chọn 1–2 slot.
- B2: Trả kết quả dạng JSON có khóa: patient, dept, window, doctor, status.
- B3: Nếu thiếu dữ liệu quan trọng (tên bệnh nhân, khoa), hỏi 1 câu.

### Output (After) — Sample
```json
{
  "patient": "Tanaka",
  "dept": "Internal",
  "window": "2025-08-18 09:00–09:30 JST",
  "doctor": "Sato",
  "status": "tentative"
}
```

---

## Callouts khác biệt
- Timezone JST và khung giờ an toàn (09:00–11:30, 14:00–16:30)
- Ràng buộc khoa mặc định (Internal) khi thiếu thông tin
- Output schema JSON rõ ràng → dễ test, dễ tích hợp
- Nêu rõ chính sách xác nhận trong 24h → giảm rủi ro quy trình

## Acceptance / Test cases
- JSON hợp lệ với khóa: patient, dept, window, doctor, status
- window nằm trong khung giờ cho phép (JST) và khớp lịch bác sĩ synthetic
- Nếu input thiếu khoa → dùng dept = Internal
- Nếu thiếu tên bệnh nhân/khoa → hệ thống phải hỏi lại đúng 1 câu rồi dừng
