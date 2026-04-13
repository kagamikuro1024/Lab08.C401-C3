# 🎯 HƯỚNG DẪN CHI TIẾT — NGHĨA (LLM & Prompt Engineering)

**Vai trò:** LLM & Prompt Engineering Lead  
**Trách nhiệm:** Implement `call_llm()`, tối ưu prompt, test generation quality  
**Điểm chịu trách nhiệm:** Sprint 2 generation + Sprint 3 prompt tuning (embedded trong Trung's 10 điểm)

---

## 📋 TÓM TẮT CÔNG VIỆC

| Sprint | Công việc chính | File chính | Timeline |
|--------|-----------------|-----------|----------|
| **Chuẩn bị** | Setup `.env`, test API key | `.env` | T-5 phút |
| **2** | Implement `call_llm()` | `rag_answer.py` L~293 | 15 phút |
| **2** | Optimize `build_grounded_prompt()` | `rag_answer.py` L~264 | 15 phút |
| **2** | Test generation on 5 queries | `rag_answer.py` main | 10 phút |
| **3–4** | (Light) prompt tweaking if needed | `rag_answer.py` | 5 phút |

---

## 🔧 CHUẨN BỊ — SETUP LLM (5 phút)

### Step 1: Tạo `.env` file

**File:** `lab/.env` (tạo từ `.env.example`)

```bash
# Option A: OpenAI API
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
LLM_MODEL=gpt-4o-mini
LLM_PROVIDER=openai

# Option B: Google Gemini (alternative)
# GOOGLE_API_KEY=AIzaSyCA...
# LLM_MODEL=gemini-1.5-flash
# LLM_PROVIDER=google
```

### Step 2: Test API connection

```bash
python -c "
from openai import OpenAI
import os

key = os.getenv('OPENAI_API_KEY')
if not key:
    print('ERROR: OPENAI_API_KEY not set in .env')
    exit(1)

client = OpenAI(api_key=key)
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': 'Hello'}],
    max_tokens=10
)
print('✓ API connection successful')
print(f'  Response: {response.choices[0].message.content}')
"
```

**Expected output:**
```
✓ API connection successful
  Response: Hello! How can I help you today?
```

---

## 🚀 SPRINT 2: IMPLEMENT LLM GENERATION

### Task 1: Implement `build_grounded_prompt()` (15')

**File:** `lab/rag_answer.py` (Line ~264)

```python
def build_grounded_prompt(query: str, context_block: str) -> str:
    """
    Xây dựng prompt ép LLM trả lời từ context, không bịa.
    
    Key rules:
    1. "Answer ONLY from context" — ép LLM không dùng background knowledge
    2. "If insufficient, say 'Không đủ dữ liệu'" — abstain, không bịa
    3. Cite sources [1], [2] — format rõ ràng
    4. Keep short — tránh LLM dài dòng, "lost in the middle"
    
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are a helpful company assistant that answers questions based ONLY on provided context.

**CRITICAL RULES:**
1. Answer ONLY using information from the Context below.
2. Do NOT use your general knowledge or make assumptions.
3. If the Context does NOT contain enough information to answer, respond with exactly: "Không đủ dữ liệu."
4. When using information from Context, cite the source using format [1], [2], etc.
5. Keep your answer concise (1-3 sentences), clear, and factual.

**Question:** {query}

**Context:**
{context_block}

**Answer:**"""
    
    return prompt

# Expected prompt output (example):
"""
You are a helpful company assistant that answers questions based ONLY on provided context.

**CRITICAL RULES:**
1. Answer ONLY using information from the Context below.
2. Do NOT use your general knowledge or make assumptions.
3. If the Context does NOT contain enough information to answer, respond with exactly: "Không đủ dữ liệu."
4. When using information from Context, cite the source using format [1], [2], etc.
5. Keep your answer concise (1-3 sentences), clear, and factual.

**Question:** SLA xử lý ticket P1 là bao lâu?

**Context:**
[1] sla_p1_2026.txt | P1 SLA Metrics | score=0.92
P1 tickets require 15-minute response time and 4-hour resolution time SLA.

[2] sla_p1_2026.txt | P1 Escalation | score=0.85
If P1 cannot be resolved within 4 hours, escalate to Level 2 support team.

**Answer:**
"""
```

### Task 2: Implement `call_llm()` (15')

**File:** `lab/rag_answer.py` (Line ~293)

```python
def call_llm(prompt: str) -> str:
    """
    Call LLM with grounded prompt, return answer.
    
    Args:
        prompt: Formatted prompt từ build_grounded_prompt()
    
    Returns:
        str: LLM output (answer text)
    """
    from openai import OpenAI
    import os
    
    # 1. Initialize LLM client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in .env")
    
    client = OpenAI(api_key=api_key)
    
    # 2. Call LLM
    response = client.chat.completions.create(
        model=LLM_MODEL,  # "gpt-4o-mini" from config
        messages=[
            {
                "role": "system",
                "content": "You are a factual company assistant. Answer only from provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,      # IMPORTANT: Deterministic output for evaluation
        max_tokens=512,     # Limit output length
        top_p=1.0           # Use default nucleus sampling
    )
    
    # 3. Extract answer
    answer = response.choices[0].message.content.strip()
    
    return answer

# Expected output examples:
# Input: Q about SLA P1
# Output: "Theo tài liệu [1], P1 tickets yêu cầu phản hồi trong 15 phút và xử lý trong 4 giờ."

# Input: Q out of domain (ERR-404-NOTFOUND)
# Output: "Không đủ dữ liệu."
```

### Task 3: Test generation on 5 sample queries (10')

**Add to `rag_answer.py` main():**

```python
if __name__ == "__main__":
    print("="*80)
    print("TESTING GENERATION (Sprint 2)")
    print("="*80)
    
    test_queries = [
        # Test 1: Clear factual — should have citation
        "SLA xử lý ticket P1 là bao lâu?",
        
        # Test 2: Policy question
        "Khách hàng có thể yêu cầu hoàn tiền trong bao lâu?",
        
        # Test 3: Process question
        "Ai phải phê duyệt để cấp quyền Level 3?",
        
        # Test 4: Out of domain — should abstain
        "ERR-404-NOTFOUND là lỗi gì?",
        
        # Test 5: Edge case
        "Nếu khách hàng yêu cầu hoàn tiền sau 35 ngày?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[Test {i}] {query}")
        print("-" * 60)
        
        try:
            result = rag_answer(
                query,
                retrieval_mode="dense",
                top_k_search=10,
                top_k_select=3,
                verbose=False
            )
            
            print(f"Answer: {result['answer']}")
            print(f"Sources: {result['sources']}")
            print(f"Chunks used: {len(result['chunks_used'])}")
            
            # Quality check
            has_citation = any(f"[{j}]" for j in range(1, 10))
            is_abstain = "Không đủ dữ liệu" in result['answer']
            
            if has_citation or is_abstain or len(result['sources']) > 0:
                print("✓ Quality check PASS")
            else:
                print("⚠ Quality check WARN: No citation found")
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
```

**Expected output:**
```
[Test 1] SLA xử lý ticket P1 là bao lâu?
Answer: Theo tài liệu [1], P1 tickets yêu cầu phản hồi trong 15 phút và xử lý trong 4 giờ.
Sources: ['sla_p1_2026.txt']
Chunks used: 3
✓ Quality check PASS

[Test 2] Khách hàng có thể yêu cầu hoàn tiền trong bao lâu?
Answer: Theo chính sách [1], khách hàng có thể yêu cầu hoàn tiền trong vòng 30 ngày kể từ ngày mua.
Sources: ['policy_refund_v4.txt']
Chunks used: 3
✓ Quality check PASS

[Test 4] ERR-404-NOTFOUND là lỗi gì?
Answer: Không đủ dữ liệu.
Sources: []
Chunks used: 0
✓ Quality check PASS (abstain correctly)
```

---

## 🔍 SPRINT 2: QUALITY CHECKS

### Checklist — Grounded Generation Quality

- [ ] **Citation format correct?**
  - ✅ Good: `Theo tài liệu [1], ...`
  - ❌ Bad: `Theo tài liệu, ...` (no citation number)
  - ❌ Bad: `Source: xyz` (wrong format)

- [ ] **Abstain when insufficient?**
  - ✅ Good: "Không đủ dữ liệu"
  - ❌ Bad: Guessing ("Có lẽ là...", "Thường thì...")
  - ❌ Bad: Using general knowledge ("Theo kinh nghiệm...")

- [ ] **No hallucination?**
  - ✅ Good: `Các thành viên IT Level 2 được cấp` (from access_control_sop.txt)
  - ❌ Bad: `Hệ thống hỗ trợ AI-powered` (not in docs)
  - ❌ Bad: `SLA là 10 phút` (docs say 15 phút)

- [ ] **Concise?**
  - ✅ Good: 1–3 sentences, clear fact
  - ❌ Bad: 5+ paragraphs, rambling
  - ❌ Bad: Extra explanation not in context

- [ ] **Consistent across calls?**
  - Run same query 3×, should get same/similar answer (temperature=0)
  - ✅ Good: Consistent answers
  - ❌ Bad: Completely different answers each time (check temperature)

---

## 🎯 SPRINT 3–4: LIGHT PROMPT TUNING (Optional)

If generation quality issues arise in Sprint 3, consider tweaks:

### Tweak 1: Add format specification

```python
# If answers are too long/rambling:
def build_grounded_prompt(query: str, context_block: str) -> str:
    prompt = f"""...
    
**Answer Format:** 
- If answer found: 1-2 sentences citing [1], [2], etc.
- If answer NOT found: Respond with EXACTLY "Không đủ dữ liệu."

**Question:** {query}
..."""
    return prompt
```

### Tweak 2: Add fallback to abstain

```python
# If LLM still tries to guess:
def call_llm(prompt: str) -> str:
    ...
    answer = response.choices[0].message.content.strip()
    
    # Detect if LLM is hallucinating (heuristic)
    if answer.startswith("Có thể", "Tôi nghĩ", "Theo kinh nghiệm"):
        answer = "Không đủ dữ liệu"
    
    return answer
```

### Tweak 3: Include examples in prompt

```python
def build_grounded_prompt(query: str, context_block: str) -> str:
    prompt = f"""...

**Examples:**
Q: What is sick leave policy?
Context: [Information provided]
A: According to [1], employees receive 5 sick days per year.

Q: What is the company's quantum computing roadmap?
Context: [No information about this topic]
A: Không đủ dữ liệu.

**Your Turn:**
Question: {query}
..."""
    return prompt
```

---

## ✅ FINAL CHECKLIST — NGHĨA

### Before Sprint 2 Ends
- [ ] `.env` file created with OPENAI_API_KEY
- [ ] API connection test successful
- [ ] `build_grounded_prompt()` implemented
- [ ] `call_llm()` implemented and working
- [ ] Tested on 5 sample queries
- [ ] No hallucination in outputs
- [ ] Citation format correct [1], [2]
- [ ] Abstain working ("Không đủ dữ liệu")

### Before Sprint 3 Starts
- [ ] Pass code to Trung for integration
- [ ] Trung confirms `rag_answer()` end-to-end works
- [ ] Ready for retrieval variant testing (Sprint 3)

### During Sprint 3–4
- [ ] Monitor generation quality in scorecards
- [ ] Minor prompt tweaks if needed (optional)
- [ ] Final QC before 18:00 commit

---

## 🚀 QUICK REFERENCE

### Setup
```bash
# Edit .env
OPENAI_API_KEY=sk-proj-...

# Test API
python -c "from openai import OpenAI; OpenAI(api_key=os.getenv('OPENAI_API_KEY')).chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': 'hi'}], max_tokens=5)"
```

### Implement
```python
# build_grounded_prompt()
# - Tell LLM to answer ONLY from context
# - Specify citation format [1], [2]
# - Say "Không đủ dữ liệu" when insufficient

# call_llm()
# - Initialize OpenAI client
# - Use temperature=0 (deterministic)
# - Extract answer from response.choices[0].message.content
```

### Test
```bash
# Add to rag_answer.py main():
result = rag_answer("Test query")
print(result['answer'])  # Should have citation or abstain
```

---

## 📌 IMPORTANT NOTES

1. **Temperature = 0 is CRITICAL**
   - Ensures deterministic output for evaluation
   - DO NOT use random sampling (temperature > 0)

2. **Citation format must match retrieval**
   - If retrieve_dense() returns 3 chunks → citations [1], [2], [3]
   - Else LLM can create invalid citations like [5] when only 3 chunks

3. **Abstain is BETTER than hallucinate**
   - Saying "Không đủ dữ liệu" = 0 points but NO PENALTY
   - Hallucinating = -50% penalty
   - So abstain when unsafe!

4. **Test across both retrieval modes**
   - Sprint 2: Test with dense (baseline)
   - Sprint 3: Test with hybrid (variant)
   - Generation should work same way for both

---

**Chúc bạn làm tốt! 🎯**
