### **Bản thiết kế để xây dựng AI Agent Tương tác**

Đây là bản đúc kết các nguyên tắc và kỹ thuật mà chúng ta đã sử dụng để thiết kế "InsightAgent". Bạn có thể dùng nó như một cẩm nang để xây dựng các AI Agent phức tạp, có khả năng tương tác và thực thi nhiều tác vụ khác nhau.

### **Triết lý Cốt lõi: Từ "Công cụ" đến "Người Đồng hành"**

Mục tiêu là chuyển AI từ một cỗ máy hỏi-đáp thụ động thành một **Agent chủ động, có trạng thái (stateful) và được điều khiển bằng lệnh**. Agent này sẽ dẫn dắt người dùng qua một quy trình làm việc rõ ràng, thay vì chờ đợi người dùng phải tự nghĩ ra prompt hoàn hảo.

### **1\. Định danh và Nguyên tắc Hoạt động (Identity & Guiding Principles)**

Đây là "linh hồn" của Agent, quyết định cách nó tư duy và hành xử.

* **Định danh (Your Core Identity):**  
  * Luôn bắt đầu prompt bằng việc gán cho AI một vai trò cụ thể, có chuyên môn cao (VD: "Strategic Business Anthropologist").  
  * Nhấn mạnh các đặc tính cốt lõi (VD: "stateful", "command-driven").  
* **Nguyên tắc Hoạt động (Guiding Principles):**  
  * Đây là các quy tắc bất biến mà Agent phải tuân theo trong mọi phản hồi. Nó giúp đảm bảo chất lượng và sự nhất quán.  
  * **Ví dụ:** Chúng ta đã tạo ra 2 nguyên tắc cho InsightAgent:  
    1. **Pragmatism & Accessibility**: Ưu tiên các công cụ AI phổ thông.  
    2. **Cultural Nuance**: Luôn phân tích qua lăng kính văn hóa Việt Nam.

### **2\. Giao diện Dòng lệnh (The Command Interface)**

Đây là cách bạn và Agent "nói chuyện" với nhau một cách hiệu quả và có cấu trúc.

* **Thiết kế Command:**  
  * Sử dụng cú pháp rõ ràng, thường là ĐỘNG\_TỪ\_DANH\_TỪ viết hoa (VD: GENERATE\_PERSONAS, DETAIL\_USE\_CASE).  
  * Cho phép có tham số (parameter) để tăng tính linh hoạt (VD: SELECT\_PERSONA \<number\>).  
  * Luôn bao gồm các command "meta" để quản lý Agent: HELP, RESET, SHOW\_STATE.

### **3\. Quy trình Tương tác & Trạng thái (Interaction Protocol & State)**

Đây là phần "bộ não" điều khiển luồng hội thoại và trí nhớ của Agent.

* **Tự giới thiệu (Initialization):**  
  * Luôn yêu cầu Agent phải bắt đầu bằng một lời giới thiệu.  
  * Trong lời giới thiệu, nó phải **nêu rõ mục đích** và **liệt kê danh sách các lệnh (command)** mà nó có thể thực hiện. Điều này giúp người dùng biết ngay lập tức phải làm gì.  
* **Chủ động hỏi thông tin (Eliciting Information):**  
  * Thay vì để người dùng phải tự điền vào các placeholder như \[điền vào đây\], hãy thiết kế các command để Agent chủ động hỏi.  
  * **Cách làm:** Trong logic của command, hãy chỉ thị rõ: "Your first action is to ask me to provide the source material". Agent sẽ dừng lại và chờ bạn cung cấp thông tin.  
* **Gợi ý bước tiếp theo (Suggesting Next Steps):**  
  * Để dẫn dắt người dùng, hãy yêu cầu Agent **luôn kết thúc một tác vụ bằng một gợi ý** về lệnh tiếp theo nên dùng.  
  * **Ví dụ:** Sau khi GENERATE\_PERSONAS thành công, Agent phải gợi ý: "I have generated 3 personas. You can now use the LIST\_PERSONAS command to see them."  
* **Quản lý Trạng thái / Trí nhớ (State Management):**  
  * Đây là khái niệm quan trọng nhất. Hãy định nghĩa rõ các "biến nhớ" (state variables) mà Agent cần theo dõi (VD: current\_material, generated\_personas, selected\_persona).  
  * Mỗi command sẽ có nhiệm vụ đọc hoặc ghi vào các biến nhớ này. Đây là cách Agent "nhớ" được persona nào đã được chọn để thực hiện các lệnh tiếp theo.

### **4\. Logic Thực thi (Module Definitions)**

Phần này định nghĩa chi tiết **"nếu người dùng ra lệnh X, thì Agent phải làm Y"**.

* Với mỗi command, hãy viết ra một kịch bản thực thi rõ ràng, từng bước một.  
* **Ví dụ:**  
  * **Khi PROBE\_FOR\_INSIGHTS được gọi:**  
    1. Kiểm tra biến nhớ selected\_persona có tồn tại không.  
    2. Nếu có, hãy đặt 3-5 câu hỏi phỏng vấn.  
    3. Sau khi người dùng trả lời, hãy tổng hợp thông tin.  
    4. Cập nhật lại biến nhớ selected\_persona với thông tin mới.  
    5. Thông báo cho người dùng rằng persona đã được làm giàu và gợi ý lệnh GENERATE\_USE\_CASES.

Bằng cách tuân theo bản thiết kế này, bạn có thể tạo ra các prompt có khả năng biến các mô hình ngôn ngữ thành những trợ lý AI thông minh, có phương pháp và thực sự hữu ích trong công việc.