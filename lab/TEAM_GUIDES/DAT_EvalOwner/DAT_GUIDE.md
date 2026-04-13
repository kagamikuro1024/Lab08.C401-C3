# 🎯 HƯỚNG DẪN CHI TIẾT — ĐẠT (Eval Owner)

**Vai trò:** Eval Owner & Documentation Lead  
**Trách nhiệm:** Tạo test_questions.json, implement scoring, viết architecture.md + tuning-log.md  
**Điểm chịu trách nhiệm:** Documentation (10 điểm) + Grading logistics (30 điểm)

---

## 📋 TÓM TẮT CÔNG VIỆC

| Sprint | Công việc chính | File chính | Điểm | Status |
|--------|-----------------|-----------|------|--------|
| **1–2** | Chuẩn bị test_questions.json | `data/test_questions.json` | 5 | ⬜ |
| **3–4** | Implement scoring functions | `eval.py` | 5 | ⬜ |
| **4** | Viết `architecture.md` & `tuning-log.md` | `docs/` | 10 | ⬜ |
| **4** | Generate grading_run.json + scorecard | `logs/`, `results/` | Bonus | ⬜ |

---

## 📝 SPRINT 1–2: CHUẨN BỊ TEST QUESTIONS (Song song với Sprint 1–2)

### Công việc: Tạo `data/test_questions.json`

**File:** `lab/data/test_questions.json`

### Định nghĩa test_questions.json

```json
[
  {
    "id": "q01",
    "question": "SLA xử lý ticket P1 là bao lâu?",
    "expected_answer": "P1 tickets yêu cầu phản hồi trong 15 phút và xử lý hoàn tất trong 4 giờ",
    "expected_sources": ["sla_p1_2026.txt"],
    "grading_criteria": [
      "Mention 15-minute response time",
      "Mention 4-hour resolution time",
      "Cite source document"
    ]
  },
  {
    "id": "q02",
    "question": "Khách hàng có thể yêu cầu hoàn tiền trong bao lâu kể từ ngày mua?",
    "expected_answer": "Khách hàng có thể yêu cầu hoàn tiền trong vòng 30 ngày kể từ ngày mua",
    "expected_sources": ["policy_refund_v4.txt"],
    "grading_criteria": [
      "Mention 30-day window",
      "Clarify it's from purchase date",
      "Cite source"
    ]
  },
  {
    "id": "q03",
    "question": "Ai phải phê duyệt để cấp quyền Level 3?",
    "expected_answer": "Level 3 access yêu cầu phê duyệt từ [Department Head + Security Officer] hoặc [Manager + Team Lead]",
    "expected_sources": ["access_control_sop.txt"],
    "grading_criteria": [
      "Identify approval chain correctly",
      "Mention both required roles",
      "Cite source"
    ]
  },
  {
    "id": "q04",
    "question": "ERR-403-ACCESS-DENIED có nghĩa gì và cách khắc phục?",
    "expected_answer": "Permission denied - user lacks required role/access level. Solution: Submit access request to IT Security team at ...",
    "expected_sources": ["it_helpdesk_faq.txt"],
    "grading_criteria": [
      "Explain error meaning",
      "Provide resolution steps",
      "Link to IT helpdesk contact"
    ]
  },
  {
    "id": "q05",
    "question": "Chính sách leave bao nhiêu ngày phép mỗi năm?",
    "expected_answer": "Tùy vào công ty - [check hr_leave_policy.txt para expected], typically 15–20 days per year",
    "expected_sources": ["hr_leave_policy.txt"],
    "grading_criteria": [
      "Find correct annual leave allocation",
      "Mention any conditions (tenure-based, etc)",
      "Cite source"
    ]
  },
  {
    "id": "q06",
    "question": "P1 vs. P2 tickets có sự khác biệt gì về SLA?",
    "expected_answer": "P1: 15min response + 4hr resolution | P2: 1hr response + 24hr resolution (theo tài liệu [1])",
    "expected_sources": ["sla_p1_2026.txt"],
    "grading_criteria": [
      "Compare both P1 and P2 SLA times",
      "Must have both response + resolution",
      "Numbers must be exact from doc"
    ]
  },
  {
    "id": "q07",
    "question": "Làm sao để request Level 2 access nếu là Level 1 user?",
    "expected_answer": "Submit access request form tại [URL] to [email], Manager phê duyệt, IT thực hiện",
    "expected_sources": ["access_control_sop.txt"],
    "grading_criteria": [
      "Step-by-step process",
      "Mention form/URL",
      "Mention approver role",
      "Mention action owner (IT)"
    ]
  },
  {
    "id": "q08",
    "question": "Nếu khách hàng muốn refund sau 35 ngày mua, có được không?",
    "expected_answer": "Không được - chính sách chỉ cho phép hoàn tiền trong vòng 30 ngày",
    "expected_sources": ["policy_refund_v4.txt"],
    "grading_criteria": [
      "Clear rejection answer",
      "Must explain why (beyond 30-day window)",
      "Cite policy document"
    ]
  },
  {
    "id": "q09",
    "question": "Tôi là nhân viên IT Level 2, có thể approve Level 3 access request không?",
    "expected_answer": "Không - chỉ [specific roles từ access_control_sop.txt] mới có quyền approve Level 3",
    "expected_sources": ["access_control_sop.txt"],
    "grading_criteria": [
      "Clear 'No' answer",
      "Must cite who CAN approve",
      "Must reference approval matrix"
    ]
  },
  {
    "id": "q10",
    "question": "Công ty cấp sick leave, parental leave, hay sabbatical không?",
    "expected_answer": "Theo chính sách [tên cụ thể từ file], công ty cấp [list specific leaves]",
    "expected_sources": ["hr_leave_policy.txt"],
    "grading_criteria": [
      "Identify which leave types are supported",
      "Any specific conditions/rules?",
      "Cite source document"
    ]
  }
]
```

