from fastapi import APIRouter
import ollama
from app.core.metrics import metrics
from app.core.store import vs

router = APIRouter()

@router.get("/debug/metrics")
def get_metrics():
    return metrics.summary()

@router.get("/debug/health")
def health_check():
    # Vector store status
    vector_store_ok = vs.index is not None and vs.meta is not None

    # Check Ollama availability
    try:
        models = ollama.list()
        ollama_ok = len(models.get("models", [])) > 0
    except Exception:
        ollama_ok = False

    return {
        "api_status": "ok",
        "vector_store_ok": vector_store_ok,
        "ollama_ok": ollama_ok,
        "loaded_models": models.get("models", []) if ollama_ok else [],
        "query_count": metrics.data["query_count"],
        "uptime_seconds": metrics.uptime_seconds(),
    }

@router.get("/debug/ping")
def ping():
    return {"status": "ok", "message": "pong"}