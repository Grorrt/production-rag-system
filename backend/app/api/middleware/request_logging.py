"""
Structured request logging middleware using Structlog.
Logs all incoming requests with timing, status, and user info.
"""

import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs every request with structured data.
    Includes request ID, method, path, status, duration, and user.
    """

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        logger = structlog.get_logger()
        start_time = time.time()

        log = logger.bind(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        log.info("request_started")

        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000

            log.info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )

            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as exc:
            duration_ms = (time.time() - start_time) * 1000
            log.error(
                "request_failed",
                error=str(exc),
                duration_ms=round(duration_ms, 2),
            )
            raise
