import os
from pydantic import BaseModel, Field, field_validator

class RagConfig(BaseModel):
    # ---------------------------
    # Models
    # ---------------------------
    llm_model: str = Field(default="llama3.2:3b")
    embedding_model: str = Field(default="nomic-embed-text")

    # ---------------------------
    # Retrieval
    # ---------------------------
    top_k: int = Field(default=5, ge=1, le=20)
    rerank_enabled: bool = Field(default=True)

    # ---------------------------
    # Chunking
    # ---------------------------
    max_chunk_chars: int = Field(default=800, ge=200)
    overlap_chars: int = Field(default=120, ge=0)

    # ---------------------------
    # Generation
    # ---------------------------
    temperature: float = Field(default=0.2, ge=0.0, le=1.5)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)

    @field_validator("overlap_chars")
    @classmethod
    def overlap_less_than_chunk(cls, v, info):
        max_chars = info.data.get("max_chunk_chars")
        if max_chars and v >= max_chars:
            raise ValueError("overlap_chars must be < max_chunk_chars")
        return v

def load_config() -> RagConfig:
    return RagConfig(
        llm_model=os.getenv("RAG_LLM_MODEL", "llama3.2:3b"),
        embedding_model=os.getenv("RAG_EMBED_MODEL", "nomic-embed-text"),
        top_k=int(os.getenv("RAG_TOP_K", 5)),
        rerank_enabled=os.getenv("RAG_RERANK", "true").lower() == "true",
        temperature=float(os.getenv("RAG_TEMPERATURE", 0.2)),
        top_p=float(os.getenv("RAG_TOP_P", 0.9)),
    )

CONFIG = load_config()
