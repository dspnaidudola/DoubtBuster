import pytest
from backend.services.code_exec_service import execute_python_code, check_code_safety, run_coding_challenge
from backend.services.rag_service import chunk_sections, retrieve_grounded_chunks, answer_with_rag

def test_code_exec_normal():
    code = "print(2 + 2)"
    res = execute_python_code(code)
    assert res["success"] is True
    assert "4" in res["stdout"].strip()

def test_code_exec_blocks_unsafe():
    bad_code = "import os\nos.system('dir')"
    res = execute_python_code(bad_code)
    assert res["success"] is False
    assert "forbidden token" in res["stderr"]

def test_code_exec_timeout():
    infinite_loop = "while True:\n    pass"
    res = execute_python_code(infinite_loop, timeout_sec=0.5)
    assert res["success"] is False
    assert res["timed_out"] is True

def test_coding_challenge_runner():
    challenge = {
        "func_name": "add",
        "test_cases": [
            {"input": (1, 2), "expected": 3},
            {"input": (5, 5), "expected": 10}
        ]
    }
    good_code = "def add(a, b):\n    return a + b\n"
    res = run_coding_challenge(good_code, challenge)
    assert res["success"] is True
    assert res["all_passed"] is True

def test_rag_chunking_and_retrieval():
    sections = [
        {"doc_name": "ml_notes.pdf", "section": "Page 1", "text": "Linear regression minimizes the mean squared error loss function between predictions and labels."},
        {"doc_name": "ml_notes.pdf", "section": "Page 2", "text": "Logistic regression uses the sigmoid activation function to map inputs to probabilities."}
    ]
    chunks = chunk_sections(sections, chunk_size=200)
    assert len(chunks) >= 2

    # Query for sigmoid
    results = retrieve_grounded_chunks("sigmoid activation", chunks, top_k=1)
    assert len(results) == 1
    assert "sigmoid" in results[0]["content"].lower()

def test_rag_answer_formatting():
    chunks = [{"doc_name": "unit1.pdf", "section": "Page 3", "content": "Backpropagation computes gradients using the chain rule.", "relevance_score": 0.85}]
    ans = answer_with_rag("What does backprop compute?", chunks, api_key=None)
    assert ans is not None
    assert len(ans) > 20
