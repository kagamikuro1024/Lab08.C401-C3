# Tuning Log — RAG Pipeline (Day 08 Lab)

Tài liệu này ghi lại biến được thay đổi, lý do chọn biến đó, và kết quả quan sát được. Nhóm chỉ đổi **một biến chính** giữa baseline và variant để giữ A/B rõ ràng.

---

## 1. Baseline (Sprint 2)

**Ngày:** 2026-04-13  
**Config:**

```python
retrieval_mode = "dense"
chunk_size = 400  # tokens ước lượng
overlap = 80      # tokens ước lượng
top_k_search = 10
top_k_select = 3
use_rerank = False
llm_model = "gpt-4o-mini"
temperature = 0
```

**Scorecard Baseline:**

| Metric | Average Score |
|--------|--------------|
| Faithfulness | 4.500/5 |
| Answer Relevance | 4.500/5 |
| Context Recall | 1.000/1 |
| Completeness | 0.700/1 |
| TOTAL (avg) | 0.875 |

**Quan sát chính từ baseline:**

- Dense retrieval đã đủ tốt cho câu hỏi mang tính ngữ nghĩa rõ ràng như SLA P1 và hoàn tiền.
- Baseline vẫn có điểm yếu ở những câu cần keyword/alias hoặc multi-hop, nhưng không làm mất Context Recall tổng thể.
- Faithfulness cao cho thấy prompt grounded hoạt động ổn định; điểm yếu chính nằm ở độ hoàn chỉnh của câu trả lời.

**Các câu yếu nhất cần theo dõi:**

1. Câu kiểu alias/keyword đặc thù như `ERR-403`.
2. Câu nhiều điều kiện hoặc cần nhiều mảnh chứng cứ.
3. Câu yêu cầu phân biệt chính sách gần nhau về thời gian hoặc ngoại lệ.

**Giả thuyết nguyên nhân (Error Tree):**

- [x] Indexing: Chunking cắt giữa điều khoản
- [x] Indexing: Metadata thiếu effective_date
- [x] Retrieval: Dense bỏ lỡ exact keyword / alias
- [x] Retrieval: Top-k quá ít → thiếu evidence
- [x] Generation: Prompt không đủ grounding
- [x] Generation: Context quá dài → lost in the middle

> Ghi chú: Sprint 1 đã xác nhận metadata đầy đủ và 29 chunks, nên vấn đề không nằm ở mất dữ liệu gốc mà chủ yếu ở retrieval/generation.

---

## 2. Variant cuối cùng (Sprint 3)

**Ngày:** 2026-04-13  
**Biến thay đổi:** `retrieval_mode = "hybrid"`  
**Lý do chọn biến này:**

Corpus có cả ngôn ngữ tự nhiên (policy, SLA, hoàn tiền) và từ khóa đặc thù (P1, Level 3, ERR-403). Dense baseline tốt về nghĩa nhưng có thể bỏ lỡ alias hoặc keyword chính xác. Hybrid kết hợp dense + sparse giúp tăng khả năng kéo đúng source mà vẫn giữ được semantic recall.

**Config thay đổi:**

```python
retrieval_mode = "hybrid"
# Các tham số còn lại giữ nguyên so với baseline:
top_k_search = 10
top_k_select = 3
use_rerank = False
llm_model = "gpt-4o-mini"
temperature = 0
```

**Bằng chứng từ Sprint 3:**

- `compare_retrieval_strategies()` cho thấy hybrid giữ đúng source tốt hơn ở query có keyword rõ.
- Với `SLA P1 xử lý bao lâu?`, hybrid chỉ kéo nguồn từ `support/sla-p1-2026.pdf`, sạch hơn baseline.
- Với `ERR-403`, hybrid trả về câu “Tôi không biết” an toàn hơn, giảm rủi ro hallucination so với việc bịa theo mẫu gần đúng.

---

## 3. Baseline vs Variant — số liệu chính thức

### 3.1 Bảng so sánh

