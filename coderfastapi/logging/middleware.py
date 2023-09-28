from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from coderfastapi.lib.validation.schemas.request import HTTPRequestSchema
from coderfastapi.logging.context import CloudTraceContext

TRACE_HEADER = "x-cloud-trace-context"


class LoggingMiddleware(BaseHTTPMiddleware):
    cloud_trace_context: CloudTraceContext
    http_request_context: ContextVar

    def __init__(
        self,
        cloud_trace_context: CloudTraceContext,
        http_request_context: ContextVar,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.cloud_trace_context = cloud_trace_context
        self.http_request_context = http_request_context

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if TRACE_HEADER in request.headers:
            self.cloud_trace_context.set(request.headers[TRACE_HEADER])

        self.http_request_context.set(HTTPRequestSchema.from_request(request))

        return await call_next(request)
