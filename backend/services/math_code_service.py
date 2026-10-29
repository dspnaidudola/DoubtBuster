import ast
import traceback
from typing import Dict, Any, Optional, List
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)

MATH_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)

def solve_math_expression(expression_str: str, operation: str = "solve", variable: str = "x") -> Dict[str, Any]:
    """
    Safely solves mathematical expressions and equations using SymPy.
    Supports implicit multiplication (e.g. 9(m-2), 7m), powers via ^,
    equations with '=', and automatic symbol inference.
    Operations supported: 'solve', 'derivative', 'integrate', 'simplify', 'limit', 'matrix'
    """
    try:
        clean_input = expression_str.strip().replace("−", "-")
        steps: List[str] = []

        # Check if the student entered an equation with '=' or '=='
        if "=" in clean_input:
            parts = clean_input.split("==" if "==" in clean_input else "=", 1)
            lhs_raw = parts[0].strip()
            rhs_raw = parts[1].strip()

            lhs = parse_expr(lhs_raw, transformations=MATH_TRANSFORMATIONS)
            rhs = parse_expr(rhs_raw, transformations=MATH_TRANSFORMATIONS)
            eq = sp.Eq(lhs, rhs)
            
            # Detect active variable symbol
            all_symbols = eq.free_symbols
            var = sp.Symbol(variable.strip()) if variable.strip() else sp.Symbol("x")
            if var not in all_symbols and all_symbols:
                # If student typed 'm' in equation but forgot to change variable from 'x'
                var = sorted(list(all_symbols), key=lambda s: s.name)[0]

            # Solve the equation
            solutions = sp.solve(eq, var)
            lhs_expanded = sp.expand(lhs)
            rhs_expanded = sp.expand(rhs)
            diff_simplified = sp.simplify(lhs - rhs)

            steps.append(f"1. **Original Equation:** $${sp.latex(lhs)} = {sp.latex(rhs)}$$")
            if lhs_expanded != lhs or rhs_expanded != rhs:
                steps.append(f"2. **Expanded Form:** $${sp.latex(lhs_expanded)} = {sp.latex(rhs_expanded)}$$")
            steps.append(f"3. **Standard Form ($f({var}) = 0$):** $${sp.latex(diff_simplified)} = 0$$")
            
            if solutions:
                sol_str = ", ".join(sp.latex(s) for s in solutions)
                steps.append(f"4. **Isolate ${var}$:** $${var} = {sol_str}$$")
                latex_sol = f"{sp.latex(var)} = {sol_str}"
            else:
                steps.append("4. **Solution:** No solution or identity equation.")
                latex_sol = "\\text{No solution}"

            return {
                "success": True,
                "original_expr": expression_str,
                "latex_expr": f"{sp.latex(lhs)} = {sp.latex(rhs)}",
                "result_str": f"{var} = {solutions}",
                "latex_result": latex_sol,
                "explanation": f"Step-by-step resolution of equation for ${sp.latex(var)}$:",
                "steps": steps
            }

        # Otherwise, handle regular single expressions
        expr = parse_expr(clean_input, transformations=MATH_TRANSFORMATIONS)
        all_symbols = expr.free_symbols
        var = sp.Symbol(variable.strip()) if variable.strip() else sp.Symbol("x")
        if var not in all_symbols and all_symbols:
            var = sorted(list(all_symbols), key=lambda s: s.name)[0]

        result = None
        latex_result = ""
        explanation = ""

        if operation == "solve":
            result = sp.solve(expr, var)
            latex_result = sp.latex(result)
            explanation = f"Solutions for ${var}$ in ${sp.latex(expr)} = 0$:"
            steps.append(f"1. **Set Expression to Zero:** $${sp.latex(expr)} = 0$$")
            steps.append(f"2. **Factor / Solve for ${var}$:** $${sp.latex(result)}$$")
        elif operation == "derivative":
            result = sp.diff(expr, var)
            latex_result = sp.latex(result)
            explanation = f"Derivative with respect to ${var}$ ($\\frac{{d}}{{d{var}}} [{sp.latex(expr)}]$):"
            steps.append(f"1. **Function:** $$f({var}) = {sp.latex(expr)}$$")
            steps.append(f"2. **Differentiate:** $$\\frac{{d}}{{d{var}}} f({var}) = {latex_result}$$")
        elif operation == "integrate":
            result = sp.integrate(expr, var)
            latex_result = sp.latex(result) + " + C"
            explanation = f"Indefinite integral with respect to ${var}$ ($\\int {sp.latex(expr)} \\, d{var}$):"
            steps.append(f"1. **Integrand:** $$\\int {sp.latex(expr)} \\, d{var}$$")
            steps.append(f"2. **Antiderivative:** $${latex_result}$$")
        elif operation == "simplify":
            result = sp.simplify(expr)
            latex_result = sp.latex(result)
            explanation = f"Simplified form of ${sp.latex(expr)}$:"
            steps.append(f"1. **Original Expression:** $${sp.latex(expr)}$$")
            steps.append(f"2. **Simplified Form:** $${latex_result}$$")
        elif operation == "limit":
            result = sp.limit(expr, var, 0)
            latex_result = sp.latex(result)
            explanation = f"Limit as ${var} \\to 0$ of ${sp.latex(expr)}$:"
            steps.append(f"1. **Evaluate Limit:** $$\\lim_{{{var} \\to 0}} \\left( {sp.latex(expr)} \\right) = {latex_result}$$")
        else:
            result = sp.simplify(expr)
            latex_result = sp.latex(result)
            explanation = "Evaluated expression:"

        return {
            "success": True,
            "original_expr": expression_str,
            "latex_expr": sp.latex(expr),
            "result_str": str(result),
            "latex_result": latex_result,
            "explanation": explanation,
            "steps": steps
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "original_expr": expression_str
        }

