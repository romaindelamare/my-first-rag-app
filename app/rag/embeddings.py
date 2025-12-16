import ollama
from app.core.config import CONFIG

def embed_text(text):
    response = ollama.embeddings(
        model=CONFIG.embedding_model,
        prompt=text
    )
    return response['embedding']
