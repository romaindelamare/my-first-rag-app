import os
import uuid
import faiss
from fastapi import APIRouter, File, UploadFile
import numpy as np
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
    for c in chunks:
        emb = embed_text(c)
        vs.add(emb, c, doc_id)

    vs.save()

    return {
        "status": "indexed",
        "chunks": len(chunks),
        "filename": file.filename,
        "doc_id": doc_id
    }

@router.get("/documents")
def list_documents():
    docs = {}
    for entry in vs.meta:
        doc_id = entry["doc_id"]
        docs.setdefault(doc_id, 0)
        docs[doc_id] += 1

    return docs

@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str):
    # filter out chunks from this document
    new_meta = []
    new_embeddings = []

    # rebuild data
    for i, entry in enumerate(vs.meta):
        if entry["doc_id"] != doc_id:
            new_meta.append(entry)
            new_embeddings.append(vs.index.reconstruct(i))

    # create a fresh index
    new_index = faiss.IndexFlatL2(vs.dim)
    if new_embeddings:
        new_index.add(np.array(new_embeddings).astype("float32"))

    vs.meta = new_meta
    vs.index = new_index
    vs.save()

    return {"status": "deleted", "doc_id": doc_id}