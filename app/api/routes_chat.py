from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest
from app.rag.rag_chat import answer_chat
from app.core.logger import logger
from app.core.errors import RagError

router = APIRouter()

@router.post("/chat")
def chat_route(body: ChatRequest):
    try:
        return answer_chat(
            session_id=body.session_id,
            user_message=body.messages[-1].content,
            model=body.model,
            temperature=body.temperature,
            top_p=body.top_p,
            top_k=body.top_k,
        )
    
    except RagError as e:
        logger.error(f"❌ RAG PIPELINE ERROR: {e}")
        raise

    except Exception as e:
        logger.error(f"❌ UNEXPECTED ERROR: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error. Check logs."
        )
