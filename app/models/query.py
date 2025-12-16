from pydantic import BaseModel
from app.core.config import CONFIG

class QueryRequest(BaseModel):
    question: str
    model: str = CONFIG.llm_model
    temperature: float = CONFIG.temperature
    top_p: float = CONFIG.top_p
    top_k: int = CONFIG.top_k