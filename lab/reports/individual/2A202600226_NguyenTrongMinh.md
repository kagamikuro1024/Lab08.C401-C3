# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Nguyễn Trọng Minh  
**Vai trò trong nhóm:** Documentation Owner  
**Ngày nộp:** 13/04/2026  
**Độ dài:** 750 từ

---

## 1. Tôi đã làm gì trong lab này?

Là QA Lead, tôi đảm bảo pipeline hoạt động ổn định qua 4 sprints từ environment setup → final validation → report grounding.

**Sprint 1-2**: Setup environment (`chromadb`, `rank-bm25` via `requirements.txt`), test từng component riêng, chạy `python index.py` → 29 chunks, metadata coverage 100%. Verify mỗi chunk có source + effective_date + department + access_level.

**Sprint 3-4**: Monitor `compare_retrieval_strategies()` trên 10 test cases. Track metrics: baseline 0.875 → hybrid v1 ~2.7 (failed) → hybrid final 0.880. Ensure A/B fairness: top_k_search=10, top_k_select=3 constant. Final QC: `python eval.py` runs E2E, validate `logs/grading_run.json`, cross-check numbers vs report.

**Post-delivery (Report Grounding)**: Verify 11 group_report sections map to 60-point rubric. Artifact checklist (index.py, rag_answer.py, eval.py, logs/*, results/*, docs/architecture, docs/tuning-log, reports/group). Contribution matrix: map each member to function (Trung → `retrieve_dense()`, Vinh → `retrieve_sparse()`).

---

## 2. Điều tôi hiểu rõ hơn sau lab này

**A/B Testing Framework & Confounding Variables**: Ban đầu tôi chỉ biết "so sánh 2 cấu hình". Nhưng khi là QA, tôi học được tầm quan trọng của **giữ biến control không đổi**. Ví dụ cụ thể: nhóm chúng tôi cố ý KHÔNG đổi:
- Chunk size (400 tokens) / overlap (80) — vì nếu đổi, khó biết tác động là từ retrieval hay chunking
- Top_k_search (10) / top_k_select (3) — để context window cho LLM như nhau
- Prompt template — để generation quá trình bằng nhau

Chỉ đổi `retrieval_mode` (dense → hybrid + rerank) và sửa `eval context_len` (để công bằng trong scoring). Result: nếu metric thay đổi, ta tự tin đó là do retrieval tối ưu, không phải noise từ biến khác. Đây gọi là **causal isolation** — rất quan trọng trong ML experiments.

**QC as Evidence Grounding**: Trước đây tôi nghĩ QC = "tìm bug". Nhưng qua lab, QC là process để:
- ✅ **Input validation**: metadata coverage (100%), 29 chunks valid
- ✅ **Process monitoring**: logs from each sprint (0.875 → ~2.7 → 0.880), tracking failures
- ✅ **Output verification**: scorer numbers match (baseline Faithfulness 4.5 = tuning-log Sprint 2 row)
- ✅ **Report grounding**: claim "Hybrid tăng Answer Relevance +0.1" → proof là tuning-log table K4 + `compare()` function

Điều này tránh nguy cơ "report viết đẹp nhưng code không match" — một lỗi phổ biến khi deadline gần.

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn

**Ngạc nhiên**: Faithfulness GIẢM (-0.1/5), nhưng variant vẫn thắng (0.880 > 0.875). Hiểu rằng reranker trade-off: tránh hallucination, nhưng +0.1 Answer Relevance, +0.02 Completeness, Context Recall 1.0 giữ nguyên. Bài học: metrics là trade-off — tối ưu tổng score > từng metric riêng.

**Debugging Sprint 3**: Hybrid v1 failed (Faithfulness ~2.7). Root cause: `eval.py` cắt context 150 chars → LLM-judge thiếu bằng chứng. Fix: tăng 1200 chars. Sprint 4 metrics phục hồi ~4.4. Lesson: **instrumentation bias matters**.

**Report Grounding**: Trace 11 group_report claims → code/output. Example: "Hybrid retrieves SLA P1 better" ← `compare_retrieval_strategies()` output; "Metadata 100%" ← tuning-log Sprint 1 checklist; "Variant wins 0.880" ← tuning-log comparison table. No floating claims.

---

## 4. Phân tích một câu hỏi trong scorecard

**Câu hỏi**: `gq07: Tìm thông tin về mức phạt SLA P1 nếu SLA không được đáp ứng.`

**Đặc điểm**: Câu này là **anti-hallucination test** — tài liệu KHÔNG có mức phạt chi tiết, nên đáp án mong đợi là abstain/không biết.

**Baseline (Dense)**:
- Retrieve: Dense kéo `sla_p1_2026.txt` chính xác ✅
- Generate: "Tài liệu không cụ thể mức phạt"
- Scores: Faithfulness 4.5 (abstain đúng), Answer Relevance 4.5 (reply semantically match query), Context Recall 1.0, Completeness 0.7
- Status: Baseline đúng format (grounded abstain), nhưng response hơi generic

**Variant (Hybrid + Rerank)**:
- Retrieve: Hybrid + rerank kéo (1) `sla_p1_2026.txt` + (2) `it_helpdesk_faq.txt` để verify → có thêm context
- Generate: "Tài liệu nội bộ hiện tại không quy định mức phạt cụ thể cho SLA P1"
- Scores: Faithfulness 4.4 (rerank loại chunk phụ → score -0.1), Answer Relevance 4.6 (**+0.1** confidence), Context Recall 1.0, Completeness 0.72 (**+0.02** explanation rõ hơn)
- Status: Variant vẫn abstain (tránh hallucination) nhưng **more confident** + **clearer reasoning**

**Kết luận**: Câu này chứng tỏ variant tốt ở anti-hallucination + clarity (không chỉ tấnsay "không biết" mà explain TẠI SAO).

---

## 5. Bonus: Nếu có thêm thời gian

**Custom LLM-as-Judge** (2-3h): Implement domain-aware rubric scoring in `eval.py`. Define 4 domain prompts (Legal, HR, IT, SLA). Inject penalty context ("P1 SLA = 5% refund"). Extract confidence scores (0.0-1.0) from reasoning. A/B test vs ragas default → expect +2-3% delta. Unlock +2 bonus points.
