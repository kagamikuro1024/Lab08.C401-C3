# Kiến Trúc RAG Pipeline — Phiên Bản Tối Ưu (v2)

Tài liệu này mô tả thiết kế hệ thống RAG cuối cùng sau khi đã tối ưu hóa thông qua 4 đợt Sprint.

---

## 1. Tổng Quan Hệ Thống
Hệ thống sử dụng kiến trúc tìm kiếm đa tầng (Multi-stage Retrieval) để đảm bảo độ chính xác tối đa cho cả ngữ nghĩa chính sách và các từ khóa đặc thù (mã lỗi, SLA, cấp độ truy cập).

- **Sinh văn bản**: OpenAI `gpt-4o-mini`
- **Đánh giá**: LLM-as-Judge (`gpt-4-turbo`)

---

## 2. Quy Trình Thu Thập Dữ Liệu (Indexing)
- **Tài liệu**: 5 bộ chính sách công ty (IT, HR, Sales, Support).
- **Chunking**: Section-based kết hợp Paragraph overlap.
  - `CHUNK_SIZE`: 400 tokens.
  - `CHUNK_OVERLAP`: 80 tokens.
- **Embedding**: OpenAI `text-embedding-3-small`.
- **Lưu trữ**: ChromaDB (Vector Store).

**Tài liệu được index:**

| File | Nguồn | Department | Số chunk |
|------|-------|-----------|---------|
| `policy_refund_v4.txt` | `policy/refund-v4.pdf` | CS | 6 |
| `sla_p1_2026.txt` | `support/sla-p1-2026.pdf` | IT | 5 |
| `access_control_sop.txt` | `it/access-control-sop.md` | IT Security | 7 |
| `it_helpdesk_faq.txt` | `support/helpdesk-faq.md` | IT | 6 |
| `hr_leave_policy.txt` | `hr/leave-policy-2026.pdf` | HR | 5 |

**Tổng số chunks: 29**

**Quyết định chunking:**

| Tham số | Giá trị | Lý do |
|---------|---------|-------|
| Chunk size | 400 tokens (ước lượng) | Giữ đủ ngữ cảnh điều khoản, tránh chunk quá dài |
| Overlap | 80 tokens (ước lượng) | Giảm rủi ro mất ngữ nghĩa ở biên chunk |
| Chunking strategy | Section-based + paragraph-aware | Bám heading tự nhiên của tài liệu |
| Metadata fields | source, section, effective_date, department, access | Phục vụ traceability, freshness, citation |

**Kết quả kiểm tra Sprint 1:**
- ✓ `python index.py` chạy thành công và tạo index ChromaDB.
- ✓ `list_chunks()` cho thấy chunk không bị cắt vỡ điều khoản chính.
- ✓ `inspect_metadata_coverage()` cho thấy **0 chunk thiếu `effective_date`**.

---

## 3. Kiến Trúc Tìm Kiếm (Retrieval & Reranking)
Hệ thống sử dụng quy trình 3 giai đoạn để lọc context chất lượng nhất:

### Giai đoạn 1: Tìm kiếm song song (Parallel Retrieval)
- **Dense Search**: Sử dụng Vector Similarity để tìm kiếm theo ý nghĩa ngữ nghĩa.
- **Sparse Search (BM25)**: Tìm kiếm theo từ khóa chính xác. 
  - *Cải tiến*: Áp dụng **Aggressive Stopword Filtering** để loại bỏ nhiễu từ các từ thông dụng tiếng Việt.

### Giai đoạn 2: Hợp nhất kết quả (Fusion)
- Sử dụng thuật toán **Reciprocal Rank Fusion (RRF)** để kết hợp danh sách kết quả từ Dense và Sparse.
- Trọng số tối ưu: `Dense (0.7)` / `Sparse (0.3)`.

