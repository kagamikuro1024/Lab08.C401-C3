# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Hoàng Đức Nghĩa 
**Vai trò trong nhóm:** LLM & Prompt Engineering Lead
**Ngày nộp:** 13/04/2026 
**Độ dài yêu cầu:** 500–800 từ

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

Vai trò trong nhóm của tôi là LLM & Prompt Engineering Lead, chủ yếu tập trung vào Sprint 2 — xây dựng dense baseline và grounded prompt cho RAG. Cụ thể, tôi đã:

1. **Tối ưu `build_grounded_prompt()`**: Thiết kế prompt có 5 quy tắc rõ ràng để LLM:
   - Trả lời CHỈ từ context (không dùng general knowledge)
   - Abstain khi không đủ dữ liệu ("Không đủ dữ liệu.")
   - Citation theo format [1], [2] để trace lại nguồn
   - Giữ câu trả lời ngắn gọn (1-3 câu) để tránh hallucination

2. **Implement `call_llm()`**: Gọi OpenAI API với cấu hình deterministic (`temperature=0`, `top_p=1.0`, `max_tokens=512`) để output ổn định cho evaluation.

3. **Kiểm thử**: Xây dựng pipeline test cho 5 câu hỏi mẫu để verify answer quality.

Công việc của tôi kết nối với phần tuning của Đạt và Trung : Tôi lấy chunks, tôi đóng gói chunks thành context block và sinh câu trả lời grounded rồi tôi gửi phần của mình cho Đạt và Trung để họ tune bằng hybrid retrieval.

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

Trước lab này, tôi nghĩ "prompt engineering" chỉ là viết instruction cho LLM sao cho mô tả rõ. Nhưng sau khi triển khai, tôi hiểu rằng **grounded generation là một kỹ thuật engineering cụ thể** với 4 yếu tố:

1. **Explicit constraint**: Phải ghi rõ "ONLY from context", "do NOT assume", "if insufficient say..."
2. **Citation format**: Format [1], [2] không phải "nice-to-have" mà là cơ chế trace evidence về tài liệu gốc
3. **Temperature tuning**: `temperature=0` là chìa khóa để output ổn định, không bịa rand
4. **Abstain mechanism**: "Không đủ dữ liệu" là lựa chọn tốt hơn hallucination, ngay cả khi có risk scoring low

Bài học quan trọng: grounded generation không phải "làm tốt hơn" mà là "tuân thủ constraint". Sự khác biệt giữa prompt good/bad ở đây là có/không có cơ chế để kiểm soát Output không bịa.

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

**Ngạc nhiên nhất**: Khi test `rag_answer()` lần đầu, mọi câu đều trả về "Không đủ dữ liệu" dù code `call_llm()` đã chạy đúng. Lỗi là `Collection [rag_lab] does not exist` từ `retrieve_dense()`. Ban đầu tôi nghĩ có vấn đề logic bên LLM side, nhưng thực ra cần chạy `index.py` trước để xây dựng ChromaDB.

**Khó khăn**: Cân bằng giữa "ép LLM abstain" và "LLM vẫn có thể giải thích tự do". Nếu prompt quá kỳ cục (ví dụ: toàn viết hoa, repeat 10 lần), LLM có thể không nghe. Giải pháp là dùng natural language nhưng rõ ràng, kết hợp với `temperature=0` để LLM không random thoát khỏi intent.

**Hypothesis ban đầu**: Tôi tưởng citation [1], [2] là optional. Nhưng trong evaluation, không có citation = mất điểm Faithfulness. Điều kiện này phải enforce từ prompt setup, không phải rely on LLM goodwill.

---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

**Câu hỏi:** Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?

**Expected answer** (từ test_questions.json): Khách hàng có thể yêu cầu hoàn tiền trong vòng 7 ngày làm việc kể từ thời điểm xác nhận đơn hàng.

**Expected sources**: policy/refund-v4.pdf

