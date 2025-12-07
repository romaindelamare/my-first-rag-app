from fastapi.responses import JSONResponse
from fastapi.requests import Request
from app.core.errors import RagError


async def rag_error_handler(request: Request, exc: RagError):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
            "type": "rag_error"
        }
    )