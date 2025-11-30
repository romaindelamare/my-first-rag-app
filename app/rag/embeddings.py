import ollama

def embed_text(text):
    response = ollama.embeddings(
        model='nomic-embed-text',
        prompt=text
    )
    return response['embedding']