### Hướng dẫn tạo test_questions.json

1. **Yêu cầu 10 câu hỏi đa dạng:**
   - ✅ 2–3 câu từ policy_refund (factual, straightforward)
   - ✅ 2–3 câu từ sla_p1 (comparison, specific numbers)
   - ✅ 2–3 câu từ access_control (process, approval chain)
   - ✅ 1–2 câu từ it_helpdesk (error codes, troubleshooting)
   - ✅ 1–2 câu từ hr_leave (benefits, policy)

2. **Mỗi câu phải có:**
   - `id`: "q01"–"q10" (dùng cho scoring sau)
   - `question`: Câu hỏi bằng Tiếng Việt, tự nhiên (không formal)
   - `expected_answer`: Câu trả lời "đúng" theo doc (tham khảo, không bắt buộc nghe)
   - `expected_sources`: List file nào chứa câu trả lời
   - `grading_criteria`: 2–4 điều kiện để chấm **Full** (benchmark)

3. **Gợi ý câu hỏi:**
   - **Factual:** "X là bao nhiêu?" (SLA P1, refund window)
   - **Comparison:** "P1 vs P2 khác gì?" (cần compare 2+ attributes)
   - **Boundary:** "Nếu X là 35 ngày, được không?" (test extreme case)
   - **Process:** "Làm sao để ...?" (approval chain, request process)
   - **Error:** "ERR-403-... là gì?" (error code explanation)
   - **Out-of-domain:** (tùy chọn) Câu không trong docs → test abstain

4. **Expected sources mapping:**
   ```
   policy_refund_v4.txt → refund timeline, refund process, conditions
   sla_p1_2026.txt → P1 SLA, P2 SLA, escalation
   access_control_sop.txt → approval matrix, access levels, request process
   it_helpdesk_faq.txt → error codes, troubleshooting, common issues
   hr_leave_policy.txt → annual leave, sick leave, special leave types
   ```

