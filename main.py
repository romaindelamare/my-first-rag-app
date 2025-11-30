from fastapi import FastAPI
from pydantic import BaseModel
from rag import index_document, answer_query
from rag_evaluator import evaluate_answer


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
    answer, sources = answer_query(body.question)
    evaluation = evaluate_answer(answer, sources)

    return {
        "answer": answer,
        "sources": sources,
        "evaluation": evaluation
    }
