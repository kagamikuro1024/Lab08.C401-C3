# 🎯 HƯỚNG DẪN CHI TIẾT — TRUNG (Tech Lead)

**Vai trò:** Tech Lead & Retrieval Owner  
**Trách nhiệm:** Quản lý nhịp độ, nối code end-to-end, quyết định architecture retrieval  
**Điểm chịu trách nhiệm:** Sprint 1–4 deliverables (20 điểm)

---

## 📋 TÓM TẮT CÔNG VIỆC

| Sprint | Công việc chính | File chính | Điểm | Status |
|--------|-----------------|-----------|------|--------|
| **1** | Quyết định chunking + implement preprocess/chunk | `index.py` | 5 | ⬜ |
| **2** | Implement retrieve_dense() + nối code | `rag_answer.py` | 5 | ⬜ |
| **3** | Quyết định hybrid variant + compare_retrieval_strategies() | `rag_answer.py` | 5 | ⬜ |
| **4** | End-to-end testing + final QC + commit | Tất cả | 5 | ⬜ |

---

## 🚀 SPRINT 1 — INDEXING (60')

### Thời điểm: [Ngày D, từ 00:00–01:00]

### 📌 Công việc cụ thể

**File cần implement:** `lab/index.py`

#### Task 1.1: Quyết định chunking strategy (10')
```
Viết comment vào đầu index.py giải thích:

# CHUNKING DECISION:
# - chunk_size: 400 tokens (~1600 ký tự)
#   Lý do: Đủ context VS không quá lớn (tránh lost-in-middle)
# 
# - chunk_overlap: 80 tokens
#   Lý do: Đảm bảo không mất context giữa các chunk
#
# - Strategy: Section-based (split theo === Section === heading)
#   Lý do: Tài liệu có cấu trúc rõ, tránh cắt giữa điều khoản
#
# - Metadata fields: source, section, effective_date, department, access
#   Lý do: source → trace lại doc, effective_date → check freshness
```

#### Task 1.2: Implement `preprocess_document()` (15')
```python
# File: lab/index.py (Line ~50)
# Hàm này xử lý: parse metadata từ header → clean text

TODO: Xử lý dòng khoá "Source:", "Effective Date:" ở đầu file
      Sau đó bỏ những dòng này khỏi nội dung chính

Pseudocode:
  1. Split file thành lines
  2. Parse dòng "Key: Value" → metadata dict
  3. Loại bỏ header lines khỏi content
  4. Normalize whitespace (max 2 dòng trống liên tiếp)
  5. Return: { "text": cleaned, "metadata": {...} }

Expected output ví dụ:
{
  "text": "=== Policy Refund ===\n\nRefund timeline...",
  "metadata": {
    "source": "policy_refund_v4.txt",
    "effective_date": "2024-01-01",
    "department": "CS",
    "access": "internal"
  }
}
```

#### Task 1.3: Implement `chunk_document()` (20')
```python
# File: lab/index.py (Line ~100)
# Hàm này: chia document thành chunks nhỏ theo section

TODO: 
  1. Split theo === Section ... === heading
  2. Nếu section quá dài (> CHUNK_SIZE * 4), split thêm theo paragraph
  3. Thêm overlap: 80 tokens từ chunk trước vào chunk tiếp theo
  4. Mỗi chunk giữ đầy đủ metadata từ document gốc

Pseudocode:
  sections = re.split(r"(===.*?===)", text)
  # sections = ["", "=== Sec1 ===", "content1", "=== Sec2 ===", "content2", ...]
  
  for i in range(0, len(sections), 2):
    section_heading = sections[i]
    section_content = sections[i+1] if i+1 < len(sections) else ""
    
    # Split section_content theo paragraph nếu quá dài
    chunks_from_section = _split_by_size(section_content, ...)
    
    # Thêm overlap
    for j, chunk in enumerate(chunks_from_section):
      if j > 0: chunk = last_chunk_tail + chunk  # overlap
      chunks.append({
        "text": chunk,
        "metadata": {**base_metadata, "section": section_heading}
      })

Expected output:
[
  {
    "text": "=== Refund Timeline ===\nCustomers can request refund within...",
    "metadata": {
      "source": "policy_refund_v4.txt",
      "section": "Refund Timeline",
      "effective_date": "2024-01-01",
      ...
    }
  },
  {
    "text": "Customers can request refund within...\n=== Refund Process ===",
    "metadata": {..., "section": "Refund Timeline/Refund Process"}
  },
  ...
]
```

