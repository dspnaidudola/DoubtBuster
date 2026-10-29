# DoubtBuster — Formal Test Report

**Project:** 14. DoubtBuster — GMRIT Student Doubt-Solving AI Tutor  
**Handbook Requirement:** Deliverables to Submit #5 (At least 8 test cases with input, expected result, actual result, and pass/fail status).  
**Test Suite Date:** Academic Year 2026–2027  
**Test Framework:** Pytest 9.1.1 & Automated Subprocess Sandbox  

---

## 📊 Summary of Test Execution

| Total Tests Planned | Total Tests Executed | Passed | Failed | Success Rate |
| :---: | :---: | :---: | :---: | :---: |
| 32 | 32 | 32 | 0 | **100%** |

---

## 🧪 Detailed Test Cases (Minimum 8 Required)

### Test Case 1: Standard Programming Doubt (Recursion)
- **Component:** `backend.core.pipeline.answer_doubt`
- **Input:** 
  - Subject: `Programming`
  - Topic: `Recursion`
  - Question: `How does recursion utilize the system call stack?`
  - Mode: `Step-by-step explanation`
- **Expected Result:** Produces a structured explanation explaining the base case, stack frames, unwinding, and a follow-up comprehension question.
- **Actual Result:** Returned step-by-step guidance outlining call stack push/pop behavior with code example and comprehension reflection.
- **Status:** **PASS**

---

### Test Case 2: Input Validation (Empty Question Rejection)
- **Component:** `backend.utils.validators.validate_question`
- **Input:** `"   "` (Whitespace only)
- **Expected Result:** Raises `ValueError("Please enter a question or upload a text-based problem statement.")`
- **Actual Result:** Raised `ValueError` with the exact readable error message.
- **Status:** **PASS**

---

### Test Case 3: Input Validation (Oversized Question Guardrail)
- **Component:** `backend.utils.validators.validate_question`
- **Input:** String of 12,001 characters (`"x" * 12001`)
- **Expected Result:** Raises `ValueError("Your question is too long. Keep it under 12,000 characters.")`
- **Actual Result:** Raised `ValueError` with character boundary enforcement message.
- **Status:** **PASS**

---

### Test Case 4: Deterministic Mathematical Derivative Calculation
- **Component:** `backend.services.math_code_service.solve_math_expression`
- **Input:** 
  - Expression: `"x**3 + 2*x"`
  - Operation: `"derivative"`
  - Variable: `"x"`
- **Expected Result:** Returns symbolic derivative $3x^2 + 2$ with valid LaTeX markup.
- **Actual Result:** Returned `success=True`, `result_str="3*x**2 + 2"`, `latex_result="3 x^{2} + 2"`.
- **Status:** **PASS**

---

### Test Case 5: Matrix Property Analysis (Determinant & Invertibility)
- **Component:** `backend.services.math_code_service.analyze_matrix`
- **Input:** `"[[1, 2], [3, 4]]"`
- **Expected Result:** Calculates determinant $\det(M) = -2$, confirms invertibility, and computes inverse.
- **Actual Result:** Returned `determinant="-2"`, `is_invertible=True`, `latex_inverse` matched exact inverse matrix.
- **Status:** **PASS**

---

### Test Case 6: Isolated Code Sandbox (Normal Execution)
- **Component:** `backend.services.code_exec_service.execute_python_code`
- **Input:** Code: `"print(2 + 2)"`
- **Expected Result:** Runs in isolated subprocess and captures standard output `"4"`.
- **Actual Result:** Captured `stdout="4\n"`, `success=True`, execution time = 18.4 ms.
- **Status:** **PASS**

---

### Test Case 7: Sandbox Security (Unsafe Token Blocking)
- **Component:** `backend.services.code_exec_service.execute_python_code`
- **Input:** Code: `"import os\nos.system('dir')"`
- **Expected Result:** Blocks execution before launch; returns error detailing forbidden token.
- **Actual Result:** Blocked execution with message: `"Execution blocked: forbidden token 'import os' detected for sandbox security."`
- **Status:** **PASS**

