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
from components.theme import inject_theme, render_header, render_quick_nav

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="DoubtBuster | Universal AI Academic Companion",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global cutting-edge design system
inject_theme()

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
# Signature Hero Header & Quick Switcher
# ==============================================================================
render_header(
    title="✨ DoubtBuster",
    subtitle="Universal AI Academic Tutor — On-the-fly multi-domain reasoning, SymPy math verification & isolated sandbox",
    badges=[
        "⚡ Dynamic Synthesis",
        "🌐 All Disciplines",
        "🧮 SymPy Engine",
        "🧪 Secure Sandbox",
        f"🎯 Level: {adaptive_suggestion}"
    ],
    streak=stats.get("study_streak", 0),
    doubts_count=stats.get("total_doubts", 0),
    show_stats=True
)

# Navigation Bar
render_quick_nav(active="Home")

# ==============================================================================
# Sidebar Configuration
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Tutor Controls")

    # New Chat action
    if st.button("✨ New Chat / Reset", use_container_width=True, type="primary"):
        st.session_state["chat_messages"] = []
        st.session_state["pending_prompt"] = ""
        st.rerun()

    st.markdown("---")

    # 1. Pedagogical Mode & Level
    st.markdown("#### 🎓 Pedagogical Settings")
    st.caption(f"🎯 **Adaptive System Suggestion:** `{adaptive_suggestion}`")
    level = st.select_slider(
        "Skill Level",
        options=["Beginner", "Intermediate", "Advanced"],
        value=adaptive_suggestion,
        key="global_skill_level"
    )

    mode = st.radio(
        "Pedagogical Mode",
        [
            "Step-by-step explanation",
            "Hint first",
            "Verify my answer",
            "Practice question with answer key"
        ],
        help="Step-by-step: full conceptual guide; Hint first: guided Socratic hints; Verify: evaluates your attempt."
    )

    user_attempt = ""
    if mode == "Verify my answer":
        user_attempt = st.text_area(
            "Your attempt / reasoning to verify:",
            height=85,
            placeholder="Type your preliminary answer or reasoning here...",
            key="verify_attempt_input"
        )

    language = st.selectbox(
        "Response Language",
        ["English", "Simple English", "Telugu (Technical mix)", "Hindi (Technical mix)"],
        key="global_lang_select"
    )

    st.markdown("---")

    # 2. RAG Course Document Grounding
    st.markdown("#### 📎 Course Material & Grounding")
    uploaded = st.file_uploader(
        "Attach Notes (PDF, PPTX, TXT, PY, MD, CSV)",
        type=["pdf", "pptx", "txt", "py", "md", "csv"],
        help="Upload lecture notes, textbooks, or syllabus problem sheets."
    )
    rag_toggle = False
    if uploaded:
        st.success(f"📎 Attached: **{uploaded.name}**")
        rag_toggle = st.checkbox("Ground response strictly in document (RAG Citations)", value=True)

    st.markdown("---")

    # 3. AI Engine Configuration
    st.markdown("#### 🔑 AI Engine & Provider")
    saved_openai_key = get_setting("OPENAI_API_KEY", "")
    saved_gemini_key = get_setting("GEMINI_API_KEY", "") or get_setting("GOOGLE_API_KEY", "")

    provider_choice = st.selectbox(
        "AI Engine Provider",
        ["Auto-detect / Free Built-in Mode", "Google Gemini (2.5 Flash)", "OpenAI (GPT-4o)", "Groq (LLaMA-3.3)"],
        index=0
    )

    api_key_input = st.text_input(
        "API Key (Optional)",
        value=saved_gemini_key if "Gemini" in provider_choice else (saved_openai_key if "OpenAI" in provider_choice else ""),
        type="password",
        placeholder="AIza... / sk-... / gsk_...",
        help="Leave blank to use the Built-in Zero-Config Engine with SymPy math solver."
    )
    st.session_state["active_api_key"] = api_key_input.strip()

    if st.button("🔌 Test Provider Connection", use_container_width=True):
        if not api_key_input.strip():
            st.info("ℹ️ No custom key provided. Built-in Offline Mode is 100% active with zero rate limits!")
        else:
            with st.spinner("Testing API key connection..."):
                model_to_test = "gemini-2.5-flash" if "Gemini" in provider_choice else ("llama-3.3-70b-versatile" if "Groq" in provider_choice else "gpt-4o-mini")
                res = test_api_connection(api_key_input.strip(), model=model_to_test)
                if res.get("success"):
                    st.success(res.get("message"))
                else:
                    st.error(f"Error: {res.get('message')}")

    if api_key_input.strip():
        st.caption("🟢 Connected to custom AI provider.")
    else:
        st.caption("💡 **Active:** Built-in Universal Pedagogical Engine (0 cost, SymPy math solver, dynamic code execution).")

    st.markdown("---")
    st.caption("DoubtBuster • Project 14 • GMRIT Academic Companion")

