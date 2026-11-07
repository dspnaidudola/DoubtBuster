import streamlit as st
from backend.services.doc_service import CURATED_STUDY_MATERIALS, extract_text_from_file
from backend.services.llm_service import ask_llm
from backend.services.db_service import init_db, save_note, get_notes, delete_note
from components.theme import inject_theme, render_header, render_quick_nav

init_db()

st.set_page_config(
    page_title="Study Materials | DoubtBuster",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_theme()

render_header(
    title="📄 Academic Study Hub & Document Explorer",
    subtitle="Access curated engineering cheat sheets, inspect uploaded lecture slides/PDFs, and manage your revision notebook",
    badges=["📖 Topic Reference", "📁 PDF & PPTX Analyzer", "📝 Revision Notes", "⚡ Local Storage"],
    show_stats=False
)

render_quick_nav(active="Study")

tab_cheatsheet, tab_doc_reader, tab_notes = st.tabs([
    "📖 Curated Subject Cheat Sheets",
    "📁 Document & PDF Concept Explorer",
    "📝 Personal Revision Notebook"
])

# ==========================================
# TAB 1: CURATED SUBJECT CHEAT SHEETS
# ==========================================
with tab_cheatsheet:
    st.markdown("### 📚 Comprehensive Engineering Topic Reference")
    selected_subject = st.selectbox(
        "Select Academic Subject to Review",
        list(CURATED_STUDY_MATERIALS.keys())
    )

    mat = CURATED_STUDY_MATERIALS.get(selected_subject)
    if mat:
        st.caption(mat["description"])
        st.markdown(mat["content"])

# ==========================================
# TAB 2: DOCUMENT & PDF EXPLORER
# ==========================================
with tab_doc_reader:
    st.markdown("### 📁 Document Inspection & Concept Summarizer")
    st.caption("Upload lecture slides, problem sheets, or syllabus notes in PDF, TXT, PY, or MD format.")

    uploaded_doc = st.file_uploader(
        "Choose a course material file",
        type=["pdf", "pptx", "txt", "py", "md", "csv"],
        key="study_doc_upload"
    )

    if uploaded_doc:
        doc_text = extract_text_from_file(uploaded_doc)
        st.success(f"📎 Successfully processed **{uploaded_doc.name}** ({len(doc_text):,} characters extracted)")

        col_d1, col_d2 = st.columns([1, 1])
        with col_d1:
            st.subheader("📄 Extracted Text Preview")
            st.text_area(
                "Document Content",
                value=doc_text[:3500] + ("\n... [truncated for display]" if len(doc_text) > 3500 else ""),
                height=320
            )

        with col_d2:
            st.subheader("✨ Concept Summary & Study Prompts")
            if st.button("Generate Structured Summary & Key Questions", type="primary", use_container_width=True):
                with st.spinner("Analyzing document structure and extracting concepts..."):
                    try:
                        active_key = st.session_state.get("active_api_key", "")
                        summary_prompt = f"""
Analyze the following course material and provide:
1. A concise 3-sentence summary of the core academic concepts.
2. A bulleted list of 5 key technical terms defined or referenced with 1-line definitions.
3. 3 high-yield university exam / viva questions based directly on this text.

Document content:
{doc_text[:6000]}
"""
                        summary_res = ask_llm(summary_prompt, api_key=active_key)
                        st.markdown(summary_res)
                    except Exception as e:
                        # Fallback structured extraction
                        st.markdown(f"""
                        #### 📑 Automated Document Outline
                        - **Total Characters Extracted:** {len(doc_text):,}
                        - **Sample Keywords Detected:** {', '.join([w for w in doc_text.split() if len(w) > 6][:10])}
                        
                        **Quick Recommendation:** Ground your questions in the **💬 AI Tutor Chat** tab with RAG enabled to retrieve citations directly from this document.
                        """)

# ==========================================
# TAB 3: PERSONAL REVISION NOTES
# ==========================================
with tab_notes:
    st.markdown("### 📝 Student Revision Notebook")
    st.caption("Save custom formulas, code snippets, and tutor explanations to your local SQLite database.")

    with st.expander("➕ Add New Revision Note", expanded=False):
        with st.form("new_note_form"):
            note_topic = st.text_input("Note Topic / Concept", placeholder="e.g. 8086 Memory Segmentation, Taylor Series")
            note_subject = st.selectbox(
                "Subject Area",
                ["Programming", "Mathematics", "Machine Learning", "Deep Learning", "Microprocessors", "Physics", "Other"]
            )
            note_content = st.text_area("Note Content / Key Takeaway", height=120)
            submitted_note = st.form_submit_button("💾 Save Note to Database", type="primary")

            if submitted_note:
                if not note_topic.strip() or not note_content.strip():
                    st.warning("Please provide both a topic and note content.")
                else:
                    save_note(subject=note_subject, topic=note_topic.strip(), content=note_content.strip())
                    st.success("Note saved successfully!")
                    st.rerun()

    # View existing notes
    saved_notes = get_notes()
    if saved_notes:
        st.markdown(f"**Saved Notes ({len(saved_notes)}):**")
        for n in saved_notes:
            n_id = n.get("id")
            with st.expander(f"📌 [{n.get('subject')}] {n.get('topic')} ({n.get('created_at', '')[:10]})"):
                st.markdown(n.get("content"))
                if st.button("🗑️ Delete Note", key=f"del_note_{n_id}"):
                    delete_note(n_id)
                    st.toast("Note deleted!")
                    st.rerun()
    else:
        st.info("No revision notes saved yet. Click **➕ Add New Revision Note** above to record key concepts!")
