from fastapi import APIRouter
from app.models.chat import ChatRequest
from app.rag.rag_chat import answer_chat

router = APIRouter()

@router.post("/chat")
def chat_route(body: ChatRequest):
    answer, sources, memory_context = answer_chat(
        session_id=body.session_id,
        user_message=body.messages[-1].content,
        model=body.model,
        temperature=body.temperature,
        top_p=body.top_p,
        top_k=body.top_k
    )

    return {
        "answer": answer,
        "sources": sources,
        "memory_context": memory_context
    }