# ==============================================================================
# Workspace Tabs
# ==============================================================================
tab_chat, tab_math, tab_code, tab_history = st.tabs([
    "💬 AI Tutor Chat (Gemini Canvas)",
    "🧮 Math & Equation Studio (SymPy)",
    "🧪 Python Sandbox & Code Diagnoser",
    "📚 Learning History & Bookmarks"
])

# Quick suggestion prompt starters for empty state
PROMPT_STARTERS = [
    {
        "domain": "💻 Computer Architecture",
        "title": "Intel 8086 Architecture",
        "prompt": "Explain the Intel 8086 microprocessor internal architecture, detailing the difference between the BIU and EU, 6-byte instruction queue, and memory segmentation."
    },
    {
        "domain": "🤖 AI & Machine Learning",
        "title": "CNN & Backpropagation",
        "prompt": "How does backpropagation compute gradient descent in deep convolutional neural networks with ReLU and MaxPooling?"
    },
    {
        "domain": "🐍 Algorithms & DS",
        "title": "Recursion & Call Stack",
        "prompt": "How does recursion utilize the system call stack in Python? Write a recursive binary search with base cases and time complexity."
    },
    {
        "domain": "📐 Mathematics & Calculus",
        "title": "Symbolic Calculus Derivation",
        "prompt": "Find the symbolic derivative of f(x) = x^3 + 4*x^2 - 10 and calculate its critical points."
    },
    {
        "domain": "⚡ Electrical & Microcontrollers",
        "title": "8051 Microcontroller & Timers",
        "prompt": "Explain the Intel 8051 microcontroller architecture, Harvard memory organization, and how timer mode 1 functions."
    },
    {
        "domain": "🔬 Physics & Engineering",
        "title": "Photoelectric Effect & Photons",
        "prompt": "Explain the photoelectric effect, Einstein's photon hypothesis, and the work function equation with physical significance."
    }
]

