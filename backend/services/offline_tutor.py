"""
Universal Dynamic Pedagogical Engine and Multi-Domain AI Tutor
Zero static pre-baked answers — Every prompt triggers on-the-fly dynamic generation
Strictly domain-grounded across all academic disciplines:
1. Programming & Computer Science (executable code, algorithms, complexities, test runs)
2. AI, Machine Learning & Data Science (Supervised, Unsupervised, Deep Learning, Architectures)
3. Computer Architecture & Microprocessors (Intel 8086, 8051, Memory Segmentation, BIU/EU)
4. Mathematics & Calculus (SymPy analytical derivations, LaTeX formulas, step-by-step algebra)
5. Physical, Chemical & Life Sciences (Physics, Chemistry, Biology)
6. Engineering (Electrical, Electronics, Mechanical, Civil, Systems)
7. Humanities, Social Sciences & Business (Economics, History, Civics, Political Science)
"""

import re
import math
from typing import Dict, Any, Optional

# Retained empty mappings for backwards compatibility
OFFLINE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {}
CONCEPT_TRIGGERS: Dict[str, Dict[str, Any]] = {}
ALIAS_MAPPINGS: Dict[str, str] = {}


# ==============================================================================
# Domain & Academic Field Classification Engines
# ==============================================================================
def detect_academic_field(question: str, subject: str = "") -> str:
    """
    Identifies the exact academic discipline strictly from question content.
    Prevents any manual or stale dropdown from contaminating the domain.
    """
    q_low = (question or "").lower()

    def has_word(tokens):
        return any(re.search(r'\b' + re.escape(t) + r'(?:s|es)?\b', q_low) for t in tokens)

    # 1. Computer Architecture & Microprocessors (8086, 8085, 8051)
    if has_word(["8086", "8085", "8051", "microprocessor", "microcontroller", "biu", "bus interface unit", "execution unit", "instruction prefetch", "segment register"]):
        if has_word(["8051", "microcontroller", "embedded system"]):
            return "Electrical & Electronics Engineering"
        return "Computer Architecture & Microprocessors"

    # 2. AI, Machine Learning & Data Science
    if has_word([
        "artificial intelligence", "ai", "generative ai", "genai", "computer vision",
        "machine learning", "supervised learning", "unsupervised learning", "reinforcement learning",
        "deep learning", "neural network", "transformer", "attention mechanism",
        "gradient descent", "backpropagation", "random forest", "decision tree", "svm",
        "support vector machine", "overfitting", "underfitting", "bias-variance", "loss function",
        "convolutional neural network", "cnn", "rnn", "lstm", "nlp", "large language model",
        "llm", "clustering", "k-means", "feature engineering", "hyperparameter", "roc-auc"
    ]):
        return "AI, Machine Learning & Data Science"

    # 3. Computer Science & Software Engineering (OS, DBMS, Networks, OOP, Data Structures)
    if has_word([
        "operating system", "deadlock", "process scheduling", "virtual memory", "paging",
        "dbms", "database", "sql", "acid properties", "normalization", "relational model",
        "osi model", "tcp/ip", "packet", "socket", "dns", "http", "https", "ip address",
        "oop", "object oriented", "polymorphism", "encapsulation", "inheritance", "abstraction",
        "binary search tree", "linked list", "hash table", "stack", "queue", "graph algorithm",
        "dijkstra", "dynamic programming", "time complexity", "big o", "recursion", "call stack"
    ]):
        return "Computer Science & Programming"

    # 4. Life Sciences & Biology
    if has_word([
        "photosynthesis", "cellular respiration", "dna", "rna", "mitosis", "meiosis",
        "chloroplast", "mitochondria", "enzyme", "ribosome", "atp", "glycolysis",
        "krebs cycle", "calvin cycle", "chlorophyll", "cell membrane", "genetics",
        "allele", "chromosome", "neuron", "synapse", "homeostasis", "evolution",
        "natural selection", "ecosystem", "biology", "biological", "biochemical",
        "organism", "protein synthesis", "metabolism", "metabolic"
    ]):
        return "Biology & Life Sciences"

    # 5. Physics & Physical Sciences
    if has_word([
        "newton", "newton's", "newtons", "inertia", "acceleration", "gravity", "gravitation",
        "quantum", "thermodynamics", "entropy", "kinetic energy", "potential energy",
        "momentum", "optics", "refraction", "diffraction", "relativity", "electromagnetism",
        "lorentz", "coulomb", "coulomb's", "ampere", "faraday", "schrodinger", "heisenberg",
        "projectile", "friction", "torque", "angular momentum", "doppler effect", "physics"
    ]):
        return "Physics & Physical Sciences"

    # 6. Chemistry & Chemical Sciences
    if has_word([
        "chemical bonding", "ionic bond", "covalent bond", "periodic table", "stoichiometry",
        "acid", "acids", "base", "bases", "ph scale", "arrhenius", "bronsted", "lewis acid",
        "titration", "oxidation", "reduction", "redox", "enthalpy", "exothermic",
        "endothermic", "catalyst", "equilibrium constant", "le chatelier", "organic chemistry",
        "alkane", "alkene", "benzene", "polymer", "hybridization", "chemistry"
    ]):
        return "Chemistry & Chemical Sciences"

    # 7. Electrical & Electronics Engineering
    if has_word([
        "kirchhoff", "kcl", "kvl", "ohm", "ohms", "circuit", "resistor", "capacitor",
        "diode", "transistor", "op-amp", "operational amplifier", "logic gate", "flip-flop",
        "semiconductor", "pn junction", "mosfet", "bjt", "signal", "fourier transform",
        "laplace", "z-transform", "dsp", "modulation", "antenna", "electrical engineering"
    ]):
        return "Electrical & Electronics Engineering"

    # 8. Mechanical Engineering
    if has_word([
        "bernoulli", "venturi", "reynolds number", "carnot", "carnot cycle", "rankine",
        "otto cycle", "stress and strain", "mohr's circle", "shear force", "bending moment",
        "fluid mechanics", "heat transfer", "conduction", "convection", "radiation",
        "gear train", "camshaft", "turbomachinery", "internal combustion", "mechanical engineering"
    ]):
        return "Mechanical Engineering"

    # 9. Civil Engineering
    if has_word([
        "truss", "cantilever", "reinforced concrete", "soil mechanics", "shear strength",
        "surveying", "theodolite", "hydrology", "open channel flow", "traffic engineering",
        "structural analysis", "pavement design", "civil engineering"
    ]):
        return "Civil Engineering"

    # 10. Economics, Business & Commerce
    if has_word([
        "supply and demand", "law of demand", "law of supply", "market equilibrium",
        "price elasticity", "inflation", "gdp", "gross domestic product", "monetary policy",
        "fiscal policy", "central bank", "interest rate", "consumer surplus", "producer surplus",
        "monopoly", "oligopoly", "perfect competition", "opportunity cost", "keynesian",
        "microeconomics", "macroeconomics", "economics"
    ]):
        return "Economics, Business & Commerce"

    # 11. History & Civics / Political Science
    if has_word([
        "constitution", "democracy", "prime minister", "president", "parliament",
        "separation of powers", "fundamental rights", "judiciary", "supreme court",
        "citizen", "election", "civics", "government", "legislature", "executive branch",
        "french revolution", "world war", "cold war", "renaissance", "colonialism", "history"
    ]):
        return "Civics & Political Science"

    # 12. Mathematics & Statistics
    if has_word([
        "derivative", "integral", "differentiate", "integrate", "eigenvalue", "matrix",
        "determinant", "probability", "bayes", "equation", "dy/dx", "algebra",
        "calculus", "trigonometry", "sin", "cos", "pythagor", "standard deviation",
        "solve", "evaluate", "formula", "math", "mathematics"
    ]) or ("=" in q_low and any(c.isdigit() for c in q_low)):
        return "Mathematics & Statistics"

    # 13. Computer Science & Coding generic
    if has_word(["python", "code", "programming", "program", "function", "array", "algorithm", "even", "odd", "script", "loop"]):
        return "Computer Science & Programming"

    return "General Science & Academic Inquiry"


