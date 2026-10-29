import json
from typing import List, Dict, Any, Optional
from backend.services.llm_service import ask_llm
from backend.services.db_service import save_doubt
from backend.services.offline_tutor import detect_domain

# Comprehensive offline quiz bank for GMRIT engineering students
OFFLINE_QUIZ_BANK: Dict[str, List[Dict[str, Any]]] = {
    "Programming": [
        # Topic: Loops & Iteration
        {
            "topic": "loops",
            "tags": ["loops", "loop", "for loop", "range", "iteration"],
            "question": "What is the output of `list(range(1, 10, 2))` in Python?",
            "options": ["[1, 3, 5, 7, 9]", "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "[2, 4, 6, 8]", "[1, 3, 5, 7]"],
            "correct": 0,
            "explanation": "`range(start, stop, step)` generates numbers from start (1) up to but excluding stop (10), incrementing by step (2): 1, 3, 5, 7, 9."
        },
        {
            "topic": "loops",
            "tags": ["loops", "loop", "for loop", "while loop", "break", "else"],
            "question": "When does the `else` block attached to a `for` or `while` loop execute in Python?",
            "options": [
                "Only when the loop terminates naturally without encountering a `break` statement",
                "After every iteration of the loop",
                "Only when an exception occurs inside the loop",
                "Never; `else` cannot be used with loops in Python"
            ],
            "correct": 0,
            "explanation": "In Python, a loop's `else` clause executes if and only if the loop completes all iterations without hitting a `break`."
        },
        {
            "topic": "loops",
            "tags": ["loops", "loop", "nested loop", "time complexity", "big o"],
            "question": "What is the worst-case time complexity of two nested loops where both the outer and inner loops iterate $n$ times?",
            "options": ["O(n^2)", "O(n log n)", "O(n)", "O(2^n)"],
            "correct": 0,
            "explanation": "An inner loop executing $n$ times for each of the $n$ outer iterations yields $n \\times n = O(n^2)$ quadratic operations."
        },
        {
            "topic": "loops",
            "tags": ["loops", "loop", "while loop", "infinite loop"],
            "question": "What happens if the loop termination variable in a `while` loop is never updated inside the loop body?",
            "options": [
                "The loop becomes an infinite loop and runs indefinitely until interrupted",
                "Python automatically terminates the loop after 1000 iterations",
                "A `WhileLoopError` is raised immediately",
                "The loop executes exactly once"
            ],
            "correct": 0,
            "explanation": "Without updating the state variable, the loop test condition remains permanently True, creating an infinite loop."
        },

        # Topic: Functions & Scope
        {
            "topic": "functions",
            "tags": ["functions", "function", "args", "parameters", "arguments"],
            "question": "In Python, what does the `*args` parameter allow in a function definition?",
            "options": [
                "Accepting an arbitrary number of positional arguments as a tuple",
                "Accepting keyword arguments as a dictionary",
                "Restricting arguments strictly to integer types",
                "Passing arguments by reference"
            ],
            "correct": 0,
            "explanation": "`*args` packs excess positional arguments passed to the function into an immutable tuple."
        },
        {
            "topic": "functions",
            "tags": ["functions", "function", "default arguments", "mutable defaults"],
            "question": "What is the danger of using a mutable object (like a list `[]`) as a default parameter in a Python function?",
            "options": [
                "The default list is created once and shared across all subsequent calls that omit the argument",
                "It raises a `SyntaxError` at compile time",
                "It forces the function to execute in $O(n^2)$ time",
                "It automatically converts the list into a tuple"
            ],
            "correct": 0,
            "explanation": "In Python, default arguments are evaluated once at function definition time, so mutations persist across all invocations."
        },
        {
            "topic": "functions",
            "tags": ["functions", "function", "scope", "legb", "namespaces"],
            "question": "According to Python's LEGB rule, in what order does the interpreter resolve variable names?",
            "options": [
                "Local -> Enclosing -> Global -> Built-in",
                "Global -> Local -> Enclosing -> Built-in",
                "Local -> Global -> Enclosing -> Built-in",
                "Built-in -> Global -> Local -> Enclosing"
            ],
            "correct": 0,
            "explanation": "LEGB lookup order: first Local scope, then Enclosing functions, then Global (module level), and finally Built-in names."
        },
        {
            "topic": "functions",
            "tags": ["functions", "function", "return", "none"],
            "question": "What value does a Python function return by default if execution reaches the end without a `return` statement?",
            "options": ["None", "0", "False", "An empty string \"\""],
            "correct": 0,
            "explanation": "In Python, any function that finishes without an explicit return statement returns `None` of type `NoneType`."
        },

        # Topic: Recursion & Call Stack
        {
            "topic": "recursion",
            "tags": ["recursion", "recursive", "base case", "call stack"],
            "question": "Which of the following will occur if a recursive function does not have a properly terminating base case?",
            "options": [
                "RecursionError: maximum recursion depth exceeded",
                "MemoryLeakError",
                "Segmentation Fault",
                "ZeroDivisionError"
            ],
            "correct": 0,
            "explanation": "Recursive calls without a terminating base case keep allocating stack frames until `sys.getrecursionlimit()` is reached, raising `RecursionError`."
        },
        {
            "topic": "recursion",
            "tags": ["recursion", "recursive", "call stack", "stack frame"],
            "question": "What internal data structure does the runtime environment use to manage recursive function calls and local variables?",
            "options": ["Call Stack", "FIFO Queue", "Min-Heap", "Binary Search Tree"],
            "correct": 0,
            "explanation": "Every active subroutine call allocates a stack frame on the Call Stack to preserve local state and return addresses."
        },

        # Topic: Microprocessors & Microcontrollers
        {
            "topic": "microprocessor",
            "tags": ["8086", "8051", "microprocessor", "architecture", "biu"],
            "question": "What is the primary role of the 6-byte instruction queue in the Intel 8086 Bus Interface Unit (BIU)?",
            "options": [
                "To pre-fetch instructions from memory, enabling pipelined instruction execution",
                "To store temporary arithmetic results from the ALU",
                "To hold interrupt vectors during hardware interrupts",
                "To store 20-bit physical memory addresses"
            ],
            "correct": 0,
            "explanation": "The 6-byte FIFO queue in the 8086 BIU overlaps fetch and execute cycles, prefetching up to 6 opcode bytes to eliminate bus latency."
        },
        {
            "topic": "microcontroller",
            "tags": ["8051", "8086", "microcontroller", "harvard architecture"],
            "question": "How does the Intel 8051 microcontroller fundamentally differ from the 8086 microprocessor in memory architecture?",
            "options": [
                "8051 uses Harvard Architecture (physically separate Program ROM & Data RAM buses), while 8086 uses Von Neumann",
                "8051 has a 16-bit ALU, while 8086 has an 8-bit ALU",
                "8051 requires external RAM/ROM chips to execute any program",
                "8051 has no general purpose I/O ports"
            ],
            "correct": 0,
            "explanation": "The 8051 is a Harvard Architecture microcontroller with independent Program ROM and Data RAM spaces, whereas 8086 is a Von Neumann processor."
        },

        # Topic: Data Structures & Core Python
        {
            "topic": "data structures",
            "tags": ["hash table", "dict", "time complexity"],
            "question": "What is the average-case time complexity of looking up a key in a Python dictionary (Hash Table)?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
            "correct": 0,
            "explanation": "Hash tables provide $O(1)$ constant time average lookup due to direct bucket indexing via hash codes."
        },
        {
            "topic": "data structures",
            "tags": ["equality", "identity", "is vs =="],
            "question": "What does the `is` keyword check in Python, compared to `==`?",
            "options": [
                "`is` checks identity (same memory address), `==` checks equality of values",
                "`is` checks mathematical equality, `==` checks types",
                "`is` checks if values are within the same scope, `==` checks references",
                "They are completely interchangeable"
            ],
            "correct": 0,
            "explanation": "`is` checks object identity (`id(a) == id(b)`), while `==` invokes `__eq__` to compare values."
        }
    ],
    "Mathematics": [
        {
            "question": "What is the derivative of f(x) = ln(3x^2 + 1) with respect to x using the Chain Rule?",
            "options": ["6x / (3x^2 + 1)", "1 / (3x^2 + 1)", "6x ln(3x^2 + 1)", "3x / (3x^2 + 1)"],
            "correct": 0,
            "explanation": "By the Chain Rule, d/dx[ln(u)] = (1/u) * du/dx. Here u = 3x^2 + 1, and du/dx = 6x, yielding 6x / (3x^2 + 1)."
        },
        {
            "question": "For a square matrix A to be invertible, what must be true about its determinant det(A)?",
            "options": ["det(A) = 0", "det(A) != 0", "det(A) > 1", "det(A) must be an integer"],
            "correct": 1,
            "explanation": "A matrix is non-singular (invertible) if and only if its determinant is non-zero (det(A) != 0)."
        },
        {
            "question": "If P(A) = 0.4, P(B) = 0.5, and A and B are independent events, what is P(A and B)?",
            "options": ["0.9", "0.2", "0.1", "0.0"],
            "correct": 1,
            "explanation": "For independent events, P(A and B) = P(A) * P(B) = 0.4 * 0.5 = 0.20."
        },
        {
            "question": "What are the eigenvalues of the matrix A = [[3, 0], [0, 5]]?",
            "options": ["3 and 5", "8 and 15", "0 and 3", "-3 and -5"],
            "correct": 0,
            "explanation": "For any diagonal or triangular matrix, the eigenvalues are simply the entries along the main diagonal (here, 3 and 5)."
        }
    ],
    "Machine Learning": [
        {
            "question": "Which regularization technique adds the sum of absolute values of weights (|w|) to the loss function?",
            "options": ["L2 Regularization (Ridge)", "L1 Regularization (Lasso)", "Dropout", "Batch Normalization"],
            "correct": 1,
            "explanation": "L1 (Lasso) adds lambda * sum(|w|), which drives less important feature weights strictly to zero, effectively performing feature selection."
        },
        {
            "question": "What does a high training accuracy combined with a low validation/test accuracy strongly indicate?",
            "options": ["High Bias (Underfitting)", "High Variance (Overfitting)", "Data Leakage", "Optimal Generalization"],
            "correct": 1,
            "explanation": "When a model memorizes noise and specific patterns in training data without generalizing to unseen test data, it is overfitting (high variance)."
        },
        {
            "question": "In a medical diagnosis task where missing a disease (False Negative) is catastrophic, which metric should be prioritized?",
            "options": ["Precision", "Recall (Sensitivity)", "Specificity", "Mean Absolute Error"],
            "correct": 1,
            "explanation": "Recall = TP / (TP + FN). Maximizing recall minimizes False Negatives, ensuring that actual positive cases are rarely missed."
        }
    ],
    "Deep Learning": [
        {
            "question": "Why is the ReLU activation function (f(x) = max(0, x)) preferred over Sigmoid in deep feedforward hidden layers?",
            "options": [
                "It is completely differentiable everywhere including at 0",
                "It mitigates the vanishing gradient problem for positive activations and is fast to compute",
                "It produces outputs bounded strictly between -1 and 1",
                "It prevents dying neurons under all circumstances"
            ],
            "correct": 1,
            "explanation": "For positive inputs, ReLU has a constant gradient of 1, preventing gradients from vanishing exponentially through deep layers."
        },
        {
            "question": "What is the primary role of Pooling layers (e.g. MaxPooling) in Convolutional Neural Networks (CNNs)?",
            "options": [
                "To increase the number of channels",
                "To reduce spatial dimensions, parameter count, and introduce translational invariance",
                "To calculate the final loss function",
                "To normalize layer weights to zero mean"
            ],
            "correct": 1,
            "explanation": "Pooling downsamples feature maps spatially (e.g. 2x2 with stride 2), reducing computational overhead while retaining salient features."
        }
    ],
    "NLP": [
        {
            "question": "What problem does Subword Tokenization (e.g., Byte Pair Encoding / WordPiece) solve compared to Word-Level tokenization?",
            "options": [
                "It eliminates the need for attention mechanisms",
                "It handles Out-Of-Vocabulary (OOV) words effectively while maintaining a manageable vocabulary size",
                "It converts text into audio spectrograms",
                "It forces all sentences to have equal length without padding"
            ],
            "correct": 1,
            "explanation": "Subword tokenizers decompose unseen or rare words into recognizable subword morphemes, preventing large OOV token rates."
        },
        {
            "question": "In the Transformer architecture, why is Positional Encoding added to input token embeddings?",
            "options": [
                "Because self-attention operations are permutation-invariant and do not inherently encode word order",
                "To normalize vector magnitudes to unit length",
                "To encrypt student data",
                "To speed up gradient descent convergence"
            ],
            "correct": 0,
            "explanation": "Since Self-Attention processes all tokens in parallel without recurrence, positional encodings must be injected so the model knows token sequence order."
        }
    ],
    "Data Science": [
        {
            "question": "Which pandas method is used to obtain summary statistics (mean, std, min, quartiles, max) for numeric columns?",
            "options": ["df.info()", "df.describe()", "df.summary()", "df.head()"],
            "correct": 1,
            "explanation": "`df.describe()` generates descriptive statistics summarizing the central tendency, dispersion, and shape of a dataset's distribution."
        },
        {
            "question": "When should you use Median imputation instead of Mean imputation for missing numerical data?",
            "options": [
                "When the feature contains extreme outliers or is heavily skewed",
                "When the data is normally distributed",
                "Only when all values are integers",
                "Never, mean is always mathematically superior"
            ],
            "correct": 0,
            "explanation": "The median is robust against extreme outliers and skewness, whereas the mean is easily distorted by extreme values."
        }
    ]
}

# Curated Coding Exercises with automated test cases
CURATED_CODING_CHALLENGES = {
    "Programming": [
        {
            "title": "Reverse a String Recursively",
            "description": "Write a function `reverse_str(s: str) -> str` that recursively reverses a string without using built-in slicing `[::-1]`.",
            "func_name": "reverse_str",
            "starter_code": "def reverse_str(s: str) -> str:\n    # Write your recursive code here\n    if len(s) <= 1:\n        return s\n    return reverse_str(s[1:]) + s[0]\n",
            "test_cases": [
                {"input": ("hello",), "expected": "olleh"},
                {"input": ("GMRIT",), "expected": "TIRMG"},
                {"input": ("",), "expected": ""}
            ]
        },
        {
            "title": "Find Missing Number in Array [0..n]",
            "description": "Write a function `find_missing(nums: list) -> int` that finds the single missing number from an array containing $n$ distinct numbers in range $[0, n]$.",
            "func_name": "find_missing",
            "starter_code": "def find_missing(nums: list) -> int:\n    n = len(nums)\n    expected_sum = n * (n + 1) // 2\n    return expected_sum - sum(nums)\n",
            "test_cases": [
                {"input": ([3, 0, 1],), "expected": 2},
                {"input": ([0, 1],), "expected": 2},
                {"input": ([9, 6, 4, 2, 3, 5, 7, 0, 1],), "expected": 8}
            ]
        }
    ],
    "Mathematics": [
        {
            "title": "Euclidean GCD Algorithm",
            "description": "Write a function `gcd(a: int, b: int) -> int` to compute the greatest common divisor using Euclid's algorithm.",
            "func_name": "gcd",
            "starter_code": "def gcd(a: int, b: int) -> int:\n    while b != 0:\n        a, b = b, a % b\n    return a\n",
            "test_cases": [
                {"input": (48, 18), "expected": 6},
                {"input": (101, 103), "expected": 1},
                {"input": (20, 100), "expected": 20}
            ]
        }
    ],
    "Machine Learning": [
        {
            "title": "Sigmoid Activation Function",
            "description": "Write a function `sigmoid(x: float) -> float` that calculates $\\sigma(x) = \\frac{1}{1 + e^{-x}}$ rounded to 4 decimal places.",
            "func_name": "sigmoid",
            "starter_code": "import math\n\ndef sigmoid(x: float) -> float:\n    val = 1.0 / (1.0 + math.exp(-x))\n    return round(val, 4)\n",
            "test_cases": [
                {"input": (0.0,), "expected": 0.5},
                {"input": (2.0,), "expected": 0.8808},
                {"input": (-2.0,), "expected": 0.1192}
            ]
        }
    ]
}

def get_adaptive_difficulty(stats: Dict[str, Any]) -> str:
    """Dynamically suggests difficulty level based on rolling quiz score and study activity."""
    avg_score = stats.get("avg_quiz_score", 0.0)
    quizzes = stats.get("total_quizzes", 0)

    if quizzes >= 3 and avg_score >= 80.0:
        return "Advanced"
    elif quizzes >= 1 and avg_score >= 55.0:
        return "Intermediate"
    return "Beginner"

def answer_doubt(
    question: str,
    subject: str,
    topic: str,
    level: str,
    mode: str,
    language: str,
    attempt: str,
    api_key: str,
    model: str,
    persist: bool = True
) -> str:
    # Strictly ground domain to the question content (prevents stale UI selection leaks)
    from backend.services.offline_tutor import detect_academic_field
    subject = detect_academic_field(question)
    if mode == "Hint first":
        mode_instruction = (
            "Give one useful pedagogical hint and a short explanation of why it helps. Do not reveal "
            "the complete final answer immediately. End with one thought-provoking question inviting the student to try."
        )
    elif mode == "Verify my answer":
        mode_instruction = (
            "Evaluate the student's attempt. Identify what is correct, what is incorrect or missing, "
            "and how to verify it. If no attempt was supplied, ask them to provide one before judging it; "
            "you may still explain the method without pretending to verify an absent answer."
        )
    elif mode == "Practice question with answer key":
        mode_instruction = "Create one relevant practice problem, then provide a clearly separated worked solution and answer key."
    else:
        mode_instruction = (
            "Give a logically ordered step-by-step explanation, define important terms, show intermediate "
            "calculations or code reasoning, format math in LaTeX ($...$ or $$...$$), and state the final result only after the steps. "
            "Include a simple visual flowchart or diagram in Mermaid syntax (```mermaid ... ```) where appropriate."
        )

    # Adapt pedagogical instructions dynamically based on question domain
    detected_domain = detect_domain(question, subject)

    if detected_domain == "coding":
        domain_instruction = """- SUBJECT FOCUS: PROGRAMMING & CODING
  1. Break down the logic, data structures, and algorithmic strategy first.
  2. Provide clean, well-commented, complete working Python code (do NOT use placeholder stubs).
  3. Walk through line-by-line code explanation and identify common student errors / edge cases.
  4. Specify time complexity O(...) and space complexity O(...).
  5. Conclude with executable driver test cases and expected terminal output in '### 🎯 Final Answer / Complete Solution'."""
    elif detected_domain == "math":
        domain_instruction = """- SUBJECT FOCUS: MATHEMATICAL REASONING & DERIVATIONS
  1. Formalize the problem statement and identify governing mathematical theorems, axioms, and formulas.
  2. Format all equations and mathematical variables using LaTeX ($...$ inline or $$...$$ display blocks).
  3. Show every intermediate algebraic transformation step-by-step; never skip calculation steps.
  4. Provide geometric or algebraic intuition so the student understands *why* the method works.
  5. Conclude with the explicit, simplified final mathematical answer in '### 🎯 Final Answer / Complete Solution'."""
    else:
        domain_instruction = """- SUBJECT FOCUS: COMPREHENSIVE CONCEPTUAL & THEORETICAL EXPLANATION ACROSS ANY FIELD / DISCIPLINE
  1. Provide a thorough, academically rigorous explanation strictly centered on the student's question and proper academic domain (Science, Engineering, Mathematics, Humanities, Economics, etc.). Do NOT force code blocks or unrelated computer architecture analogies unless requested.
  2. Begin with a clear, authoritative definition and executive summary of what the concept is and why it matters in its field.
  3. Detail the governing principles, step-by-step scientific mechanisms, chronological events, or underlying theoretical laws relevant to the question.
  4. Provide an intuitive, domain-appropriate analogy to make abstract concepts concrete.
  5. Discuss practical applications, real-world examples, or comparative trade-offs relevant to the discipline.
  6. Conclude with high-yield exam takeaways and key summary points in '### 🎯 Key Academic Takeaways / Summary'."""

    prompt = f"""
Student context:
- Subject: {subject}
- Topic: {topic or "Not specified"}
- Skill level: {level}
- Preferred language: {language}
- Help mode: {mode}

Student question:
{question}

Student's attempt (if provided):
{attempt or "No attempt provided."}

Instructions:
{mode_instruction}

Teaching requirements:
- Use clear, student-friendly language appropriate to the stated skill level ({level}).
- Answer strictly and directly about the concept requested by the student; never divert to unrelated topics or fields.
{domain_instruction}
- Ask one brief follow-up question to check understanding before moving to the next concept.
- Do not claim that code was run or a calculation was independently verified unless it actually was.
- If the question is ambiguous, state the ambiguity and ask for clarification.
- Clearly mark assumptions and uncertainty. Do not fabricate references.
"""
    result = ask_llm(prompt, api_key=api_key, model=model)

    # Persist in SQLite database
    if persist and question and result:
        try:
            save_doubt(
                question=question,
                answer=result,
                subject=subject,
                topic=topic,
                level=level,
                mode=mode,
                attempt=attempt
            )
        except Exception:
            pass

    return result

def answer_followup(
    original_question: str,
    original_answer: str,
    followup_question: str,
    subject: str,
    api_key: str,
    model: str
) -> str:
    """Answers a student's follow-up question within the same conversation thread."""
    prompt = f"""
You are continuing a tutoring session with a GMRIT engineering student.

Context:
Subject: {subject}

Previous Question:
{original_question}

Your Previous Explanation:
{original_answer}

Student's Follow-up Question:
{followup_question}

Instructions:
Address the follow-up directly, building on the earlier context. If they are asking for simpler terms, use an intuitive analogy. If they want a code example or math derivation, provide clean, step-by-step reasoning.
"""
    return ask_llm(prompt, api_key=api_key, model=model)

def generate_interactive_quiz(
    subject: str,
    topic: str,
    level: str,
    num_questions: int = 3,
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini"
) -> List[Dict[str, Any]]:
    """Generates structured quiz questions via LLM or offline question bank."""
    clean_key = (api_key or "").strip()
    
    if clean_key:
        prompt = f"""
Generate an interactive multiple-choice quiz for an undergraduate engineering student.
Subject: {subject}
Topic: {topic or "Core concepts in " + subject}
Difficulty Level: {level}
Number of Questions: {num_questions}

Respond strictly with valid JSON conforming to this schema (no extra markdown outside the JSON block):
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0,
    "explanation": "Why Option A is correct and other options are incorrect."
  }}
]
The 'correct' field must be an integer index (0, 1, 2, or 3) indicating the correct option in 'options'.
"""
        try:
            raw_response = ask_llm(prompt, api_key=clean_key, model=model)
            clean_json = raw_response.strip()
            if clean_json.startswith("```json"):
                clean_json = clean_json[7:]
            if clean_json.startswith("```"):
                clean_json = clean_json[3:]
            if clean_json.endswith("```"):
                clean_json = clean_json[:-3]
            clean_json = clean_json.strip()
            
            parsed = json.loads(clean_json)
            if isinstance(parsed, list) and len(parsed) > 0 and "question" in parsed[0]:
                return parsed[:num_questions]
        except Exception:
            pass

    # Fallback to curated offline bank with topic-aware prioritization
    bank = OFFLINE_QUIZ_BANK.get(subject, OFFLINE_QUIZ_BANK["Programming"])

    clean_topic = (topic or "").strip().lower()
    if clean_topic and clean_topic not in ["general", "all", "not specified"]:
        matched = []
        for q in bank:
            q_topic = q.get("topic", "").lower()
            q_tags = [t.lower() for t in q.get("tags", [])]
            q_text = q.get("question", "").lower()
            if (clean_topic == q_topic or
                clean_topic in q_topic or
                clean_topic in q_tags or
                any(clean_topic in tag for tag in q_tags) or
                clean_topic in q_text or
                any(word in q_text for word in clean_topic.split() if len(word) > 2)):
                matched.append(q)

        if matched:
            if len(matched) >= num_questions:
                return matched[:num_questions]
            remaining = [q for q in bank if q not in matched]
            return (matched + remaining)[:num_questions]

    selected = bank[:min(num_questions, len(bank))]
    return selected

def generate_lesson_summary(
    subject: str,
    topics_covered: List[str],
    doubts_count: int,
    quiz_score: Optional[float] = None,
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini"
) -> str:
    """Generates a structured lesson completion summary with concepts, mistakes, and revision advice."""
    prompt = f"""
Generate a structured Lesson-Completion Summary for a GMRIT engineering student.

Context:
- Subject: {subject}
- Topics Covered in Session: {', '.join(topics_covered) if topics_covered else 'Core concepts'}
- Doubts Resolved: {doubts_count}
- Quiz Performance: {f"{quiz_score}%" if quiz_score is not None else "Not attempted yet"}

Structure your response into:
1. 🎓 **Core Concepts Mastered**: Bulleted summary of the key principles covered.
2. ⚠️ **Common Mistakes & Misconceptions Identified**: Typical pitfalls (e.g. edge cases, off-by-one, formula signs).
3. 📌 **Recommended Topics for Revision**: 2-3 specific topics to review next to solidify knowledge.
4. 🚀 **Next Challenge Action**: Encouraging closing action for the student.
"""
    return ask_llm(prompt, api_key=api_key, model=model)
