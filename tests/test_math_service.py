import pytest
from backend.services.math_code_service import solve_math_expression, analyze_matrix, diagnose_python_code

def test_solve_math_derivative():
    res = solve_math_expression("x**3 + 2*x", operation="derivative", variable="x")
    assert res["success"] is True
    assert "3*x**2 + 2" in res["result_str"]

def test_solve_math_equation():
    res = solve_math_expression("x**2 - 9", operation="solve", variable="x")
    assert res["success"] is True
    assert "-3" in res["result_str"] and "3" in res["result_str"]

def test_analyze_matrix():
    res = analyze_matrix("[[1, 2], [3, 4]]")
    assert res["success"] is True
    assert res["determinant"] == "-2"
    assert res["is_invertible"] is True

def test_diagnose_python_syntax_error():
    bad_code = "def foo()\n    return 42"
    diag = diagnose_python_code(bad_code)
    assert diag["success"] is True
    assert diag["syntax_ok"] is False
    assert len(diag["issues"]) > 0

def test_diagnose_clean_python():
    good_code = "def foo():\n    return 42\n"
    diag = diagnose_python_code(good_code)
    assert diag["success"] is True
    assert diag["syntax_ok"] is True
    assert diag["is_clean"] is True

def test_solve_math_equation_with_equals_and_implicit_mult():
    # Direct test for equation from user screenshot: -9(m-2)+7m=-10
    res = solve_math_expression("-9(m-2)+7m=-10", operation="simplify", variable="m")
    assert res["success"] is True
    assert "14" in res["result_str"]
    assert "steps" in res and len(res["steps"]) > 0

def test_solve_math_implicit_multiplication_with_powers():
    res = solve_math_expression("2x + 5 = 15", operation="solve", variable="x")
    assert res["success"] is True
    assert "5" in res["result_str"]

