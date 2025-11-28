from fastapi import FastAPI
from rag import index_document, answer_query
from pydantic import BaseModel

app = FastAPI()

class IndexRequest(BaseModel):
    doc: str

@app.post("/index")
def index_route(body: IndexRequest):
    index_document(body.doc)
    return {"status": "indexed"}

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query_route(body: QueryRequest):
    answer = answer_query(body.question)
    return {"answer": answer}