#### Task 1.4: Implement `get_embedding()` (10')
```python
# File: lab/index.py (Line ~220)
# Chọn 1 trong 2 option:

# OPTION A: OpenAI (nếu có API key)
def get_embedding(text: str) -> List[float]:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# OPTION B: Sentence Transformers (local, không cần API key)
def get_embedding(text: str) -> List[float]:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return model.encode(text).tolist()

# TRỊ CHỌN: OPTION B (tránh phụ thuộc API, nhanh hơn cho dev)
```

#### Task 1.5: Test Sprint 1 (5')
```bash
# Chạy command:
cd lab
python index.py

# Expected output:
# ChromaDB initialized at ./chroma_db
# Processing 5 documents...
# ✓ policy_refund_v4.txt (12 chunks)
# ✓ sla_p1_2026.txt (8 chunks)
# ✓ access_control_sop.txt (10 chunks)
# ✓ it_helpdesk_faq.txt (6 chunks)
# ✓ hr_leave_policy.txt (9 chunks)
# Total: 45 chunks indexed

# Inspect chunks:
python -c "from index import list_chunks; list_chunks(n=10)"
# Output mẫu:
# [1] policy_refund_v4.txt | Refund Timeline | score=N/A
#     Customers can request refund within 30 days...
# [2] policy_refund_v4.txt | Refund Process | score=N/A
#     Submit form to cs-team@company.com...
# ...
```

### ✅ Definition of Done — Sprint 1

- [ ] `python index.py` chạy không lỗi
- [ ] ChromaDB folder tạo được (~chroma_db/)
- [ ] Tất cả 5 documents indexed (kiểm tra bằng list_chunks())
- [ ] **Mỗi chunk có 3+ metadata fields:**
  - [ ] `source` (chứa filename)
  - [ ] `section` (chứa heading nếu có)
  - [ ] `effective_date` (lấy từ file header)
- [ ] `list_chunks(n=10)` output rõ mạch, không bị cắt gọt
- [ ] **Commit:** `git add index.py && git commit -m "Sprint 1: Build index"`

---

## 🔍 SPRINT 2 — BASELINE RETRIEVAL (60')

### Thời điểm: [Ngày D, từ 01:00–02:00]

### 📌 Công việc cụ thể

**File cần implement:** `lab/rag_answer.py`

#### Task 2.1: Implement `retrieve_dense()` (20')
```python
# File: lab/rag_answer.py (Line ~40)

def retrieve_dense(query: str, top_k: int = TOP_K_SEARCH) -> List[Dict[str, Any]]:
    """
    Dense retrieval: embed query → query ChromaDB → return top-k chunks
    """
    import chromadb
    from index import get_embedding, CHROMA_DB_DIR
    
    # 1. Connect to ChromaDB
    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    collection = client.get_collection("rag_lab")
    
    # 2. Embed query
    query_embedding = get_embedding(query)
    
    # 3. Query ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    # 4. Format results
    # Note: ChromaDB distance = 1 - cosine_similarity
    chunks = []
    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "metadata": metadata,
            "score": 1 - distance  # Convert to similarity
        })
    
    return chunks

# Expected output:
# [
#   {
#     "text": "P1 tickets require 15-minute response time...",
#     "metadata": {"source": "sla_p1_2026.txt", "section": "P1 SLA", ...},
#     "score": 0.92
#   },
#   ...
# ]
```

#### Task 2.2: Nối code — Test `retrieve_dense()` (10')
```python
# Thêm vào main của rag_answer.py:

if __name__ == "__main__":
    # Test retrieve_dense
    query = "SLA xử lý ticket P1 là bao lâu?"
    chunks = retrieve_dense(query, top_k=5)
    
    print(f"Query: {query}")
    print(f"Retrieved {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n[{i}] {chunk['metadata'].get('source')} | Score: {chunk['score']:.3f}")
        print(f"    {chunk['text'][:200]}...")
```

#### Task 2.3: Implement `call_llm()` + `build_grounded_prompt()` (15')

**LƯU Ý:** Phần này do **NGHĨA** implement, nhưng Trung cần biết output format.