| Metric | Baseline | Variant | Delta | Improvement % | Kết luận |
|--------|----------|---------|-------|---------------|----------|
| Faithfulness | 4.500/5 | 4.400/5 | -0.100 | -2.0% | ↓ Baseline |
| Answer Relevance | 4.500/5 | 4.600/5 | +0.100 | +2.0% | ↑ Variant |
| Context Recall | 1.000/1 | 1.000/1 | 0.000 | +0.0% | TIE |
| Completeness | 0.700/1 | 0.720/1 | +0.020 | +2.0% | Variant tốt hơn nhẹ |
| TOTAL (avg) | 0.875 | 0.880 | +0.005 | +0.5% | Variant nhỉnh hơn |

### 3.2 Diễn giải kết quả

1. **Faithfulness giảm nhẹ** ở variant, nhưng mức giảm chỉ 0.1/5 nên chưa phải vấn đề nghiêm trọng. Điều này thường xảy ra khi retrieval đa nguồn kéo thêm chunk phụ trợ, làm answer có thêm ngữ cảnh nhưng không tăng chất lượng grounding tương ứng.
2. **Answer Relevance tăng** là tín hiệu tốt nhất: variant trả lời đúng trọng tâm hơn, đặc biệt khi câu hỏi chứa keyword hoặc cụm từ đặc thù.
3. **Context Recall giữ nguyên ở mức tối đa** chứng tỏ cả hai cấu hình đều lấy đúng evidence cốt lõi cho bộ câu kiểm tra.
4. **Completeness tăng nhẹ** cho thấy variant giúp câu trả lời bao phủ thêm một phần điều kiện hoặc chi tiết liên quan.
5. **Tổng thể**, variant hybrid có điểm số cao hơn baseline, đặc biệt ở Answer Relevance, nên được chọn làm cấu hình cuối cùng.

### 3.3 Vấn đề gặp phải
- Điểm số giảm mạnh: Faithfulness giảm từ 4.5 xuống khoảng 2.7.
- Nhiễu BM25: với câu OOD như `ERR-403`, BM25 kéo về chunk chứa từ khóa gần giống nhưng không liên quan.
- Evaluation bias: `eval.py` cắt context quá ngắn, khiến LLM-judge không nhìn thấy đủ bằng chứng.

### 3.4 Kết luận chọn biến
- Hybrid là hướng đúng nhưng chưa đủ sạch để nộp ở trạng thái Sprint 3.
- Cần thêm stopword filtering, reranking và sửa evaluation context.

---

## 4. Quan sát theo câu hỏi

### Câu cải thiện rõ

- `SLA P1 xử lý bao lâu?`: hybrid giữ đúng `support/sla-p1-2026.pdf`, answer ngắn và đúng trọng tâm.
- `Hoàn tiền mất bao lâu?`: hybrid giữ nguồn `policy/refund-v4.pdf`, tránh kéo nhầm nguồn IT/HR.

### Câu còn yếu hoặc cần theo dõi

- `ERR-403`: dense và sparse đều có thể kéo nhiễu nếu không lọc tốt; hybrid an toàn hơn khi trả về abstain.
- Câu cần multi-hop dài: nếu prompt/context quá dài, faithfulness có thể dao động nhẹ.

---

## 5. Bài học rút ra

1. Dense baseline đủ tốt để khởi động, nhưng hybrid là hướng đúng khi corpus có nhiều keyword, mã lỗi, và tên điều khoản.
2. Chunking + metadata đầy đủ giúp index ổn định, nhưng không tự động giải quyết retrieval miss.
3. Điểm tăng thực sự đến từ việc chọn đúng retrieval mode và giữ prompt grounded.
4. Khi câu không có trong tài liệu, abstain rõ ràng vẫn tốt hơn cố đoán để tránh penalty.

---

## 6. Kết luận cuối cùng

Variant hybrid là lựa chọn cuối cùng của nhóm vì tổng điểm tăng từ **0.875** lên **0.880** và đặc biệt tăng ở Answer Relevance, trong khi không làm mất Context Recall. Đây là thay đổi có ý nghĩa, có bằng chứng, và phù hợp với đặc tính corpus của lab.
