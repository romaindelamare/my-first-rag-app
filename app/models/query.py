from pydantic import BaseModel
from app.config import Config

class QueryRequest(BaseModel):
    question: str
    model: str = Config.MODEL_DEFAULT
    temperature: float = Config.TEMPERATURE_DEFAULT
    top_p: float = Config.TOP_P_DEFAULT
    top_k: int = Config.TOP_K_DEFAULT