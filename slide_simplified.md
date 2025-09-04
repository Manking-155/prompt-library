---
marp: true
title: Prompt Techniques for Maintain & Workflow
paginate: true
theme: default
---

# Tại sao cần Prompt rõ ràng?

- Prompt mơ hồ → AI trả lời mơ hồ → mất thời gian
- Prompt rõ ràng → AI trả lời đúng → tiết kiệm cho user

👉 Một thông điệp chung: *“Cách mình giao việc cho AI quyết định chất lượng kết quả.”*

---

# Framework 5 bước (Backbone)

1) Role & Objective (AI là ai, làm gì?)  
2) Instructions (yêu cầu chính)  
3) Examples (cho ví dụ mẫu)  
4) Context (bối cảnh liên quan)  
5) Final check (kiểm tra kết quả)

👉 Giống như giao việc cho đồng nghiệp mới.

---

# Role Prompting

- Giao **một vai trò rõ ràng** cho AI.  
- Kết quả đồng nhất, sát ngữ cảnh  

- Ví dụ: *“Bạn là trợ lý IT, hãy viết thông báo bảo trì dễ hiểu cho khách hàng.”*  
👉 Giúp AI tập trung, không lan man.

---

# Few-shot Prompting

- Cho AI **1–2 ví dụ ngắn gọn** để AI bắt chước. 
- Kết quả AI trả về sẽ đồng nhất, sát ngữ cảnh  

- Ví dụ: *“Đây là mẫu thông báo bảo trì lần trước…”* → AI sinh bản mới dựa theo.  
👉 Giúp kết quả đồng nhất, chuẩn hơn.

---

# Step-back Prompting

- Lùi một bước để nghĩ về **nguyên tắc cốt lõi** trước khi viết.  
- Tạo output sâu sắc, không hời hợt  

- Ví dụ: Khi viết thông báo bảo trì → cần ngày giờ, hệ thống ảnh hưởng, liên hệ hỗ trợ.  
👉 Tránh thiếu ý, tránh mơ hồ.

---

# Chain of Thought (CoT)

- Buộc AI suy nghĩ theo từng bước logic.  
- Ví dụ:
  - B1: Xác định hệ thống ảnh hưởng  
  - B2: Nêu thời gian  
  - B3: Liệt kê rủi ro  
  - B4: Soạn thông báo  
👉 Output có luồng suy luận, dễ kiểm tra.

---

# Tree of Thoughts (ToT)

- Yêu cầu AI đưa **nhiều phương án** rồi chọn cái tốt nhất.  
- Đảm bảo sáng tạo nhưng sát mục tiêu  

- Ví dụ: AI tạo 3 bản thông báo: ngắn gọn, chi tiết, thân thiện → team chọn.  
👉 Đảm bảo sáng tạo nhưng sát mục tiêu.

---

# Ví dụ Before/After

| Trước | Sau |
|-------|-----|
| “Hệ thống ERP sẽ maintain tuần sau.” | “Hệ thống ERP sẽ bảo trì ngày 8/9, 20:00–22:00 JST. Trong thời gian này khách hàng không truy cập được. Liên hệ support@…” |

---

# Tối ưu Prompt với AI


Bạn là một chuyên gia về prompt engineering.
Nhiệm vụ của bạn là giúp tôi tối ưu hóa các prompt mà tôi gửi cho bạn, dựa trên các kỹ thuật prompt tốt nhất.

Hãy làm theo các bước sau để phân tích và cải thiện prompt mà tôi cung cấp:

1. Phân tích prompt
   - Xác định mục tiêu và nhiệm vụ của prompt.
   - Xác định xem prompt có rõ ràng, cụ thể và dễ hiểu không.

2. Đánh giá prompt
   - Kiểm tra xem prompt có sử dụng các kỹ thuật prompt tốt nhất như Step-back Prompting, Tree-of-Thoughts, Few-shot Prompting, Chain of Thought, hoặc Role Prompting không.
   - Xem xét liệu prompt có cung cấp đủ ngữ cảnh hoặc ví dụ để hướng dẫn AI không.

3. Đề xuất cải tiến
   - Đề xuất các thay đổi cụ thể để làm cho prompt hiệu quả hơn (ví dụ: thêm ví dụ, làm rõ hướng dẫn, hoặc sử dụng một kỹ thuật prompt khác).
   - Giải thích lý do tại sao các cải tiến này sẽ giúp cải thiện chất lượng của phản hồi từ AI.

4. Cung cấp phiên bản prompt đã tối ưu hóa
   - Viết lại prompt với các cải tiến đã đề xuất.
   - Đảm bảo rằng phiên bản mới tuân theo các best practices và sẽ giúp AI tạo ra phản hồi chính xác và hữu ích hơn.

 Hãy áp dụng quy trình này cho prompt mà tôi sẽ gửi cho bạn tiếp theo.

---

# Takeaway chung

- Nhớ 3 điều: **Rõ ràng – Có ví dụ – Có bối cảnh.**  
- Tên kỹ thuật (Role Prompting, Few-shot, Step-back, CoT, ToT) là *công cụ* để đạt điều đó.  
👉 Mọi team đều có thể dùng ngay, không cần học thuật phức tạp.

