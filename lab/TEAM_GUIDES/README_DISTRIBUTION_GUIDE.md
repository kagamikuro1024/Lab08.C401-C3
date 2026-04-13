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