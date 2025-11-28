from chunking import chunk_text
from embeddings import embed_text
from vectorstore import VectorStore
from prompts.rag_answer import build_rag_prompt
import ollama

vs = VectorStore(dim=768)

def index_document(text):
    chunks = chunk_text(text)

    for chunk in chunks:
        emb = embed_text(chunk)
        vs.add(emb, chunk)

    vs.save()

def answer_query(question):
    q_emb = embed_text(question)
    relevant_chunks = vs.search(q_emb, top_k=5)
    context = "\n\n".join(relevant_chunks)

    prompt = build_rag_prompt(context=context, question=question)

    response = ollama.generate(
        model='llama3',
        prompt=prompt
    )

    return response['response']