5. **JSON format validation:**
   ```bash
   python -c "import json; f=open('data/test_questions.json'); d=json.load(f); print(f'{len(d)} questions, keys: {d[0].keys()}')"
   # Output: 10 questions, keys: dict_keys(['id', 'question', 'expected_answer', 'expected_sources', 'grading_criteria'])
   ```

---

## 🎯 SPRINT 3–4: IMPLEMENT SCORING FUNCTIONS

### Công việc: Implement `eval.py` functions

**File:** `lab/eval.py`

### Task 1: Implement `score_faithfulness()` (10')

```python
# File: lab/eval.py (Line ~50)

def score_faithfulness(
    answer: str,
    chunks_used: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Faithfulness: Câu trả lời có bám đúng chứng cứ không?
    Scale: 1–5
      5: Mọi thông tin trong answer đều có trong chunks
      4: Gần 100% grounded, 1 chi tiết nhỏ chưa chắc
      3: Phần lớn grounded, vài thông tin từ model knowledge
      2: Nhiều thông tin không có trong chunks
      1: Phần lớn/toàn bộ answer là model bịa
    """
    
    # CÁCH 1: Chấm thủ công (Simple, dùng cho dev/testing)
    # Đơn giản: đọc answer + chunks, check xem info có trong chunks không
    # → Trả về dict với score (1–5) + notes
    
    # CÁCH 2: LLM-as-Judge (Tự động, nâng cao)
    # Gửi prompt cho LLM, LLM rating faithfulness
    
    # Đề xuất: CÁCH 1 (thủ công) cho dev, CÁCH 2 (LLM) nếu có thời gian
    
    # PLACEHOLDER:
    return {
        "score": None,  # Developer phải chấm thủ công
        "notes": "Manual review required: check if answer grounded in context"
    }
```

### Task 2: Implement `run_scorecard()` (20')

```python
# File: lab/eval.py (Line ~216)

def run_scorecard(
    config: Dict[str, Any],  # {"retrieval_mode": "dense", ...}
    test_questions: Optional[List[Dict]] = None,
    verbose: bool = True,
) -> List[Dict[str, Any]]:
    """
    Run pipeline trên test_questions, return scorecard results
    """
    if test_questions is None:
        with open(TEST_QUESTIONS_PATH) as f:
            test_questions = json.load(f)
    
    results = []
    for q in test_questions:
        # 1. Run RAG pipeline
        result = rag_answer(
            q["question"],
            retrieval_mode=config.get("retrieval_mode", "dense"),
            top_k_search=config.get("top_k_search", 10),
            top_k_select=config.get("top_k_select", 3),
            use_rerank=config.get("use_rerank", False),
            verbose=False
        )
        
        # 2. Score answer
        faithfulness = score_faithfulness(result["answer"], result["chunks_used"])
        answer_relevance = score_answer_relevance(q["question"], result["answer"])
        context_recall = score_context_recall(
            result["chunks_used"],
            q.get("expected_sources", [])
        )
        completeness = score_completeness(
            q["question"],
            result["answer"],
            q.get("expected_answer", "")
        )
        
        # 3. Log result
        results.append({
            "id": q["id"],
            "question": q["question"],
            "answer": result["answer"],
            "expected_answer": q.get("expected_answer", "N/A"),
            "expected_sources": q.get("expected_sources", []),
            "retrieved_sources": result["sources"],
            "faithfulness": faithfulness,
            "answer_relevance": answer_relevance,
            "context_recall": context_recall,
            "completeness": completeness,
            "config": config,
        })
        
        if verbose:
            print(f"[{q['id']}] {q['question'][:50]}...")
            print(f"  Faithfulness: {faithfulness['score']}/5")
            print(f"  Answer Relevance: {answer_relevance['score']}/5")
    
    return results
```

### Task 3: Implement `compare_ab()` (15')

