import os
import pytest
from backend.services.db_service import (
    init_db, save_doubt, get_history, get_doubt, toggle_bookmark, toggle_difficult,
    rate_doubt, delete_doubt, save_quiz_result, get_quiz_history,
    save_note, get_notes, delete_note, get_student_stats,
    save_coding_attempt, get_coding_attempts, get_faculty_analytics, purge_student_data,
    get_difficult_topics
)

TEST_DB = "test_doubtbuster.db"

@pytest.fixture(autouse=True)
def setup_teardown():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_db(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_save_and_get_doubt():
    d_id = save_doubt(
        question="What is recursion?",
        answer="Function calling itself.",
        subject="Programming",
        topic="Recursion",
        level="Beginner",
        mode="Step-by-step explanation",
        db_path=TEST_DB
    )
    assert d_id > 0
    doubt = get_doubt(d_id, db_path=TEST_DB)
    assert doubt is not None
    assert doubt["question"] == "What is recursion?"
    assert doubt["subject"] == "Programming"

def test_bookmark_and_rate_and_difficult():
    d_id = save_doubt(
        question="Matrix invertibility",
        answer="Determinant != 0",
        subject="Mathematics",
        topic="Eigenvalues",
        db_path=TEST_DB
    )
    # Toggle bookmark
    is_bookmarked = toggle_bookmark(d_id, db_path=TEST_DB)
    assert is_bookmarked is True

    # Toggle difficult
    is_diff = toggle_difficult(d_id, db_path=TEST_DB)
    assert is_diff is True
    
    # Rate thumbs up (+1)
    rate_doubt(d_id, 1, db_path=TEST_DB)
    doubt = get_doubt(d_id, db_path=TEST_DB)
    assert doubt["rating"] == 1
    assert doubt["bookmarked"] == 1
    assert doubt["marked_difficult"] == 1

    diff_topics = get_difficult_topics(db_path=TEST_DB)
    assert len(diff_topics) == 1
    assert diff_topics[0]["topic"] == "Eigenvalues"

def test_quiz_and_stats():
    q_id = save_quiz_result(
        subject="Programming",
        topic="Python loops",
        score=3,
        total_questions=4,
        db_path=TEST_DB
    )
    assert q_id > 0
    history = get_quiz_history(db_path=TEST_DB)
    assert len(history) == 1
    assert history[0]["percentage"] == 75.0

    stats = get_student_stats(db_path=TEST_DB)
    assert stats["total_quizzes"] == 1
    assert stats["avg_quiz_score"] == 75.0

def test_coding_attempt_persistence():
    ca_id = save_coding_attempt(
        challenge_name="Reverse a String Recursively",
        subject="Programming",
        passed=True,
        code="def reverse_str(s): return s[::-1]",
        execution_time_ms=12.5,
        db_path=TEST_DB
    )
    assert ca_id > 0
    attempts = get_coding_attempts(db_path=TEST_DB)
    assert len(attempts) == 1
    assert attempts[0]["challenge_name"] == "Reverse a String Recursively"
    assert attempts[0]["passed"] == 1

def test_faculty_analytics_and_purge():
    save_doubt(
        question="How does backprop work?",
        answer="Chain rule explanation",
        subject="Deep Learning",
        topic="Backpropagation",
        marked_difficult=True,
        db_path=TEST_DB
    )
    analytics = get_faculty_analytics(db_path=TEST_DB)
    assert analytics["total_queries"] >= 1
    assert len(analytics["challenging_topics"]) >= 1

    # Privacy purge
    purge_student_data(db_path=TEST_DB)
    assert len(get_history(db_path=TEST_DB)) == 0
