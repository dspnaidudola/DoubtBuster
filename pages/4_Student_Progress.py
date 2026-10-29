import streamlit as st
import pandas as pd
import plotly.express as px
from backend.services.db_service import init_db, get_student_stats, purge_student_data

init_db()

st.set_page_config(page_title="Student Progress | DoubtBuster", page_icon="📈", layout="wide")

st.markdown("""
<style>
.progress-header {
    background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    color: white;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.03);
}
.kpi-val {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0f172a;
}
.kpi-lbl {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="progress-header">
    <h1 style="margin:0; font-size: 2rem;">📈 Student Learning Analytics & Mastery</h1>
    <p style="margin: 0.3rem 0 0 0; color: #a7f3d0;">Real-time progress tracking, subject mastery evaluation, and personalized study recommendations.</p>
</div>
""", unsafe_allow_html=True)

stats = get_student_stats()
total_doubts = stats.get("total_doubts", 0)
total_quizzes = stats.get("total_quizzes", 0)
avg_score = stats.get("avg_quiz_score", 0.0)
streak = stats.get("study_streak", 0)
total_coding = stats.get("total_coding", 0)
passed_coding = stats.get("passed_coding", 0)

# Top KPI Metric Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-lbl">Doubts Resolved</div>
        <div class="kpi-val">{total_doubts}</div>
        <div style="font-size:0.8rem; color:#10b981;">Persistent tracking</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-lbl">Quizzes Completed</div>
        <div class="kpi-val">{total_quizzes}</div>
        <div style="font-size:0.8rem; color:#3b82f6;">Interactive tests</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-lbl">Coding Challenges</div>
        <div class="kpi-val" style="color: #6366f1;">{passed_coding}/{total_coding}</div>
        <div style="font-size:0.8rem; color:#64748b;">Passed in sandbox</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-lbl">Active Study Streak</div>
        <div class="kpi-val" style="color: #f59e0b;">🔥 {streak}</div>
        <div style="font-size:0.8rem; color:#64748b;">Consecutive active days</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Interactive Charts
col_chart1, col_chart2 = st.columns([1, 1])

with col_chart1:
    st.subheader("📊 Doubts Resolved by Subject")
    subject_counts = stats.get("subject_counts", {})
    if subject_counts:
        df_subj = pd.DataFrame(list(subject_counts.items()), columns=["Subject", "Questions"])
        fig1 = px.pie(
            df_subj,
            values="Questions",
            names="Subject",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig1.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No doubts recorded yet. Ask questions on the Home page to populate this chart.")

with col_chart2:
    st.subheader("🎯 Quiz Accuracy by Subject")
    quiz_stats = stats.get("quiz_subject_stats", {})
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
        fig2.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300, yaxis_range=[0, 100])
        fig2.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No quiz data recorded yet. Take a quiz in the Practice section to view your accuracy breakdown.")

st.divider()

# Subject Mastery Matrix
st.subheader("🏅 Subject Mastery Matrix")
all_subjects = ["Programming", "Mathematics", "Machine Learning", "Deep Learning", "NLP", "Data Science"]

m_cols = st.columns(3)
for idx, subj in enumerate(all_subjects):
    with m_cols[idx % 3]:
        d_count = subject_counts.get(subj, 0)
        q_info = quiz_stats.get(subj, {"avg_score": 0.0, "count": 0})
        q_score = q_info["avg_score"]

        if d_count == 0 and q_info["count"] == 0:
            level_text = "Not Started"
            pct = 0.05
            badge_color = "#94a3b8"
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
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:1rem; margin-bottom:1rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color:#1e293b;">{subj}</strong>
                <span style="background:{badge_color}; color:white; font-size:0.75rem; font-weight:700; padding:0.2rem 0.5rem; border-radius:6px;">{level_text}</span>
            </div>
            <div style="font-size:0.8rem; color:#64748b; margin-top:0.3rem;">{d_count} doubts asked • {q_info['count']} quizzes ({q_score}%)</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(pct)

st.divider()

# Personalized Learning Recommendations
st.subheader("💡 Tailored Learning Recommendations")
recs = []

unstudied = [s for s in all_subjects if s not in subject_counts and s not in quiz_stats]
if unstudied:
    recs.append(f"Explore **{unstudied[0]}**: You haven't resolved any doubts or taken quizzes in this area yet.")

if quiz_stats:
    low_scoring = sorted(quiz_stats.items(), key=lambda x: x[1]["avg_score"])
    if low_scoring[0][1]["avg_score"] < 70:
        recs.append(f"Reinforce **{low_scoring[0][0]}**: Your average quiz accuracy is {low_scoring[0][1]['avg_score']}%. Head to the **Study Materials** tab to review the formula and concept guide.")

if streak < 3:
    recs.append("Consistency Boost: Aim for at least one doubt or practice quiz daily to build an unstoppable study streak!")

if not recs:
    recs.append("Great job! You have broad coverage across subjects. Challenge yourself with Advanced difficulty quizzes.")

for r in recs:
    st.info(f"👉 {r}")

# Student Privacy & Data Controls
st.divider()
st.subheader("🔒 Student Privacy & Data Controls")
st.caption("Your academic history and assessment performance are stored locally on your machine in SQLite (`doubtbuster.db`). No personal student identification or registration data is transmitted externally.")

with st.expander("🛡️ Privacy Settings & Data Purge"):
    st.write("Per GMRIT academic privacy policies, you have full control over your learning records.")
    if st.button("🗑️ Purge All My Learning History & Analytics", type="secondary"):
        purge_student_data()
        st.success("All personal doubt history, quiz results, and coding attempts have been permanently cleared from local storage.")
        st.rerun()
