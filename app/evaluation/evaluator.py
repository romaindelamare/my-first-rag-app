from typing import Dict, List
import re

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def fact_coverage(text: str, expected_facts: List[str]) -> Dict[str, bool]:
    text_norm = normalize(text)
    return {
        fact: normalize(fact) in text_norm
        for fact in expected_facts
    }

def evaluate_retrieval(chunks: List[Dict], expected_doc_ids: List[str]) -> Dict:
    retrieved_doc_ids = {c["doc_id"] for c in chunks}

    return {
        "expected_docs": expected_doc_ids,
        "retrieved_docs": list(retrieved_doc_ids),
        "missing_docs": [
            d for d in expected_doc_ids if d not in retrieved_doc_ids
        ],
        "success": all(d in retrieved_doc_ids for d in expected_doc_ids),
    }

def evaluate_answer(
    answer: str,
    retrieved_chunks: List[Dict],
    expected_facts: List[str],
) -> Dict:
    answer_fact_hits = fact_coverage(answer, expected_facts)

    combined_chunks = "\n".join(c["text"] for c in retrieved_chunks)
    chunk_fact_hits = fact_coverage(combined_chunks, expected_facts)

    return {
        "answer_fact_hits": answer_fact_hits,
        "chunk_fact_hits": chunk_fact_hits,
        "answer_completeness": sum(answer_fact_hits.values()) / max(len(expected_facts), 1),
        "retrieval_coverage": sum(chunk_fact_hits.values()) / max(len(expected_facts), 1),
    }