```python
# File: lab/eval.py (Line ~325)

def compare_ab(
    baseline_results: List[Dict],
    variant_results: List[Dict],
    output_file: Optional[str] = None,
) -> None:
    """
    Create A/B comparison table: baseline vs variant
    """
    print(f"\n{'='*100}")
    print(f"A/B COMPARISON: Baseline vs Variant")
    print(f"{'='*100}\n")
    
    # Create comparison table
    comparison = []
    for b_res, v_res in zip(baseline_results, variant_results):
        comparison.append({
            "id": b_res["id"],
            "question": b_res["question"][:50] + "...",
            "baseline_faith": b_res["faithfulness"]["score"],
            "variant_faith": v_res["faithfulness"]["score"],
            "delta_faith": (v_res["faithfulness"]["score"] or 0) - (b_res["faithfulness"]["score"] or 0),
            "baseline_recall": b_res["context_recall"]["score"],
            "variant_recall": v_res["context_recall"]["score"],
            "delta_recall": (v_res["context_recall"]["score"] or 0) - (b_res["context_recall"]["score"] or 0),
        })
    
    # Print table
    import pandas as pd
    df = pd.DataFrame(comparison)
    print(df.to_string(index=False))
    
    # Summary
    avg_baseline_faith = sum(r["faithfulness"]["score"] or 0 for r in baseline_results) / len(baseline_results)
    avg_variant_faith = sum(r["faithfulness"]["score"] or 0 for r in variant_results) / len(variant_results)
    
    print(f"\n\nSUMMARY:")
    print(f"  Baseline Avg Faithfulness: {avg_baseline_faith:.2f}/5")
    print(f"  Variant Avg Faithfulness: {avg_variant_faith:.2f}/5")
    print(f"  Delta: {avg_variant_faith - avg_baseline_faith:+.2f}")
    
    # Questions improved/regressed
    improved = [c for c in comparison if c["delta_faith"] > 0]
    regressed = [c for c in comparison if c["delta_faith"] < 0]
    print(f"\n  Improved: {len(improved)} questions")
    print(f"  Regressed: {len(regressed)} questions")
```

### Task 4: Run Scorecard (10')

```bash
# In eval.py main():

if __name__ == "__main__":
    print("Running Scorecard Evaluation...")
    
    # Load test questions
    with open(TEST_QUESTIONS_PATH) as f:
        test_questions = json.load(f)
    
    # Run baseline
    print("\n[1/2] Running BASELINE (dense retrieval)...")
    baseline_results = run_scorecard(BASELINE_CONFIG, test_questions, verbose=True)
    
    # Run variant
    print("\n[2/2] Running VARIANT (hybrid retrieval)...")
    variant_results = run_scorecard(VARIANT_CONFIG, test_questions, verbose=True)
    
    # Compare
    compare_ab(baseline_results, variant_results)
    
    # Save results
    RESULTS_DIR.mkdir(exist_ok=True)
    with open(RESULTS_DIR / "baseline_results.json", "w") as f:
        json.dump(baseline_results, f, indent=2, ensure_ascii=False)
    with open(RESULTS_DIR / "variant_results.json", "w") as f:
        json.dump(variant_results, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Evaluation complete. Results saved to results/")
```

---

## 📄 SPRINT 4: VIẾT DOCUMENTATION

### Task 1: Viết `docs/architecture.md` (30')

**File:** `lab/docs/architecture.md`

