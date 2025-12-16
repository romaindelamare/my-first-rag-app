from app.core.memory import memory
from app.rag.rag import answer_query
from app.rag.summarizer import summarize_messages

def answer_chat(
    session_id: str,
    user_message: str,
    model: str,
    temperature: float,
    top_p: float,
    top_k: int,
):
    """
    Full RAG-powered chat pipeline with memory.
    """

    # 1. Store user message
    memory.add_message(session_id, "user", user_message)

    # 2. Summarize history
    history = summarize_messages(
        memory.get_messages(session_id)
    )

    # 3. Build chat context (for UI / debugging)
    chat_context = "\n".join(
        f"{m['role']}: {m['content']}" for m in history
    )

    # 4. Run unified RAG pipeline
    result = answer_query(
        question=user_message,
        model=model,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
    )

    # 5. Store assistant answer
    memory.add_message(
        session_id,
        "assistant",
        result["answer"],
    )

    return {
        **result,
        "memory_context": chat_context,
    }
