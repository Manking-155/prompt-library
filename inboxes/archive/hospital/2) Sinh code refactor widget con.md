Bạn là Senior Flutter Engineer, dùng GetX. 
Nhiệm vụ: TÁCH NHỎ màn hình <PatientDetailView> (path: <feature>/lib/app/presentation/views/patient_detail_view.dart).

Yêu cầu:
- Chia thành các widget con theo đề xuất:
  1) PatientHeaderCard (shows avatar, name, age, ID, BHYT)
  2) VitalsSection (BP, HR, SpO2, Temp)
  3) AppointmentsSection (list)
  4) PrescriptionsSection (list)
- Mỗi widget con đặt trong: 
    - Nếu dùng chung cho các màn hình khác: <feature>/lib/app/presentation/views/widgets/
    - Nếu dùng chỉ màn hình thì đặt trong thư mục widgets
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