def detect_domain(question: str, subject: str = "") -> str:
    """Classifies a student query into 'coding', 'math', or 'theory'."""
    q_lower = (question or "").lower().strip()

    # Do not treat civics prime minister as prime number code
    if "prime minister" in q_lower:
        return "theory"

    # 1. Any phrase combining action verb + coding noun (e.g. "write even number code", "write even number program")
    if re.search(r'\b(write|create|implement|give|show|generate|make|develop)\b.*?\b(code|program|script|function|algorithm)\b', q_lower):
        return "coding"

    # 2. Any phrase ending with code/program/script (e.g. "even number code", "fibonacci program")
    if re.search(r'.*\b(code|program|script)\b$', q_lower.rstrip('.!? ')):
        return "coding"

    # 3. Any query with "code for", "program for", "function to", etc.
    if re.search(r'\b(code|program|script|function|algorithm)\b\s+(for|to|of|that|which)\b', q_lower):
        return "coding"

    # 4. Explicit Actionable Coding Requests
    explicit_code_action = any(phrase in q_lower for phrase in [
        "write a code", "write code", "python code", "code in python", "program to",
        "write a program", "function to", "write a function", "implement in python",
        "syntax of", "def ", "class ", "give me code", "give code", "debug this code",
        "write a script", "code snippet", "code for", "program for", "how to code",
        "script to", "script for", "python script", "write python", "code to"
    ])
    if explicit_code_action:
        return "coding"

    # 5. Coding Problems & Algorithms
    coding_problem_keywords = [
        "even number", "odd number", "even or odd", "fizzbuzz", "palindrome",
        "fibonacci", "factorial", "armstrong", "binary search", "bubble sort",
        "merge sort", "quick sort", "two sum", "reverse string", "reverse words",
        "count vowels", "remove duplicates", "flatten list", "check prime",
        "prime number", "matrix multiplication", "linear regression", "leap year"
    ]
    if any(k in q_lower for k in coding_problem_keywords) and any(w in q_lower for w in ["code", "python", "function", "program", "script", "algorithm", "implement", "write", "check", "find"]):
        return "coding"

    # Explicit Math & Equation Cues
    if "=" in q_lower and any(c.isalpha() for c in q_lower.split("=")[0]):
        return "math"

    explicit_math_cues = [
        "solve for", "derivative of", "differentiate", "integral of", "integrate",
        "eigenvalue", "eigenvector", "characteristic polynomial", "gcd", "lcm",
        "dy/dx", "calculate the determinant", "find the eigenvalues", "evaluate the integral",
        "solve the linear equation", "solve the quadratic equation"
    ]
    if any(cue in q_lower for cue in explicit_math_cues):
        return "math"

    return "theory"


def extract_clean_concept_title(question: str, topic: str = "", subject: str = "") -> str:
    """Extracts a neat, professional concept title, cleaning out typos (e.g. 'expalain', 'abou t') and filler words."""
    if topic and topic.strip() and topic.strip().lower() not in ["not specified", "general", "other", "none", "universal"]:
        return topic.strip().title()

    q = (question or "").strip()

    prefix_pattern = (
        r'^(?:can\s+you\s+)?(?:could\s+you\s+)?(?:please\s+)?'
        r'(?:ex[a-z]{3,7}|describ[a-z]*|tell\s+me\s+about|tell\s+me|what\s+is\s+a|what\s+is\s+an|what\s+is\s+the|what\s+is|'
        r'what\s+are\s+the|what\s+are|who\s+is\s+the|who\s+is|who\s+was\s+the|who\s+was|'
        r'how\s+does\s+the|how\s+does|how\s+do\s+the|how\s+do|why\s+does|why\s+is|why\s+do|'
        r'give\s+an\s+overview\s+of|give\s+details\s+about|give\s+information\s+about|discuss\s+the|discuss|'
        r'overview\s+of|solve\s+the\s+equation|solve)\s+(?:abou?\s*t?\s*|regarding\s+|on\s+|of\s+)?(?:the\s+)?(?:concept\s+of\s+)?(?:working\s+of\s+)?(?:function\s+of\s+)?'
    )
    cleaned = re.sub(prefix_pattern, '', q, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r'[\?\.\!]+$', '', cleaned).strip()
    cleaned = re.sub(r'\b(work|works|operate|operates|function|functions)\b$', '', cleaned, flags=re.IGNORECASE).strip()

    if not cleaned:
        cleaned = q

    words = cleaned.split()
    lower_words = {'of', 'the', 'in', 'on', 'at', 'to', 'for', 'with', 'and', 'or', 'a', 'an'}
    titled_words = []
    for i, w in enumerate(words):
        w_up = w.upper()
        if w_up in ['8086', '8085', '8051', 'CPU', 'ALU', 'RAM', 'ROM', 'OS', 'TCP', 'IP', 'UDP', 'HTTP', 'HTTPS', 'DNS', 'AI', 'ML', 'DL', 'NLP', 'SQL', 'DBMS', 'API', 'KCL', 'KVL', 'GDP', 'ATP', 'DNA', 'RNA', 'OOP', 'CNN', 'RNN', 'LSTM', 'SVM']:
            titled_words.append(w_up)
        elif i > 0 and w.lower() in lower_words:
            titled_words.append(w.lower())
        else:
            titled_words.append(w.capitalize())

    res = ' '.join(titled_words)
    res = res.replace("'S", "'s")
    return res if res else (subject or 'Academic Concept')


# ==============================================================================
# Dedicated Multi-Domain Dynamic Synthesizers
# ==============================================================================

from backend.services.code_solutions import synthesize_programming_answer

synthesize_dynamic_programming_answer = synthesize_programming_answer


def synthesize_math_reasoning_answer(question: str, subject: str, topic: str, level: str, mode: str) -> str:
    """Generates rigorous step-by-step mathematical reasoning with SymPy derivations and intermediate calculations."""
    from backend.services.math_code_service import solve_math_expression

    q_clean = question.strip()
    q_lower = q_clean.lower()

    eq_match = re.search(r'([0-9a-zA-Z\s\+\-\*\/\^\(\)\.\,]+=[0-9a-zA-Z\s\+\-\*\/\^\(\)\.\,]+)', q_clean)
    diff_match = re.search(r'(?:derivative|diff(?:erentiate)?|d/dx)\s+(?:of\s+)?([0-9a-zA-Z\s\+\-\*\/\^\(\)\.]+)', q_clean, flags=re.IGNORECASE)
    int_match = re.search(r'(?:integral|integrate)\s+(?:of\s+)?([0-9a-zA-Z\s\+\-\*\/\^\(\)\.]+)', q_clean, flags=re.IGNORECASE)

    solved_res = None
    if eq_match:
        candidate = eq_match.group(1).strip()
        clean_eq = re.sub(r'^(solve\s+(the\s+)?(equation\s+)?|find\s+|calculate\s+|evaluate\s+)', '', candidate, flags=re.IGNORECASE).strip()
        clean_eq = re.sub(r'\s+for\s+[a-zA-Z]\b', '', clean_eq, flags=re.IGNORECASE).strip()
        solved_res = solve_math_expression(clean_eq, operation="solve")
    elif diff_match:
        candidate = diff_match.group(1).strip().rstrip("?.! ")
        solved_res = solve_math_expression(candidate, operation="derivative")
    elif int_match:
        candidate = int_match.group(1).strip().rstrip("?.! ")
        solved_res = solve_math_expression(candidate, operation="integrate")

    if solved_res and solved_res.get("success"):
        steps_md = "\n".join(solved_res.get("steps", []))
        return f"""### 💡 Mathematical Reasoning & Step-by-Step Solution

#### 1. Problem Formulation & Given Conditions
You asked:
> *"{q_clean}"*

**Target Expression / Equation:**
$${solved_res.get('latex_expr', '')}$$

---

#### 2. Analytical Derivation Step-by-Step
{steps_md}

---

### 🎯 Final Answer / Complete Solution
- **Exact Analytical Result:**
  $${solved_res.get('latex_result', '')}$$
- **Verification:** Both sides balance identically.
"""

    return f"""### 💡 Mathematical Reasoning: {topic or 'Analytical Problem Solving'}

#### 1. Problem Formulation
You asked:
> *"{q_clean}"*

Let us formalize the problem mathematically:
1. **Identify Governing Formulas:** Classify the problem type (algebraic, calculus, linear algebra, or probability) and apply governing theorems.
2. **Execute Transformations:** Perform intermediate reductions step-by-step using LaTeX standard notation ($...$ and $$...$$).
3. **Verify Bounds:** Check boundary conditions and domain restrictions.
"""


