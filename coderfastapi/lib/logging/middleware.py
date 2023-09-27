from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from coderfastapi.lib.logging.context import cloud_trace_context, http_request_context
from coderfastapi.lib.validation.schemas.request import HTTPRequestSchema

TRACE_HEADER = "x-cloud-trace-context"


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if TRACE_HEADER in request.headers:
            cloud_trace_context.set(request.headers[TRACE_HEADER])

        http_request_context.set(HTTPRequestSchema.from_request(request))

        return await call_next(request)
