def compute_confidence(
    evaluation: dict,
    semantic: dict,
    hallucination: dict,
    citations: list,
    safety: dict
) -> dict:
    score = 100

    # Hard penalties
    if not safety["safe"]:
        return {"score": 0, "level": "blocked"}

    if hallucination["score"] < 0.25:
        return {"score": 15, "level": "very_low"}

    # Semantic confidence
    if semantic["confidence"] == "low":
        score -= 25
    elif semantic["confidence"] == "medium":
        score -= 10

    # Keyword overlap
    if evaluation["confidence"] == "low":
        score -= 20
    elif evaluation["confidence"] == "medium":
        score -= 10

    # Citations
    unsupported = [c for c in citations if c["source_doc_id"] is None]
    if len(unsupported) > 1:
        score -= 15

    score = max(0, min(100, score))

    level = (
        "high" if score >= 80 else
        "medium" if score >= 55 else
        "low"
    )

    return {
        "score": score,
        "level": level
    }
