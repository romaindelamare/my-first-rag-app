from fastapi import APIRouter
from app.models.upload import IndexRequest
from app.rag.rag import index_document

router = APIRouter()

@router.post("/index")
def index_route(body: IndexRequest):
    index_document(body.doc)
    return {"status": "indexed"}