import io
from typing import Optional, Dict, Any, List
import pypdf

CURATED_STUDY_MATERIALS: Dict[str, Dict[str, Any]] = {
    "Programming": {
        "title": "Python Programming & Data Structures Core Guide",
        "description": "Essential syntax, time complexities, OOP principles, and common pitfalls.",
        "content": r"""# 🐍 Python Programming & Core Concepts Cheat Sheet

### 1. Time & Space Complexity (Big-O)
| Data Structure | Access | Search | Insertion | Deletion |
|---|---|---|---|---|
| **Python List** | $O(1)$ | $O(n)$ | $O(n)$ ($O(1)$ amortized append) | $O(n)$ |
| **Dict (Hash Table)** | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |
| **Set** | N/A | $O(1)$ | $O(1)$ | $O(1)$ |
| **Binary Search Tree** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |

### 2. Common Recursion Rules
- **Base Case**: The condition where recursion stops. Without it, you get a `RecursionError: maximum recursion depth exceeded`.
- **Recursive Step**: Moving toward the base case with a smaller subproblem.

```python
def factorial(n: int) -> int:
    # Base Case
    if n <= 1:
        return 1
    # Recursive Step
    return n * factorial(n - 1)
```

### 3. Object-Oriented Programming (OOP) Pillars
1. **Encapsulation**: Bundling data & methods; private attributes with `_` or `__`.
2. **Inheritance**: Subclasses inherit attributes from parent class (`super().__init__()`).
3. **Polymorphism**: Same method name behaves differently across classes.
4. **Abstraction**: Hiding internal implementation details using `abc.ABC`.

### 4. Common Python Pitfalls
- **Mutable default arguments**: Never use `def fn(item, my_list=[]):`. Use `my_list=None` instead.
- **Copying lists**: `b = a` creates a reference, not a copy! Use `b = a.copy()` or `copy.deepcopy()`.
- **Modifying during iteration**: Avoid `for x in my_list: my_list.remove(x)`. Use list comprehensions.
"""
    },
    "Mathematics": {
        "title": "Engineering Mathematics & Linear Algebra Guide",
        "description": "Formulas for Calculus, Matrix Decomposition, Eigenvalues, and Probability.",
        "content": r"""# 📐 Engineering Mathematics & Linear Algebra

### 1. Essential Calculus Derivatives & Integrals
- $\\frac{d}{dx}[x^n] = n x^{n-1}$
- $\\frac{d}{dx}[e^x] = e^x$, $\\frac{d}{dx}[\\ln(x)] = \\frac{1}{x}$
- $\\frac{d}{dx}[\\sin(x)] = \\cos(x)$, $\\frac{d}{dx}[\\cos(x)] = -\\sin(x)$
- **Product Rule**: $\\frac{d}{dx}[u \\cdot v] = u'v + uv'$
- **Chain Rule**: $\\frac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)$

### 2. Linear Algebra & Matrices
- **Determinant of $2\\times 2$ Matrix**:
  $$\\det \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} = ad - bc$$
- **Eigenvalues and Eigenvectors**:
  Satisfy $A v = \\lambda v$, found by solving the characteristic equation:
  $$\\det(A - \\lambda I) = 0$$

### 3. Probability & Bayes Theorem
- **Conditional Probability**:
  $$P(A|B) = \\frac{P(A \\cap B)}{P(B)}$$
- **Bayes Theorem**:
  $$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)}$$
- **Expectation & Variance**:
  $$E[X] = \\sum x_i P(x_i), \\quad \\text{Var}(X) = E[X^2] - (E[X])^2$$
"""
    },
    "Machine Learning": {
        "title": "Machine Learning Foundations & Algorithms",
        "description": "Supervised, unsupervised, loss functions, optimization, and regularization.",
        "content": r"""# 🤖 Machine Learning Fundamentals

### 1. Loss Functions
- **Mean Squared Error (Regression)**:
  $$MSE = \\frac{1}{n} \\sum_{i=1}^n (y_i - \\hat{y}_i)^2$$
- **Binary Cross-Entropy (Log Loss)**:
  $$\\mathcal{L} = -\\frac{1}{n} \\sum_{i=1}^n [y_i \\ln(\\hat{y}_i) + (1 - y_i) \\ln(1 - \\hat{y}_i)]$$

### 2. Gradient Descent Update Rule
$$W := W - \\alpha \\nabla_W \\mathcal{L}$$
- $\\alpha$: Learning rate (too high $\\to$ divergence, too low $\\to$ very slow convergence).

### 3. Bias-Variance Tradeoff
- **High Bias (Underfitting)**: Model is too simple; performs poorly on both train and test data.
  *Fix*: Add features, use a more complex model, reduce regularization.
- **High Variance (Overfitting)**: Model memorizes training noise; high train accuracy, low test accuracy.
  *Fix*: Regularization ($L_1$ Lasso, $L_2$ Ridge), collect more data, dropout, early stopping.

### 4. Classification Metrics
- **Accuracy**: $\\frac{TP + TN}{TP + TN + FP + FN}$
- **Precision**: $\\frac{TP}{TP + FP}$ (Quality of positive predictions)
- **Recall (Sensitivity)**: $\\frac{TP}{TP + FN}$ (Fraction of actual positives found)
- **F1 Score**: $2 \\times \\frac{\\text{Precision} \\times \\text{Recall}}{\\text{Precision} + \\text{Recall}}$
"""
    },
    "Deep Learning": {
        "title": "Deep Learning & Neural Network Architectures",
        "description": "Activation functions, Backpropagation, CNNs, RNNs, and Transformers.",
        "content": r"""# 🧠 Deep Learning & Neural Networks

### 1. Common Activation Functions
- **ReLU**: $f(x) = \\max(0, x)$ — prevents vanishing gradient for positive values; zero derivative for $x < 0$ (dying ReLU).
- **Sigmoid**: $\\sigma(x) = \\frac{1}{1 + e^{-x}}$ — maps inputs to $(0, 1)$, prone to vanishing gradients.
- **Softmax**: $\\sigma(z)_i = \\frac{e^{z_i}}{\\sum_{j} e^{z_j}}$ — output probabilities for multi-class classification.

### 2. Backpropagation Intuition
Applies the chain rule recursively from the output layer backwards to compute the gradient of loss with respect to every weight $\\frac{\\partial \\mathcal{L}}{\\partial W_{ij}}$.

### 3. Convolutional Neural Networks (CNNs)
- **Convolution**: Feature extraction using learnable kernels/filters.
- **Pooling (Max/Average)**: Spatial dimension reduction, translational invariance.
- **Flatten & Dense**: Final classification decision.

### 4. Transformers & Self-Attention
- **Scaled Dot-Product Attention**:
  $$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q K^T}{\\sqrt{d_k}}\\right) V$$
"""
    },
    "NLP": {
        "title": "Natural Language Processing & LLMs Guide",
        "description": "Text preprocessing, embeddings, tokenization, seq2seq, and prompt engineering.",
        "content": r"""# 💬 Natural Language Processing (NLP)

### 1. Text Preprocessing Pipeline
1. **Tokenization**: Splitting text into words, subwords (BPE, WordPiece), or characters.
2. **Stopword Removal**: Removing non-informative words like 'is', 'the', 'at'.
3. **Stemming / Lemmatization**: Reducing words to base root (e.g. 'running' $\\to$ 'run').

### 2. Text Representation
- **Bag of Words (BoW)**: Word occurrence frequency vector (ignores word order).
- **TF-IDF**:
  $$\\text{TF-IDF} = \\text{TF}(t, d) \\times \\log\\left(\\frac{N}{DF(t)}\\right)$$
- **Word Embeddings (Word2Vec / GloVe)**: Dense vector representations where semantic similarity corresponds to cosine proximity.

### 3. Modern Large Language Models (LLMs)
- Built on Transformer decoder or encoder-decoder architectures.
- **Pre-training**: Next-token prediction on massive corpora.
- **Fine-tuning & RLHF**: Alignment with human instructions and helpfulness.
"""
    },
    "Data Science": {
        "title": "Data Science & Exploratory Data Analysis (EDA)",
        "description": "Pandas workflows, data cleaning, outlier detection, and statistical testing.",
        "content": r"""# 📊 Data Science & Data Analysis Guide

### 1. Essential Pandas Workflow
```python
import pandas as pd

# Load & Inspect
df = pd.read_csv("data.csv")
print(df.info())
print(df.describe())

# Handling Missing Values
df['column'].fillna(df['column'].median(), inplace=True)
df.dropna(subset=['critical_column'], inplace=True)

# Grouping & Aggregating
grouped = df.groupby('category')['sales'].agg(['mean', 'sum', 'count'])
```

### 2. Feature Scaling
- **Min-Max Normalization**: Maps values to $[0, 1]$:
  $$X_{\\text{norm}} = \\frac{X - X_{\\min}}{X_{\\max} - X_{\\min}}$$
- **Standardization (Z-Score)**: Mean $= 0$, Std $= 1$:
  $$Z = \\frac{X - \\mu}{\\sigma}$$
"""
    }
}

def extract_text_from_file(uploaded_file) -> str:
    """
    Extracts plain text from various file formats: txt, py, csv, md, and pdf.
    """
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()
    
    # Handle PDF
    if filename.endswith(".pdf"):
        try:
            pdf_bytes = uploaded_file.getvalue()
            pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            text_pages = []
            for page_idx, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(f"--- Page {page_idx + 1} ---\n" + page_text)
            return "\n\n".join(text_pages)
        except Exception as e:
            return f"Error reading PDF: {e}"

    # Handle text files (txt, py, csv, md, json)
    try:
        content = uploaded_file.getvalue().decode("utf-8", errors="replace")
        return content
    except Exception as e:
        return f"Error decoding file: {e}"

def get_study_material(subject: str) -> Optional[Dict[str, Any]]:
    return CURATED_STUDY_MATERIALS.get(subject)
