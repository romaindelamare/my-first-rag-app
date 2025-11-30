import ollama
from app.config import Config

def rewrite_query(question: str) -> str:
    prompt = f"""
Rewrite the following question so it becomes a better search query for a document-based retrieval system.

Guidelines:
- Add missing context.
- Expand abbreviations.
- Clarify vague terms.
- Keep the meaning the same.
- Do NOT answer the question.
- Return only the rewritten question.

Original question:
{question}
"""

    response = ollama.generate(
        model=Config.MODEL_DEFAULT,
        prompt=prompt
    )

    return response["response"].strip()
