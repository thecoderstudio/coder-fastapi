from collections.abc import Callable
from contextvars import ContextVar
from http import HTTPStatus

from fastapi.logger import logger
from starlette.requests import Request
from starlette.responses import JSONResponse
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
        if not self._is_http_request(scope):
            return await self.app(scope, receive, send)

        self._set_context(Request(scope, receive=receive))
        await self._call_upstream(scope, receive, send)

    @staticmethod
    def _is_http_request(scope: dict) -> bool:
        return bool(scope["type"] == "http")

    def _set_context(self, request: Request) -> None:
        if TRACE_HEADER in request.headers:
            self.cloud_trace_context.set(request.headers[TRACE_HEADER])

        self.http_request_context.set(HTTPRequestSchema.from_request(request))

    async def _call_upstream(
        self,
        scope: dict,
        receive: Callable,
        send: Callable,
    ) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception:
            logger.exception(INTERNAL_SERVER_ERROR)
            response = JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content=INTERNAL_SERVER_ERROR,
            )
            await response(scope, receive, send)
