# ============================================================
# JobReady AI — parser.py
# ============================================================
# Handles raw LLM response string.
# Three jobs — exactly as designed in the TDD:
#
#   Job 1 — Extract  : parse raw string into Python dict
#   Job 2 — Validate : check all expected keys are present
#   Job 3 — Fallback : return safe error dict if parsing fails
#
# Rahul never sees a Python traceback. Ever.
# ============================================================

import json
import re

# All keys the LLM must return for a valid JD Analyser response
REQUIRED_KEYS = [
    "fit_score",
    "matched_skills",
    "missing_skills",
    "partial_matches",
    "ats_keywords",
    "recommendations",
    "role_level_match",
    "apply_recommendation",
]


# ── Job 1: Extract ───────────────────────────────────────────

def extract_json(raw_response: str) -> dict:
    """
    Parses raw LLM string into a Python dict.
    Strips markdown fences if the LLM included them despite instructions.
    """
    # Strip markdown code fences if present (```json ... ```)
    cleaned = re.sub(r"```(?:json)?", "", raw_response).strip()
    cleaned = cleaned.strip("`").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parsing failed: {e}\n\nRaw response received:\n{raw_response[:500]}")


# ── Job 2: Validate ──────────────────────────────────────────

def validate_response(parsed: dict) -> dict:
    """
    Checks all required keys are present and fit_score is valid integer.
    Adds defaults for any missing optional fields rather than failing hard.
    """
    missing_keys = [k for k in REQUIRED_KEYS if k not in parsed]
    if missing_keys:
        raise ValueError(f"LLM response missing required keys: {missing_keys}")

    # Validate fit_score type and range
    score = parsed.get("fit_score")
    if not isinstance(score, (int, float)):
        raise ValueError(f"fit_score must be a number. Got: {type(score)} — {score}")
    parsed["fit_score"] = max(0, min(100, int(score)))  # clamp to 0-100

    # Ensure all list fields are actually lists
    list_fields = ["matched_skills", "missing_skills", "partial_matches", "ats_keywords", "recommendations"]
    for field in list_fields:
        if not isinstance(parsed[field], list):
            parsed[field] = [str(parsed[field])]  # coerce to list rather than fail

    return parsed


# ── Job 3: Fallback ──────────────────────────────────────────

def build_fallback(error_message: str) -> dict:
    """
    Returns a safe, user-friendly error response.
    Called when extraction or validation fails.
    Rahul sees a clear message — not a traceback.
    """
    return {
        "fit_score": None,
        "matched_skills": [],
        "missing_skills": [],
        "partial_matches": [],
        "ats_keywords": [],
        "recommendations": [
            "Analysis could not be completed. Please try again.",
            "If this keeps happening, try shortening the job description.",
        ],
        "role_level_match": "Unable to determine",
        "apply_recommendation": "Please retry the analysis.",
        "error": True,
        "error_message": error_message,
        "retry": True,
    }


# ── Main parse function ──────────────────────────────────────

def parse_response(raw_response: str) -> dict:
    """
    Full parse pipeline: Extract → Validate → Fallback if either fails.
    Called by jd_analyser.py after llm_engine returns a response.
    Returns a clean, validated dict ready for display and PDF generation.
    """
    try:
        parsed  = extract_json(raw_response)
        cleaned = validate_response(parsed)
        print("  [Parser] Response parsed and validated successfully.")
        return cleaned

    except ValueError as e:
        print(f"  [Parser] Parsing failed — returning fallback.\n  Reason: {e}")
        return build_fallback(str(e))

    except Exception as e:
        print(f"  [Parser] Unexpected error — returning fallback.\n  Reason: {e}")
        return build_fallback(f"Unexpected error: {str(e)}")
