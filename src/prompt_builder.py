# ============================================================
# JobReady AI — prompt_builder.py
# ============================================================
# Assembles the final prompt sent to the LLM.
# Three layers — exactly as designed in the TDD:
#
#   Layer 1 — System prompt   : role, tone, output contract
#   Layer 2 — User context    : profile + JD text
#   Layer 3 — Task instruction: what the LLM must return
#
# Output: a single string passed to llm_engine.llm_call()
# ============================================================

from config import MAX_JD_WORDS


# ── Layer 1: System prompt ───────────────────────────────────

SYSTEM_PROMPT = """You are a career advisor for a mid-career professional who has been laid off.
Your role is to analyse the fit between their profile and a job description — honestly, specifically, and usefully.

Rules you must follow:
- Be specific. Never give generic advice.
- Be honest. If the fit is weak, say so and explain why.
- Be warm but direct. This person is under real pressure.
- Return ONLY valid JSON. No preamble. No explanation outside the JSON.
- Do not add markdown code fences (no ```json). Raw JSON only."""


# ── Layer 2: User context ────────────────────────────────────

def build_user_context(profile: dict, jd_text: str) -> str:
    """
    Injects the user's profile and the job description into the prompt.
    Truncates JD if it exceeds MAX_JD_WORDS to avoid token overflow.
    """
    jd_words = jd_text.split()
    if len(jd_words) > MAX_JD_WORDS:
        jd_text = " ".join(jd_words[:MAX_JD_WORDS])
        jd_text += "\n[JD truncated to first 3000 words]"

    context = f"""
USER PROFILE:
- Name: {profile.get('name', 'Not provided')}
- Years of experience: {profile.get('years_exp', 'Not provided')}
- Last role: {profile.get('last_role', 'Not provided')}
- Target role: {profile.get('target_role', 'Not provided')}
- Key skills: {', '.join(profile.get('skills', []))}
- Industry background: {profile.get('industry', 'Not provided')}
- Notable achievements: {profile.get('achievements', 'Not provided')}

JOB DESCRIPTION:
{jd_text}
"""
    return context.strip()


# ── Layer 3: Task instruction ────────────────────────────────

TASK_INSTRUCTION = """
Analyse the fit between the user profile and the job description above.

Return a JSON object with EXACTLY these keys:
{
  "fit_score": <integer 0-100>,
  "matched_skills": <list of strings — skills in profile that match JD>,
  "missing_skills": <list of strings — skills JD requires but profile lacks>,
  "partial_matches": <list of strings — skills partially covered>,
  "ats_keywords": <list of strings — high-frequency JD keywords not in profile>,
  "recommendations": <list of 3-5 specific, actionable strings>,
  "role_level_match": <string — does experience level match JD requirements?>,
  "apply_recommendation": <string — should they apply? Yes/No/Conditional + one sentence reason>
}

Scoring guide for fit_score:
- 80-100: Strong fit. Apply immediately and tailor resume.
- 60-79 : Good fit with gaps. Apply and close specific gaps.
- 40-59 : Partial fit. Apply only if you can address gaps quickly.
- 0-39  : Weak fit. Address core gaps before applying.
"""


# ── Main builder function ────────────────────────────────────

def build_prompt(profile: dict, jd_text: str) -> str:
    """
    Assembles all three layers into the final prompt string.
    Called by jd_analyser.py before passing to llm_engine.
    """
    user_context = build_user_context(profile, jd_text)

    prompt = f"{SYSTEM_PROMPT}\n\n{user_context}\n\n{TASK_INSTRUCTION}"
    return prompt
