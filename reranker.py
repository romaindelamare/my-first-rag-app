import ollama
from config import Config

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

def rerank(question: str, chunks: list, retrieval_k: int = 5):
    scored = []
    for chunk in chunks:
        s = score_chunk(question, chunk)
        scored.append((s, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [chunk for score, chunk in scored[:retrieval_k]]
