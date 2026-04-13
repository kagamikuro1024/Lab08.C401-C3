# 📂 TEAM GUIDES — CẤU TRÚC & HƯỚNG DẪN PHÂN PHỐI

**Tạo bởi:** Copilot AI Assistant  
**Cho:** Trung, Đạt, Nghĩa, Vinh, Minh (Lab Day 08 Group)

---

## 📁 Cấu Trúc Thư Mục

```
lab/
├── TEAM_GUIDES/                           ← Folder này (toàn bộ hướng dẫn)
│   ├── TRUNG_TechLead/
│   │   ├── TRUNG_GUIDE.md                 ← Detail chi tiết pour Trung
│   │   └── TRUNG_END_TO_END_GUIDE.md      ← End-to-end + reports guide
│   ├── DAT_EvalOwner/
│   │   └── DAT_GUIDE.md                   ← Detail chi tiết pour Đạt
│   ├── NGHIA_LLM/
│   │   └── NGHIA_GUIDE.md                 ← Detail chi tiết pour Nghĩa
│   ├── VINH_Retrieval/
│   │   └── VINH_GUIDE.md                  ← Detail chi tiết pour Vinh
│   ├── MINH_QA/
│   │   └── MINH_GUIDE.md                  ← Detail chi tiết pour Minh
│   └── README.md (file này)               ← Overview & distribution
│
├── GROUP_PLAN.md                          ← Group plan chi tiết (tạo trước)
├── index.py                               ← Trung implement
├── rag_answer.py                          ← Trung + Nghĩa + Vinh implement
├── eval.py                                ← Đạt implement
├── requirements.txt
├── .env.example
├── data/
│   ├── docs/ (5 files)
│   └── test_questions.json                ← Đạt tạo
├── logs/
│   └── grading_run.json                   ← Auto-generate from eval.py
├── results/
│   ├── scorecard_baseline.md              ← Auto-generate
│   └── scorecard_variant.md               ← Auto-generate
├── docs/
│   ├── architecture.md                    ← Đạt viết
│   └── tuning-log.md                      ← Đạt viết
└── reports/
    ├── group_report.md                    ← Trung viết (after 18:00)
    └── individual/
        ├── trung.md                       ← Trung viết (after 18:00)
        ├── dat.md                         ← Đạt viết (after 18:00)
        ├── nghia.md                       ← Nghĩa viết (after 18:00)
        ├── vinh.md                        ← Vinh viết (after 18:00)
        └── minh.md                        ← Minh viết (after 18:00)
```

---

## 🎯 CÁCH PHÂN PHỐI & SỬ DỤNG

### Cho Trung (Tech Lead)

**Bạn cần đọc:**
1. ✅ `GROUP_PLAN.md` (đã read)
2. ✅ `TEAM_GUIDES/TRUNG_TechLead/TRUNG_GUIDE.md` ← chi tiết implement mỗi sprint
3. ✅ `TEAM_GUIDES/TRUNG_TechLead/TRUNG_END_TO_END_GUIDE.md` ← end-to-end + báo cáo

