import streamlit as st
import pandas as pd
import plotly.express as px
from backend.services.db_service import init_db, get_student_stats, purge_student_data
from components.theme import inject_theme, render_header, render_quick_nav

init_db()

st.set_page_config(
    page_title="Student Progress | DoubtBuster",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_theme()

stats = get_student_stats()
total_doubts = stats.get("total_doubts", 0)
total_quizzes = stats.get("total_quizzes", 0)
avg_score = stats.get("avg_quiz_score", 0.0)
streak = stats.get("study_streak", 0)
total_coding = stats.get("total_coding", 0)
passed_coding = stats.get("passed_coding", 0)

render_header(
    title="📈 Student Learning Analytics & Mastery",
    subtitle="Real-time progress tracking, subject mastery evaluation, and personalized study recommendations",
    badges=["🔥 Study Streak", "🎯 Quiz Mastery", "💻 Sandbox Coding", "🔒 100% Local Privacy"],
    streak=streak,
    doubts_count=total_doubts,
    show_stats=True
)

render_quick_nav(active="Progress")

# Top KPI Metric Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"""
    <div class="db-kpi-card">
        <div class="db-kpi-label">Doubts Resolved</div>
        <div class="db-kpi-value" style="color: #38bdf8;">{total_doubts}</div>
        <div style="font-size:0.75rem; color:#10b981;">Persistent tracking</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="db-kpi-card">
        <div class="db-kpi-label">Quizzes Completed</div>
        <div class="db-kpi-value" style="color: #818cf8;">{total_quizzes}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Avg: {avg_score}% accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="db-kpi-card">
        <div class="db-kpi-label">Coding Challenges</div>
        <div class="db-kpi-value" style="color: #f472b6;">{passed_coding}/{total_coding}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Passed in sandbox</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="db-kpi-card">
        <div class="db-kpi-label">Active Study Streak</div>
        <div class="db-kpi-value" style="color: #fbbf24;">🔥 {streak}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Consecutive days</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Interactive Charts
col_chart1, col_chart2 = st.columns([1, 1])

subject_counts = stats.get("subject_counts", {})
quiz_stats = stats.get("quiz_subject_stats", {})

with col_chart1:
    st.subheader("📊 Doubts Resolved by Discipline")
    if subject_counts:
        df_subj = pd.DataFrame(list(subject_counts.items()), columns=["Subject", "Questions"])
        fig1 = px.pie(
            df_subj,
            values="Questions",
            names="Subject",
            hole=0.48,
            color_discrete_sequence=px.colors.sequential.Plasma_r
        )
        fig1.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0")
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No doubts recorded yet. Ask questions on the Home page to populate this distribution.")

with col_chart2:
    st.subheader("🎯 Quiz Accuracy by Discipline")
    if quiz_stats:
        data_quiz = []
        for subj, d in quiz_stats.items():
            data_quiz.append({"Subject": subj, "Average Score (%)": d["avg_score"], "Quizzes Taken": d["count"]})
        df_qz = pd.DataFrame(data_quiz)
        fig2 = px.bar(
            df_qz,
            x="Subject",
            y="Average Score (%)",
            color="Average Score (%)",
            color_continuous_scale="Viridis",
            text="Average Score (%)"
        )
        fig2.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            height=320,
            yaxis_range=[0, 100],
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0")
        )
        fig2.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No quiz data recorded yet. Complete a quiz in the Practice section to view your accuracy breakdown.")

st.divider()

# Subject Mastery Matrix
st.subheader("🏅 Academic Mastery Matrix")
all_subjects = [
    "Computer Science & Programming",
    "Mathematics & Statistics",
    "AI, Machine Learning & Data Science",
    "Computer Architecture & Microprocessors",
    "Electrical & Electronics Engineering",
    "Physics & Physical Sciences"
]

m_cols = st.columns(3)
for idx, subj in enumerate(all_subjects):
    with m_cols[idx % 3]:
        d_count = subject_counts.get(subj, 0)
        q_info = quiz_stats.get(subj, {"avg_score": 0.0, "count": 0})
        q_score = q_info["avg_score"]

        if d_count == 0 and q_info["count"] == 0:
            level_text = "Not Started"
            pct = 0.05
            badge_color = "#64748b"
        elif d_count < 3 and q_score < 60:
            level_text = "Novice"
            pct = 0.3
            badge_color = "#3b82f6"
        elif d_count < 5 or q_score < 75:
            level_text = "Developing"
            pct = 0.65
            badge_color = "#f59e0b"
        else:
            level_text = "Proficient"
            pct = 0.95
            badge_color = "#10b981"

        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1.1rem; margin-bottom: 1rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color:#f8fafc; font-size: 0.9rem;">{subj}</strong>
                <span style="background:{badge_color}; color:white; font-size:0.72rem; font-weight:700; padding:0.2rem 0.55rem; border-radius:6px;">{level_text}</span>
            </div>
            <div style="font-size:0.78rem; color:#94a3b8; margin-top:0.35rem;">{d_count} doubts asked • {q_info['count']} quizzes ({q_score}%)</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(pct)

st.divider()

# Privacy & Data Controls
st.subheader("🛡️ Student Privacy & Data Management")
st.caption("DoubtBuster stores all learning history, notes, and quiz metrics in a local SQLite database on your machine with 0 telemetry.")

with st.expander("⚠️ Data Management & Purge Controls", expanded=False):
    st.warning("Purging data will permanently delete your doubts, quizzes, notes, and coding attempts from your local database.")
    col_p1, col_p2 = st.columns([1, 3])
    with col_p1:
        if st.button("🗑️ Purge All Student Data", type="primary"):
            purge_student_data()
            st.success("All student data purged successfully from local database!")
            st.rerun()
