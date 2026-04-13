# 🎯 HƯỚNG DẪN CHI TIẾT — VINH (Retrieval & Sparse Search)

**Vai trò:** Retrieval Owner & Hybrid Search Specialist  
**Trách nhiệm:** Implement BM25 sparse retrieval, hybrid fusion, debug retrieval issues  
**Điểm chịu trách nhiệm:** Sprint 3 variant implementation (5 điểm hybrid + comparison)

---

## 📋 TÓM TẮT CÔNG VIỆC

| Sprint | Công việc chính | File chính | Timeline |
|--------|-----------------|-----------|----------|
| **1–2** | Audit chunk quality | `index.py` | Parallel, 5' |
| **3** | Implement `retrieve_sparse()` | `rag_answer.py` L~90 | 15' |
| **3** | Implement `retrieve_hybrid()` | `rag_answer.py` L~128 | 20' |
| **3** | Test & compare baseline vs hybrid | `rag_answer.py` | 20' |
| **4** | Final QC retrieval metrics | `eval.py` | 5' |

---

## 🔍 SPRINT 1–2: AUDIT CHUNK QUALITY (Song song)

### Task: Kiểm tra chunks hợp lý

**Do:** Sau khi Trung chạy `python index.py`

```bash
python -c "
from index import list_chunks
# Check 10 mẫu chunks
list_chunks(n=10)
"

# Expected output:
# [1] policy_refund_v4.txt | Refund Timeline | score=N/A
#     Customers may request a refund within 30 days of purchase...
# [2] policy_refund_v4.txt | Refund Process | score=N/A
#     Submit refund request form to cs-team@company...
# ...
```

### Checklist — Chunk Quality

```bash
python -c "
from index import inspect_metadata_coverage, CHROMA_DB_DIR
import chromadb

# 1. Check metadata completeness
inspect_metadata_coverage()

# 2. Check chunk count per document
client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
coll = client.get_collection('rag_lab')
print(f'Total chunks: {coll.count()}')

# 3. Spot check chunk content (no truncation)
results = coll.get(limit=5)
for doc, meta in zip(results['documents'], results['metadatas']):
    print(f'{meta[\"source\"]} | {len(doc)} chars')
    if len(doc) > 2000:
        print('  ⚠ Very long chunk, might be lost-in-middle')
    if len(doc) < 300:
        print('  ⚠ Very short chunk, lacks context')
"
```

### Red Flags — Fix if you see

| Red Flag | Meaning | Action |
|----------|---------|--------|
| Chunk cuts mid-sentence | Chunking too aggressive | Ask Trung to increase chunk_size or overlap |
| No "section" metadata | section not extracted | Ask Trung to debug chunk_document() |
| "effective_date" all "unknown" | Metadata parse failed | Ask Trung to debug preprocess_document() |
| 200 chars avg per chunk | Too small, no context | Increase CHUNK_SIZE |
| 3000+ chars per chunk | Too big, lost-in-middle | Decrease CHUNK_SIZE, increase overlap |

---

## 🚀 SPRINT 3: IMPLEMENT SPARSE RETRIEVAL

### Task 1: Implement `retrieve_sparse()` (15')

**File:** `lab/rag_answer.py` (Line ~90)

