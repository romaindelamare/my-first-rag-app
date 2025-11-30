import ollama
from config import Config

def evaluate_answer(answer: str, sources: list) -> dict:
    src_text = "\n\n".join(sources)

    prompt = f"""
You are an evaluator for a Retrieval-Augmented Generation (RAG) system.

Given:
- The system's ANSWER
- The set of SOURCE CHUNKS it used

Your tasks:
1. Determine if the answer is fully supported by the source chunks.
2. If unsupported, identify hallucinated or extra information.
3. Return the result as JSON with:
   - "supported": true/false
   - "explanation": a short explanation

ANSWER:
{answer}

SOURCES:
{src_text}

Respond ONLY with JSON.
"""

    response = ollama.generate(
        model=Config.MODEL_DEFAULT,
        prompt=prompt,
    )

    return response["response"]
