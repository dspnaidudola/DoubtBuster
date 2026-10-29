# DoubtBuster — Presentation Slides Deck
**Project 14:** DoubtBuster — GMRIT Student Doubt-Solving AI Tutor  
**Handbook Requirement:** Deliverables to Submit #7 (5–8 Slides explaining product, workflow, technical choices, demo, results, and limitations)

---

## Slide 1: Title & Project Overview
### 🎓 DoubtBuster: GMRIT Student Doubt-Solving AI Tutor
*Active Learning Scaffolding, Mathematical Verification & Course Grounding*

- **Target Audience:** GMRIT Undergraduate Engineering Students (CSE, AI&DS, IT, ECE)
- **Domain:** Generative AI, Natural Language Processing, and Educational Technology
- **Core Philosophy:** Teach intermediate reasoning, eliminate hallucinations via deterministic engines, and connect student struggles directly to classroom lectures.

---

## Slide 2: The Problem Statement
### Why Traditional AI Fails Engineering Students
- **Direct Answer Spoon-Feeding:** Generic LLMs output final answers without teaching intermediate reasoning steps, hindering long-term retention.
- **AI Hallucinations in Math & Code:** LLMs frequently produce plausible-sounding but mathematically incorrect equations or buggy code with unhandled edge cases.
- **Disconnected from Curriculum:** Answers ignore specific GMRIT course notes, syllabi, and faculty lecture conventions.
- **Faculty Blindspot:** Professors cannot identify which topics are causing the most confusion outside of classroom hours.

---

## Slide 3: System Architecture & Workflow
### Modular, Scalable & Streamlit Community Cloud Deployable
- **User Interface Layer:** Streamlit with custom CSS tokens, Mermaid flowchart rendering, and Plotly analytics.
- **Context Routing & Guardrails:** Validates character bounds and routes inputs to deterministic solvers vs. AI pipelines.
- **RAG Retrieval Engine:** TF-IDF semantic chunking and cosine similarity over uploaded PDFs and PPTXs with direct slide/page citations.
- **AI Engine Layer:** Multi-provider support (OpenAI `gpt-4o-mini`, Google Gemini `gemini-2.5-flash`, and Built-in Offline Mode).
- **Local Persistence:** Zero-cloud SQLite database (`doubtbuster.db`) storing queries, quiz outcomes, difficult flags, and notes.

---

## Slide 4: Core Pedagogical Features
### Scaffolding Learning Modes
- **Hint-First Mode:** Scaffolds the problem with targeted questions rather than revealing the solution.
- **Step-by-Step Mode:** Unpacks complex mathematical proofs and algorithms with LaTeX equations and visual Mermaid diagrams.
- **Verify My Attempt:** Reviews the student's submitted code or calculations, pinpointing logic errors and confirming sound assumptions.
- **Multi-Turn Conversational Thread:** Ask continuous follow-up questions within the active context without losing state.
- **Adaptive Difficulty:** Automatically suggests Beginner, Intermediate, or Advanced level based on student performance.

---

## Slide 5: Deterministic Verification & Sandbox Execution
### Beyond Generative AI: Exact Verification Tools
- **Deterministic SymPy Engine:**
  - Exact symbolic derivatives, indefinite integrals, and limits ($\lim_{x \to 0}$).
  - Matrix analysis: Determinants, inverse matrices, and characteristic eigenvalue/eigenvector decompositions.
- **Safe Code Diagnoser & Subprocess Sandbox:**
  - Static AST parsing flags syntax errors, unclosed brackets, and recursive loops lacking base cases.
  - Subprocess execution sandbox executes Python scripts with a strict 3.0-second timeout.
  - Live Coding Challenge Evaluator tests student functions against automated test-case assertions.

---

## Slide 6: GMRIT Faculty Analytics & Intervention Hub
### Connecting Student Doubts to Classroom Teaching
- **Cohort Doubt Volume Tracking:** Monitors question counts across all curriculum subjects.
- **Topic Confusion Heatmap:** Identifies concepts most frequently flagged by students as difficult.
- **Automated Lecture Interventions:** Generates actionable guidance for professors on what to re-teach in upcoming lectures (e.g. *"Address Backpropagation in upcoming lecture: 4 students flagged this topic as difficult"*).
- **Privacy by Design:** All student records remain local on-device with a 1-click **Purge My Data** option.

---

## Slide 7: Evaluation Results & Test Evidence
### Rigorous Quality & Security Validation
- **Pytest Suite:** 32 out of 32 unit tests passing (100% test success rate).
  - Validation: Empty, oversized, and malformed inputs rejected.
  - Deterministic Math: Exact derivatives and matrix properties validated against SymPy truth.
  - Sandbox Security: Forbidden tokens (`import os`, `subprocess`) blocked before execution.
  - Infinite Loop Guardrail: `while True` terminated cleanly after 500 ms without crashing server.
- **Live Coding Challenges:** 100% automated test-case pass rate.

---

## Slide 8: Known Limitations & Future Roadmap
### Transparent Limitations & Next Steps
- **Current Limitations:**
  - Code sandbox is currently restricted to Python (C/Java/C++ analyzed statically).
  - Scanned PDFs without OCR text require pre-extracted text layers.
  - Streamlit Community Cloud free tier storage is ephemeral (mitigated by JSON/Markdown export).
- **Future Roadmap:**
  - Integration with GMRIT Moodle LMS for automated assignment doubt sync.
  - Speech-to-Text voice interface for regional language queries.
  - Multi-language Dockerized code sandboxing (C, C++, Java).
