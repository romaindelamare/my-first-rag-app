import ollama
import codecs
from app.core.store import vs
from app.config import Config
from app.rag.rag_answer import build_rag_prompt
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_text
from app.rag.reranker import rerank_chunks
from app.rag.rewriter import rewrite_query

def index_document(text):
    chunks = chunk_text(text)

    for chunk in chunks:
        emb = embed_text(chunk)
        vs.add(emb, chunk)

    vs.save()

def answer_query(
        question,
        model=Config.MODEL_DEFAULT,
        temperature=Config.TEMPERATURE_DEFAULT,
        top_p=Config.TOP_P_DEFAULT,
        top_k=Config.TOP_K_DEFAULT):
    # 1. Rewrite the question
    rewritten = rewrite_query(question)

    # 2. Embed and retrieve chunks
    q_emb = embed_text(rewritten)
    retrieved = vs.search(
        q_emb,
        retrieval_k=10,
        query_text=rewritten
    )

    # 3. Rerank
    top_chunks = rerank_chunks(rewritten, retrieved)

    # 4. Extract only text for the prompt
    context = "\n\n".join([entry["text"] for entry in top_chunks])

    # 5. Build final RAG prompt
    prompt = build_rag_prompt(context, question)

    # 6. Ask the LLM
    result = ollama.generate(
        model=model,
        prompt=prompt,
        options={
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }
    )
    answer = result["response"]

    # 7. Decode all escape sequences properly
    if isinstance(answer, str):
        answer = codecs.decode(answer, 'unicode_escape')

    # 8. Return answer with full metadata for UI
    sources = [
        {"doc_id": entry["doc_id"], "text": entry["text"]}
        for entry in top_chunks
    ]

    return answer, sources