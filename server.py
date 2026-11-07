"""
DoubtBuster Cutting-Edge FastAPI Backend Server
Exposes high-performance, asynchronous REST APIs for:
- Multi-domain pedagogical doubt solving & offline reasoning
- Deterministic SymPy mathematics & matrix analysis
- Python AST code diagnostics & isolated subprocess sandbox
- RAG document parsing & TF-IDF grounded citations
- Student quiz generation, evaluation & persistence
- Real-time learning analytics, streaks, & faculty dashboard
"""

import os
import sys
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Ensure project root is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from backend.services.db_service import (
    init_db, save_doubt, get_history, toggle_bookmark, toggle_difficult,
    rate_doubt, delete_doubt, clear_history, get_difficult_topics,
    save_quiz_result, get_quiz_history, save_coding_attempt, get_coding_attempts,
    save_note, get_notes, delete_note, get_student_stats, purge_student_data,
    get_faculty_analytics
)
from backend.services.math_code_service import (
    solve_math_expression, analyze_matrix, diagnose_python_code
)
from backend.services.code_exec_service import (
    execute_python_code, run_coding_challenge, check_code_safety
)
from backend.services.offline_tutor import detect_academic_field
from backend.services.doc_service import (
    extract_text_from_file, CURATED_STUDY_MATERIALS
)
from backend.services.rag_service import (
    parse_course_document, chunk_sections, retrieve_grounded_chunks, answer_with_rag
)
from backend.core.pipeline import (
    answer_doubt, generate_interactive_quiz, get_adaptive_difficulty,
    CURATED_CODING_CHALLENGES
)

# Initialize database
init_db()

app = FastAPI(
    title="DoubtBuster API",
    description="Universal AI Academic Companion REST API",
    version="2.0.0"
)

# Enable CORS for Vite dev server and local clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Request / Response Schemas
# ------------------------------------------------------------------------------
class ChatRequest(BaseModel):
    question: str
    subject: Optional[str] = ""
    topic: Optional[str] = ""
    level: Optional[str] = "Intermediate"
    mode: Optional[str] = "Step-by-step explanation"
    language: Optional[str] = "English"
    attempt: Optional[str] = ""
    api_key: Optional[str] = ""
    model: Optional[str] = "offline"

class MathSolveRequest(BaseModel):
    expression: str
    operation: str = "solve"
    variable: str = "x"

class MatrixRequest(BaseModel):
    matrix_str: str

class CodeDiagnoseRequest(BaseModel):
    code: str

class CodeExecRequest(BaseModel):
    code: str
    stdin_input: Optional[str] = ""
    timeout_sec: Optional[float] = 3.0

class QuizSubmitRequest(BaseModel):
    subject: str
    topic: str
    score: int
    total_questions: int
    details: Dict[str, Any]

class ChallengeRunRequest(BaseModel):
    code: str
    challenge: Dict[str, Any]
    subject: Optional[str] = "Programming"

class NoteCreateRequest(BaseModel):
    subject: str
    topic: str
    content: str

class RateRequest(BaseModel):
    rating: int

# ------------------------------------------------------------------------------
# Core Endpoints
# ------------------------------------------------------------------------------
@app.get("/api/health")
def health_check():
    stats = get_student_stats()
    return {
        "status": "online",
        "app": "DoubtBuster",
        "version": "2.0.0",
        "study_streak": stats.get("study_streak", 0),
        "total_doubts": stats.get("total_doubts", 0)
    }