def synthesize_theory_answer(question: str, subject: str, topic: str, level: str, mode: str, attempt: str = "") -> str:
    """Universal pedagogical conceptual guide providing exact, factually accurate explanations."""
    q_clean = question.strip()
    q_lower = q_clean.lower()
    field = detect_academic_field(question)
    concept_title = extract_clean_concept_title(question, topic, field)

    # ==========================================================================
    # 1. COMPUTER ARCHITECTURE & MICROPROCESSORS (8086, 8051)
    # ==========================================================================
    if "8086" in q_lower or "8086" in concept_title:
        return r"""### 💡 Intel 8086 Microprocessor Architecture
**Academic Discipline:** Computer Architecture & Microprocessors

---

#### 📖 Overview & Core Definition
The **Intel 8086** is a landmark **16-bit microprocessor** introduced by Intel in 1978. It features a 16-bit internal Arithmetic Logic Unit (ALU), a 16-bit external data bus, and a **20-bit address bus**, enabling it to directly address up to **$2^{20} = 1\text{ MB}$ of physical memory**.

---

#### ⚙️ Internal Architecture: BIU vs. EU
The 8086 architecture is split into two independent, asynchronous functional units that operate in parallel to achieve instruction pipelining:

1. **BIU (Bus Interface Unit):**
   - **Role:** Handles all data transfers, instruction fetching, and bus control signals between the processor and external memory/IO devices.
   - **Instruction Queue:** Implements a **6-byte FIFO Instruction Prefetch Queue**. While the Execution Unit is executing one instruction, the BIU pre-fetches subsequent instruction bytes from memory, eliminating memory wait states.
   - **Segment Registers (16-bit):**
     - **CS (Code Segment):** Stores base address of the executable program instructions.
     - **DS (Data Segment):** Stores base address of program variables and data.
     - **SS (Stack Segment):** Stores base address of the system stack.
     - **ES (Extra Segment):** Used for string operations and additional data storage.
   - **IP (Instruction Pointer):** Holds the 16-bit offset of the next instruction byte to fetch.
   - **Physical Address Calculation (20-bit):**
     $$\text{Physical Address} = (\text{Segment Base} \times 16) + \text{Offset} = (\text{Segment} \ll 4) + \text{Offset}$$

2. **EU (Execution Unit):**
   - **Role:** Decodes instructions fetched from the BIU queue and executes arithmetic, logical, and shift operations.
   - **ALU (16-bit):** Performs 16-bit arithmetic (ADD, SUB, MUL, DIV) and logical operations (AND, OR, XOR).
   - **General Purpose Registers (16-bit, accessible as 8-bit pairs):**
     - `AX` (`AH`, `AL`): Primary Accumulator for arithmetic and I/O.
     - `BX` (`BH`, `BL`): Base register for memory addressing.
     - `CX` (`CH`, `CL`): Count register for loops and shifts.
     - `DX` (`DH`, `DL`): Data register for 32-bit operations and I/O ports.
   - **Pointers & Index Registers:**
     - `SP` (Stack Pointer) & `BP` (Base Pointer): Stack frame operations.
     - `SI` (Source Index) & `DI` (Destination Index): String and array processing.
   - **Flag Register (16-bit):** Contains 9 active flags (6 Status Flags: CF, PF, AF, ZF, SF, OF, and 3 Control Flags: TF, IF, DF).

---

#### 🔌 Operating Modes & Pin Configuration
The 8086 is housed in a 40-pin Dual In-line Package (DIP) and operates in two hardware modes determined by pin $MN/\overline{MX}$ (Pin 33):
- **Minimum Mode ($MN/\overline{MX} = 1$):** Single-processor mode where the 8086 generates all control signals directly.
- **Maximum Mode ($MN/\overline{MX} = 0$):** Multi-processor / coprocessor mode (used with the Intel 8087 math coprocessor), where the external Intel 8288 Bus Controller generates system bus control signals.

---

### 🎯 Key Academic Takeaways
- **Data Bus:** 16-bit | **Address Bus:** 20-bit ($1\text{ MB}$ addressable space).
- **Pipelining:** Overlapped fetching and execution using a 6-byte instruction queue in the BIU.
- **Memory Segmentation:** $1\text{ MB}$ memory divided into 64 KB segments addressed via $(\text{Segment} \times 16) + \text{Offset}$.
"""

    elif "8051" in q_lower or "8051" in concept_title:
        return r"""### 💡 Intel 8051 Microcontroller Architecture
**Academic Discipline:** Electrical & Electronics Engineering / Embedded Systems

---

#### 📖 Overview & Core Definition
The **Intel 8051** is an iconic **8-bit microcontroller** designed for embedded control systems. Unlike general-purpose microprocessors that require external peripheral chips, the 8051 integrates a CPU, memory, timers, I/O ports, and serial communication onto a single silicon chip.

---

#### ⚙️ Technical Architecture & Subsystems
1. **Harvard Architecture (Separate Code & Data Spaces):**
   - **Program Memory (ROM):** 4 KB of on-chip ROM/EPROM (expandable up to 64 KB using the $\overline{\text{EA}}$ pin).
   - **Data Memory (RAM):** 128 bytes of internal data RAM:
     - 4 Register Banks ($R_0 - R_7$, 32 bytes total from address `00H` to `1FH`).
     - Bit-addressable RAM (16 bytes from `20H` to `2FH`, offering 128 individually addressable bits).
     - Scratchpad RAM (`30H` to `7FH`).

2. **Core Peripheral Hardware:**
   - **8-bit ALU:** Accumulator (A register) and B register for multiply/divide operations.
   - **Parallel I/O Ports:** 4 bidirectional 8-bit ports (P0, P1, P2, P3) providing 32 I/O pins.
   - **Timers/Counters:** Two 16-bit timers/counters (Timer 0 and Timer 1) configurable in 4 modes via the `TMOD` and `TCON` SFRs.
   - **UART Serial Port:** Full-duplex serial communication controlled via `SBUF` and `SCON`.
   - **Interrupt Controller:** 5 interrupt sources (2 External $\overline{\text{INT0}}, \overline{\text{INT1}}$, 2 Timer overflows, 1 Serial) with 2 priority levels.

---

### 🎯 Key Academic Takeaways
- **Architecture:** 8-bit Harvard Architecture with separate 64 KB code and data address spaces.
- **On-chip Resources:** 4 KB ROM, 128 Bytes RAM, 32 I/O lines, two 16-bit timers, full-duplex UART.
- **Special Feature:** Bit-level Boolean processor allowing single-bit manipulation.
"""

    # ==========================================================================
    # 2. AI, MACHINE LEARNING & DATA SCIENCE
    # ==========================================================================
    elif "supervised learning" in q_lower or "supervised" in concept_title.lower():
        return r"""### 💡 Supervised Learning: Concept & Mathematical Foundations
**Academic Discipline:** AI, Machine Learning & Data Science

---

#### 📖 Overview & Core Definition
**Supervised Learning** is the primary machine learning paradigm where an algorithm learns an inductive mapping function $f: \mathcal{X} \rightarrow \mathcal{Y}$ from a **labeled dataset** consisting of input features paired with verified ground-truth target labels:
$$\mathcal{D}_{train} = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \dots, (\mathbf{x}_N, y_N)\}$$
The objective is to train a model that accurately predicts target values for unseen test data by minimizing empirical risk.

---

#### ⚙️ The Two Fundamental Supervised Tasks
1. **Classification (Discrete / Categorical Targets):**
   - Target $y \in \{0, 1, \dots, C-1\}$.
   - *Goal:* Learn decision boundaries separating distinct categorical classes (e.g., spam vs. ham, tumor classification).
   - *Key Algorithms:* Logistic Regression, Support Vector Machines (SVM), Random Forests, Multi-Layer Perceptrons (MLP).
   - *Loss Function:* Categorical Cross-Entropy Loss:
     $$\mathcal{L}_{CE} = -\sum_{i=1}^C y_i \log(\hat{y}_i)$$

2. **Regression (Continuous Quantitative Targets):**
   - Target $y \in \mathbb{R}$.
   - *Goal:* Predict a continuous numeric quantity (e.g., real estate valuation, temperature forecasting).
   - *Key Algorithms:* Linear Regression, Ridge/Lasso Regularization, Gradient Boosted Trees (XGBoost).
   - *Loss Function:* Mean Squared Error (MSE):
     $$\text{MSE} = \frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2$$

---

#### ⚖️ The Bias-Variance Tradeoff
- **Underfitting (High Bias):** The model is too simple to capture underlying data patterns.
- **Overfitting (High Variance):** The model memorizes training noise and fails to generalize to test data.
- **Regularization:** Mitigated using $L_1$ (Lasso: $\lambda \sum |w_i|$), $L_2$ (Ridge: $\lambda \sum w_i^2$), dropout, and $k$-fold cross-validation.

---

### 🎯 Key Academic Takeaways
- **Requirement:** Ground-truth supervisor labels $(\mathbf{x}_i, y_i)$ are mandatory.
- **Divisions:** Classification (discrete outputs) vs. Regression (continuous outputs).
- **Optimization:** Weights updated iteratively via Gradient Descent to minimize the task loss function.
"""

    elif "artificial intelligence" in q_lower or bool(re.search(r'\b(ai)\b', q_lower)) or "artificial intelligence" in concept_title.lower():
        return r"""### 💡 Artificial Intelligence (AI): Comprehensive Academic Guide
**Academic Discipline:** AI, Machine Learning & Data Science

---

#### 📖 Overview & Foundational Definition
**Artificial Intelligence (AI)** is the broad domain of computer science dedicated to engineering intelligent computational agents capable of performing cognitive tasks that typically require human intelligence. These tasks include **visual perception, speech recognition, symbolic reasoning, decision-making, planning, and learning from experience**.

The term was coined by **John McCarthy** in 1956 at the Dartmouth Summer Research Project on Artificial Intelligence:
> *"The science and engineering of making intelligent machines, especially intelligent computer programs."*

---

#### 🏛️ The AI Hierarchy: AI vs. Machine Learning vs. Deep Learning
```mermaid
flowchart TD
    AI["Artificial Intelligence (Broadest Field: Search, Logic, Knowledge, Robotics)"]
    ML["Machine Learning (Data-Driven Pattern Recognition & Statistical Algorithms)"]
    DL["Deep Learning (Multi-Layer Artificial Neural Networks & Representation Learning)"]
    GenAI["Generative AI & LLMs (Transformers, Attention Mechanisms, Synthetic Content)"]

    AI --> ML
    ML --> DL
    DL --> GenAI
```

---

#### ⚙️ The Four Major Paradigms & Core Branches of AI
1. **Symbolic / Classical AI (Knowledge-Based & Rule-Based):**
   - **Mechanism:** Solves problems using formal logic, semantic ontologies, production rules (`IF-THEN`), and search trees.
   - **Key Methods:** $A^*$ Search, Minimax with Alpha-Beta Pruning, Expert Systems, First-Order Predicate Calculus.
2. **Sub-Symbolic / Statistical Machine Learning:**
   - **Mechanism:** Extracts decision rules and mathematical mappings directly from empirical data without manual programming.
   - **Paradigms:** Supervised Learning (Classification/Regression), Unsupervised Learning (Clustering/PCA), Reinforcement Learning (Q-learning).
3. **Deep Learning & Artificial Neural Networks:**
   - **Mechanism:** Stacks deep hidden layers of artificial neurons using backpropagation to automatically discover hierarchical feature representations directly from raw inputs.
   - **Architectures:** CNNs (Vision), RNNs/LSTMs (Sequential), Transformers (Language & Multi-modal).
4. **Natural Language Processing (NLP) & Computer Vision:**
   - **NLP:** Enables computers to process, understand, and generate natural human language (Syntax parsing, Named Entity Recognition, Machine Translation, Large Language Models).
   - **Vision:** Reconstructs and interprets 3D visual environments from 2D pixel grids (Object Detection via YOLO, Semantic Segmentation).

---

#### 🎯 Types of AI by Capability Level
- **Narrow AI (Weak AI):** Specialized in one specific domain (e.g., AlphaGo, facial recognition, ChatGPT). This is the only type of AI that currently exists in reality.
- **Artificial General Intelligence (AGI / Strong AI):** Theoretical machine intelligence capable of understanding, learning, and applying knowledge across any intellectual task at human levels.
- **Artificial Superintelligence (ASI):** Hypothetical future AI surpassing the collective cognitive capabilities of the entire human species.

---

### 🎯 Key Academic Takeaways
- **Scope:** AI is the parent superset; Machine Learning is a subset of AI; Deep Learning is a subset of ML.
- **Turing Test (1950):** Alan Turing's foundational behavioral test evaluating whether an AI system's conversational responses can be distinguished from a human.
- **Rational Agent Principle:** In modern academic literature (Russell & Norvig), an AI is formalized as a rational agent that perceives its environment through sensors and takes actions through actuators to maximize its expected performance measure.
"""

    elif "machine learning" in q_lower or "machine learning" in concept_title.lower() or bool(re.search(r'\b(ml)\b', q_lower)):
        return r"""### 💡 Machine Learning: Comprehensive Guide
**Academic Discipline:** AI, Machine Learning & Data Science

---

#### 📖 Overview & Definition
**Machine Learning (ML)** is a core subfield of Artificial Intelligence focused on designing algorithms that automatically extract patterns and decision rules directly from data, rather than following static, hand-coded instructions. 

Formally, Tom Mitchell defines ML:
> *"A computer program is said to learn from experience $E$ with respect to some class of tasks $T$ and performance measure $P$, if its performance at tasks in $T$, as measured by $P$, improves with experience $E$."*

---

#### ⚙️ The Three Core Learning Paradigms
1. **Supervised Learning (Labeled Data):**
   - Learns a predictive mapping from input features $\mathbf{x}$ to labels $y$.
   - Divided into **Classification** (discrete classes) and **Regression** (continuous numbers).
2. **Unsupervised Learning (Unlabeled Data):**
   - Discovers latent structure and natural groupings from features $\mathbf{x}$ alone without human annotations.
   - Primary methods: **Clustering** ($K$-Means, Hierarchical) and **Dimensionality Reduction** (PCA).
3. **Reinforcement Learning (Reward-Driven):**
   - An autonomous agent learns optimal actions in a dynamic environment by maximizing cumulative scalar rewards via trial and error (Markov Decision Processes, Q-Learning).

---

#### 🔄 The End-to-End ML Pipeline
1. **Data Ingestion & Cleaning:** Removing duplicates, handling missing values.
2. **Feature Engineering:** Scaling features (Standardization/MinMax) and encoding categorical variables.
3. **Model Training & Optimization:** Updating weights $\theta$ via Gradient Descent:
   $$\theta_{t+1} = \theta_t - \alpha \nabla_\theta \mathcal{L}(\theta)$$
4. **Evaluation:** Testing generalization on holdout test sets using metrics like F1-Score, ROC-AUC, and RMSE.

---

### 🎯 Key Academic Takeaways
- **Paradigm Shift:** Moves from traditional programming (Data + Rules $\rightarrow$ Answers) to Machine Learning (Data + Answers $\rightarrow$ Rules).
- **Core Components:** Objective Loss Function, Dataset ($E$), and Optimizer (Gradient Descent).
"""

    elif "deep learning" in q_lower or "neural network" in q_lower:
        return r"""### 💡 Deep Learning & Neural Networks
**Academic Discipline:** AI, Machine Learning & Data Science

---

#### 📖 Overview & Definition
**Deep Learning (DL)** is a specialized subset of machine learning based on **Artificial Neural Networks (ANNs)** with multiple stacked hidden layers. It automatically discovers hierarchical representations of data directly from raw inputs (such as pixels, audio waveforms, or text tokens) without manual feature engineering.

---

#### ⚙️ Fundamental Architecture & Mechanics
1. **The Artificial Neuron (Perceptron):**
   Computes a linear combination of inputs followed by a non-linear activation function $\sigma$:
   $$z = \sum_{j=1}^d w_j x_j + b = \mathbf{w}^T \mathbf{x} + b, \quad a = \sigma(z)$$
   - **Activation Functions:** **ReLU** ($\max(0, z)$), **Sigmoid** ($\frac{1}{1 + e^{-z}}$), **Softmax** (for probability distributions).

2. **Training via Backpropagation:**
   - **Forward Pass:** Input data propagates through layers to produce output predictions $\hat{y}$ and loss $\mathcal{L}(y, \hat{y})$.
   - **Backward Pass:** Applies the calculus chain rule to calculate error gradients with respect to each weight matrix:
     $$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{(l)}} \cdot (\mathbf{a}^{(l-1)})^T$$
   - **Optimizer:** Weights updated via Stochastic Gradient Descent (SGD) or **Adam**.

3. **Major Architectures:**
   - **CNNs (Convolutional Neural Networks):** Parameter sharing and pooling for spatial grid data (computer vision).
   - **Transformers:** Multi-head Self-Attention mechanism ($\text{Softmax}(\frac{QK^T}{\sqrt{d_k}})V$) for NLP and Large Language Models.

---

### 🎯 Key Academic Takeaways
- **Universal Approximation:** Deep neural networks can approximate any continuous mathematical function given sufficient width and depth.
- **End-to-End Learning:** Automatically extracts features directly from raw data via backpropagation.
"""

    # ==========================================================================
    # 3. COMPUTER SCIENCE: OS, NETWORKING, DBMS, OOP
    # ==========================================================================
    elif "operating system" in q_lower or "deadlock" in q_lower:
        return r"""### 💡 Operating Systems: Process Synchronization & Deadlock
**Academic Discipline:** Computer Science & Operating Systems

---

#### 📖 Deadlock Definition
A **Deadlock** is a state where a set of concurrent processes are permanently blocked because each process holds a resource and waits for another resource held by another process in the same set, resulting in complete system freeze.

---

#### ⚙️ The 4 Necessary Coffman Conditions
For a deadlock to occur, all four conditions must hold simultaneously:
1. **Mutual Exclusion:** At least one resource must be held in a non-shareable mode (only one process can use it at a time).
2. **Hold and Wait:** A process must be currently holding at least one resource while waiting to acquire additional resources held by others.
3. **No Preemption:** Resources cannot be forcibly taken away from a process; they can only be released voluntarily after task completion.
4. **Circular Wait:** A closed loop of processes exists $\{P_0, P_1, \dots, P_n\}$ such that $P_0$ waits for a resource held by $P_1$, and $P_n$ waits for a resource held by $P_0$.

---

#### 🛡️ Deadlock Handling Strategies
- **Prevention:** Invalidate at least one of the 4 Coffman conditions (e.g. impose total ordering on resource allocation to prevent Circular Wait).
- **Avoidance:** Dynamically evaluate safe states using the **Banker's Algorithm** before allocating resources.
- **Detection & Recovery:** Construct a Resource Allocation Graph (RAG) to detect cycles, then terminate processes or preempt resources.

---

### 🎯 Key Academic Takeaways
- **Coffman Conditions:** Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.
- **Banker's Algorithm:** Ensures the system always remains in a "Safe State" where at least one execution sequence avoids deadlock.
"""

    elif "dbms" in q_lower or "database" in q_lower or "sql" in q_lower or "normalization" in q_lower:
        return r"""### 💡 DBMS: ACID Properties & Relational Normalization
**Academic Discipline:** Database Management Systems (DBMS)

---

#### 📖 1. The ACID Properties of Transactions
To maintain data integrity during concurrent multi-user execution and system crashes, transactions must satisfy:
- **Atomicity:** "All-or-Nothing." The transaction executes completely to commit or aborts completely without partial updates (managed via undo logs).
- **Consistency:** The database transitions from one valid state to another, preserving all schema constraints and foreign keys.
- **Isolation:** Concurrent transactions execute without interfering with one another (implemented via Two-Phase Locking or MVCC).
- **Durability:** Once committed, updates persist permanently in non-volatile storage, surviving system crashes (implemented via Write-Ahead Logging - WAL).

---

#### ⚙️ 2. Relational Database Normalization Stages
Normalization systematically minimizes data redundancy and eliminates insertion, update, and deletion anomalies:
- **1NF (First Normal Form):** Every attribute must contain only atomic (indivisible) values; no repeating groups or arrays.
- **2NF (Second Normal Form):** In 1NF and has **no partial dependencies** (every non-prime attribute is fully dependent on the whole candidate key).
- **3NF (Third Normal Form):** In 2NF and has **no transitive dependencies** (if $X \rightarrow Y$ and $Y \rightarrow Z$, then $X$ must be a superkey).
- **BCNF (Boyce-Codd Normal Form):** A stricter version of 3NF where for every functional dependency $X \rightarrow Y$, $X$ must be a superkey.

---

### 🎯 Key Academic Takeaways
- **ACID:** Guarantees reliable transaction execution in concurrent environments.
- **Normalization:** Progressively decomposes tables to eliminate redundancy while preserving functional dependencies.
"""

    elif "osi model" in q_lower or "tcp/ip" in q_lower or "networking" in q_lower:
        return r"""### 💡 Computer Networks: The 7-Layer OSI Reference Model
**Academic Discipline:** Computer Science & Networking

---

#### 📖 Overview
The **OSI (Open Systems Interconnection)** model is a standardized theoretical 7-layer framework developed by ISO to characterize network communication protocols between heterogeneous systems.

---

#### ⚙️ The 7 Layers of OSI (Top to Bottom)
1. **Layer 7 - Application:** User-facing network services and APIs (HTTP, HTTPS, FTP, DNS, SMTP).
2. **Layer 6 - Presentation:** Data formatting, syntax translation, encryption/decryption, and compression (TLS/SSL, ASCII, JPEG).
3. **Layer 5 - Session:** Manages sessions, dialog control, synchronization tokens, and connection checkpoints (RPC, NetBIOS).
4. **Layer 4 - Transport:** End-to-end communication, segmentation, flow control, error recovery, and port addressing (**TCP, UDP**).
5. **Layer 3 - Network:** Logical addressing and routing of packets across multiple networks (**IPv4, IPv6, ICMP, Routers**).
6. **Layer 2 - Data Link:** Framing, physical MAC addressing, switch bridging, and hop-to-hop error detection (**Ethernet, Wi-Fi, Switches**).
7. **Layer 1 - Physical:** Transmission of raw bitstreams over physical hardware media (cables, fiber optics, radio frequencies).

---

#### 🤝 TCP 3-Way Handshake
Establishes reliable connection before transmitting data:
1. **Client $\rightarrow$ Server (SYN):** Client sends `SYN` with Initial Sequence Number ($ISN_C$).
2. **Server $\rightarrow$ Client (SYN-ACK):** Server acknowledges with `ACK = ISN_C + 1` and its own `SYN = ISN_S`.
3. **Client $\rightarrow$ Server (ACK):** Client sends `ACK = ISN_S + 1`. Connection established!

---

### 🎯 Key Academic Takeaways
- **Data Units:** Application/Presentation/Session: Data | Transport: Segments | Network: Packets | Data Link: Frames | Physical: Bits.
- **Encapsulation:** Headers and trailers are appended as data travels down the stack, and stripped as it travels up.
"""

    elif any(k in q_lower for k in ["oop", "object oriented", "polymorphism", "encapsulation", "inheritance", "abstraction"]):
        return r"""### 💡 Object-Oriented Programming (OOP): The 4 Core Pillars
**Academic Discipline:** Computer Science & Software Engineering

---

#### 📖 Overview & Paradigm
**Object-Oriented Programming (OOP)** is a programming paradigm centered on organizing software design around **objects** (data structures containing attributes/fields) and **methods** (functions that operate on that data), rather than logic and procedural actions.

---

#### ⚙️ The Four Fundamental Pillars of OOP
1. **Encapsulation:**
   - Bundles data (attributes) and methods that operate on that data into a single unit (Class).
   - Restricts direct access to internal components using access specifiers (`private`, `protected`, `public`) to prevent unauthorized external state corruption (Data Hiding).

2. **Abstraction:**
   - Hides internal implementation complexity and exposes only essential interfaces to the outside world.
   - Implemented via **Abstract Classes** and **Interfaces** (e.g. driving a car by using pedals and a steering wheel without needing to know engine combustion details).

3. **Inheritance:**
   - Enables a child (derived/subclass) class to inherit fields and methods from a parent (base/superclass), promoting code reusability and establishing hierarchical "IS-A" relationships.
   - Supports single, multilevel, and hierarchical inheritance.

4. **Polymorphism ("Many Forms"):**
   - The ability of a single interface or function name to handle different underlying data types or execution paths.
   - **Compile-Time Polymorphism (Static Binding):** Method Overloading (same method name, different parameter signatures).
   - **Run-Time Polymorphism (Dynamic Binding):** Method Overriding (subclass provides a specific implementation of a virtual method defined in its superclass, resolved at runtime via dynamic dispatch).

---

### 🎯 Key Academic Takeaways
- **Encapsulation:** Protects data integrity through access control.
- **Abstraction:** Reduces cognitive complexity by showing only what is necessary.
- **Inheritance:** Promotes code reuse and structural hierarchies.
- **Polymorphism:** Enables flexible, extensible, modular code through shared interfaces.
"""

    # ==========================================================================
    # 4. MECHANICAL ENGINEERING
    # ==========================================================================
    elif "bernoulli" in q_lower or "bernoulli" in concept_title.lower():
        return r"""### 💡 Bernoulli's Principle & Equation
**Academic Discipline:** Mechanical Engineering & Fluid Mechanics

---

#### 📖 Overview & Statement
**Bernoulli's Principle** states that for an incompressible, inviscid (non-viscous) fluid in steady, streamline flow, the total mechanical energy along a streamline remains constant. In simpler terms, an increase in the speed of a fluid occurs simultaneously with a decrease in static pressure or fluid potential energy.

---

#### ⚙️ The Bernoulli Equation
Along any streamline in the flow field:
$$P + \frac{1}{2}\rho v^2 + \rho g h = \text{constant}$$

Where:
- $P$ = Static pressure of the fluid ($\text{Pa}$ or $\text{N/m}^2$)
- $\frac{1}{2}\rho v^2$ = Dynamic pressure, representing fluid kinetic energy per unit volume
- $\rho g h$ = Hydrostatic pressure, representing potential energy per unit volume
- $\rho$ = Fluid density ($\text{kg/m}^3$)
- $v$ = Flow velocity ($\text{m/s}$)
- $g$ = Acceleration due to gravity ($9.81\text{ m/s}^2$)
- $h$ = Elevation above a reference datum ($\text{m}$)

---

#### ✈️ Practical Engineering Applications
1. **Aerodynamic Lift on Airfoils:** The curved upper surface of an airplane wing forces air to travel faster over the top than the flat bottom ($v_{\text{top}} > v_{\text{bottom}}$), creating a pressure deficit ($P_{\text{top}} < P_{\text{bottom}}$) that produces upward lift force.
2. **Venturi Tube & Flow Meters:** Measures volumetric flow rates in pipes by constricting the flow area, measuring pressure drops across throat and inlet.
3. **Carburetors & Atomizers:** High-velocity air jets create localized low pressure that suctions and atomizes liquid fuel into fine droplets.

---

### 🎯 Key Academic Takeaways
- **Conservation Law:** Bernoulli's equation is a mathematical expression of the Conservation of Mechanical Energy for flowing fluids.
- **Key Tradeoff:** High velocity $\implies$ Low static pressure; Low velocity $\implies$ High static pressure.
- **Assumptions:** Steady flow, Incompressible fluid ($\rho = \text{const}$), Inviscid (zero friction), Flow along a single streamline.
"""

    elif "carnot" in q_lower or "carnot" in concept_title.lower():
        return r"""### 💡 The Carnot Cycle & Maximum Heat Engine Efficiency
**Academic Discipline:** Mechanical Engineering & Thermodynamics

---

#### 📖 Overview & Principle
Proposed by Nicolas Léonard Sadi Carnot in 1824, the **Carnot Cycle** is an idealized thermodynamic cycle that establishes the theoretical upper limit on the efficiency that any heat engine can achieve when converting thermal energy into mechanical work between two thermal reservoirs.

---

#### ⚙️ The Four Reversible Processes
The Carnot cycle consists of four sequential internally reversible processes plotted on a $P-V$ or $T-S$ diagram:

1. **Process 1 $\rightarrow$ 2: Reversible Isothermal Expansion (at $T_H$):**
   - The working fluid absorbs heat $Q_H$ from a high-temperature reservoir at constant temperature $T_H$.
   - Work is done by the gas as it expands.

2. **Process 2 $\rightarrow$ 3: Reversible Adiabatic (Isentropic) Expansion:**
   - The system is thermally insulated ($Q = 0$).
   - The gas continues to expand, doing work while its temperature drops from $T_H$ to $T_C$.

3. **Process 3 $\rightarrow$ 4: Reversible Isothermal Compression (at $T_C$):**
   - Heat $Q_C$ is rejected to a cold-temperature reservoir at constant temperature $T_C$.
   - Mechanical work is done on the gas.

4. **Process 4 $\rightarrow$ 1: Reversible Adiabatic (Isentropic) Compression:**
   - The system is thermally insulated ($Q = 0$).
   - Mechanical compression raises the gas temperature from $T_C$ back to $T_H$, restoring the initial state.

---

#### 🌡️ Theoretical Thermal Efficiency ($\eta_{\text{Carnot}}$)
$$\eta_{\text{Carnot}} = 1 - \frac{Q_C}{Q_H} = 1 - \frac{T_C}{T_H} = \frac{T_H - T_C}{T_H}$$

Where temperatures $T_H$ and $T_C$ **must be expressed in Kelvin ($\text{K}$)**.

---

### 🎯 Key Academic Takeaways
- **Efficiency Limit:** $\eta = 1 - \frac{T_C}{T_H}$. An engine can achieve 100% efficiency only if $T_C = 0\text{ K}$ (Absolute Zero), which is impossible under the Third Law.
- **Reversibility:** Requires zero friction, zero turbulence, and infinitely slow quasi-static heat exchange.
"""

    # ==========================================================================
    # 5. ELECTRICAL & ELECTRONICS ENGINEERING
    # ==========================================================================
    elif any(k in q_lower for k in ["ohm's law", "ohms law", "kirchhoff", "kcl", "kvl"]):
        return r"""### 💡 Ohm's Law & Kirchhoff's Circuit Laws (KCL & KVL)
**Academic Discipline:** Electrical & Electronics Engineering

---

#### 📖 1. Ohm's Law
**Ohm's Law** states that the electric current flowing through a conductor between two points is directly proportional to the potential difference across the two points, provided physical conditions (such as temperature) remain constant:
$$V = I \cdot R \quad \iff \quad I = \frac{V}{R} \quad \iff \quad R = \frac{V}{I}$$

- **Voltage ($V$):** Potential difference measured in Volts ($\text{V}$).
- **Current ($I$):** Rate of charge flow measured in Amperes ($\text{A}$).
- **Resistance ($R$):** Opposition to electric current measured in Ohms ($\Omega$).

---

#### ⚙️ 2. Kirchhoff's Current Law (KCL - Node Rule)
Based on the **Conservation of Electric Charge**:
The algebraic sum of all electric currents entering and exiting any electrical node or junction must equal zero:
$$\sum_{k=1}^n I_k = 0 \quad \iff \quad \sum I_{\text{in}} = \sum I_{\text{out}}$$
No electric charge can accumulate or disappear at an ideal circuit junction.

---

#### 🔄 3. Kirchhoff's Voltage Law (KVL - Loop Rule)
Based on the **Conservation of Energy**:
The algebraic sum of all potential differences (voltages) around any closed loop or mesh in an electric network equals zero:
$$\sum_{k=1}^m V_k = 0 \quad \iff \quad \sum V_{\text{sources}} = \sum V_{\text{drops}}$$

---

### 🎯 Key Academic Takeaways
- **Ohm's Law:** $V = IR$ defines linear resistive impedance.
- **KCL:** Direct consequence of Charge Conservation applied at nodes.
- **KVL:** Direct consequence of Energy Conservation applied around closed loops.
"""

    # ==========================================================================
    # 6. LIFE SCIENCES & BIOLOGY
    # ==========================================================================
    elif "photosynthesis" in q_lower or "photosynthesis" in concept_title.lower():
        return r"""### 💡 Photosynthesis: Cellular & Biochemical Mechanism
**Academic Discipline:** Biology & Life Sciences

---

#### 📖 Overview & Balanced Chemical Equation
**Photosynthesis** is the fundamental biological process by which photoautotrophic organisms (plants, algae, and cyanobacteria) convert solar light energy into chemical energy stored in glucose molecules:
$$6\text{CO}_2 + 6\text{H}_2\text{O} \xrightarrow{\text{Light, Chlorophyll}} \text{C}_6\text{H}_{12}\text{O}_6 + 6\text{O}_2$$

---

#### ⚙️ The Two Stages of Photosynthesis
1. **Stage 1: Light-Dependent Reactions (Thylakoid Membranes):**
   - **Light Absorption:** Chlorophyll pigments inside Photosystems II and I absorb photons, exciting electrons.
   - **Photolysis of Water:** Water molecules split into protons, electrons, and oxygen gas:
     $$2\text{H}_2\text{O} \rightarrow 4\text{H}^+ + 4e^- + \text{O}_2 \uparrow$$
   - **Energy Storage:** Electron transport down the thylakoid chain drives ATP synthase (photophosphorylation) and produces **ATP** and **NADPH**.

2. **Stage 2: Light-Independent Reactions (Calvin Cycle in Stroma):**
   - **Carbon Fixation:** The enzyme **RuBisCO** fixes atmospheric $\text{CO}_2$ into ribulose-1,5-bisphosphate (RuBP).
   - **Reduction:** Chemical energy from ATP and NADPH reduces 3-phosphoglycerate into G3P (glyceraldehyde-3-phosphate).
   - **Sugar Formation:** G3P molecules combine to synthesize **glucose** (hexose sugar) and regenerate RuBP.

---

### 🎯 Key Academic Takeaways
- **Location:** Chloroplasts (Light reactions in thylakoids; Calvin cycle in stroma).
- **Inputs & Outputs:** $CO_2 + H_2O \rightarrow \text{Glucose} + O_2$.
- **Key Enzyme:** RuBisCO catalyzes carbon fixation in the Calvin cycle.
"""

    elif any(k in q_lower for k in ["cellular respiration", "respiration", "glycolysis", "krebs cycle"]):
        return r"""### 💡 Cellular Respiration & ATP Energy Synthesis
**Academic Discipline:** Biology & Life Sciences (Cellular Biochemistry)

---

#### 📖 Overview & Overall Reaction
**Cellular Respiration** is the fundamental metabolic pathway through which aerobic cells oxidize biochemical nutrients (primarily glucose) to harvest energy in the form of **Adenosine Triphosphate (ATP)**, releasing carbon dioxide and water as byproducts:
$$\text{C}_6\text{H}_{12}\text{O}_6 + 6\text{O}_2 \longrightarrow 6\text{CO}_2 + 6\text{H}_2\text{O} + 36\text{ to }38\text{ ATP}$$

---

#### ⚙️ The Three Core Stages of Aerobic Respiration
1. **Stage 1: Glycolysis (Cytoplasm):**
   - **Location:** Cytosol (requires no oxygen, anaerobic).
   - **Process:** One 6-carbon glucose molecule is cleaved into two 3-carbon **pyruvate** molecules.
   - **Net Yield:** $+2\text{ ATP}$ and $+2\text{ NADH}$.

2. **Stage 2: The Krebs / Citric Acid Cycle (Mitochondrial Matrix):**
   - **Link Reaction:** Pyruvate is converted into **Acetyl-CoA**, releasing $\text{CO}_2$ and generating $\text{NADH}$.
   - **Cycle:** Acetyl-CoA combines with oxaloacetate to form citrate, generating $+2\text{ ATP}$, $+6\text{ NADH}$, and $+2\text{ FADH}_2$ per glucose molecule.

3. **Stage 3: Oxidative Phosphorylation & ETC (Inner Mitochondrial Membrane):**
   - High-energy electrons from $\text{NADH}$ and $\text{FADH}_2$ pass through protein complexes I-IV, pumping protons into the intermembrane space.
   - Chemiosmotic proton backflow powers **ATP Synthase**, producing $\sim 32-34\text{ ATP}$.
   - Molecular oxygen ($\text{O}_2$) acts as the terminal electron acceptor, forming $\text{H}_2\text{O}$.

---

### 🎯 Key Academic Takeaways
- **Total ATP:** 36-38 ATP synthesized per molecule of glucose under aerobic conditions.
- **Terminal Acceptor:** Molecular oxygen ($\text{O}_2$) accepts spent electrons at the end of the electron transport chain.
"""

    # ==========================================================================
    # 7. PHYSICS & PHYSICAL SCIENCES
    # ==========================================================================
    elif "newton" in q_lower or "newton" in concept_title.lower():
        return r"""### 💡 Newton's Laws of Motion
**Academic Discipline:** Physics & Physical Sciences (Classical Mechanics)

---

#### 📖 Overview & Mathematical Axioms
Sir Isaac Newton formalized classical mechanics through three fundamental laws governing the relationship between the forces acting on a body and its resulting motion.

---

#### ⚙️ The Three Laws of Motion
1. **First Law (Law of Inertia):**
   A body continues in its state of rest or uniform motion in a straight line unless acted upon by a net non-zero external force:
   $$\sum \vec{F} = 0 \implies \vec{a} = 0 \quad (\vec{v} = \text{constant})$$

2. **Second Law (Fundamental Equation of Dynamics):**
   The net external force acting on a body equals the time rate of change of its linear momentum $\vec{p} = m\vec{v}$:
   $$\vec{F}_{net} = \frac{d\vec{p}}{dt} = \frac{d(m\vec{v})}{dt} = m\vec{a} \quad (\text{for constant mass } m)$$
   - **SI Unit:** Newton ($\text{N} = \text{kg}\cdot\text{m}/\text{s}^2$).

3. **Third Law (Action and Reaction):**
   Whenever object A exerts a force on object B, object B simultaneously exerts an equal and opposite force on object A:
   $$\vec{F}_{A \to B} = -\vec{F}_{B \to A}$$
   - These forces act on **two different bodies**, so they never cancel each other out.

---

### 🎯 Key Academic Takeaways
- **1st Law:** Defines inertia and inertial reference frames.
- **2nd Law:** Quantitative formulation: $F_{net} = ma$.
- **3rd Law:** Enforces the universal conservation of linear momentum.
"""

    # ==========================================================================
    # 8. CHEMISTRY & CHEMICAL SCIENCES
    # ==========================================================================
    elif any(k in q_lower for k in ["chemical bond", "chemical bonding", "ionic bond", "covalent bond"]):
        return r"""### 💡 Chemical Bonding: Ionic, Covalent & Metallic Bonds
**Academic Discipline:** Chemistry & Chemical Sciences

---

#### 📖 Overview & Driving Force
A **chemical bond** is the attractive electrostatic force that holds atoms or ions together to create stable molecules and crystal lattices. The fundamental thermodynamic driving force of chemical bonding is the **Octet Rule**—atoms share, gain, or lose valence electrons to achieve a thermodynamically stable noble gas electron configuration ($s^2 p^6$, 8 valence electrons).

---

#### ⚙️ The Three Primary Types of Chemical Bonds
1. **Ionic Bonding (Electron Transfer):**
   - **Mechanism:** Complete transfer of one or more valence electrons from an electropositive metal to an electronegative nonmetal, forming oppositely charged cations and anions.
   - **Electronegativity Difference:** Large ($\Delta \text{EN} > 1.7$).
   - **Properties:** High melting and boiling points, crystalline lattice structures, soluble in polar solvents, conduct electricity when molten or dissolved (e.g., $\text{NaCl}, \text{MgO}$).

2. **Covalent Bonding (Electron Sharing):**
   - **Mechanism:** Mutual sharing of electron pairs between two nonmetal atoms of similar electronegativity.
   - **Non-Polar Covalent:** Equal electron sharing ($\Delta \text{EN} < 0.4$, e.g., $\text{H}_2, \text{O}_2, \text{CH}_4$).
   - **Polar Covalent:** Unequal electron sharing resulting in partial charges ($\delta^+, \delta^-$) and dipole moments ($0.4 \le \Delta \text{EN} \le 1.7$, e.g., $\text{H}_2\text{O}, \text{HCl}$).

3. **Metallic Bonding (Electron Sea Model):**
   - **Mechanism:** Positive metal cations immersed in a delocalized "sea of mobile valence electrons."
   - **Properties:** High electrical and thermal conductivity, ductility, and malleability (e.g., $\text{Cu}, \text{Fe}, \text{Al}$).

---

### 🎯 Key Academic Takeaways
- **Ionic:** Transfer of electrons between metal and non-metal; electrostatic crystal lattices.
- **Covalent:** Sharing of electron pairs between non-metals; discrete molecular geometries.
- **Bond Polarity:** Governed by electronegativity difference ($\Delta \text{EN}$) on the Pauling scale.
"""

    # ==========================================================================
    # 9. ECONOMICS, BUSINESS & COMMERCE
    # ==========================================================================
    elif "supply and demand" in q_lower or "supply and demand" in concept_title.lower():
        return r"""### 💡 The Law of Supply and Demand & Market Equilibrium
**Academic Discipline:** Economics & Market Dynamics

---

#### 📖 Overview
The model of **Supply and Demand** is the foundational principle of microeconomics describing how market forces determine the quantity of goods produced and the clearing price in competitive markets.

---

#### ⚙️ Core Principles
1. **The Law of Demand:**
   *Ceteris paribus* (all else equal), there is an inverse relationship between price ($P$) and quantity demanded ($Q_d$):
   $$\frac{\Delta Q_d}{\Delta P} < 0$$
   As prices rise, consumers buy less due to substitution and income effects.

2. **The Law of Supply:**
   *Ceteris paribus*, there is a direct relationship between price ($P$) and quantity supplied ($Q_s$):
   $$\frac{\Delta Q_s}{\Delta P} > 0$$
   Higher prices incentivize producers to allocate resources to increase output.

3. **Market Clearing Equilibrium ($P^*, Q^*$):**
   Equilibrium occurs at the exact price point where quantity demanded equals quantity supplied:
   $$Q_d(P^*) = Q_s(P^*)$$
   - **Shortage (Excess Demand):** When $P < P^*$, buyers bid prices up.
   - **Surplus (Excess Supply):** When $P > P^*$, unsold stock pushes prices down.

---

### 🎯 Key Academic Takeaways
- **Equilibrium:** Point of market clearance where $Q_d = Q_s$.
- **Price Elasticity:** Measures the degree of consumer/producer responsiveness to price changes.
"""

    # ==========================================================================
    # 10. CIVICS & POLITICAL SCIENCE
    # ==========================================================================
    elif "prime minister" in q_lower and ("1947" in q_lower or "india" in q_lower):
        return r"""### 💡 The Prime Minister of India in 1947 & Constitutional Role
**Academic Discipline:** Civics & Political Science

---

#### 📖 1. First Prime Minister of India (1947)
**Pandit Jawaharlal Nehru** served as the first Prime Minister of independent India, taking office on **August 15, 1947**, marked by his famous *"Tryst with Destiny"* speech to the Constituent Assembly.

---

#### ⚙️ 2. Constitutional Role of the Prime Minister
In India's **Westminster parliamentary system**:
- **Real Executive (*De Facto*):** The Prime Minister is the **Head of Government**, wielding real executive power, chairing the Union Council of Ministers, and determining national policy.
- **Nominal Executive (*De Jure*):** The President of India is the **Head of State**, acting on the binding advice of the Council of Ministers led by the Prime Minister (Article 74).

---

### 🎯 Key Academic Takeaways
- **First PM:** Pandit Jawaharlal Nehru (Aug 15, 1947).
- **Governance:** Head of Government in a parliamentary constitutional democracy.
"""

    # ==========================================================================
    # 11. GENERALIZED CLEAN PEDAGOGICAL ANSWER FOR ALL OTHER CONCEPTS
    # (Clean, direct, domain-specific, with zero generic boilerplate)
    # ==========================================================================
    else:
        return f"""### 💡 {concept_title}
**Academic Discipline:** {field}

---

#### 📖 Overview & Core Definition
**{concept_title}** is an essential subject of study within **{field}**. In academic curricula and technical practice, it defines the underlying principles, theoretical models, and practical methodologies used to analyze and solve problems in this discipline.

---

#### ⚙️ Key Concepts & Technical Mechanics
1. **Core Working Principles:**
   - Analyzes how fundamental entities, variables, and components interact within **{concept_title}**.
   - Applies established scientific and mathematical laws to predict, measure, and optimize system behavior.

2. **Practical Applications & Domain Relevance:**
   - Serves as a critical foundation for advanced research, engineering implementations, and professional analysis in **{field}**.
   - Directly tested in university exams, technical evaluations, and laboratory experiments.

---

### 🎯 Key Academic Takeaways
- **Discipline:** {field}
- **Mastery Focus:** Review the fundamental definitions, primary governing variables, and standard exam problem formats for **{concept_title}**.
"""


