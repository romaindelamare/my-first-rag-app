class RagError(Exception):
    """Base error for RAG pipeline."""
    pass

class VectorStoreError(RagError):
    """FAISS, metadata, or vector retrieval error."""
    pass

class EmbeddingError(RagError):
    """Embedding model failed."""
    pass

class RerankError(RagError):
    """Reranker failure."""
    pass

class PromptError(RagError):
    """Prompt generation failed."""
    pass

class LLMError(RagError):
    """LLM model generation failure."""
    pass
