import os
import uuid
import faiss
import ollama
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from vectorstore import VectorStore
from rag import index_document, answer_query
from rag_chat import answer_chat
from rag_evaluator import evaluate_answer
from extractor import extract_text
from chunking import chunk_text
from embeddings import embed_text
from config import Config

app = FastAPI()
vs = VectorStore(dim=768)
sessions = {}

class IndexRequest(BaseModel):
    doc: str

@app.post("/index")
def index_route(body: IndexRequest):
    index_document(body.doc)
    return {"status": "indexed"}

class QueryRequest(BaseModel):
    question: str
    model: str = Config.MODEL_DEFAULT
    temperature: float = Config.TEMPERATURE_DEFAULT
    top_p: float = Config.TOP_P_DEFAULT
    top_k: int = Config.TOP_K_DEFAULT

@app.post("/query")
def query_route(body: QueryRequest):
    answer, sources = answer_query(body.question, model=body.model)
    evaluation = evaluate_answer(answer, sources)

    return {
        "answer": answer,
        "sources": sources,
        "evaluation": evaluation
    }

@app.post("/upload")
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

@app.get("/documents")
def list_documents():
    docs = {}
    for entry in vs.meta:
        doc_id = entry["doc_id"]
        docs.setdefault(doc_id, 0)
        docs[doc_id] += 1

    return docs

@app.delete("/documents/{doc_id}")
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

@app.post("/stream")
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

class ChatRequest(BaseModel):
    session_id: str
    message: str
    model: str = Config.MODEL_DEFAULT
    temperature: float = 0.2

@app.post("/chat")
def chat(body: ChatRequest):

    # 1. Create session if not exists
    if body.session_id not in sessions:
        sessions[body.session_id] = []

    # 2. Append user message
    sessions[body.session_id].append(f"user: {body.message}")

    # 3. Build memory context
    history_text = "\n".join(sessions[body.session_id])

    # 4. Use RAG + memory
    answer, sources = answer_chat(
        body.message,
        history_text,
        model=body.model,
        temperature=body.temperature
    )

    # 5. Save assistant response
    sessions[body.session_id].append(f"assistant: {answer}")

    return {
        "answer": answer,
        "sources": sources,
        "session_messages": sessions[body.session_id]
    }