```markdown
# Architecture — RAG Pipeline

## 1. Tổng quan

Xây dựng internal assistant trả lời câu hỏi về:
- Chính sách hoàn tiền (policy_refund)
- SLA ticket (sla_p1)
- Cấp quyền hệ thống (access_control)
- FAQ IT Helpdesk (it_helpdesk)
- HR Leave Policy (hr_leave)

Pipeline: **Docs → Chunk → Embed → Store** → **Query → Retrieve → Generate → Answer**

## 2. Indexing Decision

| Tham số | Giá trị | Lý do |
|---------|---------|-------|
| Chunk size | 400 tokens (~1600 ký tự) | Đủ context, tránh lost-in-middle |
| Overlap | 80 tokens | Đảm bảo không mất context giữa chunks |
| Chunking | Section-based | Tài liệu có === Heading ===, tránh cắt gọt |
| Metadata | source, section, effective_date | source → trace doc, effective_date → freshness |

### 2.1 Metadata Fields

```python
{
    "source": "policy_refund_v4.txt",      # File name (dùng cho citation)
    "section": "Refund Timeline",            # Heading (context clarity)
    "effective_date": "2024-01-01",        # When policy applies
    "department": "CS",                      # Filter option
    "access": "internal"                     # Access control
}
```

## 3. Retrieval Pipeline

### 3.1 Baseline (Dense)

```
User Query → Embed (Sentence Transformers) → ChromaDB Vector Search → Top-10 → Select Top-3 → LLM
```

**Config:**
- Retrieval mode: Dense (semantic similarity)
- Top-k search: 10 (broad search)
- Top-k select: 3 (send to LLM)
- Rerank: No

### 3.2 Variant (Hybrid)

```
User Query → Dense + BM25 → RRF Fusion → Top-10 → Select Top-3 → LLM
```

**Config:**
- Retrieval mode: Hybrid (dense + BM25)
- Dense weight: 0.6, Sparse weight: 0.4
- RRF scoring per chunk
- Rerank: No (optional)

## 4. Embedding & LLM

| Component | Choice | Reason |
|-----------|--------|--------|
| Embedding model | Sentence Transformers: paraphrase-multilingual-MiniLM-L12-v2 | Local, no API key, multilingual |
| Vector store | ChromaDB PersistentClient | Simple, persistent, local |
| LLM | GPT-4o-mini (OpenAI) | Fast, cheap, reliable |
| Temperature | 0 | Deterministic output for evaluation |
| Max tokens | 512 | Keep answer focused |

## 5. Generation Prompt

```
Answer ONLY from the retrieved context below.
If the context is insufficient, say "Không đủ dữ liệu".
Cite the source field when possible using [1], [2], etc.
Keep your answer short, clear, and factual.

Question: {query}

Context:
[1] {source} | {section}
{chunk_text}

[2] ...

Answer:
```

## 6. Pipeline Architecture (Mermaid)

\`\`\`mermaid
graph LR
    A["📄 Raw Docs<br/>(5 files)"] --> B["🔄 Preprocess<br/>(extract metadata)"]
    B --> C["✂️ Chunk<br/>(section-based)"]
    C --> D["🧮 Embed<br/>(Sentence-Transformers)"]
    D --> E["💾 ChromaDB<br/>(PersistentClient)"]
    
    F["🤔 User Query"] --> G{"Retrieval Mode"}
    G -->|Dense| H["🔎 ChromaDB Vector Search<br/>(Top-10)"]
    G -->|Hybrid| I["🔎 Dense + BM25<br/>(RRF Fusion)"]
    
    H --> J["🎯 Select Top-3"]
    I --> J
    
    J --> K["📝 Build Context Block<br/>(with citations)"]
    K --> L["📋 Grounded Prompt"]
    L --> M["🤖 LLM (GPT-4o-mini)<br/>(temperature=0)"]
    M --> N["📤 Answer + Sources<br/>(with citations)"]
    
    style A fill:#e1f5ff
    style E fill:#fff3e0
    style M fill:#f3e5f5
    style N fill:#c8e6c9
\`\`\`

## 7. Metadata Examples

**Example 1: Refund Policy**
```
source: policy_refund_v4.txt
section: Refund Timeline
effective_date: 2024-01-01
department: CS
access: internal
```

**Example 2: SLA P1**
```
source: sla_p1_2026.txt
section: P1 SLA Metrics
effective_date: 2026-01-01
department: Support
access: internal
```

## 8. Failure Modes & Debugging

| Mode | Symptom | Check |
|------|---------|-------|
| Indexing fail | Retrieve old/wrong chunk | `list_chunks()` → verify metadata |
| Chunking sucks | Chunk cuts mid-sentence | Review chunk text, increase overlap |
| Retrieval miss | Expected source not found | Run dense vs hybrid comparison |
| Generation fail | Answer not grounded | Check temperature=0, prompt clarity |
| Format error | JSON invalid | Validate UTF-8, check quotes |

---

**Created:** [DATE]  
**Last Updated:** [TODAY]
```

