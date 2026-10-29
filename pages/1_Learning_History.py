import streamlit as st
import json
from datetime import datetime
from backend.services.db_service import (
    init_db, get_history, toggle_bookmark, toggle_difficult, rate_doubt, delete_doubt, clear_history, get_difficult_topics
)

init_db()

st.set_page_config(page_title="Learning History | DoubtBuster", page_icon="📚", layout="wide")

st.markdown("""
<style>
.history-header {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    color: white;
    margin-bottom: 1.5rem;
}
.revision-card {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1.5rem;
}
.time-tag {
    color: #64748b;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="history-header">
    <h1 style="margin:0; font-size: 2rem;">📚 Student Learning History & Revision Planner</h1>
    <p style="margin: 0.3rem 0 0 0; color: #c7d2fe;">Review past doubts, revisit topics marked as difficult, and export structured study reports.</p>
</div>
""", unsafe_allow_html=True)

# Difficult Topics Revision Planner
difficult_topics = get_difficult_topics()
if difficult_topics:
    st.markdown("""
    <div class="revision-card">
        <h4 style="margin:0 0 0.5rem 0; color:#92400e;">📌 Personalized Revision Planner (Topics You Marked as Difficult)</h4>
        <p style="font-size:0.88rem; color:#78350f; margin:0 0 0.6rem 0;">These topics challenged you during recent sessions. Take time to re-solve related practice problems:</p>
    """, unsafe_allow_html=True)
    r_cols = st.columns(min(len(difficult_topics), 4))
    for idx, dt in enumerate(difficult_topics[:4]):
        with r_cols[idx]:
            st.info(f"**{dt['topic']}** ({dt['subject']})\n\nFlagged {dt['count']} times")
    st.markdown("</div>", unsafe_allow_html=True)

# Filter controls
col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([1.5, 1, 1, 1])

with col_filter1:
    search_query = st.text_input("🔍 Search History", placeholder="Search by topic, keyword, or concept...")

with col_filter2:
    subject_filter = st.selectbox(
        "Filter by Subject",
        ["All Subjects", "Programming", "Mathematics", "Machine Learning", "Deep Learning", "NLP", "Data Science", "Other"]
    )

with col_filter3:
    bookmarked_only = st.checkbox("⭐ Bookmarked Only", value=False)

with col_filter4:
    difficult_only = st.checkbox("📌 Difficult Only", value=False)

# Fetch history
history = get_history(
    subject=subject_filter,
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
    st.metric("Distinct Subjects", subjects_in_view)

st.divider()

if not history:
    st.info("No learning history found matching your filters. Head to the **Ask AI Doubt Tutor** home page to ask a question!")
else:
    for item in history:
        doubt_id = item["id"]
        formatted_time = item["timestamp"][:16].replace("T", " ")
        is_bm = item.get("bookmarked", 0) == 1
        is_diff = item.get("marked_difficult", 0) == 1
        rating = item.get("rating", 0)

        bm_icon = "⭐" if is_bm else "☆"
        diff_tag = " [📌 Difficult]" if is_diff else ""
        rating_badge = "👍" if rating > 0 else ("👎" if rating < 0 else "")

        title = f"{bm_icon}{diff_tag} [{item['subject']}] {item['topic'] or 'General Doubt'}: {item['question'][:75]}... ({formatted_time})"
        
        with st.expander(title, expanded=False):
            st.markdown(f"**Subject:** `{item['subject']}` | **Difficulty:** `{item.get('level', 'Beginner')}` | **Mode:** `{item.get('mode', 'Step-by-step')}` | {rating_badge}")
            st.markdown(f"<span class='time-tag'>Asked on: {formatted_time}</span>", unsafe_allow_html=True)
            
            st.markdown("#### ❓ Question:")
            st.info(item["question"])

            if item.get("attempt"):
                st.markdown("#### ✍️ Your Attempt:")
                st.code(item["attempt"])

            st.markdown("#### 💡 Tutor Guidance:")
            st.markdown(item["answer"])

            # Card action buttons
            col_b1, col_b2, col_b3, col_b4 = st.columns([1, 1.2, 1, 2])
            with col_b1:
                bm_label = "Unstar" if is_bm else "⭐ Bookmark"
                if st.button(bm_label, key=f"bm_{doubt_id}"):
                    toggle_bookmark(doubt_id)
                    st.rerun()

            with col_b2:
                diff_label = "Unflag" if is_diff else "📌 Flag Difficult"
                if st.button(diff_label, key=f"diff_{doubt_id}"):
                    toggle_difficult(doubt_id)
                    st.rerun()

            with col_b3:
                if st.button("🗑️ Delete", key=f"del_{doubt_id}"):
                    delete_doubt(doubt_id)
                    st.rerun()

    # Export & Management Section
    st.divider()
    st.subheader("📥 Export & Backup")
    exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 1])

    with exp_col1:
        json_data = json.dumps(history, indent=2)
        st.download_button(
            label="Download as JSON",
            data=json_data,
            file_name=f"doubtbuster_history_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )

    with exp_col2:
        md_lines = ["# 🎓 DoubtBuster Learning History Report\n\n"]
        for h in history:
            md_lines.append(f"## [{h['subject']}] {h.get('topic', 'Doubt')} ({h['timestamp'][:10]})\n")
            md_lines.append(f"**Question:**\n{h['question']}\n\n")
            if h.get('attempt'):
                md_lines.append(f"**Student Attempt:**\n{h['attempt']}\n\n")
            md_lines.append(f"**Explanation:**\n{h['answer']}\n\n---\n\n")
        md_report = "".join(md_lines)

        st.download_button(
            label="Download as Markdown Report",
            data=md_report,
            file_name=f"doubtbuster_report_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with exp_col3:
        if st.button("⚠️ Clear All History", type="secondary", use_container_width=True):
            clear_history()
            st.success("All learning history cleared!")
            st.rerun()
