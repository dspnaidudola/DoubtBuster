# DoubtBuster — Requirements

## Problem statement
GMRIT students need personalized, step-by-step support for technical questions outside classroom sessions, rather than only final answers.

## Target users
GMRIT undergraduate students studying programming, mathematics, data science, machine learning, deep learning, generative AI, and NLP fundamentals.

## MVP functional requirements
1. Let students select subject, topic, difficulty, and learning mode.
2. Accept a typed question and selected text-based problem files.
3. Provide hint-first and step-by-step explanations.
4. Support review of a student's attempted answer.
5. Explain programming concepts and discuss likely errors and corrections.
6. Explain mathematical reasoning with intermediate steps where applicable.
7. Generate a similar practice question with an answer key.
8. Support follow-up questions within the active session.
9. Validate empty and oversized input and display readable errors.
10. Disclose uncertainty and remind users to verify important outputs.

## Non-functional requirements
- Modular Python code and clear separation of UI and business logic.
- API keys read from environment variables or Streamlit secrets.
- No credentials or private student data committed to Git.
- Helpful failure behavior for missing credentials and provider errors.
- Documented setup, testing, limitations, and deployment.
- Clear privacy notice and responsible-use guidance.

## Acceptance checks
- Test programming, mathematics, ML, and NLP questions.
- Test empty, oversized, ambiguous, and unsupported inputs.
- Confirm hint-first mode does not immediately reveal the complete solution.
- Review mathematical and code explanations independently.
- Confirm missing API keys result in a readable message.
- Run automated tests and test a clean installation.

## Out of scope for this starter MVP
PDF/PPT parsing, RAG, persistent student profiles, faculty dashboard, adaptive learning, and secure code execution.
