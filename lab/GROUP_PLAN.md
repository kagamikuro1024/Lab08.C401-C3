# 📋 KỂ HOẠCH LAB DAY 08 — RAG PIPELINE

**Nhóm:** Trung, Đạt, Nghĩa, Vinh, Minh  
**Tổng điểm:** 100 (60 nhóm + 40 cá nhân)  
**Deadline:** **18:00 (code + log + docs)** | Sau 18:00: được nộp report

---

## 📊 CẤU TRÚC ĐIỂM KHÔNG MISS

### Phần Nhóm — 60 điểm

| Phần | Chi tiết | Điểm |
|------|----------|------|
| **Sprint 1** | `python index.py` chạy OK + 3 metadata fields | **5** |
| **Sprint 2** | `rag_answer()` có citation + abstain khi không đủ dữ liệu | **5** |
| **Sprint 3** | Implement 1 variant (hybrid/rerank/query-transform) + scorecard | **5** |
| **Sprint 4** | `eval.py` chạy end-to-end + A/B comparison rõ ràng | **5** |
| **Docs** | `architecture.md` (5 điểm) + `tuning-log.md` (5 điểm) | **10** |
| **Grading** | 10 câu hỏi ẩn (Full/Partial/Zero/Penalty) | **30** |

### Phần Cá Nhân — 40 điểm (mỗi người)

- **Báo cáo cá nhân** (500-800 từ): với template có 6 mục cơ bản

---

## 👥 PHÂN VAI CHI TIẾT

### 1️⃣ **TRUNG — Tech Lead & Retrieval Owner**

