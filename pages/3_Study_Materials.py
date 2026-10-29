import streamlit as st
from backend.services.doc_service import CURATED_STUDY_MATERIALS, extract_text_from_file
from backend.services.llm_service import ask_llm
from backend.services.db_service import init_db, save_note, get_notes, delete_note

init_db()

st.set_page_config(page_title="Study Materials | DoubtBuster", page_icon="📄", layout="wide")

st.markdown("""
<style>
.study-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    color: white;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="study-header">
    <h1 style="margin:0; font-size: 2rem;">📄 Academic Study Hub & Document Explorer</h1>
    <p style="margin: 0.3rem 0 0 0; color: #cbd5e1;">Access curated GMRIT engineering cheat sheets, inspect uploaded PDF/code documents, and manage your personal revision notes.</p>
</div>
""", unsafe_allow_html=True)

tab_cheatsheet, tab_doc_reader, tab_notes = st.tabs([
    "📖 Curated Subject Cheat Sheets",
    "📁 Document & PDF Explorer",
    "📝 Personal Revision Notes"
])

# ==========================================
# TAB 1: CURATED SUBJECT CHEAT SHEETS
# ==========================================
with tab_cheatsheet:
    st.markdown("### 📚 Comprehensive Engineering Topic Reference")
    selected_subject = st.selectbox(
        "Select Subject to Review",
        ["Programming", "Mathematics", "Machine Learning", "Deep Learning", "NLP", "Data Science"]
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
        type=["pdf", "txt", "py", "md", "csv"],
        key="study_doc_upload"
    )

    if uploaded_doc:
        doc_text = extract_text_from_file(uploaded_doc)
        st.success(f"Successfully processed **{uploaded_doc.name}** ({len(doc_text):,} characters)")

        col_d1, col_d2 = st.columns([1, 1])
        with col_d1:
            st.subheader("📄 Document Preview")
            st.text_area("Extracted Content", value=doc_text[:3000] + ("\n... [truncated]" if len(doc_text) > 3000 else ""), height=300)

        with col_d2:
            st.subheader("✨ Concept Summary & Study Prompts")
            if st.button("Generate Concept Summary & Key Questions", type="primary"):
                with st.spinner("Analyzing document..."):
                    try:
                        active_key = st.session_state.get("active_api_key", "")
                        summary_prompt = f"""
Analyze the following course material and provide:
1. A concise 3-sentence summary of the core concepts.
2. A bulleted list of 5 key technical terms defined or referenced.
3. 3 potential exam / interview practice questions based directly on this text.

Document content:
{doc_text[:6000]}
"""
                        summary_res = ask_llm(summary_prompt, api_key=active_key)
                        st.markdown(summary_res)
                    except Exception as e:
                        st.error(f"Error analyzing document: {e}")

# ==========================================
# TAB 3: PERSONAL REVISION NOTES
# ==========================================
with tab_notes:
    st.markdown("### 📝 Student Revision Notebook")
    st.caption("Save custom formulas, code snippets, and tutor explanations to your local database.")

    with st.expander("➕ Add New Note", expanded=False):
        with st.form("new_note_form"):
            note_title = st.text_input("Title", placeholder="e.g. Master Theorem for Divide-and-Conquer")
            note_subject = st.selectbox("Subject", ["Programming", "Mathematics", "Machine Learning", "Deep Learning", "NLP", "Data Science", "General"])
            note_tags = st.text_input("Tags (comma separated)", placeholder="Algorithms, Big-O, Asymptotic")
            note_content = st.text_area("Note Content (Markdown supported)", height=150, placeholder="Write formulas, proofs, or notes here...")
            submit_note = st.form_submit_button("Save Note to Database", type="primary")

            if submit_note:
                if not note_title.strip() or not note_content.strip():
                    st.warning("Please enter both a title and note content.")
                else:
                    save_note(title=note_title.strip(), content=note_content.strip(), subject=note_subject, tags=note_tags.strip())
                    st.success("Note saved successfully!")
                    st.rerun()

    # View existing notes
    st.markdown("#### 📓 Saved Notes")
    notes = get_notes()

    if not notes:
        st.info("No saved notes yet. Click 'Add New Note' above to record key concepts!")
    else:
        for n in notes:
            with st.expander(f"📌 [{n['subject']}] {n['title']} ({n['timestamp'][:10]})"):
                if n.get("tags"):
                    st.caption(f"Tags: `{n['tags']}`")
                st.markdown(n["content"])
                if st.button("Delete Note", key=f"del_note_{n['id']}"):
                    delete_note(n["id"])
                    st.rerun()
