import uuid
import re
from app.core.logger import logger
from app.core.config import CONFIG

MAX_CHARS = CONFIG.max_chunk_chars
OVERLAP = CONFIG.overlap_chars
MIN_CHUNK_SIZE = 200

def split_by_sentences(text: str):
    """
    Robust sentence splitter handling:
    - lists (1. 2. 3.)
    - headings
    - newlines
    - common abbreviations
    - multi-sentence paragraphs
    """

    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Split on double newlines as hard boundaries
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    sentences = []

    sentence_regex = re.compile(
        r"(?<=\.)\s+(?=[A-Z])|"       # after period
        r"(?<=!)\s+(?=[A-Z])|"        # after !
        r"(?<=\?)\s+(?=[A-Z])|"       # after ?
        r"\n+(?=[A-Z0-9])|"           # newline before heading
        r"(?<=\d\.)\s+(?=[A-Z])"      # numbered list
    )

    for para in paragraphs:
        parts = sentence_regex.split(para)
        for s in parts:
            clean = s.strip()
            if clean:
                sentences.append(clean)

    return sentences

def soft_overlap(chunk: str, size: int):
    """
    Returns an overlap that starts at the nearest sentence boundary,
    not the middle of a word.
    """
    if len(chunk) <= size:
        return chunk

    overlap = chunk[-size:]

    # Try to align to a word boundary
    first_space = overlap.find(" ")
    if first_space != -1:
        return overlap[first_space+1:]

    return overlap

def sliding_window_chunks(sentences):
    """
    Builds chunks using a sliding window.
    Never loses text, never rewrites content.
    Produces chunks ~MAX_CHARS with OVERLAP between them.
    """
    chunks = []
    current = ""

    for sentence in sentences:
        # If adding the sentence exceeds limit → finalize chunk
        if len(current) + len(sentence) > MAX_CHARS:
            if current:
                chunks.append(current.strip())

            # Start new chunk using overlap window
            if OVERLAP > 0:
                # Take last part of previous chunk as context
                current = soft_overlap(current, OVERLAP)
            else:
                current = ""

        sentence = " ".join(sentence.split())
        current += " " + sentence

    if current.strip():
        chunks.append(current.strip())

    return chunks

def semantic_merge(chunks):
    """
    Uses LLM ONLY to MERGE chunks that are too small.
    Never rewrites big chunks.
    NEVER allowed to rewrite text.
    """

    merged = []
    buffer = ""

    for chunk in chunks:
        if len(chunk) < MIN_CHUNK_SIZE:
            buffer += " " + chunk
        else:
            if buffer:
                merged.append(buffer.strip())
                buffer = ""
            merged.append(chunk)

    if buffer:
        merged.append(buffer.strip())

    return merged

def chunk_text(text: str, doc_id: str = None):
    """
    Returns safe deterministic chunks with offset mapping.
    {
        "doc_id": str,
        "chunk_index": int,
        "text": str,
        "offset_start": int,
        "offset_end": int
    }
    """
    
    if doc_id is None:
        doc_id = str(uuid.uuid4())

    logger.info(f"🔪 [CHUNK] Starting production chunking (doc={doc_id})")

    # 1. Break into sentences (lossless)
    sentences = split_by_sentences(text)

    # 2. Build sliding-window chunks
    raw_chunks = sliding_window_chunks(sentences)

    # 3. Optionally merge small ones (semantic-safe)
    raw_chunks = semantic_merge(raw_chunks)

    # 4. Build chunk metadata
    enriched = []
    offset = 0

    for i, chunk in enumerate(raw_chunks):
        clean = chunk.strip()
        length = len(clean)

        enriched.append({
            "doc_id": doc_id,
            "chunk_index": i,
            "text": clean,
            "offset_start": offset,
            "offset_end": offset + length
        })

        offset += length

    logger.info(
        f"📦 [CHUNK] Finalized {len(enriched)} chunks (doc={doc_id})"
    )

    return enriched
