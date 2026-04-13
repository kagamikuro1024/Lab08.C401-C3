# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Lê Văn Quang Trung  
**Vai trò trong nhóm:** Tech Lead & Retrieval Owner  
**Ngày nộp:** 13/04/2026  
**Độ dài:** ~650 từ

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

Trong lab này, tôi đảm nhận vai trò **Tech Lead** điều phối nhịp độ làm việc của cả nhóm qua 4 Sprints và là **Retrieval Owner** chịu trách nhiệm chính về phần tìm kiếm dữ liệu. 
- Trong **Sprint 1**, tôi cùng nhóm quyết định chiến lược chunking theo Section (Section-based chunking) để đảm bảo các điều khoản pháp lý không bị cắt nửa chừng, đồng thời thiết lập hệ thống metadata bắt buộc bao gồm: `source`, `section`, và `effective_date`.
- Trong **Sprint 2**, tôi trực tiếp cùng với Đạt implement hàm `retrieve_dense()` sử dụng ChromaDB và kết nối các thành phần để chạy được pipeline baseline đầu tiên, đảm bảo output có citation đúng format `[1]`.
- Trong **Sprint 3**, tôi tập trung tối ưu hóa `retrieve_hybrid()` kết hợp Dense và Sparse (BM25) sử dụng thuật toán Reciprocal Rank Fusion (RRF). Tôi cũng đã tinh chỉnh bộ lọc Stopwords tiếng Việt mở rộng để loại bỏ nhiễu cho các mã lỗi kỹ thuật.
- Trong **Sprint 4**, tôi cùng Minh đảm nhận việc kiểm thử chất lượng cuối cùng (QC), tích hợp code từ các thành viên khác để đảm bảo file `eval.py` chạy ổn định và chính xác.

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

Sau lab này, tôi thực sự hiểu sâu hơn về cơ chế **Hybrid Retrieval** và tầm quan trọng của việc **Grounded Prompting**.
Trước đây, tôi nghĩ chỉ cần ném dữ liệu vào Vector Database là đủ, nhưng thực tế, Dense Retrieval (Semantic Search) đôi khi "quá thông minh" dẫn đến kết quả nhiễu khi gặp các từ khóa chuyên môn hoặc mã lỗi.
Việc kết hợp với BM25 (Sparse Retrieval) giúp hệ thống bám sát các từ khóa chính xác như "ERR-403" hay "P1". Đặc biệt, tôi hiểu rõ cơ chế **Reciprocal Rank Fusion (RRF)** giúp tổng hợp kết quả keyword và semantic một cách khoa học bằng cách ưu tiên những kết quả đứng đầu ở cả hai bảng xếp hạng. 
Điều này giúp tăng đáng kể Recall (khả năng tìm thấy) mà không làm giảm sự tập trung của LLM vào nội dung liên quan nhất.

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

Điều khiến tôi ngạc nhiên nhất là "độ nhiễu" mà BM25 tạo ra đối với tiếng Việt nếu không được xử lý tốt.
Ban đầu, các câu hỏi chứa từ phổ biến như "lỗi" hay "xử lý" khiến BM25 trả về hàng loạt chunk không liên quan vì tần suất xuất hiện của các từ này trong tài liệu kỹ thuật rất cao.
Tôi đã gặp khó khăn khi debug câu hỏi `q09` về mã lỗi `ERR-403-AUTH`. Hệ thống baseline đôi khi lấy nhầm thông tin về lỗi đăng nhập chung chung từ các file FAQ khác. 
Để giải quyết, tôi đã phải implement một bộ **Aggressive Stopwords** và thiết lập ngưỡng `min_score` cho kết quả Sparse. 
Ngoài ra, việc tinh chỉnh Tokenizer để không tách các dấu gạch ngang (`-`) là một bài học quan trọng để xử lý chính xác các model name hoặc code định danh trong tài liệu.

---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

**Câu hỏi:** "Nếu cần hoàn tiền khẩn cấp cho khách hàng VIP, quy trình có khác không?" (ID: q10)

**Phân tích:**
- **Kết quả Baseline:** Điểm Relevance (độ liên quan) chỉ đạt 0.0. 
Trong phiên bản baseline dense, model có xu hướng trả lời chung chung hoặc đôi khi bị ảnh hưởng bởi kiến thức bên ngoài (hallucination) khi cố gắng giải thích cho đối tượng "VIP" mặc dù tài liệu không hề nhắc tới. 
Điều này cho thấy Dense retrieval đôi khi mang về các chunk có nội dung tương đồng về mặt ngữ nghĩa hoàn tiền nhưng thiếu tính "khẳng định" để model phủ định thông tin.
- **Lỗi nằm ở:** Sự kết hợp giữa **Retrieval Noise** và **Generation Control**. 
Retrieval lấy đúng tài liệu refund nhưng có thể là các đoạn không chứa từ khóa phủ định rõ ràng.
- **Kết quả Variant:** Điểm Relevance đã cải thiện rõ rệt. 
Với Hybrid Retrieval, sự xuất hiện của từ khóa "hoàn tiền" đã kéo về các chunk chứa bảng quy trình tiêu chuẩn một cách chính xác hơn. 
Kết hợp với Grounded Prompt ép chặt model "chỉ trả lời từ context", model đã nhận diện tốt hơn rằng không có quy trình đặc biệt nào cho VIP được nhắc tới và trả lời đúng rằng: tất cả đều theo quy trình tiêu chuẩn. 
Đây là minh chứng rõ nhất cho việc Hybrid giúp tăng độ tin cậy của Context đầu vào cho LLM.

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

Tôi muốn thử nghiệm kỹ thuật **Query Expansion** (mở rộng câu hỏi) sử dụng LLM. Qua kết quả evaluation, tôi thấy một số câu hỏi sử dụng thuật ngữ cũ (như "Approval Matrix" ở câu q07) đôi khi vẫn khiến hệ thống hụt hơi nếu chỉ dựa vào embedding. 
Nếu có thể dùng LLM sinh ra 3 phrasings khác nhau trước khi retrieve, Recall chắc chắn sẽ đạt tuyệt đối. 
Ngoài ra, tôi muốn tối ưu hóa Cross-Encoder Reranker để giảm thiểu tối đa số lượng tokens đưa vào Prompt, giúp giảm latency và chi phí API.
Thêm vào đó tôi còn muốn thử nghiệm và đánh giá chiến lược của tôi dựa trên 1 bộ data lớn và phức tạp về mặt ngữ nghĩa hơn, từ đó có thể có con số đánh giá chính xác hơn về lợi ích của việc sử dụng chiến lược này so với baseline.
---