```python
# File: lab/rag_answer.py (Line ~270)

def build_grounded_prompt(query: str, context_block: str) -> str:
    """
    Xây dựng prompt ép LLM chỉ trả lời từ context
    """
    return f"""Answer ONLY from the retrieved context below.
If the context is insufficient, say "Không đủ dữ liệu" instead of guessing.
Cite the source field when possible, using format [1], [2], etc.
Keep output short, clear, and factual.

Question: {query}

Context:
{context_block}

Answer:"""

def call_llm(prompt: str) -> str:
    """
    Gọi LLM (OpenAI hoặc Gemini)
    Return: text answer từ LLM
    """
    # Implementation bởi NGHĨA
    pass

# Expected output:
# "Theo tài liệu [1], P1 tickets có SLA 15 phút response time và 4 giờ resolution time."
```

#### Task 2.4: Implement `rag_answer()` full function (15')
```python
# File: lab/rag_answer.py (Line ~330)

def rag_answer(
    query: str,
    retrieval_mode: str = "dense",
    top_k_search: int = TOP_K_SEARCH,
    top_k_select: int = TOP_K_SELECT,
    use_rerank: bool = False,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Main RAG function: retrieve → build context → call LLM → return grounded answer
    """
    
    # 1. Retrieve
    if retrieval_mode == "dense":
        chunks = retrieve_dense(query, top_k=top_k_search)
    elif retrieval_mode == "hybrid":
        chunks = retrieve_hybrid(query, top_k=top_k_search)
    else:
        raise ValueError(f"Unknown retrieval_mode: {retrieval_mode}")
    
    # 2. Rerank (if enabled)
    if use_rerank:
        chunks = rerank(query, chunks, top_k=top_k_select)
    else:
        chunks = chunks[:top_k_select]
    
    # 3. Build context block
    context_block = build_context_block(chunks)
    
    # 4. Build prompt
    prompt = build_grounded_prompt(query, context_block)
    
    # 5. Call LLM
    answer = call_llm(prompt)
    
    # 6. Extract sources
    sources = list(set(chunk["metadata"]["source"] for chunk in chunks if chunk["metadata"].get("source")))
    
    # 7. Return result
    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": chunks,
        "config": {
            "retrieval_mode": retrieval_mode,
            "top_k_search": top_k_search,
            "top_k_select": top_k_select,
            "use_rerank": use_rerank,
        }
    }

# Expected output:
# {
#   "answer": "Theo tài liệu [1], P1 tickets...",
#   "sources": ["sla_p1_2026.txt"],
#   "chunks_used": [...],
#   "config": {...}
# }
```

#### Task 2.5: Test Sprint 2 (5')
```bash
# Test 3 câu:

python -c "
from rag_answer import rag_answer

# Test 1: Có trong docs
result = rag_answer('SLA xử lý ticket P1?')
print('Test 1 - SLA P1:')
print(f'  Answer: {result[\"answer\"][:100]}...')
print(f'  Sources: {result[\"sources\"]}')
print()

# Test 2: Có trong docs
result = rag_answer('Khách hàng có thể yêu cầu hoàn tiền trong bao lâu?')
print('Test 2 - Refund:')
print(f'  Answer: {result[\"answer\"][:100]}...')
print(f'  Sources: {result[\"sources\"]}')
print()

# Test 3: KHÔNG trong docs → test abstain
result = rag_answer('ERR-404-NOTFOUND là gì?')
print('Test 3 - Out of domain:')
print(f'  Answer: {result[\"answer\"][:100]}...')
print(f'  Sources: {result[\"sources\"]}')
"
```

### Expected Output

```
Test 1 - SLA P1:
  Answer: Theo tài liệu [1], P1 tickets yêu cầu phản hồi trong 15 phút và xử lý trong 4 giờ [1]...
  Sources: ['sla_p1_2026.txt']

Test 2 - Refund:
  Answer: Theo tài liệu [1], khách hàng có thể yêu cầu hoàn tiền trong 30 ngày...
  Sources: ['policy_refund_v4.txt']

Test 3 - Out of domain:
  Answer: Không đủ dữ liệu để trả lời câu hỏi này.
  Sources: []
```

### ✅ Definition of Done — Sprint 2

- [ ] `retrieve_dense()` chạy được, trả về top-k chunks
- [ ] `rag_answer("SLA ticket P1?")` trả về answer có **citation [1]** ✅
- [ ] `rag_answer("ERR-404-NOTFOUND")` trả về **abstain** ✅
- [ ] Output dict có `answer`, `sources`, `chunks_used`, `config` fields
- [ ] **Commit:** `git add rag_answer.py && git commit -m "Sprint 2: Baseline retrieval + answer"`

---

## 🔄 SPRINT 3 — HYBRID VARIANT (60')

