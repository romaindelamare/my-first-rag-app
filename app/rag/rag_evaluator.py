def evaluate_answer(answer: str, sources: list) -> dict:
    """
    Simple evaluator for RAG:
    - builds a combined string of all chunk texts
    - checks if answer words appear in context
    - returns a minimal structured evaluation

    sources is a list of dicts:
        { "doc_id": "...", "text": "..." }
    """

    source_texts = [entry["text"] for entry in sources]

    src_text = "\n\n".join(source_texts)

    overlap = sum(1 for word in answer.split() if word.lower() in src_text.lower())

    return {
        "overlap_score": overlap,
        "source_count": len(sources),
        "confidence": "low" if overlap < 3 else "medium" if overlap < 10 else "high"
    }
