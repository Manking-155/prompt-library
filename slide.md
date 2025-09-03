---
marp: true
title: Prompt Techniques for Maintain & Workflow
paginate: true
theme: default
---

# Structured Prompting cho Maintain & Workflow

- Prompt tệ → kết quả tệ (mất thời gian QA, bug)
- Structured prompting = tiết kiệm thời gian, giảm lỗi
- Ứng dụng cho mọi team: BrSE, Dev, Sales, OA
- Role chung: **AI = Trợ lý Maintain hệ thống app bệnh viện tại Nhật**

<!-- Speaker notes: Hook: maintain system = critical. Structured prompting giúp mọi team align. -->

---

# Framework 5 phần

1) Role & Objective  
2) Instructions  
3) Examples  
4) Context  
5) Final steps (output/test)

👉 Backbone để áp dụng mọi kỹ thuật

<!-- Speaker notes: Giới thiệu framework, sẽ dùng xuyên suốt. -->

---

# Role Prompting

- Giao **một vai trò duy nhất**: Trợ lý Maintain hệ thống bệnh viện  
- Kết quả đồng nhất, sát ngữ cảnh  

Ứng dụng trong Instructions:
- Dev/OA: xuất JSON/CSV schema để test & log  
- BrSE: luôn thêm bản song ngữ (JP/EN) khi có khách hàng  
- Sales: sinh thêm bản email thân thiện, ngắn gọn  

👉 Takeaway: Chỉ cần **1 Role chung**, còn tùy biến qua Instructions.

<!-- Speaker notes: Giảm phân mảnh → 1 Role chung, output nhiều phiên bản. -->

---

# Few-shot Prompting

- Đưa 1–3 ví dụ để AI học theo  
- Output đồng nhất, dễ test  

Ứng dụng:
- Dev: ví dụ log maintain có JSON schema  
- BrSE: ví dụ thông báo song ngữ  
- Sales: ví dụ email maintain gửi khách  
- OA: ví dụ template cũ để sinh bản mới  

👉 Takeaway: Ví dụ đại diện = kết quả chuẩn.

<!-- Speaker notes: Lưu 1–2 ví dụ chuẩn, AI sẽ tái tạo ổn định. -->

---

# Step-back Prompting

- Lùi một bước để phân tích nguyên tắc trước khi viết  
- Tạo output sâu sắc, không hời hợt  

Ứng dụng:
- Xác định nguyên tắc chung: rõ thời gian JST, hệ thống ảnh hưởng, tránh jargon  
- Nhắc checklist: thời gian, phạm vi, ảnh hưởng, liên hệ  
- Phân tích audience: khách hàng cần gì, team nội bộ cần gì  

👉 Takeaway: Nghĩ “nguyên tắc nền” trước khi viết → thông báo rõ & chuẩn.

<!-- Speaker notes: Giúp tránh output thiếu/thiếu trọng tâm. -->

---

# Chain of Thought (CoT)

- Buộc AI suy nghĩ theo từng bước  
- Logic, traceable  

Ứng dụng:
- B1: Xác định hệ thống ảnh hưởng  
- B2: Nêu thời gian & phạm vi  
- B3: Liệt kê rủi ro & mitigation  
- B4: Sinh bản thông báo JSON/CSV + text  

👉 Takeaway: Output có luồng suy luận → dễ kiểm soát.

<!-- Speaker notes: CoT giúp output testable, dễ debug. -->

---

# Tree of Thoughts (ToT)

- Khám phá nhiều phương án, chọn tối ưu  
- Đảm bảo sáng tạo nhưng sát mục tiêu  

Ứng dụng:
- Tạo 2–3 bản nháp thông báo maintain (ngắn gọn, chi tiết, formal/friendly)  
- So sánh → chọn bản phù hợp audience  
- Xuất cả JSON schema + bản email song ngữ  

👉 Takeaway: Nhiều lựa chọn → team dễ chọn phiên bản phù hợp.

<!-- Speaker notes: ToT hữu ích cho demo hoặc khi phải gửi nhiều kênh. -->

---

# Tối ưu Prompt với AI

