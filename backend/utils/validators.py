MAX_QUESTION_CHARS = 12000

def validate_question(question: str) -> None:
    if not question or not question.strip():
        raise ValueError("Please enter a question or upload a text-based problem statement.")
    if len(question) > MAX_QUESTION_CHARS:
        raise ValueError(f"Your question is too long. Keep it under {MAX_QUESTION_CHARS:,} characters.")