def analyze_matrix(matrix_str: str) -> Dict[str, Any]:
    """
    Parses a 2D matrix (e.g., '[[1, 2], [3, 4]]' or '1, 2; 3, 4')
    and computes determinant, inverse, eigenvalues.
    """
    try:
        clean_str = matrix_str.strip()
        if ";" in clean_str:
            rows = [[sp.sympify(x.strip()) for x in row.split(",")] for row in clean_str.split(";")]
            M = sp.Matrix(rows)
        else:
            M = sp.Matrix(sp.sympify(clean_str))

        det = M.det()
        is_square = M.rows == M.cols
        inv = M.inv() if is_square and det != 0 else None
        eigenvals = M.eigenvals() if is_square else None

        return {
            "success": True,
            "rows": M.rows,
            "cols": M.cols,
            "latex_matrix": sp.latex(M),
            "determinant": sp.latex(det) if is_square else "N/A (Non-square)",
            "is_invertible": is_square and det != 0,
            "latex_inverse": sp.latex(inv) if inv is not None else "Not invertible",
            "eigenvalues": str(eigenvals) if eigenvals is not None else "N/A"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def diagnose_python_code(code_str: str) -> Dict[str, Any]:
    """
    Analyzes student Python code for syntax errors, common logical gotchas,
    and style issues. Does not execute untrusted code.
    """
    if not code_str or not code_str.strip():
        return {"success": False, "error": "No code provided for diagnosis."}

    issues = []
    lines = code_str.splitlines()

    # 1. AST Syntax Parsing
    try:
        parsed_ast = ast.parse(code_str)
        syntax_ok = True
        syntax_error = None
    except SyntaxError as syn_err:
        syntax_ok = False
        syntax_error = {
            "line": syn_err.lineno,
            "col": syn_err.offset,
            "msg": syn_err.msg,
            "snippet": syn_err.text.strip() if syn_err.text else ""
        }
        issues.append(f"❌ **SyntaxError on Line {syn_err.lineno}**: `{syn_err.msg}` in `{syn_err.text.strip() if syn_err.text else ''}`")

    # 2. Heuristic checks on lines
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        # Check missing colon on control statements
        if any(stripped.startswith(kw) for kw in ["if ", "elif ", "else", "for ", "while ", "def ", "class "]):
            if not stripped.endswith(":") and not stripped.endswith("\\"):
                issues.append(f"⚠️ **Line {idx}**: Missing colon (`:`) at the end of statement: `{stripped}`")

        # Check equality vs assignment inside if/while
        if (stripped.startswith("if ") or stripped.startswith("elif ") or stripped.startswith("while ")) and "=" in stripped:
            if "==" not in stripped and "!=" not in stripped and "<=" not in stripped and ">=" not in stripped:
                issues.append(f"⚠️ **Line {idx}**: Detected single assignment `=` instead of comparison `==` in condition.")

        # Check print statement without parentheses (Python 2 vs 3)
        if stripped.startswith("print ") and not stripped.startswith("print("):
            issues.append(f"⚠️ **Line {idx}**: In Python 3, `print` requires parentheses: `print(...)`.")

    # 3. AST semantic checks if syntax is valid
    if syntax_ok:
        class CodeAuditor(ast.NodeVisitor):
            def __init__(self):
                self.has_recursion = False
                self.func_name = None
                self.has_base_case = False

            def visit_FunctionDef(self, node):
                old_func = self.func_name
                self.func_name = node.name
                # Check for recursive calls
                has_self_call = any(
                    isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id == node.name
                    for sub in ast.walk(node)
                )
                has_if = any(isinstance(sub, ast.If) for sub in ast.walk(node))
                if has_self_call and not has_if:
                    issues.append(f"⚠️ **Function `{node.name}` (Line {node.lineno})**: Appears recursive without an `if` base condition! This may cause a `RecursionError`.")
                self.generic_visit(node)
                self.func_name = old_func

            def visit_For(self, node):
                # Check modifying sequence in loop
                if isinstance(node.iter, ast.Name):
                    target_name = node.iter.id
                    for sub in ast.walk(node):
                        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                            if isinstance(sub.func.value, ast.Name) and sub.func.value.id == target_name:
                                if sub.func.attr in ["append", "pop", "remove", "extend"]:
                                    issues.append(f"⚠️ **Line {node.lineno}**: Modifying list `{target_name}` with `.{sub.func.attr}()` while iterating over it can cause skipped elements.")
                self.generic_visit(node)

        auditor = CodeAuditor()
        auditor.visit(parsed_ast)

    return {
        "success": True,
        "syntax_ok": syntax_ok,
        "syntax_error": syntax_error,
        "total_lines": len(lines),
        "issues": issues,
        "is_clean": len(issues) == 0 and syntax_ok
    }
