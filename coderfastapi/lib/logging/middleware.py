import sys

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from coderfastapi.lib.logging.context import cloud_trace_context, http_request_context


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if "x-cloud-trace-context" in request.headers:
            cloud_trace_context.set(request.headers["x-cloud-trace-context"])

        http_request = {
            "requestMethod": request.method,
            "requestUrl": request.url.path,
            "requestSize": sys.getsizeof(request),
            "remoteIp": request.client.host,
            "protocol": request.url.scheme,
        }

        if "referrer" in request.headers:
            http_request["referrer"] = request.headers["referrer"]

        if "user-agent" in request.headers:
            http_request["userAgent"] = request.headers["user-agent"]

        http_request_context.set(http_request)

        return await call_next(request)
