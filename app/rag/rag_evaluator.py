from app.rag.embeddings import embed_text
import numpy as np

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

def semantic_score(answer: str, sources: list) -> dict:
    """
    Computes semantic similarity between the answer and each retrieved chunk.

    Returns:
        {
            "chunk_scores": [0.88, 0.53, ...],
            "average": 0.76,
            "max": 0.88,
            "min": 0.52,
            "confidence": "high" | "medium" | "low"
        }
    """

    # Embed the answer
    ans_emb = embed_text(answer)

    chunk_scores = []

    for entry in sources:
        text = entry["text"]
        src_emb = embed_text(text)

        # Cosine similarity
        dot = float(np.dot(ans_emb, src_emb))
        denom = float(np.linalg.norm(ans_emb) * np.linalg.norm(src_emb))
        cos = dot / denom if denom != 0 else 0.0

        chunk_scores.append(float(cos))

    if not chunk_scores:
        return {
            "chunk_scores": [],
            "average": 0.0,
            "max": 0.0,
            "min": 0.0,
            "confidence": "low"
        }

    avg = sum(chunk_scores) / len(chunk_scores)
    mx = max(chunk_scores)
    mn = min(chunk_scores)

    # Confidence heuristics
    if avg > 0.75:
        conf = "high"
    elif avg > 0.45:
        conf = "medium"
    else:
        conf = "low"

    return {
        "chunk_scores": chunk_scores,  # list of floats
        "average": avg,
        "max": mx,
        "min": mn,
        "confidence": conf
    }

def detect_hallucination(answer: str, sources: list, threshold: float = 0.55) -> dict:
    """
    Detects hallucinations by checking semantic similarity
    between the answer and the combined source text.

    Returns:
        {
            "score": float,
            "hallucinated": bool
        }
    """

    # Combine all chunk texts
    source_texts = [entry["text"] for entry in sources]
    combined_source = "\n".join(source_texts)

    # Embed both
    answer_emb = embed_text(answer)
    source_emb = embed_text(combined_source)

    # Compute cosine similarity
    cos = np.dot(answer_emb, source_emb) / (
        np.linalg.norm(answer_emb) * np.linalg.norm(source_emb)
    )

    return {
        "score": float(cos),
        "hallucinated": bool(cos < threshold)
    }

def align_citations(answer: str, sources: list, threshold: float = 0.45) -> list:
    """
    Aligns each sentence of the answer with the most relevant source chunk.

    Returns a list of:
    [
        {
            "sentence": "...",
            "source_doc_id": "...",
            "score": 0.87
        }
    ]
    """

    import re

    # Split answer into sentences
    sentences = re.split(r'(?<=[.!?])\s+', answer.strip())

    citations = []

    for sent in sentences:
        if not sent.strip():
            continue

        sent_emb = embed_text(sent)
        best_score = -1
        best_source = None

        for entry in sources:
            text = entry["text"]
            src_emb = embed_text(text)

            dot = float(np.dot(sent_emb, src_emb))
            denom = float(np.linalg.norm(sent_emb) * np.linalg.norm(src_emb))
            cos = dot / denom if denom != 0 else 0.0

            if cos > best_score:
                best_score = cos
                best_source = entry

        citations.append({
            "sentence": sent,
            "source_doc_id": best_source["doc_id"] if best_score >= threshold else None,
            "score": float(best_score)
        })

    return citations

def safety_check(answer: str, threshold: float = 0.65) -> dict:
    """
    Detects unsafe content using semantic similarity
    to reference unsafe category embeddings.
    
    Returns:
        {
            "safe": bool,
            "category": str,
            "score": float
        }
    """

    unsafe_categories = {
        "hate": "hate speech, racial slurs, extremist insults",
        "toxicity": "offensive language, insults, harassment, swear words",
        "self-harm": "self-harm instructions, suicide encouragement",
        "sexual": "sexual content, explicit descriptions",
        "violence": "violent acts, threats, harm instructions",
        "weapons": "weapon creation, bomb making, harmful tools"
    }

    answer_emb = embed_text(answer)

    best_cat = "safe"
    best_score = 0.0

    for category, desc in unsafe_categories.items():
        ref_emb = embed_text(desc)

        dot = float(np.dot(answer_emb, ref_emb))
        denom = float(np.linalg.norm(answer_emb) * np.linalg.norm(ref_emb))
        cos = dot / denom if denom != 0 else 0.0

        if cos > best_score:
            best_score = cos
            best_cat = category

    return {
        "safe": best_score < threshold,
        "category": None if best_score < threshold else best_cat,
        "score": float(best_score)
    }

def guardrail_decision(answer: str, evaluation: dict, hallucination: dict,
                       semantic: dict, safety: dict, citations: list) -> dict:
    """
    Final decision engine combining:
    - safety filter
    - hallucination detection
    - semantic similarity
    - lexical evaluation (keyword overlap)
    - citation alignment
    """

    # 1. HARD BLOCK: unsafe content
    if not safety["safe"]:
        return {
            "allowed": False,
            "reason": f"unsafe_content:{safety['category']}",
            "final_answer": "⚠️ I cannot answer because the content is unsafe."
        }

    # 2. HARD BLOCK: evaluation indicates NO overlap at all
    if evaluation["overlap_score"] == 0:
        return {
            "allowed": False,
            "reason": "no_evidence_in_context",
            "final_answer": "⚠️ I don’t know based on the provided context."
        }

    # 3. HARD BLOCK: hallucination extremely low
    if hallucination["score"] < 0.25:
        return {
            "allowed": False,
            "reason": "severe_hallucination",
            "final_answer": "⚠️ I don’t know based on the provided context."
        }

    # 4. SOFT WARNING: possible hallucination (moderate)
    if hallucination["hallucinated"]:
        return {
            "allowed": True,
            "reason": "possible_hallucination",
            "final_answer": "⚠️ This answer may be incomplete or uncertain.\n\n" + answer
        }

    # 5. SOFT WARNING: low semantic similarity
    if semantic["confidence"] == "low":
        return {
            "allowed": True,
            "reason": "low_semantic_confidence",
            "final_answer": "⚠️ This answer may not fully match the context.\n\n" + answer
        }

    # 6. SOFT WARNING: low evaluation confidence
    if evaluation["confidence"] == "low":
        return {
            "allowed": True,
            "reason": "low_keyword_overlap",
            "final_answer": "⚠️ This answer contains little lexical evidence from the context.\n\n" + answer
        }

    # 7. SOFT WARNING: poor citation alignment (too many unsupported sentences)
    unsupported = [c for c in citations if c["source_doc_id"] is None]
    if len(unsupported) > 1:
        return {
            "allowed": True,
            "reason": "weak_citations",
            "final_answer": "⚠️ Some parts of the answer could not be validated.\n\n" + answer
        }

    # 8. PASS (everything looks good)
    return {
        "allowed": True,
        "reason": None,
        "final_answer": answer
    }

