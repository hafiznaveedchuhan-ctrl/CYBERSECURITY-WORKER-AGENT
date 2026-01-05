"""FastAPI middleware for request processing."""

import time
from uuid import uuid4
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Add unique request ID and trace ID to each request."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate or extract request/trace IDs
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        trace_id = request.headers.get("X-Trace-ID", str(uuid4()))

        # Add to request state for access in handlers
        request.state.request_id = request_id
        request.state.trace_id = trace_id

        # Bind to structlog context
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            trace_id=trace_id,
        )

        # Process request
        response = await call_next(request)

        # Add IDs to response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id

        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """Log request timing information."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000  # Convert to ms

        # Add timing header
        response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"

        # Log request
        logger.info(
            "Request processed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time_ms=round(process_time, 2),
        )

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client identifier (IP or user ID if authenticated)
        client_id = request.client.host if request.client else "unknown"

        # Check if user is authenticated and use user ID instead
        if hasattr(request.state, "user") and request.state.user:
            client_id = f"user:{request.state.user.id}"

        current_time = time.time()
        window_start = current_time - 60  # 1 minute window

        # Clean old requests
        if client_id in self.requests:
            self.requests[client_id] = [
                t for t in self.requests[client_id] if t > window_start
            ]
        else:
            self.requests[client_id] = []

        # Check rate limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            logger.warning("Rate limit exceeded", client_id=client_id)
            return Response(
                content='{"detail": "Rate limit exceeded. Try again later."}',
                status_code=429,
                media_type="application/json",
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                },
            )

        # Record request
        self.requests[client_id].append(current_time)

        response = await call_next(request)

        # Add rate limit headers
        remaining = self.requests_per_minute - len(self.requests[client_id])
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))

        return response
