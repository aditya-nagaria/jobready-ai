# ============================================================
# JobReady AI — config.py
# ============================================================
# The single file you edit to change behaviour.
# LLM_PROVIDER : "gemini" | "openai"
# LLM_MODE     : "mock"   | "real"
#
# mock → runs without any API key (for testing logic)
# real → calls the actual LLM (paste your API key below)
# ============================================================

# ── Mode switch ──────────────────────────────────────────────
LLM_PROVIDER = "gemini"   # "gemini" or "openai"
LLM_MODE     = "mock"     # "mock"   or "real"

# ── API Keys (only needed in real mode) ─────────────────────
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"

# ── Model names ──────────────────────────────────────────────
GEMINI_MODEL = "gemini-1.5-flash"
OPENAI_MODEL = "gpt-4o-mini"

# ── Output settings ──────────────────────────────────────────
OUTPUT_DIR        = "output"       # folder where PDF reports are saved
REPORT_FILENAME   = "jd_analysis_report.pdf"
# ── Prompt settings ──────────────────────────────────────────
MAX_JD_WORDS      = 3000           # truncate JDs longer than this
MIN_FIT_SCORE_FOR_APPLY = 60       # below this, product warns Rahul to reconsider
