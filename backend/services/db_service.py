import os
import sqlite3
import json
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "doubtbuster.db")

def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    target_path = db_path or DB_FILE
    conn = sqlite3.connect(target_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: Optional[str] = None) -> None:
    conn = get_connection(db_path)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                subject TEXT NOT NULL,
                topic TEXT,
                level TEXT,
                mode TEXT,
                question TEXT NOT NULL,
                attempt TEXT,
                answer TEXT NOT NULL,
                rating INTEGER DEFAULT 0,
                bookmarked INTEGER DEFAULT 0,
                marked_difficult INTEGER DEFAULT 0
            )
        """)
        # Ensure marked_difficult column exists if upgrading older DB
        try:
            conn.execute("ALTER TABLE history ADD COLUMN marked_difficult INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # column already exists

        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                subject TEXT NOT NULL,
                topic TEXT,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                details_json TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS student_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                subject TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS coding_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                challenge_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                passed INTEGER NOT NULL,
                code TEXT NOT NULL,
                execution_time_ms REAL
            )
        """)
    conn.close()

def save_doubt(
    question: str,
    answer: str,
    subject: str = "General",
    topic: str = "",
    level: str = "Beginner",
    mode: str = "Step-by-step explanation",
    attempt: str = "",
    bookmarked: bool = False,
    marked_difficult: bool = False,
    db_path: Optional[str] = None
) -> int:
    init_db(db_path)
    now_str = datetime.now().isoformat()
    conn = get_connection(db_path)
    with conn:
        cursor = conn.execute("""
            INSERT INTO history (timestamp, subject, topic, level, mode, question, attempt, answer, rating, bookmarked, marked_difficult)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
        """, (now_str, subject, topic, level, mode, question, attempt, answer, 1 if bookmarked else 0, 1 if marked_difficult else 0))
        inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_history(
    subject: Optional[str] = None,
    bookmarked_only: bool = False,
    difficult_only: bool = False,
    search: Optional[str] = None,
    limit: int = 100,
    db_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    init_db(db_path)
    conn = get_connection(db_path)
    query = "SELECT * FROM history WHERE 1=1"
    params: List[Any] = []

    if subject and subject != "All Subjects":
        query += " AND subject = ?"
        params.append(subject)

    if bookmarked_only:
        query += " AND bookmarked = 1"

    if difficult_only:
        query += " AND marked_difficult = 1"

    if search and search.strip():
        term = f"%{search.strip().lower()}%"
        query += " AND (LOWER(question) LIKE ? OR LOWER(topic) LIKE ? OR LOWER(answer) LIKE ?)"
        params.extend([term, term, term])

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results

def get_doubt(doubt_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    init_db(db_path)
    conn = get_connection(db_path)
    row = conn.execute("SELECT * FROM history WHERE id = ?", (doubt_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def toggle_bookmark(doubt_id: int, db_path: Optional[str] = None) -> bool:
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        row = conn.execute("SELECT bookmarked FROM history WHERE id = ?", (doubt_id,)).fetchone()
        if not row:
            conn.close()
            return False
        new_val = 0 if row["bookmarked"] == 1 else 1
        conn.execute("UPDATE history SET bookmarked = ? WHERE id = ?", (new_val, doubt_id))
    conn.close()
    return bool(new_val)

def toggle_difficult(doubt_id: int, db_path: Optional[str] = None) -> bool:
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        row = conn.execute("SELECT marked_difficult FROM history WHERE id = ?", (doubt_id,)).fetchone()
        if not row:
            conn.close()
            return False
        new_val = 0 if row["marked_difficult"] == 1 else 1
        conn.execute("UPDATE history SET marked_difficult = ? WHERE id = ?", (new_val, doubt_id))
    conn.close()
    return bool(new_val)

def rate_doubt(doubt_id: int, rating: int, db_path: Optional[str] = None) -> bool:
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        conn.execute("UPDATE history SET rating = ? WHERE id = ?", (rating, doubt_id))
    conn.close()
    return True

def delete_doubt(doubt_id: int, db_path: Optional[str] = None) -> bool:
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        conn.execute("DELETE FROM history WHERE id = ?", (doubt_id,))
    conn.close()
    return True

def clear_history(db_path: Optional[str] = None) -> bool:
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        conn.execute("DELETE FROM history")
    conn.close()
    return True

def save_quiz_result(
    subject: str,
    topic: str,
    score: int,
    total_questions: int,
    details: Optional[Any] = None,
    db_path: Optional[str] = None
) -> int:
    init_db(db_path)
    now_str = datetime.now().isoformat()
    pct = round((score / total_questions) * 100, 1) if total_questions > 0 else 0.0
    details_str = json.dumps(details) if details else "{}"
    conn = get_connection(db_path)
    with conn:
        cursor = conn.execute("""
            INSERT INTO quiz_results (timestamp, subject, topic, score, total_questions, percentage, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (now_str, subject, topic, score, total_questions, pct, details_str))
        inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_quiz_history(limit: int = 50, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db(db_path)
    conn = get_connection(db_path)
    rows = conn.execute("SELECT * FROM quiz_results ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results

def save_coding_attempt(
    challenge_name: str,
    subject: str,
    passed: bool,
    code: str,
    execution_time_ms: float = 0.0,
    db_path: Optional[str] = None
) -> int:
    init_db(db_path)
    now_str = datetime.now().isoformat()
    conn = get_connection(db_path)
    with conn:
        cursor = conn.execute("""
            INSERT INTO coding_attempts (timestamp, challenge_name, subject, passed, code, execution_time_ms)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (now_str, challenge_name, subject, 1 if passed else 0, code, execution_time_ms))
        inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_coding_attempts(limit: int = 50, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db(db_path)
    conn = get_connection(db_path)
    rows = conn.execute("SELECT * FROM coding_attempts ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results

def save_note(
    title: str,
    content: str,
    subject: str = "General",
    tags: str = "",
    db_path: Optional[str] = None
) -> int:
    init_db(db_path)
    now_str = datetime.now().isoformat()
    conn = get_connection(db_path)
    with conn:
        cursor = conn.execute("""
            INSERT INTO student_notes (timestamp, subject, title, content, tags)
            VALUES (?, ?, ?, ?, ?)
        """, (now_str, subject, title, content, tags))
        inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_notes(subject: Optional[str] = None, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db(db_path)
    conn = get_connection(db_path)
    if subject and subject != "All":
        rows = conn.execute("SELECT * FROM student_notes WHERE subject = ? ORDER BY id DESC", (subject,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM student_notes ORDER BY id DESC").fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results

def delete_note(note_id: int, db_path: Optional[str] = None) -> bool:
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        conn.execute("DELETE FROM student_notes WHERE id = ?", (note_id,))
    conn.close()
    return True

def get_difficult_topics(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns topics that students marked as difficult for targeted revision."""
    init_db(db_path)
    conn = get_connection(db_path)
    rows = conn.execute("""
        SELECT topic, subject, COUNT(*) as count, MAX(timestamp) as last_seen
        FROM history 
        WHERE marked_difficult = 1 AND topic != ''
        GROUP BY topic, subject 
        ORDER BY count DESC
    """).fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results

def get_student_stats(db_path: Optional[str] = None) -> Dict[str, Any]:
    init_db(db_path)
    conn = get_connection(db_path)

    total_doubts = conn.execute("SELECT COUNT(*) as cnt FROM history").fetchone()["cnt"]
    bookmarked_count = conn.execute("SELECT COUNT(*) as cnt FROM history WHERE bookmarked = 1").fetchone()["cnt"]
    difficult_count = conn.execute("SELECT COUNT(*) as cnt FROM history WHERE marked_difficult = 1").fetchone()["cnt"]

    subject_rows = conn.execute("""
        SELECT subject, COUNT(*) as count 
        FROM history 
        GROUP BY subject 
        ORDER BY count DESC
    """).fetchall()
    subject_counts = {row["subject"]: row["count"] for row in subject_rows}

    quiz_summary = conn.execute("""
        SELECT COUNT(*) as cnt, AVG(percentage) as avg_pct 
        FROM quiz_results
    """).fetchone()
    total_quizzes = quiz_summary["cnt"] or 0
    avg_quiz_score = round(quiz_summary["avg_pct"] or 0.0, 1)

    quiz_by_subject = conn.execute("""
        SELECT subject, COUNT(*) as count, AVG(percentage) as avg_pct
        FROM quiz_results
        GROUP BY subject
    """).fetchall()
    quiz_subject_stats = {
        row["subject"]: {"count": row["count"], "avg_score": round(row["avg_pct"] or 0.0, 1)}
        for row in quiz_by_subject
    }

    # Coding exercises
    coding_summary = conn.execute("""
        SELECT COUNT(*) as total, SUM(passed) as passed_cnt FROM coding_attempts
    """).fetchone()
    total_coding = coding_summary["total"] or 0
    passed_coding = coding_summary["passed_cnt"] or 0

    # Streak calculation
    dates_rows = conn.execute("""
        SELECT DISTINCT substr(timestamp, 1, 10) as day 
        FROM history 
        UNION 
        SELECT DISTINCT substr(timestamp, 1, 10) as day 
        FROM quiz_results 
        ORDER BY day DESC
    """).fetchall()
    active_days = [row["day"] for row in dates_rows if row["day"]]

    streak = 0
    today = date.today()
    if active_days:
        day_objs = set()
        for d_str in active_days:
            try:
                day_objs.add(datetime.strptime(d_str, "%Y-%m-%d").date())
            except ValueError:
                pass

        if today in day_objs:
            curr = today
            while curr in day_objs:
                streak += 1
                curr -= timedelta(days=1)
        elif (today - timedelta(days=1)) in day_objs:
            curr = today - timedelta(days=1)
            while curr in day_objs:
                streak += 1
                curr -= timedelta(days=1)

    conn.close()

    return {
        "total_doubts": total_doubts,
        "bookmarked_count": bookmarked_count,
        "difficult_count": difficult_count,
        "subject_counts": subject_counts,
        "total_quizzes": total_quizzes,
        "avg_quiz_score": avg_quiz_score,
        "quiz_subject_stats": quiz_subject_stats,
        "total_coding": total_coding,
        "passed_coding": passed_coding,
        "study_streak": streak,
        "active_days_count": len(active_days)
    }

def get_faculty_analytics(db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Aggregates analytics for the GMRIT Faculty Dashboard:
    - Common student doubts and frequently misunderstood topics
    - Difficult topic hotspots
    - Low-performing quiz subjects
    - Recommendations for classroom lectures
    """
    init_db(db_path)
    conn = get_connection(db_path)

    # 1. Most frequent topics asked
    frequent_topics_rows = conn.execute("""
        SELECT topic, subject, COUNT(*) as query_count, 
               SUM(CASE WHEN rating = -1 THEN 1 ELSE 0 END) as negative_feedback_count,
               SUM(CASE WHEN marked_difficult = 1 THEN 1 ELSE 0 END) as difficult_flag_count
        FROM history
        WHERE topic != ''
        GROUP BY topic, subject
        ORDER BY query_count DESC
        LIMIT 10
    """).fetchall()
    frequent_topics = [dict(r) for r in frequent_topics_rows]

    # 2. Most challenging topics (marked difficult or low quiz score)
    challenging_topics = conn.execute("""
        SELECT topic, subject, COUNT(*) as cnt 
        FROM history 
        WHERE marked_difficult = 1 AND topic != ''
        GROUP BY topic, subject 
        ORDER BY cnt DESC 
        LIMIT 5
    """).fetchall()

    # 3. Quiz mastery by subject
    quiz_perf = conn.execute("""
        SELECT subject, COUNT(*) as attempts, AVG(percentage) as avg_score
        FROM quiz_results
        GROUP BY subject
        ORDER BY avg_score ASC
    """).fetchall()

    # 4. Total questions and students
    total_q = conn.execute("SELECT COUNT(*) as c FROM history").fetchone()["c"]

    conn.close()

    # Generate pedagogical interventions for faculty
    interventions = []
    if challenging_topics:
        top_diff = challenging_topics[0]
        interventions.append(
            f"Review **{top_diff['topic']}** ({top_diff['subject']}) in upcoming lecture: {top_diff['cnt']} students flagged this concept as difficult."
        )

    for q in quiz_perf:
        if q["avg_score"] < 65:
            interventions.append(
                f"Address foundational misconceptions in **{q['subject']}**: Average quiz score is currently {round(q['avg_score'], 1)}%."
            )

    if not interventions:
        interventions.append("Student cohort is progressing smoothly. Continue reinforcing active problem-solving.")

    return {
        "total_queries": total_q,
        "frequent_topics": frequent_topics,
        "challenging_topics": [dict(r) for r in challenging_topics],
        "quiz_performance": [dict(r) for r in quiz_perf],
        "suggested_interventions": interventions
    }

def purge_student_data(db_path: Optional[str] = None) -> bool:
    """Privacy control: purges all student history, quiz results, notes, and coding attempts."""
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        conn.execute("DELETE FROM history")
        conn.execute("DELETE FROM quiz_results")
        conn.execute("DELETE FROM student_notes")
        conn.execute("DELETE FROM coding_attempts")
    conn.close()
    return True
