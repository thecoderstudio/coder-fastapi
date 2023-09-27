import contextvars
import re

CLOUD_TRACE_CONTEXT_NAME = "cloud_trace_context"
HTTP_REQUEST_CONTEXT_NAME = "http_request_context"


class CloudTraceContext(contextvars.ContextVar):
    def __init__(self, name) -> None:
        super().__init__(name, default=(None, None))

    def set(self, x_cloud_trace_context: str) -> None:
        split_header = x_cloud_trace_context.split("/", 1)
        trace_id = split_header[0]
        span_id = re.findall(r"^\w+", split_header[1])[0]

        self.set((trace_id, span_id))


cloud_trace_context = CloudTraceContext(CLOUD_TRACE_CONTEXT_NAME)
http_request_context = contextvars.ContextVar(HTTP_REQUEST_CONTEXT_NAME, default={})
