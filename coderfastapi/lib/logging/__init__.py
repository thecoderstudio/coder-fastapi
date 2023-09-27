import os

import google.cloud.logging
from google.cloud.logging_v2.handlers import setup_logging

from coderfastapi.lib.logging.context import cloud_trace_context, http_request_context
from coderfastapi.lib.logging.filter import CloudLoggingFilter

CLOUD_RUN_INDICATOR = "K_SERVICE"


def setup_cloud_logging():
    if not _is_running_in_cloud_environment():
        return
    client = google.cloud.logging.Client()
    handler = client.get_default_handler()
    handler.filters = []
    handler.addFilter(
        CloudLoggingFilter(
            cloud_trace_context,
            http_request_context,
            project=client.project,
        )
    )
    setup_logging(handler)


def _is_running_in_cloud_environment() -> bool:
    return bool(os.environ.get(CLOUD_RUN_INDICATOR))
