from pydantic import BaseModel
from app.config import Config

class ChatRequest(BaseModel):
    session_id: str
    message: str
    model: str = Config.MODEL_DEFAULT
    temperature: float = Config.TEMPERATURE_DEFAULT