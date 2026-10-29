import io
import re
from typing import List, Dict, Any, Optional
import pypdf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.services.llm_service import ask_llm

def extract_pptx_slides(file_bytes: bytes) -> List[Dict[str, Any]]:
    """Extracts text per slide from PowerPoint (.pptx) files."""
    slides_data = []
    try:
        from pptx import Presentation
        prs = Presentation(io.BytesIO(file_bytes))
        for idx, slide in enumerate(prs.slides, start=1):
            text_runs = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text:
                    text_runs.append(shape.text.strip())
            slide_text = "\n".join(text_runs)
            if slide_text.strip():
                slides_data.append({
                    "section": f"Slide {idx}",
                    "text": slide_text
                })
    except Exception as e:
        slides_data.append({
            "section": "Slide Content",
            "text": f"Error parsing PPTX presentation: {e}"
        })
    return slides_data

def parse_course_document(file_obj, filename: str) -> List[Dict[str, Any]]:
    """
    Parses an uploaded file into section/page annotated passages.
    Returns list of dicts: [{'doc_name': ..., 'section': ..., 'text': ...}]
    """
    file_bytes = file_obj.getvalue()
    lower_name = filename.lower()
    sections = []

    if lower_name.endswith(".pdf"):
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page_num, page in enumerate(reader.pages, start=1):
                p_text = page.extract_text() or ""
                if p_text.strip():
                    sections.append({
                        "doc_name": filename,
                        "section": f"Page {page_num}",
                        "text": p_text.strip()
                    })
        except Exception as e:
            sections.append({
                "doc_name": filename,
                "section": "Error",
                "text": f"PDF parse error: {e}"
            })

    elif lower_name.endswith(".pptx"):
        slide_list = extract_pptx_slides(file_bytes)
        for s in slide_list:
            sections.append({
                "doc_name": filename,
                "section": s["section"],
                "text": s["text"]
            })

    else:
        # Text, Markdown, Python, CSV
        try:
            raw_text = file_bytes.decode("utf-8", errors="replace")
            # Split by markdown headers or paragraphs
            paras = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
            for idx, p in enumerate(paras, start=1):
                sections.append({
                    "doc_name": filename,
                    "section": f"Section {idx}",
                    "text": p
                })
        except Exception as e:
            sections.append({
                "doc_name": filename,
                "section": "File",
                "text": f"Text decode error: {e}"
            })

    return sections

def chunk_sections(sections: List[Dict[str, Any]], chunk_size: int = 500) -> List[Dict[str, Any]]:
    """Breaks sections into overlapping retrieval chunks with citation metadata."""
    chunks = []
    chunk_counter = 0

    for sec in sections:
        text = sec["text"]
        words = text.split()
        if not words:
            continue

        step = chunk_size // 5  # approximate words
        for i in range(0, len(words), max(1, step - 10)):
            chunk_words = words[i:i + step]
            chunk_str = " ".join(chunk_words)
            if len(chunk_str.strip()) > 30:
                chunk_counter += 1
                chunks.append({
                    "chunk_id": chunk_counter,
                    "doc_name": sec["doc_name"],
                    "section": sec["section"],
                    "content": chunk_str
                })
    return chunks

def retrieve_grounded_chunks(query: str, chunks: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """Retrieves top_k relevant document chunks using TF-IDF and Cosine Similarity."""
    if not chunks:
        return []

    corpus = [c["content"] for c in chunks]
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

        ranked_indices = similarities.argsort()[::-1][:top_k]
        results = []
        for idx in ranked_indices:
            score = round(float(similarities[idx]), 3)
            # Only include if there is some relevance or fallback to top 1
            if score > 0.05 or len(results) == 0:
                item = dict(chunks[idx])
                item["relevance_score"] = score
                results.append(item)
        return results
    except Exception:
        # Fallback to simple keyword match
        return chunks[:top_k]

def answer_with_rag(
    query: str,
    retrieved_chunks: List[Dict[str, Any]],
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini"
) -> str:
    """Answers a question strictly grounded in retrieved course materials with citations."""
    if not retrieved_chunks:
        return "No relevant course notes or slides were found matching your doubt. Please ensure your document contains information on this topic."

    # Format context with citations
    context_blocks = []
    for c in retrieved_chunks:
        context_blocks.append(f"[{c['doc_name']} - {c['section']}] (Relevance: {c.get('relevance_score', 0)}):\n\"{c['content']}\"")
    context_text = "\n\n".join(context_blocks)

    prompt = f"""
You are DoubtBuster RAG Tutor for GMRIT students.
The student asked a question based on uploaded course notes and lecture slides.

=== RETRIEVED COURSE MATERIAL (GROUND TRUTH) ===
{context_text}
================================================

Student Question:
{query}

Instructions:
1. Ground your answer strictly in the provided course material excerpts above.
2. In your explanation, explicitly cite where each fact was found using: `[Source: document_name, Section/Slide]`.
3. Distinguish between:
   - **Direct Source Information**: What the course material explicitly states.
   - **General Pedagogical Elaboration**: Intuition or helpful analogies provided to clarify the concept.
4. If the provided document does not mention an answer to part of the question, clearly state: "Note: The uploaded course material does not specify this detail."
5. Encourage active learning with one follow-up question assessing understanding.
"""
    return ask_llm(prompt, api_key=api_key, model=model)
