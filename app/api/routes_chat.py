
from fastapi import APIRouter
from app.models.chat import ChatRequest
from app.rag.rag_chat import answer_chat

router = APIRouter()
sessions = {}

@router.post("/chat")
def chat(body: ChatRequest):

    # 1. Create session if not exists
    if body.session_id not in sessions:
        sessions[body.session_id] = []

    # 2. Append user message
    sessions[body.session_id].append(f"user: {body.message}")

    # 3. Build memory context
    history_text = "\n".join(sessions[body.session_id])

    # 4. Use RAG + memory
    answer, sources = answer_chat(
        body.message,
        history_text,
        model=body.model,
        temperature=body.temperature
    )

    # 5. Save assistant response
    sessions[body.session_id].append(f"assistant: {answer}")

    return {
        "answer": answer,
        "sources": sources,
        "session_messages": sessions[body.session_id]
    }