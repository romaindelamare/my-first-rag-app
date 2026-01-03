from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import ollama
from app.core.config import CONFIG
from app.models.query import QueryRequest
from app.rag.rag import answer_query

router = APIRouter()

@router.post("/query")
def query_route(body: QueryRequest):
    return answer_query(
        body.question,
        model=body.model,
        temperature=body.temperature,
        top_p=body.top_p,
        top_k=body.top_k,
    )

@router.post("/stream")
def stream_answer(body: QueryRequest):

    async def event_stream():
        # get the final answer + top chunks
        answer, sources = answer_query(body.question)

        # stream the answer token-by-token
        stream = ollama.generate(
            model=CONFIG.llm_model,
            prompt=answer,
            stream=True
        )

        for chunk in stream:
            token = chunk.get("response", "")
            if token:
                yield token

    return StreamingResponse(event_stream(), media_type="text/plain")