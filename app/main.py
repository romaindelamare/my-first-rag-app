from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_middleware import LoggingMiddleware
from app.core.errors import RagError
from app.core.exception_handlers import rag_error_handler
from app.api.routes_query import router as query_router
from app.api.routes_chat import router as chat_router
from app.api.routes_docs import router as docs_router
from app.api.routes_debug import router as debug_router
from app.api.routes_faiss import router as faiss_router
from app.api.routes_evaluation import router as evaluation_router
from app.api.routes_benchmark import router as benchmark_router
from app.core.config import CONFIG
from app.core.logger import logger

def create_app() -> FastAPI:
    app = FastAPI(
        title="My First RAG App",
        description="A fully local RAG system using FastAPI + Ollama + FAISS.",
        version="1.0.0"
    )

    # ------------------------------------------------------
    # Middlewares
    # ------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],      # allow all for development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)

    # ------------------------------------------------------
    # Routers
    # ------------------------------------------------------
    app.include_router(query_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(docs_router, prefix="/api")
    app.include_router(debug_router, prefix="/api")
    app.include_router(faiss_router, prefix="/api")
    app.include_router(evaluation_router, prefix="/api")
    app.include_router(benchmark_router, prefix="/api")

    app.add_exception_handler(RagError, rag_error_handler)

    return app

logger.info(
    "🧩 Loaded RAG config: %s",
    CONFIG.model_dump()
)

app = create_app()