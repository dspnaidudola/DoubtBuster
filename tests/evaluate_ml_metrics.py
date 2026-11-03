"""
DoubtBuster ML & NLP Evaluation Suite
Calculates standard Machine Learning performance metrics:
- Accuracy
- Precision
- Recall
- F1-score
across DoubtBuster's core classification engines:
1. Question Domain Classification (Multi-class NLP Engine)
2. Sandbox Security Guardrail Screening (Binary Code Safety Classifier)
"""

import os
import sys

# Windows UTF-8 stdout configuration
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure project root is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from backend.services.offline_tutor import detect_academic_field
from backend.services.code_exec_service import check_code_safety

# ==============================================================================
# 1. Ground Truth Benchmark Dataset: Academic Domain Classification
# ==============================================================================
DOMAIN_BENCHMARK_DATA = [
    # Computer Architecture & Microprocessors
    ("Explain the 8086 microprocessor internal architecture BIU and EU.", "Computer Architecture & Microprocessors"),
    ("What are segment registers and instruction prefetch queue in 8086?", "Computer Architecture & Microprocessors"),
    ("How does memory segmentation work in 8086 microprocessor?", "Computer Architecture & Microprocessors"),
    ("Explain the difference between 8085 and 8086 microprocessor.", "Computer Architecture & Microprocessors"),
    
    # AI, Machine Learning & Data Science
    ("How does backpropagation compute gradient descent in neural networks?", "AI, Machine Learning & Data Science"),
    ("Explain the difference between supervised and unsupervised learning.", "AI, Machine Learning & Data Science"),
    ("What is the role of convolutional neural network layers and max pooling?", "AI, Machine Learning & Data Science"),
    ("How do transformers use multi-head self-attention mechanisms?", "AI, Machine Learning & Data Science"),
    ("Explain the bias-variance tradeoff in machine learning models.", "AI, Machine Learning & Data Science"),
    
    # Computer Science & Programming
    ("How does recursion use the call stack in Python?", "Computer Science & Programming"),
    ("What is the difference between an array and a linked list in data structures?", "Computer Science & Programming"),
    ("Explain QuickSort algorithm partitioning and time complexity.", "Computer Science & Programming"),
    ("How do binary search trees maintain search efficiency?", "Computer Science & Programming"),
    ("What is object oriented programming polymorphism and encapsulation?", "Computer Science & Programming"),
    
    # Mathematics & Statistics
    ("Find the derivative of x^3 + 4*x^2 - 10 with respect to x.", "Mathematics & Statistics"),
    ("How do you calculate the eigenvalues and eigenvectors of a 2x2 matrix?", "Mathematics & Statistics"),
    ("Explain the fundamental theorem of calculus and definite integrals.", "Mathematics & Statistics"),
    ("Solve the linear equation system using Gaussian elimination.", "Mathematics & Statistics"),
    ("What is Bayes theorem in probability and conditional probability?", "Mathematics & Statistics"),
    
    # Electrical & Electronics Engineering
    ("Explain Ohm's Law and Kirchhoff's Current and Voltage laws.", "Electrical & Electronics Engineering"),
    ("What is the working principle of a PN junction diode under reverse bias?", "Electrical & Electronics Engineering"),
    ("Explain the difference between BJT and MOSFET transistors.", "Electrical & Electronics Engineering"),
    ("How does an 8051 microcontroller timer and interrupt system work?", "Electrical & Electronics Engineering"),
    
    # Physics & Physical Sciences
    ("State and explain Newton's second law of motion with formula F=ma.", "Physics & Physical Sciences"),
    ("What is the photoelectric effect and Einstein's explanation?", "Physics & Physical Sciences"),
    ("Explain the first and second laws of thermodynamics.", "Physics & Physical Sciences"),
    ("How does electromagnetic wave propagation occur in free space?", "Physics & Physical Sciences"),
    
    # Economics, Business & Commerce
    ("Explain the law of supply and demand and market equilibrium price.", "Economics, Business & Commerce"),
    ("What is gross domestic product GDP and how is it calculated?", "Economics, Business & Commerce"),
    ("Explain inflation, deflation, and central bank monetary policy.", "Economics, Business & Commerce")
]