**Phân tích:**

### Baseline (Dense retrieval — Sprint 2)
- **Retrieval**: Lấy top-3 chunks từ `policy_refund_v4.txt` qua dense embedding, precision cao vì keyword "refund", "ngày" được semantic match tốt.
- **Generation**: `call_llm()` sinh: "Khách hàng có thể yêu cầu hoàn tiền trong vòng 7 ngày làm việc từ thời điểm xác nhận đơn hàng [1]."
- **Điểm Baseline**:
  - Faithfulness: 4.5/5 (có citation, không hallucinate)
  - Answer Relevance: 4.5/5 (phản ánh đúng nội dung expected answer)
  - Completeness: 0.7/1 (đủ thông tin nhưng có thể thêm điều kiện "làm việc")
  - **Tổng trung bình**: 0.875 ✓ Chính xác

**Root cause của Completeness không full**: Generation vốn đã đúng, nhưng prompt chưa tường minh yêu cầu liệt kê MỌI điều kiện (ví dụ: "ngày làm việc" vs "lịch calendar"). Đây là lỗi của prompt generation, không phải retrieval.

### Variant (Hybrid + Rerank — Sprint 4)
- **Retrieval**: Dense + BM25 (stopword filtered) → RRF merge → Cross-Encoder rerank
  - Dense tìm được chunk refund qua semantic
  - BM25 tìm được chunk qua keyword chính xác ("7 ngày", "hoàn tiền", "yêu cầu")
  - Rerank lọc top-3 chunk có score cao nhất (loại rác từ BM25)
- **Generation**: Cùng prompt, cùng `call_llm()`, output tương tự
- **Điểm Variant** (theo tuning-log.md Sprint 4):
  - Faithfulness: 4.4/5 (giảm 0.1 từ baseline, nhưng vẫn ổn)
  - Answer Relevance: **4.6/5** (tăng 0.1 ✓ cải thiện)
  - Completeness: **0.72/1** (tăng 0.02 ✓ cải thiện nhẹ)
  - **Tổng trung bình**: **0.880** (tăng 0.005 ✓ VARIANT THẮNG)

### Tại sao Variant cải thiện đối với câu này?
1. **RRF + Rerank tạo confidence cao hơn**: Mặc dù cả baseline và variant đều trả lời đúng, nhưng variant có 2 signal (dense + sparse) xác nhận chunk refund là relevant nhất.
2. **Completeness tăng nhẹ**: Reranker chứng minh top-3 chunk đều liên quan đến refund deadline, giúp prompt generation expand chi tiết hơn (ví dụ: thêm từ "làm việc").
3. **Trade-off**: Faithfulness giảm 0.1 vì trong tập 10 câu test, có câu OOD (gq07, gq09) mà hybrid nhỏ noise từ BM25 hơn baseline, dẫn đến model weak/abstain hơn, mất điểm faithfulness trong context chung.

### Kết luận
Câu "hoàn tiền 7 ngày" là test case "easy" mà hybrid + rerank không cải thiện đáng kể (chỉ +0.1 Answer Relevance). Variant chỉ thắng baseline vì giảm noise ở câu OOD, không phải làm tốt hơn câu này.

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

1. **Few-shot examples trong prompt**: Thêm example abstain case. Grading gq05 bị hallucination (-5 điểm) vì LLM tự tin bịa "5 ngày processing" không có docs. Few-shot sẽ dạy mô hình khi nào nên "I don't have this info".

2. **Confidence threshold enforcement**: Nếu rerank score trung bình < 0.65, auto fallback sang "Không đủ dữ liệu". Hiện tại prompt chỉ request abstain nhưng LLM vẫn synthesize; cần logic hard constraint ở generation layer.

**Lý do cụ:** Grading Score chỉ 9.2/30 (30.6%) cho thấy generation đang tự do quá. Few-shot + threshold sẽ giảm hallucination risk từ gq05-style cases.

---
