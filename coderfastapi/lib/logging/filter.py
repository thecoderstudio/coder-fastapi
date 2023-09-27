import copy
import logging

from google.cloud.logging_v2.handlers import (
    CloudLoggingFilter as GoogleCloudLoggingFilter,
)

from coderfastapi.lib.logging.context import cloud_trace_context, http_request_context


class CloudLoggingFilter(GoogleCloudLoggingFilter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.http_request = http_request_context.get()

        trace_id, span_id = cloud_trace_context.get()
        if trace_id:
            record = self._add_trace_data(record, trace_id, span_id)

        super().filter(record)
        return True

    def _add_trace_data(
        self,
        record: logging.LogRecord,
        trace_id: str,
        span_id: str,
    ) -> logging.LogRecord:
        record = copy.copy(record)
        record.trace = f"projects/{self.project}/traces/{trace_id}"
        record.span_id = span_id
        return record
