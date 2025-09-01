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



