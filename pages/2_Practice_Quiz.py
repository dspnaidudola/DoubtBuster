import streamlit as st
import json
from backend.config import get_setting
from backend.core.pipeline import generate_interactive_quiz, CURATED_CODING_CHALLENGES
from backend.services.code_exec_service import run_coding_challenge, execute_python_code
from backend.services.db_service import init_db, save_quiz_result, get_quiz_history, save_coding_attempt, get_coding_attempts

init_db()

st.set_page_config(page_title="Practice & Assessment | DoubtBuster", page_icon="🧠", layout="wide")

st.markdown("""
<style>
.quiz-header {
    background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    color: white;
    margin-bottom: 1.5rem;
}
.score-badge {
    font-size: 2rem;
    font-weight: 800;
    color: #4f46e5;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="quiz-header">
    <h1 style="margin:0; font-size: 2rem;">🧠 Interactive Practice & Coding Assessments</h1>
    <p style="margin: 0.3rem 0 0 0; color: #c7d2fe;">Test your knowledge with conceptual multiple-choice quizzes and hands-on coding challenges validated in a secure sandbox.</p>
</div>
""", unsafe_allow_html=True)

tab_mcq, tab_coding = st.tabs([
    "📝 Multiple-Choice Conceptual Quiz",
    "💻 Live Coding Challenges & Sandbox"
])

# ==========================================
# TAB 1: MCQ QUIZZES
# ==========================================
with tab_mcq:
    col_cfg1, col_cfg2, col_cfg3, col_cfg4 = st.columns([1.2, 1.2, 1, 1])

    with col_cfg1:
        subject = st.selectbox(
            "Subject",
            ["Programming", "Mathematics", "Machine Learning", "Deep Learning", "NLP", "Data Science"],
            key="mcq_subject"
        )

    with col_cfg2:
        topic = st.text_input("Topic (optional)", placeholder="e.g. Recursion, Loss Functions, Eigenvalues", key="mcq_topic")

    with col_cfg3:
        level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"], key="mcq_level")

    with col_cfg4:
        num_q = st.selectbox("Number of Questions", [3, 4, 5], index=0, key="mcq_num")

    active_key = st.session_state.get("active_api_key", "") or get_setting("OPENAI_API_KEY", "")
    chosen_model = get_setting("OPENAI_MODEL", "gpt-4o-mini")

    if st.button("🚀 Generate Quiz", type="primary"):
        with st.spinner("Generating quiz questions..."):
            try:
                questions = generate_interactive_quiz(
                    subject=subject,
                    topic=topic.strip(),
                    level=level,
                    num_questions=num_q,
                    api_key=active_key,
                    model=chosen_model
                )
                st.session_state["quiz_questions"] = questions
                st.session_state["quiz_subject"] = subject
                st.session_state["quiz_topic"] = topic or "General"
                st.session_state["quiz_submitted"] = False
                st.session_state["user_answers"] = {}
                st.rerun()
            except Exception as exc:
                st.error(f"Error generating quiz: {exc}")

    # Display Active Quiz
    if st.session_state.get("quiz_questions"):
        questions = st.session_state["quiz_questions"]
        st.divider()
        st.subheader(f"📝 Quiz: {st.session_state.get('quiz_subject')} — {len(questions)} Questions")

        if not st.session_state.get("quiz_submitted", False):
            with st.form("quiz_form"):
                user_selections = {}
                for idx, q in enumerate(questions):
                    st.markdown(f"**Question {idx + 1}:** {q['question']}")
                    opts = q.get("options", [])
                    user_choice = st.radio(
                        f"Select answer for Q{idx + 1}:",
                        options=range(len(opts)),
                        format_func=lambda i, opts=opts: f"{chr(65 + i)}) {opts[i]}",
                        key=f"q_{idx}"
                    )
                    user_selections[idx] = user_choice
                    st.markdown("---")

                submit_quiz = st.form_submit_button("🏁 Submit Quiz for Grading", type="primary")

                if submit_quiz:
                    st.session_state["user_answers"] = user_selections
                    st.session_state["quiz_submitted"] = True
                    
                    score = 0
                    for idx, q in enumerate(questions):
                        if user_selections.get(idx) == q.get("correct"):
                            score += 1
                    
                    st.session_state["quiz_score"] = score
                    save_quiz_result(
                        subject=st.session_state.get("quiz_subject", "General"),
                        topic=st.session_state.get("quiz_topic", "General"),
                        score=score,
                        total_questions=len(questions),
                        details=user_selections
                    )
                    st.rerun()
        else:
            score = st.session_state.get("quiz_score", 0)
            total = len(questions)
            pct = round((score / total) * 100, 1)

            res_col1, res_col2 = st.columns([1, 2])
            with res_col1:
                st.markdown(f"""
                <div style="background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 16px; padding: 1.5rem; text-align: center;">
                    <div style="font-size: 0.9rem; color: #64748b; text-transform: uppercase; font-weight: 700;">Your Score</div>
                    <div class="score-badge">{score} / {total}</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: {'#16a34a' if pct >= 70 else '#ea580c'};">{pct}%</div>
                </div>
                """, unsafe_allow_html=True)
                if pct >= 80:
                    st.balloons()
                    st.success("🌟 Outstanding performance! You have a solid grasp of these concepts.")
                elif pct >= 60:
                    st.info("👍 Good effort! Review the detailed solutions below to solidify your understanding.")
                else:
                    st.warning("💪 Review the concepts and solutions below, then try another quiz!")

                if st.button("🔄 Retake or New Quiz"):
                    st.session_state["quiz_submitted"] = False
                    st.session_state["quiz_questions"] = None
                    st.rerun()

            with res_col2:
                st.markdown("### 📋 Step-by-Step Question Review")
                user_answers = st.session_state.get("user_answers", {})
                for idx, q in enumerate(questions):
                    user_ans_idx = user_answers.get(idx)
                    correct_idx = q.get("correct", 0)
                    is_correct = user_ans_idx == correct_idx
                    opts = q.get("options", [])

                    status_icon = "✅ Correct" if is_correct else "❌ Incorrect"
                    with st.expander(f"Q{idx + 1}: {status_icon} — {q['question'][:70]}...", expanded=True):
                        st.markdown(f"**Question:** {q['question']}")
                        for o_idx, opt in enumerate(opts):
                            prefix = f"{chr(65 + o_idx)}) "
                            if o_idx == correct_idx:
                                st.markdown(f"🟢 **{prefix}{opt}** *(Correct Answer)*")
                            elif o_idx == user_ans_idx and not is_correct:
                                st.markdown(f"🔴 **{prefix}{opt}** *(Your Choice)*")
                            else:
                                st.markdown(f"⚪ {prefix}{opt}")

                        st.markdown("---")
                        st.markdown(f"**💡 Explanation:** {q.get('explanation', 'Review core principles.')}")

    # Past Quiz Performance from SQLite
    st.divider()
    st.subheader("📊 Your Past Quiz History")
    past_quizzes = get_quiz_history(limit=5)
    if not past_quizzes:
        st.info("No past quiz records yet. Complete a quiz above to record your score!")
    else:
        for qh in past_quizzes:
            col_q1, col_q2, col_q3, col_q4 = st.columns([1.5, 1, 1, 1])
            with col_q1:
                st.write(f"**{qh['subject']}** — {qh['topic']}")
            with col_q2:
                st.write(f"Score: **{qh['score']}/{qh['total_questions']}** ({qh['percentage']}%)")
            with col_q3:
                st.write(qh['timestamp'][:16].replace("T", " "))
            with col_q4:
                st.progress(qh['percentage'] / 100)