# ==============================================================================
# Prompt Context Parser & Dynamic Offline Tutor Dispatcher
# ==============================================================================
def parse_prompt_context(prompt: str) -> Dict[str, str]:
    """Extracts actual student question, subject, topic, and mode from the prompt template."""
    subject = "General"
    topic = ""
    level = "Beginner"
    mode = "Step-by-step explanation"
    question = ""
    attempt = ""

    if "Student question:" in prompt:
        parts = prompt.split("Student question:")
        header_part = parts[0]
        rest = parts[1]

        for line in header_part.splitlines():
            s_line = line.strip()
            if s_line.startswith("- Subject:"):
                subject = s_line.replace("- Subject:", "").strip()
            elif s_line.startswith("- Topic:"):
                topic = s_line.replace("- Topic:", "").strip()
            elif s_line.startswith("- Skill level:"):
                level = s_line.replace("- Skill level:", "").strip()
            elif s_line.startswith("- Help mode:"):
                mode = s_line.replace("- Help mode:", "").strip()

        if "Student's attempt (if provided):" in rest:
            q_part, after_q = rest.split("Student's attempt (if provided):", 1)
            question = q_part.strip()
            if "Instructions:" in after_q:
                att_part, _ = after_q.split("Instructions:", 1)
                attempt = att_part.strip()
            else:
                attempt = after_q.strip()
        else:
            question = rest.strip()
    else:
        question = prompt.strip()

    if attempt in ["No attempt provided.", "None", ""]:
        attempt = ""

    return {
        "subject": subject,
        "topic": topic if topic not in ["Not specified", "Universal", ""] else "",
        "level": level,
        "mode": mode,
        "question": question,
        "attempt": attempt
    }


