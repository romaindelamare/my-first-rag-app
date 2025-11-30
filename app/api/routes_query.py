from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import ollama
from app.config import Config
from app.models.query import QueryRequest
from app.rag.rag import answer_query
from app.rag.rag_evaluator import evaluate_answer

router = APIRouter()

@router.post("/query")
def query_route(body: QueryRequest):
    answer, sources = answer_query(body.question, model=body.model)
    evaluation = evaluate_answer(answer, sources)

    return {
        "answer": answer,
        "sources": sources,
        "evaluation": evaluation
    }

@router.post("/stream")
def stream_answer(body: QueryRequest):

    async def event_stream():
        # get the final answer + top chunks
        answer, sources = answer_query(body.question)

        # stream the answer token-by-token
        stream = ollama.generate(
            model=Config.MODEL_DEFAULT,
            prompt=answer,
            stream=True
        )

        for chunk in stream:
            token = chunk.get("response", "")
            if token:
                yield token

    return StreamingResponse(event_stream(), media_type="text/plain")