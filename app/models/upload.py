from pydantic import BaseModel

class IndexRequest(BaseModel):
    doc: str