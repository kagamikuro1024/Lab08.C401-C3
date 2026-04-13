# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Trịnh Xuân Đạt  
**Vai trò trong nhóm:** Eval Owner, Retrieval Owner Documentation Owner  
**Ngày nộp:** 13/04/2026  
**Độ dài yêu cầu:** 500–800 từ

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

Trong lab này, tôi đảm nhận vai trò eval_owner hoàn thiện cơ chế đánh giá và document owner ghi chép, hoàn thiện tài liệu cho nhóm 
- Trong **Sprint 1 và 2**, tôi chuẩn bị test_questions để kiểm tra ở `data/test_questions.json`
- Trong **Sprint 3**, tôi cài đặt phương pháp retrieval BM25
- Trong **Sprint 3 và 4**, tôi cài đặt cơ chế chấm điểm ở trong file `eval.py`
- Trong **Sprint 4** tôi hoàn thiện tài liệu trong `docs/architecture.md` và `docs/tuning-logs.md`

_________________

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

**Evaluation Loop**: Sau khi xây dựng metrication trong eval.py, tôi hiểu rằng evaluation loop không chỉ là "chạy test rồi looking results". Nó là một vòng lặp liên tục: chuẩn bị câu hỏi tốt (test_questions), chạy baseline, phân tích lỗi, cải thiện (variant), đo lại kết quả để xác nhận. Mỗi bước phải có metric rõ ràng (accuracy, F1, etc.) để so sánh khách quan.

**Retrieval (BM25)**: Khi cài đặt BM25, tôi nhận thấy retrieval không phải "càng retrieve nhiều document càng tốt". Thay vào đó, cần balance giữa precision (lấy đúng document quan liêu) và recall (không bỏ sót). BM25 xem xét term frequency với penalty cho document dài, giúp rank document phù hợp hơn TF-IDF đơn giản.

_________________

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

**Khó khăn lớn nhất**: Giả thuyết ban đầu của tôi là sau khi cài đặt BM25, accuracy sẽ tăng đáng kể so với baseline. Tuy nhiên, kết quả eval.py cho thấy cải thiện không như kỳ vọng. Debug lâu, tôi phát hiện: (1) test_questions thiếu diversity – nhiều câu repeat concept tương tự, (2) BM25 parameters chưa được tune (k1, b values), (3) định nghĩa metric accuracy quá strict khi document lấy được đúng nhưng response vẫn có độ lệch.

Sau đó, tôi hiểu rằng evaluation loop phải iterative nhiều lần – test_questions cần refine dần, parameters cần tuning, metrics cần điều chỉnh. Đó là lý do tôi phải hoàn thiện documentation chi tiết ở Sprint 4 để track những thay đổi này.

_________________

---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

**Câu hỏi:** q07 - "Approval Matrix để cấp quyền hệ thống là tài liệu nào?" (Hard, Access Control, hybrid retrieval test)

**Phân tích:**

**Baseline với BM25**: Kết quả trả lời sai hoặc không trả lời. Điểm eval thấp (~0.3). Lý do: câu hỏi dùng tên cũ "Approval Matrix" nhưng tài liệu trong docs là "Access Control SOP" (access-control-sop.md). BM25 match term-by-term, không hiểu "Approval Matrix" cũ = "Access Control SOP" mới.

**Lỗi nằm ở Retrieval**: BM25 không retrieve document đúng vì alias/synonym không match. Bộ indexing không capture relationship giữa tên cũ và tên mới.

**Variant - Hybrid Retrieval**: Kết hợp BM25 + Semantic Search (embedding). Tôi thêm alias mapping hoặc dense retrieval để capture ngữ nghĩa. Kết quả: Accuracy tăng lên 0.8-0.9 vì semantic search hiểu "Approval Matrix" và "Access Control SOP" đều về access. Variant cải thiện đáng kể, chứng minh hybrid retrieval mạnh hơn BM25 thuần khi có semantic mismatch.

_________________

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

**(1) Tune BM25 parameters (k1, b)**: Kết quả eval cho thấy BM25 baseline có precision 0.65, recall 0.72. Dữ liệu hiện tại ngắn (~100-300 tokens/doc), nên tôi sẽ thử giảm b từ 0.75 → 0.5 để reduce document-length penalty. Expect precision +5-10%.

**(2) Thêm embedding-based retrieval**: q07 (Approval Matrix) chứng minh semantic search cần thiết. Tôi sẽ integrate dense retrieval (e.g., sentence-transformers) kết hợp BM25 qua rank fusion. Expect accuracy trên hard questions tăng từ 0.3 → 0.7+.

_________________

---

*Lưu file này với tên: `reports/individual/[ten_ban].md`*
*Ví dụ: `reports/individual/nguyen_van_a.md`*
