import streamlit as st
import json
import io
import pandas as pd
from datetime import datetime
from backend.services.db_service import (
    init_db, get_history, toggle_bookmark, toggle_difficult, rate_doubt, delete_doubt, clear_history, get_difficult_topics
)
from components.theme import inject_theme, render_header, render_quick_nav

init_db()

st.set_page_config(
    page_title="Learning History | DoubtBuster",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_theme()

render_header(
    title="📚 Student Learning History & Revision Planner",
    subtitle="Review past doubts, revisit topics marked as challenging, and export structured study guides",
    badges=["🔍 Search & Filters", "📌 Revision Planner", "⭐ Bookmarks", "📥 Export Study Guides"],
    show_stats=False
)

render_quick_nav(active="History")

# Difficult Topics Revision Planner
difficult_topics = get_difficult_topics()
if difficult_topics:
    st.markdown("""
    <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 14px; padding: 1.4rem; margin-bottom: 1.5rem;">
        <h4 style="margin:0 0 0.4rem 0; color:#fbbf24;">📌 Personalized Revision Planner (Challenging Concepts)</h4>
        <p style="font-size:0.88rem; color:#fde68a; margin:0 0 0.8rem 0;">These concepts challenged you during recent sessions. Prioritize revising them before exams:</p>
    """, unsafe_allow_html=True)
    r_cols = st.columns(min(len(difficult_topics), 4))
    for idx, dt in enumerate(difficult_topics[:4]):
        with r_cols[idx]:
            st.info(f"**{dt['topic']}**\n\n_{dt['subject']}_\n\nFlagged **{dt['count']}** times")
    st.markdown("</div>", unsafe_allow_html=True)

# Filter controls
col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([1.5, 1.2, 1, 1])

with col_filter1:
    search_query = st.text_input("🔍 Search Past Doubts", placeholder="Search by topic, concept, or keyword...")

with col_filter2:
    subject_filter = st.selectbox(
        "Filter by Discipline",
        [
            "All Subjects",
            "Computer Science & Programming",
            "Mathematics & Statistics",
            "AI, Machine Learning & Data Science",
            "Computer Architecture & Microprocessors",
            "Electrical & Electronics Engineering",
            "Physics & Physical Sciences",
            "Economics, Business & Commerce"
        ]
    )

with col_filter3:
    bookmarked_only = st.checkbox("⭐ Bookmarked Only", value=False)

with col_filter4:
    difficult_only = st.checkbox("📌 Difficult Only", value=False)

# Fetch history
history = get_history(
    subject=subject_filter if subject_filter != "All Subjects" else "",
    bookmarked_only=bookmarked_only,
    difficult_only=difficult_only,
    search=search_query,
    limit=100
)

# Metric summary
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Questions Found", len(history))
with m2:
    bm_count = sum(1 for h in history if h.get("bookmarked") == 1)
    st.metric("Bookmarked", bm_count)
with m3:
    diff_count = sum(1 for h in history if h.get("marked_difficult") == 1)
    st.metric("Flagged Difficult", diff_count)
with m4:
    subjects_in_view = len(set(h["subject"] for h in history)) if history else 0
    st.metric("Distinct Disciplines", subjects_in_view)

st.divider()

# Export & Clear Actions
if history:
    col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 2])
    with col_exp1:
        # Markdown Export
        md_text = f"# DoubtBuster Learning History Export\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        for item in history:
            md_text += f"## {item.get('subject')} - {item.get('topic') or 'General'}\n"
            md_text += f"**Date:** {item.get('created_at', '')[:10]}\n\n"
            md_text += f"### Question:\n{item.get('question')}\n\n"
            md_text += f"### Solution / Guidance:\n{item.get('answer')}\n\n---\n\n"

        st.download_button(
            "📥 Export to Markdown",
            data=md_text,
            file_name=f"doubtbuster_history_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col_exp2:
        df_export = pd.DataFrame(history)[["id", "subject", "topic", "question", "bookmarked", "marked_difficult", "created_at"]]
        csv_buffer = io.StringIO()
        df_export.to_csv(csv_buffer, index=False)
        st.download_button(
            "📊 Export to CSV",
            data=csv_buffer.getvalue(),
            file_name=f"doubtbuster_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_exp3:
        if st.button("🗑️ Clear Entire History", type="secondary"):
            clear_history()
            st.toast("Learning history cleared successfully!")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Render History Cards
    for h in history:
        h_id = h.get("id")
        subject_tag = h.get("subject", "General")
        topic_tag = h.get("topic") or "General"
        date_str = h.get("created_at", "")[:10]
        is_bm = h.get("bookmarked") == 1
        is_diff = h.get("marked_difficult") == 1

        with st.expander(f"📌 [{subject_tag}] {h.get('question', '')[:75]}... ({date_str})"):
            st.markdown(f"**Discipline:** `{subject_tag}` | **Topic:** `{topic_tag}` | **Date:** `{date_str}`")
            st.markdown(f"**Status:** {'⭐ Bookmarked' if is_bm else '⚪ Not Bookmarked'} | {'📌 Marked Difficult' if is_diff else '⚪ Normal'}")
            st.markdown("---")
            st.markdown(f"#### ❓ Question:\n{h.get('question')}")
            st.markdown(f"#### 💡 Solution & Guidance:\n{h.get('answer')}")

            col_btn_a, col_btn_b, col_btn_c = st.columns([1, 1, 3])
            with col_btn_a:
                if st.button("Toggle ⭐", key=f"hist_bm_{h_id}"):
                    toggle_bookmark(h_id)
                    st.rerun()
            with col_btn_b:
                if st.button("Toggle 📌", key=f"hist_diff_{h_id}"):
                    toggle_difficult(h_id)
                    st.rerun()
            with col_btn_c:
                if st.button("🗑️ Delete Record", key=f"hist_del_{h_id}"):
                    delete_doubt(h_id)
                    st.toast("Record deleted!")
                    st.rerun()
else:
    st.info("No learning history found matching your filters. Head to the **💬 Ask AI Tutor** page to resolve your first doubt!")
