import ollama
from config import Config

def semantic_chunking(text, max_chunk_size=800):
    prompt = f"""
Split the following document into meaningful sections. 
Each section should contain complete ideas and stay under {max_chunk_size} characters. 
Return the result as a list of chunks separated by the delimiter <CHUNK>.

Document:
{text}
"""

    response = ollama.generate(
        model=Config.MODEL_DEFAULT,
        prompt=prompt
    )

    raw_output = response["response"]
    chunks = [c.strip() for c in raw_output.split("<CHUNK>") if c.strip()]
    return chunks

def fallback_chunking(text, size=800):
    return [text[i:i+size] for i in range(0, len(text), size)]

def chunk_text(text):
    try:
        chunks = semantic_chunking(text)
        if len(chunks) == 0:
            return fallback_chunking(text)
        return chunks
    except Exception:
        return fallback_chunking(text)
