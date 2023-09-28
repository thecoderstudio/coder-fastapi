from unittest.mock import patch

from coderfastapi.lib.logging import setup_cloud_logging
from coderfastapi.lib.logging.context import cloud_trace_context, http_request_context


def test_setup_cloud_logging_in_cloud_environment():
    project = "coderfastapi"
    with (
        patch("coderfastapi.lib.logging.os.environ.get", return_value=True),
        patch("coderfastapi.lib.logging.setup_logging") as setup_logging_mock,
        patch("coderfastapi.lib.logging.Client") as client_constructor_mock,
    ):
        client_mock = client_constructor_mock()
        client_mock.project = project
        handler_mock = client_mock.get_default_handler()
        handler_mock.filters = []
        setup_cloud_logging()

    setup_logging_mock.assert_called_once_with(handler_mock)
    filter_ = handler_mock.filters[0]
    assert filter_.cloud_trace_context == cloud_trace_context
    assert filter_.http_request_context == http_request_context
    assert filter_.project == project


def test_setup_cloud_logging_outside_of_cloud_environment():
    with (
        patch("coderfastapi.lib.logging.os.environ.get", return_value=False),
        patch("coderfastapi.lib.logging.setup_logging") as setup_logging_mock,
    ):
        setup_cloud_logging()

    setup_logging_mock.assert_not_called()
