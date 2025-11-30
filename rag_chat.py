from rag import answer_query
from config import Config

def answer_chat(message, history, model=Config.MODEL_DEFAULT, temperature=0.2):

    # Build a memory prompt
    memory_prompt = f"""
The following is a conversation between a user and an AI assistant.
Use the memory to help answer the user's new message.
Do NOT repeat the memory in the answer.

MEMORY:
{history}

NEW MESSAGE:
{message}
"""

    # Use RAG normally (rewriting → retrieval → reranking → answer)
    answer, sources = answer_query(
        memory_prompt,
        model=model,
        temperature=temperature
    )

    return answer, sources