@app.post("/api/chat")
def solve_doubt_endpoint(req: ChatRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    clean_q = req.question.strip()
    detected_field = detect_academic_field(clean_q)
    
    answer = answer_doubt(
        question=clean_q,
        subject=detected_field,
        topic=req.topic or "",
        level=req.level or "Intermediate",
        mode=req.mode or "Step-by-step explanation",
        language=req.language or "English",
        attempt=req.attempt or "",
        api_key=req.api_key or "",
        model=req.model or "offline",
        persist=True
    )
    
    recent_hist = get_history(limit=1)
    doubt_id = recent_hist[0]["id"] if recent_hist else None
    
    return {
        "answer": answer,
        "field": detected_field,
        "doubt_id": doubt_id
    }

@app.post("/api/math/solve")
def math_solve_endpoint(req: MathSolveRequest):
    res = solve_math_expression(
        expression_str=req.expression,
        operation=req.operation,
        variable=req.variable
    )
    return res

@app.post("/api/math/matrix")
def math_matrix_endpoint(req: MatrixRequest):
    res = analyze_matrix(req.matrix_str)
    return res

@app.post("/api/code/diagnose")
def code_diagnose_endpoint(req: CodeDiagnoseRequest):
    res = diagnose_python_code(req.code)
    return res

@app.post("/api/code/execute")
def code_execute_endpoint(req: CodeExecRequest):
    res = execute_python_code(
        code=req.code,
        stdin_input=req.stdin_input or "",
        timeout_sec=req.timeout_sec or 3.0
    )
    return res

@app.get("/api/quiz/generate")
def quiz_generate_endpoint(
    subject: str = "Programming",
    topic: str = "",
    level: str = "Intermediate",
    num_questions: int = 3,
    api_key: str = ""
):
    questions = generate_interactive_quiz(
        subject=subject,
        topic=topic,
        level=level,
        num_questions=num_questions,
        api_key=api_key
    )
    return {"questions": questions}

@app.post("/api/quiz/submit")
def quiz_submit_endpoint(req: QuizSubmitRequest):
    q_id = save_quiz_result(
        subject=req.subject,
        topic=req.topic,
        score=req.score,
        total_questions=req.total_questions,
        details=req.details
    )
    return {"success": True, "quiz_id": q_id}

@app.get("/api/quiz/history")
def quiz_history_endpoint(limit: int = 10):
    return {"history": get_quiz_history(limit=limit)}

@app.get("/api/challenges")
def challenges_list_endpoint():
    return {"challenges": CURATED_CODING_CHALLENGES}

@app.post("/api/challenges/run")
def challenges_run_endpoint(req: ChallengeRunRequest):
    eval_res = run_coding_challenge(req.code, req.challenge)
    if eval_res.get("success"):
        save_coding_attempt(
            challenge_name=req.challenge.get("title", "Coding Challenge"),
            subject=req.subject or "Programming",
            passed=eval_res.get("all_passed", False),
            code=req.code,
            execution_time_ms=eval_res.get("execution_time_ms", 0.0)
        )
    return eval_res

@app.get("/api/challenges/history")
def challenges_history_endpoint(limit: int = 10):
    return {"history": get_coding_attempts(limit=limit)}

@app.get("/api/history")
def history_endpoint(
    subject: str = "",
    bookmarked_only: bool = False,
    difficult_only: bool = False,
    search: str = "",
    limit: int = 100
):
    items = get_history(
        subject=subject,
        bookmarked_only=bookmarked_only,
        difficult_only=difficult_only,
        search=search,
        limit=limit
    )
    difficult_topics = get_difficult_topics()
    return {
        "items": items,
        "difficult_topics": difficult_topics
    }

@app.post("/api/history/bookmark/{doubt_id}")
def bookmark_endpoint(doubt_id: int):
    new_state = toggle_bookmark(doubt_id)
    return {"success": True, "bookmarked": new_state}

@app.post("/api/history/difficult/{doubt_id}")
def difficult_endpoint(doubt_id: int):
    new_state = toggle_difficult(doubt_id)
    return {"success": True, "marked_difficult": new_state}

@app.post("/api/history/rate/{doubt_id}")
def rate_endpoint(doubt_id: int, req: RateRequest):
    rate_doubt(doubt_id, req.rating)
    return {"success": True, "rating": req.rating}

@app.delete("/api/history/{doubt_id}")
def delete_doubt_endpoint(doubt_id: int):
    delete_doubt(doubt_id)
    return {"success": True}

@app.delete("/api/history")
def clear_history_endpoint():
    clear_history()
    return {"success": True}

@app.get("/api/notes")
def notes_list_endpoint():
    return {"notes": get_notes()}

@app.post("/api/notes")
def note_create_endpoint(req: NoteCreateRequest):
    n_id = save_note(
        subject=req.subject,
        topic=req.topic,
        content=req.content
    )
    return {"success": True, "note_id": n_id}

@app.delete("/api/notes/{note_id}")
def note_delete_endpoint(note_id: int):
    delete_note(note_id)
    return {"success": True}

@app.get("/api/study/materials")
def study_materials_endpoint():
    return {"materials": CURATED_STUDY_MATERIALS}

@app.get("/api/stats")
def stats_endpoint():
    stats = get_student_stats()
    adaptive = get_adaptive_difficulty(stats)
    return {
        "stats": stats,
        "adaptive_difficulty": adaptive
    }

@app.post("/api/stats/purge")
def stats_purge_endpoint():
    purge_student_data()
    return {"success": True, "message": "All student data purged successfully."}

@app.get("/api/faculty/analytics")
def faculty_analytics_endpoint():
    analytics = get_faculty_analytics()
    return {"analytics": analytics}

# ------------------------------------------------------------------------------
# Mount Production Frontend (if built)
# ------------------------------------------------------------------------------
from fastapi.staticfiles import StaticFiles

dist_path = os.path.join(CURRENT_DIR, "dist")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")

# ------------------------------------------------------------------------------
# Server Entrypoint
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Starting DoubtBuster FastAPI Backend on http://127.0.0.1:8000")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
