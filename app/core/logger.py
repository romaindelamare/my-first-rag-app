import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# -------------------------------------
# 1. GLOBAL LOGGER INSTANCE
# -------------------------------------
logger = logging.getLogger("rag")
logger.setLevel(LOG_LEVEL)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# -------------------------------------
# 2. Helper for structured stage logging
# -------------------------------------
def log_stage(stage: str, success: bool, duration_ms: float, error: str = None):
    """Standardized log output for each RAG pipeline stage."""
    if success:
        logger.info(f"✅ [{stage}] OK ({duration_ms:.2f} ms)")
    else:
        logger.error(f"❌ [{stage}] FAILED ({duration_ms:.2f} ms) — {error}")
