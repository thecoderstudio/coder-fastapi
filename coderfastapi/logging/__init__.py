import os

from google.cloud.logging import Client
from google.cloud.logging_v2.handlers import setup_logging

from coderfastapi.logging.context import cloud_trace_context, http_request_context
from coderfastapi.logging.filter import CloudLoggingFilter
from coderfastapi.logging.middleware import LoggingMiddleware  # noqa

CLOUD_RUN_INDICATOR = "K_SERVICE"


def setup_cloud_logging() -> None:
    if not _is_running_in_cloud_environment():
        return
    client = Client()
    handler = client.get_default_handler()
    handler.filters = [
        CloudLoggingFilter(
            cloud_trace_context,
            http_request_context,
            project=client.project,
        )
    ]
    setup_logging(handler)


def _is_running_in_cloud_environment() -> bool:
    return bool(os.environ.get(CLOUD_RUN_INDICATOR))