# ==============================================================================
# TAB 1: AI TUTOR CHAT
# ==============================================================================
with tab_chat:
    # 1. Welcome Screen if conversation is empty
    if len(st.session_state["chat_messages"]) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 2.5rem 1.5rem 1.8rem 1.5rem; max-width: 860px; margin: 0 auto;">
            <h2 style="font-size: 2.2rem; font-weight: 800; letter-spacing: -0.03em; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">
                Hello, Scholar 👋
            </h2>
            <p style="color: #94a3b8; font-size: 1.05rem; margin-bottom: 2rem; line-height: 1.6;">
                What would you like to master today? Ask doubts across <strong>Computer Science, Calculus, Microprocessors, AI/ML, Engineering, or Sciences</strong>. Every answer is synthesized dynamically with step-by-step logic, LaTeX math, and verified code.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**💡 Quick Prompt Starters (Click any card to start learning):**")
        p_cols = st.columns(3)
        for i, ps in enumerate(PROMPT_STARTERS):
            col = p_cols[i % 3]
            with col:
                btn_label = f"**{ps['domain']}**\n\n_{ps['title']}_\n\n{ps['prompt'][:75]}..."
                if st.button(btn_label, key=f"starter_btn_{i}", use_container_width=True):
                    st.session_state["pending_prompt"] = ps["prompt"]
                    st.rerun()

    # 2. Render Existing Chat Messages
    for idx, msg in enumerate(st.session_state["chat_messages"]):
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑‍🎓"):
                st.markdown(msg["content"])
                if msg.get("timestamp"):
                    st.caption(f"Sent at {msg['timestamp']}")
        else:
            with st.chat_message("assistant", avatar="✨"):
                field_label = msg.get("field", "Universal Science")
                st.markdown(f'<span class="domain-pill">🏷️ {field_label}</span>', unsafe_allow_html=True)
                st.markdown(msg["content"])

                # Interactive Action Row
                doubt_id = msg.get("doubt_id")
                col_a1, col_a2, col_a3, col_a4 = st.columns([1, 1, 1, 1.8])
                with col_a1:
                    if st.button("⭐ Bookmark", key=f"bm_{idx}"):
                        if doubt_id:
                            is_bm = toggle_bookmark(doubt_id)
                            st.toast("Bookmarked in Learning History!" if is_bm else "Bookmark removed!")
                        else:
                            st.toast("Marked for quick revision!")
                with col_a2:
                    if st.button("📌 Flag Difficult", key=f"diff_{idx}"):
                        if doubt_id:
                            toggle_difficult(doubt_id)
                            st.toast("Added to personalized revision planner!")
                        else:
                            st.toast("Flagged for faculty review!")
                with col_a3:
                    if st.button("👍 Helpful", key=f"up_{idx}"):
                        if doubt_id:
                            rate_doubt(doubt_id, 1)
                        st.toast("Thank you for your feedback!")
                with col_a4:
                    if st.button("🧠 Practice Challenge", key=f"prac_{idx}"):
                        st.session_state["pending_prompt"] = f"Generate a similar practice problem with worked answer key based on this concept: {msg.get('question_ref', '')[:100]}"
                        st.rerun()

    # 3. Floating Bottom Chat Input
    chat_prompt = st.chat_input("Ask DoubtBuster anything across any domain (e.g. solve equation, write algorithm, explain concept)...")

    # Determine prompt to process
    prompt_to_process = None
    if chat_prompt:
        prompt_to_process = chat_prompt.strip()
    elif st.session_state.get("pending_prompt"):
        prompt_to_process = st.session_state["pending_prompt"].strip()
        st.session_state["pending_prompt"] = ""

    if prompt_to_process:
        try:
            validate_question(prompt_to_process)

            # Display student message immediately
            with st.chat_message("user", avatar="🧑‍🎓"):
                st.markdown(prompt_to_process)

            # Synthesize pedagogical response
            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Analyzing question & synthesizing domain explanation..."):
                    active_key = st.session_state.get("active_api_key", "")
                    chosen_model = "gemini-2.5-flash" if "Gemini" in provider_choice else ("llama-3.3-70b-versatile" if "Groq" in provider_choice else "gpt-4o-mini")

                    effective_field = detect_academic_field(prompt_to_process)

                    # Check RAG document grounding
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
                            topic="",
                            level=level,
                            mode=mode,
                            language=language,
                            attempt=user_attempt.strip(),
                            api_key=active_key,
                            model=chosen_model,
                            persist=True
                        )

                    # Retrieve recent doubt ID from SQLite for bookmark actions
                    recent_hist = get_history(limit=1)
                    doubt_id = recent_hist[0]["id"] if recent_hist else None

                    # Render generated answer
                    st.markdown(f'<span class="domain-pill">🏷️ {effective_field}</span>', unsafe_allow_html=True)
                    st.markdown(answer)

                    # Update session state messages
                    now_str = datetime.now().strftime("%I:%M %p")
                    st.session_state["chat_messages"].append({
                        "role": "user",
                        "content": prompt_to_process,
                        "timestamp": now_str
                    })
                    st.session_state["chat_messages"].append({
                        "role": "assistant",
                        "content": answer,
                        "field": effective_field,
                        "question_ref": prompt_to_process,
                        "doubt_id": doubt_id,
                        "timestamp": now_str
                    })

                    st.rerun()

        except ValueError as exc:
            st.warning(f"⚠️ {exc}")
        except Exception as exc:
            st.error(f"❌ Could not complete request: {exc}")