### Thời điểm: [Ngày D, từ 02:00–03:00]

### 📌 Công việc cụ thể

**File cần modify:** `lab/rag_answer.py`

#### Task 3.1: Quyết định variant (5')

```
Viết comment vào rag_answer.py:

# VARIANT DECISION:
# Chọn HYBRID (dense + sparse)
#
# Lý do:
# 1. Corpus có câu tự nhiên về policy (SLA, refund) + tên đặc thù (P1, Level 3)
# 2. Dense alone miss alias queries (e.g., "P1" aka "Priority 1")
# 3. BM25 keyword search bắt được keyword-heavy queries
# 4. Hybrid = best of both: semantic + keyword coverage
#
# Metrics cải thiện dự kiến:
# - Context Recall: +20% (find more relevant docs)
# - Answer Relevance: +10% (better coverage)
```

#### Task 3.2: Implement `retrieve_sparse()` (15')

**LƯU Ý:** Phần này chủ yếu do **VINH** xử lý, nhưng Trung cần nối code.

```python
# File: lab/rag_answer.py (Line ~90)

def retrieve_sparse(query: str, top_k: int = TOP_K_SEARCH) -> List[Dict[str, Any]]:
    """
    Sparse retrieval: BM25 keyword search
    (Sẽ được implement bởi VINH)
    """
    pass
```

#### Task 3.3: Implement `retrieve_hybrid()` (20')

**LƯU Ý:** Phần này do **VINH** implement logic, Trung nối code và test.

```python
# File: lab/rag_answer.py (Line ~128)

def retrieve_hybrid(
    query: str,
    top_k: int = TOP_K_SEARCH,
    dense_weight: float = 0.6,
    sparse_weight: float = 0.4,
) -> List[Dict[str, Any]]:
    """
    Hybrid retrieval: Reciprocal Rank Fusion (RRF)
    
    Score = dense_weight * (1 / (rank_dense + 1)) + sparse_weight * (1 / (rank_sparse + 1))
    """
    
    # 1. Retrieve từ cả 2 sources
    dense_results = retrieve_dense(query, top_k=top_k)
    sparse_results = retrieve_sparse(query, top_k=top_k)
    
    # 2. Tạo rank mapping
    dense_rank = {chunk["metadata"]["source"]: i for i, chunk in enumerate(dense_results)}
    sparse_rank = {chunk["metadata"]["source"]: i for i, chunk in enumerate(sparse_results)}
    
    # 3. Calculate RRF scores
    all_sources = set(dense_rank.keys()) | set(sparse_rank.keys())
    rrf_scores = {}
    for source in all_sources:
        d_rank = dense_rank.get(source, top_k)
        s_rank = sparse_rank.get(source, top_k)
        rrf_scores[source] = (
            dense_weight / (d_rank + 1) +
            sparse_weight / (s_rank + 1)
        )
    
    # 4. Keep best chunks
    # (Merge dense_results + sparse_results, sort by RRF score)
    merged = {}
    for chunk in dense_results + sparse_results:
        source = chunk["metadata"]["source"]
        if source not in merged:
            merged[source] = chunk.copy()
            merged[source]["rrf_score"] = rrf_scores[source]
    
    # Sort by RRF score
    sorted_chunks = sorted(merged.values(), key=lambda x: x["rrf_score"], reverse=True)[:top_k]
    
    return sorted_chunks
```

#### Task 3.4: Implement `compare_retrieval_strategies()` (15')

```python
# File: lab/rag_answer.py (Line ~427)

def compare_retrieval_strategies(query: str) -> None:
    """
    So sánh baseline (dense) vs variant (hybrid) trên cùng 1 query
    """
    print(f"\n{'='*80}")
    print(f"COMPARE: Dense vs Hybrid")
    print(f"Query: {query}")
    print(f"{'='*80}\n")
    
    # Retrieve từ cả 2 mode
    dense_chunks = retrieve_dense(query, top_k=5)
    hybrid_chunks = retrieve_hybrid(query, top_k=5)
    
    # Print kết quả
    print("BASELINE (Dense):")
    for i, chunk in enumerate(dense_chunks, 1):
        print(f"  [{i}] {chunk['metadata'].get('source')} | Score: {chunk['score']:.3f}")
        print(f"      {chunk['text'][:80]}...")
    
    print("\nVARIANT (Hybrid):")
    for i, chunk in enumerate(hybrid_chunks, 1):
        print(f"  [{i}] {chunk['metadata'].get('source')} | RRF Score: {chunk['rrf_score']:.3f}")
        print(f"      {chunk['text'][:80]}...")
    
    print("\nANALYSIS:")
    dense_sources = {c['metadata']['source'] for c in dense_chunks}
    hybrid_sources = {c['metadata']['source'] for c in hybrid_chunks}
    print(f"  Dense sources: {dense_sources}")
    print(f"  Hybrid sources: {hybrid_sources}")
    print(f"  Additional in Hybrid: {hybrid_sources - dense_sources}")
    print(f"  Lost in Hybrid: {dense_sources - hybrid_sources}")

# Usage:
# compare_retrieval_strategies("SLA xử lý ticket P1?")
# compare_retrieval_strategies("ERR-403-ACCESS-DENIED")
```

