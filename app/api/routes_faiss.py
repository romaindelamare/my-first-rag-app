import os
from fastapi import APIRouter
from app.core.store import vs
from app.rag.vectorstore import DB_FOLDER

router = APIRouter()

@router.get("/faiss/info")
def faiss_info():
    index_path = os.path.join(DB_FOLDER, "index.faiss")
    size = os.path.getsize(index_path) if os.path.exists(index_path) else 0

    return {
        "vectors": vs.index.ntotal,
        "dimension": vs.dim,
        "documents": len(vs.meta),
        "index_file_size_bytes": size,
    }
