import streamlit as st
import pandas as pd
import plotly.express as px
from backend.services.db_service import init_db, get_faculty_analytics, get_history
from components.theme import inject_theme, render_header, render_quick_nav

init_db()

st.set_page_config(
    page_title="Faculty Dashboard | DoubtBuster",
    page_icon="👨‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_theme()

render_header(
    title="👨‍🏫 Faculty Analytics & Intervention Dashboard",
    subtitle="Identify cohort misconceptions, monitor difficult topic flags, and discover data-driven areas for classroom instruction",
    badges=["📊 Cohort Heatmap", "⚠️ Misconception Tracking", "💡 Pedagogical Interventions", "AY 2026-2027"],
    show_stats=False
)

render_quick_nav(active="Faculty")

analytics = get_faculty_analytics()

# Top KPI Summary Cards
f1, f2, f3, f4 = st.columns(4)
with f1:
    st.markdown(f"""
    <div class="db-kpi-card">
        <div class="db-kpi-label">Total Student Inquiries</div>
        <div class="db-kpi-value" style="color: #38bdf8;">{analytics['total_queries']}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Logged student questions</div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown(f"""
    <div class="db-kpi-card">
        <div class="db-kpi-label">High-Difficulty Flags</div>
        <div class="db-kpi-value" style="color: #ef4444;">{len(analytics['challenging_topics'])}</div>
        <div style="font-size:0.75rem; color:#f87171;">Flagged by students</div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    avg_score = 0.0
    if analytics["quiz_performance"]:
        avg_score = round(sum(q["avg_score"] for q in analytics["quiz_performance"]) / len(analytics["quiz_performance"]), 1)
    st.markdown(f"""
    <div class="db-kpi-card">
        <div class="db-kpi-label">Cohort Quiz Mastery</div>
        <div class="db-kpi-value" style="color: {'#10b981' if avg_score >= 70 else '#f59e0b'};">{avg_score}%</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Across all quiz attempts</div>
    </div>
    """, unsafe_allow_html=True)

with f4:
    freq_count = len(analytics['frequent_topics'])
    st.markdown(f"""
    <div class="db-kpi-card">
        <div class="db-kpi-label">Distinct Topics Tracked</div>
        <div class="db-kpi-value" style="color: #818cf8;">{freq_count}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Active curriculum areas</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Classroom Interventions Section
st.subheader("💡 Recommended Classroom Interventions for Faculty")
st.caption("AI-aggregated guidance based on frequent doubts, negative ratings, and student difficulty tags.")

if analytics["suggested_interventions"]:
    for inter in analytics["suggested_interventions"]:
        st.warning(f"📌 {inter}")
else:
    st.info("No urgent interventions detected. Student satisfaction and concept mastery are currently stable.")

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
            text="query_count",
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig.update_layout(
            height=340,
            margin=dict(t=30, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0")
        )
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
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Sunset
        )
        fig_diff.update_layout(
            height=340,
            margin=dict(t=30, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0")
        )
        st.plotly_chart(fig_diff, use_container_width=True)
    else:
        st.info("No topics have been marked as difficult by students yet.")

st.divider()

# Recent Anonymized Student Doubts Feed
st.subheader("📋 Recent Student Doubts Feed (Anonymized)")
st.caption("Review genuine student questions to inform upcoming tutorial sessions, laboratory exercises, and lecture reviews.")

recent_doubts = get_history(limit=10)
if recent_doubts:
    for d in recent_doubts:
        with st.expander(f"[{d.get('subject', 'General')}] {d.get('topic') or 'Concept'}: {d.get('question', '')[:90]}..."):
            st.markdown(f"**Question:** {d.get('question')}")
            if d.get("attempt"):
                st.markdown(f"**Student's Attempt:** `{d['attempt']}`")
            st.markdown(f"**Tutor Guidance:**\n{d.get('answer', '')[:350]}...")
            st.caption(f"Logged on {d.get('created_at', '')[:10]} • Rating: {d.get('rating', 0)}")
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
- Challenging Topics Identified: {len(analytics['challenging_topics'])}

## Key Classroom Interventions
""" + "\n".join([f"- {i}" for i in analytics["suggested_interventions"]])

st.download_button(
    label="📥 Download Faculty Intervention Report (Markdown)",
    data=report_md,
    file_name="gmrit_faculty_doubtbuster_report.md",
    mime="text/markdown",
    use_container_width=True
)
