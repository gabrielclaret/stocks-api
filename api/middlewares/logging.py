from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.responses import Response
from starlette_context import context

from api.utils.request_id import get_request_id


class RequestIdLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for CacheControl."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Middleware Dispatcher."""
        original_id = None  # Should be request.headers.get("X-Request-ID")
        context.request_id = get_request_id(original_id)

        response = await call_next(request)

        return response
