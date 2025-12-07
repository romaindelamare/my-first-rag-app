import ollama
from app.config import Config

def score_chunk(question: str, chunk: str) -> int:
    prompt = f"""
You are a relevance evaluator.

Question:
{question}

Chunk:
{chunk}

Task:
Rate how relevant this chunk is to answering the question.
Give a score from 0 (not relevant) to 100 (highly relevant).
Only return the number.
"""

    response = ollama.generate(
        model=Config.MODEL_DEFAULT,
        prompt=prompt
    )

    try:
        score = int("".join(filter(str.isdigit, response["response"])))
        return min(max(score, 0), 100)
    except:
        return 0

def rerank_chunks(question: str, chunks: list):
    if not chunks:
        return []

    scored = []
    for chunk in chunks:
        s = score_chunk(question, chunk)
        scored.append({
            "score": s,
            **chunk
        })

    return sorted(scored, key=lambda x: x["score"], reverse=True)
