import ollama
from chunking import chunk_text
from embeddings import embed_text
from vectorstore import VectorStore
from prompts.rag_answer import build_rag_prompt
from reranker import rerank
from rewriter import rewrite_query
from config import Config

vs = VectorStore(dim=768)

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
    # 0. Rewrite the user question
    rewritten = rewrite_query(question)

    # 1. Embed the rewritten question
    q_emb = embed_text(rewritten)

    # 2. Hybrid FAISS keyword/vector retrieval applied BEFORE reranking
    raw_chunks = vs.search(q_emb, retrieval_k=10, query_text=rewritten)

    # 3. LLM-based reranking for best relevance
    top_chunks = rerank(rewritten, raw_chunks, retrieval_k=5)

    # 4. Build RAG prompt using only top chunks
    context = "\n\n".join(top_chunks)
    prompt = build_rag_prompt(context, question)

    # 5. Generate the final answer with Ollama
    response = ollama.generate(
        model=model,
        prompt=prompt,
        options={
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }
    )

    answer = response["response"]

    # 6. Return both answer and sources (citations)
    return answer, top_chunks
