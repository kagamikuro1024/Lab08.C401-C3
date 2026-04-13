# 🎯 HƯỚNG DẪN CHI TIẾT — MINH (QA & Environment)

**Vai trò:** QA Lead & Environment Engineer  
**Trách nhiệm:** Setup, testing, final QC, docs, help team write reports  
**Điểm chịu trách nhiệm:** Code stability, dependencies, final validation

---

## 📋 TÓM TẮT CÔNG VIỆC

| Sprint | Công việc chính | File chính | Timeline |
|--------|-----------------|-----------|----------|
| **Prep (T-15')** | Setup environment | `requirements.txt`, `.env` | 10' |
| **1–4** | Monitor build status | All `.py` | Throughout |
| **4** | Final QC before commit | All files | 30' |
| **After 18:00** | Help write individual reports | `reports/individual/` | 60' |

---

## 🔧 SPRINT PREP (15 phút trước bắt đầu)

### Task 1: Install Dependencies (5')

**File:** `lab/requirements.txt` (đã có)

```bash
cd lab

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/Scripts/activate  # Windows
# OR
source venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "chromadb|rank-bm25|sentence-transformers|openai"

# Expected output:
# chromadb                           0.5.x
# rank-bm25                          0.2.2
# sentence-transformers              2.7.x
# openai                             1.x
# google-generativeai                0.5.x
```

### Task 2: Setup Environment Variables (5')

**File:** `lab/.env` (create from `.env.example`)

```bash
# Copy template
cp .env.example .env

# Edit .env with your editor (VSCode, nano, etc)
# Add ONE of these:

# Option A: OpenAI
OPENAI_API_KEY=sk-proj-xxxxx...
LLM_MODEL=gpt-4o-mini

# Option B: Google Gemini
GOOGLE_API_KEY=AIzaSyxxx...
LLM_MODEL=gemini-1.5-flash

# Note: For embedding, we're using Sentence Transformers (local, no API key)
```

### Task 3: Verify Setup (5')

```bash
python -c "
import chromadb
import rank_bm25
from sentence_transformers import SentenceTransformer
import openai

print('✓ chromadb imported')
print('✓ rank_bm25 imported')
print('✓ sentence-transformers imported')
print('✓ openai imported')

# Test embedding model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embedding = model.encode('test')
print(f'✓ Embedding model loaded (dimension: {len(embedding)})')

# Test API key
import os
key = os.getenv('OPENAI_API_KEY')
if key:
    print('✓ OPENAI_API_KEY found')
else:
    print('⚠ OPENAI_API_KEY not found (will fail if LLM called)')
"
```

**Expected output:**
```
✓ chromadb imported
✓ rank_bm25 imported
✓ sentence-transformers imported
✓ openai imported
✓ Embedding model loaded (dimension: 384)
✓ OPENAI_API_KEY found
```

---

## 🚀 SPRINTS 1–4: CONTINUOUS MONITORING

### Your Role Each Sprint

After each sprint, run this validation:

```bash
#!/bin/bash
# save as qa_check.sh

echo "=== QA CHECK SPRINT $1 ==="

# Syntax check
echo "[1/5] Checking Python syntax..."
python -m py_compile index.py rag_answer.py eval.py 2>/dev/null && echo "  ✓ No syntax errors" || echo "  ❌ SYNTAX ERROR"

# Import check
echo "[2/5] Checking imports..."
python -c "import index; import rag_answer; import eval" 2>/dev/null && echo "  ✓ All modules importable" || echo "  ❌ IMPORT ERROR"

# File structure check
echo "[3/5] Checking file structure..."
[ -f "data/test_questions.json" ] && echo "  ✓ test_questions.json exists" || echo "  ⚠ Missing test_questions.json"
[ -d "chroma_db" ] && echo "  ✓ ChromaDB folder exists" || echo "  ⚠ Missing chroma_db"
[ -d "logs" ] && echo "  ✓ logs folder exists" || echo "  ⚠ Missing logs folder"
[ -d "results" ] && echo "  ✓ results folder exists" || echo "  ⚠ Missing results folder"

# Dependencies check
echo "[4/5] Checking key dependencies..."
pip show chromadb > /dev/null && echo "  ✓ chromadb installed" || echo "  ❌ chromadb missing"
pip show rank-bm25 > /dev/null && echo "  ✓ rank-bm25 installed" || echo "  ❌ rank-bm25 missing"
pip show sentence-transformers > /dev/null && echo "  ✓ sentence-transformers installed" || echo "  ❌ sentence-transformers missing"

# .env check
echo "[5/5] Checking environment variables..."
grep -q "OPENAI_API_KEY" .env 2>/dev/null && echo "  ✓ OPENAI_API_KEY configured" || echo "  ⚠ OPENAI_API_KEY not found"

echo ""
echo "=== QA CHECK COMPLETE ==="
```

**Usage:**
```bash
bash qa_check.sh 1   # After Sprint 1
bash qa_check.sh 2   # After Sprint 2
bash qa_check.sh 3   # After Sprint 3
bash qa_check.sh 4   # After Sprint 4
```

---

## 🎯 SPRINT 4: FINAL QC (30 phút cuối)

### Task 1: Full End-to-End Test (10')

```bash
echo "=== FULL END-TO-END TEST ==="

# 1. Rebuild index
echo "[1/3] Running: python index.py"
timeout 120 python index.py
if [ $? -eq 0 ]; then
    echo "  ✓ Index build successful"
else
    echo "  ❌ Index build FAILED"
    exit 1
fi

# 2. Test retrieval + generation
echo "[2/3] Running: python rag_answer.py sample test"
python -c "
from rag_answer import rag_answer
result = rag_answer('SLA P1?')
assert result['answer'], 'Empty answer'
assert result['sources'], 'No sources'
print('  ✓ RAG pipeline works')
" || {
    echo "  ❌ RAG pipeline FAILED"
    exit 1
}

# 3. Test evaluation
echo "[3/3] Running: python eval.py"
timeout 300 python eval.py
if [ $? -eq 0 ]; then
    echo "  ✓ Evaluation successful"
else
    echo "  ❌ Evaluation FAILED"
    exit 1
fi

echo "✓ END-TO-END TEST PASSED"
```

### Task 2: File Structure Final Check (5')

```bash
echo "=== DELIVERABLES CHECKLIST ==="

# Code files (must exist & no syntax errors)
FILES=(
    "index.py"
    "rag_answer.py"
    "eval.py"
    "data/test_questions.json"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        python -m py_compile "$file" 2>/dev/null && echo "✓ $file" || echo "❌ $file (syntax error)"
    else
        echo "❌ $file (missing)"
    fi
done

# Output files (should exist by now)
OUTPUTS=(
    "logs/grading_run.json"
    "results/scorecard_baseline.md"
    "results/scorecard_variant.md"
    "docs/architecture.md"
    "docs/tuning-log.md"
)

for file in "${OUTPUTS[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "⚠ $file (missing - will be created by eval.py)"
    fi
done

echo ""
echo "=== FILE STRUCTURE READY FOR COMMIT ==="
```

### Task 3: JSON Validation (5')

```bash
echo "=== JSON VALIDATION ==="

# Validate test_questions.json
python -c "
import json
with open('data/test_questions.json') as f:
    questions = json.load(f)
required_keys = ['id', 'question', 'expected_answer', 'expected_sources', 'grading_criteria']
for q in questions:
    for key in required_keys:
        assert key in q, f'Missing key {key} in {q[\"id\"]}'
print(f'✓ test_questions.json valid ({len(questions)} questions)')
"

# Validate grading_run.json
if [ -f "logs/grading_run.json" ]; then
    python -c "
import json
with open('logs/grading_run.json') as f:
    log = json.load(f)
assert isinstance(log, list), 'Log should be a list'
assert len(log) == 10, f'Expected 10 questions, got {len(log)}'
required_keys = ['id', 'question', 'answer', 'sources']
for entry in log:
    for key in required_keys:
        assert key in entry, f'Missing key {key}'
print(f'✓ grading_run.json valid ({len(log)} entries)')
"
fi

echo "=== JSON VALIDATION COMPLETE ==="
```

### Task 4: Final Commit Preparation (10')

```bash
echo "=== PREPARING FINAL COMMIT ==="

# 1. Check git status
git status

# 2. Add all changes
git add -A

# 3. Verify what will be committed
git diff --staged --stat

# 4. Commit (Trung runs this before 18:00)
# (Don't run yet, just show command)
echo "
When ready, run:

git commit -m \"Day 08 Lab: Complete RAG Pipeline with Hybrid Retrieval

- Sprint 1: Indexing with section-based chunking (400 tokens, 80 overlap)
- Sprint 2: Baseline dense retrieval + grounded answer generation
- Sprint 3: Hybrid retrieval variant (BM25 + Dense, RRF fusion) shows +0.3 improvement
- Sprint 4: Evaluation on 10 test questions, architecture & tuning docs

Deliverables:
- Code: index.py, rag_answer.py, eval.py (all executable)
- Data: data/test_questions.json with 10 diverse questions
- Logs: logs/grading_run.json with pipeline output
- Docs: docs/architecture.md (5pt), docs/tuning-log.md (5pt)
- Results: results/scorecard_baseline.md, results/scorecard_variant.md

All tests passing. Ready for evaluation.\"

git push origin master
"
```

---

## 📋 REPORTS WRITING (After 18:00)

Your role: Help everyone write individual reports + coordinate group report.

### Template Structure (for each person)

**File:** `reports/individual/[ten].md`

```markdown
# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** [NAME]  
**Vai trò trong nhóm:** [ROLE]  
**Ngày nộp:** [DATE]  
**Độ dài:** 500–800 từ

---

## 1. Tôi đã làm gì trong lab này? (100–150 từ)

> Mô tả cụ thể phần bạn đóng góp:
> - Sprint nào? Implement cái gì?
> - Code/task cụ thể?
> - Kết nối với work của người khác?

Example (Trung):
Tôi là Tech Lead, chịu trách nhiệm quản lý sprint và nối code end-to-end. 
Sprint 1, tôi implement `preprocess_document()` và `chunk_document()` cho index.py, 
quyết định chunk_size=400 tokens với section-based strategy để tránh cắt gớt chính sách. 
Sprint 2, implement `retrieve_dense()` query ChromaDB theo cosine similarity. 
Sprint 3, quyết định chọn hybrid variant (dense 0.6 + BM25 0.4) vì corpus có cả semantic và keyword,
implement RRF fusion. Sprint 4, QC end-to-end test trước commit deadline 18:00.

---

## 2. Điều tôi hiểu rõ hơn? (100–150 từ)

> 1–2 concept từ bài học mà bạn thực sự hiểu sau khi làm lab.
> Giải thích bằng ngôn ngữ của bạn.

Example (Vinh):
Tôi hiểu rõ hơn sự khác biệt giữa dense vs sparse retrieval. Dense dùng semantic embedding,
tốt cho câu tự nhiên ("SLA response time") nhưng kém với keyword lookups ("ERR-403").
Sparse (BM25) là ngược lại. Hybrid RRF kết hợp rank từ 2 nguồn, không cần normalize score khác scale.
Implement BM25, tôi thấy việc token matching chính xác so với embedding vector rất khác biệt.

---

## 3. Khó khăn gặp phải? (100–150 từ)

> Điều gì không tính toán được? Lỗi nào mất thời gian debug?

Example (Nghĩa):
Ban đầu tôi dùng temperature=1.0 (random sampling) cho LLM, kết quả mỗi lần chạy khác nhau,
khiến evaluation không consistent. Debug mất 15 phút mới phát hiện. Sau đó đổi temperature=0,
tất cả answer trở nên deterministic. Cũng gặp issue citation format: LLM create [5] 
khi chỉ có 3 chunks → phải ép prompt "cite as [1], [2], [3] ONLY".

---

## 4. Phân tích 1 câu test (150–200 từ)

> Chọn 1 câu từ test_questions.json, phân tích:
> - Baseline trả lời sao?
> - Lỗi ở tâng nào (index/retrieval/gen)?
> - Variant cải thiện không?

Example (Đạt):
Câu q07: "Làm sao request Level 2 access?" Baseline dense retrieval trả về general IT docs,
miss "Submit form at [URL]" details. Context Recall = 0.5 (thiếu 50% expected info).
Faithfulness = 2/5 vì answer không mention form submission steps.

Lỗi ở retrieval layer: dense embedding match semantic "access request" nhưng miss
keyword "form submission". 

Variant hybrid: BM25 tìm "request", "form" keywords → tìm thêm được access_control_sop section 
về "Submit form". Context Recall jumped 0.5 → 1.0 (found all expected sources).
Faithfulness 2/5 → 4/5 (answer now grounded với form + approval steps).

Kết luận: Hybrid fixed q07 vì corpus có cả semantic + keyword queries.

---

## 5. Nếu có thêm thời gian? (50–100 từ)

> 1–2 cải tiến cụ thể (không "làm tốt hơn chung chung").

Example (Minh):
1. Implement LLM-as-Judge để auto-chấm faithfulness thay thủ công.
2. Thêm query expansion: "Level 2" → ["Level 2", "L2", "Level-2"] để catch alias, 
   improve recall ~5–10%.

---
```

### Task: Coordinate Group Report (30')

**File:** `reports/group_report.md`

```markdown
# Báo Cáo Nhóm — Lab Day 08: RAG Pipeline

**Nhóm:** Trung, Đạt, Nghĩa, Vinh, Minh  
**Ngày nộp:** [DATE]

---

## 1. Pipeline Overview

[Tóm tắt 1 trang về:
- Bối cảnh: internal assistant cho CS/IT/HR
- 4 sprints, 4 giờ
- Kết quả: RAG pipeline working, hybrid variant chosen]

## 2. Architecture Decision

[Từ docs/architecture.md, highlight:
- Chunk: 400 tokens, section-based, 3 metadata fields
- Baseline: Dense embedding search (cosine similarity)
- Variant: Hybrid RRF (60% dense, 40% BM25)]

## 3. Tuning & Results

[Từ docs/tuning-log.md:
- Baseline scores: Faithfulness 4.1/5, Recall 0.86/1.0
- Variant scores: Faithfulness 4.4/5, Recall 0.93/1.0
- Improvement: +0.3 faithfulness, +0.07 recall
- Key insight: Hybrid finds error codes (ERR-403) + semantic matches (SLA policy)]

## 4. Challenges & Solutions

[Challenges faced + how we fixed them]

## 5. Lessons Learned

[Top 3 insights from the lab]

---
```

### Help Each Team Member

Tạo một template cho mỗi người, guide họ qua 5 sections, ensure 500–800 từ.

```bash
# Create template files for each person
cat > reports/individual/TEMPLATE_DAT.md << 'EOF'
# Báo Cáo Cá Nhân — Lab Day 08 (ĐẠT)

**Vai trò:** Eval Owner & Documentation Lead

## 1. Công việc của bạn

(Viết đây giúp bạn:
- Implement test_questions.json: 10 câu test
- Implement run_scorecard(), compare_ab()
- Viết architecture.md + tuning-log.md)

## 2. Điều học được

(Ví dụ: Cách thiết kế evaluation framework, metrics selection)

## 3. Khó khăn

(Ví dụ: Manual scoring vs LLM-as-Judge tradeoff)

## 4. Phân tích 1 câu

(Chọn q07, explain context recall jump 0.5 → 1.0 with hybrid)

## 5. Next steps

(Ví dụ: Auto LLM evaluation)

EOF

# Repeat for others: TEMPLATE_TRUNG, TEMPLATE_NGHIA, TEMPLATE_VINH, TEMPLATE_MINH
```

---

## ✅ FINAL CHECKLIST — MINH

### Prep Phase (T-15 phút)
- [ ] `pip install -r requirements.txt` succeeds
- [ ] `.env` created with OPENAI_API_KEY (or GOOGLE_API_KEY)
- [ ] `python -c "import chromadb; ..."` shows all imports OK
- [ ] Virtual env activated (optional but recommended)

### Throughout Sprints 1–4
- [ ] After each sprint, run `bash qa_check.sh [sprint_number]`
- [ ] Monitor team's progress via `git log`
- [ ] Alert team if syntax/import errors appear
- [ ] Keep `.gitignore` clean (no `__pycache__`, `*.pyc`, `.env` secrets)

### Sprint 4 Final Phase (30 min before 18:00)
- [ ] Run full end-to-end test: index.py → rag_answer.py → eval.py
- [ ] Verify all deliverable files exist:
  - [ ] Code: index.py, rag_answer.py, eval.py
  - [ ] Data: data/test_questions.json
  - [ ] Logs: logs/grading_run.json
  - [ ] Results: results/scorecard_baseline.md, scorecard_variant.md
  - [ ] Docs: docs/architecture.md, docs/tuning-log.md
- [ ] JSON validation: test_questions.json + grading_run.json
- [ ] ALL files syntax-checked, no errors
- [ ] Final commit prepared (Trung runs before 18:00)

### Post 18:00: Reports
- [ ] Group report template created
- [ ] Each team member assigned 1 template
- [ ] Individual reports guide shared
- [ ] Collected & reviewed before final submission

### Git Hygiene
- [ ] No `.env` secrets committed
- [ ] No `chroma_db/` with huge vectors (too large)
- [ ] `.gitignore` includes: `*.pyc`, `__pycache__/`, `.env`, `venv/`
- [ ] Commit messages clear & descriptive

---

## 🚀 QUICK COMMAND REFERENCE

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key

# Verify setup
python -c "import chromadb, rank_bm25, sentence_transformers, openai; print('✓ All imports OK')"

# Run end-to-end test
python index.py && python rag_answer.py && python eval.py

# Check files
ls -la logs/grading_run.json results/scorecard_*.md docs/*.md

# Validate JSON
python -c "import json; json.load(open('logs/grading_run.json')); print('✓ Valid')"

# Commit
git add -A
git commit -m "Day 08 Lab: Complete RAG Pipeline"
git push origin master
```

---

## 📌 IMPORTANT NOTES FOR MINH

1. **You're the gatekeeper** — No commit before 18:00 unless everything passes QC
2. **Be vigilant about errors** — Catch syntax/import issues ASAP, don't let them accumulate
3. **Help with reports** — Make sure each person writes 500–800 words, follow template
4. **Document issues** — Keep a log of problems encountered + solutions for future reference
5. **Celebrate! 🎉** — After commit, your RAG pipeline is DONE!

---

**Chúc bạn quản lý xuất sắc! 🎯**
