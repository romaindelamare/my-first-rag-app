from app.core.memory import memory
from app.rag.rag import answer_query
from app.rag.summarizer import summarize_messages

def answer_chat(session_id: str, user_message: str, model: str, temperature: float,
                top_p: float, top_k: int):
    """
    Full RAG-powered chat pipeline.
    """

    # 1. Add user message to memory
    memory.add_message(session_id, "user", user_message)

    # 2. Summarize long history
    history = memory.get_messages(session_id)
    history = summarize_messages(history)

    # 3. Build chat context from memory
    chat_context = "\n".join(f"{m['role']}: {m['content']}" for m in history)

    # 4. Run RAG to answer user's message
    answer, sources = answer_query(
        question=user_message,
        model=model,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k
    )

    # 5. Add assistant response to memory
    memory.add_message(session_id, "assistant", answer)

    return answer, sources, chat_context
