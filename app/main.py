from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_query import router as query_router
from app.api.routes_chat import router as chat_router
from app.api.routes_docs import router as docs_router
from app.api.routes_debug import router as debug_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="My First RAG App",
        description="A fully local RAG system using FastAPI + Ollama + FAISS.",
        version="1.0.0"
    )

    # ------------------------------------------------------
    # CORS
    # ------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],      # allow all for development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------
    # Routers
    # ------------------------------------------------------
    app.include_router(query_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(docs_router, prefix="/api")
    app.include_router(debug_router, prefix="/api")

    return app

app = create_app()
