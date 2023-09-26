import os

import google.cloud.logging


def setup_cloud_logging():
    if not _is_running_in_cloud_environment():
        return
    client = google.cloud.logging.Client()
    client.setup_logging()


def _is_running_in_cloud_environment() -> bool:
    return bool(os.environ.get("K_SERVICE"))
