import ollama
from app.core.config import CONFIG

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
        model=CONFIG.llm_model,
        prompt=prompt
    )

    return response["response"].strip()