# ==========================================
# TAB 2: LIVE CODING CHALLENGES & SANDBOX
# ==========================================
with tab_coding:
    st.markdown("### 💻 Live Coding Challenges with Test-Case Verification")
    st.caption("Write solutions to algorithmic, mathematics, or ML challenges and run them in our isolated Python sandbox.")

    code_subject = st.selectbox("Subject for Coding Challenges", list(CURATED_CODING_CHALLENGES.keys()), key="code_subj_select")
    available_challenges = CURATED_CODING_CHALLENGES[code_subject]

    challenge_titles = [c["title"] for c in available_challenges]
    selected_ch_title = st.selectbox("Select Challenge", challenge_titles)
    selected_ch = next(c for c in available_challenges if c["title"] == selected_ch_title)

    st.markdown(f"#### 📌 Problem: {selected_ch['title']}")
    st.info(selected_ch["description"])

    user_code_attempt = st.text_area(
        "Your Solution Code:",
        value=selected_ch["starter_code"],
        height=180,
        key=f"code_editor_{selected_ch_title}"
    )

    if st.button("🚀 Run & Verify Against Test Cases", type="primary"):
        with st.spinner("Executing solution against test cases in sandbox..."):
            eval_res = run_coding_challenge(user_code_attempt, selected_ch)

            if not eval_res["success"]:
                st.error(f"❌ Error during test run: {eval_res.get('error')}")
            else:
                all_passed = eval_res["all_passed"]
                if all_passed:
                    st.success(f"🎉 **All Test Cases Passed!** Execution Time: {eval_res['execution_time_ms']} ms")
                else:
                    st.warning(f"⚠️ **Some test cases failed.** Execution Time: {eval_res['execution_time_ms']} ms")

                save_coding_attempt(
                    challenge_name=selected_ch_title,
                    subject=code_subject,
                    passed=all_passed,
                    code=user_code_attempt,
                    execution_time_ms=eval_res.get("execution_time_ms", 0.0)
                )

                st.markdown("#### Test Case Results:")
                for idx, tc in enumerate(eval_res["results"], start=1):
                    p_icon = "✅ Passed" if tc["passed"] else "❌ Failed"
                    st.markdown(f"- **Test Case {idx}:** {p_icon} | **Input:** `{tc['input']}` | **Expected:** `{tc['expected']}` | **Actual:** `{tc['actual']}`")

    # Coding attempts history
    st.divider()
    st.subheader("📜 Past Coding Challenge Submissions")
    c_attempts = get_coding_attempts(limit=5)
    if c_attempts:
        for ca in c_attempts:
            pass_status = "✅ Passed" if ca["passed"] == 1 else "❌ Failed"
            st.write(f"**{ca['challenge_name']}** ({ca['subject']}) — {pass_status} ({ca['execution_time_ms']} ms) at {ca['timestamp'][:16].replace('T', ' ')}")
    else:
        st.info("No coding challenges submitted yet. Try one above!")