### Task 2: Viết `docs/tuning-log.md` (30')

**File:** `lab/docs/tuning-log.md`

```markdown
# Tuning Log — RAG Pipeline Optimization

## Baseline (Sprint 2)

**Date:** [Sprint 2 completion date]

### Configuration

\`\`\`
retrieval_mode = "dense"
chunk_size = 400 tokens
chunk_overlap = 80 tokens
top_k_search = 10
top_k_select = 3
embedding_model = "paraphrase-multilingual-MiniLM-L12-v2"
llm_model = "gpt-4o-mini"
temperature = 0
rerank = False
\`\`\`

### Baseline Scorecard (10 test questions)

| ID | Question | Faithfulness | Answer Relevance | Context Recall | Completeness | Status |
|----|----------|--------------|------------------|-----------------|--------------|--------|
| q01 | SLA P1? | 5/5 | 5/5 | 1.0 | 1.0 | ✓ Full |
| q02 | Refund window? | 5/5 | 5/5 | 1.0 | 0.9 | ✓ Full |
| q03 | Level 3 approver? | 4/5 | 4/5 | 1.0 | 0.8 | Partial |
| q04 | ERR-403? | 3/5 | 4/5 | 0.8 | 0.7 | Partial |
| q05 | Annual leave? | 5/5 | 5/5 | 1.0 | 1.0 | ✓ Full |
| q06 | P1 vs P2 SLA? | 5/5 | 5/5 | 1.0 | 1.0 | ✓ Full |
| q07 | Request Level 2? | 2/5 | 3/5 | 0.5 | 0.4 | ❌ Zero |
| q08 | Refund after 35 days? | 5/5 | 5/5 | 1.0 | 1.0 | ✓ Full |
| q09 | IT Level 2 approve L3? | 4/5 | 5/5 | 1.0 | 1.0 | ✓ Full |
| q10 | Special leave types? | 3/5 | 3/5 | 0.6 | 0.5 | Partial |

### Baseline Averages
- Faithfulness: 4.1/5
- Answer Relevance: 4.2/5
- Context Recall: 0.86/1.0
- Completeness: 0.85/1.0

### Weakest Questions
1. **q07** (Request Level 2): Dense misses "request form" + "approval steps" details
   - Root cause: Semantic query doesn't match "form submission" keywords well
   - Evidence: Expected source mentions "Submit form at [URL]" but retrieval ranks it low
   
2. **q04** (ERR-403): Dense retrieves general IT FAQ but misses error-code section
   - Root cause: Error code lookup needs keyword matching, not semantic match
   - Evidence: BM25 would find "ERR-403" keyword directly
   
3. **q10** (Special leave): Scattered across HR policy, dense retrieval incomplete

### Hypothesis: Why Variant (Hybrid) Should Help
- Dense struggles with **keyword/code lookups** (ERR-403, "form", "Level 2")
- Dense misses **alias queries** ("P1" semantic vs "Priority 1" keyword)
- **Hybrid (BM25 + Dense)** will find exact keyword matches + semantic meaning
- Expected improvement: q04, q07 from Partial → Full

---

## Variant 1: Hybrid Retrieval (Sprint 3)

**Date:** [Sprint 3 completion date]  
**Change:** Switch from Dense-only to **Hybrid (Dense 0.6 + BM25 0.4)**

### Configuration

\`\`\`
retrieval_mode = "hybrid"  # Changed from "dense"
dense_weight = 0.6
sparse_weight = 0.4         # Added BM25
RRF_scoring = True          # Reciprocal Rank Fusion
# All other params unchanged
\`\`\`

### Variant 1 Scorecard

| ID | Question | Faithfulness | Answer Relevance | Context Recall | Completeness | vs Baseline |
|----|----------|--------------|------------------|-----------------|--------------|------------|
| q01 | SLA P1? | 5/5 | 5/5 | 1.0 | 1.0 | ↔ Same |
| q02 | Refund? | 5/5 | 5/5 | 1.0 | 1.0 | ↔ Same |
| q03 | L3 approver? | 4/5 | 4/5 | 1.0 | 0.9 | ↑ +0.1 |
| q04 | ERR-403? | 4/5 | 5/5 | 1.0 | 0.9 | ↑ +1/5 |
| q05 | Leave? | 5/5 | 5/5 | 1.0 | 1.0 | ↔ Same |
| q06 | P1 vs P2? | 5/5 | 5/5 | 1.0 | 1.0 | ↔ Same |
| q07 | Request L2? | 4/5 | 4/5 | 1.0 | 0.8 | ↑ +2/5 ⭐ |
| q08 | After 35 days? | 5/5 | 5/5 | 1.0 | 1.0 | ↔ Same |
| q09 | IT L2 approve? | 4/5 | 5/5 | 1.0 | 1.0 | ↔ Same |
| q10 | Special leave? | 4/5 | 4/5 | 0.8 | 0.7 | ↑ +1/5 |

### Variant 1 Averages
- Faithfulness: 4.4/5 (**↑ +0.3**)
- Answer Relevance: 4.4/5 (**↑ +0.2**)
- Context Recall: 0.93/1.0 (**↑ +0.07**)
- Completeness: 0.94/1.0 (**↑ +0.09**)

### Analysis: Questions That Improved

**q07 (Request Level 2) — Key Improvement ⭐**
- Baseline Dense: Retrieved general IT docs, missed "form submission" details
  - Retrieved chunks: "Lorem ipsum IT general info..."
  - Context Recall: 0.5 (missed ~50% of expected info)
  
- Variant Hybrid: BM25 found "Submit form at" keyword, Dense found "Level 2 access" semantic
  - Retrieved chunks: "Submit form at [URL]" + "Level 2 requires approval from [role]"
  - Context Recall: 1.0 (found all expected sources)
  - Faithfulness: 2/5 → 4/5 (answer now grounded, complete)

**q04 (ERR-403) — Good Improvement**
- Baseline: Missed error-code section
- Variant: Hybrid BM25 found "ERR-403" keyword, returned error explanation + troubleshooting
- Improvement: 3/5 → 4/5 faithfulness, better completeness

**q10 (Special leave types) — Moderate Improvement**
- Baseline: Retrieved only 60% of special leave types
- Variant: BM25 keyword search for "sick", "parental", "sabbatical" found more sections
- Improvement: 3/5 → 4/5 faithfulness

### Conclusion

**Hybrid retrieval is BETTER than Dense for this corpus.** 
- ✓ Faithfulness improved by 0.3 points (+7%)
- ✓ Context Recall improved by 0.07 (+8%)
- ✓ Key questions (q04, q07) resolved
- ✓ No regression: all other questions maintained or improved

**Why:** This corpus mixes semantic queries (policy, SLA) with keyword lookups (error codes, form terms). Hybrid captures both.

---

## Tuning Summary

| Metric | Baseline | Variant 1 | Delta | Winner |
|--------|----------|-----------|-------|--------|
| Avg Faithfulness | 4.1 | 4.4 | +0.3 | ✓ Variant |
| Avg Answer Relevance | 4.2 | 4.4 | +0.2 | ✓ Variant |
| Avg Context Recall | 0.86 | 0.93 | +0.07 | ✓ Variant |
| Avg Completeness | 0.85 | 0.94 | +0.09 | ✓ Variant |
| Full (5/5+1.0+1.0) | 5/10 | 6/10 | +1 | ✓ Variant |

---

## Key Learnings

1. **Dense alone insufficient for mixed corpus**
   - Semantic embeddings good for natural language ("SLA policy")
   - Bad for exact keyword lookups ("ERR-403")

2. **Hybrid (RRF) is simple & effective**
   - Combining dense + BM25 scores via RRF formula
   - No extra latency, simple to implement

3. **Metadata crucial for citation**
   - "source" field enables exact citation format
   - User can trace answer back to document

4. **A/B rule matters**
   - Changed ONLY retrieval mode
   - Kept chunking, LLM, prompt same
   - Can attribute improvements directly to Hybrid

---

**Experiment conducted by:** [NAME]  
**Reviewed by:** [TECH LEAD]
```

