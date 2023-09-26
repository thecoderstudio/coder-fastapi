import os

import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingFilter

CLOUD_RUN_INDICATOR = "K_SERVICE"


def setup_cloud_logging():
    if not _is_running_in_cloud_environment():
        return
    client = google.cloud.logging.Client()
    client.setup_logging()


def _is_running_in_cloud_environment() -> bool:
    return bool(os.environ.get(CLOUD_RUN_INDICATOR))