```python
def retrieve_sparse(query: str, top_k: int = TOP_K_SEARCH) -> List[Dict[str, Any]]:
    """
    Sparse retrieval: BM25 keyword search.
    
    BM25 excels at exact keyword matching (error codes, specific terms).
    Unlike dense vectors which use semantic similarity, BM25 uses:
    - Term frequency within document
    - Inverse document frequency (IDF)
    - Document length normalization
    
    Args:
        query: User's question text
        top_k: Number of top chunks to return
    
    Returns:
        List[Dict] with same format as retrieve_dense()
    """
    from rank_bm25 import BM25Okapi
    import chromadb
    from index import CHROMA_DB_DIR
    
    # 1. Get all chunks from ChromaDB
    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    collection = client.get_collection("rag_lab")
    
    # Retrieve ALL chunks (no filtering yet)
    all_results = collection.get(
        include=["documents", "metadatas"],
        limit=10000  # Get all chunks
    )
    
    # 2. Prepare corpus for BM25
    documents = all_results["documents"]
    metadatas = all_results["metadatas"]
    
    # Tokenize documents (simple: split by whitespace)
    corpus = [doc.lower().split() for doc in documents]
    
    # 3. Build BM25 index
    bm25 = BM25Okapi(corpus)
    
    # 4. Tokenize query
    query_tokens = query.lower().split()
    
    # 5. Score all documents
    scores = bm25.get_scores(query_tokens)
    
    # 6. Get top-k
    top_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]
    
    # 7. Format results
    chunks = []
    for idx in top_indices:
        chunks.append({
            "text": documents[idx],
            "metadata": metadatas[idx],
            "score": scores[idx]  # BM25 score
        })
    
    return chunks

# Expected output:
# Query: "ERR-403-ACCESS-DENIED"
# [
#   {
#     "text": "ERR-403: Permission denied...",
#     "metadata": {"source": "it_helpdesk_faq.txt", "section": "Error Codes", ...},
#     "score": 4.2
#   },
#   ...
# ]

# Note: BM25 score != cosine similarity, but higher = more relevant
```

### BM25 Explanation (Why it helps)

```
Dense (Semantic) vs Sparse (Keyword):

Dense Query: "I need access"
  → Embedding captures semantic meaning
  → Matches similar concepts: "grant permission", "assign role"
  ✓ Good for NL semantic queries
  ❌ Bad for exact keyword: "ERR-403"

Sparse Query: "ERR-403"
  → BM25 finds exact term match "ERR-403"
  → Doesn't understand semantics, just term frequency
  ✓ Good for error codes, specific names
  ❌ Bad for paraphrased queries: "permission denied" ← doesn't match "ERR-403"
```

### Task 2: Implement `retrieve_hybrid()` (20')

**File:** `lab/rag_answer.py` (Line ~128)

```python
def retrieve_hybrid(
    query: str,
    top_k: int = TOP_K_SEARCH,
    dense_weight: float = 0.6,
    sparse_weight: float = 0.4,
) -> List[Dict[str, Any]]:
    """
    Hybrid retrieval: Combine Dense + Sparse using Reciprocal Rank Fusion (RRF).
    
    RRF formula: score = sum of (weight / (rank + 1)) across sources
    
    Why RRF is good:
    - Simple: doesn't need score normalization (cosine vs BM25 use different scales)
    - Effective: combines two complementary signals
    - Robust: one source's failure doesn't hurt much
    
    Args:
        query: User's question
        top_k: Final n results to return
        dense_weight: Weight for dense results (0.6 = 60%)
        sparse_weight: Weight for sparse results (0.4 = 40%)
    
    Returns:
        List[Dict] merged & reranked by RRF score
    """
    
    # 1. Retrieve from both sources
    print(f"  [Hybrid] Retrieving dense results...")
    dense_results = retrieve_dense(query, top_k=top_k)
    
    print(f"  [Hybrid] Retrieving sparse (BM25) results...")
    sparse_results = retrieve_sparse(query, top_k=top_k)
    
    # 2. Create rank mappings (chunk_id → rank)
    # Use chunk text as ID (simple approach)
    dense_rank_map = {
        chunk["text"]: i
        for i, chunk in enumerate(dense_results)
    }
    sparse_rank_map = {
        chunk["text"]: i
        for i, chunk in enumerate(sparse_results)
    }
    
    # 3. Collect all unique chunks
    all_chunks = {}
    for chunk in dense_results + sparse_results:
        text = chunk["text"]
        if text not in all_chunks:
            all_chunks[text] = chunk.copy()
            all_chunks[text]["rrf_score"] = 0.0
    
    # 4. Calculate RRF score for each chunk
    for text, chunk in all_chunks.items():
        dense_rank = dense_rank_map.get(text, top_k)  # Use top_k if not found
        sparse_rank = sparse_rank_map.get(text, top_k)
        
        # RRF formula
        rrf_score = (
            dense_weight / (dense_rank + 1) +
            sparse_weight / (sparse_rank + 1)
        )
        
        chunk["rrf_score"] = rrf_score
    
    # 5. Sort by RRF score & return top-k
    sorted_chunks = sorted(
        all_chunks.values(),
        key=lambda x: x["rrf_score"],
        reverse=True
    )[:top_k]
    
    return sorted_chunks

# Expected output:
# Query: "ERR-403"
# Dense: Finds semantic matches (error, access, permission)
# Sparse: Finds exact "ERR-403"
# RRF Merge:
#   [1] ERR-403 doc (rank 3 dense, rank 1 sparse) → RRF score = 0.6/4 + 0.4/2 = 0.35 ⭐ HIGH
#   [2] Permission doc (rank 1 dense, rank 10+ sparse) → RRF = 0.6/2 + 0 = 0.30
#   [3] Another access doc (rank 2 dense, rank 5 sparse) → RRF = 0.6/3 + 0.4/6 = 0.27
```

