import streamlit as st
import pandas as pd
import plotly.express as px
from backend.services.db_service import init_db, get_faculty_analytics, get_history

init_db()

st.set_page_config(page_title="Faculty Dashboard | DoubtBuster", page_icon="👨‍🏫", layout="wide")

st.markdown("""
<style>
.faculty-header {
    background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    color: white;
    margin-bottom: 1.5rem;
}
.kpi-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.03);
}
.kpi-title {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 700;
    text-transform: uppercase;
}
.kpi-number {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0.3rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="faculty-header">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h1 style="margin:0; font-size: 2rem;">👨‍🏫 GMRIT Faculty Analytics & Intervention Dashboard</h1>
            <p style="margin: 0.3rem 0 0 0; color: #cbd5e1;">Identify common student misconceptions, track difficult topics, and discover targeted areas for classroom instruction.</p>
        </div>
        <div style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; padding: 0.6rem 1rem; text-align:center;">
            <div style="font-size: 0.75rem; color: #cbd5e1; text-transform: uppercase;">Cohort View</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff;">AY 2026-2027</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

analytics = get_faculty_analytics()

# Top KPI Summary Cards
f1, f2, f3, f4 = st.columns(4)
with f1:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">Total Student Doubts</div>
        <div class="kpi-number">{analytics['total_queries']}</div>
        <div style="font-size:0.8rem; color:#64748b;">Logged student questions</div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">High-Difficulty Flags</div>
        <div class="kpi-number" style="color:#ef4444;">{len(analytics['challenging_topics'])}</div>
        <div style="font-size:0.8rem; color:#64748b;">Flagged by students</div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    avg_score = 0.0
    if analytics["quiz_performance"]:
        avg_score = round(sum(q["avg_score"] for q in analytics["quiz_performance"]) / len(analytics["quiz_performance"]), 1)
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">Cohort Quiz Mastery</div>
        <div class="kpi-number" style="color:{'#16a34a' if avg_score >= 70 else '#f59e0b'};">{avg_score}%</div>
        <div style="font-size:0.8rem; color:#64748b;">Across all quiz attempts</div>
    </div>
    """, unsafe_allow_html=True)

with f4:
    freq_count = len(analytics['frequent_topics'])
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">Distinct Topics Tracked</div>
        <div class="kpi-number" style="color:#6366f1;">{freq_count}</div>
        <div style="font-size:0.8rem; color:#64748b;">Curriculum areas</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Classroom Interventions Section
st.subheader("💡 Recommended Classroom Interventions for Faculty")
st.caption("AI-aggregated guidance based on frequent doubts, negative ratings, and student difficulty tags.")

for inter in analytics["suggested_interventions"]:
    st.warning(f"📌 {inter}")

st.divider()

# Topic Confusion & Doubt Frequency Heatmap
col_g1, col_g2 = st.columns([1.2, 1])

with col_g1:
    st.subheader("📊 Most Frequently Asked Topics")
    if analytics["frequent_topics"]:
        df_freq = pd.DataFrame(analytics["frequent_topics"])
        fig = px.bar(
            df_freq,
            x="topic",
            y="query_count",
            color="subject",
            title="Doubt Volume per Topic",
            labels={"query_count": "Number of Doubts", "topic": "Topic"},
            text="query_count"
        )
        fig.update_layout(height=340, margin=dict(t=30, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No topic query data recorded yet.")

with col_g2:
    st.subheader("⚠️ Topics Flagged as Difficult by Students")
    if analytics["challenging_topics"]:
        df_diff = pd.DataFrame(analytics["challenging_topics"])
        fig_diff = px.pie(
            df_diff,
            names="topic",
            values="cnt",
            title="Distribution of Difficult Topic Flags",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_diff.update_layout(height=340, margin=dict(t=30, b=10, l=10, r=10))
        st.plotly_chart(fig_diff, use_container_width=True)
    else:
        st.info("No topics have been marked as difficult by students yet.")

st.divider()

# Recent Anonymized Student Doubts
st.subheader("📋 Recent Student Doubts Feed (Anonymized)")
st.caption("Review genuine student questions to inform tutorial and lab sessions.")

recent_doubts = get_history(limit=10)
if recent_doubts:
    for d in recent_doubts:
        with st.expander(f"[{d['subject']}] {d['topic'] or 'Concept'}: {d['question'][:90]}..."):
            st.markdown(f"**Question:** {d['question']}")
            if d.get("attempt"):
                st.markdown(f"**Student's Attempt:** `{d['attempt']}`")
            st.markdown(f"**Tutor Guidance:**\n{d['answer'][:350]}...")
            st.caption(f"Logged at {d['timestamp'][:16].replace('T', ' ')} • Rating: {d.get('rating', 0)}")
else:
    st.info("No student doubts recorded yet.")

st.divider()
# Export Faculty Analytics Report
st.subheader("📥 Export Faculty Summary")
report_md = f"""# GMRIT Faculty Analytics Report
Generated on: AY 2026-2027

## Cohort Summary
- Total Questions Asked: {analytics['total_queries']}
- Average Quiz Mastery: {avg_score}%

## Key Classroom Interventions
""" + "\n".join([f"- {i}" for i in analytics["suggested_interventions"]])

st.download_button(
    label="Download Faculty Intervention Report (Markdown)",
    data=report_md,
    file_name="gmrit_faculty_doubtbuster_report.md",
    mime="text/markdown"
)
