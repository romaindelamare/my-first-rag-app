from pydantic import BaseModel
from typing import List, Dict

from app.config import Config

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    model: str = Config.MODEL_DEFAULT
    temperature: float = Config.TEMPERATURE_DEFAULT
    top_p: float = Config.TOP_P_DEFAULT
    top_k: int = Config.TOP_K_DEFAULT
