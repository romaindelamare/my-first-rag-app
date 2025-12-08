import os
import uuid
from fastapi import APIRouter, File, UploadFile
from app.ingestion.extractor import extract_text
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_text
from app.core.store import vs

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # generate ID
    doc_id = str(uuid.uuid4())

    # save file
    filepath = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    # extract text
    text = extract_text(filepath)

    # chunk text
    chunks = chunk_text(text)

    # embed and store
    for chunk in chunks:
        emb = embed_text(chunk["text"])
        vs.add(emb, chunk)

    vs.save()

    return {
        "status": "indexed",
        "chunks": len(chunks),
        "filename": file.filename,
        "doc_id": doc_id
    }

@router.get("/documents")
def list_documents():
    results = {}

    for entry in vs.meta:
        doc_id = entry["doc_id"]
        if doc_id not in results:
            results[doc_id] = 0
        results[doc_id] += 1

    return results

@router.get("/documents/{doc_id}")
def get_document_chunks(doc_id: str):
    chunks = [entry for entry in vs.meta if entry["doc_id"] == doc_id]

    if not chunks:
        return {"error": "Document not found"}

    return {
        "doc_id": doc_id,
        "chunks": chunks
    }

@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str):
    new_meta = []
    new_vectors = []

    # Filter out chunks from that document
    for idx, entry in enumerate(vs.meta):
        if entry["doc_id"] != doc_id:
            new_meta.append(entry)
            new_vectors.append(vs.index.reconstruct(idx))

    if len(new_meta) == len(vs.meta):
        return {"error": "Document not found"}

    # Rebuild FAISS index
    import numpy as np
    import faiss

    vs.meta = new_meta
    vs.index = faiss.IndexFlatL2(vs.dim)

    if new_vectors:
        vs.index.add(np.array(new_vectors).astype("float32"))

    vs.save()

    return {"status": "deleted", "doc_id": doc_id}

@router.post("/documents/{doc_id}/reindex")
def reindex_document(doc_id: str):
    delete_document(doc_id)
    return {"status": "ready_for_upload", "doc_id": doc_id}