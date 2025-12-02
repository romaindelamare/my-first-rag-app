from fastapi import APIRouter
from app.core.store import vs

router = APIRouter()

@router.get("/faiss/info")
def faiss_info():
    return {
        "dimension": vs.index.d,
        "total_vectors": vs.index.ntotal,
        "is_trained": vs.index.is_trained,
    }