### Giai đoạn 3: Tuyên lọc (Cross-Encoder Reranking) — *Mới*
- Sử dụng mô hình **Cross-Encoder** (`ms-marco-MiniLM-L-6-v2`) để chấm điểm lại mức độ liên quan giữa Câu hỏi và Top-10 Chunks.
- Chức năng: Loại bỏ hoàn toàn các "kết quả rác" mà BM25 có thể mang lại do trùng lặp từ khóa ngẫu nhiên.

---

## 4. Kết Quả Đánh Giá
Hệ thống Hybrid + Reranking đã vượt qua Baseline sau khi được tối ưu hóa.

| Chỉ số | Baseline (Dense) | Hybrid + Rerank | Kết quả |
| :--- | :--- | :--- | :--- |
| **Độ Trung Thực** | 4.5/5 | 4.4/5 | Duy trì ổn định |
| **Độ Liên Quan** | 4.5/5 | **4.6/5** | **📈 Cải thiện (+2%)** |
| **Context Recall** | 1.0/1 | 1.0/1 | TIE (Hoàn hảo) |
| **Độ Hoàn Chỉnh** | 0.70/1 | **0.72/1** | **📈 Cải thiện (+2%)** |
| **Tổng Trung Bình** | **0.875** | **0.880** | **🏆 VƯỢT TRỘI** |

---

## 5. Cấu Hình Khuyên Dùng cho Sản Phẩm
Dựa trên các thử nghiệm, đây là cấu hình mang lại chất lượng câu trả lời tốt nhất:

```python
# Cấu hình tìm kiếm
RETRIEVAL_MODE = "hybrid"
DENSE_WEIGHT = 0.7
SPARSE_WEIGHT = 0.3
USE_RERANK = True  # Sử dụng Cross-Encoder

# Cấu hình Sinh văn bản
LLM_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.0  # Đảm bảo tính trung thực (Grounding)
```

---

## 6. Sơ Đồ Kiến Trúc Luồng
```
User Query ──► [Tokenizer + Stopword Removal] 
                     │
                     ├─► Dense Search (Vector Store) ──┐
                     │                                 ▼
                     └─► Sparse Search (BM25 Index) ──► [RRF Fusion]
                                                       │
                                                       ▼
[Top-3 Selected] ◄── [Cross-Encoder Reranking] ◄── [Top-10 Candidates]
       │
       ▼
 [GPT-4o-Mini] ───► Final Answer (với trích dẫn nguồn [1][2])
```

**Cập Nhật Lần Cuối**: 13/04/2026  
**Trạng Thái**: Đã tối ưu hóa và kiểm chứng qua Sprint 4.

---

## 7. Phần Cấu Hình Chi Tiết Baseline vs Variant

### Baseline (Sprint 2)

| Tham số | Giá trị |
|---------|---------|
| Strategy | Dense (embedding similarity) |
| Top-k search | 10 |
| Top-k select | 3 |
| Rerank | Không |

### Variant cuối cùng (Sprint 4)

| Tham số | Giá trị | Thay đổi so với baseline |
|---------|---------|------------------------|
| Strategy | Hybrid + rerank | Dense + sparse tăng recall, rerank lọc nhiễu |
| Top-k search | 10 | Giữ nguyên để A/B công bằng |
| Top-k select | 3 | Giữ nguyên để context ổn định |
| Rerank | Có (Cross-Encoder) | Loại chunk rác từ BM25 |
| Query transform | Không | Không đổi |

### Lý do chọn variant

Corpus có cả ngôn ngữ tự nhiên và từ khóa đặc thù. Dense baseline tốt cho semantic search nhưng dễ hụt alias/keyword; hybrid khắc phục recall. Sau khi thêm rerank, pipeline giữ được chunk liên quan tốt hơn ở câu keyword/OOD.

---

## 8. Kết luận thiết kế

Thiết kế cuối cùng giữ triết lý đơn giản nhưng có bằng chứng. Dense baseline là nền, hybrid + rerank là bản nộp tối ưu vì cải thiện Answer Relevance/Completeness và giữ Context Recall tối đa.
