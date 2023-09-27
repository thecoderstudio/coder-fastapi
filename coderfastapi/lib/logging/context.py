import re
from contextvars import ContextVar

CLOUD_TRACE_CONTEXT_NAME = "cloud_trace_context"
HTTP_REQUEST_CONTEXT_NAME = "http_request_context"


class CloudTraceContext:
    _context_var: ContextVar

    def __init__(self, name: str) -> None:
        self._context_var = ContextVar(name, default=(None, None))

    def get(self) -> tuple[str | None, str | None]:
        return self._context_var.get()

    def set(self, x_cloud_trace_context: str) -> None:
        split_header = x_cloud_trace_context.split("/", 1)
        trace_id = split_header[0]
        span_id = re.findall(r"^\w+", split_header[1])[0]

        self._context_var.set((trace_id, span_id))

    @property
    def name(self) -> str:
        return self._context_var.name


cloud_trace_context = CloudTraceContext(CLOUD_TRACE_CONTEXT_NAME)
http_request_context = ContextVar(HTTP_REQUEST_CONTEXT_NAME, default=None)
