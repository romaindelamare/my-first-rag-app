from fastapi import APIRouter
from app.evaluation.eval_dataset import EVAL_DATASET
from app.evaluation.evaluator import (
    evaluate_answer,
    evaluate_retrieval,
)
from app.rag.rag import answer_query

router = APIRouter(prefix="/evaluation", tags=["evaluation"])

@router.post("/run")
def run_evaluation():
    results = []

    for sample in EVAL_DATASET:
        question = sample["question"]

        # Run RAG
        answer, sources = answer_query(question)

        # Evaluation
        retrieval_eval = evaluate_retrieval(
            sources, sample["expected_doc_ids"]
        )

        answer_eval = evaluate_answer(
            answer,
            sources,
            sample["expected_facts"]
        )

        results.append({
            "id": sample["id"],
            "question": question,
            "answer": answer,
            "sources": sources,
            "retrieval": retrieval_eval,
            "answer_eval": answer_eval,
        })

    return {
        "total": len(results),
        "results": results
    }
