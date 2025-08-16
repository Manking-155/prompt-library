# Before/After — EHR Query / Báo cáo (Structured vs Unstructured)

> Lưu ý: Ví dụ synthetic; ẩn thông tin nhận dạng. Tuân thủ phân quyền báo cáo.

## Prompt (Before — Unstructured)
"Xuất danh sách bệnh nhân tiểu đường trong quý 1."

### Output (Before) — Rủi ro
- Có thể trả về PII (tên/địa chỉ) → vi phạm tuân thủ
- Không tiêu chí lâm sàng/codeset → kết quả không traceable
- Không schema CSV rõ → khó test tự động, khó import BI

---

## Prompt (After — Structured, 5 phần)
1) Role & Objective
- Bạn là trợ lý báo cáo cho hệ thống EHR. Mục tiêu: tạo báo cáo tổng hợp tuân thủ, không lộ PII.

2) Instructions
- Chỉ sử dụng dữ liệu tổng hợp đã ẩn danh, không xuất PII (tên, địa chỉ, số hồ sơ).
- Nếu cần lọc bệnh tiểu đường, dùng tiêu chí: HbA1c >= 6.5% hoặc ICD-10 E11.* (ví dụ synthetic).
- Đầu ra CSV; phân tách bằng dấu phẩy, UTF-8, header rõ ràng.

3) Examples
- Input: "Quý 1FY2025 (Apr–Jun), lọc HbA1c >= 6.5%, khoa Nội."
  Output (CSV header): patient_id_hash, quarter, condition, dept, age_band, visits, medication_flag

4) Context
- Năm tài chính Nhật: FY2025 (Apr 2025 – Mar 2026); Quý 1: Apr–Jun.
- Phân quyền: chỉ người có vai trò Report Analyst mới truy cập.
- KPI: số bệnh nhân theo age_band (20s/30s/…), visits, medication_flag (metformin/insulin; synthetic).

5) Final instructions / Step-by-step
- B1: Xác định khoảng thời gian, tiêu chí lọc rõ ràng.
- B2: Xây dựng schema CSV (các cột như phần Examples) và xuất sample 5 dòng synthetic.
- B3: Nhắc nhở kiểm tra phân quyền trước khi truy cập.

### Output (After) — Sample (CSV)
```
patient_id_hash,quarter,condition,dept,age_band,visits,medication_flag
b1a2c3,2025Q1,diabetes,Internal,50s,3,metformin
c9d8e7,2025Q1,diabetes,Internal,40s,1,insulin
f0e1d2,2025Q1,diabetes,Internal,30s,2,none
ab12cd,2025Q1,diabetes,Internal,60s,4,metformin
9f8e7d,2025Q1,diabetes,Internal,20s,1,none
```

---

## Callouts khác biệt
- Không PII; chỉ patient_id_hash (ẩn danh)
- Tiêu chí traceable: HbA1c>=6.5% hoặc ICD-10 E11.*
- CSV header rõ ràng → dễ test và nhập vào BI
- Nhắc kiểm tra phân quyền trước truy cập

## Acceptance / Test cases
- Header CSV đúng: patient_id_hash, quarter, condition, dept, age_band, visits, medication_flag
- Không có PII ở data rows
- quarter phù hợp phạm vi thời gian đã nêu
- Có thể dùng test tự động để kiểm tra header và absence of PII