### Task 3: Generate Output Files (5')

```bash
# After running eval.py, verify files created:

# 1. scorecard_baseline.md
cat results/scorecard_baseline.md

# 2. scorecard_variant.md
cat results/scorecard_variant.md

# 3. logs/grading_run.json
python -c "import json; d=json.load(open('logs/grading_run.json')); print(f'{len(d)} questions logged')"

# 4. Commit documentation
git add docs/architecture.md docs/tuning-log.md
git commit -m "Sprint 4: Complete architecture and tuning documentation

- architecture.md: chunking decision, metadata schema, retrieval config, pipeline diagram
- tuning-log.md: baseline vs variant comparison, analysis of improved questions"
```

---

## 📋 CHECKLIST — ĐẠT

### Sprint 1–2: Test Questions
- [ ] Tạo `data/test_questions.json` với 10 câu đa dạng
- [ ] Mỗi câu có: id, question, expected_answer, expected_sources, grading_criteria
- [ ] 10 câu phân bố: 2–3 refund, 2–3 SLA, 2–3 access, 1–2 error code, 1–2 HR
- [ ] JSON format valid (test `json.load()`)

### Sprint 3–4: Scoring Functions
- [ ] `score_faithfulness()` implemented (manual chấm first)
- [ ] `run_scorecard()` chạy được, return List[Dict] với metrics
- [ ] `compare_ab()` print bảng baseline vs variant rõ ràng