#### Task 3.5: Test Sprint 3 (5')
```bash
# Chạy compare trên 3–5 câu test khác nhau

python -c "
from rag_answer import compare_retrieval_strategies, rag_answer

# Test 1: Simple semantic
compare_retrieval_strategies('SLA xử lý ticket P1 là bao lâu?')

# Test 2: Keyword-heavy / alias
compare_retrieval_strategies('Level 3 access cần ai approve?')

# Test 3: Out of domain
compare_retrieval_strategies('ERR-404-NOTFOUND')

print('\n' + '='*80)
print('FULL RAG_ANSWER TEST:')
print('='*80)

# Test full pipeline với hybrid
result = rag_answer('Khách hàng yêu cầu hoàn tiền trong bao lâu?', retrieval_mode='hybrid')
print(f'Answer: {result[\"answer\"]}')
print(f'Sources: {result[\"sources\"]}')
"
```

### ✅ Definition of Done — Sprint 3

- [ ] `retrieve_sparse()` return chunks từ BM25
- [ ] `retrieve_hybrid()` chạy được, RRF score meaningful
- [ ] `compare_retrieval_strategies()` in bảng so sánh rõ ràng
- [ ] Bảng so sánh cho 3+ queries, delta rõ ràng (ví dụ: hybrid find +1, -0 for this query)
- [ ] **Commit:** `git add rag_answer.py && git commit -m "Sprint 3: Add hybrid retrieval + comparison"`

---

## 📊 SPRINT 4 — EVALUATION + END-TO-END (60')

### Thời điểm: [Ngày D, từ 03:00–04:00]

### 📌 Công việc cụ thể

**File cần test/coordinate:** `lab/eval.py`

#### Task 4.1: Coordinate với ĐẠT — setup eval.py (10')

Đạt sẽ implement `run_scorecard()`, nhưng Trung cần đảm bảo nó output đúng format.

```python
# File: lab/eval.py (Line ~216)

# Expected function signature:
def run_scorecard(
    config: Dict[str, Any],
    test_questions: Optional[List[Dict]] = None,
    verbose: bool = True,
) -> List[Dict[str, Any]]:
    """
    Run pipeline trên test_questions với config cho sẵn.
    
    Return: List[{
        "question": str,
        "answer": str,
        "expected_sources": [str],
        "retrieved_sources": [str],
        "faithfulness": float (1–5),
        "answer_relevance": float (1–5),
        "context_recall": float (0–1),
        "completeness": float (0–1),
    }]
    """
```

#### Task 4.2: Test End-to-End (15')

```bash
# Run tất cả 3 scripts liên tiếp

echo "=== SPRINT 1: Building index ==="
python index.py

echo -e "\n=== SPRINT 2: Testing retrieval ==="
python -c "from rag_answer import rag_answer; result = rag_answer('SLA P1?'); print(result['answer'])"

echo -e "\n=== SPRINT 3: Testing hybrid ==="
python -c "from rag_answer import rag_answer; result = rag_answer('SLA P1?', retrieval_mode='hybrid'); print(result['answer'])"

echo -e "\n=== SPRINT 4: Running evaluation ==="
python eval.py

# Expected: Tất cả chạy không lỗi, output log/results
```

#### Task 4.3: Verify Output Files (15')

```bash
# Kiểm tra các file tạo ra:

# 1. ChromaDB index tạo được?
ls -la chroma_db/ 
# → Có nhiều file *.parquet

# 2. logs/grading_run.json tạo được?
ls -la logs/grading_run.json
# → File JSON với 10 câu hỏi

# 3. results/scorecard_*.md tạo được?
ls -la results/
# → scorecard_baseline.md, scorecard_variant.md

# 4. Kiểm tra JSON format
python -c "import json; f=open('logs/grading_run.json'); d=json.load(f); print(len(d), 'questions logged')"
# → 10 questions logged
```