**Nhiệm vụ:**
- Manage 4 sprints (60' each)
- Implement core logic: preprocess, chunk, retrieve_dense, retrieve_hybrid
- Ensure code chạy end-to-end sau mỗi sprint
- Commit trước 18:00
- Viết group report + hướng dẫn cá nhân sau 18:00

**Cách dùng:**
```bash
# Sprint 1
cat TEAM_GUIDES/TRUNG_TechLead/TRUNG_GUIDE.md | head -150
# → Làm theo section "SPRINT 1"

# Sprint 2–4
# → Tiếp tục các section tiếp theo

# Cuối cùng
cat TEAM_GUIDES/TRUNG_TechLead/TRUNG_END_TO_END_GUIDE.md
# → Hướng dẫn chạy end-to-end + viết báo cáo
```

---

### Cho Đạt (Eval Owner)

**Bạn cần đọc:**
- `TEAM_GUIDES/DAT_EvalOwner/DAT_GUIDE.md` ← toàn bộ hướng dẫn

**Nhiệm vụ:**
- Sprint 1–2: Tạo test_questions.json (10 câu)
- Sprint 3–4: Implement scoring functions, write docs
- Generate scorecard files + logs

**Cách dùng:**
```bash
cat TEAM_GUIDES/DAT_EvalOwner/DAT_GUIDE.md
# → Follow các task: test_questions → scoring → docs
```

---

### Cho Nghĩa (LLM Engineer)

**Bạn cần đọc:**
- `TEAM_GUIDES/NGHIA_LLM/NGHIA_GUIDE.md` ← toàn bộ hướng dẫn

**Nhiệm vụ:**
- Setup .env, test API
- Implement call_llm(), optimize prompt
- Ensure grounding & abstain

**Cách dùng:**
```bash
cat TEAM_GUIDES/NGHIA_LLM/NGHIA_GUIDE.md
# → Follow: Setup → implement call_llm() → optimize prompt
```

---

### Cho Vinh (Retrieval Specialist)

**Bạn cần đọc:**
- `TEAM_GUIDES/VINH_Retrieval/VINH_GUIDE.md` ← toàn bộ hướng dẫn

**Nhiệm vụ:**
- Audit chunking quality
- Implement retrieve_sparse (BM25)
- Implement retrieve_hybrid (RRF)
- Test & compare baseline vs variant

**Cách dùng:**
```bash
cat TEAM_GUIDES/VINH_Retrieval/VINH_GUIDE.md
# → Follow: Chunk audit → BM25 → RRF → testing
```

---

### Cho Minh (QA Lead)

**Bạn cần đọc:**
- `TEAM_GUIDES/MINH_QA/MINH_GUIDE.md` ← toàn bộ hướng dẫn

**Nhiệm vụ:**
- Setup environment
- Monitor build throughout sprints
- Final QC before commit
- Help write individual reports

**Cách dùng:**
```bash
cat TEAM_GUIDES/MINH_QA/MINH_GUIDE.md
# → Follow: Setup → monitoring → QC → reports help
```

---

## 🚀 QUICK START (Trung làm ngay)

### 1. Gửi guides cho team (5 phút)

```bash
# Mỗi người check folder của mình:

# Đạt:
cat TEAM_GUIDES/DAT_EvalOwner/DAT_GUIDE.md | head -50

# Nghĩa:
cat TEAM_GUIDES/NGHIA_LLM/NGHIA_GUIDE.md | head -50

# Vinh:
cat TEAM_GUIDES/VINH_Retrieval/VINH_GUIDE.md | head -50

# Minh:
cat TEAM_GUIDES/MINH_QA/MINH_GUIDE.md | head -50
```

### 2. Read GROUP_PLAN.md + Your Personal GUIDE (10 phút)

Mỗi người:
1. Read `GROUP_PLAN.md` → hiểu timeline overall
2. Read guide của mình → hiểu chi tiết task

### 3. Kick-off (5 phút)

```
Trung: "Mỗi người đã read guide chưa? Có câu hỏi gì không?"
(Wait for yes)

"OK, giờ bắt đầu Sprint 1. Trung + Vinh quản lý chunking.
 Đạt, chuẩn bị data. Nghĩa, setup LLM. Minh, monitor.
 4 giờ nữa có deadline 18:00. Let's GO! 🚀"
```

### 4. Execute Sprints

**Follow timeline:**
- Sprint 1 (00:00–01:00): Trung implement index.py
- Sprint 2 (01:00–02:00): Trung + Nghĩa implement rag_answer.py
- Sprint 3 (02:00–03:00): Trung + Vinh implement hybrid
- Sprint 4 (03:00–04:00): Đạt eval.py, Trung coordinate, Minh QC

### 5. Post 18:00: Reports

Follow `TRUNG_END_TO_END_GUIDE.md` section "WRITE REPORTS"

```bash
# Trung viết group report
cat TEAM_GUIDES/TRUNG_TechLead/TRUNG_END_TO_END_GUIDE.md | grep -A 50 "WRITE REPORTS"

# Guide từng người viết individual report
```

---

## 📝 TEMPLATES INSIDE EACH GUIDE

### TRUNG_GUIDE.md

```
├── SPRINT 1–4 detailed breakdown
├── Code checklist cho mỗi sprint
├── Expected output examples
├── Commit commands
└── Quick reference
```

### DAT_GUIDE.md

```
├── Test questions format + examples
├── Scoring functions implementation
├── Documentation templates (architecture.md, tuning-log.md)
├── JSON validation
└── Submission checklist
```

### NGHIA_GUIDE.md

```
├── .env setup
├── API key test
├── call_llm() implementation
├── Prompt engineering tips
├── Generation quality checks
└── Troubleshooting
```

### VINH_GUIDE.md

```
├── Chunk quality audit
├── retrieve_sparse (BM25) implementation
├── retrieve_hybrid (RRF) implementation
├── Testing procedures
├── BM25 explanation + examples
└── Metrics monitoring
```

### MINH_GUIDE.md

```
├── Environment setup
├── Continuous monitoring
├── Final QC checklist
├── JSON validation
├── Reports writing guidance
└── Team troubleshooting
```

### TRUNG_END_TO_END_GUIDE.md

```
├── 4 phases (Sprint 1–4)
├── Timeline + checkpoints
├── Code checklists
├── Test cases
├── Expected outputs
├── Reports templates
├── Key commands
└── Appendix: help teammates
```

---

## 💡 TIPS FOR SUCCESS

### 1. **Parallel Execution When Possible**

```
Sprint 1–2: Parallel
  - Trung: implement index.py (Sprint 1) + retrieve_dense (Sprint 2)
  - Nghĩa: setup LLM env (Sprint 1–2) + call_llm (Sprint 2)
  - Đạt: prepare test_questions.json (Sprint 1–2)
  - Vinh: audit chunks (Sprint 1–2)
  - Minh: setup environment (Sprint 1)

Sprint 3: Sequential
  - Vinh: implement BM25
  - Trung: implement RRF fusion (after BM25 ready)
  - Test & compare

Sprint 4: Sequential
  - eval.py must wait for everything else (Sprint 1–3)
```

### 2. **Communication Between Team Members**

```
Each sprint end:
- Trung: "Can you test my code? Is output correct?"
- Vinh: "Chunks look good? Any issues?"
- Nghĩa: "LLM working? Citations correct?"
- Đạt: "Test questions ready? Scoring functions?"
- Minh: "Everything still working? Any errors?"
```

### 3. **Backup Plans**

```
If retrieve_sparse fails:
  → Skip BM25, use pure dense (lose 0.3 points, still passing)

If LLM API times out:
  → Use cached responses from earlier tests
  → Or fallback to simple string generation

If eval.py breaks:
  → Run manual scoring, document in results
  → Better than no scorecard at all
```

### 4. **Keep Git Clean**

```bash
# After each sprint:
git add -A
git commit -m "Sprint X: [task] - [status]"
git push origin master

# If mistake:
git log --oneline  # Check history
git revert HEAD    # Undo last commit
```

---

## 📞 EMERGENCY CONTACTS (During Lab)

If something breaks:

### Retrieval Error
→ Contact: **Vinh** (chunk quality) or **Trung** (ChromaDB query)

### LLM Error
→ Contact: **Nghĩa** (API key, temperature)

### Evaluation Error
→ Contact: **Đạt** (test_questions format, scoring)

### Environment Error
→ Contact: **Minh** (dependencies, imports)

### Stuck on Timeline
→ Contact: **Trung** (reallocate tasks, prioritize)

---

## 🎯 SUCCESS CRITERIA

By 18:00 on Day 8:

✅ All 3 Python files run without error
✅ ChromaDB index created (45 chunks)
✅ RAG pipeline returns cited answers
✅ Hybrid variant tested & compared to baseline
✅ 10 test questions scored
✅ architecture.md + tuning-log.md written
✅ logs/grading_run.json auto-generated
✅ Results scorecard files created
✅ ALL COMMITTED BEFORE 18:00

After 18:00:
✅ Group report written
✅ 5 individual reports (500–800 words each)
✅ Ready for submission

---

## 🚀 FINAL WORDS

> **This is your comprehensive guide. Everything you need is here.**
>
> - **Trung:** You have detailed sprints + end-to-end guide + report templates
> - **Đạt:** You have test quesitons + scoring + docs templates
> - **Nghĩa:** You have LLM setup + prompt engineering guide
> - **Vinh:** You have retrieval implementation + testing guide
> - **Minh:** You have environment setup + QC guide + reports help
>
> **No guessing. Just follow your guide.**
>
> **Timeline is tight but doable: 4 hours = 4 sprints × 60 minutes.**
>
> **You've got this! 💪**

---

## 📚 REFERENCE

**Files in TEAM_GUIDES/**
- TRUNG_TechLead/
  - TRUNG_GUIDE.md (Sprint implementation details)
  - TRUNG_END_TO_END_GUIDE.md (Full pipeline + reports)
  
- DAT_EvalOwner/
  - DAT_GUIDE.md (test_questions + scoring + docs)
  
- NGHIA_LLM/
  - NGHIA_GUIDE.md (LLM setup + prompt + generation)
  
- VINH_Retrieval/
  - VINH_GUIDE.md (Chunking + BM25 + RRF + testing)
  
- MINH_QA/
  - MINH_GUIDE.md (Environment + QC + reports help)

**Master Document in lab/**
- GROUP_PLAN.md (Overall timeline + scoring + checklist)

---

**Created:** April 13, 2026  
**Last Updated:** Today  
**Status:** 🟢 Ready to Execute

---

## 🎉 LET'S GO!

```
4 giờ, 5 người, 1 mục tiêu:
Build a working RAG system 
that answers questions with evidence.

Sprints: 1️⃣ Index → 2️⃣ Retrieve → 3️⃣ Variant → 4️⃣ Evaluate

Timeline: 00:00 → 04:00 (then reports 04:00+ → 18:00)

Deadline: 18:00 COMMIT ✅

Giờ bắt đầu! 🚀
```

---

**Mọi thắc mắc, refer vào guide của bạn. Mọi issue, report cho Trung. Let's build! 🎯**
