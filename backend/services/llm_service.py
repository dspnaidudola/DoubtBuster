import os
import json
import re
from typing import Optional, List, Dict, Any

from backend.services.offline_tutor import (
    OFFLINE_KNOWLEDGE_BASE,
    ALIAS_MAPPINGS,
    parse_prompt_context,
    generate_offline_answer,
    synthesize_dynamic_programming_answer
)

UNIVERSAL_SYSTEM_PROMPT = (
    "You are DoubtBuster, a supportive, universally knowledgeable, and academically rigorous AI tutor for students across ALL fields and domains — including Computer Science, Programming, Mathematics, Physics, Chemistry, Biology, Electrical, Mechanical, Civil Engineering, Economics, Business, History, Civics, Geography, Humanities, Languages, and General Knowledge. "
    "Always ensure your explanation directly, accurately, and thoroughly answers the student's exact question and field, without diverting to unrelated subjects or forcing computer science analogies when the question belongs to another domain. "
    "1) For coding questions: provide clean, working, fully runnable code with step-by-step logic, edge cases, and test runs. "
    "2) For mathematics and calculations: provide rigorous step-by-step derivations, LaTeX formatting ($...$ and $$...$$), intermediate calculations, and clear final mathematical results. "
    "3) For scientific, engineering, economic, historical, civic, and theoretical concepts: provide in-depth, domain-accurate explanations, core mechanisms, intuitive real-world analogies, and key academic takeaways."
)


def ask_llm(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini",
    provider: str = "auto"
) -> str:
    """
    Main entry point for LLM queries.
    Supports OpenAI, Google Gemini, Groq, and graceful fallback to built-in pedagogical engine.
    """
    clean_key = (api_key or "").strip()

    # 1. Google Gemini via google.genai
    is_gemini = "gemini" in model.lower() or provider.lower() == "gemini" or clean_key.startswith("AIza")
    if (is_gemini or provider == "gemini") and clean_key:
        try:
            from google import genai
            client = genai.Client(api_key=clean_key)
            gemini_model = model if "gemini" in model else "gemini-2.5-flash"
            try:
                response = client.models.generate_content(
                    model=gemini_model,
                    contents=prompt,
                    config={"system_instruction": UNIVERSAL_SYSTEM_PROMPT}
                )
            except Exception:
                response = client.models.generate_content(
                    model=gemini_model,
                    contents=f"[System Instructions: {UNIVERSAL_SYSTEM_PROMPT}]\n\n{prompt}"
                )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            if not clean_key.startswith("sk-") and not clean_key.startswith("gsk_"):
                raise RuntimeError(f"Gemini API error: {e}")

    # 2. Groq API via OpenAI client (recommended free tier in GMRIT Handbook)
    is_groq = "llama" in model.lower() or "mixtral" in model.lower() or clean_key.startswith("gsk_")
    if is_groq and clean_key:
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=clean_key,
                timeout=30.0,
                max_retries=2
            )
            groq_model = model if ("llama" in model or "mixtral" in model) else "llama-3.3-70b-versatile"
            response = client.chat.completions.create(
                model=groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": UNIVERSAL_SYSTEM_PROMPT,
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception as e:
            raise RuntimeError(f"Groq API error: {e}")

    # 3. OpenAI via openai client
    if clean_key and not is_gemini and not is_groq:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=clean_key, timeout=45.0, max_retries=2)
            response = client.chat.completions.create(
                model=model if "gpt" in model else "gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": UNIVERSAL_SYSTEM_PROMPT,
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")

    # 4. If no API key provided, parse prompt context properly and run built-in pedagogical tutor
    ctx = parse_prompt_context(prompt)
    return generate_offline_answer(
        question=ctx["question"],
        subject=ctx["subject"],
        topic=ctx["topic"],
        level=ctx["level"],
        mode=ctx["mode"],
        attempt=ctx["attempt"]
    )


def test_api_connection(api_key: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    """Tests if the provided key is valid and can generate a test token."""
    key = api_key.strip()
    if not key:
        return {"success": False, "message": "API key cannot be empty."}

    # Test as Gemini
    if "gemini" in model.lower() or key.startswith("AIza"):
        try:
            from google import genai
            client = genai.Client(api_key=key)
            test_m = model if "gemini" in model else "gemini-2.5-flash"
            resp = client.models.generate_content(
                model=test_m,
                contents="Say 'OK'",
            )
            return {"success": True, "provider": "Google Gemini", "message": f"Connected to {test_m} successfully!"}
        except Exception as e:
            return {"success": False, "provider": "Google Gemini", "message": str(e)}

    # Test as Groq
    if key.startswith("gsk_") or "llama" in model.lower():
        try:
            from openai import OpenAI
            client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=key, timeout=10.0)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": "Respond with 'OK'"}],
                max_tokens=5,
            )
            return {"success": True, "provider": "Groq", "message": "Connected to Groq LLaMA-3.3 successfully!"}
        except Exception as e:
            return {"success": False, "provider": "Groq", "message": str(e)}

    # Test as OpenAI
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key, timeout=10.0, max_retries=1)
        resp = client.chat.completions.create(
            model=model if "gpt" in model else "gpt-4o-mini",
            messages=[{"role": "user", "content": "Respond with 'OK'"}],
            max_tokens=5,
        )
        return {"success": True, "provider": "OpenAI", "message": f"Connected to {model} successfully!"}
    except Exception as e:
        return {"success": False, "provider": "OpenAI", "message": str(e)}
