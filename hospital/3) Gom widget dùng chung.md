Bạn là Codebase Steward. 
Tìm các widget UI có thể TÁI SỬ DỤNG từ các màn: <LIỆT_KÊ_MÀN_HÌNH/FILE>.
Tiêu chí: dùng ở ≥2 feature, không phụ thuộc đặc thù feature.

Yêu cầu:
- Đề xuất danh sách widget chung + props + use-cases.
- Tạo cấu trúc:
  features/utility/
    lib/
      widgets/
        buttons/
        cards/
        forms/
      theme/
        spacing.dart
        typography.dart
        colors.dart
- Viết code mẫu cho 2 widget chung nổi bật (vd: PrimaryActionButton, SectionHeader).
- Cập nhật import ở các feature đang sử dụng (liệt kê patch diff).
- Kiểm tra circular deps: utility không import ngược về feature.

Đầu ra:
- Sơ đồ di chuyển file (from → to).
- CODE cho các widget chung đề xuất.
- Danh sách file cần cập nhật import.
