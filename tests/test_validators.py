import pytest
from backend.utils.validators import validate_question

def test_accepts_normal_question():
    validate_question("Explain recursion in Python.")

def test_rejects_empty_question():
    with pytest.raises(ValueError):
        validate_question("   ")

def test_rejects_too_long_question():
    with pytest.raises(ValueError):
        validate_question("x" * 12001)
