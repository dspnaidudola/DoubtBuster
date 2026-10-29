import subprocess
import sys
import time
from typing import Dict, Any, List, Optional

UNSAFE_PATTERNS = [
    "import os", "from os", "import subprocess", "from subprocess",
    "import socket", "from socket", "import shutil", "from shutil",
    "__import__('os')", "__import__('subprocess')", "eval(", "exec(",
    "open(", "write("
]

def check_code_safety(code: str) -> Optional[str]:
    """Scans code for dangerous patterns that could compromise system security."""
    for line in code.splitlines():
        clean = line.strip()
        if clean.startswith("#"):
            continue
        for pat in UNSAFE_PATTERNS:
            if pat in clean:
                return f"Execution blocked: forbidden token '{pat}' detected for sandbox security."
    return None

def execute_python_code(code: str, stdin_input: str = "", timeout_sec: float = 3.0) -> Dict[str, Any]:
    """
    Executes Python code in an isolated subprocess with a strict timeout.
    Returns output, errors, and execution metrics.
    """
    safety_err = check_code_safety(code)
    if safety_err:
        return {
            "success": False,
            "stdout": "",
            "stderr": safety_err,
            "timed_out": False,
            "execution_time_ms": 0.0
        }

    start_time = time.perf_counter()
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "timed_out": False,
            "execution_time_ms": elapsed_ms
        }
    except subprocess.TimeoutExpired:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout_sec}s. Check for infinite loops (e.g., 'while True').",
            "timed_out": True,
            "execution_time_ms": elapsed_ms
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution error: {e}",
            "timed_out": False,
            "execution_time_ms": 0.0
        }

def run_coding_challenge(user_code: str, challenge: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates student code against challenge test cases.
    challenge format:
    {
        "func_name": "reverse_string",
        "test_cases": [
            {"input": ("hello",), "expected": "olleh"},
            {"input": ("GMRIT",), "expected": "TIRMG"}
        ]
    }
    """
    safety_err = check_code_safety(user_code)
    if safety_err:
        return {"success": False, "error": safety_err, "results": []}

    func_name = challenge["func_name"]
    test_cases = challenge["test_cases"]
    
    # Construct runner script
    runner_script = user_code + "\n\n"
    runner_script += "import json\n"
    runner_script += "results = []\n"
    runner_script += f"test_data = {repr(test_cases)}\n"
    runner_script += "for tc in test_data:\n"
    runner_script += "    try:\n"
    runner_script += f"        out = {func_name}(*tc['input'])\n"
    runner_script += "        passed = out == tc['expected']\n"
    runner_script += "        results.append({'passed': passed, 'input': tc['input'], 'expected': tc['expected'], 'actual': out, 'error': None})\n"
    runner_script += "    except Exception as e:\n"
    runner_script += "        results.append({'passed': False, 'input': tc['input'], 'expected': tc['expected'], 'actual': None, 'error': str(e)})\n"
    runner_script += "print(json.dumps(results))\n"

    exec_res = execute_python_code(runner_script, timeout_sec=4.0)
    if not exec_res["success"]:
        return {
            "success": False,
            "error": exec_res["stderr"] or "Runtime error during execution.",
            "results": []
        }

    try:
        import json
        out_json = json.loads(exec_res["stdout"].strip())
        all_passed = all(tc.get("passed", False) for tc in out_json)
        return {
            "success": True,
            "all_passed": all_passed,
            "results": out_json,
            "execution_time_ms": exec_res["execution_time_ms"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to parse test runner output: {e}\nRaw output: {exec_res['stdout']}",
            "results": []
        }