Bạn là một chuyên gia về prompt engineering. Nhiệm vụ của bạn là giúp tôi tối ưu hóa các prompt mà tôi gửi cho bạn, dựa trên các kỹ thuật prompt tốt nhất. Hãy làm theo các bước sau để phân tích và cải thiện prompt mà tôi cung cấp: 1.Phân tích prompt: Xác định mục tiêu và nhiệm vụ của prompt. Xác định xem prompt có rõ ràng, cụ thể và dễ hiểu không. 2.Đánh giá prompt: Kiểm tra xem prompt có sử dụng các kỹ thuật prompt tốt nhất như Step-back Prompting, Tree-of- Thoughts, few-shot prompting, chain of thought, hoặc role prompting không. Xem xét liệu prompt có cung cấp đủ ngữ cảnh hoặc ví dụ để hướng dẫn AI không. 3.Đề xuất cải tiến: Đề xuất các thay đổi cụ thể để làm cho prompt hiệu quả hơn. Ví dụ, thêm ví dụ, làm rõ hướng dẫn, hoặc sử dụng một kỹ thuật prompt khác. Giải thích lý do tại sao các cải tiến này sẽ giúp cải thiện chất lượng của phản hồi từ AI. 4.Cung cấp phiên bản prompt đã tối ưu hóa: Viết lại prompt với các cải tiến đã đề xuất. Đảm bảo rằng phiên bản mới tuân theo các best practices và sẽ giúp AI tạo ra phản hồi chính xác và hữu ích hơn. Hãy áp dụng quy trình này cho prompt mà tôi sẽ gửi cho bạn tiếp theo.

👉 Takeaway: Do it.

<!-- Speaker notes: Đây là meta-prompt: để AI giúp nâng chất lượng prompt. -->

---

# Tối ưu Prompt với AI

- Dùng AI như **người phản biện prompt**  
- 4 bước cải thiện liên tục:  

1. Phân tích mục tiêu & độ rõ ràng  
2. Đánh giá: có dùng kỹ thuật (Role, Few-shot, CoT…) chưa  
3. Đề xuất cải tiến (ví dụ, thêm schema, thêm context)  
4. Viết lại prompt tối ưu  

👉 Takeaway: AI không chỉ trả lời, mà còn giúp bạn viết prompt tốt hơn.

<!-- Speaker notes: Đây là meta-skill: để AI giúp nâng chất lượng prompt. -->

---

# Before/After — Maintain Notice

<div class="two-col">

| Before (Unstructured) | After (Structured) |
|---|---|
| "Hệ thống ERP sẽ maintain tuần sau." | Role: Trợ lý Maintain hệ thống app bệnh viện tại Nhật |
| Mơ hồ: khi nào, ai ảnh hưởng | Instructions: Ngắn, JST, JSON schema + email song ngữ |
| Text tự do, khó test | Context: hệ thống, phạm vi, audience |
|  | Output: JSON schema (Dev/OA) + JP/EN email (BrSE/Sales) |

</div>

<!-- Speaker notes: Structured = testable, traceable, multi-view cho tất cả team. -->

---

# Demo
hãy tạo kế hoạch hoàn chỉnh cho việc thông báo với khách hành khi hệ thống maintain vào ngày 8/9

<!-- Speaker notes: Kết thúc bằng action cụ thể, dễ áp dụng ngay. -->


# Keyword tìm hiểu thêm
LOẠI TƯ DUY QUAN TRỌNG 
1. Tư Duy Phân Tích (Analytical Thinking) MECE + SWOT - Chia nhỏ vấn đề có hệ thống, đánh giá toàn diện
2. Tư Duy Phản Biện (Critical Thinking): RED Model + 5 Whys - Kiểm tra giả định, tìm nguyên nhân gốc rễ
3. Tư Duy Hệ Thống (Systems Thinking): Iceberg Model + SSM - Nhìn mối liên hệ, hiểu cấu trúc sâu
4. Tư Duy Sáng Tạo (Creative Thinking): SCAMPER + Design Thinking - Tạo giải pháp mới, tư duy khác biệt