---

### Test Case 8: Sandbox Timeout Guardrail (Infinite Loop Protection)
- **Component:** `backend.services.code_exec_service.execute_python_code`
- **Input:** Code: `"while True:\n    pass"` with timeout = 0.5s
- **Expected Result:** Halts process after 0.5 seconds; sets `timed_out=True` without hanging server.
- **Actual Result:** Subprocess terminated after 500 ms with `timed_out=True` and readable timeout message.
- **Status:** **PASS**

---

### Test Case 9: Live Coding Challenge Automated Evaluation
- **Component:** `backend.services.code_exec_service.run_coding_challenge`
- **Input:** 
  - Challenge: `reverse_str`
  - Submitted Code: `"def reverse_str(s):\n    return s[::-1]\n"`
  - Test Cases: `[("hello",) -> "olleh", ("GMRIT",) -> "TIRMG", ("",) -> ""]`
- **Expected Result:** Evaluates all 3 test cases in sandbox and returns `all_passed=True`.
- **Actual Result:** All 3 test cases evaluated to `passed=True` with `all_passed=True`.
- **Status:** **PASS**

---

### Test Case 10: RAG Course Material Retrieval & Citation Grounding
- **Component:** `backend.services.rag_service.retrieve_grounded_chunks`
- **Input:** 
  - Query: `"sigmoid activation function"`
  - Document Chunks: Excerpts from linear regression vs. logistic regression notes.
- **Expected Result:** Selects the chunk containing sigmoid activation as top rank with highest cosine similarity.
- **Actual Result:** Retrieved top chunk with `relevance_score > 0.6` citing document name and page.
- **Status:** **PASS**

---

### Test Case 11: SQLite Learning History Persistence & Flagging
- **Component:** `backend.services.db_service.save_doubt` & `toggle_difficult`
- **Input:** Doubt question, answer, topic `"Eigenvalues"`, subject `"Mathematics"`.
- **Expected Result:** Inserts record with auto-increment ID, allows toggling bookmark and `marked_difficult=1`.
- **Actual Result:** Inserted record, `toggle_difficult` updated value to 1, and `get_difficult_topics()` returned topic in revision list.
- **Status:** **PASS**

---

### Test Case 12: Privacy Data Purge Control
- **Component:** `backend.services.db_service.purge_student_data`
- **Input:** Call `purge_student_data()` on active database.
- **Expected Result:** Deletes all rows from `history`, `quiz_results`, `student_notes`, and `coding_attempts`.
- **Actual Result:** All database tables cleared; subsequent query returned 0 records.
- **Status:** **PASS**


---

### Test Case 13: Computer Architecture 8086 Microprocessor Isolation
- **Component:** `backend.core.pipeline.answer_doubt` & `backend.services.offline_tutor.synthesize_theory_answer`
- **Input:** 
  - Question: `"explain about 8086 microprocessor"`
  - Subject parameter: `"Mechanical Engineering"` (cross-domain test)
- **Expected Result:** Routes strictly to Computer Architecture, explains 16-bit ALU, 20-bit address bus, BIU 6-byte queue, EU, and CS/DS/SS/ES segment registers; contains zero mechanical jargon ("load factors", "structural integrity").
- **Actual Result:** Returned accurate 8086 architecture with 0 occurrences of mechanical terms.
- **Status:** **PASS**

---

### Test Case 14: Machine Learning AI & Data Science Grounding
- **Component:** `backend.core.pipeline.answer_doubt` & `backend.services.offline_tutor.synthesize_theory_answer`
- **Input:** 
  - Question: `"explain about machine learning"`
  - Subject parameter: `"Civil Engineering"` (cross-domain test)
- **Expected Result:** Routes strictly to AI & Machine Learning, details Tom Mitchell definition, Supervised/Unsupervised/Reinforcement paradigms, Gradient Descent optimization, and Bias-Variance tradeoff; contains zero civil engineering boilerplate.
- **Actual Result:** Returned exact Machine Learning guide with 0 occurrences of civil or generic boilerplate.
- **Status:** **PASS**
