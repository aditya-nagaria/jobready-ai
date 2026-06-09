# ============================================================
# JobReady AI — llm_engine.py
# ============================================================
# LLM-agnostic wrapper. Supports:
#   - mock mode   : returns structured fake response (no API key needed)
#   - gemini mode : calls Gemini 1.5 Flash via google-generativeai
#   - openai mode : calls GPT-4o mini via openai SDK
#
# All other modules call llm_call(prompt) only.
# They never know which provider is running underneath.
# ============================================================

import json
from config import LLM_PROVIDER, LLM_MODE, GEMINI_API_KEY, OPENAI_API_KEY, GEMINI_MODEL, OPENAI_MODEL


# ── Mock response ────────────────────────────────────────────
# Realistic fake output used to test the full pipeline
# without spending API credits or needing a key.

MOCK_RESPONSE = {
    "fit_score": 72,
    "matched_skills": [
        "Product Management",
        "Agile delivery",
        "Stakeholder management",
        "CI/CD governance",
        "Cross-functional team leadership"
    ],
    "missing_skills": [
        "Hands-on LLM fine-tuning experience",
        "Python-based AI/ML development",
        "A/B testing at scale"
    ],
    "partial_matches": [
        "GenAI product experience (building JobReady AI — in progress)",
        "Data pipeline management (exposure, not ownership)"
    ],
    "ats_keywords": [
        "AI Product Manager",
        "Large Language Models",
        "Prompt engineering",
        "Product roadmap",
        "KPI definition",
        "Go-to-market strategy",
        "API integration"
    ],
    "recommendations": [
        "Add a dedicated 'GenAI Projects' section to your resume listing JobReady AI with the GitHub link",
        "Quantify your CI/CD governance impact — number of pipelines, teams, or release cycles affected",
        "Complete one hands-on LLM fine-tuning tutorial (Hugging Face has a free one) and reference it",
        "Frame your GxP compliance experience as AI governance capability — it is directly transferable",
        "Add 'Prompt engineering' and 'LLM' explicitly to your Skills section on LinkedIn and Naukri"
    ],
    "role_level_match": "Strong match — JD targets 10-15 years experience, your profile shows 13 years",
    "apply_recommendation": "Yes — strong fit. Tailor resume to surface the GenAI and governance angle."
}


# ── Core call function ───────────────────────────────────────

def llm_call(prompt: str) -> str:
    """
    Single entry point for all LLM calls across the product.
    Returns raw string response (JSON expected).
    """
    if LLM_MODE == "mock":
        return _mock_call()
    elif LLM_PROVIDER == "gemini":
        return _gemini_call(prompt)
    elif LLM_PROVIDER == "openai":
        return _openai_call(prompt)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}. Use 'gemini' or 'openai'.")


# ── Mock call ────────────────────────────────────────────────

def _mock_call() -> str:
    """Returns realistic mock JSON — no API key needed."""
    print("  [LLM] Running in MOCK mode — no API call made.")
    return json.dumps(MOCK_RESPONSE)


# ── Gemini call ──────────────────────────────────────────────

def _gemini_call(prompt: str) -> str:
    """Calls Gemini 1.5 Flash via google-generativeai SDK."""
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError(
            "google-generativeai not installed. "
            "Run: pip install google-generativeai"
        )

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)

    print(f"  [LLM] Calling Gemini ({GEMINI_MODEL})...")
    response = model.generate_content(prompt)
    return response.text


# ── OpenAI call ──────────────────────────────────────────────

def _openai_call(prompt: str) -> str:
    """Calls GPT-4o mini via openai SDK."""
    try:
        import openai
    except ImportError:
        raise ImportError(
            "openai not installed. "
            "Run: pip install openai"
        )

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    print(f"  [LLM] Calling OpenAI ({OPENAI_MODEL})...")
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content
