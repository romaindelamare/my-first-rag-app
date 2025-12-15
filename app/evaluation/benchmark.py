from typing import List, Dict
from app.evaluation.eval_dataset import EVAL_DATASET
from app.evaluation.evaluator import (
    evaluate_answer,
    evaluate_retrieval,
)
from app.rag.rag import answer_query

BENCHMARK_CONFIGS = [
    {"name": "top_k_3", "top_k": 3},
    {"name": "top_k_5", "top_k": 5},
    {"name": "top_k_8", "top_k": 8},
]


def run_benchmark() -> List[Dict]:
    results = []

    for config in BENCHMARK_CONFIGS:
        config_name = config["name"]
        top_k = config["top_k"]

        scores = []

        for sample in EVAL_DATASET:
            answer, sources = answer_query(
                question=sample["question"],
                top_k=top_k
            )

            retrieval = evaluate_retrieval(
                sources, sample["expected_doc_ids"]
            )

            answer_eval = evaluate_answer(
                answer,
                sources,
                sample["expected_facts"]
            )

            scores.append({
                "retrieval_success": retrieval["success"],
                "answer_completeness": answer_eval["answer_completeness"],
                "retrieval_coverage": answer_eval["retrieval_coverage"],
            })

        results.append({
            "config": config_name,
            "top_k": top_k,
            "avg_retrieval_success": sum(s["retrieval_success"] for s in scores) / len(scores),
            "avg_answer_completeness": sum(s["answer_completeness"] for s in scores) / len(scores),
            "avg_retrieval_coverage": sum(s["retrieval_coverage"] for s in scores) / len(scores),
        })

    return results