#### Task 4.4: QC Final Code (15')

```bash
# Check mọi file Python:

python -m py_compile index.py rag_answer.py eval.py
# → Không có syntax error

# Check imports:
python -c "import index, rag_answer, eval"
# → Không có missing dependency

# Check main flows:
python index.py --help 2>/dev/null || echo "OK"
```

#### Task 4.5: Final Commit & Push (5')

```bash
# Sprint 4 final commit — trước 18:00!

git add -A
git commit -m "Sprint 4: Complete RAG pipeline + evaluation + docs

- All 3 demo scripts working end-to-end
- Logs and scorecard generated
- Architecture and tuning docs completed"

git push origin master
```

### ✅ Definition of Done — Sprint 4

- [ ] `python index.py` chạy không lỗi
- [ ] `python rag_answer.py` chạy test queries không lỗi
- [ ] `python eval.py` chạy evaluation không lỗi
- [ ] `logs/grading_run.json` tạo được (10 câu)
- [ ] `results/scorecard_baseline.md` tạo được
- [ ] `results/scorecard_variant.md` tạo được
- [ ] `docs/architecture.md` viết đầy đủ (do ĐẠT)
- [ ] `docs/tuning-log.md` viết đầy đủ (do ĐẠT)
- [ ] **Final commit trước 18:00** ✅

---

## 🎯 TÓNG TẮT — COMMIT CHECKLIST

Sau mỗi sprint, Trung commit:

```bash
# Sprint 1 commit
git commit -m "Sprint 1: Build index with metadata

- preprocess_document() extracts metadata from file headers
- chunk_document() splits by section, keeps 80-token overlap
- get_embedding() uses Sentence Transformers for local embeddings
- All 5 documents indexed into ChromaDB PersistentClient
- Metadata fields: source, section, effective_date"

# Sprint 2 commit
git commit -m "Sprint 2: Baseline dense retrieval + grounded answer

- retrieve_dense() queries ChromaDB with embedding similarity
- build_grounded_prompt() enforces 'answer only from context'
- call_llm() integration (OpenAI or Gemini)
- rag_answer() returns dict with answer, sources, chunks_used
- Test: SLA P1 → has citation; out-of-domain → abstain"

# Sprint 3 commit
git commit -m "Sprint 3: Add hybrid retrieval variant

- retrieve_sparse() BM25 keyword search
- retrieve_hybrid() Reciprocal Rank Fusion (60% dense, 40% sparse)
- compare_retrieval_strategies() shows delta for 5 test queries
- Hybrid finds +2 additional relevant docs for keyword-heavy queries"

# Sprint 4 commit
git commit -m "Sprint 4: Complete evaluation + documentation

- eval.py run_scorecard() for baseline and variant
- logs/grading_run.json (10 test questions)
- results/scorecard_baseline.md and scorecard_variant.md
- docs/architecture.md with chunking decision, retrieval config, pipeline diagram
- docs/tuning-log.md with baseline vs variant comparison
- End-to-end demo: python index.py && python rag_answer.py && python eval.py"
```

---

## 🚀 HOW TO RUN — QUICK REFERENCE

```bash
# 1. Setup
cd lab
pip install -r requirements.txt
cp .env.example .env
# Edit .env: add OPENAI_API_KEY or leave for Sentence Transformers

# 2. Sprint 1: Build index
python index.py
python -c "from index import list_chunks; list_chunks(n=10)"

# 3. Sprint 2: Test baseline
python rag_answer.py
# Interactive test in main()

# 4. Sprint 3: Compare hybrid
python -c "from rag_answer import compare_retrieval_strategies; compare_retrieval_strategies('SLA P1?')"

# 5. Sprint 4: Run evaluation
python eval.py
# Output: logs/grading_run.json, results/

# 6. Final: View results
cat results/scorecard_baseline.md
cat results/scorecard_variant.md
```

---

## 📌 NOTES

- **Mỗi sprint 60 phút** — quản lý thời gian chặt để không miss deadline 18:00
- **Nối code sau mỗi sprint** — không để pending, test end-to-end
- **Commit thường xuyên** — mỗi sprint 1 lần, message rõ ràng
- **QC nội bộ** — trước khi push, chạy qua 3–5 test queries
- **Ghi log khi debug** → giúp viết report sau

---

**Chúc bạn thành công! 🎯**