### RRF Scoring Example

```
Query: "Level 3 access approval"

Dense Results:
  [1] (rank 1) "Approval process for Level 3..." - score: 0.85
  [2] (rank 2) "Access control policies..." - score: 0.78
  [3] (rank 3) "Manager approval matrix..." - score: 0.72

Sparse Results:
  [1] (rank 1) "Level 3 access requires..." - score: 4.5
  [2] (rank 2) "Approval by Manager and..." - score: 4.2
  [3] (rank 3) "Level 2 access differs..." - score: 3.1

RRF Scores (dense_weight=0.6, sparse_weight=0.4):

"Approval process for Level 3..."
  Dense rank: 1, Sparse rank: ~8 (not in top-3)
  RRF = 0.6/(1+1) + 0.4/(8+1) = 0.30 + 0.044 = 0.344

"Level 3 access requires..."
  Dense rank: ~5 (not top-3)
  Sparse rank: 1
  RRF = 0.6/(5+1) + 0.4/(1+1) = 0.1 + 0.2 = 0.3

"Manager approval matrix..."
  Dense rank: 3, Sparse rank: 2
  RRF = 0.6/(3+1) + 0.4/(2+1) = 0.15 + 0.133 = 0.283

Final ranking: [1] → [2] → [3] (sorted by RRF score)
```

---

## 🧪 SPRINT 3: TEST & COMPARE

### Task 3: Test `retrieve_hybrid()` on sample queries (15')

