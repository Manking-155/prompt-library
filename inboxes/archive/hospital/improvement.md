1) Prompt rà soát & đề xuất tách file quá dài
Bạn là Flutter Architect.
Dựa trên kiến trúc feature-based sau:
- Presentation: views/ (UI), controllers/ (GetX), bindings/
- Mỗi feature có routes/ riêng, utility chung ở features/utility/

Hãy RÀ SOÁT các màn hình Flutter sau và đề xuất cách tách nhỏ:
<LIỆT_KÊ_CÁC_FILE>. 
Tiêu chí dài: >300 dòng hoặc >3 responsibilities UI.

Đầu ra YAML (ngắn gọn):
- screen: <tên màn>
- hot-spots: [list vùng UI phức tạp kèm số dòng]
- đề-xuất-widget-con:
  - name: <PatientHeaderCard>
    src-lines: <80-160>
    props: { patient: Patient }
    logic: "chỉ UI, không chứa business"
  - ...
- move-to-utility (nếu có):
  - name: <PrimaryActionButton>
    reason: "được dùng ở >2 feature"
    path: features/utility/lib/widgets/primary_action_button.dart
- side-effects:
  - routes: <có/không> (nếu đổi file import)
  - bindings: <có/không>
  - controller: <cần tách logic/không>

2) Prompt sinh code refactor widget con cho 1 màn hình
Bạn là Senior Flutter Engineer, dùng GetX. 
Nhiệm vụ: TÁCH NHỎ màn hình <PatientDetailView> (path: <feature>/lib/app/presentation/views/patient_detail_view.dart).

Yêu cầu:
- Chia thành các widget con theo đề xuất:
  1) PatientHeaderCard (shows avatar, name, age, ID, BHYT)
  2) VitalsSection (BP, HR, SpO2, Temp)
  3) AppointmentsSection (list)
  4) PrescriptionsSection (list)
- Mỗi widget con đặt trong: <feature>/lib/app/presentation/views/widgets/
- Quy tắc:
  - Không đặt business logic trong widget con; chỉ nhận `props` cần thiết.
  - Nếu cần gọi action: expose callback dưới dạng Function()? hoặc ValueChanged<T>.
  - Tránh Get.find() trong widget con → truyền từ cha (Top-Down).
- Tạo file barrel:
  - <feature>/lib/app/presentation/views/widgets/widgets.dart
- Cập nhật PatientDetailView để dùng các widget con, không đổi hành vi.

Đầu ra:
1) Danh sách FILES sẽ tạo/sửa (kèm path).
2) CODE đầy đủ cho từng file (import chuẩn, không placeholder).
3) Lý do tách & mapping dòng (trước → sau).

3) Prompt gom widget dùng chung về features/utility
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

4) Prompt tách controller-logic nếu UI đang “ôm” quá nhiều
Bạn là GetX Practitioner.
Phát hiện và di dời BUSINESS LOGIC khỏi UI trong <feature>/lib/app/presentation/views/<SCREEN>.dart.

Yêu cầu:
- Nếu UI gọi trực tiếp repository/usecase, chuyển vào <feature>/lib/app/presentation/controllers/<SCREEN>_controller.dart
- UI chỉ gọi controller.method()/observables.
- Chuẩn hóa State:
  - loading: RxBool
  - error: Rxn<String>
  - data: Rx<T> hoặc RxList<T>
- Viết test cho controller (mock repository/usecase).

Đầu ra:
1) CODE controller (đã inject qua binding).
2) Sửa view (chỉ UI & bind rx).
3) Binding bổ sung/điều chỉnh (nếu có).
4) Widget test cơ bản cho view (pump + expect).

5) Prompt cập nhật routes & bindings sau refactor
Bạn là GetX Router Specialist.
Sau khi tách widget & controller cho feature <FEATURE_NAME>, hãy:

- Kiểm tra và cập nhật:
  - <feature>/lib/routes/<feature>_routes.dart
  - <feature>/lib/app/presentation/bindings/<SCREEN>_binding.dart
- Đảm bảo:
  - Các widget con KHÔNG đăng ký route riêng (chỉ screen đầy đủ).
  - Binding cung cấp đầy đủ controller/usecase cần thiết cho screen.

Đầu ra:
- CODE mới cho file routes & bindings.
- Kiểm tra import breakages (liệt kê).
- Gợi ý test: điều hướng đến screen và verify controller đã được put().

6) Prompt viết smoke test sau refactor (bảo toàn hành vi)
Bạn là QA/Flutter Test Engineer.
Viết widget test "smoke" cho <SCREEN> sau refactor:
- Pump screen bằng GetMaterialApp + routes.
- Verify:
  - Header hiển thị tên bệnh nhân.
  - VitalsSection render đủ metrics.
  - AppointmentsSection hiển thị n hẹn.
  - Nhấn nút "Xem toa thuốc" → điều hướng đúng.
- Dùng fake repository/usecase + controller injected qua binding test.

Đầu ra:
- CODE test file: <feature>/test/presentation/views/<screen>_smoke_test.dart
- Hướng dẫn chạy: `flutter test <path>`

7) Prompt “tách nhanh theo mẫu” cho một file cụ thể (one-shot)

(dùng khi bạn đã biết file cần tách ngay)

Bạn là Flutter Refactor Bot.
Hãy tách file sau thành widget con theo checklist chuẩn, kèm patch diff:

FILE: <feature>/lib/app/presentation/views/<SCREEN>.dart
CHECKLIST:
- [ ] Xác định vùng UI lặp/xuyên màn
- [ ] Trích xuất thành widget con trong views/widgets/
- [ ] Truyền dữ liệu qua props, không dùng Get.find() trong widget con
- [ ] Tạo barrel widgets.dart
- [ ] Cập nhật imports ở <SCREEN>.dart
- [ ] Không thay đổi hành vi/logic
- [ ] Chạy quick format & remove unused imports

Đầu ra:
- Danh sách file tạo/sửa
- CODE sau cùng của tất cả file
- Patch dạng unified diff cho <SCREEN>.dart

Gợi ý đặt tên & chuẩn hóa nhanh