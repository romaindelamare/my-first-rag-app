import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("api")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()

        path = request.url.path
        method = request.method

        try:
            response = await call_next(request)
            status = response.status_code
        except Exception as e:
            status = 500
            logger.exception(f"ERROR during request {method} {path}: {e}")
            raise

        duration = (time.time() - start) * 1000

        logger.info(f"{method} {path} - {status} - {duration:.2f}ms")

        return response