```bash
python -c "
from rag_answer import retrieve_dense, retrieve_sparse, retrieve_hybrid

# Test queries where hybrid should help
test_queries = [
    'SLA P1 response time',           # Semantic + keyword
    'ERR-403-ACCESS-DENIED',          # Mostly keyword (error code)
    'Request Level 2 access form',    # Keyword heavy (form, request)
]

for query in test_queries:
    print(f'\n{\"=\"*70}')
    print(f'Query: {query}')
    print(f'{\"=\"*70}')
    
    # Dense
    dense = retrieve_dense(query, top_k=3)
    print(f'\nDENSE Results:')
    for i, chunk in enumerate(dense, 1):
        print(f'  [{i}] {chunk[\"metadata\"][\"source\"]} | Score: {chunk[\"score\"]:.3f}')
        print(f'      {chunk[\"text\"][:70]}...')
    
    # Sparse
    sparse = retrieve_sparse(query, top_k=3)
    print(f'\nSPARSE Results:')
    for i, chunk in enumerate(sparse, 1):
        print(f'  [{i}] {chunk[\"metadata\"][\"source\"]} | Score: {chunk[\"score\"]:.3f}')
        print(f'      {chunk[\"text\"][:70]}...')
    
    # Hybrid
    hybrid = retrieve_hybrid(query, top_k=3)
    print(f'\nHYBRID Results (RRF):')
    for i, chunk in enumerate(hybrid, 1):
        print(f'  [{i}] {chunk[\"metadata\"][\"source\"]} | RRF Score: {chunk[\"rrf_score\"]:.3f}')
        print(f'      {chunk[\"text\"][:70]}...')
    
    # Analysis
    dense_sources = {c['metadata']['source'] for c in dense}
    sparse_sources = {c['metadata']['source'] for c in sparse}
    hybrid_sources = {c['metadata']['source'] for c in hybrid}
    
    print(f'\nAnalysis:')
    print(f'  Dense sources: {dense_sources}')
    print(f'  Sparse sources: {sparse_sources}')
    print(f'  Hybrid sources: {hybrid_sources}')
    
    added = hybrid_sources - dense_sources
    if added:
        print(f'  ✓ Hybrid added: {added}')
"
```

### Task 4: Implement `compare_retrieval_strategies()` (do via Trung)

This is called by Trung in Sprint 3 to show side-by-side comparison.

```python
# Already in rag_answer.py (Trung implements)
# Your job: make sure retrieve_dense(), retrieve_sparse(), retrieve_hybrid() work correctly

# Test it:
python -c "
from rag_answer import compare_retrieval_strategies
compare_retrieval_strategies('ERR-403-ACCESS-DENIED')
compare_retrieval_strategies('Request Level 2 access')
"
```

### Expected Output

```
================================================================================
COMPARE: Dense vs Hybrid
Query: ERR-403-ACCESS-DENIED
================================================================================

BASELINE (Dense):
  [1] it_helpdesk_faq.txt | Score: 0.82
      Error 403 occurs when user lacks required permission to access...
  [2] access_control_sop.txt | Score: 0.68
      Access Control defines 5 levels from 0 (guest) to 4 (admin)...
  [3] policy_refund_v4.txt | Score: 0.45
      Refund requests process... [NOT RELEVANT]

VARIANT (Hybrid):
  [1] it_helpdesk_faq.txt | RRF Score: 0.42
      ERR-403: Permission Denied Error [Exact match on "ERR-403"]
  [2] access_control_sop.txt | RRF Score: 0.35
      Permission denied errors require access request...
  [3] ?

ANALYSIS:
  Dense sources: {'it_helpdesk_faq.txt', 'access_control_sop.txt', 'policy_refund_v4.txt'}
  Hybrid sources: {'it_helpdesk_faq.txt', 'access_control_sop.txt'}
  Additional in Hybrid: {}
  Lost in Hybrid: {'policy_refund_v4.txt'} ← Removed noise! ✓
```

---

## 🎯 SPRINT 4: RETRIEVAL METRICS IN EVAL

### Metric: Context Recall

Your job: Make sure `score_context_recall()` works correctly (Đạt implements, but you need to understand).

```python
# What it measures:
# "Did we retrieve the expected sources?"

# Example:
# Question: "SLA P1?"
# expected_sources: ["sla_p1_2026.txt"]
# retrieved_sources: ["sla_p1_2026.txt", "policy_refund_v4.txt"]
# Score: 1.0 (found expected source)

# Example 2:
# Question: "Request Level 2 access?"
# expected_sources: ["access_control_sop.txt"]
# retrieved_sources: ["it_helpdesk_faq.txt"]  ← Wrong source!
# Score: 0.0 (missed expected source)
```

### Your Responsibility — Final QC

