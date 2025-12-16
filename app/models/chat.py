from pydantic import BaseModel
from typing import List, Dict

from app.core.config import CONFIG

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    model: str = CONFIG.llm_model
    temperature: float = CONFIG.temperature
    top_p: float = CONFIG.top_p
    top_k: int = CONFIG.top_k
