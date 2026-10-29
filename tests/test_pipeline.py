from unittest.mock import patch
from backend.core.pipeline import answer_doubt

@patch("backend.core.pipeline.ask_llm", return_value="A helpful explanation.")
def test_answer_doubt_builds_response(mock_llm):
    result = answer_doubt(
        question="What is a loop?", subject="Programming", topic="Loops",
        level="Beginner", mode="Step-by-step explanation", language="English",
        attempt="", api_key="test-key", model="test-model"
    )
    assert result == "A helpful explanation."
    assert mock_llm.called

def test_generate_interactive_quiz_topic_filtering():
    from backend.core.pipeline import generate_interactive_quiz
    quiz_loops = generate_interactive_quiz("Programming", topic="loops", level="Beginner", num_questions=3)
    assert len(quiz_loops) == 3
    assert any("range" in q["question"].lower() or "loop" in q["question"].lower() for q in quiz_loops)

    quiz_funcs = generate_interactive_quiz("Programming", topic="functions", level="Beginner", num_questions=3)
    assert len(quiz_funcs) == 3
    assert any("args" in q["question"].lower() or "function" in q["question"].lower() for q in quiz_funcs)

def test_answer_doubt_8051_offline():
    result = answer_doubt(
        question="explain about 8051",
        subject="Programming",
        topic="",
        level="Beginner",
        mode="Step-by-step explanation",
        language="English",
        attempt="",
        api_key="",
        model="gpt-4o-mini",
        persist=False
    )
    assert "8051" in result
    assert "Harvard Architecture" in result or "harvard" in result.lower()
    assert "def solve_problem" not in result

def test_answer_doubt_biology_photosynthesis():
    result = answer_doubt(
        question="What is photosynthesis and how does it produce glucose?",
        subject="General / Any Domain (All Subjects)",
        topic="",
        level="Beginner",
        mode="Step-by-step explanation",
        language="English",
        attempt="",
        api_key="",
        model="gpt-4o-mini",
        persist=False
    )
    assert "Photosynthesis" in result
    assert ("Chlorophyll" in result or "Calvin" in result or "glucose" in result.lower())
    assert "def solve_problem" not in result
    assert "pipeline stages" not in result

def test_answer_doubt_civics_not_prime_code():
    result = answer_doubt(
        question="Who was the prime minister of India in 1947?",
        subject="Other",
        topic="",
        level="Beginner",
        mode="Step-by-step explanation",
        language="English",
        attempt="",
        api_key="",
        model="gpt-4o-mini",
        persist=False
    )
    # Must NOT return prime number code or is_prime
    assert "is_prime" not in result
    assert "def is_prime" not in result
    assert "Prime Minister" in result

def test_answer_doubt_physics_newton():
    result = answer_doubt(
        question="Explain Newton's second law of motion with formula",
        subject="Physics & Physical Sciences",
        topic="",
        level="Beginner",
        mode="Step-by-step explanation",
        language="English",
        attempt="",
        api_key="",
        model="gpt-4o-mini",
        persist=False
    )
    assert "Newton" in result
    assert ("momentum" in result.lower() or "acceleration" in result.lower() or "f_{net}" in result.lower() or "f = ma" in result.lower())
    assert "def solve_problem" not in result

def test_answer_doubt_economics_supply_demand():
    result = answer_doubt(
        question="Explain the law of supply and demand",
        subject="Economics, Business & Commerce",
        topic="",
        level="Beginner",
        mode="Step-by-step explanation",
        language="English",
        attempt="",
        api_key="",
        model="gpt-4o-mini",
        persist=False
    )
    assert "Supply and Demand" in result or "Supply" in result
    assert ("equilibrium" in result.lower() or "demand" in result.lower())
    assert "def solve_problem" not in result

def test_answer_doubt_math_equation_solving():
    result = answer_doubt(
        question="Solve 3x + 12 = 33",
        subject="Mathematics & Statistics",
        topic="",
        level="Beginner",
        mode="Step-by-step explanation",
        language="English",
        attempt="",
        api_key="",
        model="gpt-4o-mini",
        persist=False
    )
    assert "x = 7" in result or "7" in result
    assert "Analytical" in result or "Derivation" in result

def test_answer_doubt_coding_anagram():
    result = answer_doubt(
        question="write a python function to check if two strings are anagrams",
        subject="Computer Science & Programming",
        topic="",
        level="Beginner",
        mode="Step-by-step explanation",
        language="English",
        attempt="",
        api_key="",
        model="gpt-4o-mini",
        persist=False
    )
    assert "def are_anagrams" in result
    assert "Anagram" in result


def test_answer_doubt_8086_microprocessor_no_mechanical_bleed():
    result = answer_doubt(
        question="explain about 8086 microprocessor",
        subject="Mechanical Engineering",
        topic="",
        level="Beginner",
        mode="Step-by-step explanation",
        language="English",
        attempt="",
        api_key="",
        model="gpt-4o-mini",
        persist=False
    )
    assert "8086" in result
    assert "BIU" in result or "Bus Interface Unit" in result
    assert "Execution Unit" in result or "EU" in result
    assert "load factors" not in result.lower()
    assert "structural integrity" not in result.lower()

def test_answer_doubt_machine_learning_no_mechanical_bleed():
    result = answer_doubt(
        question="explain about machine learning",
        subject="Mechanical Engineering",
        topic="",
        level="Beginner",
        mode="Step-by-step explanation",
        language="English",
        attempt="",
        api_key="",
        model="gpt-4o-mini",
        persist=False
    )
    assert "Machine Learning" in result
    assert "Supervised" in result
    assert "Gradient Descent" in result or "Optimization" in result or "Pipeline" in result
    assert "load factors" not in result.lower()
    assert "structural integrity" not in result.lower()
