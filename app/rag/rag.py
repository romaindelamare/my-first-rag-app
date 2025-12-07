import ollama
import codecs
import logging
from app.core.store import vs
from app.config import Config
from app.rag.rag_answer import build_rag_prompt
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_text
from app.rag.reranker import rerank_chunks
from app.rag.rewriter import rewrite_query
from app.core.errors import EmbeddingError, LLMError, PromptError, RagError, RerankError, VectorStoreError
from app.core.timer import Timer
from app.core.logger import log_stage
from app.core.metrics import metrics

logger = logging.getLogger("rag")

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
    try:
        return _answer_query_internal(question, model, temperature, top_p, top_k)
    except RagError as e:
        logger.error("🔥 [RAG ERROR] %s", str(e))
        raise
    except Exception as e:
        logger.error("🔥 [UNKNOWN ERROR] %s", str(e))
        raise RagError("Unknown internal error") from e
    
def _answer_query_internal(
        question,
        model=Config.MODEL_DEFAULT,
        temperature=Config.TEMPERATURE_DEFAULT,
        top_p=Config.TOP_P_DEFAULT,
        top_k=Config.TOP_K_DEFAULT):

    logger.info("🔎 [QUERY] User question: %s", question)

    # 1. Rewrite the question
    try:
        with Timer() as t:
            rewritten = rewrite_query(question)
        log_stage("REWRITE", True, t.ms)
        metrics.record("rewrite_ms", t.ms)
    except Exception as e:
        log_stage("REWRITE", False, t.ms if 't' in locals() else 0, str(e))
        raise PromptError(f"Rewrite failed: {e}")

    # 2. Embed and retrieve chunks
    try:
        with Timer() as t:
            q_emb = embed_text(rewritten)
        log_stage("EMBED", True, t.ms)
        metrics.record("embed_ms", t.ms)
    except Exception as e:
        log_stage("EMBED", False, t.ms if 't' in locals() else 0, str(e))
        raise EmbeddingError(f"Embedding failed: {e}")

    # 3️. Vector search
    try:
        with Timer() as t:
            raw_chunks = vs.search(
                q_emb,
                retrieval_k=10,
                query_text=rewritten
            )
        log_stage("SEARCH", True, t.ms)
        metrics.record("search_ms", t.ms)
    except Exception as e:
        log_stage("SEARCH", False, t.ms if 't' in locals() else 0, str(e))
        raise VectorStoreError(f"Vector search failed: {e}")

    # Preview chunks
    for i, c in enumerate(raw_chunks[:3]):
        logger.info("    • Chunk %d preview: %.50s", i, c["text"])

    # 4. Rerank
    try:
        with Timer() as t:
            reranked = rerank_chunks(rewritten, raw_chunks)
        log_stage("RERANK", True, t.ms)
        metrics.record("rerank_ms", t.ms)
    except Exception as e:
        log_stage("RERANK", False, t.ms if 't' in locals() else 0, str(e))
        raise RerankError(f"Reranking failed: {e}")

    if reranked:
        logger.info("📊 [RERANK TOP] %s", [c["score"] for c in reranked[:5]])

    top_chunks = reranked[:top_k]

    # 5. Build context
    context = "\n\n".join([c["text"] for c in top_chunks])

    # 6. Build RAG prompt
    try:
        with Timer() as t:
            prompt = build_rag_prompt(context, question)
        log_stage("PROMPT", True, t.ms)
        metrics.record("prompt_ms", t.ms)
    except Exception as e:
        log_stage("PROMPT", False, t.ms if 't' in locals() else 0, str(e))
        raise PromptError(f"Prompt creation failed: {e}")

    # 7. LLM CALL
    try:
        with Timer() as t:
            result = ollama.generate(
                model=model,
                prompt=prompt,
                options={
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k
                }
            )
        log_stage("LLM_GENERATION", True, t.ms)
        metrics.record("llm_ms", t.ms)
        answer = result["response"]
        logger.info("✨ [ANSWER] %s", answer[:200] + "...")
    except Exception as e:
        log_stage("LLM_GENERATION", False, t.ms if 't' in locals() else 0, str(e))
        raise LLMError(f"LLM generation failed: {e}")

    # 8. Decode
    if isinstance(answer, str):
        answer = codecs.decode(answer, "unicode_escape")

    # 9. Build sources
    sources = [{"doc_id": c["doc_id"], "text": c["text"]} for c in top_chunks]

    logger.info("🎉 [RAG] Query completed successfully")
    metrics.increment_queries()

    return answer, sources
