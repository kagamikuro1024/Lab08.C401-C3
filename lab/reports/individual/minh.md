# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Minh  
**Vai trò trong nhóm:** QA Lead  
**Ngày nộp:** 13/04/2026  
**Độ dài:** 650 từ

---

## 1. Tôi đã làm gì trong lab này?

Là QA Lead, trách nhiệm chính của tôi là đảm bảo pipeline hoạt động ổn định từ đầu đến cuối của 4 sprints, và giúp nhóm viết báo cáo cuối cùng.

**Sprint 1-2**: Setup environment — cài đặt ChromaDB, OpenAI API, rank-bm25, và tất cả dependencies trong `requirements.txt`. Tôi kiểm tra `python index.py` chạy không lỗi sau Sprint 1, xác nhận 29 chunks được tạo trong `chroma_db/` và metadata có đầy đủ `effective_date`. Sau Sprint 2, tôi test `rag_answer()` trên 5 mẫu query để đảm bảo có citation `[1]` và abstain khi câu OOD.

**Sprint 3-4**: Monitoring toàn quy trình — kiểm tra xem `compare_retrieval_strategies()` output ra sao, theo dõi metrics baseline vs variant từ 0.875 → 0.880. Cuối Sprint 4, tôi làm final QC: chạy `python eval.py`, kiểm tra `logs/grading_run.json` và `results/scorecard_*.md` tạo được, đối chiếu với group_report assumptions (30 điểm grading từ 98 raw).

**Post-deadline**: Giúp team viết báo cáo nhóm (group_report.md) bằng cách soát lại architectural decisions, kiểm tra artifact compliance table, và đảm bảo các claim trong report có bằng chứ từ code output. Làm proof-read cuối cùng trước khi commit.

---

## 2. Điều tôi hiểu rõ hơn sau lab này

**A/B Testing Framework trong ML**: Ban đầu tôi chỉ biết "so sánh 2 cấu hình", nhưng sau lab tôi hiểu rõ hơn tầm quan trọng của **giữ biến không đổi**. Nhóm chúng tôi cố ý KHÔNG đổi chunking, top_k, hay prompt khi chuyển từ baseline sang variant. Chỉ đổi `retrieval_mode` từ dense → hybrid + rerank. Điều này giúp ta tách rời tác động — nếu metric thay đổi, chúng ta biết chắc là do retrieval, không phải do chunk hay context window.

**QC Process trong Pipeline**: Trước đây tôi nghĩ QC chỉ là "tìm lỗi". Nhưng qua lab này, QC là:
- Kiểm tra input (metadata coverage 100%)
- Giám sát quy trình (logs từ mỗi sprint)
- Xác minh output (numbers match giữa code output vs report)
- Documentation (đảm bảo insights từ code được ghi trong architecture.md / tuning-log.md)

Đây giúp ta tránh nguy cơ report giả hay không khớp với thực tế.

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn

**Ngạc nhiên 1**: Faithfulness của variant GIẢM (-0.1/5) thay vì tăng. Ban đầu tôi lo là variant có vấn đề, nhưng sau đó hiểu rằng đây là **trade-off có chính đáng**: reranker loại bỏ một số chunk không chắc chắn để tránh hallucination, nhưng đổi lại Answer Relevance tăng +0.1 và Context Recall vẫn giữ 1.0. Tổng thể variant vẫn thắng (0.880 > 0.875).

**Khó khăn 1**: Monitoring Sprint 3 khi hybrid đầu tiên bị thất bại (Faithfulness rơi ~2.7). Tôi đoàn là có vấn đề cấu hình, nhưng hóa ra nguồn gốc là **eval context bị cắt quá ngắn** (150 ký tự), khiến LLM-judge không thấy đủ bằng chứng. Sau khi team tăng lên 1200 ký tự ở Sprint 4, kết quả bình thường. Bài học: đừng đổi quá nhiều biến cùng lúc — khó debug.

**Khó khăn 2**: Soát lại group_report mapping 60 điểm rubric vào code/docs output. Ban đầu các claim trong report không có mục đích rõ, nên tôi phải trace back từ từng section để xác minh "này là prove bởi file/function nào". Ví dụ: "Hybrid + Rerank cải thiện Answer Relevance +0.1" được prove bởi `tuning-log.md` table Sprint 4 + `compare_retrieval_strategies()` output.

---

## 4. Phân tích một câu hỏi trong scorecard

**Câu hỏi**: `gq07: Tìm thông tin về mức phạt SLA penalty P1 nếu SLA không được đáp ứng.`

**Phân tích Baseline (Dense)**:
- Baseline trả về: "Không tìm thấy mức phạt cụ thể trong tài liệu"
- Score: Faithfulness 4.5 (đúng format abstain), Answer Relevance 4.5 (trúng query), Context Recall 1.0 (retrieve đúng SLA source), Completeness 0.7 (abstain vì chưa có penalty number)
- Lỗi: Dense retrieve đúng `sla_p1_2026.txt` nhưng mức phạt không nằm trong đó. Pipeline đúng: không bịa number.

**Phân tích Variant (Hybrid + Rerank)**:
- Variant trả về: "Không tìm thấy mức phạt cụ thể trong tài liệu nội bộ hiện tại"
- Score: Faithfulness 4.4 (vẫn abstain, nhưng rerank loại 1-2 chunk phụ trợ → score giảm nhẹ), Answer Relevance 4.6 (more confident trả về abstain vs bịa), Context Recall 1.0 (hybrid lấy đủ SLA content để confirm không có penalty), Completeness 0.72 (explain rõ hơn tại sao thiếu)
- Lợi ích: Hybrid + Rerank giúp LLM **confident hơn** khi nói "không có dữ liệu", tránh cưỡng ép answer từ context yếu. Cái này là điểm mạnh của variant ở câu abstain — không bịa nhưng rõ ràng hơn.

**Kết luận**: Câu này prove rằng variant tốt hơn ở anti-hallucination + clarity, đặc biệt với câu OOD hoặc câu không có đủ dữ liệu.

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì?

Tôi sẽ **implement LLM-as-Judge scoring function** trong `eval.py`. Hiện tại `score_faithfulness()` vẫn trong TODO. Nếu có thêm 2-3 giờ, tôi sẽ:

1. Viết prompt để `gpt-4-turbo` chấm từng metric (Faithfulness / Answer Relevance / Context Recall / Completeness).
2. Chạy trên full 98 grading questions để test cách scoring có consistent không.
3. So sánh LLM-judge scores vs manual scores để validate.

Bằng chứng cần: eval.py output + logs/grading_run.json + comparison table trong report. Cái này sẽ unlock bonus +2 điểm trong rubric và giúp grading tự động hơn, thay vì thủ công.