**Trách nhiệm chính:**
- Quản lý nhịp độ 4 sprints (60' mỗi cái)
- Nối code end-to-end sau mỗi sprint
- Quyết định: chunk size, overlap strategy, metadata fields
- Implement `retrieve_dense()` (Sprint 2)
- QC: đảm bảo `python index.py && python rag_answer.py && python eval.py` chạy liên tục không lỗi

**Sprint 1 (60'):**
- [ ] Cùng nhóm review `index.py` TODO
- [ ] Quyết định: chunk_size, overlap (ưu tiên section-based, tránh cắt giữa điều khoản)
- [ ] Thêm metadata: source, section, effective_date (bắt buộc)
- [ ] Test: `list_chunks()` → đảm bảo chunk hợp lý
- [ ] **Deliverable:** ChromaDB index chạy được

**Sprint 2 (60'):**
- [ ] Implement `retrieve_dense()` (lấy query embedding → query ChromaDB)
- [ ] Implement `build_context_block()` và `call_llm()` (cơ bản)
- [ ] Test 3 câu: SLA P1, refund policy, access control
- [ ] **Deliverable:** `rag_answer("SLA ticket P1?")` có citation `[1]`

**Sprint 3 (60'):**
- [ ] Quyết định variant (hybrid nên chọn vì corpus có cả keyword + semantic)
- [ ] Implement `retrieve_sparse()` + `retrieve_hybrid()` hoặc `rerank()`
- [ ] Chạy `compare_retrieval_strategies()` để so sánh baseline vs variant
- [ ] **Deliverable:** Bảng so sánh có số liệu cụ thể

**Sprint 4 (60'):**
- [ ] Coi lại `eval.py` → chắc chắn có log grading_run.json
- [ ] Test end-to-end: chạy tất cả 3 file `.py` không crash
- [ ] Final QC: commit trước 18:00

---

### 2️⃣ **ĐẠT — Eval Owner & Documentation Lead**

**Trách nhiệm chính:**
- Viết test_questions.json (nếu chưa có)
- Implement `run_scorecard()` và `compare_ab()`
- Viết `architecture.md` và `tuning-log.md`
- Quản lý log/results folder

**Sprint 1–2:**
- [ ] Chuẩn bị test_questions.json với 10 câu đa dạng:
  - Câu về chính sách (policy_refund, hr_leave)
  - Câu về SLA/ticket (sla_p1, it_helpdesk)
  - Câu về quy trình (access_control)
  - Câu "lạ" (out-of-domain) → test abstain
- [ ] Ghi expected_answer và expected_sources cho mỗi câu

**Sprint 3–4:**
- [ ] Implement `score_faithfulness()` (thủ công hoặc LLM-as-Judge)
- [ ] Implement `run_scorecard()` → chạy 10 test questions qua pipeline
- [ ] Implement `compare_ab()` → tạo bảng so sánh baseline vs variant
- [ ] **Viết architecture.md:** 
  - Mô tả chunking (size, overlap, strategy)
  - Mô tả retrieval config (baseline vs variant)
  - Thêm sơ đồ pipeline (Mermaid hay ASCII art)
- [ ] **Viết tuning-log.md:**
  - Ghi lại config baseline + scorecard (4 metrics)
  - Ghi lại config variant + scorecard
  - Bảng so sánh: baseline vs variant, đầy đủ giải thích

**Deliverables:**
- [ ] `results/scorecard_baseline.md`
- [ ] `results/scorecard_variant.md`
- [ ] `logs/grading_run.json` (auto-generate từ eval.py)
- [ ] `docs/architecture.md` (5 điểm)
- [ ] `docs/tuning-log.md` (5 điểm)

---

### 3️⃣ **NGHĨA — LLM & Prompt Engineering**

**Trách nhiệm chính:**
- Implement `call_llm()` (OpenAI hoặc Gemini)
- Tối ưu `build_grounded_prompt()` → đảm bảo:
  - Answer chỉ dùng context (không bịa)
  - Citation đúng format `[1]`, `[2]`
  - Abstain khi không đủ dữ liệu
- Test prompt với các câu hỏi khác nhau

**Sprint 2 (60'):**
- [ ] Setup `.env`: OPENAI_API_KEY hoặc GOOGLE_API_KEY
- [ ] Implement `call_llm()`:
  ```python
  # Pseudocode
  client = OpenAI(api_key=...)
  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": prompt}],
      temperature=0,  # ổn định answer
      max_tokens=512
  )
  return response.choices[0].message.content
  ```
- [ ] Tối ưu prompt template trong `build_grounded_prompt()`:
  ```
  Answer ONLY from context. If insufficient, say "Không đủ dữ liệu".
  Cite sources: [1] source_name, [2], etc.
  ```
- [ ] Test 5 câu, đảm bảo output có citation

**Sprint 4:**
- [ ] Implement `score_faithfulness()` → có thể dùng LLM-as-Judge:
  ```python
  judge_prompt = f"""
  Given context: {chunks}
  Answer: {answer}
  Is answer grounded? Rate 1-5: ...
  """
  # Gửi cho LLM, parse JSON response
  ```

**Deliverable:**
- [ ] `rag_answer()` trả về dict với: answer, sources, config, chunks_used

---

### 4️⃣ **VINH — Retrieval & Tuning**

**Trách nhiệm chính:**
- Implement `retrieve_sparse()` (BM25 keyword search)
- Implement `retrieve_hybrid()` (dense + sparse fusion)
- Quyết định variant nào tốt hơn
- Debug retrieval issues

**Sprint 2 (60'):**
- [ ] Setup ChromaDB: đảm bảo có `.list_chunks()` hoạt động
- [ ] Kiểm tra chunk quality:
  - Chunk không bị cắt giữa câu/điều khoản?
  - Metadata (source, section, effective_date) đủ?

**Sprint 3 (60') — HYBRID VARIANT:**
- [ ] Implement `retrieve_sparse()` dùng BM25:
  ```python
  from rank_bm25 import BM25Okapi
  # Build BM25 index từ tất cả chunks
  # Query BM25 với keyword từ user's query
  ```
- [ ] Implement `retrieve_hybrid()` → Reciprocal Rank Fusion:
  ```python
  # dense_results = retrieve_dense(query)
  # sparse_results = retrieve_sparse(query)
  # Merge by RRF: score = 1/(rank_dense) + 1/(rank_sparse)
  ```
- [ ] Compare với baseline:
  - Câu đơn giản (SLA P1) → dense vs hybrid có khác?
  - Câu có keyword/alias (ERR-403) → hybrid tốt hơn không?
  - Câu "lạ" → cả dense và hybrid đều fail?

**Test Sprint 3:**
- [ ] `compare_retrieval_strategies(query)` → in ra top-3 của baseline vs variant
- [ ] Lấy 3–5 câu test, chạy so sánh, ghi nhận cải thiện

**Deliverable:**
- [ ] Bảng so sánh Baseline vs Variant (trong tuning-log.md)

---

### 5️⃣ **MINH — Quality Assurance & Report**

**Trách nhiệm chính:**
- Setup environment (requirements.txt, .env)
- QC: tất cả files có chạy được không?
- Viết báo cáo cá nhân + group report
- Checkout lỗi ý nhân trước deadline

**Sprint 1–2:**
- [ ] Setup: `pip install -r requirements.txt`
- [ ] Tạo `.env.example` → `.env`
- [ ] Test step by step:
  - [ ] `python index.py` → có ChromaDB không?
  - [ ] `python rag_answer.py` → có output giống mẫu không?
  - [ ] `python eval.py` → có log tạo không?

**Sprint 3–4:**
- [ ] QC code trước deadline 18:00:
  - [ ] Không có syntax error
  - [ ] Không có missing dependency
  - [ ] Log format đúng JSON
- [ ] Viết **group_report.md** (1–2 trang):
  - Tóm tắt pipeline
  - Variant được chọn + lý do
  - Kết quả so sánh baseline vs variant (điểm số)
  - Điểm yếu và cách cải tiến
- [ ] Giúp mỗi người viết **individual reports** (500–800 từ)
  - Mục 1: "Tôi đã làm gì?" (task cụ thể)
  - Mục 2: "Điều tôi hiểu rõ hơn?" (concept từ lab)
  - Mục 3: "Khó khăn gặp phải?" (bugs, error tree)
  - Mục 4: "Phân tích 1 câu trong scorecard" (why baseline fail, variant better?)
  - Mục 5: "Nếu có thêm thời gian?" (improvements)

**Deliverable:**
- [ ] `reports/group_report.md`
- [ ] `reports/individual/trung.md`, `reports/individual/dat.md`, etc.

---

## ⏰ TIMELINE CHI TIẾT

### **T-15 phút (Chuẩn bị)**

| Task | Owner | Checklist |
|------|-------|-----------|
| Clone repo, pull latest | Trung | Git setup OK |
| Install dependencies | Minh | `pip list` → có chromadb, rank-bm25 không? |
| Setup `.env` | Minh | OPENAI_API_KEY hoặc GOOGLE_API_KEY có value |
| Assign roles | Trung | Mỗi người hiểu task của mình |

---

### **SPRINT 1 (60') — Build Index**

| Thời điểm | Việc cần làm | Owner | Checklist ✅ |
|-----------|-------------|-------|-------------|
| 00'–10' | Review `index.py` TODO, quyết định chunk_size/overlap | Trung + Vinh | Viết comment giải thích tại sao chọn |
| 10'–30' | Implement `preprocess_document()`, `chunk_document()` | Trung | Không cắt giữa điều khoản |
| 30'–45' | Implement `get_embedding()`, `build_index()` | Trung | Có 5 docs, mỗi doc có 5+ chunks |
| 45'–55' | Test: `list_chunks()` → in ra 10 chunks mẫu | Vinh + Minh | Metadata có source, section, effective_date |
| 55'–60' | Commit code Sprint 1 | Trung | `git add && git commit` |

**Definition of Done:**
- [ ] Chạy `python index.py` không lỗi
- [ ] ChromaDB folder tạo được (~chroma_db/)
- [ ] Mỗi chunk có ≥3 metadata fields
- [ ] `list_chunks(n=10)` output rõ mạch, không bị cắt gọt

---

### **SPRINT 2 (60') — Baseline Retrieval + Answer**

| Thời điểm | Việc cần làm | Owner | Checklist ✅ |
|-----------|-------------|-------|-------------|
| 00'–15' | Setup LLM: `.env` có key, tạo dummy `call_llm()` | Nghĩa | `from openai import OpenAI` chạy OK |
| 15'–30' | Implement `retrieve_dense()` | Trung | ChromaDB query trả về top-10 chunks |
| 30'–40' | Implement `build_grounded_prompt()` + `call_llm()` | Nghĩa | Prompt có "Answer only from context", citation format |
| 40'–50' | Implement `rag_answer()` full function | Trung | Trả về dict: {answer, sources, config, chunks_used} |
| 50'–55' | Test 3+ queries (SLA P1, refund, lạ) | Vinh | Output có citation [1], abstain cho câu lạ |
| 55'–60' | Commit & push | Trung | **18:00 deadline note: Sprint 2 code phải commit trước 18:00** |

**Definition of Done:**
- [ ] `rag_answer("SLA xử lý ticket P1 là bao lâu?")` → có citation `[1]`
- [ ] `rag_answer("ERR-404-NOTFOUND")` → "Không đủ dữ liệu" (abstain)
- [ ] Output format: JSON-serializable, có sources field

---

### **SPRINT 3 (60') — Tuning & Variant**

| Thời điểm | Việc cần làm | Owner | Checklist ✅ |
|-----------|-------------|-------|-------------|
| 00'–10' | Decide variant: Hybrid (RECOMMEND) vì corpus có cả semantic + keyword | Trung + Vinh | Ghi vào tuning-log.md "Lý do chọn hybrid" |
| 10'–25' | Implement `retrieve_sparse()` (BM25) | Vinh | Chạy được, trả về chunks độc lập |
| 25'–40' | Implement `retrieve_hybrid()` (RRF fusion) | Vinh | Merge dense + sparse với weight |
| 40'–50' | Implement `compare_retrieval_strategies()` | Vinh + Trung | In bảng so sánh top-3 của baseline vs variant |
| 50'–55' | Chạy thứ thử 5 câu test, ghi lại kết quả | Vinh | Delta rõ ràng: baseline 3/5 đúng, variant 4/5 đúng |
| 55'–60' | Commit code Sprint 3 | Trung | trước 18:00 |

**Definition of Done:**
- [ ] Variant chạy được end-to-end
- [ ] Bảng so sánh baseline vs variant (ít nhất 2 metrics)
- [ ] Giải thích rõ tại sao variant tốt hơn (ví dụ: "Hybrid tìm thêm được alias 'P1' ngoài ngữ nghĩa")

---

### **SPRINT 4 (60') — Evaluation + Docs + Report**

| Thời điểm | Việc cần làm | Owner | Checklist ✅ |
|-----------|-------------|-------|-------------|
| 00'–10' | Implement `score_faithfulness()`, `run_scorecard()` | Đạt | Chấm 10 test questions |
| 10'–25' | Run baseline scorecard + variant scorecard | Đạt + Trung | Ghi số liệu ra `scorecard_baseline.md`, `scorecard_variant.md` |
| 25'–35' | Implement `compare_ab()`, tạo log grading_run.json | Đạt + Trung | JSON format đúng, có tất cả 10 câu |
| 35'–45' | Viết `docs/architecture.md` + `docs/tuning-log.md` | Đạt | 2 files hoàn chỉnh, có sơ đồ pipeline |
| 45'–55' | Final QC: chạy `python eval.py` end-to-end + check syntax | Minh + Trung | Không lỗi, log có tạo |
| 55'–60' | **FINAL COMMIT trước 18:00** | Trung | Tất cả code + logs + docs + scorecard |

**Definition of Done:**
- [ ] `python eval.py` chạy không crash
- [ ] `logs/grading_run.json` tạo được, format JSON
- [ ] `results/scorecard_baseline.md` + `results/scorecard_variant.md` có số liệu
- [ ] `docs/architecture.md` (5 điểm) + `docs/tuning-log.md` (5 điểm) hoàn chỉnh
- [ ] **Commit ALL before 18:00**

---

### **SAU 18:00 (Report Writing)**

| Task | Owner | Deadline |
|------|-------|----------|
| Viết `reports/group_report.md` | Đạt + Minh | Không giới hạn |
| Viết `reports/individual/[ten].md` (mỗi người) | Tất cả | Mỗi người viết của mình (500–800 từ) |
| Review + final polish | Trung | Trước khi nộp |

---

## 🚨 CHECKLIST KHÔNG MISS ĐIỂM

### ✅ Sprint 1 Checklist (5 điểm)

- [ ] `python index.py` chạy không lỗi
- [ ] ChromaDB index tạo được
- [ ] Mỗi chunk có ≥3 metadata fields: **source**, **section**, **effective_date**
- [ ] `list_chunks()` output rõ, không cắt gọt

### ✅ Sprint 2 Checklist (5 điểm)

- [ ] `rag_answer("SLA ticket P1?")` → **có citation [1]**
- [ ] `rag_answer("ERR-404-NOTFOUND")` → **abstain, không bịa**
- [ ] Output có `sources` field không rỗng
- [ ] `sources` trùng metadata của chunks retrieved

### ✅ Sprint 3 Checklist (5 điểm)

- [ ] Implement đúng **1 variant** (hybrid / rerank / query-transform)
- [ ] Bảng so sánh baseline vs variant có số liệu cụ thể (không "tốt hơn chung chung")
- [ ] Ghi rõ **tại sao** chọn biến này (reference error tree từ baseline)
- [ ] `results/scorecard_baseline.md` + `results/scorecard_variant.md` có digits

### ✅ Sprint 4 Checklist (5 điểm)

- [ ] `python eval.py` chạy end-to-end, không crash
- [ ] `logs/grading_run.json` có đúng 10 câu hỏi
- [ ] `logs/grading_run.json` format JSON đúng: [{"id", "question", "answer", "sources", ...}]
- [ ] A/B comparison rõ ràng: "Variant tốt hơn ở câu X vì Y"

### ✅ Docs Checklist (10 điểm)

**architecture.md (5 điểm):**
- [ ] Mô tả chunking: size, overlap, strategy, lý do (2 điểm)
- [ ] Mô tả retrieval: baseline (dense) vs variant (hybrid/rerank) config (2 điểm)
- [ ] Sơ đồ pipeline: Mermaid hoặc ASCII art (1 điểm)

**tuning-log.md (5 điểm):**
- [ ] Baseline config + scorecard (4 metrics) (1 điểm auto)
- [ ] Variant config + scorecard (1 điểm auto)
- [ ] Bảng so sánh baseline vs variant (2 metrics minimum) (1 điểm)
- [ ] Kết luận: "Variant tốt hơn ở metric X vì bằng chứng Y" (1 điểm)

### ✅ Grading Checklist (30 điểm)

- [ ] `logs/grading_run.json` có 10 câu, mỗi câu có `answer`, `sources`
- [ ] **Không hallucinate**: nếu context insufficient → "Không có dữ liệu"
- [ ] Citation đúng format: `[1] source_name`
- [ ] Expected sources từ `test_questions.json` match với retrieved sources

### ⏰ DEADLINE CHECKLIST (18:00)

**Phải commit trước 18:00:**
- [ ] `index.py` ✅
- [ ] `rag_answer.py` ✅
- [ ] `eval.py` ✅
- [ ] `logs/grading_run.json` ✅
- [ ] `results/scorecard_baseline.md` ✅
- [ ] `results/scorecard_variant.md` ✅
- [ ] `docs/architecture.md` ✅
- [ ] `docs/tuning-log.md` ✅

**Được phép commit sau 18:00:**
- [ ] `reports/group_report.md`
- [ ] `reports/individual/[ten].md` (×5)

---

## 🔧 TIPS & GOTCHAS

### 📌 Chunking Tips

1. **Section-based chunking tốt hơn token-based**
   - Chia theo `=== Section ... ===` heading đầu tiên
   - Tránh cắt giữa điều khoản
   - Ghi `section` vào metadata → dễ trace lại document

2. **Metadata fields bắt buộc:**
   ```python
   {
       "source": "policy_refund_v4.txt",      # File name
       "section": "Refund Timeline",          # Heading
       "effective_date": "2024-01-01",        # Khi áp dụng
       "department": "CS",                    # (optional nhưng giúp filter)
       "access": "internal"                   # (optional)
   }
   ```

3. **Chunk size recommend:** 300–500 tokens (~1200–2000 ký tự), overlap 50–100 tokens
   - Quá bé: ngữ cảnh mất, phải retrieve nhiều chunk
   - Quá lớn: LLM bị "lost in the middle"

---

### 📌 Retrieval Tips

1. **Dense vs Hybrid:**
   - **Dense**: tốt cho câu tự nhiên (SLA, refund policy)
   - **Hybrid**: tốt khi corpus có mã lỗi, alias, tên riêng (ERR-403, Level 3 access)
   - **Recommend:** Hybrid vì corpus day has both

2. **Top-k sweet spot:**
   - `top_k_search`: 10–15 (search rộng để không miss)
   - `top_k_select`: 3 (context limited → LLM chỉ focus 3 best chunks)

3. **Rerank alternative (nếu dense noise quá):**
   ```python
   from sentence_transformers import CrossEncoder
   reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
   scores = reranker.predict([[query, chunk] for chunk in candidates])
   # Sắp xếp lại theo score
   ```

---

### 📌 Grounded Answer Tips

1. **Prompt engineering critical:**
   ```
   Answer ONLY from the retrieved context.
   If the context is insufficient, say "Không đủ dữ liệu" instead of guessing.
   Cite sources using [1], [2], etc.
   Keep your answer short (1–3 sentences) and factual.
   ```

2. **Citation format:**
   - ✅ Good: `Theo tài liệu [1], SLA P1 là 15 phút response.`
   - ❌ Bad: `Theo tài liệu, SLA P1 là...` (no citation)
   - ❌ Bad: `SLA P1 là 15 phút và 20 phút đồng thời` (hallucination, không trong docs)

3. **Abstain khi không confident:**
   - LLM output: "Không đủ dữ liệu để trả lời câu này."
   - Score eval: Faithful (0 points) nhưng không penalty vì không bịa

---

### 📌 Evaluation Tips

1. **4 Metrics core:**
   - **Faithfulness (1–5):** Answer grounded in context? (không bịa)
   - **Answer Relevance (1–5):** Answer trả lời đúng câu hỏi?
   - **Context Recall (0–1):** Expected sources có được retrieve?
   - **Completeness (%):** Answer đầy đủ so với expected_answer?

2. **Scoring framework:**
   - **Full (100%):** Đáp ứng tất cả criteria
   - **Partial (50%):** ≥50% criteria, không hallucinate
   - **Zero (0%):** <50% criteria, không hallucinate
   - **Penalty (-50%):** Hallucinate hoặc bịa thông tin

3. **A/B rule quan trọng:**
   - Chỉ đổi **MỘT biến** giữa baseline vs variant
   - ví dụ: "Đổi từ dense → hybrid, giữ nguyên chunk size, top-k, prompt"
   - Nếu đổi 3 thứ cùng lúc → không biết cái nào có tác dụng

---

### 📌 Common Pitfalls

| Lỗi | Triệu chứng | Cách fix |
|-----|-------------|---------|
| **Chunking cắt gọt** | Chunk bị cắt giữa câu | Dùng section-based chunking, thêm overlap |
| **Missing metadata** | Citation không match | Thêm source, section vào metadata |
| **Hallucination** | Answer có info không trong docs | Prompt: "only_from_context", kiểm tra temperature=0 |
| **Lost in middle** | Context quá dài, LLM ignore | Top-k_select = 3, không quá 5 chunks |
| **Retrieval miss** | expected_sources không retrieve được | Test dense vs hybrid, thử rerank |
| **Dense poor recall** | Câu có keyword/alias miss | Switch to hybrid, thêm BM25 |
| **Grading_run.json lỗi** | Log tạo không được / format sai | Test format, check UTF-8 encoding |

---

### 📌 Debug Error Tree

Nếu pipeline sai, kiểm tra theo thứ tự:

```
1. Indexing lỗi?
   → python index.py → list_chunks() → Chunks có metadata không?
   → Metadata có source, section, effective_date không?

2. Retrieval lỗi?
   → Gọi retrieve_dense(query) → Top-3 chunks có chứa expected info không?
   → Thử retrieve_hybrid() → kết quả tốt hơn không?

3. Generation lỗi?
   → Kiểm tra call_llm() output (raw, trước post-processing)
   → Prompt có "Answer only from context" không?
   → Temperature = 0 không (để ổn định)?

4. Evaluation lỗi?
   → Kiểm tra test_questions.json format
   → run_scorecard() có tạo được không?
   → Metrics có meaningful không?
```

---

## 📝 FILE CHECKLIST — QUI ĐỊNH NỘP BÀI

### Bắt buộc (Deadline 18:00)

```
lab/
├── index.py                          ✅ Code chạy được
├── rag_answer.py                     ✅ Code chạy được  
├── eval.py                           ✅ Code chạy được
├── data/
│   ├── docs/                         ✅ 5 tài liệu
│   └── test_questions.json           ✅ 10 câu test
├── logs/
│   └── grading_run.json              ✅ Log 10 câu grading
├── results/
│   ├── scorecard_baseline.md         ✅ Có 4 metrics
│   └── scorecard_variant.md          ✅ Có 4 metrics
└── docs/
    ├── architecture.md               ✅ 5 điểm (chunking, retrieval, sơ đồ)
    └── tuning-log.md                 ✅ 5 điểm (baseline, variant, comparison)
```

### Được nộp sau 18:00

```
└── reports/
    ├── group_report.md               📝 Tóm tắt 1–2 trang
    └── individual/
        ├── trung.md                  📝 500–800 từ (Trung)
        ├── dat.md                    📝 500–800 từ (Đạt)
        ├── nghia.md                  📝 500–800 từ (Nghĩa)
        ├── vinh.md                   📝 500–800 từ (Vinh)
        └── minh.md                   📝 500–800 từ (Minh)
```

---

## 🎯 SUMMARY — KHI NHỜ "THỰC HIỆN LÚC NÀO?"

1. **Trước khi bắt đầu (T-30 phút):**
   - [ ] Mỗi người đọc qua file `README.md` + vai trò của mình
   - [ ] Setup environment: `pip install -r requirements.txt`, `.env` có key
   - [ ] Chia vai: Tech Lead, Retrieval Owner, LLM, Eval Owner, QA

2. **Sprint 1 → Sprint 4:** Làm theo timeline và checklist trên (4×60 phút = 4 giờ)

3. **Trước 18:00:** Final commit tất cả code + logs + docs

4. **Sau 18:00:** Viết reports cá nhân

5. **Nộp:** Push repo + verify các file trong checklist

---

## 💡 TIPS CUỐI CÙNG

✅ **Đảm bảo SUCCESS:**
- Chạy test end-to-end sau mỗi sprint: `python index.py && python rag_answer.py && python eval.py`
- Commit thường xuyên (mỗi sprint 1 lần minimum)
- Ghi log/note khi debug (giúp viết report sau)
- Không quá cầu kỳ: code đơn giản chạy được > code phức tạp nhưng bị lỗi
- A/B test tuần tự: chỉ thay 1 biến, observe delta

✅ **Điểm cao:**
- Metadata đầy đủ (source, section, effective_date) → dễ trace lại document
- Citation rõ ràng → faithfulness cao
- Abstain thay vì hallucinate → tránh penalty
- Giải thích lý do → reviewer hiểu quyết định của nhóm

---

**Chúc nhóm thành công! 🚀**