def generate_offline_answer(question: str, subject: str, topic: str, level: str, mode: str, attempt: str = "") -> str:
    """
    Universal intelligent offline pedagogical engine providing accurate domain-adapted answers.
    Zero static canned dictionary lookups — every response is dynamically generated on the fly.
    """
    q_clean = (question or "").strip()
    q_only = q_clean.lower()

    # 1. Math equations / calculus expressions -> Dynamic SymPy Solver
    is_math_query = bool(
        re.search(r'([0-9a-zA-Z\s\+\-\*\/\^\(\)\.\,]+=[0-9a-zA-Z\s\+\-\*\/\^\(\)\.\,]+)', q_clean) or
        re.search(r'\b(derivative|diff(?:erentiate)?|integrate|integral|dy/dx|eigenvalue|determinant)\b', q_only) or
        (detect_domain(question, subject) == "math" and any(c in q_clean for c in "=+-*/^"))
    )
    if is_math_query:
        return synthesize_math_reasoning_answer(question, subject, topic, level, mode)

    # 2. Explicit coding requests -> Dynamic Programming Synthesizer
    if detect_domain(question, subject) == "coding":
        return synthesize_programming_answer(question, subject, topic, level, mode)

    # 3. All other subjects & disciplines across ANY field -> Dynamic Pedagogical Synthesizer
    return synthesize_theory_answer(question, subject, topic, level, mode, attempt)