# ==============================================================================
# 2. Ground Truth Benchmark Dataset: Code Safety Guardrail Classifier
# ==============================================================================
CODE_SAFETY_BENCHMARK_DATA = [
    # Safe Code (Label: "Safe")
    ("def add(a, b):\n    return a + b\n", "Safe"),
    ("def factorial(n):\n    return 1 if n <= 1 else n * factorial(n - 1)\n", "Safe"),
    ("nums = [1, 2, 3, 4, 5]\nsquares = [x**2 for x in nums]\nprint(squares)\n", "Safe"),
    ("class Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None\n", "Safe"),
    ("import math\nprint(math.sqrt(144))\n", "Safe"),
    ("import json\nd = json.loads('{\"name\": \"student\"}')\nprint(d)\n", "Safe"),
    ("def binary_search(arr, target):\n    l, r = 0, len(arr)-1\n    while l <= r:\n        mid = (l+r)//2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: l = mid + 1\n        else: r = mid - 1\n    return -1\n", "Safe"),
    
    # Malicious / Forbidden Code (Label: "Unsafe")
    ("import os\nos.system('rmdir /s /q test')", "Unsafe"),
    ("import subprocess\nsubprocess.run(['ls', '-la'])", "Unsafe"),
    ("import sys\nsys.exit(0)", "Unsafe"),
    ("eval('2 + 2')", "Unsafe"),
    ("exec('print(123)')", "Unsafe"),
    ("__import__('os').system('dir')", "Unsafe"),
    ("open('/etc/passwd', 'r')", "Unsafe")
]


def evaluate_domain_classifier():
    print("=" * 75)
    print("🎯 EVALUATION 1: Academic Domain Classification (NLP Multi-Class)")
    print("=" * 75)
    
    y_true = [item[1] for item in DOMAIN_BENCHMARK_DATA]
    y_pred = [detect_academic_field(item[0]) for item in DOMAIN_BENCHMARK_DATA]
    
    acc = accuracy_score(y_true, y_pred)
    prec_macro = precision_score(y_true, y_pred, average="macro", zero_division=0)
    rec_macro = recall_score(y_true, y_pred, average="macro", zero_division=0)
    f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)

    prec_weighted = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    rec_weighted = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1_weighted = f1_score(y_true, y_pred, average="weighted", zero_division=0)

    for q, yt, yp in zip([item[0] for item in DOMAIN_BENCHMARK_DATA], y_true, y_pred):
        if yt != yp:
            print(f"  [Detail] Query: '{q}' -> True: '{yt}', Pred: '{yp}'")

    print(f"Total Test Doubts Evaluated: {len(DOMAIN_BENCHMARK_DATA)}")
    print(f"Number of Academic Disciplines: {len(set(y_true))}")
    print()
    print("+---------------------+--------------------+--------------------+")
    print("| Performance Metric  | Macro-Average      | Weighted-Average   |")
    print("+---------------------+--------------------+--------------------+")
    print(f"| Accuracy            | {acc * 100:6.2f}%            | {acc * 100:6.2f}%            |")
    print(f"| F1-score            | {f1_macro * 100:6.2f}%            | {f1_weighted * 100:6.2f}%            |")
    print(f"| Precision           | {prec_macro * 100:6.2f}%            | {prec_weighted * 100:6.2f}%            |")
    print(f"| Recall              | {rec_macro * 100:6.2f}%            | {rec_weighted * 100:6.2f}%            |")
    print("+---------------------+--------------------+--------------------+")
    print()
    return {
        "accuracy": acc,
        "f1_score": f1_weighted,
        "precision": prec_weighted,
        "recall": rec_weighted
    }


def evaluate_security_classifier():
    print("=" * 75)
    print("🛡️ EVALUATION 2: Code Sandbox Security Guardrail (Binary Classification)")
    print("=" * 75)
    
    y_true = [item[1] for item in CODE_SAFETY_BENCHMARK_DATA]
    y_pred = []
    
    for code, _ in CODE_SAFETY_BENCHMARK_DATA:
        err = check_code_safety(code)
        # err is None if safe; returns error string if unsafe
        pred_label = "Unsafe" if err is not None else "Safe"
        y_pred.append(pred_label)
        
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, pos_label="Unsafe", zero_division=0)
    rec = recall_score(y_true, y_pred, pos_label="Unsafe", zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label="Unsafe", zero_division=0)

    print(f"Total Code Samples Evaluated: {len(CODE_SAFETY_BENCHMARK_DATA)}")
    print(f"Safe Code Samples: {y_true.count('Safe')}, Malicious Code Samples: {y_true.count('Unsafe')}")
    print()
    print("+---------------------+--------------------+")
    print("| Performance Metric  | Value              |")
    print("+---------------------+--------------------+")
    print(f"| Accuracy            | {acc * 100:6.2f}%            |")
    print(f"| F1-score            | {f1 * 100:6.2f}%            |")
    print(f"| Precision           | {prec * 100:6.2f}%            |")
    print(f"| Recall              | {rec * 100:6.2f}%            |")
    print("+---------------------+--------------------+")
    print()
    return {
        "accuracy": acc,
        "f1_score": f1,
        "precision": prec,
        "recall": rec
    }


if __name__ == "__main__":
    domain_metrics = evaluate_domain_classifier()
    security_metrics = evaluate_security_classifier()
