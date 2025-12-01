from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import ollama
from app.config import Config
from app.models.query import QueryRequest
from app.rag.rag import answer_query
from app.rag.rag_evaluator import align_citations, detect_hallucination, evaluate_answer, guardrail_decision, safety_check, semantic_score

router = APIRouter()

@router.post("/query")
def query_route(body: QueryRequest):
    answer, sources = answer_query(body.question, model=body.model)
    evaluation = evaluate_answer(answer, sources)
    hallucination = detect_hallucination(answer, sources)
    semantic = semantic_score(answer, sources)
    citations = align_citations(answer, sources)
    safety = safety_check(answer)
    decision = guardrail_decision(answer, evaluation, hallucination, semantic, safety, citations)

    return {
        "answer": answer,
        "sources": sources,
        "evaluation": evaluation,
        "hallucination": hallucination,
        "semantic": semantic,
        "citations": citations,
        "safety_check": safety,
        "decision": decision
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