```bash
# After eval.py runs:

python -c "
import json

# Check baseline vs variant context_recall
with open('results/baseline_results.json') as f:
    baseline = json.load(f)

with open('results/variant_results.json') as f:
    variant = json.load(f)

print('Context Recall Comparison:')
for b, v in zip(baseline, variant):
    b_recall = b['context_recall']['score']
    v_recall = v['context_recall']['score']
    delta = v_recall - b_recall if v_recall and b_recall else None
    print(f\"  {b['id']}: {b_recall:.2f} → {v_recall:.2f} (delta: {delta:+.2f})\")
"
```

---

## ✅ FINAL CHECKLIST — VINH

### Sprint 1–2: Chunk Audit
- [ ] ChromaDB index exists (chroma_db/ folder)
- [ ] `list_chunks(n=10)` shows meaningful chunks
- [ ] No chunks truncated mid-sentence
- [ ] Metadata fields: source, section, effective_date all populated
- [ ] No red flags (too large, too small, incomplete)

### Sprint 3: Sparse & Hybrid Implementation
- [ ] `retrieve_sparse()` implemented with BM25
- [ ] `retrieve_sparse()` returns top-k chunks with BM25 score
- [ ] `retrieve_hybrid()` implemented with RRF fusion
- [ ] RRF scoring formula correct: weight/(rank+1) + weight/(rank+1)
- [ ] Test on 3+ queries, hybrid shows meaningful improvement
- [ ] Error codes (ERR-403, etc) found by sparse but not dense

### Sprint 3: Comparison & Analysis
- [ ] `compare_retrieval_strategies()` outputs clear table
- [ ] Shows dense vs hybrid for same query
- [ ] Identifies: new sources, lost sources, rank changes
- [ ] Analysis appendix explains why hybrid better for this corpus

### Sprint 4: Evaluation
- [ ] Eval runs without errors on both baseline (dense) and variant (hybrid)
- [ ] Context Recall metric improves with hybrid (expected +0.05 to +0.15)
- [ ] No regression: other metrics stable or improved
- [ ] Final log/scorecard ready for commit

### Code Quality
- [ ] No syntax errors in retrieve_sparse(), retrieve_hybrid()
- [ ] BM25Okapi imported correctly
- [ ] chromadb client initialized correctly
- [ ] Results format matches retrieve_dense() signature

---

## 💡 TIPS & GOTCHAS

1. **BM25 score is NOT normalized**
   - Cosine similarity: 0.0–1.0
   - BM25: 0.0–∞ (depends on corpus)
   - RRF fixes this by using rank instead of raw score ✓

2. **Whitespace tokenization is simple but works**
   - For sophistication, could use `nltk.word_tokenize()` or `spacy`
   - But simple `.split()` is fine for MVP

3. **Dense weights should match corpus type**
   - 60% dense + 40% sparse: balanced approach
   - If corpus 80% semantic, use 0.8 + 0.2
   - If corpus 80% keyword, use 0.4 + 0.6

4. **Test on diverse queries**
   - Semantic: "SLA P1 response time"
   - Keyword: "ERR-403"
   - Mixed: "Request Level 2 access form"

5. **BM25 is vocabulary-dependent**
   - "P1 vs P1" → exact match ✓
   - "P1 vs Priority 1" → NO match (different tokens) ✗
   - To fix: need query expansion or synonym handling (Sprint 3+ feature)

---

## 🚀 QUICK COMMAND

```bash
# Test sparse + hybrid
python -c "
from rag_answer import retrieve_dense, retrieve_sparse, retrieve_hybrid

q = 'ERR-403'
print('=== Dense ===')
for c in retrieve_dense(q, top_k=3): print(f\"{c['metadata']['source']} | {c['score']:.2f}\")

print('\n=== Sparse ===')
for c in retrieve_sparse(q, top_k=3): print(f\"{c['metadata']['source']} | {c['score']:.2f}\")

print('\n=== Hybrid ===')
for c in retrieve_hybrid(q, top_k=3): print(f\"{c['metadata']['source']} | {c['rrf_score']:.2f}\")
"
```

---

**Chúc bạn thành công! 🎯**
