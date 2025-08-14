# Before/After — EHR Query / Báo cáo (Structured vs Unstructured)

> Lưu ý: Ví dụ synthetic; ẩn thông tin nhận dạng. Tuân thủ phân quyền báo cáo.

## Before (Unstructured)

"Xuất danh sách bệnh nhân tiểu đường trong quý 1."

- Không rõ tiêu chí lâm sàng/codeset
- Không rõ trường cần export / định dạng file
- Không đề cập ẩn danh hóa / kiểm soát truy cập
- Không có tiêu chí kiểm thử

## After (Structured — 5 phần)

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

---

### Đầu ra mong muốn (Acceptance)
- CSV schema rõ ràng, không PII.
- Có tiêu chí lọc traceable (HbA1c/ICD-10) và thời gian.
- Dễ test (validate header; kiểm tra không có PII).