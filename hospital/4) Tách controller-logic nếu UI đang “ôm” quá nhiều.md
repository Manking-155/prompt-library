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