# ==============================================================================
# TAB 2: MATH & EQUATION STUDIO (SYMPY)
# ==============================================================================
with tab_math:
    st.markdown("### 🧮 Deterministic SymPy Mathematical Engine")
    st.caption("Verify calculus derivations, algebraic equations, limits, and matrix properties with 100% mathematical precision and zero hallucinations.")

    math_col1, math_col2 = st.columns([1.2, 1])

    with math_col1:
        math_mode = st.selectbox(
            "Select Mathematical Operation",
            [
                "Solve Equation (f(x) = 0)",
                "Symbolic Derivative",
                "Indefinite Integral",
                "Simplify Expression",
                "Limit (x -> 0)",
                "Matrix Analysis"
            ]
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
            expr_val = st.text_input(
                "Expression / Equation",
                value="3*x + 12 = 33",
                placeholder="e.g. x**2 - 5*x + 6, sin(x), 3*x + 12 = 33"
            )
            var_sym = st.text_input("Variable", value="x", max_chars=2)
            op_map = {
                "Solve Equation (f(x) = 0)": "solve",
                "Symbolic Derivative": "derivative",
                "Indefinite Integral": "integrate",
                "Simplify Expression": "simplify",
                "Limit (x -> 0)": "limit"
            }
            calc_math = st.button("Calculate Step-by-Step", type="primary")

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
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1.2rem;">
            <h4 style="margin-top:0; color: #38bdf8;">📝 Mathematical Syntax Guide</h4>
            <p style="font-size:0.85rem; color:#94a3b8;">Write math expressions in natural or Python syntax:</p>
            <ul style="font-size:0.85rem; color:#cbd5e1; padding-left:1.2rem; line-height: 1.7;">
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
# TAB 3: PYTHON SANDBOX & CODE DIAGNOSER
# ==============================================================================
with tab_code:
    st.markdown("### 🧪 Safe Python AST Code Diagnoser & Secure Sandbox")
    st.caption("Inspect syntax statically, detect unsafe modules, and run Python code safely in an isolated subprocess with a 3-second timeout.")

    code_to_check = st.text_area(
        "Paste or write Python code here:",
        height=220,
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
        if st.button("🔍 Diagnose Code Statically", type="primary", use_container_width=True):
            diag = diagnose_python_code(code_to_check)
            if not diag["success"]:
                st.warning(diag["error"])
            else:
                if diag["is_clean"]:
                    st.success("✅ **Code passed static syntax and safety checks!**")
                else:
                    if not diag["syntax_ok"]:
                        st.error("❌ **Syntax Error Detected:**")
                    else:
                        st.warning("⚠️ **Potential Issues Detected:**")

                    for issue in diag["issues"]:
                        st.markdown(f"- {issue}")

    with col_c2:
        if st.button("▶️ Execute in Secure Sandbox", type="secondary", use_container_width=True):
            with st.spinner("Running in isolated sandbox subprocess..."):
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
    st.markdown("### 📚 Student Learning History & Concept Bookmarks")
    st.caption("Review your past doubts, bookmarked questions, and revision areas directly from SQLite.")

    history_items = get_history(limit=25)
    if history_items:
        for h in history_items:
            with st.expander(f"📌 {h.get('subject', 'General')} — {h.get('question', '')[:65]}... ({h.get('created_at', '')[:10]})"):
                st.markdown(f"**Question:** {h.get('question')}")
                st.markdown(f"**Discipline:** `{h.get('subject')}` | **Topic:** `{h.get('topic') or 'General'}`")
                st.markdown(f"**Rating:** {h.get('rating', 0)} | **Bookmarked:** {'⭐ Yes' if h.get('bookmarked') else 'No'} | **Flagged Difficult:** {'📌 Yes' if h.get('marked_difficult') else 'No'}")
                st.divider()
                st.markdown(h.get("answer", ""))
    else:
        st.info("No learning history recorded yet. Start chatting in the **💬 AI Tutor Chat** tab!")

st.markdown("---")
st.markdown('<p style="text-align: center; color: #64748b; font-size: 0.85rem;">DoubtBuster • Project 14 • GMRIT Student Academic Companion</p>', unsafe_allow_html=True)
