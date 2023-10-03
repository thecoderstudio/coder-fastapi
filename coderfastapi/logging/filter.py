import json
import logging
from contextvars import ContextVar

from google.cloud.logging_v2.handlers import (
    CloudLoggingFilter as GoogleCloudLoggingFilter,
)

from coderfastapi.logging.context import CloudTraceContext


class CloudLoggingFilter(GoogleCloudLoggingFilter):
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

    def filter(self, record: logging.LogRecord) -> bool:
        trace_id, span_id = self.cloud_trace_context.get()
        if trace_id:
            record = self._add_trace_data(record, trace_id, span_id)

        if http_request := self.http_request_context.get():
            record.http_request = json.loads(http_request.json(by_alias=True))

        super().filter(record)
        return True

    def _add_trace_data(
        self,
        record: logging.LogRecord,
        trace_id: str,
        span_id: str,
    ) -> logging.LogRecord:
        record.trace = f"projects/{self.project}/traces/{trace_id}"
        record.span_id = span_id
        return record
