import contextvars

CLOUD_TRACE_CONTEXT_NAME = "cloud_trace_context"
HTTP_REQUEST_CONTEXT_NAME = "http_request_context"


class CloudTraceContext(contextvars.ContextVar):
    def __init__(self, name) -> None:
        super().__init__(name, default="")

    def set(self, x_cloud_trace_context: str) -> None:
        self.set(x_cloud_trace_context)


cloud_trace_context = CloudTraceContext(CLOUD_TRACE_CONTEXT_NAME)
http_request_context = contextvars.ContextVar(HTTP_REQUEST_CONTEXT_NAME, default={})