### Sprint 4: Documentation
- [ ] `docs/architecture.md` viết đầy đủ:
  - [ ] Chunking decision (size, overlap, strategy, lý do)
  - [ ] Metadata schema (source, section, effective_date, etc)
  - [ ] Retrieval config (baseline + variant)
  - [ ] Pipeline diagram (Mermaid hay ASCII)
- [ ] `docs/tuning-log.md` viết đầy đủ:
  - [ ] Baseline config + scorecard (4 metrics)
  - [ ] Variant config + scorecard
  - [ ] Analysis: questions improved/regressed, why
  - [ ] Kết luận: variant tốt hơn/kém hơn, bằng chứng
- [ ] `logs/grading_run.json` tạo được (10 câu)
- [ ] `results/scorecard_baseline.md` + `results/scorecard_variant.md` có số liệu

### Final Commit
- [ ] Tất cả files committed trước 18:00
- [ ] Commit message rõ ràng (reference architecture + tuning)

---

## 🚀 QUICK COMMAND

```bash
# Check test_questions format
python -c "
import json
with open('data/test_questions.json') as f:
    q = json.load(f)
print(f'{len(q)} questions')
for question in q[:2]:
    print(f'  {question[\"id\"]}: {question[\"question\"][:60]}...')
"

# Run evaluation (after Sprint 2 complete)
python eval.py

# View results
cat results/scorecard_baseline.md
cat results/scorecard_variant.md
```

---

**Chúc bạn hoàn thành xuất sắc! 🎯**
