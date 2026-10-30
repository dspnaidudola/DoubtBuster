import streamlit as st
import json
from datetime import datetime
from backend.config import get_setting
from backend.core.pipeline import (
    answer_doubt, answer_followup, generate_lesson_summary, get_adaptive_difficulty
)
from backend.utils.validators import validate_question
from backend.services.doc_service import extract_text_from_file
from backend.services.rag_service import (
    parse_course_document, chunk_sections, retrieve_grounded_chunks, answer_with_rag
)
from backend.services.math_code_service import solve_math_expression, analyze_matrix, diagnose_python_code
from backend.services.code_exec_service import execute_python_code
from backend.services.llm_service import test_api_connection
from backend.services.db_service import (
    init_db, get_student_stats, toggle_bookmark, toggle_difficult, rate_doubt, get_history, get_difficult_topics
)
from backend.services.offline_tutor import detect_domain, detect_academic_field

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="DoubtBuster | Gemini-Style AI Academic Companion",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern Gemini-like UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Gemini Hero Header */
.gemini-header-card {
    background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 18px;
    padding: 1.5rem 2rem;
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.3);
}

.gemini-gradient-title {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.gemini-subtitle {
    color: #94a3b8;
    font-size: 0.98rem;
    margin-top: 0.3rem;
}

.gemini-badge-container {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.8rem;
    flex-wrap: wrap;
}

.gemini-badge {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 0.25rem 0.7rem;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #e2e8f0;
}

/* Welcome Card for Empty State */
.welcome-container {
    text-align: center;
    padding: 3rem 1.5rem 2rem 1.5rem;
    max-width: 820px;
    margin: 0 auto;
}

.welcome-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.welcome-desc {
    color: #64748b;
    font-size: 1.05rem;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* Suggestion Chips */
.chip-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.8rem;
    margin-top: 1rem;
    text-align: left;
}

.domain-pill {
    background: rgba(59, 130, 246, 0.12);
    border: 1px solid rgba(59, 130, 246, 0.28);
    color: #38bdf8;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []
if "session_topics" not in st.session_state:
    st.session_state["session_topics"] = []
if "pending_prompt" not in st.session_state:
    st.session_state["pending_prompt"] = ""
if "active_api_key" not in st.session_state:
    st.session_state["active_api_key"] = ""

# Fetch stats for student
stats = get_student_stats()
adaptive_suggestion = get_adaptive_difficulty(stats)

# ==============================================================================
# Header
# ==============================================================================
st.markdown(f"""
<div class="gemini-header-card">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
        <div>
            <h1 class="gemini-gradient-title">✨ DoubtBuster</h1>
            <p class="gemini-subtitle">Gemini-Style Universal AI Academic Tutor — On-the-fly multi-domain reasoning & mathematical verification</p>
            <div class="gemini-badge-container">
                <span class="gemini-badge">⚡ Dynamic Synthesis (Zero Static Answers)</span>
                <span class="gemini-badge">🌐 All Academic Domains</span>
                <span class="gemini-badge">🧮 SymPy Engine</span>
                <span class="gemini-badge">🧪 Isolated Sandbox</span>
            </div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 0.6rem 1rem; text-align: center; min-width: 130px; margin-top: 0.4rem;">
            <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Study Streak</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #38bdf8;">🔥 {stats.get('study_streak', 0)} <span style="font-size: 0.85rem; font-weight: 600; color: #cbd5e1;">days</span></div>
            <div style="font-size: 0.72rem; color: #64748b;">{stats.get('total_doubts', 0)} doubts resolved</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# Sidebar Configuration
# ==============================================================================
with st.sidebar:
    st.title("✨ Tutor Controls")

    # New Chat action
    if st.button("✨ New Chat / Reset", use_container_width=True, type="primary"):
        st.session_state["chat_messages"] = []
        st.session_state["pending_prompt"] = ""
        st.rerun()

    st.info("🌐 **Universal AI Assistant:** Doubts across all fields (AI/ML, CS, Microprocessors, Engineering, Sciences, Math, Humanities) are answered with zero configuration.")
    subject = "Universal"
    topic = ""

    st.caption(f"🎯 **Adaptive Level:** Recommended **{adaptive_suggestion}**.")
    level = st.select_slider("Skill Level", options=["Beginner", "Intermediate", "Advanced"], value=adaptive_suggestion)

    mode = st.radio(
        "Pedagogical Mode",
        ["Step-by-step explanation", "Hint first", "Verify my answer", "Practice question with answer key"],
        help="Hint first guides you with questions; Verify my answer evaluates your attempt."
    )

    user_attempt = ""
    if mode == "Verify my answer":
        user_attempt = st.text_area(
            "Your attempt / reasoning to verify:",
            height=85,
            placeholder="Type your preliminary answer or reasoning here..."
        )

    language = st.selectbox("Language", ["English", "Simple English", "Telugu (Technical mix)", "Hindi (Technical mix)"])

    st.divider()

    # RAG File Upload
    st.subheader("📎 Course Material & Grounding")
    uploaded = st.file_uploader(
        "Attach Document (PDF, PPTX, TXT, PY, CSV)",
        type=["pdf", "pptx", "txt", "py", "md", "csv"],
        help="Upload lecture notes, textbooks, or assignments."
    )
    rag_toggle = False
    if uploaded:
        st.success(f"📎 Attached: **{uploaded.name}**")
        rag_toggle = st.checkbox("Ground response strictly in document (RAG Citations)", value=True)

    st.divider()

    # AI Engine & Key
    st.subheader("🔑 AI Provider & Engine")
    saved_openai_key = get_setting("OPENAI_API_KEY", "")
    saved_gemini_key = get_setting("GEMINI_API_KEY", "") or get_setting("GOOGLE_API_KEY", "")

    provider_choice = st.selectbox(
        "AI Engine",
        ["Auto-detect / Built-in Pedagogical Mode", "Google Gemini (2.5 Flash)", "OpenAI (GPT-4o)"],
        index=0
    )

    api_key_input = st.text_input(
        "API Key (Optional)",
        value=saved_gemini_key if "Gemini" in provider_choice else (saved_openai_key if "OpenAI" in provider_choice else ""),
        type="password",
        placeholder="AIza... or sk-...",
        help="Leave blank to use the Built-in Pedagogical Tutor with SymPy math engine."
    )
    st.session_state["active_api_key"] = api_key_input.strip()

    if st.button("🔌 Test Provider Connection", use_container_width=True):
        if not api_key_input.strip():
            st.info("No key provided. Built-in Offline Mode is 100% active with zero rate limits!")
        else:
            with st.spinner("Testing API key..."):
                model_to_test = "gemini-2.5-flash" if "Gemini" in provider_choice else "gpt-4o-mini"
                res = test_api_connection(api_key_input.strip(), model=model_to_test)
                if res.get("success"):
                    st.success(res.get("message"))
                else:
                    st.error(f"Error: {res.get('message')}")

    if api_key_input.strip():
        st.caption("🟢 Connected to custom AI provider.")
    else:
        st.caption("💡 **Active:** Built-in Universal Pedagogical Engine (0 cost, SymPy math solver, dynamic code execution).")

    st.divider()
    st.caption("DoubtBuster • Gemini-Style Multi-Domain AI Companion")

# ==============================================================================
# Workspace Tabs
# ==============================================================================
tab_chat, tab_math, tab_code, tab_history = st.tabs([
    "💬 Gemini AI Chatbot",
    "🧮 Instant Math & Equation Verifier",
    "🧪 Python Code Diagnoser & Sandbox",
    "📊 Learning History & Bookmarks"
])

# Quick suggestion prompts for the Gemini Empty State
GEMINI_SUGGESTIONS = [
    {
        "title": "🔬 Physics & Mechanics",
        "prompt": "Explain Newton's second law of motion with formula and how force relates to acceleration."
    },
    {
        "title": "📐 Mathematics & Equations",
        "prompt": "Solve the linear equation 3x + 12 = 33 step-by-step."
    },
    {
        "title": "🐍 Computer Science & Coding",
        "prompt": "Write a python function to check if two strings are anagrams with test cases."
    },
    {
        "title": "🌿 Biology & Life Sciences",
        "prompt": "What is photosynthesis and how does it produce glucose?"
    },
    {
        "title": "📊 Economics & Market Forces",
        "prompt": "Explain the law of supply and demand and market clearing equilibrium price."
    },
    {
        "title": "⚡ Electrical & Microcontrollers",
        "prompt": "Explain the 8051 microcontroller architecture and memory organization."
    },
    {
        "title": "🏛️ Civics & History",
        "prompt": "Who was the prime minister of India in 1947 and what was their constitutional role?"
    },
    {
        "title": "🧪 Chemistry & Reaction Bonds",
        "prompt": "Explain chemical bonding and the difference between ionic and covalent bonds."
    }
]

# ==============================================================================
# TAB 1: GEMINI AI CHATBOT
# ==============================================================================
with tab_chat:
    # 1. Render Welcome Screen if conversation is empty
    if len(st.session_state["chat_messages"]) == 0:
        st.markdown("""
        <div class="welcome-container">
            <h1 class="welcome-title">Hello, Scholar 👋</h1>
            <p class="welcome-desc">What would you like to master or solve today? Ask questions across any field — equations, algorithms, sciences, economics, or humanities. Every response is dynamically synthesized strictly for your specific domain.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**💡 Try these prompt starters (click to ask):**")
        cols = st.columns(4)
        for i, sug in enumerate(GEMINI_SUGGESTIONS):
            col = cols[i % 4]
            with col:
                if st.button(f"**{sug['title']}**\n\n_{sug['prompt'][:50]}..._", key=f"sug_btn_{i}", use_container_width=True):
                    st.session_state["pending_prompt"] = sug["prompt"]
                    st.rerun()

    # 2. Render Existing Chat Messages in Gemini Style
    for idx, msg in enumerate(st.session_state["chat_messages"]):
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑‍🎓"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="✨"):
                field_label = msg.get("field", "Universal Science")
                st.markdown(f'<span class="domain-pill">🏷️ {field_label}</span>', unsafe_allow_html=True)
                st.markdown(msg["content"])

                # Action row for bookmarking, rating, practice
                col_a1, col_a2, col_a3, col_a4 = st.columns([1, 1, 1, 2])
                doubt_id = msg.get("doubt_id")
                with col_a1:
                    if st.button("⭐ Bookmark", key=f"bm_{idx}"):
                        if doubt_id:
                            is_bm = toggle_bookmark(doubt_id)
                            st.toast("Bookmarked in Learning History!" if is_bm else "Bookmark removed!")
                        else:
                            st.toast("Response noted!")
                with col_a2:
                    if st.button("👍 Helpful", key=f"up_{idx}"):
                        if doubt_id:
                            rate_doubt(doubt_id, 1)
                        st.toast("Thank you for your feedback!")
                with col_a3:
                    if st.button("📌 Flag Topic", key=f"diff_{idx}"):
                        if doubt_id:
                            toggle_difficult(doubt_id)
                            st.toast("Added to revision list!")
                with col_a4:
                    if st.button("🧠 Practice Challenge", key=f"prac_{idx}"):
                        st.session_state["pending_prompt"] = f"Generate a similar practice problem with worked answer key based on this question: {msg.get('question_ref', '')}"
                        st.rerun()

    # 3. Floating Bottom Chat Input
    chat_prompt = st.chat_input("Ask DoubtBuster anything across any domain (e.g. solve equation, write code, explain concept)...")

    # Determine prompt to process (either from input box or from clicked chip)
    prompt_to_process = None
    if chat_prompt:
        prompt_to_process = chat_prompt.strip()
    elif st.session_state.get("pending_prompt"):
        prompt_to_process = st.session_state["pending_prompt"].strip()
        st.session_state["pending_prompt"] = ""

    if prompt_to_process:
        try:
            validate_question(prompt_to_process)

            # Display user message immediately
            with st.chat_message("user", avatar="🧑‍🎓"):
                st.markdown(prompt_to_process)

            # Generate response
            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Analyzing question & dynamically synthesizing domain explanation..."):
                    active_key = st.session_state.get("active_api_key", "")
                    chosen_model = "gemini-2.5-flash" if "Gemini" in provider_choice else "gpt-4o-mini"

                    # Identify true domain directly from student's prompt
                    effective_field = detect_academic_field(prompt_to_process)

                    # Check RAG mode
                    if uploaded and rag_toggle:
                        sections = parse_course_document(uploaded, uploaded.name)
                        chunks = chunk_sections(sections)
                        retrieved = retrieve_grounded_chunks(prompt_to_process, chunks, top_k=3)
                        answer = answer_with_rag(prompt_to_process, retrieved, api_key=active_key, model=chosen_model)
                    else:
                        extracted_text = extract_text_from_file(uploaded) if uploaded else ""
                        query_with_doc = prompt_to_process
                        if extracted_text:
                            query_with_doc = (prompt_to_process + "\n\n[Attached File Content]:\n" + extracted_text[:10000]).strip()

                        answer = answer_doubt(
                            question=query_with_doc,
                            subject=effective_field,
                            topic=topic.strip(),
                            level=level,
                            mode=mode,
                            language=language,
                            attempt=user_attempt.strip(),
                            api_key=active_key,
                            model=chosen_model,
                            persist=True
                        )

                    # Get recent doubt ID for bookmarking
                    recent_hist = get_history(limit=1)
                    doubt_id = recent_hist[0]["id"] if recent_hist else None

                    # Render generated answer
                    st.markdown(f'<span class="domain-pill">🏷️ {effective_field}</span>', unsafe_allow_html=True)
                    st.markdown(answer)

                    # Append to session state chat thread
                    st.session_state["chat_messages"].append({
                        "role": "user",
                        "content": prompt_to_process,
                        "timestamp": datetime.now().strftime("%I:%M %p")
                    })
                    st.session_state["chat_messages"].append({
                        "role": "assistant",
                        "content": answer,
                        "field": effective_field,
                        "question_ref": prompt_to_process,
                        "doubt_id": doubt_id,
                        "timestamp": datetime.now().strftime("%I:%M %p")
                    })

                    # Track session topic
                    if topic.strip() and topic.strip() not in st.session_state["session_topics"]:
                        st.session_state["session_topics"].append(topic.strip())

                    st.rerun()

        except ValueError as exc:
            st.warning(f"⚠️ {exc}")
        except Exception as exc:
            st.error(f"❌ Could not complete request: {exc}")

# ==============================================================================
# TAB 2: INSTANT MATH & EQUATION VERIFIER
# ==============================================================================
with tab_math:
    st.markdown("#### 🧮 Deterministic SymPy Mathematical Engine")
    st.caption("Verify calculus, algebraic equations, limits, and matrices with zero AI hallucinations.")

    math_col1, math_col2 = st.columns([1.2, 1])

    with math_col1:
        math_mode = st.selectbox(
            "Select Mathematical Operation",
            ["Solve Equation (f(x) = 0)", "Symbolic Derivative", "Indefinite Integral", "Simplify Expression", "Limit (x -> 0)", "Matrix Analysis"]
        )

        if math_mode == "Matrix Analysis":
            matrix_input = st.text_area(
                "Matrix format (e.g. '1, 2; 3, 4' or '[[1, 2], [3, 4]]')",
                value="1, 2; 3, 4",
                height=100
            )
            calc_matrix = st.button("Compute Matrix Properties", type="primary")
            if calc_matrix:
                res = analyze_matrix(matrix_input)
                if res["success"]:
                    st.success("Matrix Computed Successfully!")
                    st.markdown(f"**Matrix $M$:** $${res['latex_matrix']}$$")
                    st.markdown(f"- **Dimensions:** {res['rows']} $\\times$ {res['cols']}")
                    st.markdown(f"- **Determinant $\\det(M)$:** $${res['determinant']}$$")
                    st.markdown(f"- **Invertible?** {'✅ Yes' if res['is_invertible'] else '❌ No'}")
                    if res["is_invertible"]:
                        st.markdown(f"- **Inverse $M^{{-1}}$:** $${res['latex_inverse']}$$")
                    st.markdown(f"- **Eigenvalues:** `{res['eigenvalues']}`")
                else:
                    st.error(f"Error computing matrix: {res['error']}")
        else:
            expr_val = st.text_input("Expression", value="3*x + 12 = 33", placeholder="e.g. x**2 - 5*x + 6, sin(x), 3*x + 12 = 33")
            var_sym = st.text_input("Variable", value="x", max_chars=2)
            op_map = {
                "Solve Equation (f(x) = 0)": "solve",
                "Symbolic Derivative": "derivative",
                "Indefinite Integral": "integrate",
                "Simplify Expression": "simplify",
                "Limit (x -> 0)": "limit"
            }
            calc_math = st.button("Calculate Step", type="primary")

            if calc_math:
                res = solve_math_expression(expr_val, operation=op_map[math_mode], variable=var_sym)
                if res["success"]:
                    st.markdown(f"#### {res['explanation']}")
                    st.latex(res["latex_result"])
                    if res.get("steps"):
                        with st.expander("🔍 Step-by-Step Mathematical Derivation", expanded=True):
                            for step in res["steps"]:
                                st.markdown(step)
                    st.info(f"Raw Result: `{res['result_str']}`")
                else:
                    st.error(f"Computation Error: {res['error']}")

    with math_col2:
        st.markdown("""
        <div style="background: #f1f5f9; border-radius: 12px; padding: 1.2rem; border: 1px solid #cbd5e1;">
            <h4 style="margin-top:0;">📝 Syntax Guide for Math & Equations</h4>
            <p style="font-size:0.85rem; color:#475569;">Write math expressions in natural or Python syntax:</p>
            <ul style="font-size:0.85rem; color:#475569; padding-left:1.2rem;">
                <li><strong>Equations:</strong> <code>3x + 12 = 33</code> or <code>x**2 - 5*x + 6 = 0</code></li>
                <li><strong>Powers:</strong> <code>x^2</code> or <code>x**2</code></li>
                <li><strong>Multiplication:</strong> <code>2x</code> or <code>2*x</code>, <code>3(x+1)</code></li>
                <li><strong>Trig Functions:</strong> <code>sin(x), cos(x), tan(x)</code></li>
                <li><strong>Exponential:</strong> <code>exp(x)</code></li>
                <li><strong>Natural Log:</strong> <code>log(x)</code></li>
                <li><strong>Square Root:</strong> <code>sqrt(x)</code></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: PYTHON CODE DIAGNOSER & SANDBOX
# ==============================================================================
with tab_code:
    st.markdown("#### 🧪 Safe Python AST Code Diagnoser & Secure Sandbox Execution")
    st.caption("Inspect syntax and logic statically, then run your code safely in an isolated sandbox with a 3-second timeout.")

    code_to_check = st.text_area(
        "Paste or write Python code here:",
        height=200,
        value="""def calculate_sum(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

print("Sum 1..10 is:", calculate_sum(10))
"""
    )

    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        if st.button("🔍 Diagnose Code Statically", type="primary"):
            diag = diagnose_python_code(code_to_check)
            if not diag["success"]:
                st.warning(diag["error"])
            else:
                if diag["is_clean"]:
                    st.success("✅ **Code passed static syntax and safety checks!**")
                else:
                    if not diag["syntax_ok"]:
                        st.error("❌ **Syntax Error Found!**")
                    else:
                        st.warning("⚠️ **Potential Issues Detected:**")

                    for issue in diag["issues"]:
                        st.markdown(f"- {issue}")

    with col_c2:
        if st.button("▶️ Execute in Secure Sandbox", type="secondary"):
            with st.spinner("Running in isolated environment..."):
                run_res = execute_python_code(code_to_check, timeout_sec=3.0)
                if run_res["success"]:
                    st.success(f"Execution Succeeded ({run_res['execution_time_ms']} ms)")
                    st.code(run_res["stdout"] if run_res["stdout"] else "[No stdout output]")
                else:
                    st.error(f"Execution Failed ({run_res['execution_time_ms']} ms)")
                    st.code(run_res["stderr"])

# ==============================================================================
# TAB 4: LEARNING HISTORY & BOOKMARKS
# ==============================================================================
with tab_history:
    st.markdown("#### 📊 Student Learning History & Concept Bookmarks")
    st.caption("Review your past doubts, bookmarked questions, and revision areas.")

    history_items = get_history(limit=20)
    if history_items:
        for h in history_items:
            with st.expander(f"📌 {h.get('subject', 'General')} — {h.get('question', '')[:60]}... ({h.get('created_at', '')[:10]})"):
                st.markdown(f"**Question:** {h.get('question')}")
                st.markdown(f"**Discipline:** `{h.get('subject')}` | **Topic:** `{h.get('topic') or 'N/A'}`")
                st.markdown(f"**Rating:** {h.get('rating', 0)} | **Bookmarked:** {'⭐ Yes' if h.get('bookmarked') else 'No'} | **Flagged Difficult:** {'📌 Yes' if h.get('flagged_difficult') else 'No'}")
                st.divider()
                st.markdown(h.get("answer", ""))
    else:
        st.info("No learning history recorded yet. Start chatting in the **💬 Gemini AI Chatbot** tab!")

st.markdown("---")
st.markdown('<p style="text-align: center; color: #64748b; font-size: 0.85rem;">DoubtBuster • Gemini-Style AI Academic Companion • Streamlit Native</p>', unsafe_allow_html=True)
