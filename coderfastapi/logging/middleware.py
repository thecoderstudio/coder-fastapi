from collections.abc import Callable
from contextvars import ContextVar

from starlette.requests import Request
from starlette.types import ASGIApp

from coderfastapi.lib.validation.schemas.request import HTTPRequestSchema
from coderfastapi.logging.context import CloudTraceContext

TRACE_HEADER = "x-cloud-trace-context"
INTERNAL_SERVER_ERROR = "Internal Server Error"


class LoggingMiddleware:
    app: ASGIApp
    cloud_trace_context: CloudTraceContext
    http_request_context: ContextVar

    def __init__(
        self,
        app: ASGIApp,
        cloud_trace_context: CloudTraceContext,
        http_request_context: ContextVar,
        *args,
        **kwargs,
    ) -> None:
        self.app = app
        self.cloud_trace_context = cloud_trace_context
        self.http_request_context = http_request_context

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive=receive)
        if TRACE_HEADER in request.headers:
            self.cloud_trace_context.set(request.headers[TRACE_HEADER])

        self.http_request_context.set(HTTPRequestSchema.from_request(request))

        await self.app(scope, receive, send)
